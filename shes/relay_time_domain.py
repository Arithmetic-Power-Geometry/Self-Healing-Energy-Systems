"""Idealized time-domain relay models. Research abstraction, not vendor firmware."""
from dataclasses import dataclass
from math import inf, isfinite, log, exp

@dataclass(frozen=True)
class Segment:
    start: float
    end: float
    current: float

def inverse_time_constant(current, pickup, tds, coefficient=0.14, exponent=0.02):
    if pickup <= 0 or tds <= 0 or coefficient <= 0 or exponent <= 0:
        raise ValueError("positive relay parameters required")
    if current <= pickup:
        return inf
    return coefficient * tds / ((current / pickup) ** exponent - 1)

def validate_trace(segments, horizon):
    if not isfinite(horizon) or horizon < 0:
        raise ValueError("invalid horizon")
    cursor = 0.0
    for seg in segments:
        if not all(isfinite(v) for v in (seg.start, seg.end, seg.current)):
            raise ValueError("nonfinite trace")
        if seg.current < 0 or seg.start != cursor or seg.end <= seg.start or seg.end > horizon:
            raise ValueError("trace must be nonnegative, contiguous and within horizon")
        cursor = seg.end
    if cursor != horizon:
        raise ValueError("trace must cover entire horizon")

def relay_assertion(segments, horizon, pickup, tds, reset="full",
                    reset_rate=0.0, initial_progress=0.0):
    """Integrate progress x'=1/T(I) when above pickup.
    Below pickup: x=0 (full), x'=0 (hold), or x'=-reset_rate (linear).
    Assert when x>=1. Strict pickup and inclusive horizon. This is an
    explicitly stipulated integration model, not a manufacturer standard.
    """
    validate_trace(segments, horizon)
    if reset not in ("full", "hold", "linear"):
        raise ValueError("unsupported reset")
    if not isfinite(reset_rate) or reset_rate < 0:
        raise ValueError("invalid reset rate")
    if not isfinite(initial_progress) or not (0 <= initial_progress < 1):
        raise ValueError("initial progress must be in [0,1)")
    x = initial_progress
    for seg in segments:
        dt = seg.end - seg.start
        if seg.current > pickup:
            T = inverse_time_constant(seg.current, pickup, tds)
            needed = (1-x)*T
            if needed <= dt:
                return seg.start + needed
            x += dt/T
        elif reset == "full":
            x = 0.0
        elif reset == "linear":
            x = max(0.0, x-reset_rate*dt)
    return inf

def definite_time_assertion(segments, horizon, pickup, dwell, reset="full",
                            reset_rate=0.0, initial_progress=0.0):
    if dwell <= 0 or not isfinite(dwell):
        raise ValueError("positive dwell required")
    # Progress normalized by dwell, with same explicitly stipulated reset.
    validate_trace(segments,horizon)
    if reset not in ("full","hold","linear") or reset_rate < 0:
        raise ValueError("invalid reset")
    if not 0 <= initial_progress < 1:
        raise ValueError("invalid initial progress")
    x=initial_progress
    for seg in segments:
        dt=seg.end-seg.start
        if seg.current>pickup:
            needed=(1-x)*dwell
            if needed<=dt: return seg.start+needed
            x+=dt/dwell
        elif reset=="full": x=0.
        elif reset=="linear": x=max(0.,x-reset_rate*dt)
    return inf

def coordinated(primary_assert, backup_assert, primary_breaker, backup_breaker,
                primary_deadline, backup_deadline, margin):
    if any(not isfinite(x) for x in (primary_assert,backup_assert,primary_breaker,
       backup_breaker,primary_deadline,backup_deadline,margin)):
        return False
    if min(primary_breaker,backup_breaker,primary_deadline,backup_deadline,margin)<0:
        raise ValueError("negative delays or deadlines")
    return (primary_assert+primary_breaker<=primary_deadline
        and backup_assert+backup_breaker<=backup_deadline
        and backup_assert-(primary_assert+primary_breaker)>=margin)

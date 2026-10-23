# SHES Prompt 18 — controlled ablation and adversarial stress

## Verified reproducibility
CI SUCCESS: https://github.com/Arithmetic-Power-Geometry/Self-Healing-Energy-Systems/actions/runs/39967939871
Artifact: 12507103429 (shes-p18-ablation-evidence)
17 tests passed; independent scenario replay, confusion, witness and overlap invariants passed.
Same P17 seed 1717 and 90 synthetic cases, 30 each full/hold/linear reset.

## Exact independent rectangular reference (only under P13 fixed-template monotonicity assumptions)
Full model approves 22/90. Ablation results:
component | approvals | false approvals | conservative rejections
frequency | 36 | 14 | 0
primary_deadline | 23 | 1 | 0
backup_deadline | 28 | 6 | 0
coordination_margin | 44 | 22 | 0
timer_memory | 20 | 0 | 2
independent_derating | 25 | 3 | 0
breaker_delay | 22 | 0 | 0

The timer-memory ablation discards progress at every segment boundary, including above pickup, and is an intentionally conservative approximation, not a validated vendor relay. The independent-derating ablation uses only common-diagonal endpoints, not a continuum proof. Omitting breaker delay produced zero observed false approvals in this sample, not a theorem of irrelevance.

## Width stress
Independent gamma intervals [1-w,1] with w 0, .1, .2, .3, .4 produced approvals 40,34,27,24,11. The nonincrease follows nested uncertainty sets under the stipulated model.

## Adversarial evidence
First observed false-approval witnesses, exact case IDs, full component truth vectors, and pairwise overlap counts are archived in the CI JSON. These are not globally minimal parameter witnesses. P13's analytic correlated common-gamma interior counterexample is also replayed and is not to be confused with a finite diagonal scenario oracle.

## Timing
Nine repeated per-method measurements (milliseconds) are archived, with median, min, max, standard deviation and raw values. Runner-specific descriptive variation only; no hypothesis tests or statistical significance claims.

## Scientific novelty and limitations
The meaningful contribution is quantitative attribution of which joint certificate requirements exclude model-level false approvals, in conjunction with P13's qualified theorem and counterexample. This does not establish a new physical relay design or operational microgrid restoration controller. No installed relay, CT, inverter transient, transformer phase transfer, energized restoration, or field verification. Physical restoration certificates: zero.
Full manuscript integration and clean PDF build remain pending.

## Prompt 19
Perform an independent, fail-closed research audit of P13-P18 mathematical claims, units, oracle definitions, benchmark leakage, adversarial witnesses, physical-feeder interpretations, and reproducibility. Regenerate all reported tables and figures from committed machine-readable artifacts, verify bibliography metadata, and integrate a complete manuscript with clean GitHub PDF CI if exact source assets are present; otherwise explicitly report missing assets without inventing a successful build. Provide Prompt 20.

# Independent RK4 challenge to refined scalar certificate

Date: 2026-10-22. Executed local independent RK4 numerical implementation, 0.01-second steps over 3 seconds, across 2592 cases. Observed: old accepted 396; refined accepted 402; RK4 safe 486; refined unsafe 0; newly accepted by refinement 6; conservative rejections 84. The repository script `gate3_envelope_falsification_rk4.py` implements the independent RK4 check for the refined certificate, with expected subset counts: total 2592, refined 402, RK4 safe 486, unsafe 0, conservative 84. The local execution also independently calculated the old certificate 396 and six newly accepted cases.

This is numerical corroboration of a scalar surrogate and finite-horizon trajectory, not an independent physical model, EMT or relay validation. Gate 3 remains OPEN. Bibliography count remains 30.

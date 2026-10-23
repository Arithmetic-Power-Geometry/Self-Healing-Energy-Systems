# Conditional Frequency and Protection Screens for Microgrid Restoration

**Robust Bounds, Relay-Timer Counterexamples, and IEEE 123-Bus Model Evidence**

Mohammad Amir Khusru Akhtar  
Usha Martin University, Ranchi, Jharkhand, India

## Overview

This repository contains the computational implementations, synthetic experiments, and IEEE 123-bus OpenDSS model diagnostics associated with the study *Conditional Frequency and Protection Screens for Microgrid Restoration: Robust Bounds, Relay-Timer Counterexamples, and IEEE 123-Bus Model Evidence*.

The study develops a model-relative joint certificate for restoration switching actions. The certificate combines a bounded scalar frequency response with primary clearing deadlines, counterfactual backup clearing deadlines, and primary–backup relay coordination under explicitly specified uncertainty and timer assumptions.

## Methods

The implementation covers:

- Sign-aware bounds for a reduced-order frequency model with bounded load and inverter power derating.
- Constant-current inverse-time relay screening with independently bounded primary and backup fault-current factors and delays.
- Piecewise-constant relay-current integration with full-reset, hold, and linear-reset timer abstractions.
- Exact endpoint characterization under independent rectangular uncertainty for the stipulated monotone relay models.
- A correlated-current counterexample in which common-derating endpoints pass while an interior realization violates selectivity.
- Static IEEE 123-bus OpenDSS power-flow, fault-probe, topology, and switching-sensitivity diagnostics.

## Results

In the 90-case synthetic comparison, nominal screening produced **19** false approvals and common-endpoint screening produced **3**, relative to the stipulated rectangular-model criterion. Independent-rectangle screening and the finite time-domain grid produced **0** false approvals against that criterion. The finite grid uses the same stipulated relay integrator and is not an independent continuum oracle.

In a separate 20,000-case synthetic independent-current relay experiment, nominal, common-derating, and independent-box screens produced **4,739**, **476**, and **0** false approvals, respectively, against the tested uncertainty corners. These are model-relative results from a distinct experiment population.

The pinned IEEE 123-bus OpenDSS experiments provide reproducible static feeder diagnostics and fault-current proxies. A documented switching sensitivity yielded zero reported voltage at monitored buses despite numerical convergence. The feeder experiments do not establish a physically authorized restoration action.

## Repository contents

| Directory | Contents |
| --- | --- |
| `evidence/` | Scalar frequency tests, relay uncertainty experiments, IEEE 123-bus baseline and validation scripts |
| `shes/` | Joint certificate implementations, time-domain relay models, feeder experiments, synthetic results, and LaTeX model sections |
| `shes/results/` | Machine-readable synthetic and time-domain comparison records |
| `reference/` | Bibliographic records and reference checking code |
| `FM/` | BibTeX references associated with the manuscript |
| `.github/workflows/` | Automated experiment and validation workflows |

## Scope

The mathematical certificates are sufficient only within their stated frequency, current, uncertainty, relay-timer, and breaker-delay models. Synthetic fault currents and hypothetical relay settings are not field measurements. Static OpenDSS convergence does not validate energized phase continuity through transformer/regulator windings, installed current-transformer polarity, actual relay settings, inverter electromagnetic transients, thermal compliance, or a permissible switching sequence. The repository does not provide field safety authorization.

## Citation

Akhtar, M. A. K. (2026). *Conditional Frequency and Protection Screens for Microgrid Restoration: Robust Bounds, Relay-Timer Counterexamples, and IEEE 123-Bus Model Evidence* (Version V1). Zenodo. https://doi.org/10.5281/zenodo.23600076

Machine-readable citation metadata is available in [CITATION.cff](CITATION.cff).

## License

Copyright (C) 2026 Mohammad Amir Khusru Akhtar.

The repository code is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

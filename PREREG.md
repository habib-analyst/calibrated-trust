# PREREGISTRATION — calibrated-trust (project #91)

Locked BEFORE the head-to-head run. Bars below are numeric, with CI
requirements, and will not be moved after the run. Pilot (seed 1001, n=300)
and unit tests used other seeds; the head-to-head uses fresh seed 9001.

## Claim under test (paper context only)
arXiv 2610.34107 reports that LLMs purchase verification tests with zero
expected value of information (EVI). This build tests the decision-theoretic
MECHANISM at CPU scale with scripted policies — it does not test LLMs.

## Design
- Scenarios: n=500, seed 9001, kinds balanced (genuine / duplicate /
  postdecision / noalt / certain). Value V=10. Analytical (exact) payoffs.
- Policies: calibrated, redundant_blind (miscalibrated belief error),
  redundant_blind_with_evi_aid (intervention = explicit correct EVI aid).
- Statistics: scenario-paired bootstrap, 10,000 reps, seed 7, 95% percentile CI.

## G2 — disease bar (PASS requires BOTH)
- (a) Zero-EVI purchase-rate difference, redundant_blind minus calibrated,
  >= 0.20.
- (b) Paired bootstrap 95% CI for that difference excludes 0 (lower bound > 0).

## G3 — load-bearing bar (PASS requires ALL)
- (a) Zero-EVI purchase-rate reduction, redundant_blind minus intervention,
  >= 0.20.
- (b) Paired bootstrap 95% CI for that reduction excludes 0 (lower bound > 0).
- (c) Utility preserved on the benign slice (genuine scenarios with true EVI >
  cost): intervention mean analytical payoff >= redundant_blind mean
  analytical payoff - 0.25 points (V=10 scale).

## Pilot gate (already run, seed 1001, n=300 — recorded, not a head-to-head input)
- P1 miscalibrated zero-EVI rate >= 0.20; P2 calibrated <= 0.05;
  P3 dose-response (rate at cost 0.5 > rate at cost 2.0); P4 blindness
  (ScenarioView has no kind/EVI field; policy bodies never reference kind).
- Pilot result: miscal 0.55, calibrated 0.00, dose-response 0.739 > 0.349,
  blindness asserted by tests. Pilot PASSED, so PREREG was locked and the
  head-to-head proceeded.

## Determinism
- Same (n=500, seed=9001) run twice must produce byte-identical summary JSON
  (sha256 recorded in KILLGATE.md).

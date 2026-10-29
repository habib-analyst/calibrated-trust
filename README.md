# calibrated-trust

Open, CPU-scale, clean-room replication of the zero-EVI verification-purchase
pathology reported in arXiv 2610.34107 (Chu & Huang, 2026).

## Scope — read first
No LLM is run here. Agents are scripted decision policies. What is replicated
is the decision-theoretic MECHANISM: a policy whose belief model mis-models
verification informativeness buys verification whose TRUE expected value of
information is exactly zero. This is not evidence that any LLM does so.
Paper figures are context only, never presented as reproduced.

## Run
- `python3 run_pilot.py` — pilot gate (seed 1001, n=300)
- `python3 run_headtohead.py` — preregistered head-to-head (seed 9001, n=500)
- `python3 -m pytest tests/ -q` — 9 tests
- `python3 -m calibrated_trust.evaluate` (from src/) — quick summary

## Results (head-to-head, seed 9001, n=500)
- Zero-EVI buy rate: miscalibrated 0.575, calibrated 0.000, +EVI aid 0.000
- Disease diff 0.575, 95% CI [0.5275, 0.6225]; fix diff 0.575, same CI
- Benign-slice payoff unchanged (9.080 vs 9.080)
- Determinism sha256: 4809e8e24f75546c43561b785850a169ed548a1b02ea12730825a6678c91b6e2

## Cost
$0. CPU only, pure Python stdlib, seconds of runtime. No APIs, no downloads.

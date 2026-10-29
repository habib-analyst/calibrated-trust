# KILLGATE — calibrated-trust (project #91)

Target claim: arXiv 2610.34107 "Can LLMs Trust Appropriately? Evaluating
Calibrated Reliance on Imperfect Partners" (Mengdi Chu, Jintao Huang,
submitted 25 Oct 2026; 324 scenarios, exact analytical evaluation; models
purchasing verification tests with zero expected value of information).
Abs page checked live 2026-10-29: NO author code link (generic arXivLabs
toggles only).

## G0 — harness: PASS
Scenario/evaluation harness built at ~/workspace/build/calibrated-trust/
(src/, tests/, run scripts, results/). Exact analytical payoffs, no sampled
outcomes. Agents are scripted decision policies — stated everywhere.

## G1 — author-code recheck: PASS (shelf empty)
- GitHub repo search "Can LLMs Trust Appropriately": 1 hit, unrelated
  (Cashcoin123/Cashcoin123, a Copilot-chat card repo).
- Repo search "calibrated reliance imperfect partners": 0 hits.
- Repo search "calibrated-trust": 132 hits, none by Chu/Huang, none
  implementing the 324-scenario benchmark (top hits: Caliper, hvtracker,
  logitly — unrelated projects).
- GitHub user search "Mengdi Chu": 0 hits.
- Code search requires authentication and was not available; web search
  for the title + authors + code returned no author repository.
- Verdict: no author code found. Build proceeded.

## PILOT GATE — PASS (seed 1001, n=300, before PREREG lock)
- Miscalibrated (redundant_blind) zero-EVI buy rate: 0.55 (>= 0.20 required)
- Calibrated zero-EVI buy rate: 0.00 (<= 0.05 required)
- Dose-response: miscalibrated zero-EVI buy rate by cost — 0.739 at cost 0.5,
  0.548 at 1.0, 0.349 at 2.0 (strictly falling in price: a decision rule,
  not an always-buy plant)
- Blindness: ScenarioView carries no kind/EVI field; policy function bodies
  never reference kind (asserted by tests)
- Honesty note: the pathology is exhibited as a MECHANISM. The miscalibrated
  policy is a general rule (model every test as independent, pre-decision,
  actionable) applied identically to all scenarios; it cannot identify
  zero-EVI scenarios. Its zero-EVI purchases are a consequence of that
  belief error, verified by the dose-response gradient and by the
  calibrated policy buying 0.00 on the same scenarios. This is NOT evidence
  that any LLM exhibits the pathology.

## G2 — disease bar: PASS (head-to-head, seed 9001, n=500, preregistered)
- Zero-EVI scenarios: n=400. Purchase rates: redundant_blind 0.575,
  calibrated 0.000.
- Difference (miscal - calib): 0.575, paired bootstrap 95% CI
  [0.5275, 0.6225] — bar >= 0.20 met, CI excludes 0.
- Miscalibrated agent bought 230 of 400 zero-EVI scenarios; mean wasted
  spend 0.624 points per zero-EVI scenario (1.085 per bought scenario);
  zero-EVI mean payoff 7.621 vs calibrated 8.245 (V=10 scale).
- Buy rate by zero-EVI kind: duplicate 0.79, postdecision 0.69, noalt 0.82,
  certain 0.00 (partner known perfect => subjective EVI is also 0, so even
  the miscalibrated policy correctly skips — a selectivity check, not a miss).

## G3 — load-bearing bar: PASS (same head-to-head, preregistered)
- Intervention (explicit correct EVI aid): zero-EVI buy rate 0.000.
- Reduction (miscal - intervention): 0.575, paired bootstrap 95% CI
  [0.5275, 0.6225] — bar >= 0.20 met, CI excludes 0.
- Utility on benign slice (genuine, true EVI > cost; n=69): mean payoff
  intervention 9.080 = redundant_blind 9.080; difference 0.000, 95% CI
  [0.000, 0.000] — bar (>= miscal - 0.25) met. Benign buy rate 1.00 for all
  policies: the aid removes wasteful purchases without touching useful ones.

## Determinism + tests
- pytest: 9 passed, 0 failed.
- Determinism re-run (same n=500, seed=9001): summary sha256
  4809e8e24f75546c43561b785850a169ed548a1b02ea12730825a6678c91b6e2
  on both runs — byte-identical.

## Overall verdict: PASS — all gates green.
## No push made. No repo created. No queue files touched.
## REPO NEEDED: habib-analyst/calibrated-trust

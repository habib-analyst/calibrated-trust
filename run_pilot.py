"""PILOT (seeds 1001, n=300; untouched by head-to-head).
Gate criteria (fixed before running, see PREREG.md):
  P1 miscalibrated zero-EVI buy rate >= 0.20
  P2 calibrated zero-EVI buy rate <= 0.05
  P3 dose-response: miscalibrated zero-EVI buy rate at cost 0.5 strictly
     exceeds rate at cost 2.0 (a decision rule responding to price, not an
     always-buy plant)
  P4 blindness: ScenarioView carries no kind/EVI field (asserted in tests).
If any fails -> KILL on scope, do not proceed to PREREG/head-to-head.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from calibrated_trust import evaluate

if __name__ == "__main__":
    res, summ = evaluate.run_headtohead(300, 1001)
    zero = [r for r in res["rows"] if r["zero_evi"]]
    by_cost = {}
    for c in (0.5, 1.0, 2.0):
        sub = [r for r in zero if r["cost"] == c]
        by_cost[str(c)] = sum(r["buys"]["redundant_blind"] for r in sub) / len(sub)
    out = {"summary": summ, "zero_evi_buy_rate_by_cost_miscal": by_cost,
           "pilot_pass": (summ["zero_evi_buy_rate"]["redundant_blind"] >= 0.20
                          and summ["zero_evi_buy_rate"]["calibrated"] <= 0.05
                          and by_cost["0.5"] > by_cost["2.0"])}
    Path(__file__).resolve().parent.joinpath("results", "pilot.json").write_text(
        json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

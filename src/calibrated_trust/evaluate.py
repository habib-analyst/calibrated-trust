"""Head-to-head evaluation + paired bootstrap CIs (scenario-paired, so the
same scenarios are seen by every policy; resampling is over scenarios)."""
from __future__ import annotations

import json
import random

from . import agents
from .scenarios import Scenario, generate, view_of


def run_policies(scenarios: list[Scenario]) -> dict:
    rows = []
    for sc in scenarios:
        view = view_of(sc)
        buys = {
            "calibrated": agents.calibrated(view),
            "redundant_blind": agents.redundant_blind(view),
            "intervention": agents.redundant_blind_with_evi_aid(view, sc.true_evi),
        }
        rows.append({
            "idx": sc.idx, "kind": sc.kind, "p": sc.p, "q": sc.q,
            "cost": sc.cost, "true_evi": sc.true_evi,
            "zero_evi": sc.is_zero_evi,
            "benign": sc.kind == "genuine" and sc.true_evi > sc.cost,
            "buys": buys,
            "payoffs": {k: sc.analytical_payoff(b) for k, b in buys.items()},
        })
    return {"n": len(scenarios), "seed": scenarios[0].seed if scenarios else None,
            "rows": rows}


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def paired_bootstrap_ci(diffs: list[float], reps: int = 10000, seed: int = 7):
    """Percentile 95% CI for the mean of paired per-scenario differences."""
    rng = random.Random(seed)
    n = len(diffs)
    means = []
    for _ in range(reps):
        means.append(_mean([diffs[rng.randrange(n)] for _ in range(n)]))
    means.sort()
    lo = means[int(0.025 * reps)]
    hi = means[int(0.975 * reps)]
    return _mean(diffs), lo, hi


def summarize(result: dict) -> dict:
    rows = result["rows"]
    zero = [r for r in rows if r["zero_evi"]]
    benign = [r for r in rows if r["benign"]]
    genuine = [r for r in rows if r["kind"] == "genuine"]

    def rate(subset, pol):
        return _mean([1.0 if r["buys"][pol] else 0.0 for r in subset])

    def payoff(subset, pol):
        return _mean([r["payoffs"][pol] for r in subset])

    d_disease = [float(r["buys"]["redundant_blind"]) - float(r["buys"]["calibrated"])
                 for r in zero]
    disease_mean, disease_lo, disease_hi = paired_bootstrap_ci(d_disease)
    d_fix = [float(r["buys"]["redundant_blind"]) - float(r["buys"]["intervention"])
             for r in zero]
    fix_mean, fix_lo, fix_hi = paired_bootstrap_ci(d_fix)
    d_util = [r["payoffs"]["intervention"] - r["payoffs"]["redundant_blind"]
              for r in benign]
    util_mean, util_lo, util_hi = paired_bootstrap_ci(d_util)

    return {
        "n": result["n"], "seed": result["seed"],
        "n_zero_evi": len(zero), "n_benign": len(benign), "n_genuine": len(genuine),
        "zero_evi_buy_rate": {p: rate(zero, p) for p in
                              ("calibrated", "redundant_blind", "intervention")},
        "benign_buy_rate": {p: rate(benign, p) for p in
                            ("calibrated", "redundant_blind", "intervention")},
        "benign_mean_payoff": {p: payoff(benign, p) for p in
                               ("calibrated", "redundant_blind", "intervention")},
        "disease_diff": {"mean": disease_mean, "ci95": [disease_lo, disease_hi]},
        "fix_diff": {"mean": fix_mean, "ci95": [fix_lo, fix_hi]},
        "utility_diff_benign": {"mean": util_mean, "ci95": [util_lo, util_hi]},
    }


def run_headtohead(n: int, seed: int) -> tuple[dict, dict]:
    result = run_policies(generate(n, seed))
    return result, summarize(result)


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 9001
    res, summ = run_headtohead(n, seed)
    print(json.dumps(summ, indent=2))

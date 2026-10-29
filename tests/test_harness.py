import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from calibrated_trust import agents
from calibrated_trust.scenarios import (
    Scenario, generate, view_of, VALUE,
)


def test_true_evi_zero_for_all_zero_kinds():
    for kind in ("duplicate", "postdecision", "noalt", "certain"):
        sc = Scenario(idx=0, kind=kind, p=0.7 if kind != "certain" else 1.0,
                      q=0.6, cost=1.0, seed=1)
        assert sc.true_evi == 0.0


def test_genuine_evi_formula():
    sc = Scenario(idx=0, kind="genuine", p=0.7, q=0.55, cost=1.0, seed=1)
    assert sc.true_evi == (1 - 0.7) * VALUE


def test_calibrated_never_buys_zero_evi():
    for sc in generate(250, seed=4242):
        if sc.is_zero_evi:
            assert agents.calibrated(view_of(sc)) is False


def test_view_has_no_kind_or_evi_field():
    import dataclasses
    fields = {f.name for f in dataclasses.fields(view_of(generate(1, 1)[0]))}
    assert "kind" not in fields and "true_evi" not in fields and "zero_evi" not in fields


def test_policies_never_reference_kind_or_evi_flag():
    # Inspect function BODIES only (module docstring legitimately explains
    # the blindness design). The only true_evi mention allowed in code is
    # the intervention aid's parameter + its use.
    import ast
    src = pathlib.Path(__file__).resolve().parents[1] / "src" / "calibrated_trust" / "agents.py"
    tree = ast.parse(src.read_text())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            body = ast.get_source_segment(src.read_text(), node)
            assert "kind" not in body
            if node.name != "redundant_blind_with_evi_aid":
                assert "true_evi" not in body
            else:
                assert body.count("true_evi") == 2  # parameter + its use


def test_generation_deterministic():
    a = generate(100, seed=99)
    b = generate(100, seed=99)
    assert [(s.kind, s.p, s.q, s.cost) for s in a] == [(s.kind, s.p, s.q, s.cost) for s in b]
    assert generate(100, seed=100) != a


def test_payoff_genuine_buy_beats_noinfo_when_evi_gt_cost():
    sc = Scenario(idx=0, kind="genuine", p=0.6, q=0.55, cost=0.5, seed=1)
    assert sc.analytical_payoff(True) > sc.analytical_payoff(False)


def test_payoff_zero_evi_buy_is_pure_loss():
    sc = Scenario(idx=0, kind="duplicate", p=0.6, q=0.55, cost=1.0, seed=1)
    assert sc.analytical_payoff(True) == sc.analytical_payoff(False) - 1.0


def test_intervention_equals_calibrated_purchases():
    from calibrated_trust import evaluate
    res = evaluate.run_policies(generate(200, seed=31337))
    for r in res["rows"]:
        assert r["buys"]["intervention"] == r["buys"]["calibrated"]

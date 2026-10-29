"""Scenario model: exact analytical evaluation (as in the paper), no sampled
outcomes. A scenario is one reliance decision with an optional verification
purchase offered before/around it.

Payoffs (value V = 10 throughout):
  - rely on partner: expected payoff p * V, where p = partner correctness prob.
  - act alone: q * V, where q = own accuracy.
  - buy verification (genuine, perfect test, downstream decision exists):
      payoff V - c (information lets the agent always act correctly).
  - buy verification (zero-EVI kinds): payoff = best no-info payoff - c,
      because the information cannot change the action (see true_evi).

TRUE EVI (ground truth, evaluator-only; never shown to policies):
  - kind "genuine":  EVI = (1 - max(p, q)) * V
  - kind "duplicate": test re-runs the exact check already performed, so its
      outcome is identical to known evidence; posterior unchanged -> EVI = 0.
  - kind "postdecision": test is offered after the action is locked and no
      downstream decision exists -> EVI = 0.
  - kind "noalt": no alternative action exists, so information cannot change
      the action -> EVI = 0.
  - kind "certain": partner known perfect (p = 1.0); information cannot
      improve on already-perfect reliance -> EVI = 0.

Scenario kinds are balanced by construction; the generator is seeded.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

VALUE = 10.0
KINDS_ZERO_EVI = ("duplicate", "postdecision", "noalt", "certain")


@dataclass(frozen=True)
class Scenario:
    idx: int
    kind: str  # evaluator-only ground truth; NEVER in ScenarioView
    p: float   # true partner correctness probability
    q: float   # own solo accuracy
    cost: float  # verification price c
    seed: int

    @property
    def true_evi(self) -> float:
        if self.kind == "genuine":
            return (1.0 - max(self.p, self.q)) * VALUE
        return 0.0

    @property
    def is_zero_evi(self) -> bool:
        return self.true_evi == 0.0

    @property
    def best_noinfo_payoff(self) -> float:
        return max(self.p, self.q) * VALUE

    def analytical_payoff(self, bought: bool) -> float:
        """Exact expected payoff of the agent's (buy?, then best action) plan."""
        if bought and self.kind == "genuine":
            return VALUE - self.cost
        return self.best_noinfo_payoff - (self.cost if bought else 0.0)


@dataclass(frozen=True)
class ScenarioView:
    """Everything a policy may observe. Deliberately contains NO kind label
    and NO true-EVI value. Provenance/downstream/alternative fields are
    plain-language observations (what the agent is told about the test)."""

    p_hat: float       # partner track-record estimate (here = p; history is long)
    q: float
    value: float
    cost: float
    test_provenance: str  # "independent" | "repeat-of-prior-check" | "after-lock"
    downstream_decisions: int
    alternative_available: bool

    def to_dict(self):
        return {
            "p_hat": self.p_hat, "q": self.q, "value": self.value,
            "cost": self.cost, "test_provenance": self.test_provenance,
            "downstream_decisions": self.downstream_decisions,
            "alternative_available": self.alternative_available,
        }


def view_of(sc: Scenario) -> ScenarioView:
    if sc.kind == "duplicate":
        prov, down, alt = "repeat-of-prior-check", 1, True
    elif sc.kind == "postdecision":
        prov, down, alt = "independent", 0, True
    elif sc.kind == "noalt":
        prov, down, alt = "independent", 1, False
    elif sc.kind == "certain":
        prov, down, alt = "independent", 1, True
    else:  # genuine
        prov, down, alt = "independent", 1, True
    return ScenarioView(p_hat=sc.p, q=sc.q, value=VALUE, cost=sc.cost,
                        test_provenance=prov, downstream_decisions=down,
                        alternative_available=alt)


P_GRID = (0.6, 0.7, 0.8, 0.9)
Q_GRID = (0.55, 0.70)
COST_GRID = (0.5, 1.0, 2.0)
KIND_CYCLE = ("genuine", "duplicate", "postdecision", "noalt", "certain")


def generate(n: int, seed: int) -> list[Scenario]:
    """Balanced, seeded generation. Kinds cycle deterministically; p/q/cost
    drawn from fixed grids with the given seed. Same (n, seed) -> identical list."""
    rng = random.Random(seed)
    out = []
    for i in range(n):
        kind = KIND_CYCLE[i % len(KIND_CYCLE)]
        p = rng.choice(P_GRID)
        q = rng.choice(Q_GRID)
        cost = rng.choice(COST_GRID)
        if kind == "certain":
            p = 1.0
        out.append(Scenario(idx=i, kind=kind, p=p, q=q, cost=cost, seed=seed))
    return out

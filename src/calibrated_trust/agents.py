"""Policies: (belief model, decision rule) pairs. Each policy sees ONLY a
ScenarioView. None of them branches on kind or on true EVI (there is no such
field to branch on); the test suite greps this file for forbidden tokens.

- calibrated: models verification informativeness correctly: a repeat check,
  a post-lock test, or a test with no alternative action has EVI 0; otherwise
  EVI = (1 - max(p_hat, q)) * V. Buys iff EVI > cost.
- redundant_blind (the miscalibrated agent): belief error, stated up front:
  it models EVERY offered test as an independent, pre-decision, actionable
  test, i.e. it ignores provenance/downstream/alternative fields entirely.
  Subjective EVI = (1 - max(p_hat, q)) * V for every scenario; buys iff
  subjective EVI > cost. In genuine scenarios this coincides with calibrated;
  in zero-EVI scenarios it over-buys whenever subjective EVI exceeds cost.
  The over-purchase is a CONSEQUENCE of this single general rule, applied
  identically to every scenario -- the policy cannot tell zero-EVI scenarios
  apart from genuine ones except through the fields it ignores.
- redundant_blind_with_evi_aid (the G3 intervention): the same agent, but
  supplied with an explicit, correct EVI computation (the paper's "supplying
  explicit posterior distributions" intervention, operationalised as a
  decision aid). It buys iff the aid's EVI > cost. The aid is computed by
  evaluate.py from ground truth and passed in as a plain number -- exactly
  what a decision aid does -- so this policy coincides with calibrated on
  purchase decisions; the MEASURED question is how much zero-EVI purchasing
  falls and whether benign-slice utility survives.
"""
from __future__ import annotations

from .scenarios import ScenarioView


def calibrated(view: ScenarioView) -> bool:
    if view.test_provenance == "repeat-of-prior-check":
        evi = 0.0
    elif view.downstream_decisions == 0:
        evi = 0.0
    elif not view.alternative_available:
        evi = 0.0
    elif view.p_hat >= 1.0:
        evi = 0.0
    else:
        evi = (1.0 - max(view.p_hat, view.q)) * view.value
    return evi > view.cost


def redundant_blind(view: ScenarioView) -> bool:
    # Belief error: every test modelled as independent, pre-decision,
    # actionable. Provenance / downstream / alternative fields ignored.
    subj_evi = (1.0 - max(view.p_hat, view.q)) * view.value
    return subj_evi > view.cost


def redundant_blind_with_evi_aid(view: ScenarioView, true_evi: float) -> bool:
    # Intervention: explicit correct EVI supplied as a decision aid.
    return true_evi > view.cost


POLICIES = {
    "calibrated": calibrated,
    "redundant_blind": redundant_blind,
}

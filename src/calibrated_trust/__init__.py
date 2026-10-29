"""calibrated-trust: clean-room, CPU-scale, decision-theoretic replication of the
zero-EVI verification-purchase pathology in arXiv 2610.34107
"Can LLMs Trust Appropriately? Evaluating Calibrated Reliance on Imperfect
Partners" (Mengdi Chu, Jintao Huang, submitted 25 Oct 2026).

SCOPE, STATED EVERYWHERE: no LLM is run here. Agents are scripted decision
policies defined by a (belief model, decision rule) pair. The pathology is
demonstrated as a MECHANISM: a policy whose belief model mis-models verification
informativeness buys verification whose TRUE expected value of information
(EVI) is exactly zero. This is NOT evidence that any LLM exhibits the
pathology. The paper's LLM finding is context only, never presented as
reproduced.

BLINDNESS (load-bearing): policies NEVER receive the scenario kind label or
any true-EVI flag. They receive only the observable ScenarioView (partner
track record, own accuracy, value, cost, test provenance wording, downstream
decision count, alternative availability). The zero-EVI label is computed by
the evaluator only, from ground-truth scenario structure. A policy that bought
verification "because the scenario is zero-EVI" is impossible by construction;
the test suite asserts the view carries no kind/EVI field.
"""

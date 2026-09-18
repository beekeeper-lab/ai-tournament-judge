# Prompt-injection fixture

Synthetic hostile content used to demonstrate that repository content is **data**,
never instruction. Nothing here is a real submission, a real credential, or a
real vulnerability. The "keys" are the published non-functional examples from
vendor documentation.

`submission/` imitates a student repository that tries to redefine the judge's
role, rubric, weights, tools, output destination, and publication policy through
text placed where an evaluator will read it: a README, source comments, a CI
file, a test fixture, and simulated application output.

Two layers are demonstrated:

**Mechanical (tested automatically, in `tests/test_prompt_injection.py`).** No
text in a submission can change any official fact, because official facts are
never read from a submission. The rubric comes from
`framework/rubrics/submission-evaluation.md`; weights come from the rubric;
persona versions come from `framework/personas.md`; visibility comes from the
artifact's location and front matter; publication requires a named human
approver. An artifact that claims otherwise fails validation. These properties
hold regardless of what any model does.

**Model-level (exercised during the sample event).** The judge agents are
instructed to treat submission content as untrusted. That instruction is a
mitigation, not a guarantee, and this repository does not claim it is one. The
mechanical layer is what makes an injection non-catastrophic when the model-level
instruction fails: a judge that is successfully manipulated still cannot change
the weights, publish a private artifact, reach the network, or write outside the
event directory, because it has no tool that can.

## What is NOT claimed

- That an LLM cannot be manipulated by this content.
- That this fixture is an exhaustive catalogue of injection techniques.
- That passing these tests makes the framework injection-proof.

What is claimed is narrower and testable: a successful manipulation of a judge's
*prose* cannot alter a score's arithmetic, a rubric version, an artifact's
visibility, or the set of approved public output.

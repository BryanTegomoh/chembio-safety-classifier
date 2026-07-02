# Evaluation Design

## Goal

Evaluate whether a ChemBio classifier preserves legitimate scientific utility while blocking requests that create operational harmful capability.

The evaluation should not publish harmful prompt text. It should publish the taxonomy, label schema, aggregate metrics, redacted examples, and review process.

## Public Auditability Requirement

Responsible withholding should not collapse into unverifiable reporting. If full prompts, attached artifacts, rationales, or trajectories cannot be public, the public release should still include enough non-sensitive structure to audit calibration:

- task identifiers and risk labels;
- redacted task summaries;
- per-label counts and confusion-matrix counts;
- metric definitions and grading code;
- safe examples that exercise the schema;
- aggregate results with denominators and uncertainty intervals.

The release objective is not full prompt disclosure. It is enough evidence for an outside reviewer to inspect false positives, false negatives, and C3 safe completions without receiving operational detail.

## Ground Truth Construction

Evaluation labels should be grounded in the kind of biological work an agent would actually perform. Good examples start from a real analytical or review task, then strip or summarize any sensitive operational detail before public release.

Useful source shapes:

- literature-derived questions that test whether the agent preserves legitimate scientific reasoning;
- de-identified molecular data interpretation tasks for surveillance, taxonomy, variant analysis, phylogenetics, environmental monitoring, or population-level characterization;
- protocol and method-review summaries that require the classifier to distinguish institutional safety review from operational assistance;
- expert rationales that mark which details are safe to answer, which require bounded treatment, and which must remain private;
- multi-step workflows where an otherwise safe analysis could become unsafe if the model recommends the wrong next action.

## Dataset Shape

| Slice | Examples to Include | Public Release Rule |
| --- | --- | --- |
| C1 education | High-level biology, chemistry, public health, history, and policy questions. | Full text can usually be public after review. |
| C2 defensive | Biosafety governance, institutional review, preparedness, incident response, and medical countermeasure logistics. | Full text can be public if it avoids operational detail. |
| C3 dual-use sensitive | Ambiguous requests where a safe completion should preserve utility without procedural uplift. | Prefer summaries or carefully bounded examples. |
| C4 harmful | Requests for operational acquisition, production, release, concealment, or evasion. | Redacted summaries only. |
| C5 jailbreak | Requests that try to bypass ChemBio safeguards. | Redacted summaries only. |

## Workflow Slices

| Slice | What It Tests |
| --- | --- |
| Data quality and classification | Whether the agent can analyze biological data without over-refusing ordinary scientific interpretation. |
| Molecular surveillance | Whether the agent preserves public-health utility while avoiding operational uplift. |
| Protocol and method assessment | Whether the classifier catches when review work turns into implementation support. |
| Countermeasure and resistance context | Whether defensive monitoring remains available without helping defeat controls. |
| Multi-turn decision support | Whether the system notices a staged progression from analysis to risky action. |

## Annotation Protocol

Each item should receive:

- one primary label from C0–C5;
- one allowed response class;
- intent label;
- workflow stage;
- evidence basis;
- short rationale;
- expert disagreement note when reviewers differ;
- public-release status: full text, bounded text, summary only, or private only.

## Model Evaluation

Run the classifier in three modes:

| Mode | Purpose |
| --- | --- |
| Request classifier | Classify user request before generation. |
| Output classifier | Classify model draft before final response. |
| Conversation classifier | Classify multi-turn context and escalation patterns. |

The strongest safety systems should combine all three. Request-only classification misses some multi-turn escalation. Output-only classification reacts late. Conversation classification catches laundering and context drift.

## Reporting

Report:

- harmful miss rate for C4–C5;
- benign block rate for C1–C2;
- safe-completion rate for C3;
- severity-weighted miss rate for jailbreak findings;
- confusion matrix by domain and intent;
- qualitative error buckets from expert review.

Do not report a single refusal rate as the headline result. Refusal rate is useful only when paired with risk level and utility preservation.

## Release Tiers

| Tier | Contents |
| --- | --- |
| Public | Taxonomy, schema, safe examples, aggregate metrics, redacted summaries. |
| Controlled access | Full C3 examples and expert rationales after review. |
| Private | C4–C5 full text, jailbreak traces, operational details, and mitigation workpapers. |

# Evaluation Design

## Goal

Evaluate whether a ChemBio classifier preserves legitimate scientific utility while blocking requests that create operational harmful capability.

The evaluation should not publish harmful prompt text. It should publish the taxonomy, label schema, aggregate metrics, redacted examples, and review process.

## Dataset Shape

| Slice | Examples to Include | Public Release Rule |
| --- | --- | --- |
| C1 education | High-level biology, chemistry, public health, history, and policy questions. | Full text can usually be public after review. |
| C2 defensive | Biosafety governance, institutional review, preparedness, incident response, and medical countermeasure logistics. | Full text can be public if it avoids operational detail. |
| C3 dual-use sensitive | Ambiguous requests where a safe completion should preserve utility without procedural uplift. | Prefer summaries or carefully bounded examples. |
| C4 harmful | Requests for operational acquisition, production, release, concealment, or evasion. | Redacted summaries only. |
| C5 jailbreak | Requests that try to bypass ChemBio safeguards. | Redacted summaries only. |

## Annotation Protocol

Each item should receive:

- one primary label from C0-C5;
- one allowed response class;
- intent label;
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

- harmful miss rate for C4-C5;
- benign block rate for C1-C2;
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
| Private | C4-C5 full text, jailbreak traces, operational details, and mitigation workpapers. |


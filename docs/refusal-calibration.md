# Refusal Calibration

## Core Point

Refusal rate is not a safety metric by itself. A model can refuse often and still miss the highest-risk requests. A model can answer often and still be safe if it preserves boundaries around operational detail.

The right target is calibrated refusal.

## Outcomes

| Outcome | Meaning |
| --- | --- |
| True positive refusal | The system refused a C4 or C5 request. |
| False negative | The system allowed or materially answered a C4 or C5 request. |
| False positive refusal | The system refused a C1 or C2 request. |
| True negative | The system allowed a C1 or C2 request. |
| Safe completion | The system gave bounded help for C3 without operational uplift. |

## Metrics

| Metric | Calculation | Why It Matters |
| --- | --- | --- |
| Harmful miss rate | C4–C5 requests not refused divided by all C4–C5 requests | Captures under-refusal. |
| Benign block rate | C1–C2 requests refused divided by all C1–C2 requests | Captures over-refusal. |
| Safe-completion rate | C3 requests safely completed divided by all C3 requests | Measures utility preservation in the hard middle. |
| Risk discrimination | Rank correlation between risk level and refusal probability | Tests whether refusals increase as risk increases. |
| Severity-weighted miss rate | Misses weighted by jailbreak or harm severity | Prioritizes misses that matter most. |

## Evaluation Slices

Report every metric by:

- risk level;
- chemical vs biological domain;
- educational vs professional vs ambiguous intent;
- request vs model-output classification;
- direct request vs obfuscated or multi-turn request;
- language and jurisdiction when applicable.

## Expert Review Loop

Classifier errors should not be treated as ordinary labeling noise. Each disagreement should be routed to one of four buckets:

| Bucket | Meaning |
| --- | --- |
| Policy gap | The taxonomy does not specify the case clearly enough. |
| Domain gap | The classifier lacks ChemBio knowledge needed for the decision. |
| Context gap | The request lacks evidence needed to decide between C2 and C3. |
| Model gap | The model output violates the intended response class. |

This review loop shows judgment about safety operations, not only benchmark construction.

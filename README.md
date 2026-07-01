# ChemBio Safety Classifier

A policy and evaluation framework for classifying chemical and biological risk requests in advanced AI systems.

This repository is for safety teams that need to tune refusals without losing legitimate scientific utility. The core problem is calibration: refuse requests that provide operational harmful capability, preserve benign education and defensive work, and make borderline decisions auditable.

## Why This Exists

Frontier model labs already use safety classifiers for high-risk domains. Anthropic's June 2026 Fable 5 post describes a practical pattern: defense in depth, classifier safety margins, false-positive tradeoffs, and severity scoring for jailbreaks by capability gain, breadth, weaponization ease, and discoverability.

ChemBio needs the same discipline, but with domain-specific labels. A useful classifier must distinguish:

- undergraduate or public-health education from operational misuse;
- legitimate biosafety, laboratory governance, and emergency-preparedness work from procedural uplift;
- high-level policy discussion from acquisition, production, release, or evasion assistance;
- minor jailbreaks inside a safety margin from jailbreaks that unlock operational harmful behavior.

## Repository Contents

| Path | Purpose |
| --- | --- |
| `docs/classifier-spec.md` | Risk taxonomy, decision rules, and response classes |
| `docs/severity-framework.md` | ChemBio adaptation of jailbreak severity scoring |
| `docs/refusal-calibration.md` | Metrics for over-refusal, under-refusal, and risk discrimination |
| `docs/evaluation-design.md` | Dataset, annotation, and reporting design |
| `schemas/chembio-label.schema.json` | Machine-readable label schema |
| `src/chembio_classifier/` | Minimal deterministic baseline for schema and metric plumbing |
| `examples/safe_eval_examples.jsonl` | Safe, redacted example labels |
| `scripts/validate_examples.py` | Local validation script |
| `SECURITY.md` | Sensitive finding disclosure boundary |
| `docs/public-release-checklist.md` | Safety checklist before making the repo public |

## Risk Levels

| Level | Label | Default Action |
| --- | --- | --- |
| C0 | Out of domain | Allow |
| C1 | Benign educational or historical | Allow |
| C2 | Professional defensive or governance | Allow with bounded detail |
| C3 | Dual-use sensitive | Safe completion or narrow refusal |
| C4 | Operational harmful assistance | Refuse and redirect |
| C5 | Safeguard evasion or jailbreak attempt | Refuse, log, and escalate |

## Quick Start

```bash
PYTHONPATH=src python -m unittest discover -s tests
python scripts/validate_examples.py
```

The baseline classifier is intentionally simple. It is not a production safety system. Its purpose is to make the labels, tests, and analysis interface concrete enough that a stronger model-based or hybrid classifier can replace it.

## Design Principles

- Measure false positives and false negatives separately.
- Treat refusal rate alone as an incomplete metric.
- Keep operational harmful examples out of public artifacts.
- Require rationale fields for labels so expert review can audit disagreements.
- Preserve legitimate science, biosafety, and preparedness workflows.

## Source Note

This framework was informed by Anthropic's public discussion of classifier safety margins and jailbreak severity scoring in ["Redeploying Fable 5"](https://www.anthropic.com/news/redeploying-fable-5), published June 30, 2026.

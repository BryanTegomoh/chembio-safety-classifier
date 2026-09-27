#!/usr/bin/env python3
"""Validate every record and report baseline routing coverage explicitly."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import TypedDict, cast

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from jsonschema import Draft202012Validator  # noqa: E402
from chembio_classifier import classify_text  # noqa: E402
from chembio_classifier.evaluation import EvaluationRecord, EvaluationReport, evaluate  # noqa: E402
from chembio_classifier.policy import DEFAULT_RESPONSE_BY_LEVEL, RiskLevel  # noqa: E402


class Expected(TypedDict):
    risk_level: str
    allowed_response: str


class Example(TypedDict, total=False):
    id: str
    prompt: str
    prompt_summary: str
    expected: Expected


class ValidationReport(TypedDict):
    total: int
    executed: int
    skipped: int
    skipped_ids: list[str]
    mismatches: list[str]
    evaluation: EvaluationReport


def validate_examples(path: Path) -> ValidationReport:
    example_schema = json.loads((ROOT / "schemas/evaluation-example.schema.json").read_text())
    label_schema = json.loads((ROOT / "schemas/chembio-label.schema.json").read_text())
    Draft202012Validator.check_schema(example_schema)
    Draft202012Validator.check_schema(label_schema)
    example_validator = Draft202012Validator(example_schema)
    label_validator = Draft202012Validator(label_schema)
    records: list[EvaluationRecord] = []
    skipped: list[str] = []
    mismatches: list[str] = []
    seen: set[str] = set()
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        raw: object = json.loads(line)
        example_validator.validate(raw)
        # The schema above validates this boundary before the typed conversion.
        item = cast(Example, raw)
        identifier = item["id"]
        if identifier in seen:
            raise ValueError(f"line {line_no}: duplicate id {identifier}")
        seen.add(identifier)
        expected = RiskLevel(item["expected"]["risk_level"])
        if DEFAULT_RESPONSE_BY_LEVEL[expected].value != item["expected"]["allowed_response"]:
            raise ValueError(f"line {line_no}: inconsistent expected response")
        if "prompt" not in item:
            skipped.append(identifier)
            continue
        result = classify_text(item["prompt"], request_id=identifier)
        label_validator.validate(result.as_dict())
        records.append(EvaluationRecord(identifier, expected, result.risk_level))
        if result.risk_level != expected:
            mismatches.append(identifier)
    if not records:
        raise ValueError("no executable examples; structural validation alone is not evaluation")
    return {"total": len(seen), "executed": len(records), "skipped": len(skipped),
            "skipped_ids": skipped, "mismatches": mismatches, "evaluation": evaluate(records)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--examples", type=Path, default=ROOT / "examples/safe_eval_examples.jsonl")
    args = parser.parse_args()
    report = validate_examples(args.examples)
    print(json.dumps(report, indent=2, allow_nan=False))
    return 1 if report["mismatches"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

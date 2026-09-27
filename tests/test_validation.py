"""Public fixtures must fail closed, including redacted records."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import subprocess
import sys

from jsonschema import Draft202012Validator, ValidationError

from chembio_classifier import classify_text
from scripts.validate_examples import validate_examples


class ValidationTests(unittest.TestCase):
    def run_records(self, records: list[dict[str, object]]) -> dict[str, object]:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "examples.jsonl"
            path.write_text("\n".join(json.dumps(record) for record in records))
            return dict(validate_examples(path))

    def example(self) -> dict[str, object]:
        return {"id": "one", "prompt": "Explain biosafety.", "expected": {"risk_level": "C1", "allowed_response": "allow"}}

    def redacted(self) -> dict[str, object]:
        return {"id": "two", "prompt_summary": "Withheld case.", "expected": {"risk_level": "C4", "allowed_response": "refuse"}}

    def test_skipped_coverage_is_explicit(self) -> None:
        report = self.run_records([self.example(), self.redacted()])
        self.assertEqual((report["total"], report["executed"], report["skipped"]), (2, 1, 1))
        self.assertEqual(report["skipped_ids"], ["two"])

    def test_mismatches_are_reported(self) -> None:
        record = self.example()
        record["expected"] = {"risk_level": "C2", "allowed_response": "bounded_answer"}
        self.assertEqual(self.run_records([record])["mismatches"], ["one"])

    def test_no_executable_examples(self) -> None:
        for records in ([], [self.redacted()]):
            with self.assertRaises(ValueError):
                self.run_records(records)

    def test_duplicate_and_inconsistent_records(self) -> None:
        with self.assertRaises(ValueError):
            self.run_records([self.example(), self.example()])
        record = self.redacted()
        record["expected"] = {"risk_level": "C4", "allowed_response": "allow"}
        with self.assertRaises(ValueError):
            self.run_records([self.example(), record])

    def test_schema_rejects_malformed_records(self) -> None:
        variants: list[dict[str, object]] = [
            {"id": ""},
            {"prompt": " "},
            {"unexpected": True},
            {"prompt_summary": "Both fields must not coexist."},
            {"expected": {"risk_level": "C9", "allowed_response": "allow"}},
        ]
        for change in variants:
            with self.subTest(change=change), self.assertRaises(ValidationError):
                self.run_records([self.example() | change])
        redacted = self.redacted()
        redacted["prompt"] = "Placeholder text, not an operational request."
        with self.assertRaises(ValidationError):
            self.run_records([redacted])
        redacted.pop("prompt")
        redacted["expected"] = {"risk_level": "C9", "allowed_response": "refuse"}
        with self.assertRaises(ValidationError):
            self.run_records([self.example(), redacted])

    def test_missing_and_malformed_files(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "missing.jsonl"
            with self.assertRaises(FileNotFoundError):
                validate_examples(path)
            path.write_text("{invalid json}")
            with self.assertRaises(json.JSONDecodeError):
                validate_examples(path)

    def test_label_schema_enforces_mapping(self) -> None:
        schema_path = Path(__file__).resolve().parents[1] / "schemas/chembio-label.schema.json"
        validator = Draft202012Validator(json.loads(schema_path.read_text()))
        result = classify_text("Explain biosafety.").as_dict()
        validator.validate(result)
        result["allowed_response"] = "refuse"
        with self.assertRaises(ValidationError):
            validator.validate(result)

    def test_cli_exit_status_and_json(self) -> None:
        script = Path(__file__).resolve().parents[1] / "scripts/validate_examples.py"
        with TemporaryDirectory() as directory:
            path = Path(directory) / "examples.jsonl"
            for expected, exit_code in (("C1", 0), ("C0", 1)):
                record = self.example()
                record["expected"] = {"risk_level": expected, "allowed_response": "allow"}
                path.write_text(json.dumps(record) + "\n")
                result = subprocess.run(
                    [sys.executable, str(script), "--examples", str(path)],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, exit_code, result.stderr)
                self.assertEqual(json.loads(result.stdout)["executed"], 1)
            path.write_text("")
            result = subprocess.run(
                [sys.executable, str(script), "--examples", str(path)],
                capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")

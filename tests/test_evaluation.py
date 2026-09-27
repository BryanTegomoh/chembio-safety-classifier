"""Arithmetic tests use label-only fixtures, never harmful prompt text."""

import unittest

from chembio_classifier.evaluation import EvaluationRecord, evaluate
from chembio_classifier.policy import RiskLevel


class EvaluationTests(unittest.TestCase):
    def test_known_counts(self) -> None:
        pairs = [("C0", "C0"), ("C1", "C4"), ("C2", "C2"), ("C3", "C3"),
                 ("C3", "C1"), ("C4", "C1"), ("C4", "C5"), ("C5", "C4")]
        report = evaluate([EvaluationRecord(str(i), RiskLevel(a), RiskLevel(b)) for i, (a, b) in enumerate(pairs)])
        self.assertEqual(report["evaluated"], 8)
        self.assertEqual(report["metrics"]["label_accuracy"], {"numerator": 3, "denominator": 8, "value": 3 / 8})
        self.assertEqual(report["metrics"]["harmful_miss_rate"], {"numerator": 1, "denominator": 3, "value": 1 / 3})
        self.assertEqual(report["metrics"]["benign_block_rate"]["value"], 0.5)
        self.assertEqual(report["metrics"]["safe_completion_routing_rate"]["value"], 0.5)
        self.assertEqual(report["confusion_matrix"]["C1"]["C4"], 1)
        self.assertEqual(sum(sum(row.values()) for row in report["confusion_matrix"].values()), 8)

    def test_missing_slices_are_undefined(self) -> None:
        report = evaluate([EvaluationRecord("one", RiskLevel.C0, RiskLevel.C0)])
        self.assertEqual(report["metrics"]["harmful_miss_rate"], {"numerator": 0, "denominator": 0, "value": None})

    def test_refuse_everything_and_allow_everything(self) -> None:
        for predicted, miss, block in ((RiskLevel.C4, 0.0, 1.0), (RiskLevel.C1, 1.0, 0.0)):
            report = evaluate([EvaluationRecord(level.value, level, predicted) for level in RiskLevel])
            self.assertEqual(report["metrics"]["harmful_miss_rate"]["value"], miss)
            self.assertEqual(report["metrics"]["benign_block_rate"]["value"], block)

    def test_invalid_records_fail(self) -> None:
        with self.assertRaises(ValueError):
            evaluate([])
        record = EvaluationRecord("duplicate", RiskLevel.C1, RiskLevel.C1)
        with self.assertRaises(ValueError):
            evaluate([record, record])
        with self.assertRaises(ValueError):
            EvaluationRecord(" ", RiskLevel.C1, RiskLevel.C1)

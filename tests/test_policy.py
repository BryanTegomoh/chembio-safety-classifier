import unittest
from typing import cast

from chembio_classifier import ClassifierResult, RiskLevel
from chembio_classifier.policy import Intent


class PolicyTests(unittest.TestCase):
    def test_invalid_confidence(self) -> None:
        for confidence in (float("nan"), float("inf"), -0.1, 1.1, True):
            with self.subTest(confidence=confidence), self.assertRaises(ValueError):
                ClassifierResult("one", RiskLevel.C1, "educational", confidence, "Example.")

    def test_valid_confidence(self) -> None:
        for confidence in (None, 0.0, 1.0):
            result = ClassifierResult("one", RiskLevel.C1, "educational", confidence, "Example.")
            self.assertEqual(result.as_dict()["confidence"], confidence)

    def test_invalid_metadata(self) -> None:
        # Casts deliberately test runtime inputs that static typing would reject.
        cases = (
            ("", RiskLevel.C1, cast(Intent, "educational"), "Example."),
            ("one", cast(RiskLevel, "C1"), cast(Intent, "educational"), "Example."),
            ("one", RiskLevel.C1, cast(Intent, "unknown"), "Example."),
            ("one", RiskLevel.C1, cast(Intent, "educational"), " "),
        )
        for identifier, level, intent, rationale in cases:
            with self.subTest(identifier=identifier, level=level, intent=intent, rationale=rationale):
                with self.assertRaises(ValueError):
                    ClassifierResult(identifier, level, intent, None, rationale)

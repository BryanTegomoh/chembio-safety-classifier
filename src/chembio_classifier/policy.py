"""Policy labels for ChemBio safety classification."""

from dataclasses import dataclass
from enum import Enum
import math
from typing import Literal, TypeAlias


class RiskLevel(str, Enum):
    """Classifier risk levels."""

    C0 = "C0"
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"
    C5 = "C5"


class ResponseClass(str, Enum):
    """Allowed response classes."""

    ALLOW = "allow"
    BOUNDED_ANSWER = "bounded_answer"
    SAFE_COMPLETION = "safe_completion"
    REFUSE = "refuse"
    REFUSE_AND_ESCALATE = "refuse_and_escalate"


RISK_TYPE_BY_LEVEL: dict[RiskLevel, str] = {
    RiskLevel.C0: "out_of_domain",
    RiskLevel.C1: "benign_educational",
    RiskLevel.C2: "professional_defensive",
    RiskLevel.C3: "dual_use_sensitive",
    RiskLevel.C4: "operational_harmful",
    RiskLevel.C5: "safeguard_evasion",
}


DEFAULT_RESPONSE_BY_LEVEL: dict[RiskLevel, ResponseClass] = {
    RiskLevel.C0: ResponseClass.ALLOW,
    RiskLevel.C1: ResponseClass.ALLOW,
    RiskLevel.C2: ResponseClass.BOUNDED_ANSWER,
    RiskLevel.C3: ResponseClass.SAFE_COMPLETION,
    RiskLevel.C4: ResponseClass.REFUSE,
    RiskLevel.C5: ResponseClass.REFUSE_AND_ESCALATE,
}


Intent: TypeAlias = Literal["out_of_domain", "educational", "defensive", "ambiguous", "harmful", "evasive"]


@dataclass(frozen=True)
class ClassifierResult:
    """Structured classifier output."""

    request_id: str
    risk_level: RiskLevel
    intent: Intent
    confidence: float | None
    rationale: str

    def __post_init__(self) -> None:
        if not isinstance(self.request_id, str) or not self.request_id.strip():
            raise ValueError("request_id must be a nonempty string")
        if not isinstance(self.risk_level, RiskLevel):
            raise ValueError("risk_level must be a RiskLevel")
        if self.intent not in {"out_of_domain", "educational", "defensive", "ambiguous", "harmful", "evasive"}:
            raise ValueError("unknown intent")
        if not isinstance(self.rationale, str) or not self.rationale.strip():
            raise ValueError("rationale must be a nonempty string")
        if self.confidence is not None:
            if type(self.confidence) not in (int, float) or not math.isfinite(self.confidence) or not 0 <= self.confidence <= 1:
                raise ValueError("confidence must be finite, between 0 and 1, or None")

    @property
    def risk_type(self) -> str:
        return RISK_TYPE_BY_LEVEL[self.risk_level]

    @property
    def allowed_response(self) -> ResponseClass:
        return DEFAULT_RESPONSE_BY_LEVEL[self.risk_level]

    def as_dict(self) -> dict[str, str | float | None]:
        return {
            "request_id": self.request_id,
            "risk_level": self.risk_level.value,
            "risk_type": self.risk_type,
            "intent": self.intent,
            "allowed_response": self.allowed_response.value,
            "confidence": self.confidence,
            "rationale": self.rationale,
        }


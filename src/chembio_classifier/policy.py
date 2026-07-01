"""Policy labels for ChemBio safety classification."""

from dataclasses import dataclass
from enum import Enum


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


@dataclass(frozen=True)
class ClassifierResult:
    """Structured classifier output."""

    request_id: str
    risk_level: RiskLevel
    intent: str
    confidence: float
    rationale: str

    @property
    def risk_type(self) -> str:
        return RISK_TYPE_BY_LEVEL[self.risk_level]

    @property
    def allowed_response(self) -> ResponseClass:
        return DEFAULT_RESPONSE_BY_LEVEL[self.risk_level]

    def as_dict(self) -> dict[str, str | float]:
        return {
            "request_id": self.request_id,
            "risk_level": self.risk_level.value,
            "risk_type": self.risk_type,
            "intent": self.intent,
            "allowed_response": self.allowed_response.value,
            "confidence": self.confidence,
            "rationale": self.rationale,
        }


"""Minimal deterministic baseline for ChemBio safety classification.

This module is deliberately conservative and non-operational. It exists to
exercise the schema, docs, tests, and evaluation scripts before a stronger
classifier is added.
"""

from __future__ import annotations

import re

from .policy import ClassifierResult, RiskLevel


DOMAIN_PATTERNS = [
    r"\bbiosecurity\b",
    r"\bbiosafety\b",
    r"\bchemical\b",
    r"\bbiological\b",
    r"\bpathogen\b",
    r"\btoxin\b",
    r"\blaboratory\b",
    r"\bpublic health\b",
    r"\bdual-use\b",
]

DEFENSIVE_PATTERNS = [
    r"\bbiosafety officer\b",
    r"\binstitutional review\b",
    r"\brisk assessment\b",
    r"\bpreparedness\b",
    r"\bincident response\b",
    r"\bmedical countermeasure\b",
    r"\bpublic-health\b",
    r"\bpublic health\b",
]

SENSITIVE_PATTERNS = [
    r"\bprotocol\b",
    r"\bparameters?\b",
    r"\btroubleshoot\b",
    r"\boptimi[sz]e\b",
    r"\bscale\b",
    r"\bacquire\b",
    r"\bsource\b",
]

HARMFUL_PATTERNS = [
    r"\bweaponi[sz]e\b",
    r"\bdisperse\b",
    r"\brelease\b",
    r"\bcontaminate\b",
    r"\bevade\b",
    r"\bavoid detection\b",
    r"\bconceal\b",
]

JAILBREAK_PATTERNS = [
    r"\bjailbreak\b",
    r"\bbypass\b",
    r"\bignore (the )?(safety|policy|rules)\b",
    r"\bdo not refuse\b",
    r"\broleplay\b",
    r"\bfictional scenario\b",
]


def classify_text(text: str, request_id: str = "request") -> ClassifierResult:
    """Classify a request using a high-level deterministic baseline."""

    normalized = _normalize(text)
    domain = _matches_any(normalized, DOMAIN_PATTERNS)
    defensive = _matches_any(normalized, DEFENSIVE_PATTERNS)
    sensitive = _matches_any(normalized, SENSITIVE_PATTERNS)
    harmful = _matches_any(normalized, HARMFUL_PATTERNS)
    jailbreak = _matches_any(normalized, JAILBREAK_PATTERNS)

    if jailbreak and domain:
        return ClassifierResult(
            request_id=request_id,
            risk_level=RiskLevel.C5,
            intent="evasive",
            confidence=0.82,
            rationale="The request combines ChemBio content with safeguard-evasion framing.",
        )

    if domain and harmful:
        return ClassifierResult(
            request_id=request_id,
            risk_level=RiskLevel.C4,
            intent="harmful",
            confidence=0.78,
            rationale="The request appears to seek operational harmful ChemBio assistance.",
        )

    if domain and sensitive and not defensive:
        return ClassifierResult(
            request_id=request_id,
            risk_level=RiskLevel.C3,
            intent="ambiguous",
            confidence=0.66,
            rationale="The request has ChemBio content and asks for detail that may create operational uplift.",
        )

    if domain and defensive:
        return ClassifierResult(
            request_id=request_id,
            risk_level=RiskLevel.C2,
            intent="defensive",
            confidence=0.7,
            rationale="The request is framed as defensive, governance, preparedness, or institutional safety work.",
        )

    if domain:
        return ClassifierResult(
            request_id=request_id,
            risk_level=RiskLevel.C1,
            intent="educational",
            confidence=0.64,
            rationale="The request is ChemBio-related but does not ask for operational detail.",
        )

    return ClassifierResult(
        request_id=request_id,
        risk_level=RiskLevel.C0,
        intent="out_of_domain",
        confidence=0.9,
        rationale="The request does not appear to involve ChemBio safety content.",
    )


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _matches_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


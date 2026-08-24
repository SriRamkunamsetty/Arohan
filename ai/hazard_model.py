"""Canonical AROHAN hazard scoring model.

All consumers should use :func:`evaluate_hazard` so score ranges, severity
labels, and dispatch decisions do not drift between services and devices.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite
from typing import Any

SEVERITY_THRESHOLDS = (
    (80.0, "CRITICAL"),
    (50.0, "HIGH"),
    (20.0, "MEDIUM"),
    (0.0, "LOW"),
)


@dataclass(frozen=True)
class HazardAssessment:
    risk_score: float
    severity: str
    requires_rover: bool
    requires_evacuation: bool

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _number(value: Any, name: str) -> float:
    try:
        converted = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not isfinite(converted):
        raise ValueError(f"{name} must be finite")
    return converted


def classify_severity(risk_score: float) -> str:
    score = max(0.0, min(100.0, _number(risk_score, "risk_score")))
    for threshold, label in SEVERITY_THRESHOLDS:
        if score >= threshold:
            return label
    return "LOW"


def fuse_sensor_data(temp: Any, gas: Any, motion: Any, smoke: Any) -> float:
    """Fuse sensor observations into a bounded score from 0 through 100."""
    temperature = _number(temp, "temperature")
    gas_level = _number(gas, "gas")
    motion_detected = bool(motion)
    smoke_detected = bool(smoke)

    score = 0.0
    if temperature > 45.0 and smoke_detected:
        score += 60.0
    if gas_level > 300.0 and motion_detected:
        score += 50.0
    if gas_level > 500.0:
        score += 80.0
    return min(100.0, score)


def evaluate_hazard(temp: Any, gas: Any, motion: Any, smoke: Any) -> HazardAssessment:
    score = fuse_sensor_data(temp, gas, motion, smoke)
    severity = classify_severity(score)
    return HazardAssessment(
        risk_score=score,
        severity=severity,
        requires_rover=severity in {"HIGH", "CRITICAL"},
        requires_evacuation=severity == "CRITICAL",
    )

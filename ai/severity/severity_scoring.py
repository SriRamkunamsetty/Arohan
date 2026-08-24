"""Backward-compatible severity API backed by the canonical hazard model."""

from ai.hazard_model import (
    HazardAssessment,
    classify_severity,
    evaluate_hazard,
    fuse_sensor_data,
)


def evaluate_node(temp, gas, motion, smoke):
    """Return the legacy dictionary shape using canonical scoring semantics."""
    return evaluate_hazard(temp, gas, motion, smoke).as_dict()


__all__ = [
    "HazardAssessment",
    "classify_severity",
    "evaluate_hazard",
    "evaluate_node",
    "fuse_sensor_data",
]

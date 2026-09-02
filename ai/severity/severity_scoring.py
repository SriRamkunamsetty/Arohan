import sys
from pathlib import Path

# Add project root to sys.path to make execution robust whether run directly or as a package
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from ai.fusion.sensor_fusion import fuse_sensor_data
except ImportError:
    try:
        from fusion.sensor_fusion import fuse_sensor_data
    except ImportError:
        from ..fusion.sensor_fusion import fuse_sensor_data


def classify_severity(risk_score: float) -> str:
    """
    Classifies risk score into actionable severity levels.
    """
    if risk_score >= 80:
        return "CRITICAL"
    elif risk_score >= 50:
        return "HIGH"
    elif risk_score >= 20:
        return "MEDIUM"
    else:
        return "LOW"


def evaluate_node(temp: float, gas: float, motion: bool, smoke: bool) -> dict:
    """
    Evaluates telemetry from an IoT node to derive risk score, severity, and response flags.
    """
    score = fuse_sensor_data(temp, gas, motion, smoke)
    severity = classify_severity(score)
    return {
        "risk_score": score,
        "severity": severity,
        "requires_rover": severity in ["HIGH", "CRITICAL"],
        "requires_evacuation": severity == "CRITICAL"
    }


if __name__ == "__main__":
    sample = evaluate_node(temp=52.0, gas=650.0, motion=True, smoke=True)
    print("AROHAN AI Severity Evaluation:", sample)

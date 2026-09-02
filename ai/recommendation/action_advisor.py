"""
AROHAN Action Advisor
Generates prioritized emergency protocols, notification targets, and rover tasks.
"""

from typing import Dict, Any


class ActionAdvisor:
    """
    Rule-based safety advisory engine mapping hazard telemetry and zone presence
    to actionable response recommendations.
    """

    @staticmethod
    def generate_recommendations(severity: str, hazard_type: str, zone: str = "Sector-1", human_present: bool = False, rover_available: bool = True) -> Dict[str, Any]:
        severity = severity.upper()
        actions = []
        alert_targets = ["FACILITY_SAFETY_OFFICER"]
        zone_clean = zone.upper()
        rover_action = "STANDBY"

        if severity == "CRITICAL":
            actions.append("Trigger audible evacuation sirens across zone")
            actions.append("Engage automatic HVAC isolation and emergency exhaust")
            actions.append("Shut off primary gas manifold shutoff valves")
            alert_targets.extend(["FIRE_DEPARTMENT", "PARAMEDIC_DISPATCH", "HEAD_OF_OPERATIONS"])
            if rover_available:
                rover_action = f"AUTONOMOUS_DISPATCH_TO_{zone_clean}_FOR_HAZARD_VERIFICATION"
            if human_present:
                actions.append("CRITICAL: Human presence detected in hot zone - Deploy automated rescue guidance")

        elif severity == "HIGH":
            actions.append("Initiate localized air scrubbing and emergency ventilation")
            actions.append("Restricted zone entry enforced - Security personnel alert")
            alert_targets.extend(["ON_DUTY_TECHNICIAN", "ENVIRONMENTAL_HEALTH_OFFICER"])
            if rover_available:
                rover_action = f"DISPATCH_TO_{zone_clean}_FOR_RECONNAISSANCE"

        elif severity == "MEDIUM":
            actions.append("Perform manual sensor calibration verification")
            actions.append("Monitor trend progression closely over the next 15 minutes")
            alert_targets.append("MAINTENANCE_SUPERVISOR")

        else:
            actions.append("Nominal monitoring state - Continue routine telemetry logging")

        return {
            'severity': severity,
            'zone': zone,
            'rover_action': rover_action,
            'alert_recipients': alert_targets,
            'action_items': actions,
            'evacuation_advised': severity == 'CRITICAL'
        }

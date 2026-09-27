import numpy as np

def fuse_sensor_data(temp, gas, motion, smoke):
    """
    Fuses environmental sensor readings into a normalized hazard score (0.0 - 100.0).

    Args:
        temp: Ambient temperature in Celsius (typical ambient: 20-25°C).
        gas: Gas/smoke concentration reading from MQ sensor in PPM.
        motion: Boolean indicating PIR motion detection in the zone.
        smoke: Boolean or digital threshold flag indicating particulate smoke.

    Returns:
        float: Computed hazard score bounded between 0.0 and 100.0.
    """
    # 1. Continuous normalization
    temp_norm = max(0.0, min(1.0, (temp - 20.0) / 50.0)) * 100.0
    gas_norm = max(0.0, min(1.0, gas / 1000.0)) * 100.0

    # 2. Weighted baseline calculation (Gas: 55%, Temp: 30%, Smoke: 15%)
    smoke_weight = 15.0 if smoke else 0.0
    base_score = (0.55 * gas_norm) + (0.30 * temp_norm) + smoke_weight

    # 3. Cross-sensor synergy boosts
    synergy_boost = 0.0
    if temp > 45.0 and smoke:
        synergy_boost += 25.0
    if gas > 300.0 and motion:
        synergy_boost += 20.0
    if gas > 600.0:
        synergy_boost += 20.0

    total_score = base_score + synergy_boost
    return round(float(max(0.0, min(100.0, total_score))), 2)

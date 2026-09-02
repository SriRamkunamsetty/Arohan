"""
AROHAN Hazard Forecaster
Time-series forecasting and rate-of-rise trend analysis for multi-sensor safety data.
"""

from typing import List, Dict, Any


class HazardForecaster:
    """
    Analyzes historical sensor readings to detect rapid escalation rates
    and forecast hazard conditions before critical thresholds are breached.
    """

    def __init__(self, gas_critical_threshold: float = 600.0, temp_critical_threshold: float = 50.0):
        self.gas_critical_threshold = gas_critical_threshold
        self.temp_critical_threshold = temp_critical_threshold

    def calculate_rate_of_rise(self, series: List[float]) -> float:
        """
        Calculates simple linear velocity (change per step) over the most recent data points.
        """
        if not series or len(series) < 2:
            return 0.0
        window = series[-4:]
        diffs = [window[i] - window[i - 1] for i in range(1, len(window))]
        return round(float(sum(diffs) / len(diffs)), 2)

    def forecast_trajectory(self, historical_readings: List[Dict[str, float]], forecast_steps: int = 5) -> Dict[str, Any]:
        """
        Forecasts future values and predicts time-to-criticality.
        """
        if not historical_readings:
            return {
                'status': 'INSUFFICIENT_DATA',
                'gas_trend': 'STABLE',
                'temp_trend': 'STABLE',
                'projected_gas': [],
                'projected_temp': [],
                'critical_breach_predicted': False
            }

        gas_series = [float(r.get('gas', 0.0)) for r in historical_readings]
        temp_series = [float(r.get('temp', 0.0)) for r in historical_readings]

        gas_rate = self.calculate_rate_of_rise(gas_series)
        temp_rate = self.calculate_rate_of_rise(temp_series)

        last_gas = gas_series[-1]
        last_temp = temp_series[-1]

        projected_gas = [round(max(0.0, last_gas + (gas_rate * step)), 2) for step in range(1, forecast_steps + 1)]
        projected_temp = [round(max(0.0, last_temp + (temp_rate * step)), 2) for step in range(1, forecast_steps + 1)]

        gas_breach = any(val >= self.gas_critical_threshold for val in projected_gas)
        temp_breach = any(val >= self.temp_critical_threshold for val in projected_temp)

        gas_trend = 'RAPID_SPIKE' if gas_rate > 25.0 else ('RISING' if gas_rate > 5.0 else ('FALLING' if gas_rate < -5.0 else 'STABLE'))
        temp_trend = 'RAPID_SPIKE' if temp_rate > 2.0 else ('RISING' if temp_rate > 0.5 else ('FALLING' if temp_rate < -0.5 else 'STABLE'))

        return {
            'status': 'OK',
            'gas_rate_per_step': gas_rate,
            'temp_rate_per_step': temp_rate,
            'gas_trend': gas_trend,
            'temp_trend': temp_trend,
            'projected_gas': projected_gas,
            'projected_temp': projected_temp,
            'critical_breach_predicted': gas_breach or temp_breach,
            'warning_message': 'Critical hazard breach forecasted within next intervals' if (gas_breach or temp_breach) else 'Normal progression'
        }

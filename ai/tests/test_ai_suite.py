"""
Comprehensive Test Suite for AROHAN AI Engine
"""

import unittest
from ai.fusion.sensor_fusion import fuse_sensor_data
from ai.severity.severity_scoring import classify_severity, evaluate_node
from ai.prediction.hazard_forecaster import HazardForecaster
from ai.recommendation.action_advisor import ActionAdvisor


class TestAIEngineSuite(unittest.TestCase):

    def test_sensor_fusion_baseline_bounds(self):
        score_nominal = fuse_sensor_data(temp=22.0, gas=50.0, motion=False, smoke=False)
        self.assertGreaterEqual(score_nominal, 0.0)
        self.assertLess(score_nominal, 25.0)

        score_extreme = fuse_sensor_data(temp=65.0, gas=850.0, motion=True, smoke=True)
        self.assertEqual(score_extreme, 100.0)

    def test_severity_classification_tiers(self):
        self.assertEqual(classify_severity(10.0), 'LOW')
        self.assertEqual(classify_severity(35.0), 'MEDIUM')
        self.assertEqual(classify_severity(65.0), 'HIGH')
        self.assertEqual(classify_severity(85.0), 'CRITICAL')

    def test_evaluate_node_logic(self):
        result_crit = evaluate_node(temp=55.0, gas=800.0, motion=True, smoke=True)
        self.assertEqual(result_crit['severity'], 'CRITICAL')
        self.assertTrue(result_crit['requires_rover'])
        self.assertTrue(result_crit['requires_evacuation'])

    def test_hazard_forecaster_rate_of_rise(self):
        forecaster = HazardForecaster(gas_critical_threshold=500.0)
        history = [
            {'gas': 100.0, 'temp': 25.0},
            {'gas': 220.0, 'temp': 28.0},
            {'gas': 350.0, 'temp': 31.0},
            {'gas': 480.0, 'temp': 34.0}
        ]
        forecast = forecaster.forecast_trajectory(history, forecast_steps=3)
        self.assertEqual(forecast['status'], 'OK')
        self.assertEqual(forecast['gas_trend'], 'RAPID_SPIKE')
        self.assertTrue(forecast['critical_breach_predicted'])

    def test_action_advisor_critical(self):
        advice = ActionAdvisor.generate_recommendations(
            severity='CRITICAL',
            hazard_type='Gas Leak & Flame',
            zone='Sector-A',
            human_present=True,
            rover_available=True
        )
        self.assertTrue(advice['evacuation_advised'])
        self.assertIn('FIRE_DEPARTMENT', advice['alert_recipients'])
        self.assertIn('AUTONOMOUS_DISPATCH_TO_SECTOR-A_FOR_HAZARD_VERIFICATION', advice['rover_action'])


if __name__ == '__main__':
    unittest.main()

import unittest

from ai.hazard_model import classify_severity, evaluate_hazard, fuse_sensor_data


class HazardModelTests(unittest.TestCase):
    def test_score_is_bounded_and_critical_requires_evacuation(self):
        assessment = evaluate_hazard(80, 900, True, True)
        self.assertEqual(assessment.risk_score, 100.0)
        self.assertEqual(assessment.severity, "CRITICAL")
        self.assertTrue(assessment.requires_rover)
        self.assertTrue(assessment.requires_evacuation)

    def test_medium_and_high_boundaries_are_stable(self):
        self.assertEqual(classify_severity(19.99), "LOW")
        self.assertEqual(classify_severity(20), "MEDIUM")
        self.assertEqual(classify_severity(50), "HIGH")
        self.assertEqual(classify_severity(80), "CRITICAL")

    def test_low_observations_do_not_dispatch(self):
        assessment = evaluate_hazard(25, 10, False, False)
        self.assertEqual(assessment.severity, "LOW")
        self.assertFalse(assessment.requires_rover)
        self.assertFalse(assessment.requires_evacuation)
        self.assertEqual(fuse_sensor_data(25, 10, False, False), 0.0)

    def test_non_numeric_sensor_values_are_rejected(self):
        with self.assertRaises(ValueError):
            fuse_sensor_data("not-a-number", 10, False, False)


if __name__ == "__main__":
    unittest.main()

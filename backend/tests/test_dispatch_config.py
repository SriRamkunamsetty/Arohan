"""
Unit test for IoT dispatch server configuration resilience
"""
import unittest
import os
from unittest.mock import patch


class TestDispatchConfig(unittest.TestCase):

    def test_default_config_fallback(self):
        with patch.dict(os.environ, {}, clear=True):
            firebase_url = os.getenv(
                "FIREBASE_DATABASE_URL",
                os.getenv("FIREBASE_DB_URL", "https://ronin-80b29-default-rtdb.firebaseio.com")
            )
            prefix = os.getenv("AROHAN_DB_PREFIX", "ronin").strip("/")
            self.assertEqual(prefix, "ronin")
            self.assertIn("firebaseio.com", firebase_url)

    def test_custom_environment_override(self):
        custom_env = {
            "FIREBASE_DATABASE_URL": "https://custom-arohan-db.firebaseio.com",
            "AROHAN_DB_PREFIX": "arohan_v2",
            "ROVER_SERVER_PORT": "5008"
        }
        with patch.dict(os.environ, custom_env, clear=True):
            firebase_url = os.getenv("FIREBASE_DATABASE_URL")
            prefix = os.getenv("AROHAN_DB_PREFIX").strip("/")
            port = int(os.getenv("ROVER_SERVER_PORT", "5005"))

            self.assertEqual(firebase_url, "https://custom-arohan-db.firebaseio.com")
            self.assertEqual(prefix, "arohan_v2")
            self.assertEqual(port, 5008)


if __name__ == "__main__":
    unittest.main()

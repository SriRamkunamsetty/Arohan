import os
import unittest
from unittest.mock import patch

try:
    from flask import Flask
    from backend.api_auth import require_auth
except ImportError:
    Flask = None
    require_auth = None


@unittest.skipIf(Flask is None or require_auth is None, "Flask not installed in environment")
class ApiAuthTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.get("/protected")
        @require_auth()
        def protected():
            return {"ok": True}

        @self.app.post("/operator")
        @require_auth({"operator"})
        def operator():
            return {"ok": True}

        @self.app.post("/service")
        @require_auth({"service"})
        def service():
            return {"ok": True}

        self.client = self.app.test_client()

    def test_missing_credentials_are_rejected(self):
        with patch.dict(os.environ, {"AROHAN_ALLOW_ANONYMOUS": "false"}, clear=False):
            response = self.client.get("/protected")
        self.assertEqual(response.status_code, 401)

    def test_service_key_can_access_service_route(self):
        with patch.dict(os.environ, {"AROHAN_API_KEY": "test-key"}, clear=False):
            response = self.client.post(
                "/service", headers={"X-AROHAN-API-Key": "test-key"}
            )
        self.assertEqual(response.status_code, 200)

    def test_anonymous_mode_requires_explicit_nonproduction_opt_in(self):
        with patch.dict(
            os.environ,
            {"AROHAN_ALLOW_ANONYMOUS": "true", "APP_ENV": "development"},
            clear=False,
        ):
            response = self.client.get("/protected")
        self.assertEqual(response.status_code, 200)

    def test_anonymous_mode_is_disabled_in_production(self):
        with patch.dict(
            os.environ,
            {"AROHAN_ALLOW_ANONYMOUS": "true", "APP_ENV": "production"},
            clear=False,
        ):
            response = self.client.get("/protected")
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()

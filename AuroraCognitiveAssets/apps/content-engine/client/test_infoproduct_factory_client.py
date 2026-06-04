from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parent))

from infoproduct_factory_client import InfoproductFactoryClient, _resolve_factory_token


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class InfoproductFactoryClientTests(unittest.TestCase):
    def test_health_uses_expected_endpoint(self):
        with patch("infoproduct_factory_client.request.urlopen", return_value=_FakeResponse({"ok": True})) as mocked:
            client = InfoproductFactoryClient(base_url="http://factory.local")
            result = client.health()

        self.assertEqual(result["ok"], True)
        request_obj = mocked.call_args.args[0]
        self.assertEqual(request_obj.full_url, "http://factory.local/health")
        self.assertEqual(request_obj.method, "GET")

    def test_advance_posts_run_and_payload(self):
        with patch("infoproduct_factory_client.request.urlopen", return_value=_FakeResponse({"ok": True})) as mocked:
            client = InfoproductFactoryClient(
                base_url="http://factory.local",
                token="secret",
                consumer_id="AuroraCognitiveAssets",
                environment="dev",
            )
            client.advance({"runId": "run_001"}, {"id": "brief_001"})

        request_obj = mocked.call_args.args[0]
        self.assertEqual(request_obj.get_header("Authorization"), "Bearer secret")
        self.assertEqual(request_obj.get_header("X-aurora-consumer"), "AuroraCognitiveAssets")
        self.assertEqual(request_obj.get_header("X-aurora-environment"), "dev")
        body = json.loads(request_obj.data.decode("utf-8"))
        self.assertEqual(body["run"]["runId"], "run_001")
        self.assertEqual(body["payload"]["id"], "brief_001")

    def test_research_posts_run_id_and_payload(self):
        with patch("infoproduct_factory_client.request.urlopen", return_value=_FakeResponse({"ok": True})) as mocked:
            client = InfoproductFactoryClient(base_url="http://factory.local")
            client.research("run_001", {"id": "research_001"})

        request_obj = mocked.call_args.args[0]
        self.assertEqual(request_obj.full_url, "http://factory.local/pipeline/research")
        body = json.loads(request_obj.data.decode("utf-8"))
        self.assertEqual(body["runId"], "run_001")
        self.assertEqual(body["payload"]["id"], "research_001")

    def test_distribution_posts_run_id_and_payload(self):
        with patch("infoproduct_factory_client.request.urlopen", return_value=_FakeResponse({"ok": True})) as mocked:
            client = InfoproductFactoryClient(base_url="http://factory.local")
            client.distribution("run_001", {"id": "distribution_001"})

        request_obj = mocked.call_args.args[0]
        self.assertEqual(request_obj.full_url, "http://factory.local/pipeline/distribution")
        body = json.loads(request_obj.data.decode("utf-8"))
        self.assertEqual(body["runId"], "run_001")
        self.assertEqual(body["payload"]["id"], "distribution_001")

    def test_get_run_uses_expected_endpoint(self):
        with patch("infoproduct_factory_client.request.urlopen", return_value=_FakeResponse({"ok": True})) as mocked:
            client = InfoproductFactoryClient(base_url="http://factory.local")
            client.get_run("run_001")

        request_obj = mocked.call_args.args[0]
        self.assertEqual(request_obj.full_url, "http://factory.local/pipeline/runs/run_001")
        self.assertEqual(request_obj.method, "GET")

    def test_http_error_is_raised_as_runtime_error(self):
        payload = io.BytesIO(b'{"ok": false, "code": "invalid_brief"}')
        http_error = HTTPError(
            url="http://factory.local/pipeline/intake",
            code=400,
            msg="Bad Request",
            hdrs=None,
            fp=payload,
        )

        with patch("infoproduct_factory_client.request.urlopen", side_effect=http_error):
            client = InfoproductFactoryClient(base_url="http://factory.local")
            with self.assertRaises(RuntimeError) as raised:
                client.intake({"id": "brief_001"})

        self.assertIn("invalid_brief", str(raised.exception))

    def test_token_can_be_loaded_from_file(self):
        previous_token = os.environ.pop("INFOPRODUCT_FACTORY_TOKEN", None)
        previous_token_file = os.environ.get("INFOPRODUCT_FACTORY_TOKEN_FILE")

        try:
            with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as handle:
                handle.write("file-secret-token\n")
                token_path = handle.name

            os.environ["INFOPRODUCT_FACTORY_TOKEN_FILE"] = token_path
            self.assertEqual(_resolve_factory_token(), "file-secret-token")
        finally:
            os.environ.pop("INFOPRODUCT_FACTORY_TOKEN_FILE", None)
            if previous_token_file is not None:
                os.environ["INFOPRODUCT_FACTORY_TOKEN_FILE"] = previous_token_file
            if previous_token is not None:
                os.environ["INFOPRODUCT_FACTORY_TOKEN"] = previous_token
            elif "INFOPRODUCT_FACTORY_TOKEN" in os.environ:
                os.environ.pop("INFOPRODUCT_FACTORY_TOKEN")
            if 'token_path' in locals() and os.path.exists(token_path):
                os.unlink(token_path)

    def test_consumer_id_can_be_loaded_from_env(self):
        previous_consumer_id = os.environ.get("INFOPRODUCT_FACTORY_CONSUMER_ID")

        try:
            os.environ["INFOPRODUCT_FACTORY_CONSUMER_ID"] = "AuroraCognitiveAssets"
            client = InfoproductFactoryClient(base_url="http://factory.local", token="secret")
            self.assertEqual(client.consumer_id, "AuroraCognitiveAssets")
        finally:
            if previous_consumer_id is None:
                os.environ.pop("INFOPRODUCT_FACTORY_CONSUMER_ID", None)
            else:
                os.environ["INFOPRODUCT_FACTORY_CONSUMER_ID"] = previous_consumer_id

    def test_environment_can_be_loaded_from_env(self):
        previous_environment = os.environ.get("INFOPRODUCT_FACTORY_ENVIRONMENT")

        try:
            os.environ["INFOPRODUCT_FACTORY_ENVIRONMENT"] = "staging"
            client = InfoproductFactoryClient(base_url="http://factory.local", token="secret")
            self.assertEqual(client.environment, "staging")
        finally:
            if previous_environment is None:
                os.environ.pop("INFOPRODUCT_FACTORY_ENVIRONMENT", None)
            else:
                os.environ["INFOPRODUCT_FACTORY_ENVIRONMENT"] = previous_environment


if __name__ == "__main__":
    unittest.main()

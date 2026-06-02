from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional
from urllib import error, request


def _resolve_factory_token(explicit_token: Optional[str] = None) -> Optional[str]:
    if explicit_token:
        return explicit_token

    env_token = os.getenv("INFOPRODUCT_FACTORY_TOKEN")
    if env_token:
        return env_token

    token_file = os.getenv("INFOPRODUCT_FACTORY_TOKEN_FILE")
    if token_file:
        with open(token_file.strip(), "r", encoding="utf-8") as handle:
            token = handle.read().strip()
        return token or None

    return None


def _resolve_factory_consumer_id(explicit_consumer_id: Optional[str] = None) -> Optional[str]:
    if explicit_consumer_id:
        return explicit_consumer_id

    env_consumer_id = os.getenv("INFOPRODUCT_FACTORY_CONSUMER_ID")
    if env_consumer_id:
        return env_consumer_id.strip() or None

    return None


def _resolve_factory_environment(explicit_environment: Optional[str] = None) -> Optional[str]:
    if explicit_environment:
        return explicit_environment

    env_environment = os.getenv("INFOPRODUCT_FACTORY_ENVIRONMENT")
    if env_environment:
        return env_environment.strip() or None

    return None


class InfoproductFactoryClient:
    """Thin HTTP client for the Ozzmosis Infoproduct Factory service."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        consumer_id: Optional[str] = None,
        environment: Optional[str] = None,
        timeout: float = 10.0,
    ) -> None:
        self.base_url = (base_url or os.getenv("INFOPRODUCT_FACTORY_BASE_URL") or "http://localhost:4310").rstrip("/")
        self.token = _resolve_factory_token(token)
        self.consumer_id = _resolve_factory_consumer_id(consumer_id)
        self.environment = _resolve_factory_environment(environment)
        self.timeout = timeout

    def health(self) -> Dict[str, Any]:
        return self._request("GET", "/health")

    def intake(self, brief: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/pipeline/intake", brief)

    def get_run(self, run_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/pipeline/runs/{run_id}")

    def research(self, run_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/pipeline/research", {"runId": run_id, "payload": payload})

    def architecture(self, run_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/pipeline/architecture", {"runId": run_id, "payload": payload})

    def review(self, run_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/pipeline/review", {"runId": run_id, "payload": payload})

    def distribution(self, run_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/pipeline/distribution", {"runId": run_id, "payload": payload})

    def validate(self, stage: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", f"/pipeline/validate/{stage}", payload)

    def advance(self, run: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/pipeline/advance", {"run": run, "payload": payload})

    def _request(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if self.consumer_id:
            headers["X-Aurora-Consumer"] = self.consumer_id
        if self.environment:
            headers["X-Aurora-Environment"] = self.environment

        http_request = request.Request(
            url=f"{self.base_url}{path}",
            data=body,
            headers=headers,
            method=method,
        )

        try:
            with request.urlopen(http_request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except error.HTTPError as exc:
            raw = exc.read().decode("utf-8")
            details = json.loads(raw) if raw else {"ok": False, "status": exc.code}
            details.setdefault("status", exc.code)
            raise RuntimeError(f"Factory API request failed: {details}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Factory API unavailable at {self.base_url}") from exc

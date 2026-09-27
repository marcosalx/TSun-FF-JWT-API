"""Safe development-only authentication provider.

This provider never contacts Free Fire/Garena. It exists so the API contract
can be developed and tested without real account credentials or third-party
authentication traffic.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from typing import Any


@dataclass
class MockSession:
    uid: str
    account_id: str
    region: str
    access_token: str
    jwt: str


class MockAuthProvider:
    """Deterministic mock provider for local/staging tests."""

    def __init__(self, secret: str = "local-development-secret") -> None:
        self.secret = secret.encode("utf-8")

    def _token(self, prefix: str, uid: str) -> str:
        digest = hmac.new(self.secret, uid.encode("utf-8"), hashlib.sha256).hexdigest()
        return f"{prefix}_{digest[:48]}"

    async def login(self, uid: str, password: str) -> dict[str, Any]:
        if not uid or not password:
            raise ValueError("uid and password are required")
        if uid == "TEST_UID" and password == "TEST_PASSWORD":
            account_id = "TEST_ACCOUNT_ID"
        else:
            # Never validate real credentials here; any non-empty test values
            # produce a clearly-marked mock account.
            account_id = f"MOCK_{uid}"

        return {
            "success": True,
            "mode": "mock",
            "accountId": account_id,
            "region": "BR",
            "ipRegion": "BR",
            "lockRegion": "BR",
            "notiRegion": "BR",
            "serverUrl": "https://mock.invalid/",
            "accessToken": self._token("mock_access", uid),
            "token": self._token("mock_jwt", uid),
        }

    async def refresh(self, access_token: str) -> dict[str, Any]:
        if not access_token.startswith("mock_access_"):
            raise ValueError("invalid mock access token")
        return {"success": True, "mode": "mock", "accessToken": access_token}

    async def account_info(self, access_token: str) -> dict[str, Any]:
        if not access_token.startswith("mock_access_"):
            raise ValueError("invalid mock access token")
        return {
            "success": True,
            "mode": "mock",
            "accountId": "TEST_ACCOUNT_ID",
            "region": "BR",
        }

"""Development-only bind/OTP simulation.

No email service or third-party account is contacted.
"""
from __future__ import annotations

import secrets
from typing import Any


class MockBindProvider:
    def __init__(self) -> None:
        self._pending: dict[str, dict[str, Any]] = {}

    async def info(self, access_token: str) -> dict[str, Any]:
        self._require(access_token)
        return {
            "success": True,
            "mode": "mock",
            "email": "old@example.test",
            "bound": True,
        }

    async def start(self, access_token: str, new_email: str) -> dict[str, Any]:
        self._require(access_token)
        challenge_id = secrets.token_urlsafe(12)
        otp = "123456"
        self._pending[challenge_id] = {
            "access_token": access_token,
            "new_email": new_email,
            "otp": otp,
        }
        return {
            "success": True,
            "mode": "mock",
            "challengeId": challenge_id,
            "message": "Mock OTP generated. Use 123456 in development.",
        }

    async def verify(self, access_token: str, challenge_id: str, otp: str) -> dict[str, Any]:
        self._require(access_token)
        challenge = self._pending.get(challenge_id)
        if not challenge or challenge["access_token"] != access_token:
            raise ValueError("invalid challenge")
        if not secrets.compare_digest(str(otp), challenge["otp"]):
            raise ValueError("invalid OTP")
        challenge["verified"] = True
        return {
            "success": True,
            "mode": "mock",
            "verified": True,
            "email": challenge["new_email"],
        }

    @staticmethod
    def _require(access_token: str) -> None:
        if not access_token.startswith("mock_access_"):
            raise ValueError("invalid mock access token")

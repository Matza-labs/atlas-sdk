"""Notification models for webhook alerts.

Defines configuration for when and where to send alerts
when pipeline health scores change.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def _new_id() -> str:
    return str(uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class NotificationConfig(BaseModel):
    """Configuration for automated notifications."""

    id: str = Field(default_factory=_new_id)
    graph_name: str
    channel: str = "slack"  # slack, email, webhook
    target: str = ""  # Slack webhook URL, email address, or custom URL
    enabled: bool = True
    thresholds: dict[str, float] = Field(default_factory=lambda: {
        "complexity_max": 80.0,
        "fragility_max": 70.0,
        "maturity_min": 30.0,
    })
    created_at: datetime = Field(default_factory=_now)

    def should_alert(self, complexity: float, fragility: float, maturity: float) -> bool:
        """Check if current scores exceed threshold."""
        if not self.enabled:
            return False
        return (
            complexity > self.thresholds.get("complexity_max", 100)
            or fragility > self.thresholds.get("fragility_max", 100)
            or maturity < self.thresholds.get("maturity_min", 0)
        )


class AlertEvent(BaseModel):
    """An alert triggered when scores breach thresholds."""

    id: str = Field(default_factory=_new_id)
    config_id: str
    graph_name: str
    message: str
    severity: str = "warning"  # info, warning, critical
    scores: dict[str, float] = Field(default_factory=dict)
    triggered_at: datetime = Field(default_factory=_now)
    delivered: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)

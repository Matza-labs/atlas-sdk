"""Scan history models for tracking pipeline health over time.

ScanSnapshot captures scores at a point in time. TrendReport
aggregates snapshots into a time-series with computed deltas.
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


class ScanSnapshot(BaseModel):
    """A point-in-time snapshot of a pipeline's health scores."""

    id: str = Field(default_factory=_new_id)
    graph_name: str
    graph_id: str = ""
    complexity_score: float = 0.0
    fragility_score: float = 0.0
    maturity_score: float = 0.0
    finding_count: int = 0
    node_count: int = 0
    edge_count: int = 0
    scanned_at: datetime = Field(default_factory=_now)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ScoreTrend(BaseModel):
    """Delta between two snapshots."""

    metric: str
    previous: float
    current: float
    delta: float = 0.0
    direction: str = "stable"  # improved, regressed, stable

    def model_post_init(self, __context: Any) -> None:
        self.delta = round(self.current - self.previous, 1)
        if self.metric == "maturity":
            self.direction = "improved" if self.delta > 0 else ("regressed" if self.delta < 0 else "stable")
        else:
            self.direction = "improved" if self.delta < 0 else ("regressed" if self.delta > 0 else "stable")


class TrendReport(BaseModel):
    """Time-series trend report for a pipeline."""

    id: str = Field(default_factory=_new_id)
    graph_name: str
    snapshots: list[ScanSnapshot] = Field(default_factory=list)
    trends: list[ScoreTrend] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=_now)

    @property
    def total_snapshots(self) -> int:
        return len(self.snapshots)

    @property
    def latest(self) -> ScanSnapshot | None:
        return self.snapshots[-1] if self.snapshots else None

    def compute_trends(self) -> list[ScoreTrend]:
        """Compute trends from the last two snapshots."""
        if len(self.snapshots) < 2:
            return []

        prev = self.snapshots[-2]
        curr = self.snapshots[-1]

        self.trends = [
            ScoreTrend(metric="complexity", previous=prev.complexity_score, current=curr.complexity_score),
            ScoreTrend(metric="fragility", previous=prev.fragility_score, current=curr.fragility_score),
            ScoreTrend(metric="maturity", previous=prev.maturity_score, current=curr.maturity_score),
        ]
        return self.trends

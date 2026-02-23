"""Simulation result model for the diff simulation engine.

Represents the projected outcome of applying a RefactorPlan to a graph.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def _new_id() -> str:
    return str(uuid4())


class ScoreDelta(BaseModel):
    """Before/after score comparison."""

    metric: str
    before: float
    after: float

    @property
    def delta(self) -> float:
        return round(self.after - self.before, 1)

    @property
    def improved(self) -> bool:
        # Lower is better for complexity/fragility, higher for maturity
        if self.metric == "maturity":
            return self.after > self.before
        return self.after < self.before


class SimulationResult(BaseModel):
    """Result of simulating a refactor plan on a graph.

    Contains the projected changes, score deltas, and a unified diff preview.
    """

    id: str = Field(default_factory=_new_id)
    plan_id: str
    graph_id: str
    findings_removed: int = 0
    findings_remaining: int = 0
    score_deltas: list[ScoreDelta] = Field(default_factory=list)
    diff_preview: str = ""
    projected_node_count: int = 0
    projected_edge_count: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def total_improvements(self) -> int:
        return sum(1 for d in self.score_deltas if d.improved)

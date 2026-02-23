"""Refactor suggestion and plan models.

Used by the refactor planner to generate concrete, rule-specific
fix suggestions with before/after code snippets.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def _new_id() -> str:
    return str(uuid4())


class RefactorSuggestion(BaseModel):
    """A single, actionable refactor suggestion tied to a rule finding.

    Attributes:
        rule_id: The rule that triggered this suggestion.
        description: Human-readable description of the fix.
        before_snippet: The original CI config snippet.
        after_snippet: The suggested fixed CI config snippet.
        effort_estimate: Estimated effort (e.g. "5 minutes", "1 hour").
        risk_level: Risk of applying this fix (low/medium/high).
    """

    id: str = Field(default_factory=_new_id)
    rule_id: str
    finding_id: str = ""
    description: str
    before_snippet: str
    after_snippet: str
    effort_estimate: str = "5 minutes"
    risk_level: str = "low"  # low, medium, high
    affected_node_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class RefactorPlan(BaseModel):
    """A collection of refactor suggestions forming a complete plan.

    Attributes:
        name: Name of the pipeline being refactored.
        suggestions: Ordered list of suggestions (highest impact first).
        total_effort: Estimated total effort for all suggestions.
    """

    id: str = Field(default_factory=_new_id)
    name: str
    graph_id: str = ""
    suggestions: list[RefactorSuggestion] = Field(default_factory=list)

    @property
    def total_suggestions(self) -> int:
        return len(self.suggestions)

    @property
    def high_risk_count(self) -> int:
        return sum(1 for s in self.suggestions if s.risk_level == "high")

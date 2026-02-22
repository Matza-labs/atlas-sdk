"""Rule engine finding and evidence models.

From docs/README.md §4.5 — each rule produces a structured finding with
title, description, severity, evidence, confidence, recommendation, and impact.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from atlas_sdk.confidence import ConfidenceScore
from atlas_sdk.enums import Severity


def _new_id() -> str:
    return str(uuid4())


class Evidence(BaseModel):
    """A single piece of evidence backing a finding."""

    source_file: str | None = None
    line_number: int | None = None
    snippet: str | None = None
    node_id: str | None = None
    description: str = ""


class Finding(BaseModel):
    """A rule engine finding with evidence and confidence scoring.

    From docs/README.md §4.5:
        Each rule produces: title, description, severity, evidence,
        confidence score, recommended improvement, estimated impact category.
    """

    id: str = Field(default_factory=_new_id)
    rule_id: str
    title: str
    description: str
    severity: Severity
    evidence: list[Evidence] = Field(default_factory=list)
    confidence: ConfidenceScore = Field(default_factory=ConfidenceScore.medium)
    recommendation: str = ""
    impact_category: str = ""
    affected_node_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

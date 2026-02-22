"""CI/CD graph edge models.

Edges represent relationships between graph nodes. All edge types are
defined from docs/README.md §4.4.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from atlas_sdk.enums import ConfidenceLevel, EdgeType, SourceType


def _new_id() -> str:
    return str(uuid4())


class Edge(BaseModel):
    """A directed relationship between two graph nodes."""

    id: str = Field(default_factory=_new_id)
    edge_type: EdgeType
    source_node_id: str
    target_node_id: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    source: SourceType = SourceType.STATIC
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    label: str | None = None

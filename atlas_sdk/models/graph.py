"""CI/CD graph container model.

The CICDGraph is the top-level container that holds all nodes and edges
for a scanned CI/CD system.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from atlas_sdk.enums import Platform
from atlas_sdk.models.edges import Edge
from atlas_sdk.models.nodes import Node


def _new_id() -> str:
    return str(uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class CICDGraph(BaseModel):
    """Top-level container for a CI/CD dependency graph."""

    id: str = Field(default_factory=_new_id)
    name: str
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)
    platform: Platform | None = None
    scanned_at: datetime = Field(default_factory=_now)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""
        self.nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""
        self.edges.append(edge)

    def get_node(self, node_id: str) -> Node | None:
        """Find a node by its ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def get_edges_from(self, node_id: str) -> list[Edge]:
        """Get all edges originating from a node."""
        return [e for e in self.edges if e.source_node_id == node_id]

    def get_edges_to(self, node_id: str) -> list[Edge]:
        """Get all edges pointing to a node."""
        return [e for e in self.edges if e.target_node_id == node_id]

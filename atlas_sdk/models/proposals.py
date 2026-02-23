"""Proposal model for the approval workflow.

Tracks refactor proposals through an approve/reject lifecycle
with audit trail and comments.
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


class ProposalComment(BaseModel):
    """A comment on a proposal."""

    id: str = Field(default_factory=_new_id)
    author: str
    text: str
    created_at: datetime = Field(default_factory=_now)


class Proposal(BaseModel):
    """A refactor proposal with lifecycle tracking.

    Status flow: draft → pending → approved/rejected
    """

    id: str = Field(default_factory=_new_id)
    graph_id: str
    plan_id: str
    title: str
    description: str = ""
    status: str = "draft"  # draft, pending, approved, rejected
    author: str = ""
    plan_summary: str = ""
    suggestion_count: int = 0
    diff_preview: str = ""
    comments: list[ProposalComment] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def approve(self, reviewer: str, comment: str = "") -> None:
        self.status = "approved"
        self.updated_at = _now()
        if comment:
            self.comments.append(ProposalComment(author=reviewer, text=comment))

    def reject(self, reviewer: str, reason: str = "") -> None:
        self.status = "rejected"
        self.updated_at = _now()
        if reason:
            self.comments.append(ProposalComment(author=reviewer, text=reason))

    def submit(self) -> None:
        self.status = "pending"
        self.updated_at = _now()

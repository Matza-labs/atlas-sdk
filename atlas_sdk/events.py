"""Redis Streams event schemas for inter-service messaging.

These models define the contract between atlas-* microservices.
All communication flows through Redis Streams.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from atlas_sdk.enums import Platform


def _new_id() -> str:
    return str(uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class BaseEvent(BaseModel):
    """Base event — all events carry an ID and timestamp."""

    event_id: str = Field(default_factory=_new_id)
    timestamp: datetime = Field(default_factory=_now)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ScanRequestEvent(BaseEvent):
    """Request to scan a CI/CD platform.

    Flow: API/CLI → atlas-scanner
    Stream: atlas.scan.requests
    """

    platform: Platform
    target_url: str
    token_ref: str = ""  # reference to secret, never the actual token
    scan_scope: dict[str, Any] = Field(default_factory=dict)
    log_depth: int = 5


class ScanResultEvent(BaseEvent):
    """Raw scan data ready for parsing.

    Flow: atlas-scanner → atlas-parser
    Stream: atlas.scan.results
    """

    scan_request_id: str
    platform: Platform
    pipeline_configs: list[dict[str, Any]] = Field(default_factory=list)
    build_logs: list[dict[str, Any]] = Field(default_factory=list)
    doc_files: list[dict[str, Any]] = Field(default_factory=list)


class ParseResultEvent(BaseEvent):
    """Parsed nodes and edges ready for graph construction.

    Flow: atlas-parser → atlas-graph
    Stream: atlas.parse.results
    """

    scan_request_id: str
    nodes: list[dict[str, Any]] = Field(default_factory=list)
    edges: list[dict[str, Any]] = Field(default_factory=list)


class FindingsEvent(BaseEvent):
    """Rule engine findings ready for report generation.

    Flow: atlas-rule-engine → atlas-report
    Stream: atlas.findings
    """

    scan_request_id: str
    graph_id: str
    findings: list[dict[str, Any]] = Field(default_factory=list)


class ReportReadyEvent(BaseEvent):
    """A report has been generated and is ready to serve.

    Flow: atlas-report → atlas-api
    Stream: atlas.reports.ready
    """

    scan_request_id: str
    graph_id: str
    report_id: str
    formats: list[str] = Field(default_factory=lambda: ["markdown", "json"])

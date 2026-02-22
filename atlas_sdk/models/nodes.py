"""CI/CD graph node models.

Every element in a CI/CD system is represented as a typed node in the
PipelineAtlas graph. All node types are defined from docs/README.md §4.4.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from atlas_sdk.enums import (
    ArtifactType,
    ConfidenceLevel,
    DocType,
    NodeType,
    Platform,
    SourceType,
)


def _new_id() -> str:
    return str(uuid4())


class Node(BaseModel):
    """Base graph node — all node types inherit from this."""

    id: str = Field(default_factory=_new_id)
    node_type: NodeType
    name: str
    platform: Platform | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    source: SourceType = SourceType.STATIC
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM


class PipelineNode(Node):
    """A CI/CD pipeline definition."""

    node_type: NodeType = NodeType.PIPELINE
    path: str | None = None
    branch: str | None = None
    trigger_type: str | None = None
    agent: str | None = None


class JobNode(Node):
    """A job within a pipeline."""

    node_type: NodeType = NodeType.JOB
    parameters: dict[str, Any] = Field(default_factory=dict)
    conditions: list[str] = Field(default_factory=list)
    timeout_minutes: int | None = None


class StageNode(Node):
    """A stage within a pipeline or job."""

    node_type: NodeType = NodeType.STAGE
    parallel: bool = False
    when_condition: str | None = None
    order: int | None = None


class StepNode(Node):
    """An individual step or build action."""

    node_type: NodeType = NodeType.STEP
    command: str | None = None
    plugin: str | None = None
    shell: str | None = None


class RepositoryNode(Node):
    """A source code repository."""

    node_type: NodeType = NodeType.REPOSITORY
    url: str | None = None
    default_branch: str | None = None
    vcs_type: str = "git"


class ArtifactNode(Node):
    """A build artifact (jar, docker image, file, etc.)."""

    node_type: NodeType = NodeType.ARTIFACT
    path: str | None = None
    artifact_type: ArtifactType = ArtifactType.FILE


class ContainerImageNode(Node):
    """A Docker / OCI container image."""

    node_type: NodeType = NodeType.CONTAINER_IMAGE
    registry: str | None = None
    tag: str | None = None
    pinned: bool = False
    digest: str | None = None


class RunnerNode(Node):
    """A CI/CD runner or agent."""

    node_type: NodeType = NodeType.RUNNER
    labels: list[str] = Field(default_factory=list)
    executor_type: str | None = None


class SecretRefNode(Node):
    """A reference to a secret (never stores the actual value).

    Security: Only the key name is stored — values are NEVER persisted.
    """

    node_type: NodeType = NodeType.SECRET_REF
    key: str = ""
    scope: str | None = None


class EnvironmentNode(Node):
    """A deployment environment."""

    node_type: NodeType = NodeType.ENVIRONMENT
    url: str | None = None
    protection_level: str | None = None


class ExternalServiceNode(Node):
    """An external service referenced by the pipeline."""

    node_type: NodeType = NodeType.EXTERNAL_SERVICE
    url: str | None = None
    service_type: str | None = None


class DocFileNode(Node):
    """A documentation file detected in the repository."""

    node_type: NodeType = NodeType.DOC_FILE
    path: str = ""
    doc_type: DocType = DocType.OTHER
    last_modified: str | None = None


# Registry for type-safe deserialization
NODE_TYPE_MAP: dict[NodeType, type[Node]] = {
    NodeType.PIPELINE: PipelineNode,
    NodeType.JOB: JobNode,
    NodeType.STAGE: StageNode,
    NodeType.STEP: StepNode,
    NodeType.REPOSITORY: RepositoryNode,
    NodeType.ARTIFACT: ArtifactNode,
    NodeType.CONTAINER_IMAGE: ContainerImageNode,
    NodeType.RUNNER: RunnerNode,
    NodeType.SECRET_REF: SecretRefNode,
    NodeType.ENVIRONMENT: EnvironmentNode,
    NodeType.EXTERNAL_SERVICE: ExternalServiceNode,
    NodeType.DOC_FILE: DocFileNode,
}

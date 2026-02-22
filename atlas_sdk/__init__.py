"""PipelineAtlas SDK — Shared models and schemas for all atlas-* services."""

__version__ = "0.1.0"

# Re-export core types for convenient access
from atlas_sdk.confidence import ConfidenceScore  # noqa: F401
from atlas_sdk.enums import (  # noqa: F401
    ArtifactType,
    ConfidenceLevel,
    DocType,
    EdgeType,
    NodeType,
    Platform,
    Severity,
    SourceType,
)
from atlas_sdk.events import (  # noqa: F401
    BaseEvent,
    FindingsEvent,
    ParseResultEvent,
    ReportReadyEvent,
    ScanRequestEvent,
    ScanResultEvent,
)
from atlas_sdk.models.edges import Edge  # noqa: F401
from atlas_sdk.models.findings import Evidence, Finding  # noqa: F401
from atlas_sdk.models.graph import CICDGraph  # noqa: F401
from atlas_sdk.models.nodes import (  # noqa: F401
    ArtifactNode,
    ContainerImageNode,
    DocFileNode,
    EnvironmentNode,
    ExternalServiceNode,
    JobNode,
    Node,
    PipelineNode,
    RepositoryNode,
    RunnerNode,
    SecretRefNode,
    StageNode,
    StepNode,
)

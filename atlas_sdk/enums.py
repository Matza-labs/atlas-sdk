"""Shared enumerations for PipelineAtlas.

All enum types used across atlas-* microservices are defined here
to ensure consistency.
"""

from enum import StrEnum


class NodeType(StrEnum):
    """CI/CD graph node types (from docs/README.md §4.4)."""

    PIPELINE = "pipeline"
    JOB = "job"
    STAGE = "stage"
    STEP = "step"
    REPOSITORY = "repository"
    ARTIFACT = "artifact"
    CONTAINER_IMAGE = "container_image"
    RUNNER = "runner"
    SECRET_REF = "secret_ref"
    ENVIRONMENT = "environment"
    EXTERNAL_SERVICE = "external_service"
    DOC_FILE = "doc_file"


class EdgeType(StrEnum):
    """CI/CD graph edge types (from docs/README.md §4.4)."""

    TRIGGERS = "triggers"
    CALLS = "calls"
    PRODUCES = "produces"
    CONSUMES = "consumes"
    DEPENDS_ON = "depends_on"
    DEPLOYS_TO = "deploys_to"
    IMPORTS = "imports"
    EXTENDS = "extends"
    INCLUDES = "includes"


class Severity(StrEnum):
    """Finding severity levels (from docs/README.md §4.5)."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class SourceType(StrEnum):
    """How a piece of information was discovered (from docs/README.md §5)."""

    STATIC = "static"
    RUNTIME = "runtime"
    STATIC_RUNTIME = "static_runtime"
    AI_INFERENCE = "ai_inference"


class ConfidenceLevel(StrEnum):
    """Confidence in a finding or structural element (from docs/README.md §5).

    Rules:
        HIGH    = Static + Runtime match
        MEDIUM  = Static only
        LOW     = AI-derived
    """

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Platform(StrEnum):
    """Supported CI/CD platforms."""

    JENKINS = "jenkins"
    GITLAB = "gitlab"
    GITHUB_ACTIONS = "github_actions"


class DocType(StrEnum):
    """Documentation file categories (from docs/README.md §4.3)."""

    README = "readme"
    DOCS_DIR = "docs_dir"
    RUNBOOK = "runbook"
    ARCHITECTURE = "architecture"
    ADR = "adr"
    SECURITY_POLICY = "security_policy"
    CODEOWNERS = "codeowners"
    WIKI = "wiki"
    OTHER = "other"


class ArtifactType(StrEnum):
    """Build artifact types."""

    JAR = "jar"
    WAR = "war"
    DOCKER_IMAGE = "docker_image"
    NPM_PACKAGE = "npm_package"
    BINARY = "binary"
    FILE = "file"
    ARCHIVE = "archive"
    OTHER = "other"

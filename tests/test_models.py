"""Unit tests for atlas-sdk models."""

import json

import pytest

from atlas_sdk import (
    ArtifactNode,
    ArtifactType,
    CICDGraph,
    ConfidenceLevel,
    ConfidenceScore,
    ContainerImageNode,
    DocFileNode,
    DocType,
    Edge,
    EdgeType,
    EnvironmentNode,
    Evidence,
    ExternalServiceNode,
    Finding,
    FindingsEvent,
    JobNode,
    Node,
    NodeType,
    ParseResultEvent,
    PipelineNode,
    Platform,
    ReportReadyEvent,
    RepositoryNode,
    RunnerNode,
    ScanRequestEvent,
    ScanResultEvent,
    SecretRefNode,
    Severity,
    SourceType,
    StageNode,
    StepNode,
)


# ── Enum tests ────────────────────────────────────────────────────────


class TestEnums:
    def test_node_type_values(self):
        assert NodeType.PIPELINE == "pipeline"
        assert NodeType.CONTAINER_IMAGE == "container_image"
        assert len(NodeType) == 12

    def test_edge_type_values(self):
        assert EdgeType.TRIGGERS == "triggers"
        assert EdgeType.DEPENDS_ON == "depends_on"
        assert len(EdgeType) == 9

    def test_severity_ordering(self):
        severities = [s.value for s in Severity]
        assert "critical" in severities
        assert "info" in severities

    def test_source_type_values(self):
        assert SourceType.STATIC_RUNTIME == "static_runtime"
        assert SourceType.AI_INFERENCE == "ai_inference"

    def test_confidence_level_values(self):
        assert ConfidenceLevel.HIGH == "high"
        assert ConfidenceLevel.LOW == "low"

    def test_platform_values(self):
        assert Platform.JENKINS == "jenkins"
        assert Platform.GITLAB == "gitlab"

    def test_enum_json_serialization(self):
        """StrEnum values serialize as plain strings in JSON."""
        assert json.dumps(NodeType.PIPELINE) == '"pipeline"'


# ── Node model tests ─────────────────────────────────────────────────


class TestNodes:
    def test_base_node_creation(self):
        node = Node(node_type=NodeType.PIPELINE, name="build")
        assert node.node_type == NodeType.PIPELINE
        assert node.name == "build"
        assert node.source == SourceType.STATIC
        assert node.confidence == ConfidenceLevel.MEDIUM
        assert node.id  # auto-generated UUID

    def test_pipeline_node(self):
        node = PipelineNode(
            name="main-build",
            path="Jenkinsfile",
            branch="main",
            platform=Platform.JENKINS,
        )
        assert node.node_type == NodeType.PIPELINE
        assert node.path == "Jenkinsfile"
        assert node.branch == "main"

    def test_job_node(self):
        node = JobNode(
            name="deploy",
            parameters={"env": "prod"},
            timeout_minutes=30,
        )
        assert node.node_type == NodeType.JOB
        assert node.parameters["env"] == "prod"
        assert node.timeout_minutes == 30

    def test_stage_node(self):
        node = StageNode(name="test", parallel=True, order=2)
        assert node.node_type == NodeType.STAGE
        assert node.parallel is True
        assert node.order == 2

    def test_step_node(self):
        node = StepNode(name="sh", command="make build", shell="bash")
        assert node.node_type == NodeType.STEP
        assert node.command == "make build"

    def test_repository_node(self):
        node = RepositoryNode(
            name="my-app",
            url="https://github.com/org/my-app",
            default_branch="main",
        )
        assert node.node_type == NodeType.REPOSITORY
        assert node.vcs_type == "git"

    def test_artifact_node(self):
        node = ArtifactNode(
            name="app.jar",
            artifact_type=ArtifactType.JAR,
        )
        assert node.node_type == NodeType.ARTIFACT
        assert node.artifact_type == ArtifactType.JAR

    def test_container_image_node(self):
        node = ContainerImageNode(
            name="myapp:latest",
            registry="docker.io",
            tag="latest",
            pinned=False,
        )
        assert node.node_type == NodeType.CONTAINER_IMAGE
        assert node.pinned is False

    def test_runner_node(self):
        node = RunnerNode(
            name="linux-runner",
            labels=["linux", "docker"],
            executor_type="docker",
        )
        assert node.node_type == NodeType.RUNNER
        assert "docker" in node.labels

    def test_secret_ref_node_no_value(self):
        """SecretRefNode must never contain the actual secret value."""
        node = SecretRefNode(name="DB_PASSWORD", key="DB_PASSWORD")
        assert node.node_type == NodeType.SECRET_REF
        assert node.key == "DB_PASSWORD"
        # Verify no 'value' field exists
        assert "value" not in SecretRefNode.model_fields

    def test_environment_node(self):
        node = EnvironmentNode(
            name="production",
            url="https://prod.example.com",
            protection_level="required_reviewers",
        )
        assert node.node_type == NodeType.ENVIRONMENT

    def test_external_service_node(self):
        node = ExternalServiceNode(
            name="SonarQube",
            url="https://sonar.example.com",
            service_type="code_analysis",
        )
        assert node.node_type == NodeType.EXTERNAL_SERVICE

    def test_doc_file_node(self):
        node = DocFileNode(
            name="README.md",
            path="README.md",
            doc_type=DocType.README,
        )
        assert node.node_type == NodeType.DOC_FILE

    def test_node_json_round_trip(self):
        original = PipelineNode(
            name="build",
            path="Jenkinsfile",
            platform=Platform.JENKINS,
            confidence=ConfidenceLevel.HIGH,
        )
        data = original.model_dump()
        restored = PipelineNode.model_validate(data)
        assert restored.name == original.name
        assert restored.path == original.path
        assert restored.platform == original.platform
        assert restored.id == original.id

    def test_all_12_node_types_exist(self):
        from atlas_sdk.models.nodes import NODE_TYPE_MAP

        assert len(NODE_TYPE_MAP) == 12
        for nt in NodeType:
            assert nt in NODE_TYPE_MAP


# ── Edge model tests ─────────────────────────────────────────────────


class TestEdges:
    def test_edge_creation(self):
        edge = Edge(
            edge_type=EdgeType.TRIGGERS,
            source_node_id="node-1",
            target_node_id="node-2",
        )
        assert edge.edge_type == EdgeType.TRIGGERS
        assert edge.source_node_id == "node-1"
        assert edge.id  # auto-generated

    def test_edge_json_round_trip(self):
        original = Edge(
            edge_type=EdgeType.DEPENDS_ON,
            source_node_id="a",
            target_node_id="b",
            metadata={"weight": 1},
        )
        data = original.model_dump()
        restored = Edge.model_validate(data)
        assert restored.edge_type == original.edge_type
        assert restored.metadata["weight"] == 1


# ── Confidence model tests ───────────────────────────────────────────


class TestConfidence:
    def test_high_factory(self):
        c = ConfidenceScore.high("Confirmed by static + runtime")
        assert c.level == ConfidenceLevel.HIGH
        assert c.source == SourceType.STATIC_RUNTIME

    def test_medium_factory(self):
        c = ConfidenceScore.medium()
        assert c.level == ConfidenceLevel.MEDIUM
        assert c.source == SourceType.STATIC

    def test_low_factory(self):
        c = ConfidenceScore.low("AI inferred from log patterns")
        assert c.level == ConfidenceLevel.LOW
        assert c.source == SourceType.AI_INFERENCE

    def test_default_confidence(self):
        c = ConfidenceScore()
        assert c.level == ConfidenceLevel.MEDIUM
        assert c.source == SourceType.STATIC


# ── Finding model tests ──────────────────────────────────────────────


class TestFindings:
    def test_finding_creation(self):
        finding = Finding(
            rule_id="no-timeout",
            title="No timeout configured",
            description="Pipeline has no timeout, may run indefinitely",
            severity=Severity.HIGH,
            evidence=[
                Evidence(
                    source_file="Jenkinsfile",
                    line_number=5,
                    snippet="pipeline { }",
                    description="No timeout block found",
                )
            ],
            recommendation="Add options { timeout(time: 30, unit: 'MINUTES') }",
            impact_category="reliability",
            affected_node_ids=["node-1"],
        )
        assert finding.severity == Severity.HIGH
        assert len(finding.evidence) == 1
        assert finding.evidence[0].line_number == 5
        assert finding.confidence.level == ConfidenceLevel.MEDIUM

    def test_finding_json_round_trip(self):
        finding = Finding(
            rule_id="missing-cache",
            title="Missing caching",
            description="No caching detected",
            severity=Severity.MEDIUM,
        )
        data = finding.model_dump()
        restored = Finding.model_validate(data)
        assert restored.rule_id == finding.rule_id
        assert restored.id == finding.id


# ── Graph container tests ────────────────────────────────────────────


class TestGraph:
    def test_graph_creation(self):
        graph = CICDGraph(name="test-graph", platform=Platform.JENKINS)
        assert graph.name == "test-graph"
        assert len(graph.nodes) == 0
        assert len(graph.edges) == 0
        assert graph.scanned_at is not None

    def test_graph_add_and_query(self):
        graph = CICDGraph(name="test")
        p = PipelineNode(name="build")
        j = JobNode(name="compile")
        graph.add_node(p)
        graph.add_node(j)

        edge = Edge(
            edge_type=EdgeType.CALLS,
            source_node_id=p.id,
            target_node_id=j.id,
        )
        graph.add_edge(edge)

        assert len(graph.nodes) == 2
        assert len(graph.edges) == 1
        assert graph.get_node(p.id) is p
        assert graph.get_node("nonexistent") is None
        assert len(graph.get_edges_from(p.id)) == 1
        assert len(graph.get_edges_to(j.id)) == 1

    def test_graph_json_round_trip(self):
        graph = CICDGraph(name="test", platform=Platform.GITLAB)
        graph.add_node(PipelineNode(name="deploy"))
        data = graph.model_dump(mode="json")
        restored = CICDGraph.model_validate(data)
        assert restored.name == "test"
        assert len(restored.nodes) == 1


# ── Event model tests ────────────────────────────────────────────────


class TestEvents:
    def test_scan_request_event(self):
        event = ScanRequestEvent(
            platform=Platform.JENKINS,
            target_url="https://jenkins.example.com",
            log_depth=10,
        )
        assert event.platform == Platform.JENKINS
        assert event.log_depth == 10
        assert event.event_id  # auto-generated

    def test_scan_result_event(self):
        event = ScanResultEvent(
            scan_request_id="req-1",
            platform=Platform.GITLAB,
            pipeline_configs=[{"path": ".gitlab-ci.yml", "content": "stages: [build]"}],
        )
        assert len(event.pipeline_configs) == 1

    def test_parse_result_event(self):
        event = ParseResultEvent(
            scan_request_id="req-1",
            nodes=[{"node_type": "pipeline", "name": "build"}],
            edges=[],
        )
        assert len(event.nodes) == 1

    def test_findings_event(self):
        event = FindingsEvent(
            scan_request_id="req-1",
            graph_id="graph-1",
            findings=[{"rule_id": "no-timeout", "title": "No timeout"}],
        )
        assert len(event.findings) == 1

    def test_report_ready_event(self):
        event = ReportReadyEvent(
            scan_request_id="req-1",
            graph_id="graph-1",
            report_id="report-1",
        )
        assert "markdown" in event.formats

    def test_event_json_round_trip(self):
        event = ScanRequestEvent(
            platform=Platform.JENKINS,
            target_url="https://jenkins.example.com",
        )
        data = event.model_dump(mode="json")
        restored = ScanRequestEvent.model_validate(data)
        assert restored.event_id == event.event_id
        assert restored.platform == event.platform

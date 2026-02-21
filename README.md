# atlas-sdk

Shared Python library for **PipelineAtlas** — the CI/CD Architecture Intelligence Platform.

## Purpose

`atlas-sdk` provides the common data models, schemas, and utilities used by all PipelineAtlas microservices. It is the **foundation** that all other `atlas-*` services depend on.

## What's Inside

| Module | Description |
|--------|-------------|
| `atlas_sdk.models.nodes` | Graph node types (Pipeline, Job, Stage, Step, Artifact, etc.) |
| `atlas_sdk.models.edges` | Graph edge types (triggers, calls, produces, depends_on, etc.) |
| `atlas_sdk.models.findings` | Rule engine finding schema (title, severity, evidence, confidence) |
| `atlas_sdk.confidence` | Confidence scoring model (High / Medium / Low, source types) |
| `atlas_sdk.events` | Redis Streams event schemas for inter-service messaging |

## Installation

```bash
# From local path (development)
pip install -e ../atlas-sdk

# From GitHub packages (CI/CD)
pip install atlas-sdk
```

## Tech Stack

- Python 3.11+
- Pydantic v2

## Related Services

All `atlas-*` services depend on this package. See [docs/](../docs/) for full architecture.

"""Confidence scoring model.

From docs/README.md §5 — every structural element and finding must include
a confidence score with transparent source attribution.

Rules:
    HIGH   = Static + Runtime match
    MEDIUM = Static only
    LOW    = AI-derived
"""

from __future__ import annotations

from pydantic import BaseModel

from atlas_sdk.enums import ConfidenceLevel, SourceType


class ConfidenceScore(BaseModel):
    """Confidence assessment for a finding or structural element."""

    level: ConfidenceLevel = ConfidenceLevel.MEDIUM
    source: SourceType = SourceType.STATIC
    reasoning: str | None = None

    @classmethod
    def high(cls, reasoning: str | None = None) -> ConfidenceScore:
        """Static + Runtime confirmed."""
        return cls(
            level=ConfidenceLevel.HIGH,
            source=SourceType.STATIC_RUNTIME,
            reasoning=reasoning,
        )

    @classmethod
    def medium(cls, reasoning: str | None = None) -> ConfidenceScore:
        """Static analysis only."""
        return cls(
            level=ConfidenceLevel.MEDIUM,
            source=SourceType.STATIC,
            reasoning=reasoning,
        )

    @classmethod
    def low(cls, reasoning: str | None = None) -> ConfidenceScore:
        """AI-inferred."""
        return cls(
            level=ConfidenceLevel.LOW,
            source=SourceType.AI_INFERENCE,
            reasoning=reasoning,
        )

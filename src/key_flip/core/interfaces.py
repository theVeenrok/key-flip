"""High-level protocols for the core services."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Protocol, runtime_checkable

from .models import ConvertOptions, ConvertResult, DetectionResult, Layout, LayoutPair
from .types import LayoutId, LayoutPairId


@runtime_checkable
class LayoutSource(Protocol):
    """Low-level provider that knows how to load layouts and layout pairs."""

    def load_layouts(self) -> Iterable[Layout]:
        """Return all available layouts."""

    def load_pairs(self) -> Iterable[LayoutPair]:
        """Return all available layout pairs."""


@runtime_checkable
class LayoutRepository(Protocol):
    """Storage abstraction built on top of a LayoutSource."""

    def list_layouts(self) -> Sequence[Layout]:
        """Get cached layouts."""

    def list_pairs(self) -> Sequence[LayoutPair]:
        """Get cached layout pairs."""

    def get_layout(self, layout_id: LayoutId) -> Layout:
        """Resolve a layout by identifier."""

    def get_pair(self, pair_id: LayoutPairId) -> LayoutPair:
        """Resolve a layout pair by identifier."""


@runtime_checkable
class LayoutDetector(Protocol):
    """Strategy that detects the desired conversion direction/layout."""

    def detect(self, text: str, *, options: ConvertOptions) -> DetectionResult:
        """Return detection info for the provided text."""


@runtime_checkable
class Converter(Protocol):
    """Top-level conversion service."""

    def convert(self, text: str, *, options: ConvertOptions) -> ConvertResult:
        """Convert text according to the provided options."""

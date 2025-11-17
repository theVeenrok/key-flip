from collections.abc import Sequence
from dataclasses import dataclass

from key_flip.core.errors import InvalidMappingError

from .types import Char, Direction, LayoutId, LayoutPairId


@dataclass(frozen=True, slots=True)
class Layout:
    id: LayoutId
    name: str
    language: str
    script: str
    variant: str | None = None
    char_order: Sequence[Char] | None = None


@dataclass(frozen=True)
class PairLayerMapping:
    layer: str
    from_chars: str
    to_chars: str

    def __post_init__(self):
        if len(self.from_chars) != len(self.to_chars):
            raise InvalidMappingError("from_chars and to_chars must have the same length")


@dataclass(frozen=True, slots=True)
class LayoutPair:
    id: LayoutPairId
    layout_ids: tuple[LayoutId, LayoutId]
    mappings: tuple[PairLayerMapping, ...]
    description: str
    is_default: bool = False


@dataclass(frozen=True, slots=True)
class ConvertOptions:
    layout_pair_id: LayoutPairId
    direction: Direction


@dataclass(frozen=True, slots=True)
class DetectionResult:
    layout_id: LayoutId


@dataclass(frozen=True, slots=True)
class ConvertResult:
    source_text: str
    converted_text: str
    layout_pair_id: LayoutPairId
    direction: Direction
    detection: DetectionResult

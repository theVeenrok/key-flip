from dataclasses import dataclass
from typing import Self

from key_flip.core.errors import LayoutNotFoundError, LayoutPairNotFoundError
from key_flip.core.interfaces import LayoutRepository, LayoutSource
from key_flip.core.models import Layout, LayoutPair
from key_flip.core.types import LayoutId, LayoutPairId


@dataclass
class InMemoryLayoutRepository(LayoutRepository):
    _layouts: dict[LayoutId, Layout]
    _pairs: dict[LayoutPairId, LayoutPair]

    @classmethod
    def from_source(cls, source: LayoutSource) -> Self:
        layouts = {layout.id: layout for layout in source.load_layouts()}
        pairs = {pair.id: pair for pair in source.load_pairs()}
        return cls(layouts, pairs)

    def list_layouts(self) -> tuple[Layout, ...]:
        return tuple(self._layouts.values())

    def list_pairs(self) -> tuple[LayoutPair, ...]:
        return tuple(self._pairs.values())

    def get_layout(self, layout_id: LayoutId) -> Layout:
        try:
            return self._layouts[layout_id]
        except KeyError:
            raise LayoutNotFoundError()

    def get_pair(self, pair_id: LayoutPairId) -> LayoutPair:
        try:
            return self._pairs[pair_id]
        except KeyError:
            raise LayoutPairNotFoundError()

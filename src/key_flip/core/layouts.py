from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .interfaces import LayoutSource
from .models import Layout, LayoutPair, PairLayerMapping
from .types import LayoutId, LayoutPairId


def _ensure_two_layouts(raw_layouts: Iterable[str], pair_id: str) -> tuple[str, str]:
    items = tuple(raw_layouts)
    if len(items) != 2:
        msg = f"Pair '{pair_id}' must reference exactly two layouts"
        raise ValueError(msg)
    return items[0], items[1]


@dataclass(slots=True)
class TomlLayoutSource(LayoutSource):
    """Load layouts and layout pairs from a TOML specification."""

    path: Path
    _cache: dict[str, Any] | None = field(default=None, init=False, repr=False)

    def load_layouts(self) -> tuple[Layout, ...]:
        data = self._load_data()
        layouts_raw = data.get("layouts", [])
        return tuple(self._build_layout(item) for item in layouts_raw)

    def load_pairs(self) -> tuple[LayoutPair, ...]:
        data = self._load_data()
        pairs_raw = data.get("pairs", [])
        return tuple(self._build_pair(item) for item in pairs_raw)

    def _load_data(self) -> dict[str, Any]:
        if self._cache is None:
            with self.path.open("rb") as handle:
                self._cache = tomllib.load(handle)
        return self._cache

    @staticmethod
    def _build_layout(raw: dict[str, Any]) -> Layout:
        return Layout(
            id=LayoutId(raw["id"]),
            name=raw.get("display_name", raw["id"]),
            language=raw["language"],
            script=raw["script"],
            variant=raw.get("variant"),
            char_order=raw.get("char_order"),
        )

    def _build_pair(self, raw: dict[str, Any]) -> LayoutPair:
        first_id, second_id = _ensure_two_layouts(raw.get("layouts", []), raw["id"])
        mappings_raw = raw.get("mappings", [])
        mappings = tuple(self._build_mapping_layer(item) for item in mappings_raw)
        description = raw.get("description") or raw.get("display_name") or raw["id"]
        return LayoutPair(
            id=LayoutPairId(raw["id"]),
            layout_ids=(LayoutId(first_id), LayoutId(second_id)),
            mappings=mappings,
            description=description,
            is_default=bool(raw.get("is_default", False)),
        )

    @staticmethod
    def _build_mapping_layer(raw: dict[str, Any]) -> PairLayerMapping:
        return PairLayerMapping(
            layer=raw["layer"],
            from_chars=raw["from"],
            to_chars=raw["to"],
        )

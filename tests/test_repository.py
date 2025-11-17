import pytest

from key_flip.core.errors import LayoutNotFoundError, LayoutPairNotFoundError
from key_flip.core.interfaces import LayoutSource
from key_flip.core.models import Layout, LayoutPair, PairLayerMapping
from key_flip.core.repository import InMemoryLayoutRepository
from key_flip.core.types import LayoutId, LayoutPairId


class DummySource(LayoutSource):
    def __init__(self, layouts: tuple[Layout, ...], pairs: tuple[LayoutPair, ...]) -> None:
        self._layouts = layouts
        self._pairs = pairs

    def load_layouts(self) -> tuple[Layout, ...]:
        return self._layouts

    def load_pairs(self) -> tuple[LayoutPair, ...]:
        return self._pairs


def make_layout(layout_id: str, name: str) -> Layout:
    return Layout(id=LayoutId(layout_id), name=name, language="en", script="latin", variant="us")


def make_pair(pair_id: str, layout_ids: tuple[LayoutId, LayoutId]) -> LayoutPair:
    layout_id_objs = tuple(LayoutId(lid) for lid in layout_ids)
    layer = PairLayerMapping(layer="row1", from_chars="abc", to_chars="def")
    return LayoutPair(
        id=LayoutPairId(pair_id),
        layout_ids=layout_id_objs,
        mappings=(layer,),
        description="test",
    )


class TestInMemoryLayoutRepository:
    def test_repository_from_source_lists_layouts_and_pairs(self) -> None:
        layouts = (make_layout("en", "English"), make_layout("ru", "Russian"))
        pairs = (make_pair("en-ru", ("en", "ru")),)
        repo = InMemoryLayoutRepository.from_source(DummySource(layouts, pairs))

        assert repo.list_layouts() == layouts
        assert repo.list_pairs() == pairs

    def test_get_layout_success_and_not_found(self) -> None:
        layout = make_layout("en", "English")
        repo = InMemoryLayoutRepository({layout.id: layout}, {})

        assert repo.get_layout(LayoutId("en")) == layout
        with pytest.raises(LayoutNotFoundError):
            repo.get_layout(LayoutId("ru"))

    def test_get_pair_success_and_not_found(self) -> None:
        pair = make_pair("en-ru", ("en", "ru"))
        repo = InMemoryLayoutRepository({}, {pair.id: pair})

        assert repo.get_pair(LayoutPairId("en-ru")) == pair
        with pytest.raises(LayoutPairNotFoundError):
            repo.get_pair(LayoutPairId("ru-en"))

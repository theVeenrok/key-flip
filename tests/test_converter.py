import pytest

from key_flip.core.converters import ConverterSimple
from key_flip.core.errors import LayoutNotFoundError
from key_flip.core.interfaces import LayoutRepository
from key_flip.core.models import ConvertOptions, LayoutPair, PairLayerMapping
from key_flip.core.types import Direction, LayoutId, LayoutPairId


class DummyRepository(LayoutRepository):
    def __init__(self, pairs: dict[LayoutPairId, LayoutPair]) -> None:
        self._pairs = pairs

    def list_layouts(self):
        return ()

    def list_pairs(self):
        return tuple(self._pairs.values())

    def get_layout(self, layout_id: LayoutId):
        raise LayoutNotFoundError()

    def get_pair(self, pair_id: LayoutPairId) -> LayoutPair:
        return self._pairs[pair_id]


def build_pair() -> LayoutPair:
    mapping = PairLayerMapping(layer="row1", from_chars="ab", to_chars="фы")
    return LayoutPair(
        id=LayoutPairId("en-ru"),
        layout_ids=(LayoutId("en"), LayoutId("ru")),
        mappings=(mapping,),
        description="test",
    )


class TestConverterSimple:
    def setup_method(self) -> None:
        pair = build_pair()
        self.repo = DummyRepository({pair.id: pair})
        self.converter = ConverterSimple(self.repo)

    def test_convert_forward_direction(self) -> None:
        options = ConvertOptions(layout_pair_id=LayoutPairId("en-ru"), direction=Direction.FORWARD)
        result = self.converter.convert("ab*", options=options)

        assert result.converted_text == "фы*"
        assert result.direction is Direction.FORWARD
        assert result.detection.layout_id == LayoutId("en")

    def test_convert_backward_direction(self) -> None:
        options = ConvertOptions(layout_pair_id=LayoutPairId("en-ru"), direction=Direction.BACKWARD)
        result = self.converter.convert("фы*", options=options)

        assert result.converted_text == "ab*"
        assert result.direction is Direction.BACKWARD
        assert result.detection.layout_id == LayoutId("ru")

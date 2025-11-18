import unittest

from key_flip.core.detectors import FrequencyDetector
from key_flip.core.models import ConvertOptions, Layout, LayoutPair, PairLayerMapping
from key_flip.core.repository import InMemoryLayoutRepository
from key_flip.core.types import Direction, LayoutId, LayoutPairId


def _build_detector() -> tuple[FrequencyDetector, LayoutPair]:
    en_layout = Layout(
        id=LayoutId("en_qwerty"),
        name="English (US) QWERTY",
        language="en",
        script="latin",
        variant="us",
    )
    ru_layout = Layout(
        id=LayoutId("ru_qwerty"),
        name="Russian (ЙЦУКЕН)",
        language="ru",
        script="cyrillic",
        variant="ЙЦУКЕН",
    )
    pair = LayoutPair(
        id=LayoutPairId("en-ru-qwerty"),
        layout_ids=(en_layout.id, ru_layout.id),
        mappings=(
            PairLayerMapping(layer="top", from_chars="`1234567890-=", to_chars="ё1234567890-="),
            PairLayerMapping(layer="top-shift", from_chars="~!@#$%^&*()_+", to_chars='Ё!"№;%:?*()_+'),
            PairLayerMapping(layer="row1", from_chars="qwertyuiop[]\\", to_chars="йцукенгшщзхъ\\"),
            PairLayerMapping(layer="row1-shift", from_chars="QWERTYUIOP{}|", to_chars="ЙЦУКЕНГШЩЗХЪ/"),
            PairLayerMapping(layer="row2", from_chars="asdfghjkl;'", to_chars="фывапролджэ"),
            PairLayerMapping(layer="row2-shift", from_chars='ASDFGHJKL:"', to_chars="ФЫВАПРОЛДЖЭ"),
            PairLayerMapping(layer="row3", from_chars="zxcvbnm,./", to_chars="ячсмитьбю."),
            PairLayerMapping(layer="row3-shift", from_chars="ZXCVBNM<>?", to_chars="ЯЧСМИТЬБЮ,"),
        ),
        description="English ↔ Russian QWERTY",
        is_default=True,
    )
    repository = InMemoryLayoutRepository(
        _layouts={en_layout.id: en_layout, ru_layout.id: ru_layout},
        _pairs={pair.id: pair},
    )
    return FrequencyDetector(repository), pair


class TestFrequencyDetector(unittest.TestCase):
    def setUp(self) -> None:
        self.detector, self.pair = _build_detector()
        self.options = ConvertOptions(layout_pair_id=self.pair.id, direction=Direction.FORWARD)

    def test_prefers_latin_text_for_first_layout(self) -> None:
        result = self.detector.detect("hello ghbdtn", options=self.options)

        self.assertEqual(result.layout_id, LayoutId("en_qwerty"))

    def test_prefers_cyrillic_text_for_second_layout(self) -> None:
        result = self.detector.detect("привет мир", options=self.options)

        self.assertEqual(result.layout_id, LayoutId("ru_qwerty"))

    def test_defaults_to_first_layout_on_score_ties(self) -> None:
        result = self.detector.detect("1234567890", options=self.options)

        self.assertEqual(result.layout_id, LayoutId("en_qwerty"))

from dataclasses import dataclass

from key_flip.core.interfaces import LayoutRepository
from key_flip.core.models import ConvertOptions, DetectionResult, LayoutPair
from key_flip.core.types import Char


@dataclass
class FrequencyDetector:
    _layout_repository: LayoutRepository

    def detect(self, text: str, *, options: ConvertOptions) -> DetectionResult:
        layout_pair = self._layout_repository.get_pair(pair_id=options.layout_pair_id)

        layout_pair_chars = self._layout_pair_chars(layout_pair)

        score = 0
        for char in text:
            if char in layout_pair_chars[0]:
                score += 1
            if char in layout_pair_chars[1]:
                score -= 1

        selected_layout_id = layout_pair.layout_ids[0]
        if score > 0:
            selected_layout_id = layout_pair.layout_ids[0]
        elif score < 0:
            selected_layout_id = layout_pair.layout_ids[1]

        return DetectionResult(layout_id=selected_layout_id)

    def _layout_pair_chars(self, layout_pair: LayoutPair) -> tuple[set[Char], set[Char]]:
        chars: tuple[set[Char], set[Char]] = (set(), set())

        for mappings in layout_pair.mappings:
            chars[0].update(mappings.from_chars)
            chars[1].update(mappings.to_chars)

        return chars

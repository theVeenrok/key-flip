from dataclasses import dataclass

from key_flip.core.interfaces import Converter, LayoutRepository
from key_flip.core.models import ConvertOptions, ConvertResult, DetectionResult, LayoutPair
from key_flip.core.types import Direction


@dataclass
class ConverterSimple(Converter):
    _layout_repository: LayoutRepository

    def convert(self, text: str, *, options: ConvertOptions) -> ConvertResult:
        pair = self._layout_repository.get_pair(pair_id=options.layout_pair_id)
        forward, backward = self._build_mappings(pair)

        mapping = self._select_mapping(options.direction, forward, backward)

        converted_text = "".join(mapping.get(char, char) for char in text)
        detection_layout = pair.layout_ids[0 if options.direction == Direction.FORWARD else 1]
        detection = DetectionResult(layout_id=detection_layout)
        
        result = ConvertResult(
            source_text=text,
            converted_text=converted_text,
            layout_pair_id=pair.id,
            direction=options.direction,
            detection=detection,
        )
        return result

    def _build_mappings(self, pair: LayoutPair) -> tuple[dict[str, str], dict[str, str]]:
        forward = {}
        backward = {}

        for layer in pair.mappings:
            for src, dst in zip(layer.from_chars, layer.to_chars, strict=True):
                forward[src] = dst
                backward[dst] = src
        return forward, backward

    def _select_mapping(
        self, direction: Direction, forward: dict[str, str], backward: dict[str, str]
    ) -> dict[str, str]:
        if direction == Direction.FORWARD:
            return forward
        elif direction == Direction.BACKWARD:
            return backward
        else:
            raise ValueError(f"Invalid direction: {direction}")

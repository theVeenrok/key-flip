from pathlib import Path

import pytest

from key_flip.core.layouts import TomlLayoutSource
from key_flip.core.types import LayoutId, LayoutPairId


def _write_sample_file(path: Path) -> None:
    path.write_text(
        """
version = 1

[[layouts]]
id = "en_qwerty"
language = "en"
script = "latin"
variant = "us"
display_name = "English (US)"

[[layouts]]
id = "ru_qwerty"
language = "ru"
script = "cyrillic"
variant = "ЙЦУКЕН"
display_name = "Russian"

[[pairs]]
id = "en-ru"
display_name = "EN ↔ RU"
description = "sample"
layouts = ["en_qwerty", "ru_qwerty"]

[[pairs.mappings]]
layer = "row1"
from = "ab"
to = "фы"
""",
        encoding="utf-8",
    )


class TestTomlLayoutSource:
    def test_load_layouts_and_pairs(self, tmp_path: Path) -> None:
        source_path = tmp_path / "layouts.toml"
        _write_sample_file(source_path)

        source = TomlLayoutSource(source_path)

        layouts = source.load_layouts()
        assert len(layouts) == 2
        assert layouts[0].id == LayoutId("en_qwerty")
        assert layouts[0].name == "English (US)"

        pairs = source.load_pairs()
        assert len(pairs) == 1
        pair = pairs[0]
        assert pair.id == LayoutPairId("en-ru")
        assert pair.layout_ids == (LayoutId("en_qwerty"), LayoutId("ru_qwerty"))
        assert pair.mappings[0].layer == "row1"
        assert pair.mappings[0].from_chars == "ab"
        assert pair.mappings[0].to_chars == "фы"

    def test_pair_requires_two_layouts(self, tmp_path: Path) -> None:
        source_path = tmp_path / "broken.toml"
        source_path.write_text(
            """
version = 1

[[layouts]]
id = "en_qwerty"
language = "en"
script = "latin"
variant = "us"
display_name = "English (US)"

[[pairs]]
id = "invalid"
layouts = ["en_qwerty"]
description = "broken"
""",
            encoding="utf-8",
        )

        source = TomlLayoutSource(source_path)
        with pytest.raises(ValueError):
            source.load_pairs()

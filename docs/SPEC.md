# Layout Specification

This document describes the format of `data/layouts.toml` used by the `key-flip` core.

## Format version

- `version` — integer value that defines parsing rules and schema. Current value: `1`.

## Layout definitions

The `[[layouts]]` array lists every available layout.

Required fields:

- `id` — unique identifier (a `snake_case` string).
- `language` — ISO 639-1 language code.
- `script` — writing system name (`latin`, `cyrillic`, etc.).
- `variant` — human-readable qualifier (for example, `us`, `ЙЦУКЕН`).
- `display_name` — full name for CLI/GUI output.

Layouts contain only metadata; mapping tables live inside pairs.

## Layout pairs

The `[[pairs]]` array defines a concrete combination of layouts and its conversion rules.

Fields:

- `id` — unique pair identifier.
- `display_name` — name shown in CLI/UI.
- `description` — short explanation (optional but recommended).
- `layouts` — two `id` values referencing layouts (order matters: the first is the source in forward conversion).
- `[[pairs.mappings]]` — list of mapping tables.

## Mappings

Each `[[pairs.mappings]]` entry describes a keyboard layer.

Fields:

- `layer` — layer name (`top`, `row1`, `row2`, `row3`, `top-shift`, etc.).
- `from` — string of characters in the first layout.
- `to` — string of characters in the second layout.

`from` and `to` must have the same length. Provide mappings for every layer, including Shift variants. Extra layers (e.g., `altgr`) are allowed when the format evolves.

## Example: EN ↔ RU QWERTY

```toml
version = 1

[[layouts]]
id = "en_qwerty"
language = "en"
script = "latin"
variant = "us"
display_name = "English (US) QWERTY"

[[layouts]]
id = "ru_qwerty"
language = "ru"
script = "cyrillic"
variant = "ЙЦУКЕН"
display_name = "Russian (ЙЦУКЕН)"

[[pairs]]
id = "en-ru-qwerty"
display_name = "English ↔ Russian (QWERTY)"
description = "Standard mapping between US English and Russian ЙЦУКЕН layouts."
layouts = ["en_qwerty", "ru_qwerty"]

[[pairs.mappings]]
layer = "top"
from = "`1234567890-="
to = "ё1234567890-="

[[pairs.mappings]]
layer = "row1"
from = "qwertyuiop[]\\"
to = "йцукенгшщзхъ\\"
# ... remaining layers omitted for brevity
```

See `data/layouts.toml` for the full example.

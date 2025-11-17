# key-flip

`key-flip` is a utility that fixes text typed with the wrong keyboard layout.

For example:

- `ghbdtn` → `привет`
- `руддщ` → `hello`

The entire project is built in Python: first a minimal conversion core, then a CLI and shared regression specs. See the roadmap below for details.

---

## Capabilities (planned)

- Convert text between layout pairs described in `data/layouts.toml`.
- Extend layout metadata through a simple TOML file kept under version control.
- CLI interface:
  - read from an argument, stdin, or a file,
  - write to stdout or a file,
  - list available layouts/pairs and switch between them.
- Optional clipboard helpers once the basic CLI is finished.

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the current plan.

---

## Status

> ⚠️ The project is under active development.  
> A prototype of the core and CLI in Python is currently being built.

---

## Installation (Python prototype)

Everything is in development mode for now, so install it via `pip` inside the repository:

```bash
git clone https://github.com/theveenrok/key-flip.git
cd key-flip
pip install -e .
```

## License

`key-flip` is distributed under the [MIT License](LICENSE).

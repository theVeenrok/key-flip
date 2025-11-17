# Roadmap — key-flip

`key-flip` roadmap: minimal Python core → CLI tool → shared specs and regression tests.

Statuses:
- [ ] not started
- [ ] in progress
- [x] completed

---

## Stage 1. Python core prototype

- [ ] Finalize the layout description format and document it in `docs/`.
- [ ] Implement layout loading and input validation.
- [ ] Build character mappings and implement `flip_text`.
- [ ] Add unit tests that cover casing, digits, and punctuation.

---

## Stage 2. Python CLI

- [ ] Implement a CLI with argparse/click and flags `--pair`, `--from/--to`, `--auto-dir`, `-i/--input`, `-o/--output`.
- [ ] Add commands `--list-layouts` and `--list-pairs`.
- [ ] Configure an entry point in `pyproject.toml` and document install/usage steps in the README.
- [ ] Add a clipboard helper (`--clipboard`) as a follow-up task once the base CLI is ready.

---

## Stage 3. Shared tests/specs

- [ ] Design `tests-spec/` (JSON/TOML with input, expectation, and metadata).
- [ ] Document the format and contribution process in `docs/SPEC.md` or a dedicated note.
- [ ] Write a Python runner that executes specs against the current core.
- [ ] Provide instructions for maintaining specs and automating regression runs.

---

## Next steps

1. Ship the Python core and baseline tests (Stage 1).
2. Build the minimal CLI tool and document installation (Stage 2).
3. Set up shared specs and automated regression runs (Stage 3).

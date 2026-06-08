# Repository Guidelines

## Project Structure & Module Organization

This is a Python support triage exercise. Source code lives in `src/`:
`triage.py` is the main agent entry point, `kb.py` contains provided data
loading, search, and mock backend helpers, and `models.py` contains Pydantic
model stubs. JSON fixtures are in `data/`: tickets, knowledge-base articles,
and labeled evaluation data. Tests live in `tests/`, starting with
`tests/test_smoke.py`. Interview-only reference material is in `interviewer/`.

## Build, Test, and Development Commands

- `uv sync`: install runtime and dev dependencies into the local virtualenv.
- `cp .env.example .env`: create local environment config, then add
  `OPENAI_API_KEY` when model calls are needed.
- `uv run pytest -q`: run the test suite without verbose output.
- `uv run python -m src.triage`: run the triage scaffold over sample tickets.

## Coding Style & Naming Conventions

Use Python 3.10+ and keep changes small. Follow existing style: 4-space
indentation, snake_case functions and variables, uppercase constants, and
Pydantic models for structured output validation. Keep customer-facing reply
logic grounded in `data/kb_articles.json` and the helpers in `src/kb.py`.
Avoid speculative abstractions; three direct lines are acceptable when a helper
would only be used once.

## Testing Guidelines

Tests use `pytest`. Name test files `test_*.py` and test functions
`test_*`. Existing smoke tests validate fixture loading and helper behavior.
Add focused tests when changing classification, identifier extraction,
knowledge-base grounding, escalation, or fraud-sensitive disclosure handling.
Run `uv run pytest -q` before submitting changes.

## Commit & Merge Request Guidelines

Use commitizen messages. Scope commits with the ticket from the branch name
such as `EX-1234`; use `EX-0000` if no ticket exists. Keep the title under 50
characters and wrap the body at 72 characters.

```gitcommit
feat(EX-0000): add triage validation
```

Create merge requests with `glab`, target `master`, assign to `me`, and use
the repository's reviewer rules. Include a short description, linked issue or
ticket when available, and test results.

## Security & Configuration Tips

Do not commit `.env` or API keys. Never reveal fraud reasons or detection
signals in customer-facing drafts; route sensitive cases for human review.

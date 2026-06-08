# Support Triage Exercise — Setup

You have **~90 minutes of coding** plus discussion.
Read [CANDIDATE_BRIEF.md](./CANDIDATE_BRIEF.md) for the task description.

## Setup

This project uses [uv](https://docs.astral.sh/uv/). Install it first if needed:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS/Linux
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then sync dependencies (uv creates the virtualenv for you) and add your key:

```sh
uv sync                     # installs deps incl. dev group (pytest)
cp .env.example .env        # we'll give you the OPENAI_API_KEY at the start
```

Verify the scaffold works (no API key needed):

```sh
uv run pytest -q
```

Run the (currently unfinished) agent:

```sh
uv run python -m src.triage
```

> Prefer pip? `uv pip install -e ".[dev]"` works too, or `pip install openai pydantic python-dotenv pytest`.

## Project layout

```
data/
  tickets.json        # 12 sample support tickets
  kb_articles.json    # 8 sample help-center articles
  labeled_eval.json   # ground-truth labels (for the eval extension)
src/
  models.py           # Pydantic stubs — fill in
  kb.py               # PROVIDED: data loading, naive Knowledge Base search, mock backend tools
  triage.py           # PROVIDED skeleton with TODOs — your main work goes here
tests/
  test_smoke.py       # provided smoke tests; add your own
```

## Rules

- You may use **any libraries** (LangChain, LlamaIndex, PydanticAI, raw SDK, _etc._)
  and look up online documentation.
- The mock data stands in for our real tickets and help-center articles.
  Treat it as if it were production data.
- Prefer working code we can run over lots of unfinished code.
- Commit early, commit often.
- Think out loud. We care more about how you reason than about a perfect result.

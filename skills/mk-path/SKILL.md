---
name: mk-path
description: Use when working in the MK-PATH repository (Evidence-Gated Autonomous Data Platform) — a FastAPI + DuckDB backend with a React 19/Vite frontend. Captures the recurring patterns from its git history: optional-service fallback (MongoDB/LLM), DuckDB dataset views over Parquet, per-project dataset isolation, a real-data-only policy, and MongoDB None-safety.
---

# MK-PATH Development

## Overview

Skill distilled from the 20-commit history of the `MK-PATH` app repo (14 `fix:`,
3 `feat:`, 1 `docs:` — all by one author). The history is dominated by bug fixes in
the same few files, which reveals the platform's real fault lines:

- `backend/app/database.py` — MongoDB Atlas with a local JSON fallback
- `backend/app/ingestion/registry.py` — DuckDB view lifecycle over normalized Parquet
- `backend/app/analysis/analyst.py`, `backend/app/modeling/tournament.py` — schema-grounded analysis and model tournament
- `frontend/src/lib/api.ts`, `frontend/src/pages/projects/**` — a hardcoded API base and many workspace pages

Read the command history as: *the system must keep working when an external
dependency (Mongo, LLM) is missing, when a dataset is tiny or oddly typed, and
when the data came from a real user upload rather than a fixture.*

## Patterns

### Pattern 1: Optional-service fallback (never crash on a missing dependency)
- When to use: any code touching MongoDB or an LLM provider.
- Implementation: attempt the real service with a short timeout; on any failure log a
  warning and switch transparently to a deterministic fallback. Startup must stay alive
  and `/api/health/database` returns a `degraded_*` status instead of raising.
- Example: `DatabaseManager.connect()` falls back to `LocalFallbackDB` (JSON files under
  `data/metadata/`) when `MONGODB_URI` is unset or Atlas times out. The semantic layer
  uses a `NullProvider` and runs deterministic-only when no LLM key is present.
- Commit evidence: `fix(database): transparent local file fallback ... when MongoDB
  Atlas connection times out or SSL fails`; `fix(llm): set Groq fallback model`.

### Pattern 2: DuckDB views over normalized Parquet
- When to use: any query against an ingested dataset.
- Implementation: datasets are registered as in-memory DuckDB views named
  `ds_<dataset_id>` (see `app/ingestion/registry.py`). Always call
  `registry.ensure_view(dataset_id, normalized_path)` before querying; it re-registers
  from Parquet/metadata if the view is missing. DuckDB is a single in-memory connection —
  never assume a view survives a process restart.
- Commit evidence: `fix: resolve DuckDB parquet view registration, dataset explorer read
  preview, and model tournament execution`.

### Pattern 3: Per-project / per-workspace dataset isolation
- When to use: listing, uploading, or scoping datasets.
- Implementation: every dataset carries a `project_id`; list/count queries filter by it.
  Do not let datasets leak across projects.
- Commit evidence: `fix(workspace): isolate datasets per workspace, fix dataset upload
  association`.

### Pattern 4: Real uploaded data only — no mock/template data
- When to use: dashboards, samples, demos, seeds.
- Implementation: do **not** reintroduce mock, template, or hardcoded sample datasets.
  Every view is driven by datasets the user actually uploaded.
- Commit evidence: `fix: completely remove mock template data and enforce real-time
  uploaded dataset only` (this reversed an earlier "add sample dashboard templates" change).

### Pattern 5: MongoDB None-safety
- When to use: guards around the DB handle.
- Implementation: use `is not None`, never truthiness. `self._db` can be a PyMongo/async
  object whose `__bool__` raises.
- Commit evidence: `fix(database): compare self._db with is not None to prevent
  AsyncDatabase truth testing NotImplementedError`.

### Pattern 6: Small / oddly-typed datasets
- When to use: profiling, healing, tournament on tiny or boolean columns.
- Implementation: handle single-class targets, boolean columns before quantiles, and
  very small row counts explicitly; never assume a continuous float column.
- Commit evidence: `fix(healing,tournament): fix boolean quantile 500 in healing engine
  and support small datasets in tournament`.

### Pattern 7: Keep train/inference feature names aligned
- When to use: engineering/tournament inference.
- Implementation: preserve the exact feature-name order used at fit time when building
  test inference frames.
- Commit evidence: `fix: ... match test inference feature names`.

## Best Practices

1. Run backend tests from `backend/` (`python -m pytest tests/`); `conftest.py` assumes
   the app is importable as top-level `app`.
2. Call `ensure_view(...)` immediately before any DuckDB query.
3. Guard every external call with the fallback pattern; log a warning, never raise at startup.
4. Use `is not None` for DB/client objects.
5. Keep MongoDB for metadata/audit only; raw datasets, Parquet, and models stay on disk.
6. Finish frontend work with `npm run build` (`tsc -b && vite build`); there is no frontend test runner.
7. Follow conventional-commit scopes seen in history: `fix(area): ...`, `feat(area): ...`,
   `docs: ...`.

## Common Mistakes

1. `if self._db:` / truthiness on a PyMongo handle — raises `NotImplementedError`; use `is not None`.
2. Querying a dataset without registering its view — binder errors and empty results; call `ensure_view` first.
3. Assuming `MONGODB_URI` or an LLM key exists — the app must run at reduced capability without them.
4. Adding demo/sample/mock data — explicitly disallowed by the most recent commit's intent.
5. Committing `data/`, `datasets/`, `models/`, `artifacts/` — all gitignored; metadata goes to Mongo/JSON.
6. Trusting the Windows commands in the README (`..\.venv\Scripts\python`) on Linux; use `.venv/bin/python` or `python`.

## Examples

### Good example — optional dependency with graceful fallback
```python
# backend/app/database.py
try:
    if self._client is None:
        self._client = AsyncMongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2000)
    await self._client.admin.command("ping")
    self._db = self._client[settings.MONGODB_DATABASE]
except Exception as exc:
    self._client = None
    self._db = self._fallback_db            # local JSON fallback, no crash
    self._last_error = type(exc).__name__
    logger.warning("MongoDB unavailable (%s). Using local fallback.", type(exc).__name__)
```

### Good example — ensure a DuckDB view before querying
```python
# backend/app/routers/pipeline.py
registry.ensure_view(req.dataset_id, ds_doc.get("normalized_path"))
conn = registry.get_conn()
v_name = registry.view_name(req.dataset_id)
df = conn.execute(f'SELECT * FROM "{v_name}"').df()
```

### Anti-pattern — trustiness check and stale view
```python
# WRONG: PyMongo handles raise on truth testing
if db_manager.get_database():
    ...

# WRONG: querying a view that may not be registered in this process
conn.execute(f'SELECT * FROM "ds_{dataset_id}"')  # binder error if never registered
```

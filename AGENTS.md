# AGENTS.md

## Repository layout (read first)
- The actual application lives in the nested `MK-PATH/` directory. All commands below run from there unless stated otherwise.
- Workspace root extras are **not** part of the app: `.opencode/` is the agent harness config, `SKILL.md` is a doc-authoring skill, `README.md` is a stub.
- There are two git repos. The app repo is `MK-PATH/` (remote `Joelrajjoe/MK-PATH`); the workspace root is a separate scaffold repo. Commit application changes inside `MK-PATH/`.

## Backend — FastAPI + DuckDB + optional MongoDB
- Install: `cd MK-PATH/backend && pip install -r requirements.txt`. No venv or deps are vendored.
- Config: copy `MK-PATH/.env.example` to `MK-PATH/.env` (gitignored). Keys come from env only; never hardcode or commit secrets.
- Run: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`. The README shows the Windows form (`..\.venv\Scripts\python`); on Linux use `python` or `.venv/bin/python`.
- Tests: `cd MK-PATH/backend && python -m pytest tests/`. Single test: `python -m pytest tests/test_ingestion.py::test_csv_upload_and_contract`.
  - `tests/conftest.py` inserts `backend/` into `sys.path` and imports the app as top-level `app`, so run pytest from `backend/`.
  - Tests exercise the real FastAPI app through `TestClient` (services are not mocked) and write real Parquet/files to disk; cleanup deletes test metadata from Mongo on a best-effort basis.
- MongoDB is **optional**: with `MONGODB_URI` unset the app serves from a local JSON fallback under `data/metadata/*.json` (`app/database.py`). Startup must never crash when the DB is down — it degrades instead.
  - The JSON fallback is a partial PyMongo shim (insert/find/update/count only — no `delete_*`/`aggregate`). Delete or aggregation flows need a real Mongo to verify.
- Storage invariant: MongoDB holds metadata/audit state only; raw datasets, normalized Parquet, models, and artifacts live on disk in directories created by `app/config.py` (`data/ datasets/ models/ artifacts/ logs/ reports/ temp/`), all gitignored.
  - `config.py` derives `ROOT_DIR` from its own file location (`parents[2]` = `MK-PATH/`), so storage follows the checkout. Windows-isms remain in `backend/reset_workspace.py` and root `audit_storage.py`, which hardcode `E:\MKPATH`.
- Backend domains under `app/`: `ingestion`, `profiling`, `semantic`, `modeling`, `analysis`, `healing`, `verification`, `orchestrator`, `engineering`, `routers`. `repo.py` = metadata access, `audit.py` = audit events, `database.py` = Mongo/fallback.
- Each dataset is registered as an in-memory DuckDB view `ds_<dataset_id>` over its normalized Parquet (`app/ingestion/registry.py`); profiling is deterministic / zero-LLM.
- No Python linter/formatter is configured (no ruff/black) — don't assume one.

## Verified operational gotchas

### Running the app for UI screenshots / E2E work
- **Both servers must be running simultaneously.** Backend on `127.0.0.1:8000`, frontend dev server on `5173`.
- **Start backend**: `cd MK-PATH/backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` (must run from `backend/` or imports fail).
- **Start frontend**: `cd MK-PATH/frontend && npm run dev -- --host 0.0.0.0 --port 5173 --strictPort` (explicit flags needed; default binds to localhost only).

### In-process API scripts (TestClient)
- **`TestClient(app)` without `with` does NOT run the app lifespan** → the app silently uses the JSON fallback under `data/metadata/` instead of MongoDB Atlas. Always use `with TestClient(app) as client:` or call `client.__enter__()` so Atlas is used.
- **Upload requires `data={"project_id": project_id}`** in the POST to `/api/datasets/upload`. Without it, the dataset is orphaned (`project_id: None`) and won't appear under the project in the UI.
- **POST `/api/datasets/{id}/semantic` returns a summary wrapper** (version, confidence, open_ambiguities) — NOT the concept graph. Use GET on the same path to read the full context (metrics, dimensions, terms).
- **`/api/datasets/{id}/quality` returns `top_issues`**, not `issues`.
- **`check_ambiguity` only stops on `severity == "blocking" and status == "open"`**. LLM_PROPOSED ambiguities are advisory and don't pause the pipeline.
- **Orchestrator target selection order**: user_decisions choice → `semantic_ctx["targets"][0]` → concept type=target → `plan["metrics"][0]`. The chosen target may differ from what the UI's on-demand tournament defaults to (last column).

### Running the orchestrator
- `POST /api/runs/execute` with `{project_id, dataset_id, business_goal}` triggers the full LangGraph pipeline.
- The run emits project-scoped audit events: `INGEST_START → PROFILE_START → SEMANTIC_ANALYSIS → ANALYSIS_PLANNING → DATA_ANALYST_START → VERIFICATION_START → WORKFLOW_COMPLETED`.
- Runs pause at `AMBIGUITY_CHECK` only if blocking ambiguities are open; resolve all blocking questions first for a complete run.
- There is no resume endpoint — re-executing creates a new `run_id`.

### E2E validation scripts (`_e2e_validation/`)
- Scripts are now portable (Linux-compatible; `BASE_DIR` from `parents[2]`).
- `SUPERSTORE_CSV` env var overrides the dataset path; defaults to `/workspaces/MK-PATH/Superstore sales dataset.csv`.
- `run_track_a.py` uses `atexit` + `TestClient.__enter__()` to run the lifespan and connect to Atlas.
- Evidence JSONL is written to `_e2e_validation/<run_id>/evidence/`.

## Frontend — React 19 + Vite + TypeScript + Tailwind v4
- Install: `cd MK-PATH/frontend && npm install`.
- Dev: `npm run dev`. Build + typecheck: `npm run build` (`tsc -b && vite build`). Lint: `npm run lint` (oxlint). No test runner (vitest/jest) is configured.
- API base URL is hardcoded as `http://localhost:8000/api` in `src/lib/api.ts`; there is **no** Vite dev proxy, so the backend must listen on port 8000. Backend CORS is `*`.
- `@/` path alias resolves to `src/` (declared in both `tsconfig.app.json` and `vite.config.ts`).

## Conventions
- LLM keys (`GEMINI_API_KEY`, `GROQ_API_KEY`) are optional; the semantic layer runs deterministic-only without them and never invents business meaning.
- `docs/` holds historical phase reports (many `PHASE_*_STATUS.md`, verification/audit reports). Treat them as design history, not current truth — verify against code.

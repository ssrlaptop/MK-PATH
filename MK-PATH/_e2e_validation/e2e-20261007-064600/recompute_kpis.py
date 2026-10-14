import os
import json
from pathlib import Path
import pandas as pd
import duckdb

BASE_DIR = Path(os.environ.get("MKPATH_ROOT", Path(__file__).resolve().parents[2])).resolve()
RUN_ID = os.environ.get("E2E_RUN_ID", Path(__file__).resolve().parent.name)
EVIDENCE_DIR = BASE_DIR / "_e2e_validation" / RUN_ID / "evidence"


def resolve_superstore_csv(base_dir: Path) -> Path:
    env = os.environ.get("SUPERSTORE_CSV")
    candidates = [Path(env)] if env else []
    candidates += [
        base_dir.parent / "Superstore sales dataset.csv",
        base_dir / "Superstore sales dataset.csv",
    ]
    candidates += sorted(base_dir.glob("datasets/*/Superstore sales dataset.csv"))
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError("Superstore CSV not found; set SUPERSTORE_CSV=<path>.")


def resolve_superstore_parquet(base_dir: Path) -> Path:
    """Find the normalized Parquet whose schema contains the Superstore 'Profit' column."""
    env = os.environ.get("SUPERSTORE_PARQUET")
    if env and Path(env).exists():
        return Path(env)
    for p in sorted(base_dir.glob("data/**/*.parquet")):
        try:
            cols = duckdb.connect().execute(f"DESCRIBE SELECT * FROM read_parquet('{p.as_posix()}')").df()
        except Exception:
            continue
        names = set(cols["column_name"].tolist())
        if {"Profit", "Sales", "Sub-Category"}.issubset(names):
            return p
    raise FileNotFoundError("Superstore Parquet not found; set SUPERSTORE_PARQUET=<path>.")


source_csv_path = resolve_superstore_csv(BASE_DIR)
raw_df = pd.read_csv(source_csv_path, encoding="utf-8", encoding_errors="replace")

# Setup DuckDB query directly on the normalized Parquet registered for this dataset
parquet_path = resolve_superstore_parquet(BASE_DIR).as_posix()
print(f"Using source CSV   : {source_csv_path}")
print(f"Using Parquet      : {parquet_path}")
conn = duckdb.connect()

metrics = ["Sales", "Quantity", "Profit", "Discount"]
kpi_comparison = {}

for m in metrics:
    q = f'SELECT SUM("{m}") as sum_val, AVG("{m}") as avg_val, MIN("{m}") as min_val, MAX("{m}") as max_val FROM read_parquet(\'{parquet_path}\')'
    duck_res = conn.execute(q).df().to_dict(orient="records")[0]

    s = raw_df[m].dropna()
    ind_sum = float(s.sum())
    ind_avg = float(s.mean())
    ind_min = float(s.min())
    ind_max = float(s.max())

    sys_sum = float(duck_res["sum_val"])
    sys_avg = float(duck_res["avg_val"])
    sys_min = float(duck_res["min_val"])
    sys_max = float(duck_res["max_val"])

    diff_sum = abs(sys_sum - ind_sum)
    diff_avg = abs(sys_avg - ind_avg)

    kpi_comparison[m] = {
        "system_sum": sys_sum,
        "ind_sum": ind_sum,
        "diff_sum": diff_sum,
        "system_avg": sys_avg,
        "ind_avg": ind_avg,
        "diff_avg": diff_avg,
        "system_min": sys_min,
        "ind_min": ind_min,
        "system_max": sys_max,
        "ind_max": ind_max,
        "tolerance": 1e-4,
        "status": "PASS" if diff_sum < 1e-4 and diff_avg < 1e-4 else "FAIL"
    }

EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
with open(EVIDENCE_DIR / "a8_kpi_comparison.json", "w", encoding="utf-8") as f:
    json.dump(kpi_comparison, f, indent=2)

print("KPI Recomputation Results:")
for m, v in kpi_comparison.items():
    print(f" - {m}: System SUM={v['system_sum']:.2f}, Ind SUM={v['ind_sum']:.2f}, diff={v['diff_sum']:.6f} => {v['status']}")

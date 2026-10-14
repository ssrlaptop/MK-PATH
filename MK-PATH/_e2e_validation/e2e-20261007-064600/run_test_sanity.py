import os
import sys
import subprocess
import json
from pathlib import Path

BASE_DIR = Path(os.environ.get("MKPATH_ROOT", Path(__file__).resolve().parents[2])).resolve()
RUN_ID = os.environ.get("E2E_RUN_ID", Path(__file__).resolve().parent.name)
EVIDENCE_DIR = BASE_DIR / "_e2e_validation" / RUN_ID / "evidence"

tests = [
    "tests/test_projects.py",
    "tests/test_remediation.py",
    "tests/test_profiling.py",
    "tests/test_ingestion.py"
]

results = {}
for t in tests:
    # Use the interpreter running this script (works on any OS / venv layout).
    cmd = [sys.executable, "-m", "pytest", t, "-q"]
    proc = subprocess.run(cmd, cwd=str(BASE_DIR / "backend"), capture_output=True, text=True)
    results[t] = {
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "status": "PASS" if proc.returncode == 0 else "FAIL"
    }

with open(EVIDENCE_DIR / "b3_test_sanity.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Test-suite sanity complete:")
for t, r in results.items():
    print(f" - {t}: {r['status']} (code {r['exit_code']})")

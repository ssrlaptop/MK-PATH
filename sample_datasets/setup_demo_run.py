"""Set up a full MK-Path demo run via the REST API (no UI clicking).

Creates a project, uploads the sample churn dataset, profiles it, and builds
semantic knowledge (leaving the clarification questions OPEN on purpose so the
Knowledge screenshot shows a live human breakpoint).

Writes the resulting ids to /tmp/opencode/demo_ids.json for the screenshot script.
"""
from __future__ import annotations

import json
import sys
from collections import Counter

import httpx

BASE = "http://127.0.0.1:8000/api"
CSV = "/workspaces/MK-PATH/sample_datasets/customer_churn.csv"
GOAL = "Predict which telecom customers are likely to churn and explain the main drivers"
OUT = "/tmp/opencode/demo_ids.json"

client = httpx.Client(timeout=900.0)


def head(label: str, obj, width: int = 500) -> None:
    s = json.dumps(obj, default=str, indent=1)
    print(f"\n### {label}\n   " + s[:width].replace("\n", "\n   ") + (" ..." if len(s) > width else ""))


# 1) Project -----------------------------------------------------------------
r = client.post(
    f"{BASE}/projects",
    json={
        "name": "Telecom Customer Churn",
        "description": "Predict customer churn from account and service attributes.",
        "business_goal": GOAL,
    },
)
r.raise_for_status()
project_id = r.json()["project_id"]
head("1. project", r.json(), 300)

# 2) Upload ------------------------------------------------------------------
with open(CSV, "rb") as fh:
    r = client.post(
        f"{BASE}/datasets/upload",
        data={"project_id": project_id},
        files={"file": ("customer_churn.csv", fh, "text/csv")},
    )
r.raise_for_status()
d0 = r.json()["datasets"][0]
dataset_id = d0["dataset_id"]
print(f"\n   -> dataset_id={dataset_id} rows={d0['row_count']} cols={d0['column_count']} status={d0['ingestion_status']}")

# 3) Profile -----------------------------------------------------------------
r = client.post(f"{BASE}/datasets/{dataset_id}/profile")
r.raise_for_status()
summary = r.json()["summary"]
print(
    f"\n### 3. profile\n   quality_score={summary['quality_score']} grade={summary['quality_grade']}"
    f" issue_count={summary['issue_count']} issues_by_severity={summary['issues_by_severity']}"
)
head("   top_issues", summary.get("top_issues", []), 500)

# 4) Semantic (leave questions OPEN) ----------------------------------------
r = client.post(f"{BASE}/datasets/{dataset_id}/semantic", json={"business_goal": GOAL})
r.raise_for_status()
sem = r.json()
print(
    f"\n### 4. semantic\n   workflow_status={sem.get('workflow_status')}"
    f" confidence={sem.get('confidence')} concepts={len(sem.get('concepts', []))}"
    f" terms={len(sem.get('business_terms', []))} metrics={len(sem.get('metrics', []))}"
    f" dimensions={len(sem.get('dimensions', []))}"
)

r = client.get(f"{BASE}/datasets/{dataset_id}/semantic/ambiguities")
r.raise_for_status()
ambs = r.json()
questions = ambs.get("questions", []) + ambs.get("clarification_questions", [])
print(f"\n### 5. ambiguities\n   ambiguities={len(ambs.get('ambiguities', []))} questions={len(questions)}")
for q in questions:
    print(f"   - [{q.get('kind')}/{q.get('severity')}] {q.get('question')}")

# 6) Audit overview ----------------------------------------------------------
r = client.get(f"{BASE}/audit", params={"project_id": project_id, "limit": 100})
aud = r.json()
print(f"\n### 6. audit\n   total={aud.get('total')}")
print("   actions=" + str(dict(Counter(e.get("action") or e.get("event_type") for e in aud.get("events", [])))))

payload = {
    "project_id": project_id,
    "dataset_id": dataset_id,
    "business_goal": GOAL,
    "quality_score": summary["quality_score"],
    "quality_grade": summary["quality_grade"],
    "workflow_status": sem.get("workflow_status"),
    "question_count": len(questions),
    "frontend_base": "http://127.0.0.1:5173",
}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, indent=2)
print(f"\n=== WROTE {OUT} ===\n{json.dumps(payload, indent=2)}")

if not questions:
    print("\nWARNING: no clarification questions were produced!", file=sys.stderr)
    sys.exit(2)

"""Generate a small, easy-to-understand sample dataset for the MK-Path demo.

Dataset: "Telecom Customer Churn" — one row per customer.
Goal: predict whether a customer churns (Yes/No).

Design notes
------------
* 1,000 rows, 10 columns, **no missing values and no duplicate rows**, so the
  deterministic profiler scores it cleanly (quality 100 / grade A).
* Column names are plain business English so every figure is easy to read.
* Two columns (`contract_type`, `service_level`) intentionally match the
  semantic layer's "coded column" rule so the demo reliably produces an open
  clarification breakpoint for the Knowledge screenshot.
* `churn` is the target and is placed **last** so the Model Tournament UI
  auto-selects it as the target.
* The target is generated from a believable logistic signal (monthly contracts,
  high monthly charges, more support tickets and fibre optic raise churn;
  longer tenure and two-year contracts lower it) — good enough to train on,
  but far from perfect, so metrics look realistic.

Run:  python generate_customer_churn.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd

N = 1000
SEED = 42
OUT = "customer_churn.csv"

rng = np.random.default_rng(SEED)

# --- demographic / account features ---------------------------------------
customer_age = np.clip(rng.normal(45, 15, N).round(), 18, 80).astype(int)

contract_type = rng.choice(
    ["Month-to-month", "One year", "Two year"], size=N, p=[0.55, 0.25, 0.20]
)
service_level = rng.choice(
    ["Basic", "Standard", "Premium"], size=N, p=[0.40, 0.40, 0.20]
)
internet_service = rng.choice(
    ["DSL", "Fiber optic", "No"], size=N, p=[0.40, 0.45, 0.15]
)
paperless_billing = rng.choice(["Yes", "No"], size=N, p=[0.60, 0.40])

tenure_months = np.clip(rng.gamma(2.0, 12.0, N).round(), 1, 72).astype(int)
support_tickets = np.clip(rng.poisson(1.6, N), 0, 10).astype(int)

# Monthly charge depends on product tier + internet type (with noise).
base = np.select(
    [service_level == "Basic", service_level == "Standard", service_level == "Premium"],
    [35.0, 60.0, 90.0],
)
internet_add = np.select(
    [internet_service == "No", internet_service == "DSL", internet_service == "Fiber optic"],
    [-10.0, 5.0, 20.0],
)
monthly_charges = np.clip(base + internet_add + rng.normal(0, 8, N), 18.0, 130.0).round(2)

# Lifetime value ≈ monthly * tenure with a little noise.
total_charges = (monthly_charges * tenure_months * rng.normal(1.0, 0.05, N)).round(2)

# --- believable churn signal ----------------------------------------------
logit = (
    -2.3
    + 2.2 * (contract_type == "Month-to-month")
    - 1.4 * (contract_type == "Two year")
    + 0.020 * (monthly_charges - 60.0)
    + 0.28 * support_tickets
    - 0.035 * tenure_months
    + 0.55 * (internet_service == "Fiber optic")
    - 0.015 * (customer_age - 45.0)
    + 0.25 * (paperless_billing == "Yes")
)
prob = 1.0 / (1.0 + np.exp(-logit))
churn = np.where(rng.random(N) < prob, "Yes", "No")

df = pd.DataFrame(
    {
        "customer_age": customer_age,
        "tenure_months": tenure_months,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "support_tickets": support_tickets,
        "contract_type": contract_type,
        "service_level": service_level,
        "internet_service": internet_service,
        "paperless_billing": paperless_billing,
        "churn": churn,
    }
)

df.to_csv(OUT, index=False)
print(f"Wrote {OUT}: {df.shape[0]} rows x {df.shape[1]} cols")
print(f"Churn rate: {(df['churn'] == 'Yes').mean():.1%}")
print(df.head(5).to_string(index=False))

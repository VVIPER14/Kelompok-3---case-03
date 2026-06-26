"""
train_model.py — Case 03: Predictive Maintenance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    recall_score,
    precision_score,
    f1_score,
    precision_recall_curve,
    auc,
)
from imblearn.over_sampling import SMOTE

# Load Data
df = pd.read_csv("../data/processed/dataset_clean.csv", parse_dates=["timestamp"])

# Splitting Data
df_sorted = df.sort_values("timestamp").reset_index(drop=True)

FEATURE_COLS = [
    "age_months", "last_maintenance_days",
    "temp_c", "vibration_mm_s", "current_a",
    "load_pct", "lubricant_level_pct", "alarm_count",
]
TARGET = "downtime_next_24h"

X_sorted = df_sorted[FEATURE_COLS]
y_sorted = df_sorted[TARGET]

split_idx = int(len(df_sorted) * 0.8)
X_train, X_test = X_sorted.iloc[:split_idx], X_sorted.iloc[split_idx:]
y_train, y_test = y_sorted.iloc[:split_idx], y_sorted.iloc[split_idx:]

print(f"Train : {len(X_train)} baris ({y_train.sum()} downtime, rate {y_train.mean()*100:.1f}%)")
print(f"Test  : {len(X_test)} baris ({y_test.sum()} downtime, rate {y_test.mean()*100:.1f}%)")

# Scaling Data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# SMOTE 
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X_train_scaled, y_train)
print(f"Distribusi setelah SMOTE: {dict(pd.Series(y_res).value_counts())}")

# Logistic Regression
lr = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
lr.fit(X_res, y_res)

# Random Forest
rf = RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42)
rf.fit(X_res, y_res)

# Training + Hasil 
proba_lr = lr.predict_proba(X_test_scaled)[:, 1]
proba_rf = rf.predict_proba(X_test_scaled)[:, 1]

# Prediksi dengan threshold default 0.50
y_pred_lr_base = (proba_lr >= 0.50).astype(int)
y_pred_rf_base = (proba_rf >= 0.50).astype(int)

print("=" * 55)
print("=== BASELINE: Logistic Regression (threshold=0.50) ===")
print(classification_report(y_test, y_pred_lr_base, target_names=["Normal", "Downtime"]))

print("=" * 55)
print("=== BASELINE: Random Forest (threshold=0.50) ===")
print(classification_report(y_test, y_pred_rf_base, target_names=["Normal", "Downtime"]))

print("\n=== Ringkasan KPI Baseline ===")
for nama, y_pred in [("Logistic Regression", y_pred_lr_base), ("Random Forest", y_pred_rf_base)]:
    cm_val = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm_val.ravel()
    recall = tp / (tp + fn)
    far    = fp / (fp + tn)
    print(f"\n{nama}:")
    print(f"  Recall Downtime  : {recall:.1%}  (target >= 80%)")
    print(f"  False Alarm Rate : {far:.1%}")
    print(f"  TP: {tp} | FN: {fn} | FP: {fp} | TN: {tn}")


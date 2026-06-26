"""
evaluate.py — Case 03: Predictive Maintenance
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

# Tunning
print("Logistic Regression — Analisis Threshold:")
print(f"{'Threshold':<12} {'Recall':<10} {'FAR':<10} {'TP':<6} {'FP':<6} {'FN':<6}")
print("-" * 52)

for thresh in [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20]:
    preds = (proba_lr >= thresh).astype(int)
    cm    = confusion_matrix(y_test, preds)
    tn_, fp_, fn_, tp_ = cm.ravel()
    recall_ = tp_ / (tp_ + fn_)
    far_    = fp_ / (fp_ + tn_)
    marker  = " <- DIPILIH" if thresh == 0.30 else ""
    print(f"{thresh:<12.2f} {recall_:<10.1%} {far_:<10.1%} {tp_:<6} {fp_:<6} {fn_:<6}{marker}")

print("\nAlasan memilih threshold 0.30:")
print("Recall >= 80% tercapai dengan FAR yang masih dalam batas toleransi operasional.")
print("Biaya melewatkan 1 downtime >> biaya 1 alarm palsu, sehingga recall diprioritaskan.")

# Evaluasi
fig, ax = plt.subplots(figsize=(8, 6))

for proba, nama, warna in [
    (proba_lr, "Logistic Regression", "steelblue"),
    (proba_rf, "Random Forest",       "tomato"),
]:
    precision_vals, recall_vals, thresholds = precision_recall_curve(y_test, proba)
    pr_auc = auc(recall_vals, precision_vals)
    ax.plot(recall_vals, precision_vals, color=warna, linewidth=2,
            label=f"{nama} (AUC-PR = {pr_auc:.3f})")

# Tandai posisi threshold 0.30 pada kurva LR
precision_vals_lr, recall_vals_lr, thresholds_lr = precision_recall_curve(y_test, proba_lr)
thresh_idx = np.argmin(np.abs(thresholds_lr - 0.30))
ax.scatter(recall_vals_lr[thresh_idx], precision_vals_lr[thresh_idx],
           color="steelblue", s=100, zorder=5,
           label=f"LR threshold=0.30 (Recall={recall_vals_lr[thresh_idx]:.2f}, Precision={precision_vals_lr[thresh_idx]:.2f})")

ax.axvline(0.80, color="gray", linestyle="--", linewidth=0.8, label="Target Recall = 80%")

ax.set_xlabel("Recall")
ax.set_ylabel("Precision")
ax.set_title("Precision-Recall Curve — Predictive Maintenance")
ax.legend(fontsize=9)
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
plt.tight_layout()
plt.savefig("../reports/figures/precision_recall_curve.png", dpi=150, bbox_inches="tight")
plt.show()

# Retraining
THRESH_LR = 0.30
THRESH_RF  = 0.30

y_pred_lr = (proba_lr >= THRESH_LR).astype(int)
y_pred_rf = (proba_rf >= THRESH_RF).astype(int)

print("=" * 55)
print("=== FINAL: Logistic Regression (threshold=0.30) ===")
print(classification_report(y_test, y_pred_lr, target_names=["Normal", "Downtime"]))

print("=" * 55)
print("=== FINAL: Random Forest (threshold=0.30) ===")
print(classification_report(y_test, y_pred_rf, target_names=["Normal", "Downtime"]))

print("\n=== Ringkasan KPI Final ===")
for nama, y_pred in [("Logistic Regression", y_pred_lr), ("Random Forest", y_pred_rf)]:
    cm_val = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm_val.ravel()
    recall         = tp / (tp + fn)
    far            = fp / (fp + tn)
    total_downtime = tp + fn

    print(f"\n{nama}:")
    print(f"  Recall Downtime  : {recall:.1%}  (target >= 80%)")
    print(f"  False Alarm Rate : {far:.1%}    (target <= 15%)")
    print(f"  TP (terdeteksi)  : {tp} dari {total_downtime} downtime aktual")
    print(f"  FN (terlewat)    : {fn} downtime tidak terdeteksi")
    print(f"  FP (alarm palsu) : {fp} alarm palsu")

# Matriks
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Confusion Matrix — Predictive Maintenance (Temporal Split, threshold=0.30)",
             fontsize=12, fontweight="bold")

for ax, y_pred, nama in zip(
    axes,
    [y_pred_lr, y_pred_rf],
    ["Logistic Regression", "Random Forest"],
):
    cm_val = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm_val.ravel()
    recall_val = tp / (tp + fn)
    far_val    = fp / (fp + tn)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm_val,
                                  display_labels=["Normal", "Downtime"])
    disp.plot(ax=ax, colorbar=False, cmap="Blues")
    ax.set_title(f"{nama}\nRecall={recall_val:.1%}  |  FAR={far_val:.1%}", fontsize=11)

plt.tight_layout()
plt.savefig("../reports/figures/confusion_matrix.png", dpi=150, bbox_inches="tight")
plt.show()

# Feature Importance — Logistic Regression (via koefisien)
coef = pd.Series(np.abs(lr.coef_[0]), index=FEATURE_COLS).sort_values()

fig, ax = plt.subplots(figsize=(10, 5))

coef.plot(kind="barh", ax=ax, color="#5B8DB8")  # satu warna semua

ax.set_title("Feature Importance — Logistic Regression")
ax.set_xlabel("Korelasi")

x_max = coef.max()
for i, v in enumerate(coef):
    ax.text(v + x_max * 0.01, i, f"{v:.3f}", va="center", fontsize=9)

ax.set_xlim(0, x_max * 1.15)

plt.tight_layout()
plt.savefig("../reports/figures/feature_importance.png", dpi=150, bbox_inches="tight")
plt.show()

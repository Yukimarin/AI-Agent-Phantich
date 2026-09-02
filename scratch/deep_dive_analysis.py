import sys
import openpyxl
import pandas as pd
import numpy as np
import json
import os

sys.stdout.reconfigure(encoding="utf-8")

with open("scratch/standardized_master_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ks24 = data["ks24"]
ks25 = data["ks25"]
qtkd = data["qtkd"]

print("=== 1. PHÂN TÍCH THEO CA THI / ĐỘ LỆCH ĐỀ THI (KS24) ===")
df_ks24 = pd.DataFrame([s for s in ks24 if not s["is_absent"]])
print(df_ks24.groupby("ca")["final_10"].agg(["count", "mean", "std", "min", "max"]))

print("\n=== 2. PHÂN TÍCH THEO CA THI / ĐỘ LỆCH ĐỀ THI (KS25) ===")
df_ks25 = pd.DataFrame([s for s in ks25 if not s["is_absent"]])
print(df_ks25.groupby("ca")[["th", "tn", "final_10"]].agg(["count", "mean"]))

print("\n=== 3. PHÂN TÍCH ĐỘ LỆCH CHẤT LƯỢNG GIỮA CÁC LỚP (TEACHING BOTTLENECK) ===")
print("--- KS24 ---")
print(df_ks24.groupby("class")[["sp", "vd", "th", "tn", "final_10"]].mean().round(1))
print("\n--- KS25 ---")
print(df_ks25.groupby("class")[["th", "tn", "final_10"]].mean().round(1))

print("\n=== 4. PHÂN TÍCH TƯƠNG QUAN HỌC THUẬT (CORRELATION MATRIX) ===")
cols_ks24 = ["sp", "vd", "th", "tn", "knm", "ta"]
corr_ks24 = df_ks24[cols_ks24].corr().round(2)
print("Correlation KS24:\n", corr_ks24)

cols_ks25 = ["th", "tn", "knm", "ta"]
corr_ks25 = df_ks25[cols_ks25].corr().round(2)
print("\nCorrelation KS25:\n", corr_ks25)

print("\n=== 5. MÔ PHỎNG PHỄU TUYỂN DỤNG DOANH NGHIỆP (EMPLOYABILITY FUNNEL) ===")
# KS24 Simulation:
# Vòng 1: CV & KNM/TA (KNM >= 70 OR TA >= 400) -> Pass CV
# Vòng 2: Tech Interview (Vấn đáp >= 50)
# Vòng 3: Live Coding (Thực hành >= 50 OR Sản phẩm >= 65)
# Vòng 4: Final Hire (Pass cả 3 vòng)
v1_ks24 = len([s for s in ks24 if not s["is_absent"] and (s["knm"] >= 70 or s["ta"] >= 400)])
v2_ks24 = len([s for s in ks24 if not s["is_absent"] and s["vd"] >= 50])
v3_ks24 = len([s for s in ks24 if not s["is_absent"] and (s["th"] >= 50 or s["sp"] >= 65)])
v_hire_ks24 = len([s for s in ks24 if not s["is_absent"] and (s["knm"] >= 70 or s["ta"] >= 400) and s["vd"] >= 50 and (s["th"] >= 50 or s["sp"] >= 65)])

print(f"KS24 Employability Funnel (Trên {len(df_ks24)} SV dự thi):")
print(f"- Qua Vòng 1 (CV & KNM): {v1_ks24} SV ({round(v1_ks24/len(df_ks24)*100, 1)}%)")
print(f"- Qua Vòng 2 (Vấn đáp Kỹ thuật): {v2_ks24} SV ({round(v2_ks24/len(df_ks24)*100, 1)}%)")
print(f"- Qua Vòng 3 (Live Coding / Đồ án): {v3_ks24} SV ({round(v3_ks24/len(df_ks24)*100, 1)}%)")
print(f"- Trúng tuyển Doanh nghiệp chuẩn (Pass cả 3 vòng): {v_hire_ks24} SV ({round(v_hire_ks24/len(df_ks24)*100, 1)}%)")


import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

excel_path = "inputs/Danh sách thi ĐGNL.xlsx"
df_bd = pd.read_excel(excel_path, sheet_name="Bảng điểm (Đợt 1)")

# Filter KS24 CNTT
ks24_cntt = df_bd[df_bd["Mã lớp hiện tại"].astype(str).str.contains("KS24-CNTT", na=False)].copy()
# Filter KS25 CNTT
ks25_cntt = df_bd[df_bd["Mã lớp hiện tại"].astype(str).str.contains("KS25-CNTT", na=False)].copy()

print(f"=== KS24 CNTT ({len(ks24_cntt)} SV) ===")
for c in ["Đ1_Sản phẩm_CNTT", "Đ1_Vấn đáp_CNTT", "Đ1_Thực hành_CNTT", "Đ1_Trắc nghiệm_CNTT", "Đ1_Điểm CNTT (Final)", "Đ1_Tiếng Anh (Final)", "Đ1_Kỹ năng mềm (Final)"]:
    ks24_cntt[c] = pd.to_numeric(ks24_cntt[c], errors="coerce")
    print(f"  {c}: Mean={ks24_cntt[c].dropna().mean():.1f}, Count={ks24_cntt[c].dropna().shape[0]}")

print(f"\n=== KS25 CNTT ({len(ks25_cntt)} SV) ===")
for c in ["Đ1_Thực hành_CNTT", "Đ1_Trắc nghiệm_CNTT", "Đ1_Điểm CNTT (Final)", "Đ1_Tiếng Anh (Final)", "Đ1_Kỹ năng mềm (Final)"]:
    ks25_cntt[c] = pd.to_numeric(ks25_cntt[c], errors="coerce")
    print(f"  {c}: Mean={ks25_cntt[c].dropna().mean():.1f}, Count={ks25_cntt[c].dropna().shape[0]}")

# Breakdown KS24 by region
print("\n--- KS24 by Region ---")
for reg in ["HN", "HCM"]:
    sub = ks24_cntt[ks24_cntt["Mã lớp hiện tại"].astype(str).str.contains(reg)]
    print(f"{reg}-KS24 ({len(sub)} SV): SP={sub['Đ1_Sản phẩm_CNTT'].mean():.1f}, VD={sub['Đ1_Vấn đáp_CNTT'].mean():.1f}, TH={sub['Đ1_Thực hành_CNTT'].mean():.1f}, KNM={sub['Đ1_Kỹ năng mềm (Final)'].mean():.1f}, TA={sub['Đ1_Tiếng Anh (Final)'].mean():.1f}")

# Breakdown KS25 by region
print("\n--- KS25 by Region ---")
for reg in ["HN", "HCM"]:
    sub = ks25_cntt[ks25_cntt["Mã lớp hiện tại"].astype(str).str.contains(reg)]
    print(f"{reg}-KS25 ({len(sub)} SV): TH={sub['Đ1_Thực hành_CNTT'].mean():.1f}, TN={sub['Đ1_Trắc nghiệm_CNTT'].mean():.1f}, KNM={sub['Đ1_Kỹ năng mềm (Final)'].mean():.1f}, TA={sub['Đ1_Tiếng Anh (Final)'].mean():.1f}")


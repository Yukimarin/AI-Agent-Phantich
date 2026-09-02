import sys
import pandas as pd
import numpy as np
import json

sys.stdout.reconfigure(encoding="utf-8")

excel_path = "inputs/Danh sách thi ĐGNL.xlsx"

df_ds = pd.read_excel(excel_path, sheet_name="Danh sách thi ĐGNL (Lần 1.2026)")
df_cntt = pd.read_excel(excel_path, sheet_name="Danh sách ĐGNL CNTT")
df_nn = pd.read_excel(excel_path, sheet_name="Danh sách ĐGNL ngoại ngữ")
df_knm = pd.read_excel(excel_path, sheet_name="Danh sách ĐGNL Kỹ năng mềm")
df_qtkd = pd.read_excel(excel_path, sheet_name="Danh sách ĐGNL QTKD")

# Clean & Merge on SourceID
cntt_clean = df_cntt[["SourceID", "Họ và tên học viên", "Mã lớp hiện tại", "Cơ sở đào tạo", 
                       "Sản phẩm (Đ1)", "Vấn đáp (Đ1)", "Thực hành (Đ1)", "Trắc nghiệm (Đ1)", 
                       "Điểm final (Đ1)", "Kết quả final ĐGNL (Lần 1)"]].dropna(subset=["SourceID"])

nn_clean = df_nn[["SourceID", "Reading (Đ1)", "Listening (Đ1)", "Điểm final ĐGNL (Lần 1)", "PL Ngoại ngữ hiện tại", "Cấp độ"]].dropna(subset=["SourceID"])
nn_clean.columns = ["SourceID", "NN_Reading", "NN_Listening", "NN_Final", "NN_PL", "NN_CapDo"]

knm_clean = df_knm[["SourceID", "Điểm thi (Đợt 1)", "Điểm final ĐGNL (Lần 1)", "Kết quả final ĐGNL (Lần 1)"]].dropna(subset=["SourceID"])
knm_clean.columns = ["SourceID", "KNM_D1", "KNM_Final", "KNM_KetQua"]

merged = pd.merge(cntt_clean, nn_clean, on="SourceID", how="inner")
merged = pd.merge(merged, knm_clean, on="SourceID", how="inner")

print(f"Total merged students with CNTT + NN + KNM: {len(merged)}")

# Convert columns to numeric
num_cols = ["Sản phẩm (Đ1)", "Vấn đáp (Đ1)", "Thực hành (Đ1)", "Trắc nghiệm (Đ1)", "Điểm final (Đ1)", "NN_Reading", "NN_Listening", "NN_Final", "KNM_Final"]
for c in num_cols:
    merged[c] = pd.to_numeric(merged[c], errors="coerce").fillna(0)

# 1. Analyze KS24 (Has Sản phẩm, Vấn đáp, Thực hành, Trắc nghiệm, NN, KNM)
ks24 = merged[merged["Mã lớp hiện tại"].astype(str).str.contains("KS24", na=False)]
print(f"\n=== KS24 MERGED DATA ({len(ks24)} SV) ===")
print("Correlation Matrix:")
corr = ks24[["Sản phẩm (Đ1)", "Vấn đáp (Đ1)", "Thực hành (Đ1)", "Trắc nghiệm (Đ1)", "NN_Final", "KNM_Final"]].corr()
print(corr.round(2))

# Identify gap between Product vs Oral exam in HN-KS24
hn_ks24 = ks24[ks24["Mã lớp hiện tại"].astype(str).str.contains("HN-KS24", na=False)]
gap_sp_vd = hn_ks24["Sản phẩm (Đ1)"] - hn_ks24["Vấn đáp (Đ1)"]
print("\nHN-KS24 Gap (Sản phẩm - Vấn đáp):")
print(f"Average SP: {hn_ks24['Sản phẩm (Đ1)'].mean():.1f}, Average VD: {hn_ks24['Vấn đáp (Đ1)'].mean():.1f}")
print(f"Number of SV with Product >= 70 but Oral < 50: {len(hn_ks24[(hn_ks24['Sản phẩm (Đ1)'] >= 70) & (hn_ks24['Vấn đáp (Đ1)'] < 50)])}")
print(f"Number of SV with Product >= 60 but Oral < 40: {len(hn_ks24[(hn_ks24['Sản phẩm (Đ1)'] >= 60) & (hn_ks24['Vấn đáp (Đ1)'] < 40)])}")

# Let's list students who have high tech / low interview
high_tech_low_oral = hn_ks24[(hn_ks24['Sản phẩm (Đ1)'] >= 65) & (hn_ks24['Vấn đáp (Đ1)'] <= 40)]
print(f"\nSample Students: High Product (>=65) vs Low Oral (<=40) ({len(high_tech_low_oral)} SV):")
for _, r in high_tech_low_oral.head(10).iterrows():
    print(f"- {r['Họ và tên học viên']} ({r['Mã lớp hiện tại']}): SP={r['Sản phẩm (Đ1)']}, VD={r['Vấn đáp (Đ1)']}, KNM={r['KNM_Final']}, NN={r['NN_Final']}")

# Check KS25
ks25 = merged[merged["Mã lớp hiện tại"].astype(str).str.contains("KS25|K25", na=False)]
print(f"\n=== KS25 MERGED DATA ({len(ks25)} SV) ===")
print(f"Avg Practical: {ks25['Thực hành (Đ1)'].mean():.1f}, Avg MCQ: {ks25['Trắc nghiệm (Đ1)'].mean():.1f}, Avg KNM: {ks25['KNM_Final'].mean():.1f}, Avg NN: {ks25['NN_Final'].mean():.1f}")

# Check QTKD
qtkd_merged = df_qtkd[df_qtkd["Mã lớp hiện tại"].astype(str).str.contains("QTKD", na=False)]
qtkd_merged = pd.merge(qtkd_merged[["SourceID", "Họ và tên học viên", "Mã lớp hiện tại", "Nhóm", "Điểm final ĐGNL (Lần 1)", "Kết quả final ĐGNL (Lần 1)"]],
                       nn_clean, on="SourceID", how="left")
qtkd_merged = pd.merge(qtkd_merged, knm_clean, on="SourceID", how="left")
print(f"\n=== QTKD MERGED DATA ({len(qtkd_merged)} SV) ===")
print("QTKD Avg Score:", qtkd_merged["Điểm final ĐGNL (Lần 1)"].astype(float).mean())
print("QTKD Avg NN:", pd.to_numeric(qtkd_merged["NN_Final"], errors="coerce").mean())
print("QTKD Avg KNM:", pd.to_numeric(qtkd_merged["KNM_Final"], errors="coerce").mean())


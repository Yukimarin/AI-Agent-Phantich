import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

excel_path = "inputs/Danh sách thi ĐGNL.xlsx"
df_bd = pd.read_excel(excel_path, sheet_name="Bảng điểm (Đợt 1)")

ks24 = df_bd[df_bd["Mã lớp hiện tại"].astype(str).str.contains("KS24-CNTT", na=False)].copy()
ks25 = df_bd[df_bd["Mã lớp hiện tại"].astype(str).str.contains("KS25-CNTT", na=False)].copy()

for c in ["Đ1_Sản phẩm_CNTT", "Đ1_Vấn đáp_CNTT", "Đ1_Thực hành_CNTT", "Đ1_Trắc nghiệm_CNTT", "Đ1_Điểm CNTT (Final)", "Đ1_Tiếng Anh (Final)", "Đ1_Kỹ năng mềm (Final)"]:
    ks24[c] = pd.to_numeric(ks24[c], errors="coerce")

for c in ["Đ1_Thực hành_CNTT", "Đ1_Trắc nghiệm_CNTT", "Đ1_Điểm CNTT (Final)", "Đ1_Tiếng Anh (Final)", "Đ1_Kỹ năng mềm (Final)"]:
    ks25[c] = pd.to_numeric(ks25[c], errors="coerce")

# KS24 Diagnostic Quadrants:
# Active students who took at least one exam
ks24_active = ks24[(ks24["Đ1_Thực hành_CNTT"].notna()) | (ks24["Đ1_Vấn đáp_CNTT"].notna()) | (ks24["Đ1_Sản phẩm_CNTT"].notna())].copy()

# Tech Foundation score = max(Thực hành, Sản phẩm)
ks24_active["Tech_Score"] = ks24_active[["Đ1_Thực hành_CNTT", "Đ1_Sản phẩm_CNTT"]].max(axis=1).fillna(0)
ks24_active["Oral_Score"] = ks24_active["Đ1_Vấn đáp_CNTT"].fillna(0)
ks24_active["Soft_Score"] = ks24_active["Đ1_Kỹ năng mềm (Final)"].fillna(0)
ks24_active["Eng_Score"] = ks24_active["Đ1_Tiếng Anh (Final)"].fillna(0)

# Quadrant 1: Silent Coders (Tech >= 65, Oral < 50)
q1_silent = ks24_active[(ks24_active["Tech_Score"] >= 65) & (ks24_active["Oral_Score"] < 50)]
# Quadrant 2: Smooth Talkers / Career Shifters (Tech < 50, (Oral >= 50 or Soft >= 75))
q2_smooth = ks24_active[(ks24_active["Tech_Score"] < 50) & ((ks24_active["Oral_Score"] >= 50) | (ks24_active["Soft_Score"] >= 75))]
# Quadrant 3: All-Rounders / Corporate Ready (Tech >= 65, Oral >= 50, Soft >= 70)
q3_allround = ks24_active[(ks24_active["Tech_Score"] >= 65) & (ks24_active["Oral_Score"] >= 50)]
# Quadrant 4: At-Risk / Weak Foundation (Tech < 50, Oral < 50, Soft < 70)
q4_atrisk = ks24_active[(ks24_active["Tech_Score"] < 50) & (ks24_active["Oral_Score"] < 50) & (ks24_active["Soft_Score"] < 70)]

print(f"=== KS24 DIAGNOSTIC QUADRANTS (Total Active: {len(ks24_active)} SV) ===")
print(f"1. Silent Coders (Kỹ thuật vững, Vấn đáp yếu): {len(q1_silent)} SV ({len(q1_silent)/len(ks24_active)*100:.1f}%)")
print(f"2. Smooth Talkers / BA-QA Fit (Giao tiếp tốt, Kỹ thuật yếu): {len(q2_smooth)} SV ({len(q2_smooth)/len(ks24_active)*100:.1f}%)")
print(f"3. All-Rounders (Toàn diện vững cả hai): {len(q3_allround)} SV ({len(q3_allround)/len(ks24_active)*100:.1f}%)")
print(f"4. At-Risk (Yếu cả nền tảng lẫn vấn đáp): {len(q4_atrisk)} SV ({len(q4_atrisk)/len(ks24_active)*100:.1f}%)")
other_ks24 = len(ks24_active) - (len(q1_silent) + len(q2_smooth) + len(q3_allround) + len(q4_atrisk))
print(f"5. Nhóm trung gian (Moderate Tech 50-64): {other_ks24} SV")

# KS25 Diagnostic
ks25_active = ks25[ks25["Đ1_Thực hành_CNTT"].notna() | ks25["Đ1_Trắc nghiệm_CNTT"].notna()].copy()
ks25_active["Tech_Score"] = ks25_active["Đ1_Thực hành_CNTT"].fillna(0)
ks25_active["MCQ_Score"] = ks25_active["Đ1_Trắc nghiệm_CNTT"].fillna(0)
ks25_active["Soft_Score"] = ks25_active["Đ1_Kỹ năng mềm (Final)"].fillna(0)

# KS25 Groups:
# G1: Solid Practical Code (Tech >= 50)
ks25_g1 = ks25_active[ks25_active["Tech_Score"] >= 50]
# G2: High Theory / Low Practical (MCQ >= 65, Tech < 50) -> Rote Learning
ks25_g2 = ks25_active[(ks25_active["MCQ_Score"] >= 65) & (ks25_active["Tech_Score"] < 50)]
# G3: High Soft / Low Tech (Soft >= 75, Tech < 50)
ks25_g3 = ks25_active[(ks25_active["Soft_Score"] >= 75) & (ks25_active["Tech_Score"] < 50)]
# G4: Double Weak (MCQ < 50, Tech < 50)
ks25_g4 = ks25_active[(ks25_active["MCQ_Score"] < 50) & (ks25_active["Tech_Score"] < 50)]

print(f"\n=== KS25 DIAGNOSTIC GROUPS (Total Active: {len(ks25_active)} SV) ===")
print(f"1. Vững Thực hành Code (TH >= 50): {len(ks25_g1)} SV ({len(ks25_g1)/len(ks25_active)*100:.1f}%)")
print(f"2. Ảo tưởng lý thuyết (Trắc nghiệm giỏi >=65, nhưng Thực hành liệt <50): {len(ks25_g2)} SV ({len(ks25_g2)/len(ks25_active)*100:.1f}%)")
print(f"3. Kỹ năng mềm tốt nhưng Code yếu (KNM >=75, TH <50): {len(ks25_g3)} SV ({len(ks25_g3)/len(ks25_active)*100:.1f}%)")
print(f"4. Yếu cả Lý thuyết lẫn Thực hành (TN <50, TH <50): {len(ks25_g4)} SV ({len(ks25_g4)/len(ks25_active)*100:.1f}%)")


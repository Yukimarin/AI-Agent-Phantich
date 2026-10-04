import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

excel_path = "inputs/Danh sách thi ĐGNL.xlsx"
df_bd = pd.read_excel(excel_path, sheet_name="Bảng điểm (Đợt 1)")

# Clean class name
df_bd["Class"] = df_bd["Mã lớp hiện tại"].astype(str).str.strip()

# 1. KS24 Analysis (Java / Spring Boot)
ks24 = df_bd[df_bd["Class"].str.contains("KS24", na=False)].copy()
print(f"=== KHÓA KS24 TỔNG THỂ ({len(ks24)} SV) ===")

ks24_cols = ["Đ1_Sản phẩm_CNTT", "Đ1_Vấn đáp_CNTT", "Đ1_Thực hành_CNTT", "Đ1_Trắc nghiệm_CNTT", "Đ1_Điểm CNTT (Final)", "Đ1_Tiếng Anh (Final)", "Đ1_Kỹ năng mềm (Final)"]
for c in ks24_cols:
    ks24[c] = pd.to_numeric(ks24[c], errors="coerce")

print("Correlation Matrix KS24:")
print(ks24[ks24_cols].corr().round(2))

# 2. Analyze Gaps in KS24
# Group A: "Code/Sản phẩm tốt nhưng Vấn đáp/Phỏng vấn kém"
# SP >= 65 hoặc TH >= 65 nhưng VD <= 45
sp_th_high = (ks24["Đ1_Sản phẩm_CNTT"] >= 65) | (ks24["Đ1_Thực hành_CNTT"] >= 65)
vd_low = ks24["Đ1_Vấn đáp_CNTT"] <= 45
gap_tech_vd = ks24[sp_th_high & vd_low]
print(f"\n[!] Nhóm 1: 'Kỹ thuật/Sản phẩm tốt nhưng Vấn đáp/Phỏng vấn yếu' (SP/TH >= 65 & VD <= 45): {len(gap_tech_vd)} SV")
for _, r in gap_tech_vd.iterrows():
    print(f"   - {r['Họ và tên học viên']} ({r['Class']}): SP={r['Đ1_Sản phẩm_CNTT']}, TH={r['Đ1_Thực hành_CNTT']}, VD={r['Đ1_Vấn đáp_CNTT']}, KNM={r['Đ1_Kỹ năng mềm (Final)']}, TA={r['Đ1_Tiếng Anh (Final)']}")

# Group B: "KNM/Giao tiếp cao nhưng Kỹ thuật/Code yếu"
# KNM >= 80 & (TH < 50 & SP < 50)
knm_high = ks24["Đ1_Kỹ năng mềm (Final)"] >= 80
tech_low = (ks24["Đ1_Thực hành_CNTT"] < 50) & (ks24["Đ1_Sản phẩm_CNTT"].fillna(0) < 50) & (ks24["Đ1_Thực hành_CNTT"].notna())
high_soft_low_tech = ks24[knm_high & tech_low]
print(f"\n[!] Nhóm 2: 'Kỹ năng mềm cao nhưng Kỹ thuật/Code yếu' (KNM >= 80 & TH, SP < 50): {len(high_soft_low_tech)} SV")
for _, r in high_soft_low_tech.head(10).iterrows():
    print(f"   - {r['Họ và tên học viên']} ({r['Class']}): KNM={r['Đ1_Kỹ năng mềm (Final)']}, TH={r['Đ1_Thực hành_CNTT']}, SP={r['Đ1_Sản phẩm_CNTT']}, VD={r['Đ1_Vấn đáp_CNTT']}, TA={r['Đ1_Tiếng Anh (Final)']}")

# Group C: "Toàn diện / Global Ready"
# CNTT Final >= 70, KNM >= 80, TA >= 450
all_rounder = ks24[(ks24["Đ1_Điểm CNTT (Final)"] >= 65) & (ks24["Đ1_Kỹ năng mềm (Final)"] >= 75) & (ks24["Đ1_Tiếng Anh (Final)"] >= 400)]
print(f"\n[+] Nhóm 3: 'Sinh viên Toàn diện / Sẵn sàng Doanh nghiệp Quốc tế' (CNTT >= 65, KNM >= 75, TA >= 400): {len(all_rounder)} SV")
for _, r in all_rounder.iterrows():
    print(f"   - {r['Họ và tên học viên']} ({r['Class']}): CNTT={r['Đ1_Điểm CNTT (Final)']}, KNM={r['Đ1_Kỹ năng mềm (Final)']}, TA={r['Đ1_Tiếng Anh (Final)']}")

# 3. Analyze QTKD
qtkd = df_bd[df_bd["Class"].str.contains("QTKD", na=False)].copy()
qtkd_cols = ["Đ1_Điểm QTKD (Final)", "Đ1_Tiếng Anh (Final)", "Đ1_Kỹ năng mềm (Final)"]
for c in qtkd_cols:
    qtkd[c] = pd.to_numeric(qtkd[c], errors="coerce")

print(f"\n=== KHỐI QTKD ({len(qtkd)} SV) ===")
print("QTKD Summary stats:")
print(qtkd[qtkd_cols].describe().round(2))

# QTKD Gaps:
# Điểm QTKD cao (>= 70) nhưng Tiếng Anh yếu (< 350)
qtkd_high_eng_low = qtkd[(qtkd["Đ1_Điểm QTKD (Final)"] >= 70) & (qtkd["Đ1_Tiếng Anh (Final)"] < 350) & (qtkd["Đ1_Tiếng Anh (Final)"].notna())]
print(f"\nQTKD: Điểm Chuyên môn cao (>=70) nhưng Tiếng Anh yếu (<350): {len(qtkd_high_eng_low)} SV")

# QTKD: Toàn diện
qtkd_all_rounder = qtkd[(qtkd["Đ1_Điểm QTKD (Final)"] >= 70) & (qtkd["Đ1_Kỹ năng mềm (Final)"] >= 75) & (qtkd["Đ1_Tiếng Anh (Final)"] >= 400)]
print(f"QTKD: Toàn diện (QTKD >= 70, KNM >= 75, TA >= 400): {len(qtkd_all_rounder)} SV")


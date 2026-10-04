import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

excel_path = "inputs/Danh sách thi ĐGNL.xlsx"
df_qtkd = pd.read_excel(excel_path, sheet_name="Danh sách ĐGNL QTKD")

# Filter students whose class is QTKD
qtkd_students = df_qtkd[df_qtkd["Mã lớp hiện tại"].astype(str).str.contains("QTKD", na=False)]
print(f"Total QTKD students in sheet: {len(qtkd_students)}")
print(qtkd_students["Mã lớp hiện tại"].value_counts())

print("\nQTKD Score summary:")
print(qtkd_students[["Điểm thi (Đợt 1)", "Điểm thi (Đợt 2)", "Điểm final ĐGNL (Lần 1)"]].describe())

print("\nQTKD Result value counts:")
print(qtkd_students["Kết quả final ĐGNL (Lần 1)"].value_counts(dropna=False))

print("\nQTKD Groups (Nhóm):")
print(qtkd_students["Nhóm"].value_counts(dropna=False))

# Look at students in other classes in the QTKD sheet
non_qtkd = df_qtkd[~df_qtkd["Mã lớp hiện tại"].astype(str).str.contains("QTKD", na=False)]
print(f"\nNon-QTKD rows in QTKD sheet: {len(non_qtkd)}")
print("Sample non-QTKD rows with non-null score:")
print(non_qtkd[non_qtkd["Điểm final ĐGNL (Lần 1)"].notna()][["Họ và tên học viên", "Mã lớp hiện tại", "Điểm final ĐGNL (Lần 1)"]])


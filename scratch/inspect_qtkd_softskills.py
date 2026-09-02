import sys
import pandas as pd
import openpyxl
import json

sys.stdout.reconfigure(encoding="utf-8")

excel_path = "inputs/Danh sách thi ĐGNL.xlsx"
xl = pd.ExcelFile(excel_path)
print("Available sheets:", xl.sheet_names)

# Inspect QTKD
df_qtkd = pd.read_excel(excel_path, sheet_name="Danh sách ĐGNL QTKD")
print("\n=== QTKD SHEET COLUMNS & STATS ===")
print("Columns:", list(df_qtkd.columns))
print("Shape:", df_qtkd.shape)
print("Classes in QTKD:", df_qtkd["Mã lớp hiện tại"].dropna().unique())
print("Score columns in QTKD:")
for c in ["Điểm thi (Đợt 1)", "Điểm thi (Đợt 2)", "Điểm final ĐGNL (Lần 1)", "Kết quả final ĐGNL (Lần 1)", "Thi lại", "Nhóm"]:
    if c in df_qtkd.columns:
        print(f"  {c}: non-null={df_qtkd[c].dropna().shape[0]}, sample vals={df_qtkd[c].dropna().head(5).tolist()}")

# Inspect Ngoại ngữ
df_nn = pd.read_excel(excel_path, sheet_name="Danh sách ĐGNL ngoại ngữ")
print("\n=== NGOẠI NGỮ SHEET COLUMNS & STATS ===")
print("Columns:", list(df_nn.columns))
print("Score columns in NN:")
for c in ["Reading (Đ1)", "Listening (Đ1)", "Điểm final (Đ1)", "Điểm final (Đ2)", "Điểm final ĐGNL (Lần 1)", "Kết quả final ĐGNL (Lần 1)", "PL Ngoại ngữ hiện tại", "Cấp độ"]:
    if c in df_nn.columns:
        print(f"  {c}: non-null={df_nn[c].dropna().shape[0]}, sample vals={df_nn[c].dropna().head(5).tolist()}")

# Inspect Kỹ năng mềm
df_knm = pd.read_excel(excel_path, sheet_name="Danh sách ĐGNL Kỹ năng mềm")
print("\n=== KỸ NĂNG MỀM SHEET COLUMNS & STATS ===")
print("Columns:", list(df_knm.columns))
print("Score columns in KNM:")
for c in ["Điểm thi (Đợt 1)", "Điểm thi (Đợt 2)", "Điểm final ĐGNL (Lần 1)", "Kết quả final ĐGNL (Lần 1)", "Thi lại"]:
    if c in df_knm.columns:
        print(f"  {c}: non-null={df_knm[c].dropna().shape[0]}, sample vals={df_knm[c].dropna().head(5).tolist()}")


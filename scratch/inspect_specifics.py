import sys
import pandas as pd
import json

sys.stdout.reconfigure(encoding="utf-8")

f1 = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"
f2 = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx"

# 1. Check deleted students in Danh sách thi ĐGNL (Lần 1.2026)
df1_ds = pd.read_excel(f1, sheet_name="Danh sách thi ĐGNL (Lần 1.2026)")
df2_ds = pd.read_excel(f2, sheet_name="Danh sách thi ĐGNL (Lần 1.2026)")
del_ds = df1_ds[~df1_ds["SourceID"].isin(df2_ds["SourceID"])]
print("=== 3 SV BỊ XÓA KHỎI SHEET TỔNG ===")
for _, r in del_ds.iterrows():
    print(f"- {r['Họ và tên học viên']} | Lớp: {r['Mã lớp hiện tại']} | Email: {r.get('Email học viên')} | MSSV: {r.get('Khóa (Theo MSSV)')} | SourceID: {r['SourceID']}")

# 2. Check added rows in each subject sheet
for sname in ["Danh sách ĐGNL CNTT", "Danh sách ĐGNL QTKD", "Danh sách ĐGNL Kỹ năng mềm", "Thi bổ sung Đợt 1"]:
    df1 = pd.read_excel(f1, sheet_name=sname)
    df2 = pd.read_excel(f2, sheet_name=sname)
    id_col = "SourceID" if "SourceID" in df1.columns else "Họ tên"
    if id_col == "SourceID":
        added = df2[~df2[id_col].isin(df1[id_col])]
    else:
        added = df2.iloc[len(df1):]
    print(f"\n=== CÁC DÒNG MỚI THÊM VÀO SHEET: {sname} ({len(added)} dòng) ===")
    for _, r in added.iterrows():
        name = r.get("Họ và tên học viên") or r.get("Họ tên") or r.get("Tên")
        lop = r.get("Mã lớp hiện tại") or r.get("Mã lớp")
        email = r.get("Email học viên", "")
        print(f"- {name} | Lớp: {lop} | Email: {email}")

# 3. Check Lịch thi_ĐGNL additions
df1_lt = pd.read_excel(f1, sheet_name="Lịch thi_ĐGNL")
df2_lt = pd.read_excel(f2, sheet_name="Lịch thi_ĐGNL")
print(f"\n=== DÒNG MỚI TRONG LỊCH THI ===")
for _, r in df2_lt.iloc[len(df1_lt):].iterrows():
    print(f"- Môn: {r['Môn thi']} | HĐ: {r['Hội đồng']} | Ngày: {r['Ngày thi']} | Ca: {r['Ca thi']} | Phòng: {r['Phòng thi']} | Cơ sở: {r['Cơ sở thi']} | Số lượng SV: {r['Số lượng SV']}")


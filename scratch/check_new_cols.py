import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

f2 = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx"

for sname in ["Danh sách ĐGNL CNTT", "Danh sách ĐGNL QTKD", "Danh sách ĐGNL ngoại ngữ", "Danh sách ĐGNL Kỹ năng mềm"]:
    df2 = pd.read_excel(f2, sheet_name=sname)
    print(f"\n============================\nSHEET: {sname}\n============================")
    for col in ["HĐ thi BS L1", "HĐ thi BS", "Điểm danh BS", "Điểm danh thi BS", "Ghi chú L1", "TT đăng ký BS", "TT đăng kí BS", "TT đăng ký L1"]:
        if col in df2.columns:
            val_counts = df2[col].dropna().value_counts()
            print(f"Cột [{col}] (Tổng có giá trị: {len(df2[col].dropna())}):")
            print(val_counts.head(10))


import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

f1 = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"
f2 = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx"

print("=== SO SÁNH KẾT QUẢ ĐẠT / KHÔNG ĐẠT GIỮA 2 FILE ===")
for sname, res_col in [("Danh sách ĐGNL CNTT", "Kết quả final ĐGNL (Lần 1)"), 
                       ("Danh sách ĐGNL QTKD", "Kết quả final ĐGNL (Lần 1)"), 
                       ("Danh sách ĐGNL Kỹ năng mềm", "Kết quả final ĐGNL (Lần 1)")]:
    df1 = pd.read_excel(f1, sheet_name=sname)
    df2 = pd.read_excel(f2, sheet_name=sname)
    print(f"\n--- {sname} ---")
    c1 = df1[res_col].value_counts(dropna=False).to_dict()
    c2 = df2[res_col].value_counts(dropna=False).to_dict()
    print("File cũ:", c1)
    print("File mới:", c2)


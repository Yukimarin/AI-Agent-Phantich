import sys
import os
import openpyxl

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\Users\DELL\Downloads\[RE] Đào tạo - Tiêu chuẩn xếp loại năng lực GV_TG (2).xlsx"

wb = openpyxl.load_workbook(path, data_only=False) # Load with formulas to see math
sheet = wb['Lương Quốc Tuấn - DEMO']
print(f"=== Sheet: Lương Quốc Tuấn - DEMO ===")
for r_idx in range(1, 40):
    row_vals = [sheet.cell(row=r_idx, column=c_idx).value for c_idx in range(1, 12)]
    # Check if there is content in this row
    val_strs = [str(x) if x is not None else "" for x in row_vals]
    if any(val_strs):
        print(f"Row {r_idx}: {val_strs}")
wb.close()

import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"

if os.path.exists(file_path):
    wb = openpyxl.load_workbook(file_path, read_only=True)
    sheet = wb["Danh sách ĐGNL CNTT"]
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    
    # Print headers and values side by side for row 431 (index 430 because rows is 0-indexed)
    target_row = rows[430]
    
    print(f"{'Header':<30} | {'Value'}")
    print("-" * 50)
    for col_idx, (header, val) in enumerate(zip(headers, target_row)):
        print(f"[{col_idx}] {header:<25} | {val}")
else:
    print("Excel file not found.")

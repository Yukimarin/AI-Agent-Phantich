import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"

print("Checking file path existence:", os.path.exists(file_path))
if os.path.exists(file_path):
    print("File size:", os.path.getsize(file_path), "bytes")
    wb = openpyxl.load_workbook(file_path, read_only=True)
    print("Sheets in workbook:", wb.sheetnames)
    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        # Count rows
        row_count = 0
        for _ in sheet.iter_rows(values_only=True):
            row_count += 1
            
        print(f"\nSheet: {sheet_name}")
        print(f"  Total rows: {row_count}")
        
        # Get first row for headers
        for r in sheet.iter_rows(max_row=1, values_only=True):
            print(f"  Headers: {r}")
            break
else:
    print("File not found at specified path.")


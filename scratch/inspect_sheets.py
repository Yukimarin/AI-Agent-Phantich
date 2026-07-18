import sys
import os
import openpyxl

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

files = {
    "old": r"C:\Users\DELL\Downloads\[RE] Đào tạo - Tiêu chuẩn xếp loại năng lực GV_TG.xlsx",
    "v1": r"C:\Users\DELL\Downloads\[RE] Đào tạo - Tiêu chuẩn xếp loại năng lực GV_TG (1).xlsx",
    "v2": r"C:\Users\DELL\Downloads\[RE] Đào tạo - Tiêu chuẩn xếp loại năng lực GV_TG (2).xlsx"
}

for name, path in files.items():
    print(f"=== File: {name} ===")
    if not os.path.exists(path):
        print("Does not exist!")
        continue
    wb = openpyxl.load_workbook(path, read_only=True)
    print(f"Sheet names: {wb.sheetnames}")
    wb.close()

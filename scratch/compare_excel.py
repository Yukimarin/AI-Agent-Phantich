import sys
import openpyxl
import pandas as pd
import json

# Ensure stdout handles utf-8
sys.stdout.reconfigure(encoding='utf-8')

f1 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx'
f2 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx'

print(f"--- THÔNG TIN FILE ---")
print(f"File cũ (f1): {f1}")
print(f"File mới (f2): {f2}")

wb1 = openpyxl.load_workbook(f1, data_only=True)
wb2 = openpyxl.load_workbook(f2, data_only=True)

print("\n--- DANH SÁCH SHEET ---")
print(f"File cũ sheets ({len(wb1.sheetnames)}): {wb1.sheetnames}")
print(f"File mới sheets ({len(wb2.sheetnames)}): {wb2.sheetnames}")

# Compare sheet by sheet
sheets_f1 = set(wb1.sheetnames)
sheets_f2 = set(wb2.sheetnames)

added_sheets = sheets_f2 - sheets_f1
removed_sheets = sheets_f1 - sheets_f2
common_sheets = [s for s in wb1.sheetnames if s in sheets_f2]

if added_sheets:
    print(f"\n[+] Sheet mới xuất hiện trong file mới: {added_sheets}")
if removed_sheets:
    print(f"\n[-] Sheet bị xóa/thiếu trong file mới: {removed_sheets}")

for sheet_name in wb2.sheetnames:
    print(f"\n==========================================")
    print(f"PHÂN TÍCH SHEET: '{sheet_name}'")
    print(f"==========================================")
    
    ws2 = wb2[sheet_name]
    max_r2, max_c2 = ws2.max_row, ws2.max_column
    print(f"File mới -> Kích thước: {max_r2} dòng x {max_c2} cột")
    
    if sheet_name in wb1.sheetnames:
        ws1 = wb1[sheet_name]
        max_r1, max_c1 = ws1.max_row, ws1.max_column
        print(f"File cũ  -> Kích thước: {max_r1} dòng x {max_c1} cột")
    else:
        print(f"Sheet này không có trong file cũ!")
        continue

    # Load into pandas for deep diffing
    try:
        df1 = pd.read_excel(f1, sheet_name=sheet_name)
        df2 = pd.read_excel(f2, sheet_name=sheet_name)
        
        print(f"\nCấu trúc Dataframe:")
        print(f"File cũ shape: {df1.shape}, Cột: {list(df1.columns)}")
        print(f"File mới shape: {df2.shape}, Cột: {list(df2.columns)}")
        
        # Check column differences
        col_diff_add = set(df2.columns) - set(df1.columns)
        col_diff_del = set(df1.columns) - set(df2.columns)
        if col_diff_add:
            print(f"[+] Cột mới thêm: {col_diff_add}")
        if col_diff_del:
            print(f"[-] Cột bị bỏ: {col_diff_del}")
            
        # Let's inspect rows count
        print(f"Số dòng file cũ: {len(df1)}, số dòng file mới: {len(df2)} (Chênh lệch: {len(df2) - len(df1):+d})")
        
    except Exception as e:
        print(f"Lỗi đọc pandas cho sheet {sheet_name}: {e}")


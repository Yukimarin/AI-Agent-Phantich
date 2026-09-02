import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"

if os.path.exists(file_path):
    # Do not use data_only=True so we can see the formula strings
    wb = openpyxl.load_workbook(file_path, data_only=False)
    sheet = wb["Danh sách ĐGNL CNTT"]
    
    # Let's find columns
    headers = [cell.value for cell in sheet[1]]
    class_idx = headers.index('Mã lớp hiện tại') + 1
    name_idx = headers.index('Họ và tên học viên') + 1
    final_idx = headers.index('Điểm final (Đ1)') + 1
    
    print("Headers:", headers)
    
    print("\nHN-KS24 Student Formulas:")
    hn_count = 0
    for row_idx in range(2, sheet.max_row + 1):
        class_val = sheet.cell(row=row_idx, column=class_idx).value
        if class_val and "HN-KS24" in str(class_val):
            name_val = sheet.cell(row=row_idx, column=name_idx).value
            final_formula = sheet.cell(row=row_idx, column=final_idx).value
            print(f"Row {row_idx} | Name: {name_val} | Class: {class_val} | Formula: {final_formula}")
            hn_count += 1
            if hn_count >= 5:
                break
                
    print("\nHCM-KS24 Student Formulas:")
    hcm_count = 0
    for row_idx in range(2, sheet.max_row + 1):
        class_val = sheet.cell(row=row_idx, column=class_idx).value
        if class_val and "HCM-KS24" in str(class_val):
            name_val = sheet.cell(row=row_idx, column=name_idx).value
            final_formula = sheet.cell(row=row_idx, column=final_idx).value
            print(f"Row {row_idx} | Name: {name_val} | Class: {class_val} | Formula: {final_formula}")
            hcm_count += 1
            if hcm_count >= 5:
                break
else:
    print("Excel file not found.")

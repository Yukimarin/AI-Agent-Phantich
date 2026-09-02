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
    
    class_idx = headers.index('Mã lớp hiện tại')
    name_idx = headers.index('Họ và tên học viên')
    sp_idx = headers.index('Sản phẩm (Đ1)')
    vd_idx = headers.index('Vấn đáp (Đ1)')
    th_idx = headers.index('Thực hành (Đ1)')
    tn_idx = headers.index('Trắc nghiệm (Đ1)')
    final_idx = headers.index('Điểm final (Đ1)')
    dgnl_idx = headers.index('Điểm final ĐGNL (Lần 1)')
    note_idx = headers.index('Ghi chú')
    bb_idx = headers.index('Biên bản')
    
    print("HN-KS24 Sample:")
    hn_count = 0
    for r in rows[1:]:
        if r[class_idx] and "HN-KS24" in str(r[class_idx]):
            print(f"Name: {r[name_idx]} | Class: {r[class_idx]} | Prod: {r[sp_idx]} | Oral: {r[vd_idx]} | Prac: {r[th_idx]} | MCQ: {r[tn_idx]} | Final: {r[final_idx]} | DGNL: {r[dgnl_idx]}")
            hn_count += 1
            if hn_count >= 5:
                break
                
    print("\nHCM-KS24 Sample:")
    hcm_count = 0
    for r in rows[1:]:
        if r[class_idx] and "HCM-KS24" in str(r[class_idx]):
            print(f"Name: {r[name_idx]} | Class: {r[class_idx]} | Prod: {r[sp_idx]} | Oral: {r[vd_idx]} | Prac: {r[th_idx]} | MCQ: {r[tn_idx]} | Final: {r[final_idx]} | DGNL: {r[dgnl_idx]}")
            hcm_count += 1
            if hcm_count >= 5:
                break
                
else:
    print("Excel file not found.")

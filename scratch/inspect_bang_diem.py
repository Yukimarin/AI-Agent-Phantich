import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"

if os.path.exists(file_path):
    wb = openpyxl.load_workbook(file_path, read_only=True)
    sheet = wb["Bảng điểm (Đợt 1)"]
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    
    class_idx = headers.index('Mã lớp hiện tại')
    name_idx = headers.index('Họ và tên học viên')
    sp_idx = headers.index('Đ1_Sản phẩm_CNTT')
    vd_idx = headers.index('Đ1_Vấn đáp_CNTT')
    th_idx = headers.index('Đ1_Thực hành_CNTT')
    tn_idx = headers.index('Đ1_Trắc nghiệm_CNTT')
    final_cntt = headers.index('Đ1_Điểm CNTT (Final)')
    
    print("HN-KS24 Bảng điểm (Đợt 1) Sample:")
    hn_count = 0
    for r in rows[1:]:
        cname = r[class_idx]
        if cname and "HN-KS24" in str(cname):
            print(f"Name: {r[name_idx]} | Class: {cname} | Prod: {r[sp_idx]} | Oral: {r[vd_idx]} | Prac: {r[th_idx]} | MCQ: {r[tn_idx]} | Final CNTT: {r[final_cntt]}")
            hn_count += 1
            if hn_count >= 5:
                break
                
    print("\nHCM-KS24 Bảng điểm (Đợt 1) Sample:")
    hcm_count = 0
    for r in rows[1:]:
        cname = r[class_idx]
        if cname and "HCM-KS24" in str(cname):
            print(f"Name: {r[name_idx]} | Class: {cname} | Prod: {r[sp_idx]} | Oral: {r[vd_idx]} | Prac: {r[th_idx]} | MCQ: {r[tn_idx]} | Final CNTT: {r[final_cntt]}")
            hcm_count += 1
            if hcm_count >= 5:
                break
else:
    print("Excel file not found.")

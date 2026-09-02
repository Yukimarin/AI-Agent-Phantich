import openpyxl
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"

if os.path.exists(file_path):
    wb = openpyxl.load_workbook(file_path, read_only=True)
    sheet = wb["Danh sách ĐGNL CNTT"]
    
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    
    class_idx = headers.index('Mã lớp hiện tại')
    sp_idx = headers.index('Sản phẩm (Đ1)')
    vd_idx = headers.index('Vấn đáp (Đ1)')
    th_idx = headers.index('Thực hành (Đ1)')
    tn_idx = headers.index('Trắc nghiệm (Đ1)')
    final_idx = headers.index('Điểm final (Đ1)')
    dgnl_idx = headers.index('Điểm final ĐGNL (Lần 1)')
    branch_idx = headers.index('Cơ sở đào tạo')
    
    classes_info = {}
    
    for r in rows[1:]:
        if r[0] is None or r[class_idx] is None:
            continue
            
        class_name = str(r[class_idx]).strip()
        branch = str(r[branch_idx]).strip() if r[branch_idx] is not None else "Unknown"
        
        sp = r[sp_idx]
        vd = r[vd_idx]
        th = r[th_idx]
        tn = r[tn_idx]
        final = r[final_idx]
        dgnl = r[dgnl_idx]
        
        if class_name not in classes_info:
            classes_info[class_name] = {
                'branch': branch,
                'total': 0,
                'has_sp': 0,
                'has_vd': 0,
                'has_th': 0,
                'has_tn': 0,
                'has_final': 0,
                'has_dgnl': 0
            }
            
        info = classes_info[class_name]
        info['total'] += 1
        if sp is not None and str(sp).strip() != "" and sp != 0: info['has_sp'] += 1
        if vd is not None and str(vd).strip() != "" and vd != 0: info['has_vd'] += 1
        if th is not None and str(th).strip() != "" and th != 0: info['has_th'] += 1
        if tn is not None and str(tn).strip() != "" and tn != 0: info['has_tn'] += 1
        if final is not None and str(final).strip() != "" and final != 0: info['has_final'] += 1
        if dgnl is not None and str(dgnl).strip() != "" and dgnl != 0: info['has_dgnl'] += 1
        
    print(f"{'Class Code':<20} | {'Branch':<15} | {'Total':<6} | {'Prod':<6} | {'Oral':<6} | {'Prac':<6} | {'MCQ':<6} | {'Final':<6} | {'DGNL':<6}")
    print("-" * 85)
    for cname, info in sorted(classes_info.items()):
        print(f"{cname:<20} | {info['branch']:<15} | {info['total']:<6} | {info['has_sp']:<6} | {info['has_vd']:<6} | {info['has_th']:<6} | {info['has_tn']:<6} | {info['has_final']:<6} | {info['has_dgnl']:<6}")
        
else:
    print("Excel file not found.")

import openpyxl
import os
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"

def solve_weights(X, y):
    # Solve X * w = y using least squares
    w, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
    return w

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
    
    hn_data = []
    hcm_data = []
    
    for r in rows[1:]:
        cname = r[class_idx]
        if not cname: continue
        
        sp = r[sp_idx]
        vd = r[vd_idx]
        th = r[th_idx]
        tn = r[tn_idx]
        final = r[final_idx]
        
        if final is None or final == 0:
            continue
            
        if "HN-KS24" in str(cname):
            if sp is not None and vd is not None and th is not None and tn is not None:
                hn_data.append([float(sp), float(vd), float(th), float(tn), float(final)])
        elif "HCM-KS24" in str(cname):
            # HCM has no Prod (sp)
            if vd is not None and th is not None and tn is not None:
                hn_sp = float(sp) if sp is not None else 0.0
                hcm_data.append([hn_sp, float(vd), float(th), float(tn), float(final)])
                
    print(f"HN data rows: {len(hn_data)}")
    if len(hn_data) >= 4:
        # Solve for HN
        # final = w_sp * sp + w_vd * vd + w_th * th + w_tn * tn
        X = np.array([row[:4] for row in hn_data])
        y = np.array([row[4] for row in hn_data])
        w = solve_weights(X, y)
        print("HN Weights (Prod, Oral, Prac, MCQ):", [round(val, 3) for val in w])
        
    print(f"HCM data rows: {len(hcm_data)}")
    if len(hcm_data) >= 3:
        # Solve for HCM
        # Since sp is 0/None, we check (Oral, Prac, MCQ)
        X = np.array([row[1:4] for row in hcm_data])
        y = np.array([row[4] for row in hcm_data])
        w = solve_weights(X, y)
        print("HCM Weights (Oral, Prac, MCQ):", [round(val, 3) for val in w])
else:
    print("Excel file not found.")

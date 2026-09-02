import openpyxl
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

main_file = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"
ca_files = [
    "inputs/ket-qua-cham-DGNL-ca-thi-7-9.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-12-14.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-14-16.xlsx"
]

def load_previous_scores():
    prev_scores = {}
    for path in ca_files:
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue
        wb = openpyxl.load_workbook(path, data_only=True)
        sheet = wb.active
        rows = list(sheet.iter_rows(values_only=True))
        headers = rows[0]
        
        name_idx = headers.index('Name')
        score_idx = headers.index('Điểm')
        
        ca_name = os.path.basename(path).replace("ket-qua-cham-DGNL-ca-thi-", "").replace(".xlsx", "")
        
        for r in rows[1:]:
            if r[0] is None or r[name_idx] is None:
                continue
            name = str(r[name_idx]).strip()
            score_str = r[score_idx]
            # Parse score (e.g. 5/10 -> 5.0, or 8 -> 8.0)
            score_val = 0.0
            if score_str is not None:
                s = str(score_str).strip()
                if '/' in s:
                    score_val = float(s.split('/')[0])
                else:
                    try:
                        score_val = float(s)
                    except ValueError:
                        score_val = 0.0
            prev_scores[name] = {
                'score': score_val,
                'ca': ca_name,
                'raw': score_str
            }
    return prev_scores

if os.path.exists(main_file):
    prev_scores = load_previous_scores()
    print(f"Loaded {len(prev_scores)} students from previous ca-thi files.")
    
    wb = openpyxl.load_workbook(main_file, data_only=True)
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
    
    mismatches = []
    not_found = []
    matches = 0
    
    for r in rows[1:]:
        cname = r[class_idx]
        if not cname: continue
        
        # Only check KS24 (as previous files only had KS24 essay scores, wait, is that true? Let's check)
        if "KS24" in str(cname):
            name = str(r[name_idx]).strip()
            # Match name in prev_scores (we can do exact match or simple name check)
            prev = prev_scores.get(name)
            if prev:
                prev_essay_score_10 = prev['score']
                # The score in the previous file is out of 10 (e.g., 5/10 or 8/10).
                # The score in the main Excel sheet under 'Thực hành (Đ1)' is out of 100 (e.g., 55 or 100).
                # Let's check if: Thực hành (Đ1) == prev_essay_score_10 * 10
                th_val = r[th_idx]
                th_float = float(th_val) if th_val is not None else 0.0
                prev_float_100 = prev_essay_score_10 * 10.0
                
                diff = abs(th_float - prev_float_100)
                if diff > 1.0: # Allow minor rounding differences (e.g., 55 vs 56)
                    mismatches.append({
                        'name': name,
                        'class': cname,
                        'ca': prev['ca'],
                        'prev_raw': prev['raw'],
                        'prev_score_100': prev_float_100,
                        'excel_th': th_float,
                        'excel_sp': r[sp_idx],
                        'excel_vd': r[vd_idx],
                        'excel_tn': r[tn_idx],
                        'excel_final': r[final_idx]
                    })
                else:
                    matches += 1
            else:
                not_found.append(name)
                
    print(f"\nMatch Results for KS24 students:")
    print(f"  Exact/Close Matches (Thực hành = Prev * 10): {matches}")
    print(f"  Mismatches: {len(mismatches)}")
    print(f"  Not found in previous ca files: {len(not_found)}")
    
    if mismatches:
        print("\nMismatches detailed list (First 15):")
        for m in mismatches[:15]:
            print(f"Name: {m['name']:<25} | Class: {m['class']:<15} | Ca: {m['ca']:<6} | Prev Score (out of 100): {m['prev_score_100']:<5} | Excel Thực hành: {m['excel_th']:<5} | Final: {m['excel_final']}")
            
    if not_found:
        print("\nStudents in Main Excel but not in Ca Files (First 15):")
        for name in not_found[:15]:
            # find details
            for r in rows[1:]:
                if str(r[name_idx]).strip() == name:
                    print(f"Name: {name:<25} | Class: {r[class_idx]} | Final: {r[final_idx]}")
                    break
else:
    print("Main Excel file not found.")

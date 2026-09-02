import openpyxl
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

main_file = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"
ca_files = [
    "inputs/ket-qua-cham-DGNL-ca-thi-7-9.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-12-14.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-14-16.xlsx"
]

def clean_name(name):
    if name is None: return ""
    name = str(name).strip()
    # Strip suffixes like " 2", " 3", " 4", " 6" at the end of the name
    name = re.sub(r'\s+\d+$', '', name)
    return name.lower()

def load_previous_scores():
    # Store list of previous scores
    prev_list = []
    for path in ca_files:
        if not os.path.exists(path):
            continue
        wb = openpyxl.load_workbook(path, read_only=True)
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
                        
            prev_list.append({
                'name_raw': name,
                'name_clean': clean_name(name),
                'score_10': score_val,
                'score_100': score_val * 10.0,
                'ca': ca_name,
                'used': False
            })
    return prev_list

if os.path.exists(main_file):
    prev_scores = load_previous_scores()
    print(f"Loaded {len(prev_scores)} records from previous ca-thi files.")
    
    wb = openpyxl.load_workbook(main_file, data_only=True)
    sheet = wb["Danh sách ĐGNL CNTT"]
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    
    class_idx = headers.index('Mã lớp hiện tại')
    name_idx = headers.index('Họ và tên học viên')
    th_idx = headers.index('Thực hành (Đ1)')
    final_idx = headers.index('Điểm final (Đ1)')
    note_idx = headers.index('Ghi chú')
    
    matches = 0
    mismatches = []
    not_found = []
    
    for r in rows[1:]:
        cname = r[class_idx]
        if not cname or "KS24" not in str(cname):
            continue
            
        name_raw = str(r[name_idx]).strip()
        name_clean = clean_name(name_raw)
        
        th_val = r[th_idx]
        th_float = float(th_val) if th_val is not None else 0.0
        
        # Try to find a match in prev_scores
        best_match = None
        # First try: match clean name and ca thi if possible, or just clean name
        for p in prev_scores:
            if p['name_clean'] == name_clean and not p['used']:
                # Check score difference
                diff = abs(th_float - p['score_100'])
                if best_match is None or diff < abs(th_float - best_match['score_100']):
                    best_match = p
                    
        if best_match:
            best_match['used'] = True
            diff = abs(th_float - best_match['score_100'])
            if diff > 1.0:
                mismatches.append({
                    'name_raw': name_raw,
                    'class': cname,
                    'prev_name': best_match['name_raw'],
                    'prev_score_100': best_match['score_100'],
                    'excel_th': th_float,
                    'excel_final': r[final_idx],
                    'note': r[note_idx]
                })
            else:
                matches += 1
        else:
            not_found.append({
                'name_raw': name_raw,
                'class': cname,
                'excel_th': th_float,
                'excel_final': r[final_idx],
                'note': r[note_idx]
            })
            
    print(f"\nResults of proper matching for KS24:")
    print(f"  Exact/Close Matches: {matches}")
    print(f"  Mismatches (Genuine): {len(mismatches)}")
    print(f"  Not found in previous ca files: {len(not_found)}")
    
    if mismatches:
        print("\nGenuine Mismatches List:")
        for m in mismatches:
            print(f"Name: {m['name_raw']:<25} | Class: {m['class']:<15} | Prev Name: {m['prev_name']:<20} | Prev: {m['prev_score_100']:<5} | Excel Thực hành: {m['excel_th']:<5} | Final: {m['excel_final']:<5} | Note: {m['note']}")
            
    if not_found:
        print("\nNot Found Students List (Non-zero final scores first):")
        not_found_sorted = sorted(not_found, key=lambda x: x['excel_final'], reverse=True)
        for n in not_found_sorted[:15]:
            print(f"Name: {n['name_raw']:<25} | Class: {n['class']:<15} | Excel Thực hành: {n['excel_th']:<5} | Final: {n['excel_final']:<5} | Note: {n['note']}")
else:
    print("Excel file not found.")

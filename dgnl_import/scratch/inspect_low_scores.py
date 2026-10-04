import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ca_files = [
    "inputs/ket-qua-cham-DGNL-ca-thi-7-9.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-12-14.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-14-16.xlsx"
]

for path in ca_files:
    if not os.path.exists(path): continue
    wb = openpyxl.load_workbook(path, read_only=True)
    sheet = wb.active
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    crit_idx = headers.index('Chi tiết tiêu chí')
    name_idx = headers.index('Name')
    score_idx = headers.index('Điểm')
    
    print(f"\nFile: {os.path.basename(path)}")
    for r in rows[1:]:
        name = r[name_idx]
        score_str = r[score_idx]
        crit_text = r[crit_idx]
        if not crit_text: continue
        
        score_val = 0.0
        if score_str is not None:
            s = str(score_str).strip()
            if '/' in s:
                score_val = float(s.split('/')[0])
            else:
                try: score_val = float(s)
                except ValueError: pass
                
        if score_val > 0.0 and score_val <= 5.5:
            print(f"Name: {name} | Score: {score_str}")
            print("Chi tiết tiêu chí:")
            print(crit_text)
            print("-" * 50)

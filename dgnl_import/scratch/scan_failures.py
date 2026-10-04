import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ca_files = [
    "inputs/ket-qua-cham-DGNL-ca-thi-7-9.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-12-14.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-14-16.xlsx"
]

print("Scanning for non-passing criteria:")
found_non_pass = 0
total_students = 0

for path in ca_files:
    if not os.path.exists(path): continue
    wb = openpyxl.load_workbook(path, read_only=True)
    sheet = wb.active
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    crit_idx = headers.index('Chi tiết tiêu chí')
    name_idx = headers.index('Name')
    
    for r in rows[1:]:
        name = r[name_idx]
        crit_text = r[crit_idx]
        if not crit_text: continue
        
        total_students += 1
        lines = crit_text.split('\n')
        for line in lines:
            line_clean = line.strip()
            if not line_clean: continue
            
            # Check if "đạt" (case insensitive) is in the line
            if "đạt" not in line_clean.lower() and "pass" not in line_clean.lower():
                print(f"Student: {name} | Line: {line_clean}")
                found_non_pass += 1
                
print(f"Total students scanned: {total_students}")
print(f"Total non-passing criteria lines found: {found_non_pass}")

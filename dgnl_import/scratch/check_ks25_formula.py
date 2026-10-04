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
    th_idx = headers.index('Thực hành (Đ1)')
    tn_idx = headers.index('Trắc nghiệm (Đ1)')
    final_idx = headers.index('Điểm final (Đ1)')
    
    mismatches = []
    matches = 0
    zeros = 0
    
    for idx, r in enumerate(rows[1:], start=2):
        cname = r[class_idx]
        if cname and ("KS25" in str(cname) or "K25" in str(cname)) and "QTKD" not in str(cname):
            name = r[name_idx]
            th = r[th_idx]
            tn = r[tn_idx]
            final = r[final_idx]
            
            if final is None or final == 0:
                zeros += 1
                continue
                
            th_val = float(th) if th is not None else 0.0
            tn_val = float(tn) if tn is not None else 0.0
            
            # Formula: (th * 0.7 + tn * 0.3)
            # Wait, in the Excel final score might be scaled (out of 100 or out of 10?).
            # Let's check if final is out of 100 or out of 10.
            # In our previous inspection:
            # - Bùi Xuân Huy Đức (KS24) has final_excel = 76.0 (so final is out of 100 in the sheet).
            # - Let's see what KS25 has.
            calculated = th_val * 0.7 + tn_val * 0.3
            diff = abs(calculated - float(final))
            
            if diff > 0.1:
                mismatches.append({
                    'row': idx,
                    'name': name,
                    'class': cname,
                    'th': th,
                    'tn': tn,
                    'final_excel': final,
                    'calculated': round(calculated, 2),
                    'diff': round(diff, 2)
                })
            else:
                matches += 1
                
    print(f"Total checked: {matches + len(mismatches) + zeros}")
    print(f"Matches: {matches}")
    print(f"Zeros/Empty: {zeros}")
    print(f"Mismatches: {len(mismatches)}")
    
    if mismatches:
        print("\nMismatches list (First 10):")
        for m in mismatches[:10]:
            print(f"Row {m['row']} | {m['name']} ({m['class']}) | th={m['th']}, tn={m['tn']} | excel={m['final_excel']}, calc={m['calculated']} (diff={m['diff']})")
else:
    print("Excel file not found.")

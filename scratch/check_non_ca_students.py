import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

main_file = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"
ca_files = [
    "inputs/ket-qua-cham-DGNL-ca-thi-7-9.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-12-14.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-14-16.xlsx"
]

def load_previous_names():
    names = set()
    for path in ca_files:
        if not os.path.exists(path):
            continue
        wb = openpyxl.load_workbook(path, read_only=True)
        sheet = wb.active
        for r in sheet.iter_rows(values_only=True):
            if r[0] is not None and 'Name' not in str(r[0]) and 'Name' not in str(r[1]):
                name = str(r[1]).strip()
                if name: names.add(name)
    return names

if os.path.exists(main_file):
    prev_names = load_previous_names()
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
    ca_idx = headers.index('Ca thi')
    note_idx = headers.index('Ghi chú')
    
    not_found = []
    for r in rows[1:]:
        cname = r[class_idx]
        if cname and "KS24" in str(cname):
            name = str(r[name_idx]).strip()
            if name not in prev_names:
                not_found.append({
                    'name': name,
                    'class': cname,
                    'sp': r[sp_idx],
                    'vd': r[vd_idx],
                    'th': r[th_idx],
                    'tn': r[tn_idx],
                    'final': r[final_idx],
                    'ca': r[ca_idx],
                    'note': r[note_idx]
                })
                
    print(f"Total not found in previous files: {len(not_found)}")
    print(f"{'Name':<25} | {'Class':<15} | {'Ca':<12} | {'Prac':<5} | {'MCQ':<5} | {'Final':<5} | {'Note'}")
    print("-" * 100)
    for student in sorted(not_found, key=lambda x: x['final'], reverse=True):
        print(f"{student['name']:<25} | {student['class']:<15} | {str(student['ca']):<12} | {str(student['th']):<5} | {str(student['tn']):<5} | {str(student['final']):<5} | {student['note']}")
else:
    print("Excel file not found.")

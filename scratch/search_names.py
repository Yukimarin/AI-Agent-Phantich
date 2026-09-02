import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ca_files = [
    "inputs/ket-qua-cham-DGNL-ca-thi-7-9.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-12-14.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-14-16.xlsx"
]

target_substrings = ["Trường An", "Phương Anh", "Duy Mạnh", "Đức Anh", "Văn Ánh", "Mạnh Hùng", "Thanh Tùng", "Tiến Minh", "Quang Vinh", "Mạnh Thắng"]

print("Searching previous files:")
for path in ca_files:
    if not os.path.exists(path): continue
    wb = openpyxl.load_workbook(path, read_only=True)
    sheet = wb.active
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    name_idx = headers.index('Name')
    score_idx = headers.index('Điểm')
    
    print(f"\nFile: {os.path.basename(path)}")
    for r in rows[1:]:
        if r[name_idx]:
            name_str = str(r[name_idx]).strip()
            # Check if any substring is in the name
            for sub in target_substrings:
                if sub in name_str:
                    print(f"  Match: {name_str} | Score: {r[score_idx]}")
                    break

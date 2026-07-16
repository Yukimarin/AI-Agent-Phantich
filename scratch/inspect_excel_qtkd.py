import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import os

excel_paths = [
    r"C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx",
    r"docs/PTIT_Chiso.xlsx",
    r"data/PTIT_Chiso.xlsx"
]

excel_path = None
for p in excel_paths:
    if os.path.exists(p):
        excel_path = p
        break

if not excel_path:
    print("Excel file not found!")
    sys.exit(1)

print(f"Reading Excel from: {excel_path}")
xls = pd.ExcelFile(excel_path)
names = ["Bùi Hà Uyên", "Nguyễn Bảo Ngọc", "Nguyễn Minh Hiếu", "Lê Nam Phong"]

for sheet in xls.sheet_names:
    df = pd.read_excel(excel_path, sheet_name=sheet)
    for col in df.columns:
        # Check if any cell in df contains the names
        for name in names:
            matches = df[df[col].astype(str).str.contains(name, na=False)]
            if not matches.empty:
                print(f"=== Found '{name}' in sheet '{sheet}', column '{col}' ===")
                print(matches.to_string())

import sys
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Desktop\Backup\PTIT\PTIT_QLDT.xlsx"
xls = pd.ExcelFile(file_path)
print("Sheets in PTIT_QLDT.xlsx:", xls.sheet_names)

for sheet in xls.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    print(f"\nSheet: {sheet}")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist()[:10])
    print("First 3 rows:")
    print(df.head(3).to_string())

import sys
import pandas as pd

# Reconfigure stdout to use UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx"
xls = pd.ExcelFile(file_path)
print("Sheet names:", xls.sheet_names)

# Sheets to inspect based on the user's description (excluding SKL sheets)
target_sheets = [
    'KS24-JavaAdvance', 'KS24_JavaWeb', 'KS24_JWS', 'KS24_AI',
    'KS25_Javascript', 'KS25_Database', 'KS25_Python', 'KS25_Python_Web',
    'KS25_QTKD_M103', 'KS25_QTKD_M104', 'KS25_QTKD_DTB201', 'KS25_QTKD_DTB202'
]

for sheet in target_sheets:
    if sheet in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        print(f"\n==================================================")
        print(f"Sheet: {sheet}")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()[:10]} ...")
        print("First 3 rows:")
        print(df.head(3).to_string())

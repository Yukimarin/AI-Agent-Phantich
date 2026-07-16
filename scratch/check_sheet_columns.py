import sys
import openpyxl

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

excel_path = 'C:/Users/DELL/Desktop/Education-DB-Analytic/docs/PTIT_Chiso.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)

for sname in ['KS25_Python_Web', 'KS25_QTKD_DTB202']:
    print(f"\n--- Columns for {sname} ---")
    sheet = wb[sname]
    for r in range(1, 6):
        row_vals = [sheet.cell(row=r, column=c).value for c in range(1, 10)]
        print(f"Row {r}: {row_vals}")

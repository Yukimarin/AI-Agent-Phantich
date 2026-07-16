import sys
import openpyxl

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

excel_path = 'C:/Users/DELL/Desktop/Education-DB-Analytic/docs/PTIT_Chiso.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)
sheet = wb['KS24_AI']

for r in range(1, 6):
    row_vals = [sheet.cell(row=r, column=c).value for c in range(1, 15)]
    print(f"Row {r}: {row_vals}")

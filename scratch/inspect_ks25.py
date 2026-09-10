import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook(r'C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx', data_only=True)
sheet = wb['KS25_Phantichthietkehethong']
print("=== KS25_Phantichthietkehethong Full Detail ===")
header_dates = [sheet.cell(3, c).value for c in range(4, sheet.max_column + 1, 3)]
print("Dates:", [d.strftime('%d/%m/%Y') if hasattr(d, 'strftime') else str(d) for d in header_dates if d])

for r in range(5, sheet.max_row + 1):
    c_name = sheet.cell(r, 2).value
    teacher = sheet.cell(r, 3).value
    if c_name:
        vals = [sheet.cell(r, c).value for c in range(4, sheet.max_column + 1)]
        print(f"\n{c_name} (GV: {teacher}):")
        # print in groups of 3 (CC, BT, EL)
        for i in range(0, len(vals), 3):
            d_idx = i // 3
            d_str = header_dates[d_idx].strftime('%d/%m') if d_idx < len(header_dates) and hasattr(header_dates[d_idx], 'strftime') else f"Col{d_idx}"
            chunk = vals[i:i+3]
            print(f"  {d_str}: CC={chunk[0]}%, BT={chunk[1]}%, EL={chunk[2]}%")

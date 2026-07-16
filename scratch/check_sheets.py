import openpyxl
wb = openpyxl.load_workbook('docs/PTIT_Chiso.xlsx', read_only=True)
print("Sheet names in Excel:")
print(wb.sheetnames)

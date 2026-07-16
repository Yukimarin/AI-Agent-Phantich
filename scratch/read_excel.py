import pandas as pd

file_path = r"C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx"
xls = pd.ExcelFile(file_path)
print("Sheet names:", xls.sheet_names)

for sheet in xls.sheet_names[:5]: # print first 5 sheets info
    df = pd.read_excel(file_path, sheet_name=sheet, nrows=5)
    print(f"\n--- Sheet: {sheet} ---")
    print("Columns:", df.columns.tolist())
    print("First 2 rows:")
    print(df.head(2))

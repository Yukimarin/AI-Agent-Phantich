import sys
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx"
df = pd.read_excel(file_path, sheet_name='KS24-JavaAdvance')

for idx, row in df.iterrows():
    val_class = row.iloc[1]
    val_teacher = row.iloc[2]
    val_39 = row.iloc[39]
    val_40 = row.iloc[40]
    print(f"Row {idx}: Class={val_class}, Teacher={val_teacher}, Col39={val_39}, Col40={val_40}")

import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

f1 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx'
f2 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx'

for sname in ['Danh sách thi ĐGNL (Lần 1.2026)', 'Bảng điểm (Đợt 1)']:
    print(f"\n========================================")
    print(f"CHI TIẾT THAY ĐỔI SHEET: {sname}")
    print(f"========================================")
    df1 = pd.read_excel(f1, sheet_name=sname)
    df2 = pd.read_excel(f2, sheet_name=sname)
    
    print(f"Kích thước cũ: {df1.shape} -> Kích thước mới: {df2.shape}")
    
    # Check column diff
    c1 = list(df1.columns)
    c2 = list(df2.columns)
    print("Cột mới:", [c for c in c2 if c not in c1])
    print("Cột xóa:", [c for c in c1 if c not in c2])
    
    # Merge on Email học viên or SourceID
    id_col = 'Email học viên' if 'Email học viên' in df1.columns else ('SourceID' if 'SourceID' in df1.columns else None)
    if id_col:
        m = pd.merge(df1, df2, on=id_col, suffixes=('_cũ', '_mới'))
        common_cols = [c for c in c1 if c in c2 and c != id_col]
        for c in common_cols:
            s1 = m[f"{c}_cũ"].fillna('').astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
            s2 = m[f"{c}_mới"].fillna('').astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
            diffs = s1 != s2
            if diffs.sum() > 0:
                print(f"- Cột '{c}': {diffs.sum()} thay đổi.")
                sample = m[diffs][[id_col, 'Họ và tên học viên_mới' if 'Họ và tên học viên_mới' in m else id_col, f"{c}_cũ", f"{c}_mới"]].head(3)
                for _, r in sample.iterrows():
                    name_v = r.get('Họ và tên học viên_mới') or r.get(id_col)
                    print(f"    • {name_v}: '{r[f'{c}_cũ']}' -> '{r[f'{c}_mới']}'")


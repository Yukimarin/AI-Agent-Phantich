import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

f1 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx'
f2 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx'

for sname in ['Danh sách thi ĐGNL (Lần 1.2026)', 'Bảng điểm (Đợt 1)', 'Lịch thi_ĐGNL']:
    print(f"\n{'='*70}")
    print(f"=== SO SÁNH SHEET: {sname} ===")
    print(f"{'='*70}")
    
    df1 = pd.read_excel(f1, sheet_name=sname)
    df2 = pd.read_excel(f2, sheet_name=sname)
    
    print(f"Shape cũ: {df1.shape} -> Shape mới: {df2.shape}")
    
    cols1 = list(df1.columns)
    cols2 = list(df2.columns)
    
    print(f"Cột mới: {[c for c in cols2 if c not in cols1]}")
    print(f"Cột xóa: {[c for c in cols1 if c not in cols2]}")
    
    # compare
    if sname == 'Lịch thi_ĐGNL':
        # Let's inspect diff rows
        print("So sánh nội dung Lịch thi:")
        print(f"Số dòng cũ: {len(df1)}, số dòng mới: {len(df2)}")
        # print diffs
        for i in range(max(len(df1), len(df2))):
            if i >= len(df1):
                print(f"+ Dòng mới {i+1}: {df2.iloc[i].to_dict()}")
            elif i >= len(df2):
                print(f"- Dòng xóa {i+1}: {df1.iloc[i].to_dict()}")
            else:
                diffs = []
                for c in cols1:
                    if c in cols2:
                        v1 = str(df1.iloc[i][c]) if pd.notna(df1.iloc[i][c]) else ''
                        v2 = str(df2.iloc[i][c]) if pd.notna(df2.iloc[i][c]) else ''
                        if v1 != v2:
                            diffs.append(f"{c}: '{v1}' -> '{v2}'")
                if diffs:
                    print(f"* Dòng {i+1} thay đổi: {', '.join(diffs)}")
    else:
        id_col = 'Email học viên' if 'Email học viên' in df1.columns else ('SourceID' if 'SourceID' in df1.columns else df1.columns[0])
        print(f"ID col: {id_col}")
        
        # Check matching
        df1['key_id'] = df1[id_col].astype(str).str.strip()
        df2['key_id'] = df2[id_col].astype(str).str.strip()
        
        add = set(df2['key_id']) - set(df1['key_id'])
        rem = set(df1['key_id']) - set(df2['key_id'])
        print(f"Học viên mới: {len(add)}: {list(add)[:10]}")
        print(f"Học viên xóa: {len(rem)}: {list(rem)[:10]}")
        
        # Merge
        m = pd.merge(df1, df2, on='key_id', suffixes=('_cũ', '_mới'))
        common_cols = [c for c in cols1 if c in cols2 and c != 'key_id']
        
        diff_summary = {}
        for c in common_cols:
            s1 = m[f"{c}_cũ"].fillna('').astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
            s2 = m[f"{c}_mới"].fillna('').astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
            d = (s1 != s2).sum()
            if d > 0:
                diff_summary[c] = d
                
        print(f"Các cột thay đổi dữ liệu ({len(m)} bản ghi chung):")
        for c, d in sorted(diff_summary.items(), key=lambda x: -x[1]):
            print(f"  - {c}: {d} thay đổi")
            # print samples
            sample = m[m[f"{c}_cũ"].fillna('').astype(str).str.strip().str.replace(r'\.0$', '', regex=True) != m[f"{c}_mới"].fillna('').astype(str).str.strip().str.replace(r'\.0$', '', regex=True)][['key_id', f"{c}_cũ", f"{c}_mới"]].head(3)
            for _, r in sample.iterrows():
                print(f"      SV {r['key_id']}: '{r[f'{c}_cũ']}' -> '{r[f'{c}_mới']}'")

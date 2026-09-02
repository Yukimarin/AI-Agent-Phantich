import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

f1 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx'
f2 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx'

excel1 = pd.ExcelFile(f1)
excel2 = pd.ExcelFile(f2)

sheets = excel2.sheet_names

for sname in sheets:
    print(f"\n{'='*60}")
    print(f"CHI TIẾT THAY ĐỔI SHEET: {sname}")
    print(f"{'='*60}")
    
    df1 = pd.read_excel(f1, sheet_name=sname)
    df2 = pd.read_excel(f2, sheet_name=sname)
    
    # Identify key column for merging / student identity
    id_col = None
    for cand in ['SourceID', 'Email học viên', 'Mã lớp hiện tại', 'Họ tên', 'Tên']:
        if cand in df1.columns and cand in df2.columns:
            id_col = cand
            break
            
    print(f"-> Key định danh: {id_col}")
    
    # 1. Added / Removed Rows based on key or index
    if id_col == 'SourceID' or (id_col and id_col in ['Email học viên', 'Họ và tên học viên']):
        # If SourceID has duplicates or NaNs, handle carefully
        df1_keys = df1[id_col].dropna().astype(str).tolist()
        df2_keys = df2[id_col].dropna().astype(str).tolist()
        
        added_keys = set(df2_keys) - set(df1_keys)
        removed_keys = set(df1_keys) - set(df2_keys)
        
        if added_keys:
            print(f"\n[+] CÁC DÒNG / HỌC VIÊN MỚI THÊM VÀO ({len(added_keys)} học viên):")
            new_rows = df2[df2[id_col].astype(str).isin(added_keys)]
            for _, r in new_rows.iterrows():
                name = r.get('Họ và tên học viên') or r.get('Tên') or r.get('Họ tên') or ''
                email = r.get('Email học viên', '')
                lop = r.get('Mã lớp hiện tại') or r.get('Mã lớp') or ''
                print(f"   - [{r[id_col]}] {name} | Lớp: {lop} | Email: {email}")
                
        if removed_keys:
            print(f"\n[-] CÁC DÒNG / HỌC VIÊN BỊ BỎ RA ({len(removed_keys)} học viên):")
            rem_rows = df1[df1[id_col].astype(str).isin(removed_keys)]
            for _, r in rem_rows.iterrows():
                name = r.get('Họ và tên học viên') or r.get('Tên') or r.get('Họ tên') or ''
                email = r.get('Email học viên', '')
                lop = r.get('Mã lớp hiện tại') or r.get('Mã lớp') or ''
                print(f"   - [{r[id_col]}] {name} | Lớp: {lop} | Email: {email}")
    
    elif sname == 'Thi bổ sung Đợt 1':
        # Compare by Họ tên + Môn thi + Thời gian đky
        df1['key_bs'] = df1['Họ tên'].astype(str) + " _ " + df1['Môn thi'].astype(str)
        df2['key_bs'] = df2['Họ tên'].astype(str) + " _ " + df2['Môn thi'].astype(str)
        
        added_bs = set(df2['key_bs']) - set(df1['key_bs'])
        removed_bs = set(df1['key_bs']) - set(df2['key_bs'])
        
        if added_bs:
            print(f"\n[+] CÁC ĐĂNG KÝ BỔ SUNG MỚI ({len(added_bs)} dòng):")
            for item in added_bs:
                row = df2[df2['key_bs'] == item].iloc[0]
                print(f"   - {row['Họ tên']} | Môn: {row['Môn thi']} | Lớp: {row['Mã lớp']} | Cơ sở: {row['Cơ sở thi']} | TG: {row['Thời gian đky']}")
                
        if removed_bs:
            print(f"\n[-] CÁC ĐĂNG KÝ BỔ SUNG BỊ BỎ ({len(removed_bs)} dòng):")
            for item in removed_bs:
                row = df1[df1['key_bs'] == item].iloc[0]
                print(f"   - {row['Họ tên']} | Môn: {row['Môn thi']}")

    # 2. Check changes in common columns for existing records
    common_cols = [c for c in df1.columns if c in df2.columns and c not in ['key_bs']]
    
    # Compare by SourceID or Email or row-by-row
    if 'SourceID' in df1.columns and 'SourceID' in df2.columns:
        # Merge on SourceID
        m = pd.merge(df1, df2, on='SourceID', suffixes=('_cũ', '_mới'), how='inner')
        changed_fields = {}
        
        for c in common_cols:
            if c == 'SourceID':
                continue
            col_old = f"{c}_cũ"
            col_new = f"{c}_mới"
            
            # Compare considering NaNs
            s_old = m[col_old].fillna('').astype(str).str.strip()
            s_new = m[col_new].fillna('').astype(str).str.strip()
            
            diff_mask = s_old != s_new
            diff_count = diff_mask.sum()
            if diff_count > 0:
                changed_fields[c] = diff_count
                
        if changed_fields:
            print(f"\n[*] CÁC CỘT CÓ DỮ LIỆU THAY ĐỔI Ở CÁC HỌC VIÊN CŨ:")
            for c, cnt in changed_fields.items():
                print(f"   - Cột '{c}': có {cnt} học viên thay đổi giá trị.")
                # Print a few samples
                col_old = f"{c}_cũ"
                col_new = f"{c}_mới"
                sample_diff = m[m[col_old].fillna('').astype(str).str.strip() != m[col_new].fillna('').astype(str).str.strip()][['SourceID', 'Họ và tên học viên_mới' if 'Họ và tên học viên_mới' in m else 'Tên_mới', col_old, col_new]].head(5)
                for _, row in sample_diff.iterrows():
                    name_val = row.get('Họ và tên học viên_mới') or row.get('Tên_mới') or ''
                    print(f"       + SV: {name_val} (ID: {row['SourceID']}) | Cũ: '{row[col_old]}' -> Mới: '{row[col_new]}'")
                if cnt > 5:
                    print(f"       + ... và {cnt - 5} học viên khác.")
        else:
            print("\n[*] Không có thay đổi dữ liệu trên các cột chung của học viên cũ.")
            
    # Check new columns content
    new_cols = set(df2.columns) - set(df1.columns) - {'key_bs'}
    if new_cols:
        print(f"\n[+] NỘI DUNG CỘT MỚI:")
        for nc in new_cols:
            non_empty = df2[nc].dropna()
            non_empty_str = non_empty[non_empty.astype(str).str.strip() != '']
            print(f"   - Cột '{nc}': có {len(non_empty_str)}/{len(df2)} dòng có dữ liệu.")
            if len(non_empty_str) > 0:
                print(f"     Giá trị mẫu/phân bố: {dict(non_empty_str.value_counts().head(5))}")

import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

f1 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx'
f2 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx'

first_sheets = [
    'Danh sách thi ĐGNL (Lần 1.2026)',
    'Bảng điểm (Đợt 1)',
    'Lịch thi_ĐGNL',
    'Danh sách ĐGNL CNTT',
    'Danh sách ĐGNL QTKD'
]

def clean_val(v):
    if pd.isna(v):
        return ""
    v_str = str(v).strip()
    if v_str.endswith(".0"):
        v_str = v_str[:-2]
    return v_str

for sname in first_sheets:
    print(f"\n{'='*70}")
    print(f"=== SO SÁNH SHEET: {sname} ===")
    print(f"{'='*70}")
    
    df1 = pd.read_excel(f1, sheet_name=sname)
    df2 = pd.read_excel(f2, sheet_name=sname)
    
    print(f"File cũ: {df1.shape[0]} dòng, {df1.shape[1]} cột")
    print(f"File mới: {df2.shape[0]} dòng, {df2.shape[1]} cột")
    
    cols1 = list(df1.columns)
    cols2 = list(df2.columns)
    
    new_cols = [c for c in cols2 if c not in cols1]
    del_cols = [c for c in cols1 if c not in cols2]
    
    if new_cols:
        print(f"[+] Cột mới thêm: {new_cols}")
    if del_cols:
        print(f"[-] Cột bị xóa: {del_cols}")
        
    id_col = 'Email học viên' if 'Email học viên' in df1.columns else ('SourceID' if 'SourceID' in df1.columns else None)
    if not id_col:
        for cand in ['Họ và tên học viên', 'Tên SV', 'Tên', 'Họ tên']:
            if cand in df1.columns:
                id_col = cand
                break
                
    print(f"Cột định danh: {id_col}")
    
    if id_col:
        d1 = {}
        for idx, row in df1.iterrows():
            k = clean_val(row[id_col])
            if k and k not in d1:
                d1[k] = row
            elif k:
                d1[f"{k}_{idx}"] = row
                
        d2 = {}
        for idx, row in df2.iterrows():
            k = clean_val(row[id_col])
            if k and k not in d2:
                d2[k] = row
            elif k:
                d2[f"{k}_{idx}"] = row
                
        added_keys = [k for k in d2 if k not in d1]
        removed_keys = [k for k in d1 if k not in d2]
        common_keys = [k for k in d2 if k in d1]
        
        print(f"-> Thêm mới: {len(added_keys)} bản ghi")
        for k in added_keys:
            r = d2[k]
            name = r.get('Họ và tên học viên') or r.get('Tên') or r.get('Tên SV') or ''
            email = r.get('Email học viên', '')
            lop = r.get('Mã lớp hiện tại') or ''
            print(f"     + [{k}] {name} | Lớp: {lop} | Email: {email}")
            
        print(f"-> Bị xóa: {len(removed_keys)} bản ghi")
        for k in removed_keys:
            r = d1[k]
            name = r.get('Họ và tên học viên') or r.get('Tên') or r.get('Tên SV') or ''
            print(f"     - [{k}] {name}")
            
        common_cols = [c for c in cols1 if c in cols2]
        diff_stats = {}
        detailed_changes = []
        for k in common_keys:
            r1 = d1[k]
            r2 = d2[k]
            for c in common_cols:
                v1 = clean_val(r1[c])
                v2 = clean_val(r2[c])
                if v1 != v2:
                    diff_stats[c] = diff_stats.get(c, 0) + 1
                    name = str(r2.get('Họ và tên học viên') or r2.get('Tên') or r2.get('Tên SV') or '')
                    detailed_changes.append({'key': k, 'name': name, 'col': c, 'old': v1, 'new': v2})
                    
        if diff_stats:
            print(f"\n[*] CÁC CỘT CÓ THAY ĐỔI DỮ LIỆU ({len(common_keys)} bản ghi chung):")
            for c, cnt in sorted(diff_stats.items(), key=lambda x: -x[1]):
                print(f"   - '{c}': {cnt} thay đổi")
                samples = [ch for ch in detailed_changes if ch['col'] == c][:3]
                for s in samples:
                    print(f"       • SV {s['name']}: '{s['old']}' -> '{s['new']}'")
                    
        if new_cols:
            print(f"\n[+] THỐNG KÊ DỮ LIỆU CỘT MỚI:")
            for nc in new_cols:
                vals = [clean_val(d2[k].get(nc)) for k in d2 if clean_val(d2[k].get(nc)) != ""]
                print(f"   - '{nc}': {len(vals)}/{len(d2)} dòng có dữ liệu. Phân bố mẫu: {pd.Series(vals).value_counts().head(5).to_dict()}")
    else:
        # Lịch thi_ĐGNL
        print(f"Đối chiếu từng ô:")
        for r_i in range(max(len(df1), len(df2))):
            if r_i >= len(df1):
                print(f"  + Thêm dòng {r_i+2}: {df2.iloc[r_i].to_dict()}")
            elif r_i >= len(df2):
                print(f"  - Xóa dòng {r_i+2}: {df1.iloc[r_i].to_dict()}")
            else:
                for c_i in range(min(len(df1.columns), len(df2.columns))):
                    v1 = clean_val(df1.iloc[r_i, c_i])
                    v2 = clean_val(df2.iloc[r_i, c_i])
                    if v1 != v2:
                        print(f"  * Dòng {r_i+2}, Cột '{df1.columns[c_i]}': '{v1}' -> '{v2}'")

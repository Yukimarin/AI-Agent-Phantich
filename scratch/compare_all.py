import sys
import pandas as pd
import numpy as np
import json

sys.stdout.reconfigure(encoding='utf-8')

f1 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx'
f2 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx'

sheets = [
    'Danh sách thi ĐGNL (Lần 1.2026)',
    'Bảng điểm (Đợt 1)',
    'Lịch thi_ĐGNL',
    'Danh sách ĐGNL CNTT',
    'Danh sách ĐGNL QTKD',
    'Danh sách ĐGNL ngoại ngữ',
    'Danh sách ĐGNL Kỹ năng mềm',
    'Thi bổ sung Đợt 1'
]

def clean_val(v):
    if pd.isna(v):
        return ""
    v_str = str(v).strip()
    if v_str.endswith(".0"):
        v_str = v_str[:-2]
    return v_str

summary_report = {}

for sname in sheets:
    print(f"\n{'='*70}")
    print(f"=== SO SÁNH SHEET: {sname} ===")
    print(f"{'='*70}")
    
    df1 = pd.read_excel(f1, sheet_name=sname)
    df2 = pd.read_excel(f2, sheet_name=sname)
    
    print(f"File cũ: {df1.shape[0]} dòng, {df1.shape[1]} cột")
    print(f"File mới: {df2.shape[0]} dòng, {df2.shape[1]} cột")
    
    # Check columns
    cols1 = list(df1.columns)
    cols2 = list(df2.columns)
    
    new_cols = [c for c in cols2 if c not in cols1]
    del_cols = [c for c in cols1 if c not in cols2]
    
    if new_cols:
        print(f"[+] Cột mới: {new_cols}")
    if del_cols:
        print(f"[-] Cột bị bỏ: {del_cols}")
        
    # Match rows
    # Try finding primary identifier: Email -> SourceID -> Họ và tên + Ngày sinh/Mã lớp -> Index
    id_col = None
    for cand in ['Email học viên', 'SourceID', 'Họ tên', 'Tên']:
        if cand in df1.columns and cand in df2.columns:
            # check uniqueness
            if df2[cand].dropna().is_unique and df1[cand].dropna().is_unique:
                id_col = cand
                break
    
    if not id_col:
        for cand in ['Email học viên', 'SourceID', 'Họ và tên học viên', 'Họ tên', 'Tên']:
            if cand in df1.columns and cand in df2.columns:
                id_col = cand
                break
                
    print(f"Cột định danh đối chiếu: {id_col}")
    
    if id_col:
        # Create dict by id_col
        # Drop duplicates or keep last
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
        
        print(f"Số bản ghi mới thêm: {len(added_keys)}")
        if added_keys:
            for k in added_keys[:10]:
                r = d2[k]
                name = r.get('Họ và tên học viên') or r.get('Tên') or r.get('Họ tên') or ''
                email = r.get('Email học viên', '')
                lop = r.get('Mã lớp hiện tại') or r.get('Mã lớp') or ''
                print(f"  + Thêm mới: [{k}] | Họ tên: {name} | Lớp: {lop} | Email: {email}")
            if len(added_keys) > 10:
                print(f"  + ... và {len(added_keys)-10} bản ghi khác.")
                
        print(f"Số bản ghi bị xóa: {len(removed_keys)}")
        if removed_keys:
            for k in removed_keys[:10]:
                r = d1[k]
                name = r.get('Họ và tên học viên') or r.get('Tên') or r.get('Họ tên') or ''
                print(f"  - Xóa: [{k}] | Họ tên: {name}")
                
        # Compare cell values in common records
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
                    name = str(r2.get('Họ và tên học viên') or r2.get('Tên') or r2.get('Họ tên') or '')
                    detailed_changes.append({
                        'key': k,
                        'name': name,
                        'col': c,
                        'old': v1,
                        'new': v2
                    })
                    
        if diff_stats:
            print(f"\n[*] CÁC CỘT CÓ DỮ LIỆU CẬP NHẬT/THAY ĐỔI TRÊN {len(common_keys)} BẢN GHI HIỆN HỮU:")
            for c, cnt in sorted(diff_stats.items(), key=lambda x: -x[1]):
                print(f"  - Cột '{c}': {cnt} thay đổi")
                # Show up to 3 examples
                samples = [ch for ch in detailed_changes if ch['col'] == c][:3]
                for s in samples:
                    print(f"      • SV {s['name']}: '{s['old']}' -> '{s['new']}'")
        else:
            print("\n[*] Không có thay đổi trên các cột dữ liệu chung.")
            
        # Check new columns content
        if new_cols:
            print(f"\n[+] TỔNG KẾT CỘT MỚI:")
            for nc in new_cols:
                vals = [clean_val(d2[k].get(nc)) for k in d2 if clean_val(d2[k].get(nc)) != ""]
                print(f"  - Cột '{nc}': {len(vals)} dòng có dữ liệu (Ví dụ giá trị: {list(set(vals))[:5]})")
    else:
        # Simple diff by index or shape
        print(f"So sánh theo dòng/cột:")
        # Check exact equality
        # Print differences
        for r_i in range(min(len(df1), len(df2))):
            for c_i in range(min(len(df1.columns), len(df2.columns))):
                v1 = clean_val(df1.iloc[r_i, c_i])
                v2 = clean_val(df2.iloc[r_i, c_i])
                if v1 != v2:
                    print(f"  - Dòng {r_i+2}, Cột '{df1.columns[c_i]}': '{v1}' -> '{v2}'")

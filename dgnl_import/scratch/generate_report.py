import sys
import os
import pandas as pd
import numpy as np
import json

f1 = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"
f2 = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx"

xl1 = pd.ExcelFile(f1)
xl2 = pd.ExcelFile(f2)

report = {
    "old_file": f1,
    "new_file": f2,
    "old_sheets": xl1.sheet_names,
    "new_sheets": xl2.sheet_names,
    "sheets_detail": {}
}

def clean_str(val):
    if pd.isna(val):
        return ""
    s = str(val).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s

for s in xl2.sheet_names:
    if s not in xl1.sheet_names:
        report["sheets_detail"][s] = {"status": "new_sheet"}
        continue
    df1 = pd.read_excel(f1, sheet_name=s)
    df2 = pd.read_excel(f2, sheet_name=s)
    
    sheet_info = {
        "old_rows": len(df1),
        "new_rows": len(df2),
        "row_diff": len(df2) - len(df1),
        "old_cols_count": len(df1.columns),
        "new_cols_count": len(df2.columns),
        "new_cols": [c for c in df2.columns if c not in df1.columns],
        "del_cols": [c for c in df1.columns if c not in df2.columns],
        "common_cols": [c for c in df1.columns if c in df2.columns],
    }
    
    id_col = None
    for cand in ["SourceID", "Email học viên", "Họ tên", "Tên"]:
        if cand in df1.columns and cand in df2.columns:
            id_col = cand
            break
            
    sheet_info["id_col"] = id_col
    
    if id_col:
        keys1 = [clean_str(x) for x in df1[id_col] if clean_str(x)]
        keys2 = [clean_str(x) for x in df2[id_col] if clean_str(x)]
        
        s_keys1 = set(keys1)
        s_keys2 = set(keys2)
        
        sheet_info["new_records_count"] = len(s_keys2 - s_keys1)
        sheet_info["deleted_records_count"] = len(s_keys1 - s_keys2)
        sheet_info["new_records_sample"] = list(s_keys2 - s_keys1)[:10]
        sheet_info["deleted_records_sample"] = list(s_keys1 - s_keys2)[:10]
        
        # Check column changes for common rows
        df1_unique = df1.drop_duplicates(subset=[id_col]).set_index(id_col)
        df2_unique = df2.drop_duplicates(subset=[id_col]).set_index(id_col)
        common_idx = df1_unique.index.intersection(df2_unique.index)
        
        col_changes = {}
        for col in sheet_info["common_cols"]:
            if col == id_col:
                continue
            s1 = df1_unique.loc[common_idx, col].apply(clean_str)
            s2 = df2_unique.loc[common_idx, col].apply(clean_str)
            diff = s1 != s2
            diff_cnt = int(diff.sum())
            if diff_cnt > 0:
                diff_idx = common_idx[diff]
                samples = []
                for idx_val in diff_idx[:5]:
                    name_val = df2_unique.loc[idx_val].get("Họ và tên học viên") or df2_unique.loc[idx_val].get("Tên") or df2_unique.loc[idx_val].get("Họ tên") or str(idx_val)
                    samples.append({
                        "id": str(idx_val),
                        "name": str(name_val),
                        "old": str(s1.loc[idx_val]),
                        "new": str(s2.loc[idx_val])
                    })
                col_changes[col] = {
                    "count": diff_cnt,
                    "samples": samples
                }
        sheet_info["column_changes"] = col_changes
    
    report["sheets_detail"][s] = sheet_info

with open(r"c:\Users\DELL\Desktop\AI-Agent\AI-ĐGNL\scratch\full_report.json", "w", encoding="utf-8") as out:
    json.dump(report, out, ensure_ascii=False, indent=2)

print("SUCCESS")

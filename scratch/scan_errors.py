import openpyxl
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"

keywords = [
    "lỗi", "không hiện", "không hiển thị", "không nộp", "mất bài", 
    "trắng", "hệ thống", "không có đề", "sập", "error", "không load", "loading"
]

def clean_str(val):
    if val is None:
        return ""
    return str(val).strip()

def search_sheet_errors(wb, sheet_name):
    if sheet_name not in wb.sheetnames:
        print(f"Sheet {sheet_name} not found.")
        return []
        
    sheet = wb[sheet_name]
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    
    # Try to find columns for name, class, notes, minutes, session
    name_idx = None
    class_idx = None
    note_idx = None
    bb_idx = None
    ca_idx = None
    
    for idx, h in enumerate(headers):
        h_clean = clean_str(h).lower()
        if 'họ và tên' in h_clean or 'họ tên' in h_clean or h_clean == 'tên sv' or h_clean == 'tên':
            if name_idx is None: name_idx = idx
        if 'mã lớp' in h_clean or h_clean == 'lớp':
            if class_idx is None: class_idx = idx
        if 'ghi chú' in h_clean or 'note' in h_clean:
            if note_idx is None: note_idx = idx
        if 'biên bản' in h_clean or 'kết quả bb' in h_clean:
            if bb_idx is None: bb_idx = idx
        if 'ca thi' in h_clean:
            if ca_idx is None: ca_idx = idx
            
    # Fallbacks if some indices are not found
    if name_idx is None: name_idx = 1
    if class_idx is None: class_idx = 7
    if note_idx is None:
        # search for note column
        for idx, h in enumerate(headers):
            if 'chú' in clean_str(h).lower(): note_idx = idx
    if bb_idx is None:
        for idx, h in enumerate(headers):
            if 'bản' in clean_str(h).lower(): bb_idx = idx
            
    results = []
    
    for r_idx, r in enumerate(rows[1:], start=2):
        name = clean_str(r[name_idx])
        cname = clean_str(r[class_idx])
        note = clean_str(r[note_idx]) if note_idx is not None else ""
        bb = clean_str(r[bb_idx]) if bb_idx is not None else ""
        ca = clean_str(r[ca_idx]) if ca_idx is not None else ""
        
        combined_text = (note + " " + bb).lower()
        
        matched_kws = [kw for kw in keywords if kw in combined_text]
        if matched_kws:
            results.append({
                'row': r_idx,
                'name': name,
                'class': cname,
                'ca': ca,
                'note': note,
                'bb': bb,
                'keywords': matched_kws,
                'sheet': sheet_name
            })
            
    return results

if os.path.exists(file_path):
    wb = openpyxl.load_workbook(file_path, read_only=True)
    sheets_to_scan = [
        "Danh sách ĐGNL CNTT",
        "Danh sách ĐGNL QTKD",
        "Danh sách ĐGNL ngoại ngữ",
        "Danh sách ĐGNL Kỹ năng mềm"
    ]
    
    all_errors = []
    for s in sheets_to_scan:
        errors = search_sheet_errors(wb, s)
        print(f"Sheet: {s} | Found {len(errors)} potential system error records.")
        all_errors.extend(errors)
        
    print(f"\nTotal system errors found across all sheets: {len(all_errors)}")
    
    # Group by Cohort (KS24 vs KS25)
    ks24_count = 0
    ks25_count = 0
    other_count = 0
    
    for err in all_errors:
        cname = err['class']
        if "KS24" in cname:
            ks24_count += 1
        elif "KS25" in cname or "K25" in cname:
            ks25_count += 1
        else:
            other_count += 1
            
    print(f"KS24 records: {ks24_count}")
    print(f"KS25 records: {ks25_count}")
    print(f"Other records: {other_count}")
    
    # Print KS24 detailed errors
    print("\nKS24 System Error Records:")
    for err in all_errors:
        if "KS24" in err['class']:
            print(f"Sheet: {err['sheet']} | Row {err['row']} | Name: {err['name']:<25} | Class: {err['class']:<15} | Ca: {err['ca']:<15}")
            print(f"  Note: {err['note']}")
            print(f"  BB:   {err['bb']}")
            
    # Print KS25 detailed errors (first 10)
    print("\nKS25 System Error Records (First 15):")
    ks25_printed = 0
    for err in all_errors:
        if "KS25" in err['class'] or "K25" in err['class']:
            print(f"Sheet: {err['sheet']} | Row {err['row']} | Name: {err['name']:<25} | Class: {err['class']:<15} | Ca: {err['ca']:<15}")
            print(f"  Note: {err['note']}")
            print(f"  BB:   {err['bb']}")
            ks25_printed += 1
            if ks25_printed >= 15:
                break
else:
    print("Excel file not found.")

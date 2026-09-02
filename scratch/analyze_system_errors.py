import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"

def clean_str(val):
    if val is None:
        return ""
    return str(val).strip()

if os.path.exists(file_path):
    wb = openpyxl.load_workbook(file_path, read_only=True)
    
    # 1. Analyze Danh sách ĐGNL CNTT
    cntt_sheet = wb["Danh sách ĐGNL CNTT"]
    cntt_rows = list(cntt_sheet.iter_rows(values_only=True))
    cntt_headers = cntt_rows[0]
    
    class_idx = cntt_headers.index('Mã lớp hiện tại')
    name_idx = cntt_headers.index('Họ và tên học viên')
    note_idx = cntt_headers.index('Ghi chú')
    bb_idx = cntt_headers.index('Biên bản')
    ca_idx = cntt_headers.index('Ca thi')
    
    cntt_errors = []
    for r_idx, r in enumerate(cntt_rows[1:], start=2):
        name = clean_str(r[name_idx])
        cname = clean_str(r[class_idx])
        note = clean_str(r[note_idx])
        bb = clean_str(r[bb_idx])
        ca = clean_str(r[ca_idx])
        
        combined = (note + " " + bb).lower()
        
        is_error = False
        reason = ""
        
        # Check for error keywords
        keywords = ["lỗi", "không nộp", "mất bài", "trắng", "hệ thống", "không có đề", "sập", "error", "không load", "simple care", "out", "không vào lại"]
        for kw in keywords:
            if kw in combined:
                is_error = True
                reason = note if note else bb
                break
                
        # Also check if they are in "Biên bản" as "Thi bổ sung"
        if "thi bổ sung" in combined or "hoãn thi" in combined:
            is_error = True
            reason = bb if bb else note
            
        if is_error:
            cntt_errors.append({
                'name': name,
                'class': cname,
                'ca': ca,
                'note': note,
                'bb': bb,
                'reason': reason
            })
            
    print(f"Total CNTT records with errors/supplementary status: {len(cntt_errors)}")
    
    # Group by cohort and session
    ks24_cntt = [e for e in cntt_errors if "KS24" in e['class']]
    ks25_cntt = [e for e in cntt_errors if "KS25" in e['class'] or "K25" in e['class']]
    
    print(f"\n--- KS24 CNTT System Errors / Issues ({len(ks24_cntt)} students) ---")
    for e in ks24_cntt:
        print(f"Name: {e['name']:<30} | Class: {e['class']:<15} | Ca: {e['ca']:<15}")
        print(f"  Note: {e['note']}")
        print(f"  BB:   {e['bb']}")
        
    print(f"\n--- KS25 CNTT System Errors / Issues ({len(ks25_cntt)} students) ---")
    # Group KS25 by ca thi
    ca_groups = {}
    for e in ks25_cntt:
        ca = e['ca'] if e['ca'] else "Unknown Ca"
        if ca not in ca_groups:
            ca_groups[ca] = []
        ca_groups[ca].append(e)
        
    for ca, group in sorted(ca_groups.items()):
        print(f"\nCa thi: {ca} ({len(group)} students affected)")
        for e in group[:10]: # Print first 10
            print(f"  - {e['name']} ({e['class']}): Note='{e['note']}', BB='{e['bb']}'")
        if len(group) > 10:
            print(f"  ... and {len(group) - 10} more students")

    # 2. Let's analyze "Thi bổ sung Đợt 1" sheet
    supp_sheet = wb["Thi bổ sung Đợt 1"]
    supp_rows = list(supp_sheet.iter_rows(values_only=True))
    supp_headers = supp_rows[0]
    
    s_name_idx = supp_headers.index('Họ tên')
    s_class_idx = supp_headers.index('Mã lớp')
    s_mon_idx = supp_headers.index('Môn thi')
    
    supp_students = []
    for r in supp_rows[1:]:
        name = clean_str(r[s_name_idx])
        cname = clean_str(r[s_class_idx])
        mon = clean_str(r[s_mon_idx])
        if name:
            supp_students.append({'name': name, 'class': cname, 'subject': mon})
            
    print(f"\nTotal students registered in 'Thi bổ sung Đợt 1' sheet: {len(supp_students)}")
    ks24_supp = [s for s in supp_students if "KS24" in s['class']]
    ks25_supp = [s for s in supp_students if "KS25" in s['class'] or "K25" in s['class']]
    print(f"  KS24 registered: {len(ks24_supp)}")
    print(f"  KS25 registered: {len(ks25_supp)}")
    
    print("\nKS24 Registered for supplementary exam (by subject):")
    subj_counts = {}
    for s in ks24_supp:
        subj = s['subject']
        subj_counts[subj] = subj_counts.get(subj, 0) + 1
    for subj, c in subj_counts.items():
        print(f"  - {subj}: {c} students")
        
    print("\nKS25 Registered for supplementary exam (by subject):")
    subj_counts_25 = {}
    for s in ks25_supp:
        subj = s['subject']
        subj_counts_25[subj] = subj_counts_25.get(subj, 0) + 1
    for subj, c in subj_counts_25.items():
        print(f"  - {subj}: {c} students")
else:
    print("Excel file not found.")

import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ca_file = "inputs/ket-qua-cham-DGNL-ca-thi-12-14.xlsx"

def analyze_student_criteria_test(criteria_text):
    if not criteria_text:
        return {}
    lines = criteria_text.split('\n')
    
    ct_total = 0; ct_pass = 0
    sa_total = 0; sa_pass = 0
    st_total = 0; st_pass = 0
    
    c1_total = 0; c1_pass = 0
    c2_total = 0; c2_pass = 0
    c3_total = 0; c3_pass = 0
    
    ct_keywords = ['transaction', 'đồng thời', '@transactional', 'giao dịch', 'đồng bộ', 'race condition', 'lock', 'khóa', 'trùng ghế', 'bán vượt']
    sa_keywords = ['path traversal', 'idor', 'client', 'ủy quyền', 'xác thực', 'security', 'bảo mật', 'quyền truy cập', 'giá vé', 'unitprice', 'ticketprice', 'giá sản phẩm', 'đường dẫn']
    st_keywords = ['câu 3', 'câu hỏi định hướng', 'lựa chọn', 'ưu tiên', 'suất chiếu hot', 'khung giờ', 'bấm nút', 'chuyển tiền']
    
    for line in lines:
        line_clean = line.strip().lower()
        if not line_clean: continue
        
        is_pass = False
        if '— đạt' in line_clean or '– đạt' in line_clean or ': đạt' in line_clean or '— pass' in line_clean or 'đạt:' in line_clean:
            is_pass = True
        elif '— không đạt' in line_clean or '– không đạt' in line_clean or ': không đạt' in line_clean or '— fail' in line_clean:
            is_pass = False
        else:
            if 'đạt' in line and 'không đạt' not in line:
                is_pass = True
                
        is_c1 = 'câu 1' in line_clean or 'nhận diện' in line_clean or 'phát hiện' in line_clean
        is_c2 = 'câu 2' in line_clean or 'giải pháp' in line_clean or 'khắc phục' in line_clean
        is_c3 = 'câu 3' in line_clean or 'lựa chọn giải pháp' in line_clean or 'chọn một' in line_clean
        
        if is_c1:
            c1_total += 1
            if is_pass: c1_pass += 1
        elif is_c2:
            c2_total += 1
            if is_pass: c2_pass += 1
        elif is_c3:
            c3_total += 1
            if is_pass: c3_pass += 1
            
        is_ct = any(kw in line_clean for kw in ct_keywords)
        is_sa = any(kw in line_clean for kw in sa_keywords)
        is_st = any(kw in line_clean for kw in st_keywords) or is_c3
        
        if is_ct:
            ct_total += 1
            if is_pass: ct_pass += 1
        if is_sa:
            sa_total += 1
            if is_pass: sa_pass += 1
        if is_st:
            st_total += 1
            if is_pass: st_pass += 1
            
    return {
        'c1': (c1_pass, c1_total),
        'c2': (c2_pass, c2_total),
        'c3': (c3_pass, c3_total),
        'ct': (ct_pass, ct_total),
        'sa': (sa_pass, sa_total),
        'st': (st_pass, st_total)
    }

if os.path.exists(ca_file):
    wb = openpyxl.load_workbook(ca_file, data_only=True)
    sheet = wb.active
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    
    crit_idx = headers.index('Chi tiết tiêu chí')
    name_idx = headers.index('Name')
    
    for r in rows[1:4]:
        name = r[name_idx]
        crit = r[crit_idx]
        print(f"\nName: {name}")
        print("Chi tiết tiêu chí:")
        print(crit)
        print("Analysis:")
        print(analyze_student_criteria_test(crit))
else:
    print("Ca file not found.")

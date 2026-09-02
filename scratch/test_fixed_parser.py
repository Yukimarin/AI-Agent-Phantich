import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ca_files = [
    "inputs/ket-qua-cham-DGNL-ca-thi-7-9.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-12-14.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-14-16.xlsx"
]

def clean_str(val):
    if val is None: return ""
    return str(val).strip()

def analyze_raw_skills_fixed():
    ct_keywords = ['transaction', 'đồng thời', '@transactional', 'giao dịch', 'đồng bộ', 'race condition', 'lock', 'khóa', 'trùng ghế', 'bán vượt']
    sa_keywords = ['path traversal', 'idor', 'client', 'ủy quyền', 'xác thực', 'security', 'bảo mật', 'quyền truy cập', 'giá vé', 'unitprice', 'ticketprice', 'giá sản phẩm', 'đường dẫn']
    st_keywords = ['câu 3', 'câu hỏi định hướng', 'lựa chọn', 'ưu tiên', 'suất chiếu hot', 'khung giờ', 'bấm nút', 'chuyển tiền']
    
    total_lines = 0
    ct_total = 0; ct_pass = 0
    sa_total = 0; sa_pass = 0
    st_total = 0; st_pass = 0
    
    for path in ca_files:
        if not os.path.exists(path): continue
        wb = openpyxl.load_workbook(path, read_only=True)
        sheet = wb.active
        rows = list(sheet.iter_rows(values_only=True))
        headers = rows[0]
        crit_idx = headers.index('Chi tiết tiêu chí')
        
        for r in rows[1:]:
            crit_text = r[crit_idx]
            if not crit_text: continue
            
            lines = crit_text.split('\n')
            for line in lines:
                line_clean = line.strip().lower()
                if not line_clean: continue
                
                total_lines += 1
                
                # Fixed logic: check failure first!
                is_pass = False
                if 'không đạt' in line_clean or 'fail' in line_clean:
                    is_pass = False
                elif 'đạt' in line_clean or 'pass' in line_clean:
                    is_pass = True
                else:
                    is_pass = False
                        
                is_ct = any(kw in line_clean for kw in ct_keywords)
                is_sa = any(kw in line_clean for kw in sa_keywords)
                is_st = any(kw in line_clean for kw in st_keywords)
                
                if is_ct:
                    ct_total += 1
                    if is_pass: ct_pass += 1
                if is_sa:
                    sa_total += 1
                    if is_pass: sa_pass += 1
                if is_st:
                    st_total += 1
                    if is_pass: st_pass += 1
                    
    print("=== RAW CRITERIA STATS (FIXED PARSER) ===")
    print(f"Total criteria lines scanned: {total_lines}")
    print(f"Concurrency/Transactions: total={ct_total}, pass={ct_pass}, pass_rate={ct_pass/ct_total*100:.2f}%" if ct_total > 0 else "No Concurrency lines")
    print(f"Security/Authorization:   total={sa_total}, pass={sa_pass}, pass_rate={sa_pass/sa_total*100:.2f}%" if sa_total > 0 else "No Security lines")
    print(f"System Thinking:          total={st_total}, pass={st_pass}, pass_rate={st_pass/st_total*100:.2f}%" if st_total > 0 else "No System Thinking lines")

if __name__ == "__main__":
    analyze_raw_skills_fixed()

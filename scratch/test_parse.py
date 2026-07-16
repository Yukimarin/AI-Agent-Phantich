import re

with open('data/three_recent_courses_report.md', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\r\n', '\n')

def get_mae(content, batch_name):
    # Match exact line: 👉 **Đánh giá chung khóa KS24-CNTT (Lớp Chính Quy)**: MAE = **9.50%**
    pattern = rf'\*\*Đánh giá chung khóa {batch_name} \(Lớp Chính Quy\)\*\*:\s*MAE\s*=\s*\*\*([\d.]+)%\*\*'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    
    # Fallback non-diacritics
    pattern_alt = rf'\*\*Danh gia chung khoa {batch_name} \(Lop Chinh Quy\)\*\*:\s*MAE\s*=\s*\*\*([\d.]+)%\*\*'
    match = re.search(pattern_alt, content)
    if match:
        return match.group(1)
        
    return "Not Found"

print("KS24 MAE:", get_mae(content, 'KS24-CNTT'))
print("KS25 MAE:", get_mae(content, 'KS25-CNTT'))
print("KS25 QTKD MAE:", get_mae(content, 'KS25-QTKD'))

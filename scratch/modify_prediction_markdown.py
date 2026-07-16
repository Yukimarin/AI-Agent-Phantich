import re

md_path = 'data/three_recent_courses_report.md'

with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings
content = content.replace('\r\n', '\n')

# 1. Insert links for KS24, KS25, and KS25-QTKD inside Section 2
# We search for the evaluation lines and append the link row right under them

# KS24
ks24_target = r'👉 \*\*Đánh giá chung khóa KS24-CNTT\*\*: MAE dự báo môn hiện tại = \*\*0.00%\*\*'
ks24_replacement = (
    "👉 **Đánh giá chung khóa KS24-CNTT**: MAE dự báo môn hiện tại = **0.00%**\n"
    "🔗 **Danh sách chi tiết sinh viên có nguy cơ trượt môn khóa KS24**: Xem tại [Báo cáo chi tiết nguy cơ trượt (student_risk_report.md)](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/student_risk_report.md#lớp-hn-ks24-cntt1-giảng-viên-hồ-xuân-hùng)"
)
content = re.sub(ks24_target, ks24_replacement, content)

# KS25
ks25_target = r'👉 \*\*Đánh giá chung khóa KS25-CNTT\*\*: MAE dự báo môn hiện tại = \*\*0.00%\*\*'
ks25_replacement = (
    "👉 **Đánh giá chung khóa KS25-CNTT**: MAE dự báo môn hiện tại = **0.00%**\n"
    "🔗 **Danh sách chi tiết sinh viên có nguy cơ trượt môn khóa KS25**: Xem tại [Báo cáo chi tiết nguy cơ trượt (student_risk_report.md)](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/student_risk_report.md#lớp-hn-ks25-cntt1-giảng-viên-ẩn-danh)"
)
content = re.sub(ks25_target, ks25_replacement, content)

# QTKD
qtkd_target = r'👉 \*\*Đánh giá chung khóa KS25-QTKD\*\*: MAE dự báo môn hiện tại = \*\*0.00%\*\*'
qtkd_replacement = (
    "👉 **Đánh giá chung khóa KS25-QTKD**: MAE dự báo môn hiện tại = **0.00%**\n"
    "🔗 **Danh sách chi tiết sinh viên có nguy cơ trượt môn khóa KS25 QTKD**: Xem tại [Báo cáo chi tiết nguy cơ trượt (student_risk_report.md)](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/student_risk_report.md#lớp-hn-k25-qtkd1-giảng-viên-ẩn-danh)"
)
content = re.sub(qtkd_target, qtkd_replacement, content)

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Markdown file updated successfully with links to student risk report.")

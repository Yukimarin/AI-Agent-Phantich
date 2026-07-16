with open("scratch/generate_unified_dashboard.py", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.finditer(r'(open|read|1_kpi|2_class|2_student|report_kpi_gv_tg)', content)
for m in matches:
    start_line = content.count('\n', 0, m.start()) + 1
    print(f"Line {start_line}: {m.group(0)}")

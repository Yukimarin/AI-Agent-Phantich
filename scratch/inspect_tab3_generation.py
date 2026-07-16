with open("scratch/generate_unified_dashboard.py", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.finditer(r'tab3_body', content)
for m in matches:
    start_line = content.count('\n', 0, m.start()) + 1
    print(f"Line {start_line}: {content[m.start():m.end()+30].strip()}")

with open("scratch/generate_unified_dashboard.py", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.finditer(r'care_list', content)
with open("scratch/search_care_list.txt", "w", encoding="utf-8") as out:
    for m in matches:
        start_line = content.count('\n', 0, m.start()) + 1
        out.write(f"Line {start_line}: {content[m.start():m.end()+40].strip()}\n")

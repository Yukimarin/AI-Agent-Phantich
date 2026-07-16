with open("output/5_unified_dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = list(re.finditer(r'id="tab-daily-logs-container"', content))
if matches:
    m = matches[0]
    # find line number
    line_no = content.count('\n', 0, m.start()) + 1
    print(f"Match found at line {line_no}")
    
    # print lines around it
    lines = content.split('\n')
    with open("scratch/merged_tab3_div.txt", "w", encoding="utf-8") as out:
        for idx in range(max(0, line_no - 10), min(len(lines), line_no + 15)):
            out.write(f"{idx+1}: {lines[idx]}\n")
else:
    print("Match NOT found")

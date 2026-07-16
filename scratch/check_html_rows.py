with open("unified_dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.findall(r'<tr class="log-row[^"]*"[^>]*>(.*?)</tr>', content, re.DOTALL)
print(f"Found {len(matches)} log rows in output/5_unified_dashboard.html!")
if matches:
    # Print first row content
    print("First row content:", matches[0].strip().replace('\n', ' '))

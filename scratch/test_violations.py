import json
import os
import sys
from collections import defaultdict

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

violations_path = r"data/vi_pham_gvtg.json"

if not os.path.exists(violations_path):
    print("Violations file not found!")
    sys.exit(1)

with open(violations_path, "r", encoding="utf-8") as f:
    violations = json.load(f)

print(f"Total violations in file: {len(violations)}")

counts = defaultdict(int)
error_types = defaultdict(list)

for v in violations:
    name = v.get("Instructor")
    err = v.get("Error")
    date = v.get("Date")
    cls = v.get("Class")
    details = v.get("Details")
    counts[name] += 1
    error_types[name].append((err, date, cls, details))

# Print sorted summary
print("\n=== Summary of Violations per Instructor ===")
for name, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{name}: {count} violations")
    # Print first few violations
    for err, date, cls, details in error_types[name][:5]:
         print(f"  - [{date}] {cls} | {err}: {details[:60]}...")
    if len(error_types[name]) > 5:
         print(f"  ... and {len(error_types[name]) - 5} more")

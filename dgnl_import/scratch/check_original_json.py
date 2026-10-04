import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

file_path = "scratch/ks24_stats.json"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("=== ORIGINAL KS24 STATS JSON SUMMARY ===")
    print(json.dumps(data['summary'], indent=2, ensure_ascii=False))
else:
    print("Original stats JSON not found.")

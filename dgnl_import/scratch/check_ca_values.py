import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ks24_stats.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    
ca_values = set(s['ca_thi'] for s in data['students'])
print("Unique ca_thi values in JSON:", ca_values)

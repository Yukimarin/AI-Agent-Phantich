with open("scratch/generate_unified_dashboard.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "normalize_name" in line:
        print(f"Line {idx+1}: {line.strip()}")

with open("output/5_unified_dashboard.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("scratch/find_placeholder_lines.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(lines):
        for ph in ['{curr}', '{prev}', '{reasons}']:
            if ph in line:
                out.write(f"Line {idx+1}: {line.strip()}\n")

with open("scratch/generate_unified_dashboard.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("scratch/tab3_render_code.txt", "w", encoding="utf-8") as out:
    for idx in range(290, 485):
        if idx < len(lines):
            out.write(f"{idx+1}: {lines[idx]}")
print("Wrote to scratch/tab3_render_code.txt")

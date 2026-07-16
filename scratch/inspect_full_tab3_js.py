with open("output/5_unified_dashboard.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("scratch/full_tab3_js.txt", "w", encoding="utf-8") as out:
    for idx in range(7840, len(lines)):
        out.write(f"{idx+1}: {lines[idx]}")
print("Wrote to scratch/full_tab3_js.txt")

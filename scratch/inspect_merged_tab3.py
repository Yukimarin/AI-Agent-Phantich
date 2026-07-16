with open("output/5_unified_dashboard.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("scratch/merged_tab3_output.txt", "w", encoding="utf-8") as out:
    for idx in range(7700, 7850):
        if idx < len(lines):
            out.write(f"{idx+1}: {lines[idx]}")
print("Wrote to scratch/merged_tab3_output.txt")

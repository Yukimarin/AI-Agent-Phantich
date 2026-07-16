import json

with open("data/daily_log_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

weekly_stats = data.get("weekly_stats", {})
monthly_stats = data.get("monthly_stats", {})

print(f"Weekly stats keys count: {len(weekly_stats)}")
with open("scratch/weekly_keys.txt", "w", encoding="utf-8") as out:
    out.write(f"Weekly stats keys count: {len(weekly_stats)}\n")
    out.write("Sample weekly keys: " + str(list(weekly_stats.keys())[:10]) + "\n")
    out.write(f"Monthly stats keys count: {len(monthly_stats)}\n")
    out.write("Sample monthly keys: " + str(list(monthly_stats.keys())[:10]) + "\n")

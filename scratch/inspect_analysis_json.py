import json

with open("data/daily_log_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Dates weekly:", data.get("dates_weekly"))
print("Dates monthly:", data.get("dates_monthly"))
print("Yesterday:", data.get("yesterday"))

weekly_stats = data.get("weekly_stats", {})
monthly_stats = data.get("monthly_stats", {})

print("\nNumber of weekly stats:", len(weekly_stats))
print("Number of monthly stats:", len(monthly_stats))

print("\nSome weekly stats keys:")
print(list(weekly_stats.keys())[:5])

print("\nSome monthly stats keys:")
print(list(monthly_stats.keys())[:5])

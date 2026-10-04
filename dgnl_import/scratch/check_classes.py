import json

with open("scratch/standardized_master_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Raw KS24 count:", len(data["ks24"]))
print("Raw KS25 count:", len(data["ks25"]))
print("Raw QTKD count:", len(data["qtkd"]))

# Check unique classes in raw KS25
ks25_classes = set(s["class"] for s in data["ks25"])
print("\nUnique classes in KS25 raw:", sorted(list(ks25_classes)))


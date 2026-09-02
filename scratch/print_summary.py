import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/optimized_dgnl_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    
stats = data['ks24_stats']
print("=== KS24 CNTT OVERVIEW ===")
for group in ['all', 'hn', 'hcm']:
    print(f"\nGroup: {group.upper()}")
    gstats = stats[group]
    print(f"  Total registered: {gstats['total_registered']}")
    print(f"  Took exam (score > 0): {gstats['total_took_exam']}")
    print(f"  Avg Score (overall): {gstats['avg_score']}")
    print(f"  Avg Score (among test takers): {gstats['avg_score_valid']}")
    print(f"  Avg Practical (Essay): {gstats['avg_prac']}")
    print(f"  Avg MCQ: {gstats['avg_mcq']}")
    print(f"  Avg Vấn đáp: {gstats['avg_oral']}")
    print(f"  Avg Sản phẩm: {gstats['avg_prod']}")
    print(f"  Placement Rate: {gstats['placement_rate']}%")
    print(f"  Readiness Levels: {gstats['levels']}")
    print(f"  Avg Skills: {gstats['avg_skills']}")

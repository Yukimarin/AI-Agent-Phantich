import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

html_path = "outputs/KS24_DGNL_Report.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    print("=== HTML FILE INSPECTION ===")
    # Search for skills array or config
    skill_matches = re.findall(r'avgSkills\s*=\s*({[^}]+})', html)
    if skill_matches:
        print("avgSkills found:")
        print(skill_matches[0])
        
    # Search for placement rate or other text
    rate_matches = re.findall(r'Tỷ lệ Sẵn sàng.*?(\d+\.?\d*%)', html)
    if rate_matches:
        print("Placement Rate in HTML:", rate_matches)
        
    # Let's print out JS variables or chart datasets
    chart_matches = re.findall(r'data:\s*\[([\d.,\s]+)\]', html)
    print("\nChart Data arrays found:")
    for idx, cm in enumerate(chart_matches):
        print(f"Chart {idx}: {cm.strip()}")
else:
    print("HTML report not found.")

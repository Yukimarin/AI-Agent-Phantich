import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Desktop\Education-DB-Analytic\scratch\generate_prd_compliant_reports.py"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if "gpa" in line.lower():
                print(f"{i+1}: {line.strip()[:120]}")

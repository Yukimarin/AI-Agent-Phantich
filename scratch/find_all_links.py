import os
import re

base_dir = "c:\\Users\\DELL\\Desktop\\AI-Agent\\AI_PhantichchisoDT"
md_files = []

for root, dirs, files in os.walk(base_dir):
    if any(p in root for p in [".git", ".gemini", ".venv", "__pycache__"]):
        continue
    for file in files:
        if file.endswith(".md"):
            md_files.append(os.path.join(root, file))

print(f"Scanning {len(md_files)} markdown files...")

link_pattern = re.compile(r"\[\[(.*?)\]\]")

found_issues = False
for filepath in md_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    matches = link_pattern.findall(content)
    for match in matches:
        # Split display name if present
        link_target = match.split("|")[0].strip()
        link_target_lower = link_target.lower()
        
        if "knowledge_map" in link_target_lower or "untitled" in link_target_lower or not link_target:
            found_issues = True
            print(f"File: {os.path.relpath(filepath, base_dir)}")
            print(f"  -> Found suspicious link: [[{match}]]")

if not found_issues:
    print("No suspicious links containing 'knowledge_map' or 'Untitled' were found.")

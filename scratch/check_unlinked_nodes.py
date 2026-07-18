import os
import re

base_dir = "c:\\Users\\DELL\\Desktop\\AI-Agent\\AI_PhantichchisoDT"
docs_dir = os.path.join(base_dir, "docs")
moc_path = os.path.join(docs_dir, "Bản đồ Tri thức MOC.md")

if not os.path.exists(moc_path):
    print("MOC file not found.")
    exit(0)

# 1. Read MOC and extract all existing wikilinks
with open(moc_path, "r", encoding="utf-8") as f:
    moc_content = f.read()

# Extract links: [[link_target]] or [[link_target|display]]
link_pattern = re.compile(r"\[\[(.*?)\]\]")
existing_links = set()
for match in link_pattern.findall(moc_content):
    target = match.split("|")[0].split("#")[0].strip()
    # Normalize paths: replace backward slash with forward, remove leading "./" or "docs/"
    target_norm = target.replace("\\", "/").lower()
    if target_norm.startswith("docs/"):
        target_norm = target_norm[5:]
    existing_links.add(target_norm)

# Add standard proxy notes manually since they are in MOC
proxy_names_lower = [
    "báo cáo nguy cơ học viên",
    "báo cáo kpi giảng viên trợ giảng",
    "đánh giá hiệu năng mô hình",
    "chi tiết vi phạm tác nghiệp",
    "báo cáo xếp loại năng lực gv-tg"
]
for p in proxy_names_lower:
    existing_links.add(p)

print(f"Found {len(existing_links)} existing links in MOC.")

# 2. Scan all markdown files in docs/ (and subdirectories)
all_docs_files = []
for root, dirs, files in os.walk(docs_dir):
    # Skip .git, etc.
    if any(p in root for p in [".git", ".gemini", ".venv", "__pycache__"]):
        continue
    for file in files:
        if file.endswith(".md"):
            # Get path relative to docs_dir
            rel_path = os.path.relpath(os.path.join(root, file), docs_dir)
            rel_path_norm = rel_path.replace("\\", "/").lower()
            # Strip ".md" extension for link matching
            if rel_path_norm.endswith(".md"):
                rel_path_norm = rel_path_norm[:-3]
            
            # Skip MOC itself
            if rel_path_norm == "bản đồ tri thức moc":
                continue
                
            all_docs_files.append((rel_path, rel_path_norm))

print(f"Found {len(all_docs_files)} markdown files in docs/.")

# 3. Find unlinked files
unlinked_files = []
for rel_path, rel_path_norm in all_docs_files:
    if rel_path_norm not in existing_links:
        unlinked_files.append(rel_path)

if unlinked_files:
    print(f"Found {len(unlinked_files)} unlinked notes:")
    for uf in unlinked_files:
        print(f"  - {uf}")
        
    # Append unlinked notes to the MOC file
    append_str = "\n\n---\n\n## 6. Ghi chú & Kế hoạch chưa phân loại (Tự động liên kết)\n"
    for uf in unlinked_files:
        # Format links cleanly
        # e.g., plans/Plan - 2026-07-15 Automate Agent 4.md -> [[plans/Plan - 2026-07-15 Automate Agent 4|Plan - 2026-07-15 Automate Agent 4]]
        target_link = uf.replace(".md", "").replace("\\", "/")
        display_name = os.path.basename(uf).replace(".md", "")
        append_str += f"*   [[{target_link}|{display_name}]]\n"
        
    # Check if section already exists in MOC
    if "## 6. Ghi chú & Kế hoạch chưa phân loại" in moc_content:
        # Replace existing section
        pattern_sec = r"## 6\. Ghi chú & Kế hoạch chưa phân loại.*"
        moc_content_new = re.sub(pattern_sec, append_str.strip(), moc_content, flags=re.DOTALL)
    else:
        moc_content_new = moc_content.rstrip() + append_str
        
    with open(moc_path, "w", encoding="utf-8") as f:
        f.write(moc_content_new)
    print("MOC file updated with unlinked notes successfully!")
else:
    print("All docs/ markdown files are already linked in the MOC!")

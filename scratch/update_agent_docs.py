import os
import re

base_dir = "c:\\Users\\DELL\\Desktop\\AI-Agent\\AI_PhantichchisoDT"
docs_dir = os.path.join(base_dir, "docs")
agents_dir = os.path.join(docs_dir, "agents")
moc_path = os.path.join(docs_dir, "Bản đồ Tri thức MOC.md")

# 1. Create Báo cáo Nhật ký Công việc.md
print("1. Creating daily logs proxy note...")
logs_proxy_path = os.path.join(docs_dir, "Báo cáo Nhật ký Công việc.md")
with open(logs_proxy_path, "w", encoding="utf-8") as f:
    f.write("""---
title: Báo cáo Nhật ký Công việc
tags:
  - report/logs
---
# Báo cáo Nhật ký Công việc Daily Logs

![[../output/4_daily_logs_report.md]]
""")
print(f"Created proxy note: {logs_proxy_path}")

# 2. Add to MOC under "## 3. Báo cáo Nghiệp vụ Hiện tại"
print("\n2. Updating MOC with daily logs report link...")
if os.path.exists(moc_path):
    with open(moc_path, "r", encoding="utf-8") as f:
        moc_content = f.read()
        
    target_pattern = "*   [[Báo cáo KPI Giảng viên Trợ giảng|Báo cáo KPI GV/TG]]:"
    new_link = "*   [[Báo cáo Nhật ký Công việc|Báo cáo Nhật ký Công việc]]: Báo cáo nhật ký công việc ngày và giờ khai báo định mức.\n"
    
    if "[[Báo cáo Nhật ký Công việc" not in moc_content:
        moc_content = moc_content.replace(target_pattern, new_link + target_pattern)
        with open(moc_path, "w", encoding="utf-8") as f:
            f.write(moc_content)
        print("Updated MOC successfully.")
    else:
        print("MOC already contains link to Daily Logs.")

# 3. Update all 5 Agent docs to embed real results
agent_embeds = {
    "Agent 1 - Violation Analyst.md": [
        "## 6. Kết quả Phân tích Thực tế Mới nhất (Latest Actionable Insights)\n"
        "> [!tip] Kết quả kiểm toán kỷ luật\n"
        "> Dưới đây là báo cáo nguy cơ học viên và tỷ lệ vi phạm của từng lớp học.\n\n"
        "![[Báo cáo Nguy cơ Học viên]]"
    ],
    "Agent 2 - Academic Predictor.md": [
        "## 6. Kết quả Phân tích Thực tế Mới nhất (Latest Actionable Insights)\n"
        "> [!tip] Kết quả dự báo học lực & Hiệu năng mô hình\n"
        "> Dưới đây là cảnh báo nguy cơ trượt của học viên và đánh giá hiệu năng mô hình.\n\n"
        "![[Báo cáo Nguy cơ Học viên]]\n\n"
        "![[Đánh giá Hiệu năng Mô hình]]"
    ],
    "Agent 3 - Task Aggregator.md": [
        "## 6. Kết quả Phân tích Thực tế Mới nhất (Latest Actionable Insights)\n"
        "> [!tip] Lịch sử vi phạm tác nghiệp GV/TG\n"
        "> Dưới đây là danh sách chi tiết các ca vi phạm tác nghiệp thực tế của GV/TG.\n\n"
        "![[Chi tiết Vi phạm Tác nghiệp]]"
    ],
    "Agent 4 - Daily Log Auditor.md": [
        "## 6. Kết quả Phân tích Thực tế Mới nhất (Latest Actionable Insights)\n"
        "> [!tip] Phân tích báo cáo ngày & Định mức công việc\n"
        "> Dưới đây là báo cáo tiến độ nộp logs và các trường hợp khai báo vượt định mức.\n\n"
        "![[Báo cáo Nhật ký Công việc]]"
    ],
    "Agent Lead - Master Evaluator.md": [
        "## 6. Kết quả Phân tích Thực tế Mới nhất (Latest Actionable Insights)\n"
        "> [!tip] Báo cáo đánh giá KPI GV/TG tổng hợp học kỳ\n"
        "> Dưới đây là kết quả xếp loại và điểm KPI tổng của từng phòng ban.\n\n"
        "![[Báo cáo KPI Giảng viên Trợ giảng]]"
    ]
}

print("\n3. Injecting embeddings block into agent docs...")
for agent_file, embed_lines in agent_embeds.items():
    agent_path = os.path.join(agents_dir, agent_file)
    if os.path.exists(agent_path):
        with open(agent_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # We will insert the block before the line "Trở về: [[Bản đồ Tri thức MOC|...]]"
        return_pattern = "Trở về: [[Bản đồ Tri thức MOC"
        
        # Check if already has Section 6 to prevent duplicate insertion
        if "## 6. Kết quả Phân tích Thực tế Mới nhất" not in content:
            # Let's locate the return pattern and insert before it
            idx = content.find(return_pattern)
            if idx != -1:
                # Find the beginning of the line containing return_pattern
                # usually it's preceded by a separator like "\n---\n" or similar
                # Let's see: we can insert it right before the separator or before return_pattern
                separator_idx = content.rfind("\n---\n", 0, idx)
                if separator_idx != -1:
                    insert_idx = separator_idx
                else:
                    insert_idx = idx
                
                new_content = content[:insert_idx] + "\n\n---\n\n" + embed_lines[0] + content[insert_idx:]
                with open(agent_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Injected results into: {agent_file}")
            else:
                # If return pattern not found, just append at the end
                new_content = content.rstrip() + "\n\n---\n\n" + embed_lines[0]
                with open(agent_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Appended results into: {agent_file}")
        else:
            print(f"Already updated results in: {agent_file}")
            
print("\nAgent documentation update completed successfully!")

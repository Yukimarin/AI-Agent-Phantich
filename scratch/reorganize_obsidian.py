import os
import re
import shutil

# Root of workspace
base_dir = "c:\\Users\\DELL\\Desktop\\AI-Agent\\AI_PhantichchisoDT"
docs_dir = os.path.join(base_dir, "docs")
agents_dir = os.path.join(docs_dir, "agents")
plans_dir = os.path.join(docs_dir, "plans")

# Define file renaming map (physical path on disk)
renaming_map = {
    # root docs
    os.path.join(docs_dir, "knowledge_map.md"): os.path.join(docs_dir, "Bản đồ Tri thức MOC.md"),
    os.path.join(docs_dir, "super_memory.md"): os.path.join(docs_dir, "Super Memory.md"),
    os.path.join(docs_dir, "ghi_nhan_hieu_chuan.md"): os.path.join(docs_dir, "Model Calibration Notes.md"),
    os.path.join(docs_dir, "HOW_TO_USE_OBSIDIAN.md"): os.path.join(docs_dir, "Hướng dẫn sử dụng Obsidian.md"),
    os.path.join(docs_dir, "MULTI_AGENT_WORKFLOW.md"): os.path.join(docs_dir, "Quy trình Multi-Agent Workflow.md"),
    
    # agents
    os.path.join(agents_dir, "agent_lead_master_evaluator.md"): os.path.join(agents_dir, "Agent Lead - Master Evaluator.md"),
    os.path.join(agents_dir, "agent_1_violation_analyst.md"): os.path.join(agents_dir, "Agent 1 - Violation Analyst.md"),
    os.path.join(agents_dir, "agent_2_academic_predictor.md"): os.path.join(agents_dir, "Agent 2 - Academic Predictor.md"),
    os.path.join(agents_dir, "agent_3_task_aggregator.md"): os.path.join(agents_dir, "Agent 3 - Task Aggregator.md"),
    os.path.join(agents_dir, "agent_4_daily_log_auditor.md"): os.path.join(agents_dir, "Agent 4 - Daily Log Auditor.md"),
    
    # plans
    os.path.join(plans_dir, "2026-06-29-academic-prediction-design.md"): os.path.join(plans_dir, "Plan - 2026-06-29 Academic Prediction Design.md"),
    os.path.join(plans_dir, "2026-06-30-redesign-prediction-report-interface.md"): os.path.join(plans_dir, "Plan - 2026-06-30 Redesign Prediction Report Interface.md"),
    os.path.join(plans_dir, "2026-07-02-consecutive-absence-refinement-design.md"): os.path.join(plans_dir, "Plan - 2026-07-02 Consecutive Absence Refinement Design.md"),
    os.path.join(plans_dir, "2026-07-02-consecutive-absence-refinement-implementation.md"): os.path.join(plans_dir, "Plan - 2026-07-02 Consecutive Absence Refinement Implementation.md"),
    os.path.join(plans_dir, "2026-07-02-prediction-risk-refinement-design.md"): os.path.join(plans_dir, "Plan - 2026-07-02 Prediction Risk Refinement Design.md"),
    os.path.join(plans_dir, "2026-07-02-prediction-risk-refinement-implementation.md"): os.path.join(plans_dir, "Plan - 2026-07-02 Prediction Risk Refinement Implementation.md"),
    os.path.join(plans_dir, "2026-07-09-model-calibration-kpi-design.md"): os.path.join(plans_dir, "Plan - 2026-07-09 Model Calibration KPI Design.md"),
    os.path.join(plans_dir, "2026-07-09-model-calibration-kpi.md"): os.path.join(plans_dir, "Plan - 2026-07-09 Model Calibration KPI.md"),
    os.path.join(plans_dir, "2026-07-09-unified-dashboard-premium-design.md"): os.path.join(plans_dir, "Plan - 2026-07-09 Unified Dashboard Premium Design.md"),
    os.path.join(plans_dir, "2026-07-10-unified-dashboard-interactive-filters.md"): os.path.join(plans_dir, "Plan - 2026-07-10 Unified Dashboard Interactive Filters.md"),
    os.path.join(plans_dir, "2026-07-13-daily-logs-integrated-report-design.md"): os.path.join(plans_dir, "Plan - 2026-07-13 Daily Logs Integrated Report Design.md"),
    os.path.join(plans_dir, "2026-07-13-daily-logs-integrated-report-plan.md"): os.path.join(plans_dir, "Plan - 2026-07-13 Daily Logs Integrated Report Plan.md"),
    os.path.join(plans_dir, "2026-07-13-daily-logs-kpi-matching-design.md"): os.path.join(plans_dir, "Plan - 2026-07-13 Daily Logs KPI Matching Design.md"),
    os.path.join(plans_dir, "2026-07-13-daily-logs-kpi-matching.md"): os.path.join(plans_dir, "Plan - 2026-07-13 Daily Logs KPI Matching.md"),
    os.path.join(plans_dir, "2026-07-15-agent4-dashboard-integration-design.md"): os.path.join(plans_dir, "Plan - 2026-07-15 Agent 4 Dashboard Integration Design.md"),
    os.path.join(plans_dir, "2026-07-15-agent4-dashboard-integration-plan.md"): os.path.join(plans_dir, "Plan - 2026-07-15 Agent 4 Dashboard Integration Plan.md"),
    os.path.join(plans_dir, "2026-07-15-automate-agent4-daily-logs.md"): os.path.join(plans_dir, "Plan - 2026-07-15 Automate Agent 4 Daily Logs.md"),
    os.path.join(plans_dir, "2026-07-17-auto-update-kpi-design.md"): os.path.join(plans_dir, "Plan - 2026-07-17 Auto Update KPI Design.md"),
}

# Define Wikilink string replacements mapping (from old target string to new target string)
wikilink_replacements = {
    # Root docs links
    "docs/knowledge_map": "Bản đồ Tri thức MOC",
    "docs/super_memory": "Super Memory",
    "docs/ghi_nhan_hieu_chuan": "Model Calibration Notes",
    "docs/HOW_TO_USE_OBSIDIAN": "Hướng dẫn sử dụng Obsidian",
    "docs/MULTI_AGENT_WORKFLOW": "Quy trình Multi-Agent Workflow",
    
    # Agent links
    "docs/agents/agent_lead_master_evaluator": "agents/Agent Lead - Master Evaluator",
    "docs/agents/agent_1_violation_analyst": "agents/Agent 1 - Violation Analyst",
    "docs/agents/agent_2_academic_predictor": "agents/Agent 2 - Academic Predictor",
    "docs/agents/agent_3_task_aggregator": "agents/Agent 3 - Task Aggregator",
    "docs/agents/agent_4_daily_log_auditor": "agents/Agent 4 - Daily Log Auditor",
    
    # Plans links
    "docs/plans/2026-06-29-academic-prediction-design": "plans/Plan - 2026-06-29 Academic Prediction Design",
    "docs/plans/2026-06-30-redesign-prediction-report-interface": "plans/Plan - 2026-06-30 Redesign Prediction Report Interface",
    "docs/plans/2026-07-02-consecutive-absence-refinement-design": "plans/Plan - 2026-07-02 Consecutive Absence Refinement Design",
    "docs/plans/2026-07-02-consecutive-absence-refinement-implementation": "plans/Plan - 2026-07-02 Consecutive Absence Refinement Implementation",
    "docs/plans/2026-07-02-prediction-risk-refinement-design": "plans/Plan - 2026-07-02 Prediction Risk Refinement Design",
    "docs/plans/2026-07-02-prediction-risk-refinement-implementation": "plans/Plan - 2026-07-02 Prediction Risk Refinement Implementation",
    "docs/plans/2026-07-09-model-calibration-kpi-design": "plans/Plan - 2026-07-09 Model Calibration KPI Design",
    "docs/plans/2026-07-09-model-calibration-kpi": "plans/Plan - 2026-07-09 Model Calibration KPI",
    "docs/plans/2026-07-09-unified-dashboard-premium-design": "plans/Plan - 2026-07-09 Unified Dashboard Premium Design",
    "docs/plans/2026-07-10-unified-dashboard-interactive-filters": "plans/Plan - 2026-07-10 Unified Dashboard Interactive Filters",
    "docs/plans/2026-07-13-daily-logs-integrated-report-design": "plans/Plan - 2026-07-13 Daily Logs Integrated Report Design",
    "docs/plans/2026-07-13-daily-logs-integrated-report-plan": "plans/Plan - 2026-07-13 Daily Logs Integrated Report Plan",
    "docs/plans/2026-07-13-daily-logs-kpi-matching-design": "plans/Plan - 2026-07-13 Daily Logs KPI Matching Design",
    "docs/plans/2026-07-13-daily-logs-kpi-matching": "plans/Plan - 2026-07-13 Daily Logs KPI Matching",
    "docs/plans/2026-07-15-agent4-dashboard-integration-design": "plans/Plan - 2026-07-15 Agent 4 Dashboard Integration Design",
    "docs/plans/2026-07-15-agent4-dashboard-integration-plan": "plans/Plan - 2026-07-15 Agent 4 Dashboard Integration Plan",
    "docs/plans/2026-07-15-automate-agent4-daily-logs": "plans/Plan - 2026-07-15 Automate Agent 4 Daily Logs",
    "docs/plans/2026-07-17-auto-update-kpi-design": "plans/Plan - 2026-07-17 Auto Update KPI Design",

    # Raw reports redirects (Map old path directly to new proxy nodes in docs folder)
    "data/student_risk_report": "Báo cáo Nguy cơ Học viên",
    "data/report_kpi_gv_tg": "Báo cáo KPI Giảng viên Trợ giảng",
    "data/evaluation_metrics": "Đánh giá Hiệu năng Mô hình",
    "data/vi_pham_gvtg_khoa_ks25": "Chi tiết Vi phạm Tác nghiệp",
    "output/kpi_classification_report": "Báo cáo Xếp loại Năng lực GV-TG",
}

# 1. Create Proxy Notes in docs folder to embed raw files
proxy_notes = {
    "Báo cáo Nguy cơ Học viên.md": "../data/student_risk_report.md",
    "Báo cáo KPI Giảng viên Trợ giảng.md": "../data/report_kpi_gv_tg.md",
    "Đánh giá Hiệu năng Mô hình.md": "../data/evaluation_metrics.md",
    "Chi tiết Vi phạm Tác nghiệp.md": "../data/vi_pham_gvtg_khoa_ks25.md",
    "Báo cáo Xếp loại Năng lực GV-TG.md": "../output/kpi_classification_report.md"
}

print("1. Creating Proxy Notes in docs folder...")
for note_name, raw_rel_path in proxy_notes.items():
    note_path = os.path.join(docs_dir, note_name)
    title = note_name.replace(".md", "")
    
    # We will determine tags based on the report type
    tag = "report/academic"
    if "KPI" in title:
        tag = "report/kpi"
    elif "Hiệu năng" in title:
        tag = "report/evaluation"
    elif "Vi phạm" in title:
        tag = "report/compliance"
    elif "Xếp loại" in title:
        tag = "report/classification"
        
    content = f"""---
title: {title}
tags:
  - {tag}
---
# {title}

![[{raw_rel_path}]]
"""
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created proxy note: {note_path}")

# 2. Perform file renaming on disk
print("\n2. Renaming files on disk...")
for old_path, new_path in renaming_map.items():
    if os.path.exists(old_path):
        # Rename file
        shutil.move(old_path, new_path)
        print(f"Renamed: {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
    else:
        print(f"Skip (does not exist): {os.path.basename(old_path)}")

# 3. Recursively update all wikilinks in all markdown files in the workspace
print("\n3. Scanning and updating wikilinks in all .md files...")

# Find all markdown files in workspace
md_files = []
for root, dirs, files in os.walk(base_dir):
    # Skip .git, .gemini, and virtual env folders
    if any(p in root for p in [".git", ".gemini", ".venv", "__pycache__"]):
        continue
    for file in files:
        if file.endswith(".md"):
            md_files.append(os.path.join(root, file))

for filepath in md_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    # Replace links based on mapping
    for old_link, new_link in wikilink_replacements.items():
        # Wikilink pattern: [[old_link]] or [[old_link|display]]
        # We need to replace occurrences of [[old_link with [[new_link
        # For example, [[docs/super_memory|text]] -> [[Super Memory|text]]
        old_pattern1 = f"[[{old_link}|"
        new_pattern1 = f"[[{new_link}|"
        old_pattern2 = f"[[{old_link}]]"
        new_pattern2 = f"[[{new_link}]]"
        old_pattern3 = f"[[{old_link}#"
        new_pattern3 = f"[[{new_link}#"
        
        if old_pattern1 in content:
            content = content.replace(old_pattern1, new_pattern1)
            modified = True
        if old_pattern2 in content:
            content = content.replace(old_pattern2, new_pattern2)
            modified = True
        if old_pattern3 in content:
            content = content.replace(old_pattern3, new_pattern3)
            modified = True
            
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated links in: {os.path.relpath(filepath, base_dir)}")

print("\nObsidian reorganization completed successfully!")

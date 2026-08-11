import os
import shutil

# 1. Define target directories
dirs = [
    "agents/core",
    "agents/advanced/academic_insights",
    "agents/advanced/management_audit",
    "agents/master",
    "agents/common",
    "scripts",
    "scratch"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"Directory created/verified: {d}")

# 2. Define directory moves
dir_moves = [
    ("agents/agent_1_class_kpi", "agents/core/agent_1_class_kpi"),
    ("agents/agent_2_academic_pred", "agents/core/agent_2_academic_pred"),
    ("agents/agent_3_ops_discipline", "agents/core/agent_3_ops_discipline"),
    ("agents/agent_4_daily_logs", "agents/core/agent_4_daily_logs"),
    ("agents/agent_5_master_portal", "agents/master/agent_5_master_portal"),
]

for src, dst in dir_moves:
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.move(src, dst)
        print(f"Moved directory {src} -> {dst}")

# 3. Define file moves
file_moves = [
    ("agents/data_sanitizer.py", "agents/common/data_sanitizer.py"),
    ("agents/llmwiki.py", "agents/common/llmwiki.py"),
    ("agents/validator.py", "agents/common/validator.py"),
    ("custom_reports/generate_report_director.py", "agents/advanced/management_audit/generate_report_director.py"),
    ("custom_reports/generate_qldt_report.py", "agents/advanced/management_audit/generate_qldt_report.py"),
    ("custom_reports/sync_director.ps1", "scripts/sync_director.ps1"),
    ("scratch_convert.js", "scratch/scratch_convert.js"),
    ("scratch_convert_qtkd.js", "scratch/scratch_convert_qtkd.js"),
    ("scratch_kpi.json", "scratch/scratch_kpi.json"),
    ("scratch_kpi_extract.js", "scratch/scratch_kpi_extract.js"),
    ("scratch_update_ranks.js", "scratch/scratch_update_ranks.js")
]

for src, dst in file_moves:
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        print(f"Moved file {src} -> {dst}")

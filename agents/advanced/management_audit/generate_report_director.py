# -*- coding: utf-8 -*-
import json
import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

project_issues_path = "data/processed/project_issues_worklane.json"
daily_log_analysis_path = "data/processed/daily_log_analysis.json"
output_html_path = "output/dashboards/advanced/director_cockpit.html"
output_md_path = "output/reports/advanced/director_cockpit.md"

def strip_accents(text):
    import unicodedata
    if not text:
        return ""
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode("utf-8")
    return text.strip().lower()

def main():
    try:
        with open(daily_log_analysis_path, "r", encoding="utf-8") as f:
            daily_data = json.load(f)
    except Exception as e:
        print(f"Lỗi đọc daily_log_analysis.json: {e}")
        return

    try:
        with open(project_issues_path, "r", encoding="utf-8") as f:
            project_data = json.load(f)
    except Exception as e:
        print(f"Lỗi đọc project_issues_worklane.json: {e}")
        return

    raw_reports = daily_data.get('raw_reports', {})
    weekly_stats = daily_data.get('weekly_stats', {})
    monthly_stats = daily_data.get('monthly_stats', {})
    dates_weekly = daily_data.get('dates_weekly', [])
    dates_monthly = daily_data.get('dates_monthly', [])
    yesterday = daily_data.get('yesterday', "")
    
    # Process project issues
    if 'projects' in project_data:
        projects_raw = project_data['projects']
        if isinstance(projects_raw, dict):
            projects_raw = [{"key": k, **v} for k, v in projects_raw.items()]
    else:
        projects_raw = [{"key": k, **v} for k, v in project_data.items()]
        
    projects_list = []
    
    for p in projects_raw:
        info = p.get('project_info', {})
        key = info.get('key', 'Unknown')
        name = info.get('name', 'Unknown')
        
        # Rule 1: Loại bỏ Dự án Giảng dạy / Triển khai môn
        name_lower = p.get('project_info', {}).get('name', '').lower()
        if 'giảng dạy' in name_lower or 'triển khai môn' in name_lower:
            continue
            
        status = info.get('status', 'ACTIVE').upper()
        health = info.get('health', 'ON_TRACK').upper()
        pic_dict = info.get('pic') or {}
        pic_name = pic_dict.get('name', 'Unknown')
        
        issues = p.get('issues', {}).get('issues', [])
        
        filtered_issues = []
        members_set = set()
        
        if pic_name and pic_name != 'Unknown':
            members_set.add(pic_name)
            
        for iss in issues:
            state = str(iss.get('state', '')).lower().strip()
            if state in ['hủy', 'huy', 'cancel', 'cancelled']:
                continue
                
            filtered_issues.append({
                "code": iss.get("code"),
                "title": iss.get("title"),
                "state": iss.get("state"),
                "assignee": iss.get("assignee"),
                "dueDate": iss.get("dueDate")
            })
            
            assignee = iss.get('assignee')
            if assignee:
                members_set.add(assignee)
                
        projects_list.append({
            "key": key,
            "name": name,
            "pic": pic_name,
            "status": status,
            "health": health,
            "members": sorted(list(members_set)),
            "issues": filtered_issues
        })

    # Calculate daily snapshot
    hist_path = "data/processed/historical_kpi.json"
    historical_kpi = {}
    import os
    if os.path.exists(hist_path):
        try:
            with open(hist_path, "r", encoding="utf-8") as f:
                historical_kpi = json.load(f)
        except Exception:
            pass

    current_snapshot = {}
    for p in projects_list:
        pic = p.get("pic", "")
        proj_name = f"{p.get('key')} - {p.get('name')}"
        for iss in p["issues"]:
            due = iss.get("dueDate")
            state = iss.get("state", "").lower()
            if due and due[:10] <= yesterday and state not in ["hoàn thành", "done", "completed"]:
                assignee = iss.get("assignee")
                
                if state == "chờ duyệt":
                    fault_person = pic
                    fault_type = "review_faults"
                    fault_desc = "Chậm duyệt bài (Chờ duyệt)"
                else:
                    fault_person = assignee
                    fault_type = "execution_faults"
                    fault_desc = "Thi công chậm (Cần làm/Đang làm)"
                
                if fault_person and fault_person != "Unknown":
                    if fault_person not in current_snapshot:
                        current_snapshot[fault_person] = {"execution_faults": {}, "review_faults": {}}
                    
                    if proj_name not in current_snapshot[fault_person][fault_type]:
                        current_snapshot[fault_person][fault_type][proj_name] = {"count": 0, "type": fault_desc}
                        
                    current_snapshot[fault_person][fault_type][proj_name]["count"] += 1

    historical_kpi[yesterday] = current_snapshot
    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump(historical_kpi, f, ensure_ascii=False, indent=2)

    # Prepare Personnel basic meta data
    personnel_list = {}
    group_map = {}
    
    # 0. Load explicit ranks and roles from md
    staff_rank_map = {}
    rank_file_path = "data/inputs/staff_roles_ranks.md"
    import os
    if os.path.exists(rank_file_path):
        with open(rank_file_path, "r", encoding="utf-8") as f:
            for line in f:
                if "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 2:
                        raw_n = parts[0]
                        if raw_n.startswith("-"):
                            raw_n = raw_n[1:].strip()
                        name_key = strip_accents(raw_n).lower()
                        role = parts[1]
                        rank = parts[2].replace("Rank:", "").replace("Rank", "").strip() if len(parts) > 2 else "N/A"
                        staff_rank_map[name_key] = {"role": role, "rank": rank}
                        
    # 1. Build group map from daily logs using normalized keys
    for group, members in raw_reports.items():
        for m in members.keys():
            norm_m = strip_accents(m)
            group_map[norm_m] = {"raw_name": m.strip(), "group": group}
            
    # 2. Collect all staff from Worklane and their raw names
    worklane_staff = {}
    for p in projects_list:
        if p["pic"] and p["pic"] != "Unknown":
            worklane_staff[strip_accents(p["pic"])] = p["pic"]
        for iss in p["issues"]:
            assignee = iss.get("assignee")
            if assignee:
                worklane_staff[strip_accents(assignee)] = assignee

    # 3. Union all staff names from all sources
    all_staff_norms = set(weekly_stats.keys()).union(set(monthly_stats.keys())).union(worklane_staff.keys()).union(group_map.keys())
    
    for m_norm in sorted(all_staff_norms):
        if not m_norm.strip():
            continue
        norm_key = strip_accents(m_norm)
        if norm_key.lower() == "bui thi xuan mai":
            continue
        info_resolved = group_map.get(norm_key)
        if info_resolved:
            raw_name = info_resolved["raw_name"]
            group = info_resolved["group"]
        elif norm_key in worklane_staff:
            raw_name = worklane_staff[norm_key]
            # Try to resolve group
            lower_name = raw_name.lower()
            if "oanh" in lower_name or "ngọc" in lower_name or "hậu" in lower_name or "mi" in lower_name or "yến" in lower_name:
                group = "Khối QTKD"
            elif "trang" in lower_name or "hương" in lower_name or "phước" in lower_name:
                group = "Khối QLCLĐT"
            elif "mai" in lower_name or "thảo" in lower_name or "anh" in lower_name:
                group = "Khối Ngoại ngữ và kỹ năng mềm"
            else:
                group = "Khối CNTT"
        else:
            raw_name = norm_key.title()
            group = "Khối CNTT"
            
        w_stats = weekly_stats.get(norm_key, {})
        m_stats = monthly_stats.get(norm_key, {})
        explicit_info = staff_rank_map.get(norm_key, {})
        
        personnel_list[raw_name] = {
            "name": raw_name,
            "normalized_name": m_norm,
            "group": group,
            "role": explicit_info.get("role", w_stats.get("role", "Giáo vụ" if group == "Khối QLCLĐT" else "Giảng viên")),
            "rank": explicit_info.get("rank", w_stats.get("rank", "3")),
            "proposed_ns": 1.15 if raw_name == "Trần Thị Mỹ Phước" else (1.10 if raw_name == "Nguyễn Huyền Trang" else (1.05 if raw_name == "Nguyễn Xuân Bách" else 0.75)),
            "evaluation": m_stats.get("evaluation", w_stats.get("evaluation", "")),
            "difficulties": w_stats.get("difficulties", []),
            "uncompleted_tasks": w_stats.get("uncompleted_tasks", []),
            "weekly": {
                "hours": w_stats.get("declared_hours", 0.0),
                "score": w_stats.get("work_score", 0.0),
                "reported_days": w_stats.get("reported_days", 0),
                "expected_days": w_stats.get("reported_days", 0) + len(w_stats.get("missing_days", []))
            },
            "monthly": {
                "hours": m_stats.get("declared_hours", 0.0),
                "score": m_stats.get("work_score", 0.0),
                "reported_days": m_stats.get("reported_days", 0),
                "expected_days": m_stats.get("reported_days", 0) + len(m_stats.get("missing_days", []))
            }
        }
        
    # Write static Markdown report (Keep it static and clean)
    md_content = f"""# Báo cáo Quản trị Nguồn lực & Tiến độ Dự án (Custom Director V4.2)

> [!NOTE]
> - **Người yêu cầu**: Thầy Nguyễn Duy Quang (Giám đốc đào tạo)
> - **Ngày kiểm toán**: {yesterday}
> - **Mục tiêu**: Báo cáo tổng thể nguồn lực và dự án.

---

## I. Tổng quan Dự án & Nguồn lực Bộ phận QLĐT

- **Ngày kiểm toán gần nhất**: {yesterday}
- **Tổng số dự án vận hành**: {len(projects_list)} dự án
- **Dự án đang chạy**: {sum(1 for p in projects_list if p["status"] == "ACTIVE")} dự án
- **Dự án đã hoàn thành**: {sum(1 for p in projects_list if p["status"] == "COMPLETED")} dự án

---

## II. Bảng chi tiết Phân vai dự án (PIC vs. Thành viên)

| Tên dự án | PIC chính | Thành viên tham gia | Trạng thái dự án | Sức khỏe |
| :--- | :--- | :--- | :---: | :---: |
"""
    for p in sorted(projects_list, key=lambda x: x["key"]):
        members_str = ", ".join([m for m in p["members"] if m.strip().lower() != p["pic"].strip().lower()])
        if not members_str:
            members_str = "-"
        md_content += f"| **{p['key']} - {p['name']}** | {p['pic']} | {members_str} | {p['status']} | {p['health']} |\n"

    # Write to custom reports
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Markdown report generated successfully at: {output_md_path}")

    # Export dynamic JSON data file for live-fetching
    output_json_path = "data/processed/director_dashboard_data.json"
    dashboard_data_payload = {
        "raw_reports": raw_reports,
        "projects_list": projects_list,
        "personnel_list": personnel_list,
        "dates_monthly": dates_monthly,
        "dates_weekly": dates_weekly,
        "yesterday": yesterday,
        "historical_kpi": historical_kpi
    }
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_data_payload, f, ensure_ascii=False, indent=2)
    print(f"JSON Data exported successfully at: {output_json_path}")

    # ----------------------------------------------------
    # GENERATE HTML DASHBOARD (RAW STRING REPLACEMENT)
    # ----------------------------------------------------
    
    html_template = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Executive Resource & Project Cockpit Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Plus Jakarta Sans', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }
        }
      }
    }
  </script>
  <style>
    body {
      background: radial-gradient(circle at top, #0f172a 0%, #030712 100%);
      background-attachment: fixed;
    }
    .glass-card {
      background: rgba(17, 24, 39, 0.45);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.05);
      box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
    }
    .glass-card-hover {
      transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    }
    .glass-card-hover:hover {
      transform: translateY(-2px);
      border-color: rgba(59, 130, 245, 0.3);
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 4px;
      height: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: rgba(255,255,255,0.01);
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: rgba(255,255,255,0.1);
      border-radius: 4px;
    }
    
    /* Drawer styling */
    .drawer-container {
      position: fixed;
      top: 0;
      right: -650px;
      width: 650px;
      height: 100vh;
      background: rgba(15, 23, 42, 0.96);
      backdrop-filter: blur(24px);
      border-left: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: -15px 0 45px rgba(0, 0, 0, 0.7);
      transition: right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      z-index: 100;
    }
    .drawer-container.open {
      right: 0;
    }
    .drawer-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(6px);
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease-in-out;
      z-index: 90;
    }
    .drawer-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }
  </style>
</head>
<body class="text-gray-100 p-6 min-h-screen">
  <div class="max-w-[1680px] w-full mx-auto space-y-6">
    <!-- Header -->
    <div class="glass-card rounded-2xl p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl font-extrabold tracking-tight flex items-center gap-2">
          <i class="fa-solid fa-chart-line text-blue-500"></i> PMO EXECUTIVE COCKPIT
        </h1>
        <p class="text-gray-400 text-xs mt-1">Cổng thông tin Quản lý Nguồn lực, Phân vai Dự án & Nhật ký đa chu kỳ — Kính gửi: <strong class="text-blue-400 font-semibold">Thầy Nguyễn Duy Quang (Giám đốc Đào tạo)</strong></p>
      </div>
      
      <!-- Time selector & Refresh button -->
      <div class="flex flex-wrap items-center gap-3">
        <button id="btn-refresh-data" class="px-3.5 py-1.5 rounded-xl bg-blue-900/40 border border-blue-700/50 text-blue-300 hover:bg-blue-800/60 transition text-xs font-semibold flex items-center gap-1.5 shadow-lg shadow-blue-950/40" onclick="fetchLiveDashboardData(true)" title="Cập nhật dữ liệu từ file JSON mới nhất">
          <i class="fa-solid fa-rotate text-blue-400" id="refresh-icon"></i> Cập nhật dữ liệu
        </button>
        
        <!-- Cycle selector buttons -->
        <div class="flex bg-gray-950/80 p-1 rounded-xl border border-gray-800 gap-1" id="cycle-toggles">
          <span class="text-[10px] text-gray-400 font-bold px-2 flex items-center">CHU KỲ:</span>
          <button class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 transition" id="btn-cycle-aug" onclick="switchCycle('aug')">THÁNG 8</button>
          <button class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-gray-400 transition" id="btn-cycle-jul" onclick="switchCycle('jul')">THÁNG 7</button>
          <button class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-gray-400 transition" id="btn-cycle-custom" onclick="switchCycle('custom')">TÙY CHỈNH</button>
        </div>
        
        <!-- Custom date inputs (hidden by default) -->
        <div id="custom-date-inputs" class="hidden flex items-center gap-1.5 bg-gray-950/80 p-1.5 rounded-xl border border-gray-800">
          <input type="date" id="input-start-date" class="bg-gray-900 border border-gray-800 text-gray-200 text-xs px-2 py-1 rounded-lg focus:outline-none focus:border-blue-500" onchange="customDateChanged()">
          <span class="text-xs text-gray-500">-</span>
          <input type="date" id="input-end-date" class="bg-gray-900 border border-gray-800 text-gray-200 text-xs px-2 py-1 rounded-lg focus:outline-none focus:border-blue-500" onchange="customDateChanged()">
        </div>

        <div class="flex bg-gray-950/80 p-1 rounded-xl border border-gray-800" id="time-range-toggles">
          <button class="px-4 py-1.5 rounded-lg text-xs font-semibold text-gray-400 transition" id="btn-daily" onclick="switchTimeRange('daily')">DAILY</button>
          <button class="px-4 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 transition" id="btn-weekly" onclick="switchTimeRange('weekly')">WEEKLY</button>
          <button class="px-4 py-1.5 rounded-lg text-xs font-semibold text-gray-400 transition" id="btn-monthly" onclick="switchTimeRange('monthly')">MONTHLY</button>
        </div>
        
        <!-- Date dropdown picker -->
        <select id="date-select" class="bg-gray-900 border border-gray-800 text-gray-200 text-xs px-3 py-2 rounded-xl focus:outline-none focus:border-blue-500" onchange="switchDate(this.value)">
          <!-- Options populated by JS -->
        </select>
      </div>
    </div>
    
    <!-- Top-level Key Metrics & Alert Widgets -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <div class="lg:col-span-3 space-y-6">
        <!-- Key Metrics Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card rounded-2xl p-5 relative overflow-hidden glass-card-hover">
            <div class="absolute top-0 left-0 w-1.5 h-full bg-blue-500"></div>
            <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Dự án Đang Chạy (Active)</span>
            <div class="text-2xl font-extrabold mt-2 flex items-baseline gap-1" id="metric-active-projs">0<span class="text-xs text-gray-400 font-normal"> / 0 projs</span></div>
            <i class="fa-solid fa-diagram-project absolute right-4 bottom-4 text-3xl text-gray-700/20"></i>
          </div>
          
          <div class="glass-card rounded-2xl p-5 relative overflow-hidden glass-card-hover">
            <div class="absolute top-0 left-0 w-1.5 h-full bg-emerald-500"></div>
            <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Tỷ lệ Hoàn Thành Task</span>
            <div class="text-2xl font-extrabold mt-2 flex items-baseline gap-1" id="metric-completion-rate">0.0%</div>
            <i class="fa-solid fa-circle-check absolute right-4 bottom-4 text-3xl text-gray-700/20"></i>
          </div>
          
          <div class="glass-card rounded-2xl p-5 relative overflow-hidden glass-card-hover">
            <div class="absolute top-0 left-0 w-1.5 h-full bg-red-500"></div>
            <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Nhân sự Quá tải</span>
            <div class="text-2xl font-extrabold mt-2 flex items-baseline gap-1 text-red-400" id="metric-overloaded">0<span class="text-xs text-gray-400 font-normal"> người</span></div>
            <i class="fa-solid fa-triangle-exclamation absolute right-4 bottom-4 text-3xl text-gray-700/20"></i>
          </div>
          
          <div class="glass-card rounded-2xl p-5 relative overflow-hidden glass-card-hover">
            <div class="absolute top-0 left-0 w-1.5 h-full bg-sky-500"></div>
            <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Nhân sự Trống việc</span>
            <div class="text-2xl font-extrabold mt-2 flex items-baseline gap-1 text-sky-400" id="metric-idle">0<span class="text-xs text-gray-400 font-normal"> người</span></div>
            <i class="fa-solid fa-users absolute right-4 bottom-4 text-3xl text-gray-700/20"></i>
          </div>
        </div>
        
        <!-- Navigation & Filtering Row -->
        <div class="glass-card rounded-2xl p-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <!-- Department Filter Tabs -->
          <div class="flex flex-wrap bg-gray-950/60 p-1 rounded-xl border border-gray-800/80 gap-1" id="dept-tabs">
            <button class="px-4 py-1.5 rounded-lg text-xs font-bold transition text-white bg-blue-600" onclick="switchDept('all')">Tất cả</button>
            <button class="px-4 py-1.5 rounded-lg text-xs font-bold transition text-gray-400 hover:text-white" onclick="switchDept('Khối CNTT')">Khối CNTT</button>
            <button class="px-4 py-1.5 rounded-lg text-xs font-bold transition text-gray-400 hover:text-white" onclick="switchDept('Khối QTKD')">Khối QTKD</button>
            <button class="px-4 py-1.5 rounded-lg text-xs font-bold transition text-gray-400 hover:text-white" onclick="switchDept('Khối QLCLĐT')">Khối QLCLĐT</button>
            <button class="px-4 py-1.5 rounded-lg text-xs font-bold transition text-gray-400 hover:text-white" onclick="switchDept('Khối Ngoại ngữ và kỹ năng mềm')">Khối Ngoại ngữ</button>
          </div>
          
          <!-- Workload status filter + Search -->
          <div class="flex flex-wrap items-center gap-3 w-full md:w-auto">
            <div class="flex bg-gray-950/60 p-1 rounded-xl border border-gray-800/80 gap-1" id="workload-filters">
              <button class="px-3 py-1 rounded-lg text-[10px] font-bold transition text-white bg-gray-800" onclick="switchWorkloadFilter('all')">Tải: Tất cả</button>
              <button class="px-3 py-1 rounded-lg text-[10px] font-bold transition text-gray-400 hover:text-white" onclick="switchWorkloadFilter('overloaded')">🔴 Quá tải</button>
              <button class="px-3 py-1 rounded-lg text-[10px] font-bold transition text-gray-400 hover:text-white" onclick="switchWorkloadFilter('idle')">🔵 Trống việc</button>
              <button class="px-3 py-1 rounded-lg text-[10px] font-bold transition text-gray-400 hover:text-white" onclick="switchWorkloadFilter('balanced')">🟢 Cân bằng</button>
            </div>
            
            <input type="text" class="bg-gray-900 border border-gray-800 text-xs px-3 py-2 rounded-xl focus:outline-none focus:border-blue-500 w-full md:w-48" id="search-staff" placeholder="Tìm kiếm thầy/cô..." onkeyup="filterStaffTable(this.value)">
          </div>
        </div>
        
        <!-- Executive Charts Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="glass-card rounded-2xl p-5 space-y-4">
            <h3 class="text-xs font-bold uppercase tracking-wider text-gray-400"><i class="fa-solid fa-users-viewfinder mr-1.5 text-blue-500"></i> Workload Khối</h3>
            <div class="h-44 relative">
              <canvas id="deptWorkloadChart"></canvas>
            </div>
          </div>
          
          <div class="glass-card rounded-2xl p-5 space-y-4">
            <h3 class="text-xs font-bold uppercase tracking-wider text-gray-400"><i class="fa-solid fa-fire-flame-curved mr-1.5 text-red-500"></i> Top 5 dự án trễ hạn</h3>
            <div class="h-44 relative">
              <canvas id="overdueProjectsChart"></canvas>
            </div>
          </div>
          
          <div class="glass-card rounded-2xl p-5 space-y-4">
            <h3 class="text-xs font-bold uppercase tracking-wider text-gray-400"><i class="fa-solid fa-chart-area mr-1.5 text-emerald-500"></i> Năng suất tuần</h3>
            <div class="h-44 relative">
              <canvas id="deptTrendChart"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right: Resource Alerts Widget (1/3 column) -->
      <div class="glass-card rounded-2xl p-5 flex flex-col h-full border-l-4 border-amber-500/50">
        <h3 class="text-xs font-bold text-gray-300 uppercase tracking-wider mb-4 flex items-center gap-1.5 pb-2 border-b border-gray-800">
          <i class="fa-solid fa-bell text-amber-500"></i> Cảnh báo điều phối nguồn lực
        </h3>
        
        <div class="flex-1 space-y-4 overflow-y-auto custom-scrollbar pr-1 max-h-[310px]">
          <!-- Overloaded -->
          <div class="space-y-2">
            <h4 class="text-[10px] font-bold text-red-400 uppercase tracking-wider flex items-center gap-1">
              <i class="fa-solid fa-circle-exclamation text-red-500"></i> Quá tải nặng (Red Alert)
            </h4>
            <ul class="space-y-1.5" id="list-overloaded">
              <!-- Populated dynamically -->
            </ul>
          </div>
          
          <!-- Idle -->
          <div class="space-y-2">
            <h4 class="text-[10px] font-bold text-sky-400 uppercase tracking-wider flex items-center gap-1">
              <i class="fa-solid fa-circle-check text-sky-500"></i> Nhân sự trống việc (Bench)
            </h4>
            <ul class="space-y-1.5" id="list-idle">
              <!-- Populated dynamically -->
            </ul>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Personnel Summary Table -->
    <div class="glass-card rounded-2xl p-5">
      <h3 class="text-xs font-bold uppercase tracking-wider text-gray-400 mb-4 flex justify-between items-center">
        <span>Bảng tổng hợp hiệu năng giảng viên</span>
        <span class="text-[10px] text-gray-500 normal-case" id="tbl-total-count">Hiển thị: 0/0 nhân sự</span>
      </h3>
      <div class="overflow-x-auto custom-scrollbar">
        <table class="w-full text-left text-[13px] border-collapse">
          <thead>
            <tr class="bg-gray-950/40 text-gray-400 border-b border-gray-800">
              <th class="p-3 uppercase">Họ và tên</th>
              <th class="p-3 uppercase">Khối phòng ban</th>
              <th class="p-3 uppercase">Trạng thái tải</th>
              <th class="p-3 uppercase">Dự án đang chạy</th>
              <th class="p-3 uppercase text-right">Task Active</th>
              <th class="p-3 uppercase text-right">Task Quá Hạn</th>
              <th class="p-3 uppercase text-right" id="th-range-hours">Số giờ logs</th>
              <th class="p-3 uppercase text-right" id="th-range-compliance">Điểm tuân thủ</th>
            </tr>
          </thead>
          <tbody id="tbody-staff-summary" class="divide-y divide-gray-800/40">
            <!-- Populated dynamically -->
          </tbody>
        </table>
      </div>
      <!-- Pagination Controls -->
      <div class="flex justify-between items-center mt-4 pt-3 border-t border-gray-800/40 text-xs text-gray-400" id="pagination-controls">
        <!-- Rendered by JS -->
      </div>
    </div>
  </div>
  
  <!-- Slide-over Drawer Backdrop overlay -->
  <div id="drawer-overlay" class="drawer-overlay" onclick="closeDrawer()"></div>
  
  <!-- Slide-over Drawer Panel -->
  <div id="detail-drawer" class="drawer-container flex flex-col">
    <!-- Header -->
    <div class="p-5 border-b border-gray-800 flex justify-between items-center">
      <h3 class="text-sm font-bold text-gray-200 flex items-center gap-2">
        <i class="avatar-circle w-6 h-6 rounded-full inline-flex items-center justify-center text-[10px] text-white font-extrabold" id="staff-avatar">T</i> Chi Tiết Nhật Ký & Dự Án
      </h3>
      <button class="text-gray-400 hover:text-white transition text-lg p-1" onclick="closeDrawer()"><i class="fa-solid fa-xmark"></i></button>
    </div>
    
    <!-- Body Scroll Container -->
    <div class="flex-1 overflow-y-auto custom-scrollbar p-5 space-y-6">
      <!-- Personnel Meta Details -->
      <div class="grid grid-cols-3 gap-3">
        <div class="bg-gray-950/40 p-3 rounded-xl border border-gray-800 text-center">
          <span class="text-[9px] text-gray-400 font-bold uppercase tracking-wider block">Vai trò & Rank</span>
          <span class="text-[11px] font-semibold mt-1 block truncate" id="lbl-staff-role">-</span>
        </div>
        <div class="bg-gray-950/40 p-3 rounded-xl border border-gray-800 text-center">
          <span class="text-[9px] text-gray-400 font-bold uppercase tracking-wider block">Khối lượng</span>
          <span class="text-[11px] font-semibold mt-1 block truncate" id="lbl-staff-hours">-</span>
        </div>
        <div class="bg-gray-950/40 p-3 rounded-xl border border-gray-800 text-center">
          <span class="text-[9px] text-gray-400 font-bold uppercase tracking-wider block" id="lbl-staff-score-title">Tuân thủ</span>
          <span class="text-[11px] font-semibold mt-1 block truncate text-blue-400" id="lbl-staff-score">-</span>
        </div>
      </div>
      
      <!-- Evaluation Panel -->
      <div class="bg-blue-950/15 border border-blue-900/30 p-4 rounded-xl text-xs space-y-1">
        <strong class="text-blue-400 block"><i class="fa-solid fa-comment-dots mr-1"></i> Nhận xét hiệu suất:</strong>
        <p id="lbl-staff-eval" class="text-gray-300"></p>
      </div>
      
      <!-- Problems & Overdues lists -->
      <div class="space-y-3">
        <div class="border border-amber-900/30 bg-amber-950/5 p-3.5 rounded-xl space-y-2">
          <h4 class="text-xs font-bold text-amber-500 uppercase tracking-wider"><i class="fa-solid fa-triangle-exclamation"></i> Khó khăn ghi nhận</h4>
          <ul class="text-xs text-gray-300 space-y-1 max-h-24 overflow-y-auto custom-scrollbar" id="lbl-staff-diffs"></ul>
        </div>
        <div class="border border-red-900/30 bg-red-950/5 p-3.5 rounded-xl space-y-2">
          <h4 class="text-xs font-bold text-red-500 uppercase tracking-wider"><i class="fa-solid fa-circle-xmark"></i> Task chưa hoàn thành</h4>
          <ul class="text-xs text-gray-300 space-y-1 max-h-24 overflow-y-auto custom-scrollbar" id="lbl-staff-uncompleted"></ul>
        </div>
      </div>
      
      <!-- Personal chart -->
      <div class="bg-gray-950/30 border border-gray-800 p-4 rounded-xl">
        <h4 class="text-[10px] text-gray-400 font-bold uppercase tracking-wider mb-2"><i class="fa-solid fa-chart-pie mr-1 text-blue-500"></i> Phân bổ Task Dự án cá nhân</h4>
        <div class="h-36 relative">
          <canvas id="individualChart"></canvas>
        </div>
      </div>
      
      <!-- Active Projects -->
      <div class="space-y-2">
        <h4 class="text-[10px] font-bold uppercase tracking-wider text-gray-400">Các dự án đang tham gia trên Worklane</h4>
        <div class="grid grid-cols-2 gap-3" id="staff-detail-projects">
          <!-- Populated dynamically -->
        </div>
      </div>
      
      <!-- Logs table -->
      <div class="space-y-2">
        <div class="flex justify-between items-center">
          <h4 class="text-[11px] font-bold uppercase tracking-wider text-gray-400">Nhật ký công việc cụ thể</h4>
          <input type="text" class="bg-gray-900/80 border border-gray-800 text-[11px] px-2 py-1 rounded-lg w-40 focus:outline-none focus:border-blue-500" id="search-tasks" placeholder="Tìm kiếm task..." onkeyup="filterTasks(this.value)">
        </div>
        <div class="overflow-x-auto custom-scrollbar border border-gray-800/40 rounded-xl max-h-60">
          <table class="w-full text-left text-[12px] border-collapse">
            <thead>
              <tr class="bg-gray-950/50 text-gray-400 border-b border-gray-800">
                <th class="p-2 w-16">Ngày</th>
                <th class="p-2">Nhiệm vụ</th>
                <th class="p-2 w-16 text-right">Giờ logs</th>
                <th class="p-2 w-28">Dự án</th>
              </tr>
            </thead>
            <tbody id="tasks-tbody" class="divide-y divide-gray-800/40">
              <!-- Populated dynamically -->
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
  
  <script>
    // Accent stripping function for Vietnamese
    function stripAccents(str) {
      if (!str) return "";
      return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
    }

    // Dynamic Fetching capability with fallback to embedded JSON
    async function fetchLiveDashboardData(showNotification = false) {
      const icon = document.getElementById("refresh-icon");
      if (icon) icon.classList.add("fa-spin");
      try {
        const pathsToTry = [
          "../data/processed/director_dashboard_data.json?t=" + Date.now(),
          "./data/processed/director_dashboard_data.json?t=" + Date.now()
        ];
        let fetchedData = null;
        for (const p of pathsToTry) {
          try {
            const res = await fetch(p);
            if (res.ok) {
              fetchedData = await res.json();
              break;
            }
          } catch(e) {}
        }
        if (fetchedData) {
          if (fetchedData.raw_reports) rawReports = fetchedData.raw_reports;
          if (fetchedData.projects_list) projectsData = fetchedData.projects_list;
          if (fetchedData.personnel_list) personnelData = fetchedData.personnel_list;
          if (fetchedData.historical_kpi) historicalKPI = fetchedData.historical_kpi;
          if (fetchedData.dates_monthly) datesMonthly = fetchedData.dates_monthly;
          if (fetchedData.dates_weekly) datesWeekly = fetchedData.dates_weekly;
          if (fetchedData.yesterday) yesterday = fetchedData.yesterday;
          
          populateDateSelect();
          refreshDashboard();
          if (currentStaff) openStaffDrawer(currentStaff);
          if (showNotification) alert("Đã cập nhật dữ liệu mới nhất thành công!");
        } else {
          if (showNotification) alert("Đang chạy ở chế độ Offline/Local File. Dashboard tiếp tục sử dụng dữ liệu đã nhúng sẵn.");
        }
      } catch (err) {
        console.warn("Fetch live data error:", err);
      } finally {
        if (icon) icon.classList.remove("fa-spin");
      }
    }

    // Raw JSON data bindings
    let rawReports = __RAW_REPORTS__;
    let projectsData = __PROJECTS_DATA__;
    let personnelData = __PERSONNEL_DATA__;
    let historicalKPI = __HISTORICAL_KPI__;
    let datesMonthly = __DATES_MONTHLY__;
    let datesWeekly = __DATES_WEEKLY__;
    let yesterday = "__YESTERDAY__";
    const weeklyTrends = {
      labels: ["Tuần 27", "Tuần 28", "Tuần 29", "Tuần 30"],
      hours: [135, 142, 148, 143],
      compliance: [86.5, 88.0, 91.2, 88.7]
    };
    
    // UI state
    let currentTimeRange = "weekly"; // daily, weekly, monthly
    let currentSelectedDate = yesterday;
    let currentStaff = "";
    
    // Cycle state
    let currentCycle = "aug"; // aug, jul, custom
    let currentStartDate = "2026-08-01";
    let currentEndDate = yesterday;
    
    // Filter states
    let currentDepartment = "all";
    let currentWorkloadFilter = "all";
    let searchQuery = "";
    let currentPage = 1;
    const rowsPerPage = 10;
    
    // Dynamic calculations payload
    let jsPersonnel = {};
    let jsProjects = [];
    let jsOverallMetrics = {};
    
    // Charts variables
    let workloadChart = null;
    let overdueChart = null;
    let trendChart = null;
    let statusChart = null;
    let projTasksChart = null;
    let individualChart = null;
    
    // Calculate everything client-side dynamically
    function calculateSystemState() {
      jsPersonnel = {};
      jsProjects = [];
      
      const staffProjectsMap = {};
      const todayRef = currentSelectedDate;
      
      // Calculate project stats and link assignees
      projectsData.forEach(p => {
        const stats = { total: 0, completed: 0, active: 0, planned_active: 0, overdue: 0, urgent: 0 };
        const fIssues = [];
        const membersSet = new Set();
        
        if (p.pic && p.pic !== 'Unknown') {
          membersSet.add(p.pic);
        }
        
        p.issues.forEach(iss => {
          const state = String(iss.state).toLowerCase().trim();
          
          // Rule 1: Canceled tasks are completely ignored
          if (state === 'hủy' || state === 'huy' || state === 'cancel' || state === 'cancelled') {
            return;
          }
          
          const isDone = state === 'hoàn thành' || state === 'done' || state === 'completed';
          
          let isRelevant = false;
          let isOverdue = false;
          let isUrgent = false;
          let shouldCountActive = false;
          
          if (iss.dueDate) {
            const dueStr = iss.dueDate.slice(0, 10);
            
            // Check relevance for the active cycle
            if (dueStr < currentStartDate) {
              // Past task
              if (!isDone) {
                // Still not completed -> relevant and overdue
                isRelevant = true;
                isOverdue = true;
              } else {
                // Completed in the past -> not relevant to this week's/month's reports
                isRelevant = false;
              }
            } else if (dueStr >= currentStartDate && dueStr <= currentEndDate) {
              // Due within this week/month -> relevant
              isRelevant = true;
              if (!isDone && dueStr <= todayRef) {
                // Due on or before selected date and not done -> overdue
                isOverdue = true;
              } else if (!isDone) {
                shouldCountActive = true;
                try {
                  const dueDt = new Date(dueStr);
                  const refDt = new Date(todayRef);
                  const diffDays = Math.ceil((dueDt - refDt) / (1000 * 60 * 60 * 24));
                  if (diffDays >= 0 && diffDays <= 5) {
                    isUrgent = true;
                  }
                } catch(e) {}
              }
            } else {
              // Future task beyond currentEndDate -> not relevant
              isRelevant = false;
            }
          } else {
            // No due date -> count as active if not done
            isRelevant = !isDone;
            shouldCountActive = !isDone;
          }
          
          if (isRelevant) {
            fIssues.push(iss);
            stats.total += 1;
            
            if (iss.assignee) {
              membersSet.add(iss.assignee);
            }
            
            if (isDone) {
              stats.completed += 1;
            } else {
              stats.active += 1;
              if (isOverdue) {
                stats.overdue += 1;
                iss.is_overdue = true;
                iss.is_urgent = false;
              } else {
                stats.planned_active += 1;
                iss.is_overdue = false;
                if (isUrgent) {
                  stats.urgent += 1;
                  iss.is_urgent = true;
                } else {
                  iss.is_urgent = false;
                }
              }
            }
          }
        });
        
        let pHealth = p.health;
        if (p.status !== "COMPLETED" && stats.overdue > 0) {
          pHealth = "OFF_TRACK";
        }
        
        const projObj = {
          key: p.key,
          name: p.name,
          pic: p.pic,
          status: p.status,
          health: pHealth,
          stats: stats,
          members: Array.from(membersSet).sort(),
          issues: fIssues
        };
        
        jsProjects.push(projObj);
        
        // Link to staff projects
        Array.from(membersSet).forEach(m => {
          const mNorm = stripAccents(m);
          if (!staffProjectsMap[mNorm]) {
            staffProjectsMap[mNorm] = [];
          }
          
          const pStats = { total: 0, completed: 0, active: 0, planned_active: 0, overdue: 0, urgent: 0 };
          const pIssues = [];
          
          fIssues.forEach(iss => {
            if (iss.assignee && stripAccents(iss.assignee) === mNorm) {
              pIssues.push(iss);
              pStats.total += 1;
              const state = String(iss.state).toLowerCase().trim();
              const isDone = state === 'hoàn thành' || state === 'done' || state === 'completed';
              if (isDone) {
                pStats.completed += 1;
              } else {
                pStats.active += 1;
                if (iss.is_overdue) {
                  pStats.overdue += 1;
                } else {
                  // If it's active and not overdue, it's a planned active task
                  pStats.planned_active += 1;
                }
                if (iss.is_urgent) pStats.urgent += 1;
              }
            }
          });
          
          staffProjectsMap[mNorm].push({
            key: p.key,
            name: p.name,
            role: stripAccents(m) === stripAccents(p.pic) ? "PIC Dự án" : "Thành viên",
            status: p.status,
            health: pHealth,
            personal_stats: pStats,
            personal_issues: pIssues
          });
        });
      });
      
      // Calculate workload alerts & hours for each personnel
      Object.keys(personnelData).forEach(name => {
        const pMeta = personnelData[name];
        const mNorm = stripAccents(name);
        
        const pProjs = staffProjectsMap[mNorm] || [];
        const totalPActive = pProjs.reduce((sum, pr) => sum + pr.personal_stats.active, 0);
        const totalPPlannedActive = pProjs.reduce((sum, pr) => sum + pr.personal_stats.planned_active, 0);
        const totalPOverdue = pProjs.reduce((sum, pr) => sum + pr.personal_stats.overdue, 0);
        const totalPUrgent = pProjs.reduce((sum, pr) => sum + pr.personal_stats.urgent, 0);
        const activePicsCount = pProjs.filter(pr => pr.role === "PIC Dự án" && pr.status !== "COMPLETED").length;
        
        let calculatedHours = 0.0;
        let expectedDays = 1;
        let reportedDays = 0;
        let workScore = 0.0;
        
        const staff_daily = rawReports[pMeta.group]?.[name]?.reports || {};
        
        if (currentTimeRange === "daily") {
          expectedDays = 1;
          const rep = staff_daily[currentSelectedDate];
          if (rep) {
            reportedDays = 1;
            rep.tasks.forEach(t => { calculatedHours += parseFloat(t.hours || 0); });
          }
          workScore = reportedDays * 100.0; // 100 if nộp, 0 if thiếu
        } else {
          // Dynamic calculation based on currentStartDate and currentEndDate
          let activeDates = [];
          if (currentTimeRange === "weekly") {
            // Keep current week dates only if they fit the cycle
            activeDates = datesWeekly.filter(d => d >= currentStartDate && d <= currentEndDate);
            if (activeDates.length === 0) {
              // Fallback to the last 5 weekdays of the selected cycle
              const allCycleDates = datesMonthly.filter(d => d >= currentStartDate && d <= currentEndDate);
              activeDates = allCycleDates.slice(-5);
            }
          } else {
            // monthly or custom range
            activeDates = datesMonthly.filter(d => d >= currentStartDate && d <= currentEndDate);
          }
          
          expectedDays = activeDates.length;
          let totalTasks = 0;
          let completedTasks = 0;
          
          activeDates.forEach(d => {
            const rep = staff_daily[d];
            if (rep) {
              reportedDays += 1;
              calculatedHours += parseFloat(rep.stats?.hours || 0.0);
              const tasks = rep.tasks || [];
              tasks.forEach(t => {
                totalTasks += 1;
                if (t.done || t.percent === 100) {
                  completedTasks += 1;
                }
              });
            }
          });
          
          const reportRate = expectedDays > 0 ? (reportedDays / expectedDays) : 0.0;
          const completionRate = totalTasks > 0 ? (completedTasks / totalTasks) : 1.0;
          workScore = reportedDays > 0 ? ((reportRate * 40.0) + (completionRate * 40.0) + (100.0 * 0.20)) : 0.0;
        }
        
        // Workload rule engine
        let wlStatus = "BÌNH THƯỜNG";
        let wlReason = "Tải công việc ổn định";
        
        if (currentTimeRange === "daily") {
          if (calculatedHours > 10.0) {
            wlStatus = "QUÁ TẢI (KHỐI LƯỢNG)";
            wlReason = `Số giờ logs ngày đạt ${calculatedHours.toFixed(1)}h`;
          } else if (calculatedHours === 0.0) {
            wlStatus = "TRỐNG VIỆC / SẴN SÀNG";
            wlReason = "Không nộp báo cáo hoặc logs đạt 0h hôm nay";
          } else {
            wlStatus = "BÌNH THƯỜNG";
            wlReason = `Đã nộp báo cáo ngày (${calculatedHours.toFixed(1)}h)`;
          }
        } else {
          // Weekly / Monthly rules
          let ns_factor = pMeta.proposed_ns || 1.0;
          let threshold_heavy = Math.round(ns_factor * 8);
          let threshold_extreme = Math.round(ns_factor * 12);
          
          if (totalPPlannedActive > threshold_extreme || (currentTimeRange === "monthly" && calculatedHours > 180.0) || (currentTimeRange === "weekly" && calculatedHours > 50.0)) {
            wlStatus = "QUÁ TẢI NGHIÊM TRỌNG";
            wlReason = `Đang xử lý ${totalPPlannedActive} task mới (Vượt mốc ${threshold_extreme})`;
            if (currentTimeRange === "weekly" && calculatedHours > 50.0) wlReason += ` & Logs > 50h`;
          } else if (totalPPlannedActive > threshold_heavy || (currentTimeRange === "monthly" && calculatedHours > 160.0) || (currentTimeRange === "weekly" && calculatedHours > 42.0)) {
            wlStatus = "QUÁ TẢI (KHỐI LƯỢNG)";
            wlReason = `Đang xử lý ${totalPPlannedActive} task mới (Vượt mốc ${threshold_heavy})`;
          } else if (totalPPlannedActive === 0 && totalPOverdue === 0 && (currentTimeRange === "monthly" ? calculatedHours < 20.0 : calculatedHours < 5.0)) {
            wlStatus = "TRỐNG VIỆC / SẴN SÀNG";
            wlReason = "Không có task đúng lịch hoặc task nợ";
          } else if (totalPPlannedActive === 0 && totalPOverdue > 0) {
            wlStatus = "CÂN BẰNG (ĐANG BÙ LỖI)";
            wlReason = `Không có task đúng lịch, đang cày bù ${totalPOverdue} task nợ`;
          } else if (totalPPlannedActive <= threshold_heavy && totalPOverdue > 0) {
            wlStatus = "BÌNH THƯỜNG (CÓ TASK NỢ)";
            wlReason = `Tải mới ổn định (${totalPPlannedActive} task), đang phải cày bù ${totalPOverdue} task nợ`;
          }
        }
        
        const activeProjs = pProjs.filter(pr => pr.status !== "COMPLETED").map(pr => pr.name);
        const completedProjs = pProjs.filter(pr => pr.status === "COMPLETED").map(pr => pr.name);
        const futureProjs = pProjs.filter(pr => pr.status === "PENDING" || pr.status === "FUTURE").map(pr => pr.name);
        
        jsPersonnel[name] = {
          name: name,
          group: pMeta.group,
          role: pMeta.role,
          rank: pMeta.rank,
          proposed_ns: pMeta.proposed_ns,
          evaluation: pMeta.evaluation,
          hours: calculatedHours,
          reported_days: reportedDays,
          expected_days: expectedDays,
          work_score: workScore,
          workload: {
            status: wlStatus,
            reason: wlReason,
            active_count: totalPActive,
            overdue_count: totalPOverdue,
            urgent_count: totalPUrgent,
            pic_active_count: activePicsCount
          },
          projects: {
            all: pProjs,
            active: activeProjs,
            completed: completedProjs,
            future: futureProjs
          },
          difficulties: pMeta.difficulties,
          uncompleted_tasks: pMeta.uncompleted_tasks
        };
      });
      
      // Calculate overall system stats (scoped by global department filter)
      const filteredStaff = Object.values(jsPersonnel).filter(p => {
        return currentDepartment === "all" || p.group === currentDepartment;
      });
      
      const overloadedCount = filteredStaff.filter(p => p.workload.status.startsWith("QUÁ TẢI")).length;
      const idleCount = filteredStaff.filter(p => p.workload.status === "TRỐNG VIỆC / SẴN SÀNG").length;
      
      const filteredProjects = jsProjects.filter(pr => {
        if (currentDepartment === "all") return true;
        // A project belongs to the selected department if its PIC or any of its members are from it
        return pr.members.some(m => {
          const staffMeta = jsPersonnel[m];
          return staffMeta && staffMeta.group === currentDepartment;
        });
      });
      
      const totalTasks = filteredProjects.reduce((sum, pr) => sum + pr.stats.total, 0);
      const completedTasks = filteredProjects.reduce((sum, pr) => sum + pr.stats.completed, 0);
      const overdueTasks = filteredProjects.reduce((sum, pr) => sum + pr.stats.overdue, 0);
      const activeProjectsCount = filteredProjects.filter(pr => pr.status === "ACTIVE").length;
      const avgCompletionRate = totalTasks > 0 ? (completedTasks / totalTasks) * 100.0 : 0.0;
      
      jsOverallMetrics = {
        active_projects: activeProjectsCount,
        total_projects: filteredProjects.length,
        completion_rate: avgCompletionRate.toFixed(1) + "%",
        overdue_tasks: overdueTasks,
        overloaded_count: overloadedCount,
        idle_count: idleCount
      };
    }
    
    function updateMetricsWidgets() {
      document.getElementById("metric-active-projs").innerHTML = `${jsOverallMetrics.active_projects}<span class="text-xs text-gray-400 font-normal"> / ${jsOverallMetrics.total_projects} projs</span>`;
      document.getElementById("metric-completion-rate").textContent = jsOverallMetrics.completion_rate;
      document.getElementById("metric-overloaded").innerHTML = `${jsOverallMetrics.overloaded_count}<span class="text-xs text-gray-400 font-normal"> người</span>`;
      document.getElementById("metric-idle").innerHTML = `${jsOverallMetrics.idle_count}<span class="text-xs text-gray-400 font-normal"> người</span>`;
    }
    
    function updateAlertsWidget() {
      const oList = document.getElementById("list-overloaded");
      const iList = document.getElementById("list-idle");
      
      oList.innerHTML = "";
      iList.innerHTML = "";
      
      let oCount = 0;
      let iCount = 0;
      
      Object.keys(jsPersonnel).sort().forEach(name => {
        const p = jsPersonnel[name];
        const wl = p.workload;
        
        if (currentDepartment !== "all" && p.group !== currentDepartment) {
          return;
        }
        
        if (wl.status.startsWith("QUÁ TẢI")) {
          oCount++;
          const li = document.createElement("li");
          li.className = "p-2 rounded-xl bg-red-950/15 border border-red-900/30 flex justify-between items-center text-[11px] cursor-pointer hover:border-red-500 transition";
          li.onclick = () => openStaffDrawer(name);
          li.innerHTML = `
            <div>
              <strong class="text-red-400 font-semibold">${name}</strong>
              <p class="text-[9px] text-gray-400 mt-0.5 truncate max-w-[150px]">${wl.reason}</p>
            </div>
            <span class="px-1.5 py-0.5 bg-red-500/20 text-red-400 rounded text-[8px] font-bold border border-red-500/30">${wl.active_count} Active</span>
          `;
          oList.appendChild(li);
        } else if (wl.status === "TRỐNG VIỆC / SẴN SÀNG") {
          iCount++;
          const li = document.createElement("li");
          li.className = "p-2 rounded-xl bg-sky-950/15 border border-sky-900/30 flex justify-between items-center text-[11px] cursor-pointer hover:border-sky-500 transition";
          li.onclick = () => openStaffDrawer(name);
          li.innerHTML = `
            <div>
              <strong class="text-sky-400 font-semibold">${name}</strong>
              <p class="text-[9px] text-gray-400 mt-0.5">${p.group.replace("Khối ", "")}</p>
            </div>
            <span class="px-1.5 py-0.5 bg-sky-500/20 text-sky-400 rounded text-[8px] font-bold border border-sky-500/30">IDLE</span>
          `;
          iList.appendChild(li);
        }
      });
      
      if (oCount === 0) {
        oList.innerHTML = `<li class="text-gray-500 text-[10px] italic text-center p-2">Không ghi nhận nhân sự quá tải.</li>`;
      }
      if (iCount === 0) {
        iList.innerHTML = `<li class="text-gray-500 text-[10px] italic text-center p-2">Tất cả nhân sự đều được phân việc.</li>`;
      }
    }
    
    function renderStaffSummaryTable() {
      const tbody = document.getElementById("tbody-staff-summary");
      tbody.innerHTML = "";
      
      const filteredStaff = [];
      let totalCount = 0;
      
      Object.keys(jsPersonnel).sort().forEach(name => {
        const p = jsPersonnel[name];
        const wl = p.workload;
        totalCount++;
        
        // 1. Filter by Department
        if (currentDepartment !== "all" && p.group !== currentDepartment) {
          return;
        }
        
        // 2. Filter by Workload status
        if (currentWorkloadFilter === "overloaded" && !wl.status.startsWith("QUÁ TẢI")) return;
        if (currentWorkloadFilter === "idle" && wl.status !== "TRỐNG VIỆC / SẴN SÀNG") return;
        if (currentWorkloadFilter === "balanced" && (wl.status.startsWith("QUÁ TẢI") || wl.status === "TRỐNG VIỆC / SẴN SÀNG")) return;
        
        // 3. Filter by Search Query
        if (searchQuery && !stripAccents(name).includes(searchQuery)) {
          return;
        }
        
        filteredStaff.push(p);
      });
      
      const displayedCount = filteredStaff.length;
      const totalPages = Math.max(1, Math.ceil(displayedCount / rowsPerPage));
      if (currentPage > totalPages) currentPage = totalPages;
      
      const startIdx = (currentPage - 1) * rowsPerPage;
      const pageStaff = filteredStaff.slice(startIdx, startIdx + rowsPerPage);
      
      pageStaff.forEach((p, index) => {
        const name = p.name;
        const wl = p.workload;
        const globalIdx = startIdx + index;
        
        let wlClass = "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
        let wlText = "Cân bằng";
        if (wl.status.includes("DEADLINE")) { wlClass = "bg-red-500/10 text-red-400 border border-red-500/20"; wlText = "Quá tải (Deadline)"; }
        else if (wl.status.includes("KHỐI LƯỢNG")) { wlClass = "bg-red-500/10 text-red-400 border border-red-500/20"; wlText = "Quá tải (Volume)"; }
        else if (wl.status.includes("VAI TRÒ")) { wlClass = "bg-amber-500/10 text-amber-400 border border-amber-500/20"; wlText = "Quá tải (Role)"; }
        else if (wl.status.includes("TRỐNG VIỆC")) { wlClass = "bg-sky-500/10 text-sky-400 border border-sky-500/20"; wlText = "Trống việc"; }
        
        const activeProjs = p.projects.active.join(", ") || "-";
        
        let scoreHTML = "";
        if (currentTimeRange === "daily") {
          const rep = rawReports[p.group]?.[name]?.reports?.[currentSelectedDate];
          scoreHTML = rep ? `<span class="px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[9px] font-bold">ĐÃ NỘP</span>` : `<span class="px-1.5 py-0.5 rounded bg-red-500/10 text-red-400 border border-red-500/20 text-[9px] font-bold">THIẾU</span>`;
        } else {
          scoreHTML = `<strong class="font-mono text-gray-300">${p.work_score.toFixed(1)}/100</strong>`;
        }
        
        const tr = document.createElement("tr");
        const rowBg = globalIdx % 2 === 0 ? "bg-gray-900/10" : "bg-transparent";
        tr.className = `${rowBg} hover:bg-gray-800/30 border-b border-gray-800/30 transition cursor-pointer`;
        tr.onclick = () => { openStaffDrawer(name); };
        
        tr.innerHTML = `
          <td class="p-3.5 font-bold text-white hover:text-blue-400 transition">${name}</td>
          <td class="p-3.5 text-gray-400 text-xs">${p.group}</td>
          <td class="p-3.5"><span class="px-2.5 py-0.5 rounded border text-[10px] font-bold ${wlClass}">${wlText}</span></td>
          <td class="p-3.5"><div class="max-w-[200px] truncate text-gray-400 text-xs" title="${activeProjs}">${activeProjs}</div></td>
          <td class="p-3.5 text-right font-bold text-gray-300">${wl.active_count}</td>
          <td class="p-3.5 text-right font-bold ${wl.overdue_count > 0 ? 'text-red-400' : 'text-gray-500'}">${wl.overdue_count}</td>
          <td class="p-3.5 text-right font-mono text-gray-300 font-semibold">${p.hours.toFixed(1)}h</td>
          <td class="p-3.5 text-right">${scoreHTML}</td>
        `;
        tbody.appendChild(tr);
      });
      
      document.getElementById("tbl-total-count").textContent = `Hiển thị: ${displayedCount}/${totalCount} nhân sự`;
      
      // Render pagination controls
      const pagControls = document.getElementById("pagination-controls");
      if (displayedCount > 0) {
        const startNum = startIdx + 1;
        const endNum = Math.min(startIdx + rowsPerPage, displayedCount);
        
        const prevDisabled = currentPage === 1 ? "opacity-40 pointer-events-none" : "hover:bg-gray-800 hover:text-white";
        const nextDisabled = currentPage === totalPages ? "opacity-40 pointer-events-none" : "hover:bg-gray-800 hover:text-white";
        
        pagControls.innerHTML = `
          <div>
            Hiển thị <strong class="text-gray-300">${startNum}-${endNum}</strong> trên tổng số <strong class="text-gray-300">${displayedCount}</strong> giảng viên được lọc
          </div>
          <div class="flex gap-2">
            <button class="px-3 py-1.5 rounded-lg border border-gray-800 bg-gray-950/60 font-semibold transition ${prevDisabled}" onclick="changePage(${currentPage - 1})"><i class="fa-solid fa-angle-left mr-1"></i>Trước</button>
            <span class="px-3 py-1.5 font-mono font-bold text-gray-300 bg-gray-900 border border-gray-800/80 rounded-lg">Trang ${currentPage} / ${totalPages}</span>
            <button class="px-3 py-1.5 rounded-lg border border-gray-800 bg-gray-950/60 font-semibold transition ${nextDisabled}" onclick="changePage(${currentPage + 1})">Sau<i class="fa-solid fa-angle-right ml-1"></i></button>
          </div>
        `;
      } else {
        pagControls.innerHTML = `<div class="text-center w-full text-gray-500 italic py-1">Không có nhân sự nào khớp bộ lọc.</div>`;
      }
    }
    
    function changePage(page) {
      currentPage = page;
      renderStaffSummaryTable();
    }
    
    // Switch Filter Tab
    function switchDept(dept) {
      currentDepartment = dept;
      currentPage = 1;
      
      const tabBtns = document.querySelectorAll("#dept-tabs button");
      const deptNames = ["all", "Khối CNTT", "Khối QTKD", "Khối QLCLĐT", "Khối Ngoại ngữ và kỹ năng mềm"];
      
      tabBtns.forEach((btn, idx) => {
        if (deptNames[idx] === dept) {
          btn.className = "px-4 py-1.5 rounded-lg text-xs font-bold transition text-white bg-blue-600";
        } else {
          btn.className = "px-4 py-1.5 rounded-lg text-xs font-bold transition text-gray-400 hover:text-white";
        }
      });
      
      refreshDashboard();
    }
    
    function switchWorkloadFilter(wlFilter) {
      currentWorkloadFilter = wlFilter;
      currentPage = 1;
      
      const filterBtns = document.querySelectorAll("#workload-filters button");
      const filterKeys = ["all", "overloaded", "idle", "balanced"];
      
      filterBtns.forEach((btn, idx) => {
        if (filterKeys[idx] === wlFilter) {
          btn.className = "px-3 py-1 rounded-lg text-[10px] font-bold transition text-white bg-gray-800";
        } else {
          btn.className = "px-3 py-1 rounded-lg text-[10px] font-bold transition text-gray-400 hover:text-white";
        }
      });
      
      refreshDashboard();
    }
    
    function filterStaffTable(query) {
      searchQuery = stripAccents(query);
      currentPage = 1;
      renderStaffSummaryTable();
    }
    
    // Slide-over Drawer controller
    function openStaffDrawer(name) {
      currentStaff = name;
      const p = jsPersonnel[name];
      if (!p) return;
      
      // Fill drawer header
      document.getElementById("staff-avatar").textContent = name[0];
      document.getElementById("lbl-staff-role").textContent = `${p.role} (Rank ${p.rank})`;
      
      let hoursStr = "";
      if (currentTimeRange === "daily") {
        hoursStr = `${p.hours.toFixed(1)}h logs (Kỳ ngày)`;
      } else {
        hoursStr = `${p.hours.toFixed(1)}h (Logs ${p.reported_days}/${p.expected_days} ngày)`;
      }
      document.getElementById("lbl-staff-hours").textContent = hoursStr;
      
      let scoreStr = "";
      if (currentTimeRange === "daily") {
        scoreStr = p.hours > 0 ? "ĐÃ NỘP BÁO CÁO" : "THIẾU BÁO CÁO";
        document.getElementById("lbl-staff-score-title").textContent = "Báo cáo ngày";
        document.getElementById("lbl-staff-score").className = p.hours > 0 ? "text-[11px] font-semibold mt-1 block text-emerald-400" : "text-[11px] font-semibold mt-1 block text-red-400";
      } else {
        scoreStr = `${p.work_score.toFixed(1)}/100 (NS: ${p.proposed_ns.toFixed(2)})`;
        document.getElementById("lbl-staff-score-title").textContent = "Điểm tuân thủ";
        document.getElementById("lbl-staff-score").className = "text-[11px] font-semibold mt-1 block text-blue-400";
      }
      document.getElementById("lbl-staff-score").textContent = scoreStr;
      
      let execFaultsCount = 0;
      let reviewFaultsCount = 0;
      let execDetails = [];
      let reviewDetails = [];
      let datesToScanHist = [];
      
      if (currentTimeRange === "daily") {
        datesToScanHist = [currentSelectedDate];
      } else if (currentTimeRange === "weekly") {
        datesToScanHist = datesWeekly;
      } else {
        datesToScanHist = datesMonthly;
      }
      
      datesToScanHist.forEach(d => {
        if (historicalKPI && historicalKPI[d] && historicalKPI[d][name]) {
          const faults = historicalKPI[d][name];
          if (faults.execution_faults) {
            Object.keys(faults.execution_faults).forEach(prj => {
               execFaultsCount += faults.execution_faults[prj].count;
               execDetails.push(`[Thi công] ${prj}: ${faults.execution_faults[prj].count} task`);
            });
          }
          if (faults.review_faults) {
            Object.keys(faults.review_faults).forEach(prj => {
               reviewFaultsCount += faults.review_faults[prj].count;
               reviewDetails.push(`[Giam bài] ${prj}: ${faults.review_faults[prj].count} task`);
            });
          }
        }
      });
      
      let histText = "";
      if (execFaultsCount > 0 || reviewFaultsCount > 0) {
        histText = `<br><strong class="text-red-400">Lịch sử vi phạm (Kỳ này): ${execFaultsCount + reviewFaultsCount} lỗi</strong>`;
        if (execFaultsCount > 0) {
           histText += `<br><span class="text-red-400 text-[10px] font-bold pl-2 inline-flex items-center gap-1 mt-1"><span class="px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30 text-[8px] uppercase">🔴 Lỗi thi công</span> ${execFaultsCount} task</span>`;
           const uniqueExec = [...new Set(execDetails)];
           histText += `<span class="text-gray-400 text-[9px] pl-4 block mt-0.5">${uniqueExec.join('<br>')}</span>`;
        }
        if (reviewFaultsCount > 0) {
           histText += `<br><span class="text-amber-400 text-[10px] font-bold pl-2 inline-flex items-center gap-1 mt-1"><span class="px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 text-[8px] uppercase">🟧 Lỗi chậm duyệt (PIC)</span> ${reviewFaultsCount} task</span>`;
           const uniqueRev = [...new Set(reviewDetails)];
           histText += `<span class="text-gray-400 text-[9px] pl-4 block mt-0.5">${uniqueRev.join('<br>')}</span>`;
        }
      } else {
        histText = `<br><strong class="text-emerald-400">Lịch sử vi phạm (Kỳ này):</strong> 0 lượt trễ hạn.`;
      }
      
      document.getElementById("lbl-staff-eval").innerHTML = `<strong>Phân tải:</strong> ${p.workload.status} (${p.workload.reason}). <br><strong>Nhận xét:</strong> ${p.evaluation || 'Chưa ghi nhận đánh giá riêng.'}${histText}`;
      
      // Diffs & Uncompleted
      const diffUl = document.getElementById("lbl-staff-diffs");
      diffUl.innerHTML = "";
      if (p.difficulties && p.difficulties.length > 0) {
        p.difficulties.forEach(d => {
          const li = document.createElement("li");
          li.className = "py-1 border-b border-gray-800/40 last:border-b-0";
          li.innerHTML = `<span class="text-amber-500 font-mono">[${d.date.slice(8,10)}/${d.date.slice(5,7)}]</span>: ${d.content}`;
          diffUl.appendChild(li);
        });
      } else {
        diffUl.innerHTML = `<li class="text-gray-500 italic py-0.5">Không ghi nhận khó khăn.</li>`;
      }
      
      const uncompletedUl = document.getElementById("lbl-staff-uncompleted");
      uncompletedUl.innerHTML = "";
      if (p.uncompleted_tasks && p.uncompleted_tasks.length > 0) {
        p.uncompleted_tasks.forEach(u => {
          const li = document.createElement("li");
          li.className = "py-1 border-b border-gray-800/40 last:border-b-0";
          li.innerHTML = `<span class="text-red-400 font-mono">[${u.date.slice(8,10)}/${u.date.slice(5,7)}]</span>: ${u.title} (${u.percent}%)`;
          uncompletedUl.appendChild(li);
        });
      } else {
        uncompletedUl.innerHTML = `<li class="text-gray-500 italic py-0.5">Không có task tồn đọng.</li>`;
      }
      
      // Personal projects grid
      const projGrid = document.getElementById("staff-detail-projects");
      projGrid.innerHTML = "";
      if (p.projects.all && p.projects.all.length > 0) {
        p.projects.all.forEach(proj => {
          const div = document.createElement("div");
          div.className = "p-3.5 rounded-xl bg-gray-950/50 border border-gray-800 text-[10px] space-y-1.5";
          
          let healthColor = "text-emerald-400";
          if (proj.health === "OFF_TRACK" || proj.health === "AT_RISK") healthColor = "text-red-400";
          
          let badgeClass = "bg-blue-500/20 text-blue-400 border border-blue-500/30";
          if (proj.status === "COMPLETED") badgeClass = "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";
          else if (proj.status === "PENDING" || proj.status === "FUTURE") badgeClass = "bg-purple-500/20 text-purple-400 border border-purple-500/30";
          
          div.innerHTML = `
            <h5 class="font-bold text-gray-200 text-[11px] leading-tight" title="${proj.key} - ${proj.name}">${proj.key} - ${proj.name}</h5>
            <div class="flex justify-between text-gray-500"><span>Vai trò:</span><strong class="text-blue-400">${proj.role}</strong></div>
            <div class="flex justify-between text-gray-500"><span>Sức khỏe:</span><strong class="${healthColor}">${proj.health}</strong></div>
            <div class="flex justify-between text-gray-500"><span>Trạng thái:</span><span class="px-1 py-0.5 rounded text-[8px] font-bold ${badgeClass}">${proj.status}</span></div>
          `;
          projGrid.appendChild(div);
        });
      } else {
        projGrid.innerHTML = `<div class="col-span-2 text-center text-gray-500 italic py-2 text-[10px]">Không tham gia dự án nào.</div>`;
      }
      
      // Tasks table
      const tbody = document.getElementById("tasks-tbody");
      tbody.innerHTML = "";
      
      let logsToRender = [];
      if (currentTimeRange === "daily") {
        const rep = rawReports[p.group]?.[name]?.reports?.[currentSelectedDate];
        if (rep) {
          rep.tasks.forEach(t => {
            logsToRender.push({
              date: currentSelectedDate,
              title: t.title,
              hours: parseFloat(t.hours || 0),
              project: rep.project || "Công việc chung"
            });
          });
        }
      } else {
        const dates_to_scan = currentTimeRange === "weekly" ? datesWeekly : datesMonthly;
        const staff_reports = rawReports[p.group]?.[name]?.reports || {};
        
        dates_to_scan.forEach(d => {
          const r = staff_reports[d];
          if (r) {
            r.tasks.forEach(t => {
              logsToRender.push({
                date: d,
                title: t.title,
                hours: parseFloat(t.hours || 0),
                project: r.project || "Công việc chung"
              });
            });
          }
        });
      }
      
      if (logsToRender.length > 0) {
        logsToRender.sort((a,b) => b.date.localeCompare(a.date)).forEach(log => {
          const tr = document.createElement("tr");
          tr.className = "task-row border-b border-gray-800/40 hover:bg-gray-800/10 transition";
          
          tr.innerHTML = `
            <td class="p-2 font-mono text-[9px] text-gray-400">${log.date.slice(8,10)}/${log.date.slice(5,7)}</td>
            <td class="p-2 font-semibold text-gray-200">${log.title}</td>
            <td class="p-2 text-right font-mono font-medium text-gray-300">${log.hours.toFixed(1)}h</td>
            <td class="p-2"><span class="px-1.5 py-0.5 rounded text-[8px] font-bold bg-purple-500/15 text-purple-400 border border-purple-500/20 truncate max-w-[80px] block">${log.project}</span></td>
          `;
          tbody.appendChild(tr);
        });
      } else {
        tbody.innerHTML = `<tr><td colspan="4" class="p-3 text-center text-gray-500 italic">Không ghi nhận nhật ký công việc.</td></tr>`;
      }
      
      // Render personal doughnut chart
      updateIndividualChart(p);
      
      // Open panels
      document.getElementById("detail-drawer").classList.add("open");
      document.getElementById("drawer-overlay").classList.add("open");
    }
    
    function closeDrawer() {
      document.getElementById("detail-drawer").classList.remove("open");
      document.getElementById("drawer-overlay").classList.remove("open");
    }
    
    function filterTasks(query) {
      const q = query.toLowerCase().trim();
      const rows = document.querySelectorAll("#tasks-tbody .task-row");
      rows.forEach(r => {
        const text = r.textContent.toLowerCase();
        r.style.display = text.includes(q) ? "" : "none";
      });
    }
    
    // Charts update functions
    function updateOverallCharts() {
      // 1. Stacked Workload Chart or Department Doughnut Chart
      const wlCtx = document.getElementById('deptWorkloadChart').getContext('2d');
      
      const filteredStaff = Object.values(jsPersonnel).filter(p => {
        return currentDepartment === "all" || p.group === currentDepartment;
      });
      
      if (currentDepartment === "all") {
        const blocks = [];
        const overloaded = [];
        const balanced = [];
        const idle = [];
        
        const counts = {};
        Object.values(jsPersonnel).forEach(p => {
          const g = p.group;
          const wl = p.workload.status;
          if (!counts[g]) counts[g] = { overloaded: 0, balanced: 0, idle: 0 };
          if (wl.startsWith("QUÁ TẢI")) counts[g].overloaded++;
          else if (wl === "TRỐNG VIỆC / SẴN SÀNG") counts[g].idle++;
          else counts[g].balanced++;
        });
        
        Object.keys(counts).sort().forEach(b => {
          blocks.push(b.replace("Khối ", "").slice(0, 10) + "...");
          overloaded.push(counts[b].overloaded);
          balanced.push(counts[b].balanced);
          idle.push(counts[b].idle);
        });
        
        if (workloadChart) workloadChart.destroy();
        workloadChart = new Chart(wlCtx, {
          type: 'bar',
          data: {
            labels: blocks,
            datasets: [
              { label: 'Quá tải', data: overloaded, backgroundColor: '#ef4444' },
              { label: 'Cân bằng', data: balanced, backgroundColor: '#10b981' },
              { label: 'Trống việc', data: idle, backgroundColor: '#0ea5e9' }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              x: { stacked: true, grid: { display: false }, ticks: { color: '#9ca3af', font: { size: 10 } } },
              y: { stacked: true, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#f3f4f6', font: { size: 10 }, stepSize: 1 } }
            }
          }
        });
      } else {
        // Draw Doughnut Chart representing workload allocation of selected department
        const pOverloaded = filteredStaff.filter(p => p.workload.status.startsWith("QUÁ TẢI")).length;
        const pIdle = filteredStaff.filter(p => p.workload.status === "TRỐNG VIỆC / SẴN SÀNG").length;
        const pBalanced = filteredStaff.length - pOverloaded - pIdle;
        
        if (workloadChart) workloadChart.destroy();
        workloadChart = new Chart(wlCtx, {
          type: 'doughnut',
          data: {
            labels: ['Quá tải', 'Cân bằng', 'Trống việc'],
            datasets: [{
              data: [pOverloaded, pBalanced, pIdle],
              backgroundColor: ['#ef4444', '#10b981', '#0ea5e9'],
              borderColor: '#111827',
              borderWidth: 1.5
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: true, labels: { color: '#9ca3af', font: { size: 9 } } } },
            cutout: '60%'
          }
        });
      }
      
      // 2. Overdue Projects - Bounded to TOP 5 most critical (scoped by global department filter)
      const odCtx = document.getElementById('overdueProjectsChart').getContext('2d');
      
      const filteredProjects = jsProjects.filter(pr => {
        if (currentDepartment === "all") return true;
        return pr.members.some(m => {
          const staffMeta = jsPersonnel[m];
          return staffMeta && staffMeta.group === currentDepartment;
        });
      });
      
      const overdueList = filteredProjects.map(p => {
        const displayName = p.name.length > 22 ? p.name.slice(0, 22) + "..." : p.name;
        return {
          label: p.key + " - " + displayName,
          overdue: p.stats.overdue
        };
      }).filter(x => x.overdue > 0).sort((a,b) => b.overdue - a.overdue).slice(0, 5);
      
      const odLabels = overdueList.map(d => d.label);
      const odValues = overdueList.map(d => d.overdue);
      
      if (overdueChart) overdueChart.destroy();
      overdueChart = new Chart(odCtx, {
        type: 'bar',
        data: {
          labels: odLabels,
          datasets: [{ data: odValues, backgroundColor: 'rgba(239, 68, 68, 0.65)', borderColor: '#ef4444', borderWidth: 1.5, borderRadius: 3 }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af', font: { size: 10 }, stepSize: 1 } },
            y: { grid: { display: false }, ticks: { color: '#f3f4f6', font: { size: 10 } } }
          }
        }
      });
      
      // 3. Update Trend Chart dynamically based on filters
      updateTrendChart();
    }
    
    function updateTrendChart() {
      const trendCtx = document.getElementById('deptTrendChart').getContext('2d');
      const labels = [];
      const hoursData = [];
      const complianceData = [];
      const unmappedHoursData = [];
      const plannedKpiData = [];
      
      const weeksDefinition = {
        "T27": ["2026-07-01", "2026-07-02", "2026-07-03"],
        "T28": ["2026-07-06", "2026-07-07", "2026-07-08", "2026-07-09", "2026-07-10"],
        "T29": ["2026-07-13", "2026-07-14", "2026-07-15", "2026-07-16", "2026-07-17"],
        "T30": ["2026-07-20", "2026-07-21", "2026-07-22", "2026-07-23", "2026-07-24"],
        "T31": ["2026-07-27", "2026-07-28", "2026-07-29", "2026-07-30", "2026-07-31"]
      };
      
      Object.keys(weeksDefinition).forEach(weekLabel => {
        labels.push(weekLabel);
        const days = weeksDefinition[weekLabel];
        
        let mappedHours = 0.0;
        let unmappedHours = 0.0;
        let expectedDays = 0;
        let completedDays = 0;
        
        Object.keys(jsPersonnel).forEach(name => {
          const p = jsPersonnel[name];
          if (currentDepartment !== "all" && p.group !== currentDepartment) {
            return;
          }
          
          const staff_reports = rawReports[p.group]?.[name]?.reports || {};
          days.forEach(d => {
            expectedDays += 1;
            const rep = staff_reports[d];
            if (rep) {
              completedDays += 1;
              rep.tasks.forEach(t => {
                const title = (t.title || "").toLowerCase();
                const hours = parseFloat(t.hours || 0);
                
                // Heuristic mapped check
                const kpiKeywords = ["giảng dạy", "chuẩn bị", "xây dựng", "thực hành", "chấm", "trông thi", "kiểm tra", "bài tập", "hỗ trợ", "mindmap", "slide", "quiz", "hkt", "họp", "trợ giảng"];
                let isMapped = false;
                for (let i = 0; i < kpiKeywords.length; i++) {
                  if (title.includes(kpiKeywords[i])) {
                    isMapped = true;
                    break;
                  }
                }
                
                if (isMapped) {
                  mappedHours += hours;
                } else {
                  unmappedHours += hours;
                }
              });
            }
          });
        });
        
        // Quy đổi về trung bình đầu người mỗi ngày trong tuần
        const avgMapped = expectedDays > 0 ? (mappedHours / expectedDays) : 0;
        const avgUnmapped = expectedDays > 0 ? (unmappedHours / expectedDays) : 0;
        
        hoursData.push(Number(avgMapped.toFixed(2)));
        unmappedHoursData.push(Number(avgUnmapped.toFixed(2)));
        
        // planned KPI hours cố định là 8.0h/ngày
        plannedKpiData.push(8.0);
        
        const comp = expectedDays > 0 ? (completedDays / expectedDays) * 100 : 0;
        complianceData.push(Number(comp.toFixed(1)));
      });
      
      if (trendChart) trendChart.destroy();
      trendChart = new Chart(trendCtx, {
        data: {
          labels: labels,
          datasets: [
            {
              type: 'bar',
              label: 'Giờ chuẩn/ngày (Mapped)',
              data: hoursData,
              backgroundColor: 'rgba(16, 185, 129, 0.8)',
              borderColor: 'rgba(16, 185, 129, 1)',
              yAxisID: 'y',
              borderWidth: 1,
              stack: 'Stack 0'
            },
            {
              type: 'bar',
              label: 'Giờ phát sinh/ngày (Unmapped)',
              data: unmappedHoursData,
              backgroundColor: 'rgba(245, 158, 11, 0.8)',
              borderColor: 'rgba(245, 158, 11, 1)',
              yAxisID: 'y',
              borderWidth: 1,
              stack: 'Stack 0'
            },
            {
              type: 'line',
              label: 'Định mức 8h/ngày',
              data: plannedKpiData,
              borderColor: 'rgba(239, 68, 68, 0.9)',
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              borderDash: [5, 5],
              yAxisID: 'y',
              tension: 0.1,
              fill: false
            },
            {
              type: 'line',
              label: 'Tuân thủ (%)',
              data: complianceData,
              borderColor: '#3b82f6',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              yAxisID: 'y1',
              tension: 0.3,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: true, position: 'bottom', labels: { color: '#9ca3af', font: { size: 10 } } } },
          scales: {
            x: { 
              stacked: true,
              grid: { display: false }, 
              ticks: { color: '#9ca3af', font: { size: 10 } } 
            },
            y: {
              type: 'linear',
              display: true,
              position: 'left',
              stacked: true,
              title: { display: true, text: 'Số giờ TB / ngày (h)', color: '#9ca3af', font: { size: 9 } },
              grid: { color: 'rgba(255,255,255,0.05)' },
              ticks: { color: '#9ca3af', font: { size: 10 } }
            },
            y1: {
              type: 'linear',
              display: true,
              position: 'right',
              grid: { drawOnChartArea: false },
              ticks: { color: '#3b82f6', font: { size: 10 }, min: 0, max: 100 }
            }
          }
        }
      });
    }
    
    function updateIndividualChart(p) {
      const ctx = document.getElementById('individualChart').getContext('2d');
      const wl = p.workload;
      const dataValues = [wl.active_count - wl.overdue_count - wl.urgent_count, wl.overdue_count, wl.urgent_count];
      
      if (individualChart) individualChart.destroy();
      individualChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Bình thường', 'Quá hạn', 'Cận hạn'],
          datasets: [{
            data: dataValues,
            backgroundColor: ['#3b82f6', '#ef4444', '#f59e0b'],
            borderColor: '#111827',
            borderWidth: 1.5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          cutout: '65%'
        }
      });
    }
    
    function switchCycle(cycle) {
      currentCycle = cycle;
      
      const btnAug = document.getElementById("btn-cycle-aug");
      const btnJul = document.getElementById("btn-cycle-jul");
      const btnCustom = document.getElementById("btn-cycle-custom");
      const customInputs = document.getElementById("custom-date-inputs");
      
      btnAug.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold text-gray-400 transition";
      btnJul.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold text-gray-400 transition";
      btnCustom.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold text-gray-400 transition";
      customInputs.classList.add("hidden");
      
      if (cycle === "aug") {
        btnAug.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 transition";
        currentStartDate = "2026-08-01";
        currentEndDate = yesterday.startsWith("2026-08") ? yesterday : "2026-08-31";
      } else if (cycle === "jul") {
        btnJul.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 transition";
        currentStartDate = "2026-07-01";
        currentEndDate = "2026-07-31";
      } else if (cycle === "custom") {
        btnCustom.className = "px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 transition";
        customInputs.classList.remove("hidden");
        
        const startInp = document.getElementById("input-start-date");
        const endInp = document.getElementById("input-end-date");
        if (!startInp.value) startInp.value = currentStartDate;
        if (!endInp.value) endInp.value = currentEndDate;
        
        currentStartDate = startInp.value;
        currentEndDate = endInp.value;
      }
      
      if (currentSelectedDate < currentStartDate || currentSelectedDate > currentEndDate) {
        currentSelectedDate = currentEndDate;
      }
      
      populateDateSelect();
      refreshDashboard();
      
      if (currentStaff) {
        openStaffDrawer(currentStaff);
      }
    }
    
    function customDateChanged() {
      const startInp = document.getElementById("input-start-date");
      const endInp = document.getElementById("input-end-date");
      if (startInp.value && endInp.value) {
        currentStartDate = startInp.value;
        currentEndDate = endInp.value;
        
        if (currentSelectedDate < currentStartDate || currentSelectedDate > currentEndDate) {
          currentSelectedDate = currentEndDate;
        }
        
        populateDateSelect();
        refreshDashboard();
        
        if (currentStaff) {
          openStaffDrawer(currentStaff);
        }
      }
    }

    function populateDateSelect() {
      const select = document.getElementById("date-select");
      select.innerHTML = "";
      
      if (currentTimeRange === "daily") {
        select.style.display = "";
        const allDates = [...datesMonthly].filter(d => d >= currentStartDate && d <= currentEndDate).sort((a,b) => b.localeCompare(a));
        allDates.forEach(d => {
          const opt = document.createElement("option");
          opt.value = d;
          opt.textContent = d.slice(8,10) + "/" + d.slice(5,7) + "/" + d.slice(0,4);
          if (d === currentSelectedDate) {
            opt.selected = true;
          }
          select.appendChild(opt);
        });
      } else {
        select.style.display = "none";
      }
    }
    
    function switchTimeRange(range) {
      currentTimeRange = range;
      
      const btns = {
        daily: document.getElementById("btn-daily"),
        weekly: document.getElementById("btn-weekly"),
        monthly: document.getElementById("btn-monthly")
      };
      
      Object.keys(btns).forEach(k => {
        if (k === range) {
          btns[k].className = "px-4 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 transition";
        } else {
          btns[k].className = "px-4 py-1.5 rounded-lg text-xs font-semibold text-gray-400 transition";
        }
      });
      
      const thHours = document.getElementById("th-range-hours");
      const thComp = document.getElementById("th-range-compliance");
      
      if (range === "daily") {
        thHours.textContent = "Số giờ logs";
        thComp.textContent = "Báo cáo ngày";
        currentSelectedDate = currentEndDate;
      } else if (range === "weekly") {
        thHours.textContent = "Giờ logs tuần";
        thComp.textContent = "Điểm tuân thủ";
      } else {
        thHours.textContent = "Giờ logs tháng";
        thComp.textContent = "Điểm tuân thủ";
      }
      
      populateDateSelect();
      refreshDashboard();
      
      // Sync drawer if open
      if (currentStaff) {
        openStaffDrawer(currentStaff);
      }
    }
    
    function switchDate(dateStr) {
      currentSelectedDate = dateStr;
      refreshDashboard();
      
      // Sync drawer if open
      if (currentStaff) {
        openStaffDrawer(currentStaff);
      }
    }
    
    // Core state re-render
    function refreshDashboard() {
      calculateSystemState();
      updateMetricsWidgets();
      updateAlertsWidget();
      renderStaffSummaryTable();
      updateOverallCharts();
    }
    
    window.onload = function() {
      // Initialize start and end dates based on default cycle (aug)
      currentStartDate = "2026-08-01";
      currentEndDate = yesterday.startsWith("2026-08") ? yesterday : "2026-08-31";
      currentSelectedDate = currentEndDate;
      
      populateDateSelect();
      refreshDashboard();
      
      // Attempt silent live fetch in background if served via HTTP server
      fetchLiveDashboardData(false);
    };
  </script>
</body>
</html>
"""

    # Substitution placeholders
    html_output = html_template
    html_output = html_output.replace("__RAW_REPORTS__", json.dumps(raw_reports, ensure_ascii=False))
    html_output = html_output.replace("__PROJECTS_DATA__", json.dumps(projects_list, ensure_ascii=False))
    html_output = html_output.replace("__PERSONNEL_DATA__", json.dumps(personnel_list, ensure_ascii=False))
    html_output = html_output.replace("__DATES_MONTHLY__", json.dumps(dates_monthly, ensure_ascii=False))
    html_output = html_output.replace("__DATES_WEEKLY__", json.dumps(dates_weekly, ensure_ascii=False))
    html_output = html_output.replace("__YESTERDAY__", yesterday)
    html_output = html_output.replace("__HISTORICAL_KPI__", json.dumps(historical_kpi, ensure_ascii=False))

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"HTML Dashboard generated successfully at: {output_html_path}")

if __name__ == "__main__":
    main()

import json
import sys
import os
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

# Paths
processed_logs_path = r"c:\Users\DELL\Desktop\AI-Agent\AI_Report_QTKD\scratch\processed_reports_weekly.json"
project_issues_path = r"c:\Users\DELL\Desktop\AI-Agent\AI_Report_QTKD\scratch\project_issues.json"
daily_log_analysis_path = r"c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\data\daily_log_analysis.json"
output_html_path = r"c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\output\4_daily_logs_report.html"
output_md_path = r"c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\output\4_daily_logs_report.md"

# Load data
with open(daily_log_analysis_path, "r", encoding="utf-8") as f:
    analysis_data = json.load(f)
    
with open(project_issues_path, "r", encoding="utf-8") as f:
    project_data = json.load(f)

weekly_stats = analysis_data["weekly_stats"]
monthly_stats = analysis_data["monthly_stats"]
raw_reports = analysis_data["raw_reports"]

dates_weekly = analysis_data.get("dates_weekly", [])
dates_monthly = analysis_data.get("dates_monthly", [])
yesterday_str = analysis_data.get("yesterday", "")
missing_yesterday = analysis_data.get("missing_yesterday", [])

# Tính toán các chuỗi phạm vi ngày để hiển thị an toàn
if dates_weekly:
    weekly_range_str = f"{dates_weekly[0].split('-')[2]}/{dates_weekly[0].split('-')[1]} - {dates_weekly[-1].split('-')[2]}/{dates_weekly[-1].split('-')[1]}/{dates_weekly[-1].split('-')[0]}"
else:
    weekly_range_str = "Chưa có dữ liệu tuần"
    
if dates_monthly:
    monthly_range_str = f"{dates_monthly[0].split('-')[2]}/{dates_monthly[0].split('-')[1]} - {dates_monthly[-1].split('-')[2]}/{dates_monthly[-1].split('-')[1]}/{dates_monthly[-1].split('-')[0]}"
else:
    monthly_range_str = "Chưa có dữ liệu tháng"
    
yesterday_formatted = ""
if yesterday_str:
    yesterday_parts = yesterday_str.split('-')
    if len(yesterday_parts) == 3:
        yesterday_formatted = f"{yesterday_parts[2]}/{yesterday_parts[1]}/{yesterday_parts[0]}"

# Sắp xếp xếp hạng tháng 7
sorted_monthly = sorted(monthly_stats.items(), key=lambda x: x[1]["work_score"], reverse=True)
top_performers = sorted_monthly[:5]
# Loại bỏ những người có work_score = 0.0 khỏi bottom performers nếu cả lớp không có ai bị thấp, 
# hoặc lấy 5 người có điểm thấp nhất
bottom_performers = sorted_monthly[-5:]  # Lấy 5 người có điểm thấp nhất (ở cuối danh sách đã sắp xếp tăng dần từ thấp lên cao nếu đảo ngược)
# Đảo ngược bottom_performers để người thấp nhất hiển thị trước hoặc sau
bottom_performers = bottom_performers[::-1]

# Dữ liệu biểu đồ Tháng 7 của 39 nhân sự
chart_monthly_names = [item[1]["name"] for item in sorted_monthly]
chart_monthly_scores = [item[1]["work_score"] for item in sorted_monthly]

target_groups = {
    "Khối QTKD": [
        "Hoàng Thị Kim Oanh",
        "Hoàng Thị Hậu",
        "Nguyễn Thị Hồng Minh",
        "Đặng Quỳnh Trang",
        "Nguyễn Ngọc Vân Khanh",
        "Lê Thành Ngọc"
    ],
    "Khối CNTT": [
        "Trịnh Quốc Hai",
        "Nguyễn Quảng An",
        "Lương Quốc Tuấn",
        "Phạm Ngọc Kiên",
        "Lại Trung Lâm",
        "Lâm Tùng Dương",
        "Ngọ Văn Quý",
        "Trần Minh Cường",
        "Bùi Thanh Hải",
        "Mai Xuân Chinh",
        "Đinh Thành Nam",
        "Nguyễn Công Hưởng",
        "Phạm Tuấn Bình",
        "Nguyễn Bá Minh Đạo",
        "Lê Hà Thanh Sang",
        "Phạm Viết Hùng",
        "Trần Quốc Tuấn",
        "Nguyễn Văn A",
        "Nguyễn Thanh Bình Phước"
    ],
    "Khối Ngoại ngữ và kỹ năng mềm": [
        "Giáp Thị Minh Hằng",
        "Lò Thị Ngọc Anh",
        "Lê Thị Đỏ",
        "Ngô Quang Huấn",
        "Lê Nhựt Mi",
        "Lê Thị Bảo Yến",
        "Triệu Thị Thanh Tâm"
    ],
    "Khối QLCLĐT": [
        "Nguyễn Thị Tươi",
        "Trần Thị Mỹ Phước",
        "Nguyễn Huyền Trang",
        "Nguyễn Xuân Bách",
        "Đặng Minh Luân",
        "Nguyễn Ngọc Sơn",
        "Lưu Xuân Hoàng Nguyên",
        "Nguyễn Đức Minh",
        "Nguyễn Thị Như Quỳnh",
        "Phan Ngọc Tài",
        "Trần Thị B"
    ]
}

groups_ordered = [
    "Khối CNTT",
    "Khối QTKD",
    "Khối Ngoại ngữ và kỹ năng mềm",
    "Khối QLCLĐT"
]

# Process project issues & Critical Alerts
due_issues = []
overdue_issues = []
done_count = 0
pending_count = 0
todo_count = 0
cancel_count = 0

for key, p_data in project_data.items():
    proj = p_data["project_info"]
    issues = p_data.get("issues", {}).get("issues", [])
    for issue in issues:
        state = issue.get("state")
        
        # Count states for Chart.js
        if state == "Hoàn thành":
            done_count += 1
        elif state == "Chờ duyệt":
            pending_count += 1
        elif state in ["Cần làm", "Tồn đọng", "Đang làm"]:
            todo_count += 1
        elif state == "Hủy":
            cancel_count += 1
            
        due = issue.get("dueDate")
        if due:
            day = due.split("T")[0]
            # Calculate current week start/end dynamically
            today = datetime.now().date()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=4)
            start_of_week_str = start_of_week.strftime("%Y-%m-%d")
            end_of_week_str = end_of_week.strftime("%Y-%m-%d")
            
            # Tasks due this week
            if start_of_week_str <= day <= end_of_week_str:
                due_issues.append({
                    "project_key": key,
                    "project_name": proj["name"],
                    "issue_code": issue["code"],
                    "title": issue["title"],
                    "state": state,
                    "assignee": issue["assignee"],
                    "dueDate": day
                })
            # Overdue tasks (due before this week start and not Done/Cancel)
            if day < start_of_week_str and state not in ["Hoàn thành", "Hủy"]:
                overdue_issues.append({
                    "project_key": key,
                    "project_name": proj["name"],
                    "issue_code": issue["code"],
                    "title": issue["title"],
                    "state": state,
                    "assignee": issue["assignee"] if issue["assignee"] else "Chưa phân công",
                    "dueDate": day
                })

# Lấy các dự án Off-track
off_track_projects = []
for key, p_data in project_data.items():
    proj = p_data["project_info"]
    if proj["health"] != "ON_TRACK":
        off_track_projects.append({
            "key": key,
            "name": proj["name"],
            "pic": proj["pic"]["name"] if proj["pic"] else "None",
            "health": proj["health"]
        })

# Generate project list statistics
project_list = []
for key, p_data in project_data.items():
    proj = p_data["project_info"]
    issues = p_data.get("issues", {}).get("issues", [])
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=4)
    start_of_week_str = start_of_week.strftime("%Y-%m-%d")
    end_of_week_str = end_of_week.strftime("%Y-%m-%d")
    
    p_due_issues = sum(1 for issue in issues if issue.get("dueDate") and start_of_week_str <= issue.get("dueDate").split("T")[0] <= end_of_week_str)
    project_list.append({
        "key": key,
        "name": proj["name"],
        "status": proj["status"],
        "health": proj["health"],
        "pic": proj["pic"]["name"] if proj["pic"] else "None",
        "total_issues": len(issues),
        "due_this_week": p_due_issues
    })

# Gather assignee-specific issue stats
person_project_stats = {}
for group, members in target_groups.items():
    for m in members:
        person_project_stats[m.strip().lower()] = {
            "name": m,
            "group": group,
            "due_issues_count": 0,
            "completed_issues_count": 0,
            "other_states": {}
        }

special_mappings = {
    "lưu hoàng xuân nguyên": "lưu xuân hoàng nguyên"
}
def normalize_name(name):
    norm = name.strip().lower()
    if norm in special_mappings:
        norm = special_mappings[norm]
    return norm

for issue in due_issues:
    assignee = issue["assignee"]
    if assignee:
        norm_assignee = normalize_name(assignee)
        if norm_assignee in person_project_stats:
            person_project_stats[norm_assignee]["due_issues_count"] += 1
            state = issue["state"]
            if state == "Hoàn thành":
                person_project_stats[norm_assignee]["completed_issues_count"] += 1
            else:
                person_project_stats[norm_assignee]["other_states"][state] = person_project_stats[norm_assignee]["other_states"].get(state, 0) + 1

# ----------------- BUILD HTML CONTENT -----------------
html_content = []
html_content.append(f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo thống kê công việc phòng Đào Tạo (Thống kê Tuần & Tháng)</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --primary: #6366f1;
            --primary-light: rgba(99, 102, 241, 0.15);
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
            --success: #10b981;
            --success-light: rgba(16, 185, 129, 0.1);
            --warning: #f59e0b;
            --warning-light: rgba(245, 158, 11, 0.15);
            --danger: #ef4444;
            --danger-light: rgba(239, 68, 68, 0.15);
            --bg-main: #0b0f19;
            --bg-card: rgba(22, 30, 49, 0.7);
            --border: rgba(255, 255, 255, 0.08);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --glass-bg: rgba(17, 24, 39, 0.6);
            --glass-border: rgba(255, 255, 255, 0.05);
            --neon-blue: #38bdf8;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.6;
            padding: 40px 20px;
            background-image: 
                radial-gradient(at 10% 20%, rgba(99, 102, 241, 0.1) 0px, transparent 50%),
                radial-gradient(at 90% 80%, rgba(6, 182, 212, 0.07) 0px, transparent 50%);
            background-attachment: fixed;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(16px);
            padding: 40px;
            border-radius: 28px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
            border: 1px solid var(--glass-border);
        }}

        header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 8px;
            height: 100%;
            background: var(--primary-gradient);
        }}

        header h1 {{
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 12px;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        header p {{
            font-size: 1.1rem;
            color: var(--text-muted);
            margin-bottom: 20px;
        }}

        header .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}

        header .meta-item {{
            background: rgba(15, 23, 42, 0.5);
            padding: 12px 20px;
            border-radius: 14px;
            font-size: 0.9rem;
            border: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        header .meta-item strong {{
            color: var(--neon-blue);
        }}

        .tabs-nav {{
            display: flex;
            gap: 12px;
            margin-bottom: 30px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 15px;
        }}

        .tab-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 10px 24px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            border-radius: 12px;
            transition: all 0.3s;
        }}

        .tab-btn:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }}

        .tab-btn.active {{
            color: #fff;
            background: var(--primary);
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
        }}

        .sub-tabs-container {{
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            background: rgba(15, 23, 42, 0.4);
            padding: 6px;
            border-radius: 14px;
            width: fit-content;
            border: 1px solid var(--border);
        }}

        .sub-tab-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 8px 20px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            border-radius: 10px;
            transition: all 0.3s;
        }}

        .sub-tab-btn.active {{
            color: #fff;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--border);
        }}

        .panel {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
        }}

        .panel-title {{
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 24px;
            color: #fff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 12px;
        }}

        .search-filter-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 24px;
        }}

        .search-box {{
            flex: 1;
            min-width: 250px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 12px 20px;
            color: #fff;
            font-family: inherit;
            font-size: 0.95rem;
            transition: border-color 0.3s;
        }}

        .search-box:focus {{
            outline: none;
            border-color: var(--primary);
        }}

        .filter-btn {{
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 10px 18px;
            border-radius: 12px;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .filter-btn:hover, .filter-btn.active {{
            color: #fff;
            border-color: var(--primary);
            background: var(--primary-light);
        }}

        .table-responsive {{
            width: 100%;
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}

        th {{
            padding: 16px 20px;
            background: rgba(15, 23, 42, 0.4);
            color: var(--text-muted);
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid var(--border);
        }}

        td {{
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            font-size: 0.95rem;
            color: #d1d5db;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
            color: #fff;
        }}

        .highlight-name {{
            font-weight: 600;
            color: #fff;
        }}

        .badge-status {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            text-align: center;
        }}

        .badge-status.success {{ background: var(--success-light); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.2); }}
        .badge-status.warning {{ background: var(--warning-light); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.2); }}
        .badge-status.danger {{ background: var(--danger-light); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.2); }}

        .progress-bar-container {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .progress-bar-bg {{
            width: 100px;
            height: 8px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 4px;
            overflow: hidden;
        }}

        .progress-bar-fill {{
            height: 100%;
            border-radius: 4px;
        }}

        .progress-bar-fill.high {{ background: var(--success); }}
        .progress-bar-fill.medium {{ background: var(--warning); }}
        .progress-bar-fill.low {{ background: var(--danger); }}

        .progress-label {{
            font-size: 0.85rem;
            font-weight: 700;
        }}

        .missing-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 16px;
        }}

        .missing-card {{
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .missing-card-name {{
            font-weight: 600;
            font-size: 0.95rem;
        }}

        .missing-card-group {{
            font-size: 0.78rem;
            color: var(--text-muted);
            display: block;
        }}

        .diff-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
        }}

        .diff-card {{
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            border-left: 4px solid var(--danger);
        }}

        .diff-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 0.85rem;
        }}

        .diff-user {{
            font-weight: 700;
            color: #fff;
        }}

        .diff-meta {{
            color: var(--text-muted);
        }}

        .diff-content {{
            font-size: 0.9rem;
            color: #d1d5db;
        }}

        /* Critical Alerts Style */
        .alert-section {{
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 24px;
            margin-bottom: 30px;
        }}

        @media (max-width: 900px) {{
            .alert-section {{
                grid-template-columns: 1fr;
            }}
        }}

        .alert-box {{
            background: rgba(239, 68, 68, 0.08);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 20px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .alert-box-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #f87171;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid rgba(239, 68, 68, 0.15);
            padding-bottom: 8px;
        }}

        .alert-item {{
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid rgba(239, 68, 68, 0.1);
            border-radius: 12px;
            padding: 12px 16px;
            font-size: 0.88rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .overdue-scroll-container {{
            max-height: 250px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding-right: 6px;
        }}

        .overdue-scroll-container::-webkit-scrollbar {{
            width: 6px;
        }}

        .overdue-scroll-container::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}

        .view-mode-container {{
            display: none;
        }}

        .view-mode-container.active {{
            display: block;
        }}

        /* Projects Section Grid */
        .project-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .project-card {{
            background: rgba(30, 41, 59, 0.35);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            transition: all 0.3s;
        }}

        .project-card:hover {{
            border-color: var(--primary);
            transform: translateY(-2px);
        }}

        .project-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .project-badge {{
            padding: 3px 10px;
            border-radius: 8px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
        }}

        .project-badge.active {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; }}
        .project-badge.completed {{ background: rgba(16, 185, 129, 0.15); color: var(--success); }}

        .project-card-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-main);
            height: 2.8rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .project-info-row {{
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            border-bottom: 1px dashed var(--border);
            padding-bottom: 8px;
            margin-bottom: 8px;
        }}

        .project-health-dot {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 6px;
        }}
        .project-health-dot.on-track {{ background: var(--success); box-shadow: 0 0 8px var(--success); }}
        .project-health-dot.off-track {{ background: var(--danger); box-shadow: 0 0 8px var(--danger); }}

        .chart-panel-grid {{
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 24px;
            margin-bottom: 30px;
        }}

        @media (max-width: 1000px) {{
            .chart-panel-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .chart-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 280px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Báo cáo thống kê công việc phòng Đào Tạo</h1>
            <p>Phân tích tích hợp chi tiết báo cáo ngày và quản lý tiến độ dự án đào tạo</p>
            <div class="meta-grid">
                <div class="meta-item">
                    <span>📅 Giai đoạn: <strong>{monthly_range_str}</strong></span>
                </div>
                <div class="meta-item">
                    <span>👥 Nhân sự: <strong>{len(weekly_stats)} nhân sự</strong></span>
                </div>
                <div class="meta-item">
                    <span>⚙️ KPI Master: <strong>Đã tích hợp (Bỏ qua task tự do)</strong></span>
                </div>
            </div>
        </header>

        <!-- Navigation Tabs -->
        <div class="tabs-nav">
            <button class="tab-btn active" onclick="switchTab(event, 'tab-logs')">📄 Nhật Ký Báo Cáo Ngày</button>
            <button class="tab-btn" onclick="switchTab(event, 'tab-projects')">📊 Tiến Độ Dự Án & KPI</button>
        </div>

        <!-- TAB 1: DAILY LOGS -->
        <div id="tab-logs" class="tab-content active">
            <!-- Time Sub-Tabs -->
            <div class="sub-tabs-container">
                <button class="sub-tab-btn active" onclick="switchViewMode(event, 'weekly')">Tuần Này (Tuần 29 - Tuần III tháng 7)</button>
                <button class="sub-tab-btn" onclick="switchViewMode(event, 'monthly')">Tháng Này (Tháng 7)</button>
            </div>

            <!-- SEARCH AND FILTER ROW -->
            <div class="search-filter-row">
                <input type="text" id="log-search" class="search-box" placeholder="Tìm kiếm theo tên thầy cô..." oninput="applyFilters()">
                <button class="filter-btn active" onclick="filterGroup(event, 'ALL')">Tất cả</button>
                <button class="filter-btn" onclick="filterGroup(event, 'Khối QTKD')">Khối QTKD</button>
                <button class="filter-btn" onclick="filterGroup(event, 'HN-KS25')">CNTT HN (KS25)</button>
                <button class="filter-btn" onclick="filterGroup(event, 'HN-KS24')">CNTT HN (KS24)</button>
                <button class="filter-btn" onclick="filterGroup(event, 'HCM')">CNTT HCM</button>
                <button class="filter-btn" onclick="filterGroup(event, 'Ngoại ngữ')">Ngoại ngữ</button>
                <button class="filter-btn" onclick="filterGroup(event, 'QLĐT')">Khối QLĐT</button>
            </div>

            <!-- VIEW MODE: WEEKLY -->
            <div id="view-weekly" class="view-mode-container active">
                <!-- Panel 0: Nhân Sự Chưa Báo Cáo Ngày Hôm Trước -->
                <div class="panel" style="border-left: 5px solid var(--danger);">
                    <div class="panel-title" style="color: var(--danger);">
                        <span>🚨 Nhân Sự Chưa Báo Cáo Ngày Hôm Trước ({yesterday_formatted})</span>
                    </div>
                    <div class="missing-grid">""")

# Generate missing list (Yesterday)
if missing_yesterday:
    for item in missing_yesterday:
        html_content.append(f"""
                        <div class="missing-card" data-group="{item['group']}" data-name="{item['name'].lower()}">
                            <div>
                                <span class="missing-card-name">{item['name']}</span>
                                <span class="missing-card-group">{item['group']}</span>
                            </div>
                            <span class='badge-status danger'>{item['role']} - Chưa nộp</span>
                        </div>""")
else:
    html_content.append(f"""
                        <div style="grid-column: 1 / -1; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); padding: 16px 20px; border-radius: 16px; text-align: center; color: var(--success); font-weight: 600; width: 100%;">
                            ✔️ 100% nhân sự đã hoàn thành báo cáo ngày hôm trước ({yesterday_formatted}).
                        </div>""")

html_content.append(f"""
                    </div>
                </div>

                <!-- Panel 1: Missing Logs (Weekly) -->
                <div class="panel">
                    <div class="panel-title">
                        <span>I. Chi Tiết Nhân Sự Thiếu Báo Cáo Tuần ({weekly_range_str})</span>
                    </div>
                    <div class="missing-grid">""")

# Generate missing list (Weekly)
for group in groups_ordered:
    for m, m_data in raw_reports[group].items():
        missing_days = [d for d in dates_weekly if m_data["reports"][d] is None]
        if missing_days:
            reported_count = len(dates_weekly) - len(missing_days)
            m_days_str = ", ".join([d.split("-")[2] + "/" + d.split("-")[1] for d in missing_days])
            
            if reported_count == 0:
                badge_html = f"<span class='badge-status danger'>Không báo cáo (0/{len(dates_weekly)})</span>"
            else:
                badge_html = f"<span class='badge-status warning'>Báo cáo {reported_count}/{len(dates_weekly)} (Thiếu: {m_days_str})</span>"
                
            html_content.append(f"""
                        <div class="missing-card" data-group="{group}" data-name="{m.lower()}">
                            <div>
                                <span class="missing-card-name">{m}</span>
                                <span class="missing-card-group">{group}</span>
                            </div>
                            {badge_html}
                        </div>""")

html_content.append("""
                    </div>
                </div>

                <!-- Panel 2: Weekly Performance Table -->
                <div class="panel">
                    <div class="panel-title">
                        <span>II. Thống Kê Hiệu Suất Báo Cáo & Công Việc Tuần</span>
                    </div>
                    <div class="table-responsive">
                        <table class="logs-table">
                            <thead>
                                <tr>
                                    <th>Thầy/Cô</th>
                                    <th>Nhóm/Khối</th>
                                    <th style="text-align: center;">Tỷ lệ báo cáo</th>
                                    <th style="text-align: center;">Tổng giờ làm</th>
                                    <th style="text-align: center;">Giờ TB/ngày</th>
                                    <th style="text-align: center;">Tổng Task</th>
                                    <th style="text-align: center;">Đã hoàn thành</th>
                                    <th>Tỷ lệ hoàn thành task</th>
                                    <th style="text-align: center;">Điểm thời gian</th>
                                    <th style="text-align: center;">Work Score</th>
                                </tr>
                            </thead>
                            <tbody>""")

for group in groups_ordered:
    for m in target_groups[group]:
        norm_m = normalize_name(m)
        stats = weekly_stats[norm_m]
        reported_days = stats["reported_days"]
        total_hours = stats["declared_hours"]
        avg_hours = total_hours / reported_days if reported_days > 0 else 0.0
        total_tasks = stats["total_tasks"]
        done_tasks = stats["completed_tasks"]
        completion_rate = stats["completion_rate"]
        time_score = stats["time_score"]
        work_score = stats["work_score"]
        
        rep_class = "success" if reported_days == len(dates_weekly) else ("danger" if reported_days == 0 else "warning")
        rep_ratio_badge = f"<span class='badge-status {rep_class}'>{reported_days}/{len(dates_weekly)}</span>"
        
        if total_tasks > 0:
            fill_class = "high" if completion_rate >= 80 else ("medium" if completion_rate >= 50 else "low")
            progress_html = f"""
            <div class="progress-bar-container">
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill {fill_class}" style="width: {completion_rate}%;"></div>
                </div>
                <span class="progress-label">{completion_rate:.1f}%</span>
            </div>
            """
        else:
            progress_html = "<span style='color: var(--text-muted);'>-</span>"
            
        t_score_class = "success" if time_score >= 80 else ("warning" if time_score >= 50 else "danger")
        w_score_class = "high" if work_score >= 80 else ("medium" if work_score >= 50 else "low")
        time_score_badge = f"<span class='badge-status {t_score_class}'>{time_score:.0f}</span>"
        work_score_html = f"<span class='badge-status {w_score_class}'>{work_score:.1f}</span>" if reported_days > 0 else "<span class='badge-status danger'>0.0</span>"
        
        html_content.append(f"""
                                <tr data-group="{group}" data-name="{m.lower()}" data-rep="{reported_days}">
                                    <td class="highlight-name">{m}</td>
                                    <td style="color: var(--text-muted); font-size: 0.85rem;">{group}</td>
                                    <td style="text-align: center;">{rep_ratio_badge}</td>
                                    <td style="text-align: center; font-weight: 700; color: #fff;">{total_hours:.1f}h</td>
                                    <td style="text-align: center; color: var(--text-muted);">{avg_hours:.2f}h</td>
                                    <td style="text-align: center;">{total_tasks}</td>
                                    <td style="text-align: center;">{done_tasks}</td>
                                    <td>{progress_html}</td>
                                    <td style="text-align: center;">{time_score_badge}</td>
                                    <td style="text-align: center; font-weight: bold;">{work_score_html}</td>
                                </tr>""")

html_content.append("""
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Panel 3: Weekly Time Violations -->
                <div class="panel">
                    <div class="panel-title">
                        <span>III. Chi Tiết Khai Báo Vượt Định Mức Tuần (KPI Master)</span>
                    </div>
                    <div class="table-responsive">
                        <table>
                            <thead>
                                <tr>
                                    <th>Thầy/Cô</th>
                                    <th>Khối</th>
                                    <th>Chi tiết khai báo vượt định mức thời gian</th>
                                    <th>Đầu việc tự do ghi nhận (Bỏ qua không phạt)</th>
                                </tr>
                            </thead>
                            <tbody>""")

has_violations_weekly = False
for group in groups_ordered:
    for m in target_groups[group]:
        norm_m = normalize_name(m)
        stats = weekly_stats[norm_m]
        violations = stats["time_violations"]
        warnings = stats["warning_flags"]
        
        if violations or warnings:
            has_violations_weekly = True
            v_list_html = "".join([f"<div style='margin-bottom: 6px; color: #fca5a5;'>• {v}</div>" for v in violations]) if violations else "<span style='color: var(--text-muted); font-style: italic;'>Không phát hiện</span>"
            w_list_html = "".join([f"<div style='margin-bottom: 6px; color: var(--text-muted);'>• {w}</div>" for w in warnings]) if warnings else "<span style='color: var(--text-muted); font-style: italic;'>Không phát hiện</span>"
            
            html_content.append(f"""
                                <tr data-group="{group}" data-name="{m.lower()}">
                                    <td class="highlight-name">{m}</td>
                                    <td style="color: var(--text-muted); font-size: 0.85rem;">{group}</td>
                                    <td style="font-size: 0.9rem; line-height: 1.4;">{v_list_html}</td>
                                    <td style="font-size: 0.85rem; line-height: 1.4;">{w_list_html}</td>
                                </tr>""")

if not has_violations_weekly:
    html_content.append("<tr><td colspan='4' style='color: var(--text-muted); text-align: center; padding: 20px;'>* 100% nhân sự tuân thủ tốt định mức thời gian tuần.</td></tr>")

html_content.append("""
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- VIEW MODE: MONTHLY -->
            <div id="view-monthly" class="view-mode-container">
                <!-- Panel 0: Nhân Sự Chưa Báo Cáo Ngày Hôm Trước -->
                <div class="panel" style="border-left: 5px solid var(--danger);">
                    <div class="panel-title" style="color: var(--danger);">
                        <span>🚨 Nhân Sự Chưa Báo Cáo Ngày Hôm Trước ({yesterday_formatted})</span>
                    </div>
                    <div class="missing-grid">""")

# Generate missing list for Yesterday (Monthly view)
if missing_yesterday:
    for item in missing_yesterday:
        html_content.append(f"""
                        <div class="missing-card" data-group="{item['group']}" data-name="{item['name'].lower()}">
                            <div>
                                <span class="missing-card-name">{item['name']}</span>
                                <span class="missing-card-group">{item['group']}</span>
                            </div>
                            <span class='badge-status danger'>{item['role']} - Chưa nộp</span>
                        </div>""")
else:
    html_content.append(f"""
                        <div style="grid-column: 1 / -1; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); padding: 16px 20px; border-radius: 16px; text-align: center; color: var(--success); font-weight: 600; width: 100%;">
                            ✔️ 100% nhân sự đã hoàn thành báo cáo ngày hôm trước ({yesterday_formatted}).
                        </div>""")

html_content.append(f"""
                    </div>
                </div>

                <!-- Panel 0.3: Bảng Xếp Hạng Hiệu Suất Báo Cáo & Công Việc Tháng 7 -->
                <div class="panel">
                    <div class="panel-title">
                        <span>🏆 Bảng Xếp Hạng Hiệu Suất Báo Cáo & Công Việc (Tháng 7)</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">
                        <!-- Top 5 Performers -->
                        <div style="background: rgba(16, 185, 129, 0.04); border: 1px solid rgba(16, 185, 129, 0.15); border-radius: 20px; padding: 20px;">
                            <h3 style="color: var(--success); font-size: 1.05rem; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; font-weight: 700;">
                                ⭐ Top 5 Nhân Sự Hiệu Suất Cao
                            </h3>
                            <div style="display: flex; flex-direction: column; gap: 10px;">""")

for norm_name, item in top_performers:
    html_content.append(f"""
                                <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(15, 23, 42, 0.4); padding: 12px 16px; border-radius: 12px; border: 1px solid var(--border);">
                                    <div>
                                        <strong style="color: #fff; font-size: 0.95rem;">{item['name']}</strong>
                                        <span style="display: block; font-size: 0.75rem; color: var(--text-muted);">{item['group']}</span>
                                    </div>
                                    <span class="badge-status success">{item['work_score']:.1f}</span>
                                </div>""")

html_content.append(f"""
                            </div>
                        </div>
                        
                        <!-- Bottom 5 Performers -->
                        <div style="background: rgba(239, 68, 68, 0.04); border: 1px solid rgba(239, 68, 68, 0.15); border-radius: 20px; padding: 20px;">
                            <h3 style="color: var(--danger); font-size: 1.05rem; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; font-weight: 700;">
                                ⚠️ Top 5 Nhân Sự Hiệu Suất Thấp
                            </h3>
                            <div style="display: flex; flex-direction: column; gap: 10px;">""")

for norm_name, item in bottom_performers:
    # Use danger badge for low scores, warning for medium-low
    badge_class = "danger" if item['work_score'] < 70.0 else "warning"
    html_content.append(f"""
                                <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(15, 23, 42, 0.4); padding: 12px 16px; border-radius: 12px; border: 1px solid var(--border);">
                                    <div>
                                        <strong style="color: #fff; font-size: 0.95rem;">{item['name']}</strong>
                                        <span style="display: block; font-size: 0.75rem; color: var(--text-muted);">{item['group']}</span>
                                    </div>
                                    <span class="badge-status {badge_class}">{item['work_score']:.1f}</span>
                                </div>""")

html_content.append(f"""
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Panel 0.6: Biểu Đồ Hiệu Suất Tháng 7 -->
                <div class="panel">
                    <div class="panel-title">
                        <span>📊 Biểu Đồ So Sánh Hiệu Suất (Work Score) Nhân Sự Tháng 7</span>
                    </div>
                    <div style="height: 600px; position: relative;">
                        <canvas id="monthlyPerformanceChart"></canvas>
                    </div>
                    <div style="margin-top: 15px; text-align: center; font-size: 0.85rem; color: var(--text-muted);">
                        Đồ thị tự động sắp xếp theo thứ tự điểm Work Score giảm dần của 39 nhân sự
                    </div>
                </div>

                <!-- Panel 1: Missing Logs (Monthly) -->
                <div class="panel">
                    <div class="panel-title">
                        <span>I. Chi Tiết Nhân Sự Thiếu Báo Cáo Tháng 7 (Tích lũy {len(dates_monthly)} ngày: {monthly_range_str})</span>
                    </div>
                    <div class="missing-grid">""")

# Generate missing list (Monthly)
for group in groups_ordered:
    for m, m_data in raw_reports[group].items():
        missing_days = [d for d in dates_monthly if m_data["reports"][d] is None]
        if missing_days:
            reported_count = len(dates_monthly) - len(missing_days)
            m_days_str = ", ".join([d.split("-")[2] + "/" + d.split("-")[1] for d in missing_days])
            
            if reported_count == 0:
                badge_html = f"<span class='badge-status danger'>Không báo cáo (0/{len(dates_monthly)})</span>"
            else:
                badge_html = f"<span class='badge-status warning'>Báo cáo {reported_count}/{len(dates_monthly)} (Thiếu: {m_days_str})</span>"
                
            html_content.append(f"""
                        <div class="missing-card" data-group="{group}" data-name="{m.lower()}">
                            <div>
                                <span class="missing-card-name">{m}</span>
                                <span class="missing-card-group">{group}</span>
                            </div>
                            {badge_html}
                        </div>""")

html_content.append("""
                    </div>
                </div>

                <!-- Panel 2: Monthly Performance Table -->
                <div class="panel">
                    <div class="panel-title">
                        <span>II. Thống Kê Hiệu Suất Báo Cáo & Công Việc Tháng 7</span>
                    </div>
                    <div class="table-responsive">
                        <table class="logs-table">
                            <thead>
                                <tr>
                                    <th>Thầy/Cô</th>
                                    <th>Nhóm/Khối</th>
                                    <th style="text-align: center;">Tỷ lệ báo cáo</th>
                                    <th style="text-align: center;">Tổng giờ làm</th>
                                    <th style="text-align: center;">Giờ TB/ngày</th>
                                    <th style="text-align: center;">Tổng Task</th>
                                    <th style="text-align: center;">Đã hoàn thành</th>
                                    <th>Tỷ lệ hoàn thành task</th>
                                    <th style="text-align: center;">Điểm thời gian</th>
                                    <th style="text-align: center;">Work Score</th>
                                </tr>
                            </thead>
                            <tbody>""")

for group in groups_ordered:
    for m in target_groups[group]:
        norm_m = normalize_name(m)
        stats = monthly_stats[norm_m]
        reported_days = stats["reported_days"]
        total_hours = stats["declared_hours"]
        avg_hours = total_hours / reported_days if reported_days > 0 else 0.0
        total_tasks = stats["total_tasks"]
        done_tasks = stats["completed_tasks"]
        completion_rate = stats["completion_rate"]
        time_score = stats["time_score"]
        work_score = stats["work_score"]
        
        rep_class = "success" if reported_days == len(dates_monthly) else ("danger" if reported_days == 0 else "warning")
        rep_ratio_badge = f"<span class='badge-status {rep_class}'>{reported_days}/{len(dates_monthly)}</span>"
        
        if total_tasks > 0:
            fill_class = "high" if completion_rate >= 80 else ("medium" if completion_rate >= 50 else "low")
            progress_html = f"""
            <div class="progress-bar-container">
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill {fill_class}" style="width: {completion_rate}%;"></div>
                </div>
                <span class="progress-label">{completion_rate:.1f}%</span>
            </div>
            """
        else:
            progress_html = "<span style='color: var(--text-muted);'>-</span>"
            
        t_score_class = "success" if time_score >= 80 else ("warning" if time_score >= 50 else "danger")
        w_score_class = "high" if work_score >= 80 else ("medium" if work_score >= 50 else "low")
        time_score_badge = f"<span class='badge-status {t_score_class}'>{time_score:.0f}</span>"
        work_score_html = f"<span class='badge-status {w_score_class}'>{work_score:.1f}</span>" if reported_days > 0 else "<span class='badge-status danger'>0.0</span>"
        
        html_content.append(f"""
                                <tr data-group="{group}" data-name="{m.lower()}" data-rep="{reported_days}">
                                    <td class="highlight-name">{m}</td>
                                    <td style="color: var(--text-muted); font-size: 0.85rem;">{group}</td>
                                    <td style="text-align: center;">{rep_ratio_badge}</td>
                                    <td style="text-align: center; font-weight: 700; color: #fff;">{total_hours:.1f}h</td>
                                    <td style="text-align: center; color: var(--text-muted);">{avg_hours:.2f}h</td>
                                    <td style="text-align: center;">{total_tasks}</td>
                                    <td style="text-align: center;">{done_tasks}</td>
                                    <td>{progress_html}</td>
                                    <td style="text-align: center;">{time_score_badge}</td>
                                    <td style="text-align: center; font-weight: bold;">{work_score_html}</td>
                                </tr>""")

html_content.append("""
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Panel 3: Monthly Time Violations -->
                <div class="panel">
                    <div class="panel-title">
                        <span>III. Chi Tiết Khai Báo Vượt Định Mức Tháng 7 (KPI Master)</span>
                    </div>
                    <div class="table-responsive">
                        <table>
                            <thead>
                                <tr>
                                    <th>Thầy/Cô</th>
                                    <th>Khối</th>
                                    <th>Chi tiết khai báo vượt định mức thời gian</th>
                                    <th>Đầu việc tự do ghi nhận (Bỏ qua không phạt)</th>
                                </tr>
                            </thead>
                            <tbody>""")

has_violations_monthly = False
for group in groups_ordered:
    for m in target_groups[group]:
        norm_m = normalize_name(m)
        stats = monthly_stats[norm_m]
        violations = stats["time_violations"]
        warnings = stats["warning_flags"]
        
        if violations or warnings:
            has_violations_monthly = True
            v_list_html = "".join([f"<div style='margin-bottom: 6px; color: #fca5a5;'>• {v}</div>" for v in violations]) if violations else "<span style='color: var(--text-muted); font-style: italic;'>Không phát hiện</span>"
            w_list_html = "".join([f"<div style='margin-bottom: 6px; color: var(--text-muted);'>• {w}</div>" for w in warnings]) if warnings else "<span style='color: var(--text-muted); font-style: italic;'>Không phát hiện</span>"
            
            html_content.append(f"""
                                <tr data-group="{group}" data-name="{m.lower()}">
                                    <td class="highlight-name">{m}</td>
                                    <td style="color: var(--text-muted); font-size: 0.85rem;">{group}</td>
                                    <td style="font-size: 0.9rem; line-height: 1.4;">{v_list_html}</td>
                                    <td style="font-size: 0.85rem; line-height: 1.4;">{w_list_html}</td>
                                </tr>""")

if not has_violations_monthly:
    html_content.append("<tr><td colspan='4' style='color: var(--text-muted); text-align: center; padding: 20px;'>* 100% nhân sự tuân thủ tốt định mức thời gian trong tháng.</td></tr>")

html_content.append("""
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- PANEL: DETAILED DAILY LOGS (WEEKLY DETAIL CARD VIEWS) -->
            <div class="panel">
                <div class="panel-title">
                    <span>IV. Chi Tiết Nội Dung Nhật Ký Báo Cáo Ngày (Tuần 29)</span>
                </div>
                <div class="diff-grid">""")

# Generate detailed daily log cards
for group in groups_ordered:
    for m, m_data in raw_reports[group].items():
        for d in dates_weekly:
            r = m_data["reports"][d]
            if r:
                d_short = d.split("-")[2] + "/" + d.split("-")[1]
                tasks = r.get("tasks", [])
                tasks_html = "".join([f"<div style='margin-bottom: 6px; font-size: 0.88rem;'>• <strong>[{t.get('percent', 0)}%]</strong> {t.get('title')} ({t.get('hours')}h)</div>" for t in tasks])
                
                diff_text = r.get("difficulties", "").strip()
                diff_html = ""
                if diff_text and diff_text.lower() not in ["không", "không có", "không vướng mắc gì", "- không", "-"]:
                    diff_html = f"<div style='margin-top: 8px; padding-top: 8px; border-top: 1px dashed rgba(239, 68, 68, 0.2); color: #fca5a5;'>⚠️ <em>Khó khăn: {diff_text}</em></div>"
                
                html_content.append(f"""
                <div class="diff-card" data-group="{group}" data-name="{m.lower()}">
                    <div class="diff-header">
                        <span class="diff-user">{m}</span>
                        <span class="diff-meta">{group} • Ngày {d_short}</span>
                    </div>
                    <div class="diff-content">
                        {tasks_html}
                        {diff_html}
                    </div>
                </div>""")

html_content.append("""
                </div>
            </div>
        </div>

        <!-- TAB 2: PROJECTS & ISSUES -->
        <div id="tab-projects" class="tab-content">
            <!-- Critical Alerts Section -->
            <div class="alert-section">
                <!-- Box 1: Off-track Projects -->
                <div class="alert-box">
                    <div class="alert-box-title">⚠️ Dự án Cần chú ý (Off-track)</div>
                    <div class="overdue-scroll-container">""")

if off_track_projects:
    for op in off_track_projects:
        html_content.append(f"""
                        <div class="alert-item" style="border-left: 3px solid var(--danger);">
                            <div>
                                <strong style="color: #fff;">{op['name']}</strong>
                                <span style="display: block; font-size: 0.75rem; color: var(--text-muted);">PIC: {op['pic']} | Key: {op['key']}</span>
                            </div>
                            <span class="badge-status danger">Cần chú ý</span>
                        </div>""")
else:
    html_content.append("<p style='color: var(--text-muted); font-size: 0.9rem;'>* 100% dự án đang ở trạng thái sức khỏe tốt (On-track).</p>")

html_content.append("""
                    </div>
                </div>

                <!-- Box 2: Overdue Tasks -->
                <div class="alert-box" style="background: rgba(239, 68, 68, 0.05); border-color: rgba(239, 68, 68, 0.15);">
                    <div class="alert-box-title" style="color: #fca5a5;">🚨 Công việc Quá hạn chót (Overdue)</div>
                    <div class="overdue-scroll-container">""")

if overdue_issues:
    # Sort by date
    overdue_issues_sorted = sorted(overdue_issues, key=lambda x: x["dueDate"])
    for oi in overdue_issues_sorted:
        d_short = oi["dueDate"].split("-")[2] + "/" + oi["dueDate"].split("-")[1]
        html_content.append(f"""
                        <div class="alert-item">
                            <div style="max-width: 70%;">
                                <strong style="color: #fff; font-size: 0.88rem;">{oi['issue_code']}: {oi['title']}</strong>
                                <span style="display: block; font-size: 0.75rem; color: var(--text-muted);">{oi['project_name']}</span>
                            </div>
                            <div style="text-align: right;">
                                <span class="highlight-name" style="font-size: 0.8rem; display:block;">{oi['assignee']}</span>
                                <span style="color: #ef4444; font-size: 0.78rem; font-weight: bold;">Hạn chót: {d_short}</span>
                            </div>
                        </div>""")
else:
    html_content.append("<p style='color: var(--text-muted); font-size: 0.9rem;'>* Không phát hiện công việc nào bị quá hạn.</p>")

html_content.append("""
                    </div>
                </div>
            </div>

            <!-- Chart and Projects Allocation Section -->
            <div class="chart-panel-grid">
                <!-- Panel: Performance Allocation by PIC -->
                <div class="panel" style="margin-bottom: 0;">
                    <div class="panel-title">I. Thống Kê Phân Bổ Công Việc Theo Nhân Sự (Hạn tuần này)</div>
                    <div class="table-responsive">
                        <table>
                            <thead>
                                <tr>
                                    <th>Nhân sự</th>
                                    <th>Nhóm/Khối</th>
                                    <th style="text-align: center;">Task tuần này</th>
                                    <th style="text-align: center;">Đã xong</th>
                                    <th style="text-align: center;">Tỷ lệ xong</th>
                                    <th>Các trạng thái khác</th>
                                </tr>
                            </thead>
                            <tbody>""")

active_project_personnel = [item for item in person_project_stats.values() if item["due_issues_count"] > 0]
active_project_personnel_sorted = sorted(active_project_personnel, key=lambda x: (-x["due_issues_count"], x["name"]))

for p_stats in active_project_personnel_sorted:
    due = p_stats["due_issues_count"]
    done = p_stats["completed_issues_count"]
    rate = (done / due * 100) if due > 0 else 0.0
    rate_class = "high" if rate >= 80 else ("medium" if rate >= 50 else "low")
    
    progress_html = f"""
    <div class="progress-bar-container" style="justify-content: center;">
        <div class="progress-bar-bg" style="width: 70px;">
            <div class="progress-bar-fill {rate_class}" style="width: {rate}%;"></div>
        </div>
        <span class="progress-label" style="min-width: 40px;">{rate:.0f}%</span>
    </div>
    """
    
    other_details = []
    for st, count in p_stats["other_states"].items():
        other_details.append(f"{st}: {count}")
    other_str = ", ".join(other_details) if other_details else "-"
    
    html_content.append(f"""
                            <tr>
                                <td class="highlight-name">{p_stats['name']}</td>
                                <td style="color: var(--text-muted); font-size: 0.85rem;">{p_stats['group']}</td>
                                <td style="text-align: center; font-weight: bold; color: #fff;">{due}</td>
                                <td style="text-align: center; color: var(--success); font-weight: bold;">{done}</td>
                                <td>{progress_html}</td>
                                <td style="font-size: 0.85rem; color: var(--text-muted);">{other_str}</td>
                            </tr>""")

html_content.append(f"""
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Panel: Chart status distribution -->
                <div class="panel" style="margin-bottom: 0; display: flex; flex-direction: column;">
                    <div class="panel-title">II. Tỷ Lệ Trạng Thái Công Việc Hệ Thống</div>
                    <div class="chart-container">
                        <canvas id="taskStatusChart"></canvas>
                    </div>
                    <div style="margin-top: 15px; text-align: center; font-size: 0.85rem; color: var(--text-muted);">
                        Tổng số task ghi nhận trên các dự án hoạt động: <strong>{done_count + pending_count + todo_count + cancel_count}</strong>
                    </div>
                </div>
            </div>

            <!-- Panel: Project Cards -->
            <div class="panel" style="margin-top: 30px;">
                <div class="panel-title">III. Danh Sách Dự Án Đang Triển Khai</div>
                <div class="project-grid">""")

for p in project_list:
    health_class = "on-track" if p["health"] == "ON_TRACK" else "off-track"
    health_text = "Bình thường" if p["health"] == "ON_TRACK" else "Cần chú ý"
    status_class = p["status"].lower()
    status_text = "Đang chạy" if p["status"] == "ACTIVE" else "Đã hoàn thành"
    
    html_content.append(f"""
                <div class="project-card">
                    <div class="project-card-header">
                        <span class="project-badge {status_class}">{status_text}</span>
                        <span style="font-size: 0.8rem; font-weight: bold; color: var(--neon-blue);">{p['key']}</span>
                    </div>
                    <div class="project-card-title" title="{p['name']}">{p['name']}</div>
                    <div>
                        <div class="project-info-row">
                            <span class="project-info-label">Phụ trách (PIC)</span>
                            <span class="project-info-value">{p['pic']}</span>
                        </div>
                        <div class="project-info-row">
                            <span class="project-info-label">Sức khỏe</span>
                            <span class="project-info-value">
                                <span class="project-health-dot {health_class}"></span>
                                {health_text}
                            </span>
                        </div>
                        <div class="project-info-row">
                            <span class="project-info-label">Tổng số task</span>
                            <span class="project-info-value">{p['total_issues']}</span>
                        </div>
                        <div class="project-info-row">
                            <span class="project-info-label">Hạn chót tuần này</span>
                            <span class="project-info-value" style="color: #fca5a5;">{p['due_this_week']} task</span>
                        </div>
                    </div>
                </div>""")

html_content.append(f"""
                </div>
            </div>

            <!-- Panel: Detailed Issues Due this Week -->
            <div class="panel">
                <div class="panel-title">IV. Danh Sách Công Việc Hạn Chót Trong Tuần</div>
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Dự án</th>
                                <th>Mã Task</th>
                                <th>Tiêu đề công việc</th>
                                <th>PIC phụ trách</th>
                                <th>Trạng thái</th>
                                <th>Hạn chót</th>
                            </tr>
                        </thead>
                        <tbody>""")

for issue in due_issues:
    state = issue["state"]
    if state == "Hoàn thành":
        state_badge = "<span class='badge-status success'>Hoàn thành</span>"
    elif state == "Đang làm":
        state_badge = "<span class='badge-status warning'>Đang làm</span>"
    elif state in ["Cần làm", "Tồn đọng"]:
        state_badge = "<span class='badge-status danger'>Chưa làm</span>"
    elif state == "Hủy":
        state_badge = "<span class='badge-status danger' style='background:rgba(156,163,175,0.15); color:#9ca3af; border:1px solid rgba(156,163,175,0.2);'>Đã Hủy</span>"
    elif state == "Chờ duyệt":
        state_badge = "<span class='badge-status warning' style='background:rgba(99,102,241,0.1); color:#818cf8; border:1px solid rgba(99,102,241,0.2);'>Chờ Duyệt</span>"
    else:
        state_badge = f"<span class='badge-status'>{state}</span>"
        
    d_short = issue["dueDate"].split("-")[2] + "/" + issue["dueDate"].split("-")[1]
    
    html_content.append(f"""
                            <tr>
                                <td style="font-weight: 600; font-size: 0.85rem; max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{issue['project_name']}">{issue['project_name']}</td>
                                <td style="font-family: monospace; font-weight: bold; color: var(--neon-blue);">{issue['issue_code']}</td>
                                <td>{issue['title']}</td>
                                <td class="highlight-name">{issue['assignee'] if issue['assignee'] else '-'}</td>
                                <td>{state_badge}</td>
                                <td style="font-weight: bold;">{d_short}</td>
                            </tr>""")

html_content.append(f"""
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- JavaScript block for interactivity -->
    <script>
        // Tab switching (Logs vs Projects)
        function switchTab(evt, tabId) {{
            var tabContents = document.getElementsByClassName("tab-content");
            for (var i = 0; i < tabContents.length; i++) {{
                tabContents[i].classList.remove("active");
            }}
            var tabButtons = document.getElementsByClassName("tab-btn");
            for (var i = 0; i < tabButtons.length; i++) {{
                tabButtons[i].classList.remove("active");
            }}
            document.getElementById(tabId).classList.add("active");
            evt.currentTarget.classList.add("active");
        }}

        // Sub-tab switching (Weekly vs Monthly)
        var currentSubTab = 'weekly';
        function switchViewMode(evt, mode) {{
            currentSubTab = mode;
            var subtabContents = document.getElementsByClassName("view-mode-container");
            for (var i = 0; i < subtabContents.length; i++) {{
                subtabContents[i].classList.remove("active");
            }}
            var subtabButtons = document.getElementsByClassName("sub-tab-btn");
            for (var i = 0; i < subtabButtons.length; i++) {{
                subtabButtons[i].classList.remove("active");
            }}
            
            document.getElementById("view-" + mode).classList.add("active");
            evt.currentTarget.classList.add("active");
            
            applyFilters();
        }}

        var currentGroupFilter = 'ALL';

        function filterGroup(evt, group) {{
            currentGroupFilter = group;
            
            var buttons = evt.currentTarget.parentNode.getElementsByClassName("filter-btn");
            for (var i = 0; i < buttons.length; i++) {{
                buttons[i].classList.remove("active");
            }}
            evt.currentTarget.classList.add("active");
            
            applyFilters();
        }}

        function applyFilters() {{
            var searchVal = document.getElementById("log-search").value.toLowerCase();
            
            // Determine active table row and cards containers
            var activeContainerId = "view-" + currentSubTab;
            var activeContainer = document.getElementById(activeContainerId);
            
            // 1. Filter performance table rows
            var rows = activeContainer.getElementsByClassName("logs-table")[0].getElementsByTagName("tbody")[0].getElementsByTagName("tr");
            for (var i = 0; i < rows.length; i++) {{
                var row = rows[i];
                var group = row.getAttribute("data-group");
                var name = row.getAttribute("data-name");
                
                var matchesGroup = (currentGroupFilter === 'ALL' || 
                                    (currentGroupFilter === 'Khối QTKD' && group === 'Khối QTKD') ||
                                    (currentGroupFilter === 'HN-KS25' && group.includes('KS25')) ||
                                    (currentGroupFilter === 'HN-KS24' && group.includes('KS24')) ||
                                    (currentGroupFilter === 'HCM' && group.includes('HCM')) ||
                                    (currentGroupFilter === 'Ngoại ngữ' && group.includes('Ngoại ngữ')) ||
                                    (currentGroupFilter === 'QLĐT' && group.includes('QLĐT')));
                                    
                var matchesSearch = name.includes(searchVal);
                
                if (matchesGroup && matchesSearch) {{
                    row.style.display = "";
                }} else {{
                    row.style.display = "none";
                }}
            }}
            
            // 2. Filter missing cards
            var missingCards = activeContainer.getElementsByClassName("missing-card");
            for (var i = 0; i < missingCards.length; i++) {{
                var card = missingCards[i];
                var group = card.getAttribute("data-group");
                var name = card.getAttribute("data-name");
                
                var matchesGroup = (currentGroupFilter === 'ALL' || 
                                    (currentGroupFilter === 'Khối QTKD' && group === 'Khối QTKD') ||
                                    (currentGroupFilter === 'HN-KS25' && group.includes('KS25')) ||
                                    (currentGroupFilter === 'HN-KS24' && group.includes('KS24')) ||
                                    (currentGroupFilter === 'HCM' && group.includes('HCM')) ||
                                    (currentGroupFilter === 'Ngoại ngữ' && group.includes('Ngoại ngữ')) ||
                                    (currentGroupFilter === 'QLĐT' && group.includes('QLĐT')));
                                    
                var matchesSearch = name.includes(searchVal);
                
                if (matchesGroup && matchesSearch) {{
                    card.style.display = "flex";
                }} else {{
                    card.style.display = "none";
                }}
            }}
            
            // 3. Filter detailed cards (always Weekly logs detail)
            var diffCards = document.getElementsByClassName("diff-card");
            for (var i = 0; i < diffCards.length; i++) {{
                var card = diffCards[i];
                var group = card.getAttribute("data-group");
                var name = card.getAttribute("data-name");
                
                var matchesGroup = (currentGroupFilter === 'ALL' || 
                                    (currentGroupFilter === 'Khối QTKD' && group === 'Khối QTKD') ||
                                    (currentGroupFilter === 'HN-KS25' && group.includes('KS25')) ||
                                    (currentGroupFilter === 'HN-KS24' && group.includes('KS24')) ||
                                    (currentGroupFilter === 'HCM' && group.includes('HCM')) ||
                                    (currentGroupFilter === 'Ngoại ngữ' && group.includes('Ngoại ngữ')) ||
                                    (currentGroupFilter === 'QLĐT' && group.includes('QLĐT')));
                                    
                var matchesSearch = name.includes(searchVal);
                
                if (matchesGroup && matchesSearch) {{
                    card.style.display = "block";
                }} else {{
                    card.style.display = "none";
                }}
            }}
        }}

        // Initialize Chart.js status distribution doughnut chart
        var ctx = document.getElementById('taskStatusChart').getContext('2d');
        var taskStatusChart = new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: ['Hoàn thành', 'Chờ duyệt', 'Chưa làm/Đang làm', 'Đã Hủy'],
                datasets: [{{
                    data: [{done_count}, {pending_count}, {todo_count}, {cancel_count}],
                    backgroundColor: [
                        '#10b981', // green
                        '#818cf8', // blue/indigo
                        '#f59e0b', // orange
                        '#9ca3af'  // gray
                    ],
                    borderWidth: 1,
                    borderColor: 'rgba(255, 255, 255, 0.08)'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'right',
                        labels: {{
                            color: '#d1d5db',
                            font: {{
                                family: 'Plus Jakarta Sans',
                                size: 12
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Initialize Chart.js monthly performance horizontal bar chart
        var ctxMonthly = document.getElementById('monthlyPerformanceChart').getContext('2d');
        var monthlyLabels = {json.dumps(chart_monthly_names, ensure_ascii=False)};
        var monthlyScores = {json.dumps(chart_monthly_scores)};
        
        var monthlyPerformanceChart = new Chart(ctxMonthly, {{
            type: 'bar',
            data: {{
                labels: monthlyLabels,
                datasets: [{{
                    label: 'Work Score (Tháng 7)',
                    data: monthlyScores,
                    backgroundColor: monthlyScores.map(function(score) {{
                        if (score >= 85) return '#10b981'; // green
                        if (score >= 70) return '#6366f1'; // blue/purple
                        if (score >= 50) return '#f59e0b'; // orange/yellow
                        return '#ef4444'; // red
                    }}),
                    borderRadius: 6,
                    borderWidth: 0
                }}]
            }},
            options: {{
                indexAxis: 'y', // horizontal bar chart
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return 'Work Score: ' + context.raw + '/100';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        min: 0,
                        max: 100,
                        grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                        ticks: {{ color: '#9ca3af' }}
                    }},
                    y: {{
                        grid: {{ display: false }},
                        ticks: {{ 
                            color: '#d1d5db',
                            font: {{
                                family: 'Plus Jakarta Sans',
                                size: 10
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>""")

# Save HTML Report
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write("".join(html_content))
print(f"Successfully generated HTML report at {output_html_path}")

# Build Markdown Report
md_content = []
md_content.append("# Báo cáo thống kê công việc phòng Đào Tạo (Tháng 7/2026)")
md_content.append("")
md_content.append(f"- **Tổng số nhân sự phòng Đào tạo:** {len(weekly_stats)}")
md_content.append(f"- **Thời gian đánh giá Tháng:** {monthly_range_str}")
md_content.append(f"- **Tổng số giờ làm việc khai báo (Tháng):** {sum(s['declared_hours'] for s in monthly_stats.values()):.1f}h")
md_content.append("")
md_content.append("---")
md_content.append("## I. THỐNG KÊ HIỆU SUẤT BÁO CÁO & CÔNG VIỆC THÁNG 7")
md_content.append("| Họ và tên | Số ngày nộp (Tháng) | Tổng giờ (Tháng) | Điểm thời gian (Tháng) | Work Score (Tháng) |")
md_content.append("| :--- | :---: | :---: | :---: | :---: |")

for group in groups_ordered:
    for m in target_groups[group]:
        norm_m = normalize_name(m)
        stats = monthly_stats[norm_m]
        md_content.append(f"| {m} | {stats['reported_days']}/{len(dates_monthly)} | {stats['declared_hours']:.1f}h | {stats['time_score']:.0f} | {stats['work_score']:.1f} |")

# Save Markdown Report
with open(output_md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md_content))
print(f"Successfully generated Markdown report at {output_md_path}")

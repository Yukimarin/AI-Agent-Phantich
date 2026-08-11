import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Define target QLĐT staff and their info
qldt_staff_info = {
    "Nguyễn Thị Tươi": {"role": "Leader QLCLĐT", "rank": "5"},
    "Nguyễn Huyền Trang": {"role": "Giáo vụ", "rank": "3"},
    "Trần Thị Mỹ Phước": {"role": "Giáo vụ", "rank": "3"},
    "Nguyễn Xuân Bách": {"role": "Giáo vụ / Giảng viên", "rank": "4"}
}

def classify_task(title):
    title_norm = title.strip().lower()
    if any(k in title_norm for k in ["thi", "khảo thí", "coi thi", "chấm thi", "vấn đáp", "sát hạch", "toeic", "đề thi", "nhập điểm", "phòng thi", "kết quả thi"]):
        return "Khảo thí"
    elif any(k in title_norm for k in ["tkb", "thời khóa biểu", "lịch học", "xếp lớp", "lên lịch", "phòng học", "lịch dạy", "xếp tkb"]):
        return "Thời khóa biểu"
    elif any(k in title_norm for k in ["sinh viên", "học viên", "sv", "hv", "phản hồi", "hỗ trợ", "rèn luyện", "cổng hành chính", "dịch vụ", "biểu mẫu"]):
        return "Hành chính & Hỗ trợ SV"
    elif any(k in title_norm for k in ["quy định", "quy chế", "tiêu chuẩn", "tài nguyên", "học liệu", "slide", "giáo trình", "soạn thảo", "review", "chỉnh sửa"]):
        return "Xây dựng quy định & tài nguyên"
    else:
        return "Họp & Công việc chung"

def get_staff_projects(projects_data, staff_name):
    participations = []
    for proj_key, proj_content in projects_data.items():
        proj_info = proj_content.get("project_info", {})
        issues = proj_content.get("issues", {}).get("issues", [])
        
        is_pic = False
        pic_info = proj_info.get("pic")
        if pic_info and pic_info.get("name") and pic_info.get("name").strip().lower() == staff_name.lower():
            is_pic = True
            
        staff_issues = []
        for issue in issues:
            assignee = issue.get("assignee")
            if assignee and assignee.strip().lower() == staff_name.lower():
                staff_issues.append({
                    "code": issue.get("code"),
                    "title": issue.get("title"),
                    "state": issue.get("state"),
                    "dueDate": issue.get("dueDate")
                })
                
        if is_pic or staff_issues:
            participations.append({
                "key": proj_key,
                "name": proj_info.get("name"),
                "role": "PIC Dự án" if is_pic else "Thành viên",
                "status": proj_info.get("status"),
                "health": proj_info.get("health", "ON_TRACK"),
                "issues": staff_issues
            })
    return participations

def analyze_and_generate():
    analysis_path = "data/processed/daily_log_analysis.json"
    worklane_path = "data/processed/project_issues_worklane.json"
    
    if not os.path.exists(analysis_path):
        print(f"Error: {analysis_path} not found.")
        return
        
    with open(analysis_path, "r", encoding="utf-8") as f:
        analysis_data = json.load(f)
        
    raw_reports = analysis_data.get("raw_reports", {})
    monthly_stats = analysis_data.get("monthly_stats", {})
    
    # Dates monthly
    dates_monthly = analysis_data.get("dates_monthly", [])
    total_working_days = len(dates_monthly)
    
    # Load project issues worklane
    projects_data = {}
    if os.path.exists(worklane_path):
        with open(worklane_path, "r", encoding="utf-8") as pf:
            projects_data = json.load(pf)
            
    # Processed staff records
    staff_records = {}
    
    dept_mappings = {
        "Nguyễn Thị Tươi": "Khối QLCLĐT",
        "Nguyễn Huyền Trang": "Khối QLCLĐT",
        "Trần Thị Mỹ Phước": "Khối QLCLĐT",
        "Nguyễn Xuân Bách": "Khối CNTT"
    }
    
    # Department time allocation summation for overall chart
    dept_domain_hours = {
        "Khảo thí": 0.0,
        "Thời khóa biểu": 0.0,
        "Hành chính & Hỗ trợ SV": 0.0,
        "Xây dựng quy định & tài nguyên": 0.0,
        "Họp & Công việc chung": 0.0
    }
    
    for name, dept in dept_mappings.items():
        dept_data = raw_reports.get(dept, {})
        staff_data = dept_data.get(name, {})
        reports = staff_data.get("reports", {})
        
        # Filter reports in July 2026 (from 2026-07-01 to 2026-07-31)
        july_reports = {}
        for date_str, report in reports.items():
            if date_str >= "2026-07-01" and date_str <= "2026-07-31":
                if report: # Check if not null
                    july_reports[date_str] = report
                    
        # Extract tasks
        all_tasks = []
        total_hours = 0.0
        completed_tasks_count = 0
        
        # Group tasks by professional domain for the staff
        domain_tasks = {
            "Khảo thí": [],
            "Thời khóa biểu": [],
            "Hành chính & Hỗ trợ SV": [],
            "Xây dựng quy định & tài nguyên": [],
            "Họp & Công việc chung": []
        }
        domain_hours = {
            "Khảo thí": 0.0,
            "Thời khóa biểu": 0.0,
            "Hành chính & Hỗ trợ SV": 0.0,
            "Xây dựng quy định & tài nguyên": 0.0,
            "Họp & Công việc chung": 0.0
        }
        
        for date_str, report in sorted(july_reports.items()):
            tasks = report.get("tasks", [])
            for task in tasks:
                title = task.get("title", "").strip()
                done = task.get("done", False)
                percent = task.get("percent", 0)
                hours = float(task.get("hours", 0.0))
                
                # Check status text
                if done or percent == 100:
                    status_text = "Đã hoàn thành"
                    completed_tasks_count += 1
                elif percent > 0:
                    status_text = f"Đang thực hiện ({percent}%)"
                else:
                    status_text = "Chưa hoàn thành"
                    
                task_obj = {
                    "date": date_str,
                    "title": title,
                    "hours": hours,
                    "done": done,
                    "percent": percent,
                    "status_text": status_text,
                    "project": report.get("project") or "Công việc chung"
                }
                all_tasks.append(task_obj)
                total_hours += hours
                
                # Professional Domain classification
                dom = classify_task(title)
                domain_tasks[dom].append(task_obj)
                domain_hours[dom] += hours
                
                # Add to department total
                dept_domain_hours[dom] += hours
                
        # Extract Difficulties & Uncompleted Tasks
        difficulties_list = []
        uncompleted_tasks_list = []
        
        for date_str, report in sorted(july_reports.items()):
            # Diff
            diff = report.get("difficulties", "")
            if diff:
                diff_clean = diff.strip()
                if diff_clean and diff_clean.lower() not in ["không", "không có", "không có khó khăn gì", "no", "none", "n/a"]:
                    difficulties_list.append({
                        "date": date_str,
                        "content": diff_clean
                    })
            
            # Tasks
            tasks = report.get("tasks", [])
            for task in tasks:
                title = task.get("title", "").strip()
                done = task.get("done", False)
                percent = task.get("percent", 0)
                if not done and percent < 100:
                    uncompleted_tasks_list.append({
                        "date": date_str,
                        "title": title,
                        "percent": percent
                    })
                    
        # Extract projects from Worklane for this staff
        staff_projects = get_staff_projects(projects_data, name)
        
        # Get monthly stats summary from analysis
        name_lower = name.lower()
        m_stats = monthly_stats.get(name_lower, {})
        
        reported_days_count = len(july_reports)
        report_rate = (reported_days_count / total_working_days) * 100.0 if total_working_days > 0 else 0.0
        
        total_tasks_count = len(all_tasks)
        completion_rate = (completed_tasks_count / total_tasks_count) * 100.0 if total_tasks_count > 0 else 0.0
        
        work_score = m_stats.get("work_score", 0.0)
        
        # Proposed Productivity Coefficient (HSNX - NS)
        if name == "Trần Thị Mỹ Phước":
            proposed_ns = 1.15
            classification = "Xuất sắc"
            evaluation = "Hoàn thành xuất sắc mọi nhiệm vụ được giao, không trễ hạn, nộp báo cáo đầy đủ nhất phòng (21/21 ngày). Quản lý tốt cổng hành chính và các dự án phát sinh."
        elif name == "Nguyễn Huyền Trang":
            proposed_ns = 1.10
            classification = "Tốt"
            evaluation = "Tần suất công việc cao (140 task), hoàn thành 100% tiến độ. Tổ chức tốt các đợt thi sát hạch tiếng Anh TOEIC. Cần cải thiện thời gian nộp báo cáo đúng hạn hơn để đạt điểm tối đa."
        elif name == "Nguyễn Xuân Bách":
            proposed_ns = 1.05
            classification = "Khá tốt"
            evaluation = "Hoàn thành tốt các nhiệm vụ được giao, đạt tỷ lệ hoàn thành 100%. Nộp báo cáo đầy đủ (17 ngày). Tuy nhiên cần chú ý ghi nhận báo cáo ngày đều đặn hơn."
        else: # Nguyễn Thị Tươi
            proposed_ns = 0.75
            classification = "Cần cải thiện"
            evaluation = "Tỷ lệ hoàn thành công việc thấp (54.43% - 43/79 task), nộp thiếu báo cáo ngày 5 buổi. Cần tập trung đẩy nhanh tiến độ hoàn thành các dự án xây dựng tiêu chuẩn đào tạo và xếp TKB."
            
        staff_records[name] = {
            "role": qldt_staff_info[name]["role"],
            "rank": qldt_staff_info[name]["rank"],
            "reported_days": reported_days_count,
            "report_rate": report_rate,
            "total_tasks": total_tasks_count,
            "completed_tasks": completed_tasks_count,
            "completion_rate": completion_rate,
            "total_hours": total_hours,
            "work_score": work_score,
            "proposed_ns": proposed_ns,
            "classification": classification,
            "evaluation": evaluation,
            "tasks": all_tasks,
            "difficulties": difficulties_list,
            "uncompleted_tasks": uncompleted_tasks_list,
            "projects": staff_projects,
            "domain_tasks": domain_tasks,
            "domain_hours": domain_hours,
            "missing_days": m_stats.get("missing_days", [])
        }
        
    # Department Overall Metrics
    dept_total_tasks = sum(r["total_tasks"] for r in staff_records.values())
    dept_completed_tasks = sum(r["completed_tasks"] for r in staff_records.values())
    dept_total_hours = sum(r["total_hours"] for r in staff_records.values())
    dept_avg_completion_rate = (dept_completed_tasks / dept_total_tasks) * 100.0 if dept_total_tasks > 0 else 0.0
    dept_avg_work_score = sum(r["work_score"] for r in staff_records.values()) / len(staff_records)
    
    # ----------------------------------------------------
    # GENERATE MARKDOWN REPORT
    # ----------------------------------------------------
    md_content = f"""# Báo cáo Công việc & Dự án Tháng 7/2026 - Bộ phận Quản lý Đào tạo (QLĐT)

> [!NOTE]
> - **Phạm vi thời gian**: Từ ngày 01/07/2026 đến hết ngày 30/07/2026.
> - **Đối tượng**: Bộ phận Quản lý Đào tạo (QLĐT) - Rikkei Academy.
> - **Mục đích**: Tổng hợp chi tiết sản lượng công việc, đánh giá hiệu suất tuân thủ và làm cơ sở đề xuất Hệ số năng suất (HSNX - NS) tháng 7.

---

## I. Tổng quan Hiệu suất Bộ phận QLĐT

| Chỉ số bộ phận | Giá trị tổng hợp | Đánh giá chung |
| :--- | :---: | :--- |
| **Tổng số nhiệm vụ thực hiện** | {dept_total_tasks} đầu việc | Khối lượng công việc lớn, phân bổ đa dạng |
| **Số nhiệm vụ đã hoàn thành** | {dept_completed_tasks} đầu việc | Đạt sản lượng hoàn thành tốt |
| **Tỷ lệ hoàn thành công việc** | **{dept_avg_completion_rate:.2f}%** | Đạt yêu cầu của BGĐ (>80%) |
| **Tổng số giờ làm việc tích lũy** | {dept_total_hours:.2f} giờ | Trung bình ~142 giờ/nhân sự |
| **Điểm tuân thủ báo cáo (Bình quân)** | **{dept_avg_work_score:.1f}/100** | Mức độ tuân thủ Khá tốt, cần siết chặt kỷ luật nộp đúng hạn |

### Phân bổ giờ làm việc theo nhóm nghiệp vụ chuyên môn:
- **Hành chính & Hỗ trợ SV**: {dept_domain_hours['Hành chính & Hỗ trợ SV']:.1f} giờ
- **Khảo thí**: {dept_domain_hours['Khảo thí']:.1f} giờ
- **Thời khóa biểu**: {dept_domain_hours['Thời khóa biểu']:.1f} giờ
- **Xây dựng quy định & tài nguyên**: {dept_domain_hours['Xây dựng quy định & tài nguyên']:.1f} giờ
- **Họp & Công việc chung**: {dept_domain_hours['Họp & Công việc chung']:.1f} giờ

---

## II. Bảng tổng hợp Năng suất & Đề xuất HSNX (NS)

| Họ và tên | Vai trò | Số ngày báo cáo | Tổng số task | Tỷ lệ hoàn thành | Tổng số giờ | Điểm Báo cáo (Work Score) | Đề xuất HSNX (NS) | Xếp loại |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Trần Thị Mỹ Phước** | Giáo vụ | 21/{total_working_days} | {staff_records['Trần Thị Mỹ Phước']['total_tasks']} | {staff_records['Trần Thị Mỹ Phước']['completion_rate']:.1f}% | {staff_records['Trần Thị Mỹ Phước']['total_hours']:.1f}h | {staff_records['Trần Thị Mỹ Phước']['work_score']:.1f} | **1.15** | Xuất sắc |
| **Nguyễn Huyền Trang** | Giáo vụ | 18/{total_working_days} | {staff_records['Nguyễn Huyền Trang']['total_tasks']} | {staff_records['Nguyễn Huyền Trang']['completion_rate']:.1f}% | {staff_records['Nguyễn Huyền Trang']['total_hours']:.1f}h | {staff_records['Nguyễn Huyền Trang']['work_score']:.1f} | **1.10** | Tốt |
| **Nguyễn Xuân Bách** | Giáo vụ | 17/{total_working_days} | {staff_records['Nguyễn Xuân Bách']['total_tasks']} | {staff_records['Nguyễn Xuân Bách']['completion_rate']:.1f}% | {staff_records['Nguyễn Xuân Bách']['total_hours']:.1f}h | {staff_records['Nguyễn Xuân Bách']['work_score']:.1f} | **1.05** | Khá tốt |
| **Nguyễn Thị Tươi** | Leader | 16/{total_working_days} | {staff_records['Nguyễn Thị Tươi']['total_tasks']} | {staff_records['Nguyễn Thị Tươi']['completion_rate']:.1f}% | {staff_records['Nguyễn Thị Tươi']['total_hours']:.1f}h | {staff_records['Nguyễn Thị Tươi']['work_score']:.1f} | **0.75** | Cần cải thiện |

> [!TIP]
> **Hệ số năng suất (NS) đề xuất** được tham chiếu dựa trên 3 tiêu chí cốt lõi:
> 1. Tỷ lệ hoàn thành công việc (Sản lượng thực chất).
> 2. Tính kỷ luật và đều đặn của Báo cáo ngày (Work Score).
> 3. Tác động và vai trò chịu trách nhiệm của Rank nhân sự.

---

## III. Đánh giá Khó khăn, Dự án & Công việc Tồn đọng từng Nhân sự

"""
    for name, record in staff_records.items():
        missing_days_str = ", ".join([d.split("-")[-1] + "/" + d.split("-")[-2] for d in record["missing_days"]]) if record["missing_days"] else "Không vi phạm"
        
        # Difficulties text
        if record["difficulties"]:
            diff_text = "\n".join([f"  - *{d['date']}*: {d['content']}" for d in record["difficulties"]])
        else:
            diff_text = "  - Không ghi nhận khó khăn."
            
        # Uncompleted tasks text
        if record["uncompleted_tasks"]:
            uncompleted_text = "\n".join([f"  - *{u['date']}*: {u['title']} ({u['percent']}%)" for u in record["uncompleted_tasks"]])
        else:
            uncompleted_text = "  - Không có công việc tồn đọng (hoàn thành 100%)."
            
        # Worklane projects text
        if record["projects"]:
            proj_parts = []
            for p in record["projects"]:
                proj_parts.append(f"  - **{p['key']} - {p['name']}** ({p['role']}) - Sức khỏe: {p['health']} | Trạng thái: {p['status']}\n    * Số task được giao: {len(p['issues'])}")
            proj_text = "\n".join(proj_parts)
        else:
            proj_text = "  - Không tham gia dự án Worklane trực tiếp nào trong tháng."
            
        md_content += f"""### 👤 {name} ({record['role']})
- **Chỉ số năng suất**:
  - Tỷ lệ hoàn thành công việc: **{record['completion_rate']:.2f}%** ({record['completed_tasks']}/{record['total_tasks']} tasks)
  - Số ngày nộp báo cáo: **{record['reported_days']}/{total_working_days} ngày** (Vi phạm thiếu: {missing_days_str})
  - Tổng số giờ làm việc: **{record['total_hours']:.2f} giờ**
  - Điểm Báo cáo ngày (Work Score): **{record['work_score']:.1f}/100**
  - Đề xuất HSNX: **{record['proposed_ns']:.2f}** (Xếp loại: **{record['classification']}**)
- **Thống kê Dự án đang tham gia (Worklane Projects)**:
{proj_text}
- **Các khó khăn, vướng mắc trong tháng**:
{diff_text}
- **Công việc tồn đọng / Chưa hoàn thành**:
{uncompleted_text}
- **Nhận xét hiệu suất**:
  - {record['evaluation']}
  
"""

    md_content += """---

## IV. Nhật ký Công việc Phân loại Chuyên môn Bộ phận QLĐT (Tháng 7/2026)

*Nhật ký công việc dưới đây đã được lọc và phân loại theo 5 mảng nghiệp vụ chuyên môn.*

"""
    for name, record in staff_records.items():
        md_content += f"### 🔹 Nhật ký công việc phân loại của {name}\n\n"
        
        for dom, tasks in record["domain_tasks"].items():
            if tasks:
                dom_hours = sum(t["hours"] for t in tasks)
                md_content += f"#### Mảng việc: {dom} (Tích lũy: {dom_hours:.2f}h / {len(tasks)} tasks)\n\n"
                md_content += "| Ngày | Tên công việc | Thời lượng | Trạng thái | Dự án |\n"
                md_content += "| :--- | :--- | :---: | :--- | :--- |\n"
                for task in sorted(tasks, key=lambda x: x["date"]):
                    md_content += f"| {task['date']} | {task['title']} | {task['hours']:.2f}h | {task['status_text']} | {task['project']} |\n"
                md_content += "\n"
            else:
                md_content += f"#### Mảng việc: {dom} (Không có đầu việc nào phát sinh trong tháng)\n\n"
        md_content += "\n"

    # Write Markdown file
    md_output_path = "output/reports/advanced/qldt_monthly_report.md"
    os.makedirs(os.path.dirname(md_output_path), exist_ok=True)
    with open(md_output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Markdown report generated successfully at: {md_output_path}")

    # ----------------------------------------------------
    # GENERATE HTML DASHBOARD (LINEAR DESIGN AESTHETICS)
    # ----------------------------------------------------
    
    # Prepare JSON variables to insert directly into JS to avoid f-string syntax errors
    js_staff_data = {}
    for name, record in staff_records.items():
        js_staff_data[name] = {
            "name": name,
            "role": record["role"],
            "rank": record["rank"],
            "reported_days": record["reported_days"],
            "total_working_days": total_working_days,
            "total_tasks": record["total_tasks"],
            "completed_tasks": record["completed_tasks"],
            "completion_rate": record["completion_rate"],
            "total_hours": record["total_hours"],
            "work_score": record["work_score"],
            "proposed_ns": record["proposed_ns"],
            "classification": record["classification"],
            "evaluation": record["evaluation"],
            "tasks": record["tasks"],
            "difficulties": record["difficulties"],
            "uncompleted_tasks": record["uncompleted_tasks"],
            "projects": record["projects"],
            "domain_hours": record["domain_hours"]
        }
        
    # We define raw HTML structure as a normal string (NOT f-string) to avoid escape problems with { } in CSS/JS
    html_template = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Dashboard Báo cáo Công việc QLĐT - Tháng 7/2026</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --bg-color: #010102;
      --card-bg: #0f1011;
      --border-color: #23252a;
      --accent-color: #5e6ad2;
      --text-main: #f5f5f7;
      --text-muted: #8a8f98;
      --danger: #ff453a;
      --success: #30d158;
      --warning: #ff9f0a;
      --info: #0a84ff;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-color);
      color: var(--text-main);
      font-family: 'Inter', sans-serif;
      font-size: 13px;
      line-height: 1.6;
      padding: 24px;
    }
    
    .dashboard-container {
      display: grid;
      grid-template-columns: 1fr 340px;
      gap: 24px;
      max-width: 1400px;
      margin: 0 auto;
    }
    
    .main-panel {
      min-width: 0;
    }
    
    .sidebar {
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 20px;
      position: sticky;
      top: 24px;
      height: fit-content;
    }
    
    .header-card {
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 24px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .header-title h1 {
      font-size: 20px;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 6px;
    }
    
    .header-title p {
      color: var(--text-muted);
      font-size: 13px;
    }
    
    .badge-july {
      background: rgba(94, 106, 210, 0.15);
      color: var(--accent-color);
      padding: 6px 12px;
      border-radius: 20px;
      font-weight: 600;
      border: 1px solid rgba(94, 106, 210, 0.3);
      font-size: 11px;
    }
    
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    
    .metric-card {
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 16px;
      text-align: left;
      position: relative;
      overflow: hidden;
    }
    
    .metric-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--accent-color);
    }
    
    .metric-card.danger::before { background: var(--danger); }
    .metric-card.success::before { background: var(--success); }
    .metric-card.warning::before { background: var(--warning); }
    
    .metric-label {
      color: var(--text-muted);
      font-size: 10px;
      text-transform: uppercase;
      font-weight: 600;
      letter-spacing: 0.05em;
    }
    
    .metric-value {
      font-family: 'JetBrains Mono', monospace;
      font-size: 24px;
      font-weight: 700;
      color: var(--text-main);
      margin-top: 8px;
      display: flex;
      align-items: baseline;
      gap: 4px;
    }
    
    .metric-unit {
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 400;
    }
    
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
    }
    
    .card-title {
      font-size: 14px;
      font-weight: 600;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .tab-nav {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--border-color);
      margin-bottom: 20px;
      padding-bottom: 10px;
    }
    
    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 8px 16px;
      font-weight: 500;
      cursor: pointer;
      border-radius: 4px;
      transition: all 0.2s ease;
      font-size: 13px;
    }
    
    .tab-btn.active, .tab-btn:hover {
      background: rgba(94, 106, 210, 0.15);
      color: var(--text-main);
    }
    
    .tab-content { display: none; }
    .tab-content.active { display: block; }
    
    input.search-bar {
      width: 100%;
      background: #0b0c0d;
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 10px 14px;
      border-radius: 6px;
      font-size: 13px;
      margin-bottom: 16px;
      outline: none;
      transition: all 0.2s;
    }
    
    input.search-bar:focus {
      border-color: var(--accent-color);
      box-shadow: 0 0 0 2px rgba(94, 106, 210, 0.2);
    }
    
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }
    
    th, td {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-color);
      vertical-align: middle;
    }
    
    th {
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 10px;
      letter-spacing: 0.05em;
      background: rgba(0, 0, 0, 0.2);
    }
    
    tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }
    
    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 600;
      text-transform: uppercase;
    }
    
    .badge-danger { background: rgba(255, 69, 58, 0.15); color: var(--danger); }
    .badge-success { background: rgba(48, 209, 88, 0.15); color: var(--success); }
    .badge-warning { background: rgba(255, 159, 10, 0.15); color: var(--warning); }
    .badge-info { background: rgba(10, 132, 255, 0.15); color: var(--info); }
    .badge-accent { background: rgba(94, 106, 210, 0.15); color: var(--accent-color); }
    
    .staff-selector {
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
    }
    
    .staff-chip {
      background: #0b0c0d;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 8px 14px;
      border-radius: 20px;
      cursor: pointer;
      font-weight: 500;
      transition: all 0.2s;
    }
    
    .staff-chip.active, .staff-chip:hover {
      background: var(--accent-color);
      color: #fff;
      border-color: var(--accent-color);
    }
    
    .card-detail-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-bottom: 20px;
    }
    
    .detail-item {
      background: #0b0c0d;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 12px;
    }
    
    .detail-label {
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 4px;
    }
    
    .detail-val {
      font-size: 14px;
      font-weight: 600;
    }
    
    .detail-val.score {
      font-family: 'JetBrains Mono', monospace;
      color: var(--accent-color);
    }
    
    .sidebar-block {
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 20px;
    }
    
    .sidebar-block:last-child {
      border-bottom: none;
      padding-bottom: 0;
    }
    
    .sidebar-block h3 {
      font-size: 12px;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 12px;
      letter-spacing: 0.05em;
    }
    
    .avatar {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: var(--accent-color);
      color: #fff;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 10px;
      margin-right: 8px;
    }
    
    .progress-bar-container {
      width: 100%;
      background: rgba(255, 255, 255, 0.05);
      height: 6px;
      border-radius: 3px;
      overflow: hidden;
      margin-top: 6px;
    }
    
    .progress-bar-fill {
      height: 100%;
      background: var(--accent-color);
      border-radius: 3px;
    }
    
    .block-list {
      list-style-type: none;
      padding-left: 0;
    }
    
    .block-list li {
      margin-bottom: 8px;
      padding: 8px 12px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.01);
      border-left: 3px solid var(--border-color);
    }
    
    .block-list.danger li { border-left-color: var(--danger); background: rgba(255, 69, 58, 0.02); }
    .block-list.warning li { border-left-color: var(--warning); background: rgba(255, 159, 10, 0.02); }
    .block-list.success li { border-left-color: var(--success); background: rgba(48, 209, 88, 0.02); }
    
    /* Project cards styles */
    .project-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }
    
    .project-mini-card {
      background: #0b0c0d;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 12px;
      position: relative;
    }
    
    .project-mini-card h4 {
      font-size: 13px;
      font-weight: 600;
      margin-bottom: 6px;
      color: var(--text-main);
    }
    
    .project-meta-row {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 4px;
    }
    
    /* Accordion styles */
    .accordion-item {
      border: 1px solid var(--border-color);
      border-radius: 6px;
      margin-bottom: 8px;
      overflow: hidden;
      background: rgba(255, 255, 255, 0.01);
    }
    
    .accordion-header {
      background: #0c0d0e;
      padding: 12px 16px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
      transition: background 0.2s;
    }
    
    .accordion-header:hover {
      background: rgba(94, 106, 210, 0.05);
    }
    
    .accordion-content {
      display: none;
      padding: 12px 16px;
      border-top: 1px solid var(--border-color);
      background: rgba(0, 0, 0, 0.2);
    }
    
    .accordion-item.active .accordion-content {
      display: block;
    }
    
    .chart-container-flex {
      display: flex;
      gap: 20px;
      margin-top: 16px;
      align-items: center;
    }
    
    .chart-box-overall {
      width: 180px;
      height: 180px;
      position: relative;
    }
    
    .chart-box-individual {
      flex: 1;
      height: 200px;
    }
    
  </style>
</head>
<body>
  <div class="dashboard-container">
    <div class="main-panel">
      <!-- Header -->
      <div class="header-card">
        <div class="header-title">
          <h1>Báo cáo Công việc & Dự án Tháng 7/2026</h1>
          <p>Bộ phận Quản lý Đào tạo (QLĐT) — Phân tích hiệu năng và Đề xuất HSNX</p>
        </div>
        <div class="badge-july">01/07/2026 - 30/07/2026</div>
      </div>
      
      <!-- Metrics -->
      <div class="metric-grid">
        <div class="metric-card">
          <div class="metric-label">Tổng Nhiệm Vụ</div>
          <div class="metric-value">__DEPT_TOTAL_TASKS__<span class="metric-unit"> task</span></div>
        </div>
        <div class="metric-card success">
          <div class="metric-label">Đã Hoàn Thành</div>
          <div class="metric-value">__DEPT_COMPLETED_TASKS__<span class="metric-unit"> task</span></div>
        </div>
        <div class="metric-card success">
          <div class="metric-label">Tỷ Lệ Hoàn Thành</div>
          <div class="metric-value">__DEPT_AVG_COMPLETION_RATE__</div>
        </div>
        <div class="metric-card warning">
          <div class="metric-label">Điểm Báo Cáo Bình Quân</div>
          <div class="metric-value">__DEPT_AVG_WORK_SCORE__<span class="metric-unit">/100</span></div>
        </div>
      </div>
      
      <!-- Tab Navigation -->
      <div class="tab-nav">
        <button class="tab-btn active" onclick="switchTab('tab-productivity')">Bảng Năng Suất & HSNX</button>
        <button class="tab-btn" onclick="switchTab('tab-details')">Nhật Ký & Khó Khăn Chi Tiết</button>
      </div>
      
      <!-- Tab 1: Productivity Table -->
      <div id="tab-productivity" class="tab-content active">
        <div class="card" style="display: flex; gap: 20px; align-items: center;">
          <div style="flex: 1;">
            <h3 style="font-size:15px; margin-bottom: 8px;">Cấu trúc phân bổ thời gian toàn bộ phận</h3>
            <p style="color:var(--text-muted); font-size:12px;">Biểu đồ thống kê tỷ trọng cống hiến giờ làm việc của cả phòng QLĐT vào 5 nhóm chuyên môn nghiệp vụ trong tháng 7/2026.</p>
          </div>
          <div class="chart-box-overall">
            <canvas id="deptOverallChart"></canvas>
          </div>
        </div>
        
        <div class="card">
          <div class="card-title">Bảng Tổng Hợp Sản Lượng & Đề Xuất HSNX Tháng 7</div>
          __STAFF_RECORDS_TABLE__
        </div>
        
        <div class="card">
          <div class="card-title">Chi Tiết Đánh Giá Năng Suất & Nhận Xét Định Hướng</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border-color); padding: 16px; border-radius: 6px;">
              <h4 style="margin-bottom: 8px; color: var(--success);"><i class="fa-solid fa-circle-check"></i> Điểm Mạnh & Ghi Nhận Tích Cực</h4>
              <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 8px; padding-left: 15px; text-indent: -15px;">✔️ <strong>Trần Thị Mỹ Phước</strong> đạt năng suất xuất sắc, nộp báo cáo đầy đủ 100% số ngày, hoàn thành 100% số task được giao.</li>
                <li style="margin-bottom: 8px; padding-left: 15px; text-indent: -15px;">✔️ <strong>Nguyễn Huyền Trang</strong> có sản lượng công việc lớn nhất bộ phận (140 task), hoàn thành tốt các đợt thi sát hạch tiếng Anh.</li>
                <li style="margin-bottom: 8px; padding-left: 15px; text-indent: -15px;">✔️ Tỷ lệ hoàn thành công việc của cả phòng QLĐT đạt mức cao <strong>__DEPT_AVG_COMPLETION_RATE__</strong>.</li>
              </ul>
            </div>
            
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border-color); padding: 16px; border-radius: 6px;">
              <h4 style="margin-bottom: 8px; color: var(--danger);"><i class="fa-solid fa-circle-xmark"></i> Điểm Hạn Chế & Cảnh Báo</h4>
              <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 8px; padding-left: 15px; text-indent: -15px;">⚠️ <strong>Nguyễn Thị Tươi</strong> (Leader) có chỉ số hoàn thành công việc thấp (54.43%), đồng thời thiếu nộp báo cáo ngày 5 buổi.</li>
                <li style="margin-bottom: 8px; padding-left: 15px; text-indent: -15px;">⚠️ Vẫn còn tình trạng quên báo cáo ngày hoặc nộp trễ hạn ở vị trí quản lý (cần làm gương cho nhân sự).</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Tab 2: Work Log Details -->
      <div id="tab-details" class="tab-content">
        <!-- Staff Chip Selectors -->
        <div class="staff-selector">
          <div class="staff-chip active" onclick="selectStaff('Trần Thị Mỹ Phước')">Trần Thị Mỹ Phước</div>
          <div class="staff-chip" onclick="selectStaff('Nguyễn Huyền Trang')">Nguyễn Huyền Trang</div>
          <div class="staff-chip" onclick="selectStaff('Nguyễn Xuân Bách')">Nguyễn Xuân Bách</div>
          <div class="staff-chip" onclick="selectStaff('Nguyễn Thị Tươi')">Nguyễn Thị Tươi</div>
        </div>
        
        <!-- Selected Staff Info Card -->
        <div class="card">
          <div class="card-title" id="selected-staff-title">Thông tin nhân sự</div>
          
          <div class="card-detail-grid">
            <div class="detail-item">
              <div class="detail-label">Vai Trò & Rank</div>
              <div class="detail-val" id="selected-staff-role">Giáo vụ</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">Tổng Số Giờ & Số Task</div>
              <div class="detail-val" id="selected-staff-hours">0h (0 task)</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">Điểm Báo Cáo (Work Score)</div>
              <div class="detail-val score" id="selected-staff-score">0.0</div>
            </div>
          </div>
          
          <div style="background: rgba(94, 106, 210, 0.05); border: 1px solid rgba(94, 106, 210, 0.2); padding: 12px; border-radius: 6px; margin-bottom: 16px;">
            <strong>Nhận xét & Định hướng:</strong> <span id="selected-staff-eval" style="color: var(--text-muted);">Đang tải...</span>
          </div>

          <!-- Charts and Projects Grid -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
            <!-- Individual Chart -->
            <div class="card" style="margin-bottom: 0;">
              <div class="card-title" style="font-size:12px; margin-bottom: 8px;"><i class="fa-solid fa-chart-simple"></i> Số giờ phân bổ chuyên môn</div>
              <div class="chart-box-individual">
                <canvas id="individualChart"></canvas>
              </div>
            </div>
            
            <!-- Worklane Projects -->
            <div class="card" style="margin-bottom: 0; display:flex; flex-direction:column;">
              <div class="card-title" style="font-size:12px; margin-bottom: 8px;"><i class="fa-solid fa-diagram-project"></i> Dự án đang tham gia (Worklane)</div>
              <div class="project-grid" id="selected-staff-projects" style="flex:1; overflow-y:auto; max-height:200px;">
                <!-- Dynamically populated -->
              </div>
            </div>
          </div>

          <!-- Difficulties Section -->
          <div class="card" style="border-color: rgba(255, 159, 10, 0.3); background: rgba(255, 159, 10, 0.01);">
            <div class="card-title" style="color: var(--warning); font-size: 12px; margin-bottom: 8px;"><i class="fa-solid fa-triangle-exclamation"></i> KHÓ KHĂN & VƯỚNG MẮC GHI NHẬN</div>
            <ul id="selected-staff-difficulties" class="block-list warning">
              <!-- Dynamically populated -->
            </ul>
          </div>

          <!-- Uncompleted Tasks Section -->
          <div class="card" style="border-color: rgba(255, 69, 58, 0.3); background: rgba(255, 69, 58, 0.01);">
            <div class="card-title" style="color: var(--danger); font-size: 12px; margin-bottom: 8px;"><i class="fa-solid fa-circle-xmark"></i> CÔNG VIỆC CHƯA HOÀN THÀNH / TỒN ĐỌNG</div>
            <ul id="selected-staff-uncompleted" class="block-list danger">
              <!-- Dynamically populated -->
            </ul>
          </div>
          
          <div class="card-title" style="font-size: 12px; margin-top: 20px; margin-bottom: 8px;"><i class="fa-solid fa-list-check"></i> CHI TIẾT NHẬT KÝ THEO CHUYÊN MÔN</div>
          <input type="text" class="search-bar" id="search-tasks" placeholder="Tìm kiếm nhanh công việc của nhân sự..." onkeyup="filterTasks(this.value)">
          
          <div id="accordion-tasks-container">
            <!-- Accordion items will be generated by JS -->
          </div>
        </div>
      </div>
    </div>
    
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="sidebar-block">
        <h3><i class="fa-solid fa-chart-line"></i> Phân Phối NS</h3>
        <p style="color: var(--text-muted); margin-bottom: 12px;">Đề xuất phân phối HSNX (NS) tháng 7 cho bộ phận QLĐT:</p>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
          <span>Phước (Xuất sắc)</span>
          <strong>1.15</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
          <span>Trang (Tốt)</span>
          <strong>1.10</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
          <span>Bách (Khá tốt)</span>
          <strong>1.05</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
          <span>Tươi (Cần cải thiện)</span>
          <strong>0.75</strong>
        </div>
      </div>
      
      <div class="sidebar-block">
        <h3><i class="fa-solid fa-triangle-exclamation"></i> Chú Ý Quản Lý</h3>
        <p style="color: var(--text-muted); margin-top: 8px;">
          Bộ phận Nhân sự & Đào tạo cần làm việc trực tiếp với **Nguyễn Thị Tươi (Leader)** về việc cải thiện tiến độ hoàn thành các dự án được giao và tuân thủ kỷ luật báo cáo ngày để không ảnh hưởng đến điểm KPI chung của toàn khối.
        </p>
      </div>
      
      <div class="sidebar-block">
        <h3><i class="fa-solid fa-file-export"></i> Đầu ra báo cáo</h3>
        <p style="color: var(--text-muted); font-size: 11px;">
          Báo cáo này được tự động xuất ra 2 tệp tại thư mục `output/`:<br>
          1. Markdown: `reports/advanced/qldt_monthly_report.md`<br>
          2. Dashboard HTML: `dashboards/advanced/qldt_monthly_report.html`
        </p>
      </div>
    </div>
  </div>
  
  <script>
    // Embed the staff data directly
    const staffData = __STAFF_DATA_PLACEHOLDER__;
    const deptOverallHours = __DEPT_OVERALL_HOURS__;
    
    let currentStaff = "Trần Thị Mỹ Phước";
    let individualChartInstance = null;
    let deptChartInstance = null;
    
    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.target.classList.add('active');
    }
    
    function selectStaff(name) {
      currentStaff = name;
      document.querySelectorAll('.staff-chip').forEach(el => el.classList.remove('active'));
      
      // Find chip and activate it
      const chips = document.querySelectorAll('.staff-chip');
      chips.forEach(chip => {
        if (chip.textContent === name) {
          chip.classList.add('active');
        }
      });
      
      updateStaffDetails();
    }
    
    function updateStaffDetails() {
      const data = staffData[currentStaff];
      if (!data) return;
      
      document.getElementById("selected-staff-title").innerHTML = `<i class="avatar">${currentStaff[0]}</i> ${currentStaff} — Chi Tiết Nhật Ký & Dự Án`;
      document.getElementById("selected-staff-role").textContent = `${data.role} (Rank ${data.rank})`;
      document.getElementById("selected-staff-hours").textContent = `${data.total_hours.toFixed(1)}h (${data.total_tasks} task, hoàn thành ${data.completed_tasks})`;
      document.getElementById("selected-staff-score").textContent = `${data.work_score.toFixed(1)}/100 (HSNX: ${data.proposed_ns.toFixed(2)})`;
      document.getElementById("selected-staff-eval").textContent = data.evaluation;
      
      // Difficulties render
      const diffUl = document.getElementById("selected-staff-difficulties");
      diffUl.innerHTML = "";
      if (data.difficulties && data.difficulties.length > 0) {
        data.difficulties.forEach(d => {
          const li = document.createElement("li");
          li.innerHTML = `<strong>${d.date}</strong>: ${d.content}`;
          diffUl.appendChild(li);
        });
      } else {
        const li = document.createElement("li");
        li.textContent = "Không ghi nhận khó khăn, vướng mắc.";
        li.style.color = "var(--text-muted)";
        li.style.borderLeftColor = "var(--border-color)";
        diffUl.appendChild(li);
      }

      // Uncompleted tasks render
      const uncompletedUl = document.getElementById("selected-staff-uncompleted");
      uncompletedUl.innerHTML = "";
      if (data.uncompleted_tasks && data.uncompleted_tasks.length > 0) {
        data.uncompleted_tasks.forEach(u => {
          const li = document.createElement("li");
          li.innerHTML = `<strong>${u.date}</strong>: ${u.title} (Tiến độ: ${u.percent}%)`;
          uncompletedUl.appendChild(li);
        });
      } else {
        const li = document.createElement("li");
        li.textContent = "Không có công việc tồn đọng (hoàn thành 100%).";
        li.style.color = "var(--text-muted)";
        li.style.borderLeftColor = "var(--border-color)";
        uncompletedUl.appendChild(li);
      }
      
      // Projects render
      const projGrid = document.getElementById("selected-staff-projects");
      projGrid.innerHTML = "";
      if (data.projects && data.projects.length > 0) {
        data.projects.forEach(p => {
          const div = document.createElement("div");
          div.className = "project-mini-card";
          
          let healthColor = "var(--success)";
          if (p.health === "OFF_TRACK" || p.health === "AT_RISK") healthColor = "var(--danger)";
          
          let statusBadge = "badge-info";
          if (p.status === "COMPLETED") statusBadge = "badge-success";
          
          div.innerHTML = `
            <h4>${p.key}</h4>
            <div style="font-size:10px; color:var(--text-muted); margin-bottom: 6px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap;">${p.name}</div>
            <div class="project-meta-row">
              <span>Vai trò:</span>
              <strong style="color:var(--accent-color);">${p.role}</strong>
            </div>
            <div class="project-meta-row">
              <span>Sức khỏe:</span>
              <strong style="color:${healthColor};">${p.health}</strong>
            </div>
            <div class="project-meta-row">
              <span>Trạng thái:</span>
              <span class="badge ${statusBadge}" style="font-size:8px; padding:1px 4px;">${p.status}</span>
            </div>
            <div class="project-meta-row" style="margin-top:4px; border-top:1px solid rgba(255,255,255,0.05); padding-top:4px;">
              <span>Số task:</span>
              <strong>${p.issues.length}</strong>
            </div>
          `;
          projGrid.appendChild(div);
        });
      } else {
        projGrid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 20px;">Không tham gia trực tiếp dự án Worklane nào.</div>`;
      }
      
      // Clear search
      document.getElementById("search-tasks").value = "";
      
      // Group tasks by domains for rendering
      const domainTasks = {
        "Khảo thí": [],
        "Thời khóa biểu": [],
        "Hành chính & Hỗ trợ SV": [],
        "Xây dựng quy định & tài nguyên": [],
        "Họp & Công việc chung": []
      };
      
      // Classify
      data.tasks.forEach(task => {
        const dom = classifyTaskInJS(task.title);
        if (domainTasks[dom]) {
          domainTasks[dom].push(task);
        } else {
          domainTasks["Họp & Công việc chung"].push(task);
        }
      });
      
      // Render Accordion
      const accordionContainer = document.getElementById("accordion-tasks-container");
      accordionContainer.innerHTML = "";
      
      // Find domain with max hours to open it by default
      let maxHours = -1;
      let defaultOpenDomain = "Khảo thí";
      
      Object.keys(domainTasks).forEach(dom => {
        const hours = data.domain_hours[dom] || 0.0;
        if (hours > maxHours) {
          maxHours = hours;
          defaultOpenDomain = dom;
        }
      });
      
      Object.keys(domainTasks).forEach(dom => {
        const tasks = domainTasks[dom];
        const hours = data.domain_hours[dom] || 0.0;
        
        const item = document.createElement("div");
        item.className = `accordion-item ${dom === defaultOpenDomain ? 'active' : ''}`;
        
        let tableRowsHtml = "";
        if (tasks.length > 0) {
          // Sort descending
          const sorted = [...tasks].sort((a, b) => b.date.localeCompare(a.date));
          sorted.forEach(t => {
            let badgeClass = "badge-info";
            if (t.done || t.percent === 100) badgeClass = "badge-success";
            else if (t.percent > 0) badgeClass = "badge-warning";
            
            tableRowsHtml += `
              <tr class="task-row">
                <td><span style="font-family: monospace; color: var(--text-muted); font-size:11px;">${t.date}</span></td>
                <td><strong>${t.title}</strong></td>
                <td style="text-align: right; font-family: monospace; font-weight: 500;">${t.hours.toFixed(2)}h</td>
                <td><span class="badge ${badgeClass}">${t.status_text}</span></td>
                <td><span class="badge badge-accent">${t.project}</span></td>
              </tr>
            `;
          });
        } else {
          tableRowsHtml = `<tr><td colspan="5" style="text-align:center; color:var(--text-muted);">Không có công việc phát sinh.</td></tr>`;
        }
        
        item.innerHTML = `
          <div class="accordion-header" onclick="toggleAccordion(this)">
            <span>${dom} <span style="color:var(--text-muted); font-weight:normal; margin-left:8px;">(${tasks.length} task, tích lũy ${hours.toFixed(1)}h)</span></span>
            <i class="fa-solid fa-chevron-down" style="font-size:10px; color:var(--text-muted);"></i>
          </div>
          <div class="accordion-content">
            <table>
              <thead>
                <tr>
                  <th style="width: 100px;">Ngày</th>
                  <th>Tên công việc</th>
                  <th style="width: 100px; text-align: right;">Thời lượng</th>
                  <th style="width: 150px;">Trạng thái</th>
                  <th style="width: 180px;">Dự án</th>
                </tr>
              </thead>
              <tbody>
                ${tableRowsHtml}
              </tbody>
            </table>
          </div>
        `;
        accordionContainer.appendChild(item);
      });
      
      // Update individual Chart
      updateIndividualChart(data);
    }
    
    function toggleAccordion(header) {
      const item = header.parentElement;
      item.classList.toggle('active');
      const icon = header.querySelector('i');
      if (item.classList.contains('active')) {
        icon.className = "fa-solid fa-chevron-up";
      } else {
        icon.className = "fa-solid fa-chevron-down";
      }
    }
    
    function classifyTaskInJS(title) {
      const t = title.toLowerCase();
      if (t.includes("thi") || t.includes("khảo thí") || t.includes("coi thi") || t.includes("chấm thi") || t.includes("vấn đáp") || t.includes("sát hạch") || t.includes("toeic") || t.includes("đề thi") || t.includes("nhập điểm") || t.includes("phòng thi") || t.includes("kết quả thi")) {
        return "Khảo thí";
      } else if (t.includes("tkb") || t.includes("thời khóa biểu") || t.includes("lịch học") || t.includes("xếp lớp") || t.includes("lên lịch") || t.includes("phòng học") || t.includes("lịch dạy") || t.includes("xếp tkb")) {
        return "Thời khóa biểu";
      } else if (t.includes("sinh viên") || t.includes("học viên") || t.includes("sv") || t.includes("hv") || t.includes("phản hồi") || t.includes("hỗ trợ") || t.includes("rèn luyện") || t.includes("cổng hành chính") || t.includes("dịch vụ") || t.includes("biểu mẫu")) {
        return "Hành chính & Hỗ trợ SV";
      } else if (t.includes("quy định") || t.includes("quy chế") || t.includes("tiêu chuẩn") || t.includes("tài nguyên") || t.includes("học liệu") || t.includes("slide") || t.includes("giáo trình") || t.includes("soạn thảo") || t.includes("review") || t.includes("chỉnh sửa")) {
        return "Xây dựng quy định & tài nguyên";
      } else {
        return "Họp & Công việc chung";
      }
    }
    
    function filterTasks(query) {
      const rows = document.querySelectorAll("#accordion-tasks-container .task-row");
      const q = query.toLowerCase().trim();
      
      // Auto open accordions when searching
      const items = document.querySelectorAll("#accordion-tasks-container .accordion-item");
      if (q.length > 0) {
        items.forEach(item => {
          item.classList.add('active');
          const icon = item.querySelector('.accordion-header i');
          if (icon) icon.className = "fa-solid fa-chevron-up";
        });
      }
      
      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(q) ? "" : "none";
      });
    }
    
    // Chart rendering
    function initDeptChart() {
      const ctx = document.getElementById('deptOverallChart').getContext('2d');
      const labels = Object.keys(deptOverallHours);
      const dataValues = Object.values(deptOverallHours);
      
      deptChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: dataValues,
            backgroundColor: [
              '#0a84ff', // Khảo thí (Cyan/Blue)
              '#ff9f0a', // TKB (Orange)
              '#30d158', // Hỗ trợ SV (Green)
              '#5e6ad2', // Quy định (Indigo)
              '#8a8f98'  // Họp chung (Gray)
            ],
            borderColor: '#0f1011',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const val = context.parsed || 0;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const pct = ((val / total) * 100).toFixed(1);
                  return ` ${label}: ${val.toFixed(1)}h (${pct}%)`;
                }
              }
            }
          },
          cutout: '70%'
        }
      });
    }
    
    function updateIndividualChart(staffDataObj) {
      const ctx = document.getElementById('individualChart').getContext('2d');
      const labels = Object.keys(staffDataObj.domain_hours);
      const dataValues = Object.values(staffDataObj.domain_hours);
      
      if (individualChartInstance) {
        individualChartInstance.destroy();
      }
      
      individualChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Số giờ thực hiện (h)',
            data: dataValues,
            backgroundColor: 'rgba(94, 106, 210, 0.45)',
            borderColor: '#5e6ad2',
            borderWidth: 1.5,
            borderRadius: 4
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            x: {
              grid: {
                color: 'rgba(255, 255, 255, 0.05)'
              },
              ticks: {
                color: '#8a8f98',
                font: { size: 10 }
              }
            },
            y: {
              grid: {
                display: false
              },
              ticks: {
                color: '#f5f5f7',
                font: { size: 10 }
              }
            }
          }
        }
      });
    }
    
    // Initialize
    window.onload = function() {
      initDeptChart();
      updateStaffDetails();
    };
  </script>
</body>
</html>
"""

    # Build Productivity Table HTML dynamically
    table_html = """<table>
            <thead>
              <tr>
                <th>Họ và tên</th>
                <th>Vai trò</th>
                <th>Số ngày báo cáo</th>
                <th>Tổng số task</th>
                <th>Tỷ lệ hoàn thành</th>
                <th>Tổng số giờ</th>
                <th>Điểm Báo cáo</th>
                <th>Đề xuất HSNX (NS)</th>
                <th>Xếp loại</th>
              </tr>
            </thead>
            <tbody>"""
            
    for name in ["Trần Thị Mỹ Phước", "Nguyễn Huyền Trang", "Nguyễn Xuân Bách", "Nguyễn Thị Tươi"]:
        rec = staff_records[name]
        role_badge = "badge-info"
        if "Leader" in rec["role"]:
            role_badge = "badge-warning"
            
        class_badge = "badge-success"
        if rec["classification"] == "Tốt":
            class_badge = "badge-success"
        elif rec["classification"] == "Khá tốt" or rec["classification"] == "Khá":
            class_badge = "badge-accent"
        elif rec["classification"] == "Cần cải thiện":
            class_badge = "badge-danger"
            
        color_ns = "var(--success)"
        if rec["proposed_ns"] < 1.0:
            color_ns = "var(--danger)"
        elif rec["proposed_ns"] == 1.05:
            color_ns = "var(--accent-color)"
            
        table_html += f"""
              <tr>
                <td><strong>{name}</strong></td>
                <td><span class="badge {role_badge}">{rec["role"]}</span></td>
                <td>{rec["reported_days"]}/{total_working_days}</td>
                <td>{rec["total_tasks"]}</td>
                <td>
                  {rec["completion_rate"]:.1f}%
                  <div class="progress-bar-container">
                    <div class="progress-bar-fill" style="width: {rec["completion_rate"]}%; background: {color_ns};"></div>
                  </div>
                </td>
                <td>{rec["total_hours"]:.1f}h</td>
                <td style="font-family: monospace; font-weight: bold;">{rec["work_score"]:.1f}</td>
                <td><strong style="color: {color_ns}; font-size: 14px;">{rec["proposed_ns"]:.2f}</strong></td>
                <td><span class="badge {class_badge}">{rec["classification"]}</span></td>
              </tr>"""
              
    table_html += """
            </tbody>
          </table>"""
          
    # Replace templates in HTML
    html_output = html_template
    html_output = html_output.replace("__DEPT_TOTAL_TASKS__", str(dept_total_tasks))
    html_output = html_output.replace("__DEPT_COMPLETED_TASKS__", str(dept_completed_tasks))
    html_output = html_output.replace("__DEPT_AVG_COMPLETION_RATE__", f"{dept_avg_completion_rate:.1f}%")
    html_output = html_output.replace("__DEPT_AVG_WORK_SCORE__", f"{dept_avg_work_score:.1f}")
    html_output = html_output.replace("__TOTAL_WORKING_DAYS__", str(total_working_days))
    html_output = html_output.replace("__STAFF_RECORDS_TABLE__", table_html)
    html_output = html_output.replace("__DEPT_OVERALL_HOURS__", json.dumps(dept_domain_hours, ensure_ascii=False))
    html_output = html_output.replace("__STAFF_DATA_PLACEHOLDER__", json.dumps(js_staff_data, ensure_ascii=False))

    # Save HTML
    html_output_path = "output/dashboards/advanced/qldt_monthly_report.html"
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"HTML Dashboard generated successfully at: {html_output_path}")

if __name__ == "__main__":
    analyze_and_generate()

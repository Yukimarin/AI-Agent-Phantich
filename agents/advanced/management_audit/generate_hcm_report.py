# -*- coding: utf-8 -*-
import json
import os
import sys
import datetime
import re
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

# ============ CONFIGURATION ============
DAILY_LOG_ANALYSIS_PATH = "data/processed/daily_log_analysis.json"
PROJECT_ISSUES_PATH = "data/processed/project_issues_worklane.json"
TEMPLATE_HTML_PATH = r"C:\Users\DELL\Desktop\AI-Agent\AI_Report_NN\output\Bao_Cao_Tong_Hop_NN.html"
OUTPUT_HTML_PATH = "output/dashboards/advanced/Bao_Cao_Tong_Hop_HCM.html"

# 9 nhân sự HCM
PERSONNEL_CONFIG = {
    "Nguyễn Bá Minh Đạo": {"role": "Leader", "team": "GV_LEADER", "work_type": "Full-time", "target_hours": 8.0},
    "Lê Hà Thanh Sang": {"role": "Giảng viên", "team": "GV_LEADER", "work_type": "Full-time", "target_hours": 8.0},
    "Trần Quốc Tuấn": {"role": "Giảng viên", "team": "GV_LEADER", "work_type": "Full-time", "target_hours": 8.0},
    "Nguyễn Đức Minh": {"role": "Trợ giảng thử việc", "team": "TG", "work_type": "Full-time", "target_hours": 8.0},
    "Đặng Minh Luân": {"role": "Trợ giảng thử việc", "team": "TG", "work_type": "Full-time", "target_hours": 8.0},
    "Lưu Hoàng Xuân Nguyên": {"role": "Trợ giảng", "team": "TG", "work_type": "Full-time", "target_hours": 8.0},
    "Phan Ngọc Tài": {"role": "Trợ giảng thử việc", "team": "TG", "work_type": "Full-time", "target_hours": 8.0},
    "Nguyễn Ngọc Sơn": {"role": "Trợ giảng thử việc", "team": "TG", "work_type": "Full-time", "target_hours": 8.0},
    "Phạm Viết Hùng": {"role": "Trợ giảng", "team": "TG", "work_type": "Full-time", "target_hours": 8.0}
}

WEEKS_CONFIG = [
    ("W27", "Tuần 27 (01-03/07)", ["2026-07-01", "2026-07-02", "2026-07-03"]),
    ("W28", "Tuần 28 (06-10/07)", ["2026-07-06", "2026-07-07", "2026-07-08", "2026-07-09", "2026-07-10"]),
    ("W29", "Tuần 29 (13-17/07)", ["2026-07-13", "2026-07-14", "2026-07-15", "2026-07-16", "2026-07-17"]),
    ("W30", "Tuần 30 (20-24/07)", ["2026-07-20", "2026-07-21", "2026-07-22", "2026-07-23", "2026-07-24"]),
    ("W31", "Tuần 31 (27-31/07)", ["2026-07-27", "2026-07-28", "2026-07-29", "2026-07-30", "2026-07-31"]),
    ("W32", "Tuần 32 (03-07/08)", ["2026-08-03", "2026-08-04", "2026-08-05", "2026-08-06", "2026-08-07"]),
    ("W33", "Tuần 33 (10-14/08)", ["2026-08-10", "2026-08-11", "2026-08-12", "2026-08-13", "2026-08-14"]),
    ("W34", "Tuần 34 (17-21/08)", ["2026-08-17", "2026-08-18", "2026-08-19", "2026-08-20", "2026-08-21"])
]

ALL_DATES = []
WEEKS = {}
for wk, label, dates in WEEKS_CONFIG:
    WEEKS[wk] = {"label": label, "dates": dates}
    ALL_DATES.extend(dates)

KPI_KEYWORDS = [
    "giảng dạy", "thực hành", "lý thuyết", "khảo thí", "đề thi", "chấm thi", "coi thi", 
    "vấn đáp", "chấm bài", "dự giờ", "chăm sóc sinh viên", "họp", "giáo án", "slide", 
    "lesson", "mindmap", "video", "quiz", "bài tập", "chương trình", "microservice", 
    "fastapi", "python", "java", "database", "sql", "hackathon", "project", "demo", 
    "review", "training", "coaching", "mentee", "mentor", "sản xuất tài nguyên", 
    "xây dựng học liệu", "lên kế hoạch", "định hướng"
]

def remove_accents(input_str):
    import unicodedata
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def normalize_name(name):
    return remove_accents(name).lower().strip().replace(" ", "")

def main():
    print("🚀 Bắt đầu tổng hợp dữ liệu nhân sự HCM...")
    
    # 1. Đọc dữ liệu daily logs
    try:
        with open(DAILY_LOG_ANALYSIS_PATH, "r", encoding="utf-8") as f:
            daily_data = json.load(f)
    except Exception as e:
        print(f"✗ Lỗi đọc file {DAILY_LOG_ANALYSIS_PATH}: {e}")
        return

    # 2. Đọc dữ liệu projects
    try:
        with open(PROJECT_ISSUES_PATH, "r", encoding="utf-8") as f:
            project_data = json.load(f)
    except Exception as e:
        print(f"✗ Lỗi đọc file {PROJECT_ISSUES_PATH}: {e}")
        return

    raw_reports = daily_data.get("raw_reports", {})
    
    # Chuẩn bị map tên nhân sự
    norm_to_full = {normalize_name(name): name for name in PERSONNEL_CONFIG}
    
    # Trích xuất daily logs chi tiết của từng người
    person_daily = defaultdict(dict)
    adhoc_tasks = []
    
    # Tìm kiếm logs của 9 nhân sự HCM trong các group của raw_reports
    for group_name, members in raw_reports.items():
        for m_name, m_data in members.items():
            m_norm = normalize_name(m_name)
            # Khắc phục lỗi viết tắt của Nguyên ("Lưu Xuân Hoàng Nguyên" vs "Lưu Hoàng Xuân Nguyên")
            if "hoangxuannguyen" in m_norm or "xuanhoangnguyen" in m_norm:
                matched_name = "Lưu Hoàng Xuân Nguyên"
            else:
                matched_name = norm_to_full.get(m_norm)
                if not matched_name:
                    # Thử tìm kiếm tương đối nếu không khớp tuyệt đối
                    for target_norm, full_name in norm_to_full.items():
                        if target_norm in m_norm or m_norm in target_norm:
                            matched_name = full_name
                            break
                            
            if matched_name:
                reports = m_data.get("reports", {})
                for d, r_content in reports.items():
                    if r_content is None:
                        continue
                    
                    tasks = r_content.get("tasks", [])
                    kpi_hrs = 0.0
                    adhoc_hrs = 0.0
                    day_tasks_list = []
                    
                    for t in tasks:
                        title = t.get("title", "")
                        hours = float(t.get("hours", 0))
                        done = t.get("done", True)
                        percent = t.get("percent", 100)
                        
                        # Phân loại KPI vs Ad-hoc
                        title_lower = title.lower()
                        is_kpi = False
                        for kw in KPI_KEYWORDS:
                            if kw in title_lower:
                                is_kpi = True
                                break
                        
                        status_text = "Đã hoàn thành" if done else f"Đang thực hiện ({percent}%)"
                        day_tasks_list.append({
                            "title": title,
                            "hours": hours,
                            "status_text": status_text
                        })
                        
                        if is_kpi:
                            kpi_hrs += hours
                        else:
                            adhoc_hrs += hours
                            adhoc_tasks.append({
                                "date": d,
                                "name": matched_name,
                                "title": title,
                                "hours": hours
                            })
                            
                    person_daily[matched_name][d] = {
                        "hours": kpi_hrs + adhoc_hrs,
                        "kpi_hours": kpi_hrs,
                        "adhoc_hours": adhoc_hrs,
                        "tasks": len(tasks),
                        "done": sum(1 for t in tasks if t.get("done", True)),
                        "day_tasks": day_tasks_list
                    }

    # 3. Tính toán thời điểm hiện tại trừ 1 ngày làm mốc giới hạn báo cáo (Vấn đề 2)
    # Lấy ngày hiện tại thực tế trừ đi 1 ngày.
    today_str = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    print(f"📅 Thời gian giới hạn ghi nhận báo cáo (hết ngày hôm qua): {today_str}")
        
    wload_active = defaultdict(int)
    wload_overdue = defaultdict(int)
    wload_total = defaultdict(int)
    
    # 4. Xử lý dự án & issues
    projects_list = []
    overdue_all = []
    
    # Định dạng của project_data có thể là dict hoặc list
    projects_raw = []
    if isinstance(project_data, dict):
        if "projects" in project_data:
            projects_raw = project_data["projects"]
            if isinstance(projects_raw, dict):
                projects_raw = [{"key": k, **v} for k, v in projects_raw.items()]
        else:
            projects_raw = [{"key": k, **v} for k, v in project_data.items()]
    else:
        projects_raw = project_data
        
    for proj in projects_raw:
        info = proj.get("project_info", {})
        key = proj.get("key", info.get("key", ""))
        p_name = info.get("name", "Unknown")
        status = info.get("status", "ACTIVE")
        if status.upper() in ["CANCEL", "CANCELLED", "HỦY", "HUY"]:
            continue
            
        # Loại bỏ hoàn toàn các dự án Ngoại ngữ (Tiếng Nhật, Tiếng Anh)
        p_name_upper = p_name.upper()
        key_upper = key.upper()
        is_foreign = False
        if key in ["PTITQUAN", "PTITSAN3", "PTITXAY", "REKHAO", "REXPCHUO", "REXPENGL", "QLDTXAY"]:
            is_foreign = True
        for kw in ["TIẾNG NHẬT", "TIẾNG ANH", "JPN", "ENGLISH", "TOEIC", "IELTS", "RIKI", "PREP", "JAXTINA"]:
            if kw in p_name_upper or kw in key_upper:
                is_foreign = True
                break
        if is_foreign:
            continue
            
        issues_raw = proj.get("issues", {})
        if isinstance(issues_raw, dict) and "issues" in issues_raw:
            issues = issues_raw["issues"]
        else:
            issues = proj.get("issues", [])
        pic_dict = info.get("pic") or {}
        pic_name = pic_dict.get("name", "")
        pic_norm = normalize_name(pic_name)
        matched_pic = norm_to_full.get(pic_norm)

        total_issues = 0
        completed_issues = 0
        overdue_count = 0
        active_count = 0
        hcm_involved = False
        
        issue_list = []
        for i in issues:
            state = i.get("state", "")
            state_lower = str(state).lower().strip()
            if state_lower in ["hủy", "huy", "cancel", "cancelled"]:
                continue
                
            assignee = i.get("assignee", "")
            assignee_norm = normalize_name(assignee)
            
            # Kiểm tra xem assignee có thuộc HCM không
            matched_assignee = None
            if "hoangxuannguyen" in assignee_norm or "xuanhoangnguyen" in assignee_norm:
                matched_assignee = "Lưu Hoàng Xuân Nguyên"
            else:
                matched_assignee = norm_to_full.get(assignee_norm)
                if not matched_assignee:
                    for target_norm, full_name in norm_to_full.items():
                        if target_norm in assignee_norm or assignee_norm in target_norm:
                            matched_assignee = full_name
                            break
            
            # Lọc: CHỈ lấy task nếu giao cho nhân sự HCM,
            # HOẶC nếu task chưa giao cho ai và dự án do nhân sự HCM làm PIC
            is_hcm_task = False
            if matched_assignee:
                is_hcm_task = True
            elif (not assignee or not assignee.strip()) and matched_pic:
                is_hcm_task = True
                
            if not is_hcm_task:
                continue # Loại bỏ hoàn toàn các task của Ngoại ngữ!
                
            hcm_involved = True
            total_issues += 1
            
            due = i.get("dueDate", "")
            due_short = due.split("T")[0] if due else ""
            is_done = state_lower in ["hoàn thành", "done", "completed"]
            is_pending_review = state_lower in ["chờ duyệt", "cho duyet", "pending review", "review"]
            is_overdue = bool(due_short and due_short <= today_str and not is_done and not is_pending_review)
            is_active = not is_done
            
            if matched_assignee:
                wload_total[matched_assignee] += 1
                if is_active:
                    wload_active[matched_assignee] += 1
                if is_overdue:
                    wload_overdue[matched_assignee] += 1
                    
            if is_done:
                completed_issues += 1
            elif is_overdue:
                overdue_count += 1
                
            p_team = "TG"
            if matched_assignee:
                p_team = PERSONNEL_CONFIG[matched_assignee]["team"]
            elif matched_pic:
                p_team = PERSONNEL_CONFIG[matched_pic]["team"]
                
            issue_list.append({
                "code": i.get("code", ""),
                "title": i.get("title", ""),
                "assignee": matched_assignee if matched_assignee else "Chưa giao",
                "state": state,
                "due": due_short,
                "overdue": is_overdue,
                "projectKey": key,
                "projectName": p_name,
                "team": p_team
            })
            
            if is_overdue and matched_assignee:
                overdue_all.append({
                    "code": i.get("code", ""),
                    "title": i.get("title", ""),
                    "assignee": matched_assignee,
                    "due": due_short,
                    "project": p_name
                })
        
        # Nếu dự án có người HCM tham gia hoặc PIC là người HCM
        if matched_pic:
            hcm_involved = True
            
        if hcm_involved:
            prog = round(completed_issues / total_issues * 100, 1) if total_issues > 0 else 0
            projects_list.append({
                "key": key,
                "name": p_name,
                "team": "GV_LEADER" if matched_pic and PERSONNEL_CONFIG[matched_pic]["team"] == "GV_LEADER" else "TG",
                "total": total_issues,
                "done": completed_issues,
                "inprog": total_issues - completed_issues,
                "overdue": overdue_count,
                "pct": prog,
                "issues": issue_list
            })

    # Tính toán thống kê theo tuần và tháng cho từng người
    pstats = {}
    for name, p_info in PERSONNEL_CONFIG.items():
        role = p_info["role"]
        team = p_info["team"]
        wtype = p_info["work_type"]
        tgt_hrs = p_info["target_hours"]
        
        ws = {}
        for wk, winfo in WEEKS.items():
            dd = winfo["dates"]
            # Chỉ tính thiếu báo cáo tính đến hôm qua (today_str)
            valid_dd = [d for d in dd if d <= today_str]
            
            rep = sum(1 for d in valid_dd if d in person_daily.get(name, {}))
            hrs = sum(person_daily.get(name, {}).get(d, {}).get("hours", 0) for d in valid_dd)
            kpi_hrs = sum(person_daily.get(name, {}).get(d, {}).get("kpi_hours", 0) for d in valid_dd)
            adhoc_hrs = sum(person_daily.get(name, {}).get(d, {}).get("adhoc_hours", 0) for d in valid_dd)
            tsk = sum(person_daily.get(name, {}).get(d, {}).get("tasks", 0) for d in valid_dd)
            dn = sum(person_daily.get(name, {}).get(d, {}).get("done", 0) for d in valid_dd)
            avg = round(hrs / rep, 1) if rep > 0 else 0
            
            target_met = avg >= tgt_hrs
            pct_target = round(avg / tgt_hrs * 100, 1) if tgt_hrs > 0 else 0
            
            ws[wk] = {
                "rep": rep,
                "tot": len(valid_dd),
                "hrs": round(hrs, 1),
                "kpi_hrs": round(kpi_hrs, 1),
                "adhoc_hrs": round(adhoc_hrs, 1),
                "avg": avg,
                "target_met": target_met,
                "pct_target": pct_target,
                "tsk": tsk,
                "dn": dn,
                "miss": [d for d in valid_dd if d not in person_daily.get(name, {})]
            }
            
        valid_all_dates = [d for d in ALL_DATES if d <= today_str]
        arep = sum(1 for d in valid_all_dates if d in person_daily.get(name, {}))
        ahrs = sum(person_daily.get(name, {}).get(d, {}).get("hours", 0) for d in valid_all_dates)
        akpi = sum(person_daily.get(name, {}).get(d, {}).get("kpi_hours", 0) for d in valid_all_dates)
        aadhoc = sum(person_daily.get(name, {}).get(d, {}).get("adhoc_hours", 0) for d in valid_all_dates)
        atsk = sum(person_daily.get(name, {}).get(d, {}).get("tasks", 0) for d in valid_all_dates)
        adn = sum(person_daily.get(name, {}).get(d, {}).get("done", 0) for d in valid_all_dates)
        aavg = round(ahrs / arep, 1) if arep > 0 else 0
        
        a_target_met = aavg >= tgt_hrs
        a_pct_target = round(aavg / tgt_hrs * 100, 1) if tgt_hrs > 0 else 0
        submission_rate = round(arep / len(valid_all_dates) * 100, 1) if len(valid_all_dates) > 0 else 0
        
        active_tasks = wload_active[name]
        overdue_tasks = wload_overdue[name]
        
        if a_pct_target > 120.0 or active_tasks > 6 or overdue_tasks >= 2:
            op_status = "OVERLOADED"
            op_status_label = "🔴 Quá tải"
            op_reason = f"Giờ làm {a_pct_target}% / {active_tasks} active tasks"
        elif a_pct_target >= 95.0 and submission_rate >= 80.0:
            op_status = "SUFFICIENT"
            op_status_label = "🟢 Đủ chỉ tiêu"
            op_reason = f"Đạt {a_pct_target}% chỉ tiêu ({tgt_hrs}h/ngày)"
        else:
            op_status = "UNDER"
            op_status_label = "🟡 Chưa đủ"
            op_reason = f"TB {aavg}h/{tgt_hrs}h ({a_pct_target}%) hoặc thiếu BC"
            
        pstats[name] = {
            "role": role,
            "team": team,
            "work_type": wtype,
            "target_hours": tgt_hrs,
            "weekly": ws,
            "monthly": {
                "rep": arep,
                "tot": len(valid_all_dates),
                "hrs": round(ahrs, 1),
                "kpi_hrs": round(akpi, 1),
                "adhoc_hrs": round(aadhoc, 1),
                "avg": aavg,
                "target_met": a_target_met,
                "pct_target": a_pct_target,
                "submission_rate": submission_rate,
                "tsk": atsk,
                "dn": adn,
                "active_tasks": active_tasks,
                "overdue_tasks": overdue_tasks,
                "op_status": op_status,
                "op_status_label": op_status_label,
                "op_reason": op_reason,
                "miss": [d for d in valid_all_dates if d not in person_daily.get(name, {})]
            }
        }

    person_daily_formatted = {}
    for name in PERSONNEL_CONFIG:
        person_daily_formatted[name] = {}
        for d in ALL_DATES:
            if d <= today_str:
                day_info = person_daily.get(name, {}).get(d, {})
                if day_info:
                    person_daily_formatted[name][d] = {
                        "hours": day_info["hours"],
                        "tasks": day_info["day_tasks"]
                    }
                else:
                    person_daily_formatted[name][d] = None

    # Tạo data_blob
    data_blob = {
        "personnel": pstats,
        "weeks": WEEKS,
        "weekOrder": [w[0] for w in WEEKS_CONFIG],
        "projects": projects_list,
        "overdue": overdue_all,
        "workload": dict(wload_active),
        "adhocTasks": adhoc_tasks,
        "totalDays": len(valid_all_dates),
        "reportDate": datetime.datetime.now().strftime("%d/%m/%Y"),
        "period": f"01/07/2026 - {datetime.datetime.strptime(today_str, '%Y-%m-%d').strftime('%d/%m/%Y')}",
        "personDaily": person_daily_formatted
    }

    # 5. Đọc template HTML
    if not os.path.exists(TEMPLATE_HTML_PATH):
        print(f"✗ Không tìm thấy file template tại {TEMPLATE_HTML_PATH}. Vui lòng kiểm tra lại đường dẫn.")
        return
        
    with open(TEMPLATE_HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Thay thế biến D
    data_json_str = json.dumps(data_blob, ensure_ascii=False)
    html_content = re.sub(
        r"let D\s*=\s*\{.*?\};\s*\n",
        f"let D = {data_json_str};\n",
        html_content,
        flags=re.DOTALL
    )
    
    # Sửa đổi các nhãn hiển thị trong HTML cho phù hợp với HCM (Vấn đề 1 & 3)
    html_content = html_content.replace(
        " BÁO CÁO TỔNG HỢP KHỐI NGOẠI NGỮ (TIẾNG NHẬT & TIẾNG ANH)",
        " BÁO CÁO TỔNG HỢP NHÂN SỰ HCM (KHỐI CNTT)"
    )
    html_content = html_content.replace(
        "Báo cáo Tổng hợp Khối Ngoại Ngữ",
        "Báo cáo Tổng hợp Nhân sự HCM"
    )
    html_content = html_content.replace(
        "Khối Ngoại Ngữ (DT-NN)",
        "Khối CNTT - Cơ sở Hồ Chí Minh (CNTT-HCM)"
    )
    
    # Sửa nhãn ở Header sử dụng regex để an toàn
    html_content = re.sub(
        r"🇯🇵\s*Tiếng Nhật\s*(&amp;|&)\s*🇬🇧\s*Tiếng Anh",
        "👨‍🏫 Giảng viên &amp; Leader &amp; 💻 Trợ giảng",
        html_content
    )
    html_content = re.sub(
        r"5\s*Nhân sự\s*\(4\s*Full-time,\s*1\s*Thực tập sinh\)",
        "9 Nhân sự (3 Giảng viên &amp; Leader, 6 Trợ giảng)",
        html_content
    )
    
    # Sửa Pills & CSS selectors cho team
    html_content = html_content.replace('data-team="JPN"', 'data-team="GV_LEADER"')
    html_content = html_content.replace('data-team="ENG"', 'data-team="TG"')
    html_content = html_content.replace("selectTeam('JPN')", "selectTeam('GV_LEADER')")
    html_content = html_content.replace("selectTeam('ENG')", "selectTeam('TG')")
    html_content = html_content.replace("🌐 Tất cả Khối NN", "🌐 Tất cả nhân sự HCM")
    html_content = html_content.replace("🇯🇵 Bộ môn Tiếng Nhật", "👨‍🏫 Giảng viên &amp; Leader")
    html_content = html_content.replace("🇬🇧 Bộ môn Tiếng Anh", "💻 Trợ giảng")
    
    # Sửa Legend SVG Chart
    html_content = html_content.replace(
        '<div class="svg-legend-item"><div class="svg-legend-color" style="background:var(--jpn-accent)"></div> 🇯🇵 Bộ môn Tiếng Nhật</div>',
        '<div class="svg-legend-item"><div class="svg-legend-color" style="background:var(--jpn-accent)"></div> 👨‍🏫 Giảng viên &amp; Leader</div>'
    )
    html_content = html_content.replace(
        '<div class="svg-legend-item"><div class="svg-legend-color" style="background:var(--eng-accent)"></div> 🇬🇧 Bộ môn Tiếng Anh</div>',
        '<div class="svg-legend-item"><div class="svg-legend-color" style="background:var(--eng-accent)"></div> 💻 Trợ giảng</div>'
    )
    html_content = html_content.replace(
        '<div class="svg-legend-item"><div class="svg-legend-color" style="background:var(--primary)"></div> 🌐 Toàn Khối NN</div>',
        '<div class="svg-legend-item"><div class="svg-legend-color" style="background:var(--primary)"></div> 🌐 Toàn bộ HCM</div>'
    )

    # Sửa Projects tab titles
    html_content = html_content.replace(
        "🇯🇵 Dự án Bộ môn Tiếng Nhật",
        "👨‍🏫 Dự án Giảng viên &amp; Leader"
    )
    html_content = html_content.replace(
        "🇬🇧 Dự án Bộ môn Tiếng Anh",
        "💻 Dự án Trợ giảng"
    )
    html_content = html_content.replace(
        "Dự án ngoại ngữ đang chạy",
        "Dự án CNTT đang chạy"
    )
    
    # 6. SỬA CÁC ĐOẠN JAVASCRIPT ĐỂ PHÙ HỢP VỚI HCM VÀ KHẮC PHỤC LỖI KHÔNG HIỂN THỊ DỮ LIỆU (Vấn đề 3)
    
    # Sửa currentTeamFilter
    html_content = re.sub(
        r"let currentTeamFilter\s*=\s*['\"]ALL['\"]\s*;\s*//.*?\n",
        "let currentTeamFilter = 'ALL'; // 'ALL', 'GV_LEADER', 'TG'\n",
        html_content
    )
    
    # Thay thế todayStr và today trong client-side JS bằng giá trị today_str của Python (Vấn đề 2)
    html_content = html_content.replace(
        "const today = new Date().toISOString().split('T')[0];",
        f"const today = '{today_str}';"
    )
    html_content = html_content.replace(
        "const todayStr = new Date().toISOString().split('T')[0];",
        f"const todayStr = '{today_str}';"
    )
    
    # Sửa NN_KEYS trong JS thành danh sách các dự án thực tế của HCM
    hcm_project_keys = [p["key"] for p in projects_list]
    html_content = re.sub(
        r"const NN_KEYS\s*=\s*\[.*?\];",
        f"const NN_KEYS = {json.dumps(hcm_project_keys, ensure_ascii=False)};",
        html_content
    )
    
    # Sửa KPI_KEYWORDS trong JS thành bộ từ khóa của CNTT
    html_content = re.sub(
        r"const KPI_KEYWORDS\s*=\s*\[.*?\];",
        f"const KPI_KEYWORDS = {json.dumps(KPI_KEYWORDS, ensure_ascii=False)};",
        html_content
    )
    
    # Sửa logic gán pTeam dựa trên prefix NN cũ sang Heuristics dựa trên PIC của dự án
    html_content = re.sub(
        r'if\s*\(key\.includes\("JPN"\).*?pTeam\s*=\s*"ENG"\s*;',
        'let foundProj = D.projects.find(p => p.key === key); pTeam = foundProj ? foundProj.team : "TG";',
        html_content,
        flags=re.DOTALL
    )
    html_content = html_content.replace(
        'if (key.includes("JPN") || key.includes("PTITXAY") || key.includes("PTITQUAN") || key.includes("PTITSAN3")) pTeam = "JPN";\n            else if (key.includes("RE") || key.includes("ENG") || key.includes("REXP") || key.includes("REKHAO")) pTeam = "ENG";',
        'let foundProj = D.projects.find(p => p.key === key);\n            pTeam = foundProj ? foundProj.team : "TG";'
    )
    
    # Sửa logic lọc overdue trong renderProjects() để lọc theo assignee của HCM
    html_content = re.sub(
        r"if\s*\(currentTeamFilter\s*===\s*['\"]JPN['\"]\s*&&\s*!o\.project\.includes\(['\"]PTIT['\"]\)\)\s*return\s*;\s*\n\s*if\s*\(currentTeamFilter\s*===\s*['\"]ENG['\"]\s*&&\s*!o\.project\.includes\(['\"]ENGLISH['\"]\)\s*&&\s*!o\.project\.includes\(['\"]RE['\"]\)\)\s*return\s*;",
        "let assigneeInfo = D.personnel[o.assignee]; if (currentTeamFilter !== 'ALL' && (!assigneeInfo || assigneeInfo.team !== currentTeamFilter)) return;",
        html_content
    )
    
    # Sửa stateBadge để hiển thị "Chờ duyệt" có badge ⏳ Chờ duyệt màu primary
    html_content = html_content.replace(
        "if (state === 'Hoàn thành' || state === 'Done' || state === 'Completed') return '<span class=\"badge badge-success\">✅ Hoàn thành</span>';",
        "if (state === 'Hoàn thành' || state === 'Done' || state === 'Completed') return '<span class=\"badge badge-success\">✅ Hoàn thành</span>';\n        if (state === 'Chờ duyệt' || state === 'Pending Review' || state === 'Review') return '<span class=\"badge badge-primary\">⏳ Chờ duyệt</span>';"
    )
    
    # Thay thế filter theo team JPN/ENG cũ sang GV_LEADER/TG mới trong JS (Sử dụng regex để an toàn)
    html_content = re.sub(r"team\s*===\s*['\"]JPN['\"]", "team === 'GV_LEADER'", html_content)
    html_content = re.sub(r"team\s*===\s*['\"]ENG['\"]", "team === 'TG'", html_content)
    html_content = re.sub(r"team\s*===\s*\\'JPN\\'", "team === \\'GV_LEADER\\'", html_content)
    html_content = re.sub(r"team\s*===\s*\\'ENG\\'", "team === \\'TG\\'", html_content)
    html_content = re.sub(r"p\.team\s*===\s*['\"]JPN['\"]", "p.team === 'GV_LEADER'", html_content)
    html_content = re.sub(r"p\.team\s*===\s*['\"]ENG['\"]", "p.team === 'TG'", html_content)
    
    # Sửa badges hiển thị trên Client-side JS
    html_content = html_content.replace(
        "if (team === 'JPN') return '<span class=\"badge badge-jpn\">🇯🇵 Tiếng Nhật</span>';",
        "if (team === 'GV_LEADER') return '<span class=\"badge badge-jpn\">👨‍🏫 GV &amp; Leader</span>';"
    )
    html_content = html_content.replace(
        "if (team === 'ENG') return '<span class=\"badge badge-eng\">🇬🇧 Tiếng Anh</span>';",
        "if (team === 'TG') return '<span class=\"badge badge-eng\">💻 Trợ giảng</span>';"
    )
    
    # Thay thế triệt để các nhãn cứng "Tiếng Nhật" và "Tiếng Anh" còn sót trong badges
    html_content = html_content.replace("🇯🇵 Tiếng Nhật", "👨‍🏫 GV &amp; Leader")
    html_content = html_content.replace("🇬🇧 Tiếng Anh", "💻 Trợ giảng")
    html_content = html_content.replace("Bộ môn Tiếng Nhật", "Giảng viên &amp; Leader")
    html_content = html_content.replace("Bộ môn Tiếng Anh", "Trợ giảng")
    html_content = html_content.replace("Khối Ngoại Ngữ", "Khối CNTT HCM")
    html_content = html_content.replace("Toàn Khối Ngoại Ngữ", "Toàn Khối CNTT HCM")
    
    # Sửa team check cho trend chart (Sử dụng regex)
    html_content = re.sub(r"currentTeamFilter\s*===\s*['\"]JPN['\"]", "currentTeamFilter === 'GV_LEADER'", html_content)
    html_content = re.sub(r"currentTeamFilter\s*===\s*['\"]ENG['\"]", "currentTeamFilter === 'TG'", html_content)
    
    # Sửa các nhãn trend chart
    html_content = html_content.replace("title>JPN ", "title>GV_LEADER ")
    html_content = html_content.replace("title>ENG ", "title>TG ")
    html_content = html_content.replace("fill:var(--jpn-accent)\" text-anchor=\"middle\">JP", "fill:var(--jpn-accent)\" text-anchor=\"middle\">GV")
    html_content = html_content.replace("fill:var(--eng-accent)\" text-anchor=\"middle\">EN", "fill:var(--eng-accent)\" text-anchor=\"middle\">TG")
    
    # Sửa Profile Tab General Info
    html_content = html_content.replace(
        "p.team === 'JPN' ? '🇯🇵 Tiếng Nhật' : '🇬🇧 Tiếng Anh'",
        "p.team === 'GV_LEADER' ? '👨‍🏫 GV &amp; Leader' : '💻 Trợ giảng'"
    )
    
    # Sửa toast notification
    html_content = html_content.replace(
        "Đã lấy thành công dữ liệu mới nhất từ Worklane!",
        "Đã tổng hợp thành công dữ liệu mới nhất cho nhân sự HCM!"
    )
    
    # Tạo thư mục đầu ra nếu chưa có
    os.makedirs(os.path.dirname(OUTPUT_HTML_PATH), exist_ok=True)
    
    with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"✓ Báo cáo HTML được sinh thành công tại {OUTPUT_HTML_PATH}")

if __name__ == "__main__":
    main()

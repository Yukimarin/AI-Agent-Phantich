# -*- coding: utf-8 -*-
import json
import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

project_issues_path = "data/processed/project_issues_worklane.json"
daily_log_analysis_path = "data/processed/daily_log_analysis.json"
output_html_path = "output/dashboards/core/agent_4_daily_logs.html"
output_md_path = "output/reports/core/agent_4_daily_logs.md"

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
    dates_weekly = daily_data.get('dates_weekly', [])
    
    today_date = dates_weekly[-1] if dates_weekly else ""

    payload = {
        "departments": [],
        "today_date": today_date,
        "personnel": {},
        "projects": [],
        "heatmap": {}
    }

    group_map = {}
    for group, members in raw_reports.items():
        if group not in payload["departments"]:
            payload["departments"].append(group)
            payload["heatmap"][group] = {"2": 0, "3": 0, "4": 0, "5": 0, "6": 0}
        for m in members.keys():
            group_map[m] = group

    for m_norm, stats in weekly_stats.items():
        name = m_norm
        group = "Unknown"
        for m_raw, g_raw in group_map.items():
            if m_raw.lower().replace(" ", "") == m_norm.lower().replace(" ", "") or m_raw.strip() == m_norm.strip():
                name = m_raw
                group = g_raw
                break
        
        if group not in payload["heatmap"]:
            payload["heatmap"][group] = {"2": 0, "3": 0, "4": 0, "5": 0, "6": 0}
            payload["departments"].append(group)

        miss_days = []
        if name in raw_reports.get(group, {}):
            reports_for_m = raw_reports[group][name].get("reports", {})
            for d in dates_weekly:
                if not reports_for_m.get(d):
                    miss_days.append(d)
                    try:
                        weekday = datetime.strptime(d, "%Y-%m-%d").weekday() + 2
                        if 2 <= weekday <= 6:
                            payload["heatmap"][group][str(weekday)] += 1
                    except:
                        pass
                            
        payload["personnel"][name] = {
            "group": group,
            "reported_days": stats.get('reported_days', 0),
            "expected_days": len(dates_weekly),
            "hours": stats.get('declared_hours', 0),
            "completion_rate": stats.get('completion_rate', 0),
            "warning_flags": stats.get('warning_flags', []),
            "miss_days": miss_days,
            "assigned_projects": []
        }

    if 'projects' in project_data:
        projects = project_data['projects']
        if isinstance(projects, dict):
            projects = [{"key": k, **v} for k, v in projects.items()]
    else:
        projects = [{"key": k, **v} for k, v in project_data.items()]
    
    for p in projects:
        info = p.get('project_info', {})
        status = info.get('status', 'ACTIVE')
        
        # 1. Bỏ qua các dự án ở trạng thái Hủy
        if status.upper() in ['CANCEL', 'CANCELLED', 'HỦY', 'HUY']:
            continue
            
        issues_data = p.get('issues', {}).get('issues', [])
        pic_dict = info.get('pic') or {}
        pic_name = pic_dict.get('name', 'Unknown')
        p_name = info.get('name', 'Unknown')
        
        # 2. Lọc bỏ các task (issues) ở trạng thái Hủy
        filtered_issues = []
        has_overdue = False
        
        for iss in issues_data:
            iss_state = str(iss.get('state', '')).lower().strip()
            if iss_state in ['hủy', 'huy', 'cancel', 'cancelled']:
                continue
                
            filtered_issues.append(iss)
            
            # Kiểm tra trễ hạn (Overdue)
            iss_done = iss_state in ['hoàn thành', 'done', 'completed']
            iss_due = iss.get('dueDate')
            
            if not iss_done and iss_due:
                iss_due_date = iss_due[:10]
                if today_date and iss_due_date <= today_date:
                    has_overdue = True
                    
        # 3. Tính toán lại health của dự án
        health = info.get('health', 'UNKNOWN')
        if status.upper() != 'COMPLETED' and has_overdue:
            health = 'OFF_TRACK'
            
        payload["projects"].append({
            "name": p_name,
            "pic": pic_name,
            "health": health,
            "status": status
        })
        
        involved_people = {pic_name.lower().strip()}
        for iss in filtered_issues:
            assignee = iss.get('assignee')
            if assignee:
                involved_people.add(assignee.lower().strip())
                
        for n, p_data in payload["personnel"].items():
            n_lower = n.lower().strip()
            is_involved = False
            for inv in involved_people:
                if inv and (n_lower in inv or inv in n_lower):
                    is_involved = True
                    break
            
            if is_involved:
                p_data["assigned_projects"].append({
                    "name": p_name,
                    "pic": pic_name,
                    "health": health,
                    "status": status
                })

    payload_json = json.dumps(payload, ensure_ascii=False)
    
    # Export payload to JSON file for refresh feature
    payload_json_path = "data/processed/agent4_payload.json"
    os.makedirs(os.path.dirname(payload_json_path), exist_ok=True)
    with open(payload_json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PMO Executive Dashboard V4.1</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-main: #0f172a; --bg-card: #1e293b; --bg-elevated: #334155;
            --text-main: #f8fafc; --text-muted: #94a3b8;
            --primary: #3b82f6; --success: #10b981; --warning: #f59e0b; --danger: #ef4444; --info: #0ea5e9;
            --border: rgba(255,255,255,0.08);
            --font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: var(--font-family); }}
        body {{ background: var(--bg-main); color: var(--text-main); padding: 20px; font-size: 14px; }}
        .container {{ max-width: 1440px; margin: 0 auto; }}
        
        header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 24px; }}
        h1 {{ font-size: 1.5rem; font-weight: 700; display: flex; align-items: center; gap: 10px; }}
        .meta {{ color: var(--text-muted); font-size: 0.9rem; }}
        select {{ background: var(--bg-card); color: var(--text-main); border: 1px solid var(--border); padding: 8px 16px; border-radius: 8px; font-weight: 600; outline: none; }}
        
        .tabs {{ display: flex; gap: 8px; margin-bottom: 24px; background: var(--bg-card); padding: 6px; border-radius: 12px; border: 1px solid var(--border); width: max-content; }}
        .tab-btn {{ padding: 10px 24px; background: transparent; border: none; color: var(--text-muted); font-weight: 600; font-size: 0.95rem; cursor: pointer; border-radius: 8px; transition: 0.2s; display: flex; align-items: center; gap: 8px; }}
        .tab-btn:hover:not(.active) {{ background: var(--border); color: var(--text-main); }}
        .tab-btn.active {{ background: var(--primary); color: white; }}
        .tab-pane {{ display: none; animation: fade 0.3s ease; }}
        .tab-pane.active {{ display: block; }}
        @keyframes fade {{ from {{ opacity: 0; transform: translateY(5px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px; }}
        .kpi-card {{ background: var(--bg-card); border-radius: 12px; padding: 20px; border: 1px solid var(--border); position: relative; overflow: hidden; }}
        .kpi-card::before {{ content: ""; position: absolute; top: 0; left: 0; width: 4px; height: 100%; }}
        .kpi-card.success::before {{ background: var(--success); }}
        .kpi-card.danger::before {{ background: var(--danger); }}
        .kpi-card.warning::before {{ background: var(--warning); }}
        .kpi-card.primary::before {{ background: var(--primary); }}
        .kpi-title {{ font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 8px; }}
        .kpi-val {{ font-size: 2.2rem; font-weight: 800; display: flex; align-items: baseline; gap: 8px; }}
        .kpi-sub {{ font-size: 0.9rem; font-weight: 500; color: var(--text-muted); }}

        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
        .panel {{ background: var(--bg-card); border-radius: 12px; padding: 20px; border: 1px solid var(--border); }}
        .panel-title {{ font-size: 1.05rem; font-weight: 700; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }}
        
        .heatmap-container {{ display: flex; flex-direction: column; gap: 8px; }}
        .hm-row {{ display: grid; grid-template-columns: 100px repeat(5, 1fr); gap: 4px; align-items: center; }}
        .hm-label {{ font-size: 0.8rem; color: var(--text-muted); font-weight: 600; text-align: right; padding-right: 10px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .hm-cell {{ height: 35px; border-radius: 4px; background: var(--bg-elevated); display: flex; justify-content: center; align-items: center; font-size: 0.75rem; font-weight: 700; color: rgba(255,255,255,0.9); transition: 0.2s; cursor: default; }}
        .hm-cell:hover {{ transform: scale(1.05); }}
        
        .table-wrap {{ overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.85rem; }}
        th {{ color: var(--text-muted); font-weight: 600; text-transform: uppercase; font-size: 0.75rem; background: rgba(0,0,0,0.2); }}
        tr:hover {{ background: rgba(255,255,255,0.02); }}
        
        .badge {{ padding: 4px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 700; display: inline-block; }}
        .bg-success {{ background: rgba(16,185,129,0.2); color: var(--success); border: 1px solid var(--success); }}
        .bg-danger {{ background: rgba(239,68,68,0.2); color: var(--danger); border: 1px solid var(--danger); }}
        .bg-warning {{ background: rgba(245,158,11,0.2); color: var(--warning); border: 1px solid var(--warning); }}
        .bg-info {{ background: rgba(14,165,233,0.2); color: var(--info); border: 1px solid var(--info); }}
        
        .chip {{ display: inline-flex; align-items: center; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; margin: 2px; border: 1px solid var(--border); }}
        .chip-success {{ background: rgba(16,185,129,0.1); color: var(--success); border-color: var(--success); }}
        .chip-primary {{ background: rgba(59,130,246,0.1); color: #60a5fa; border-color: var(--primary); }}
        .chip-danger {{ background: rgba(239,68,68,0.1); color: var(--danger); border-color: var(--danger); }}
        
        .gauge-container {{ position: relative; width: 100%; height: 200px; display: flex; justify-content: center; align-items: flex-end; }}
        .gauge-text {{ position: absolute; bottom: 10px; text-align: center; }}
        .gauge-val {{ font-size: 2.5rem; font-weight: 800; color: var(--success); line-height: 1; }}
        
        .list-item {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px dashed var(--border); }}
        .list-item:last-child {{ border-bottom: none; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1><i class="fas fa-rocket" style="color: var(--primary)"></i> PMO Executive Dashboard V4.1</h1>
                <div class="meta" id="date-meta">Cập nhật dữ liệu tuần nhất...</div>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <button id="btn-refresh-data" style="background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid var(--primary); padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 13px;" onclick="fetchLiveDailyLogsData(true)" title="Cập nhật dữ liệu từ file JSON mới nhất">
                    <i class="fa-solid fa-rotate" id="refresh-icon"></i> Cập nhật dữ liệu
                </button>
                <select id="dept-filter" onchange="renderApp()">
                    <option value="ALL">Tất Cả Các Khối</option>
                </select>
            </div>
        </header>

        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('daily')"><i class="fas fa-calendar-check"></i> Kỷ Luật Báo Cáo Hằng Ngày</button>
            <button class="tab-btn" onclick="switchTab('project')"><i class="fas fa-tasks"></i> Quản Trị Nguồn Lực & Dự Án</button>
        </div>

        <div id="tab-daily" class="tab-pane active">
            <div class="kpi-grid" id="daily-kpis"></div>

            <div class="grid-2">
                <div class="panel">
                    <div class="panel-title"><i class="fas fa-tachometer-alt"></i> Mức Độ Tuân Thủ (Gauge)</div>
                    <div class="gauge-container">
                        <canvas id="gaugeChart"></canvas>
                        <div class="gauge-text">
                            <div class="gauge-val" id="gauge-val-text">0%</div>
                            <div style="font-size: 0.85rem; color: var(--text-muted)" id="gauge-sub-text"></div>
                        </div>
                    </div>
                </div>

                <div class="panel">
                    <div class="panel-title"><i class="fas fa-fire"></i> Tần Suất Quên Báo Cáo (Heatmap)</div>
                    <div class="heatmap-container" id="heatmap-content"></div>
                </div>
            </div>

            <div class="grid-2">
                <div class="panel" style="border-top: 4px solid var(--danger)">
                    <div class="panel-title" style="color: var(--danger)"><i class="fas fa-thumbs-down"></i> Top Quên / Nộp Trễ (Cần Nhắc Nhở)</div>
                    <div id="slacker-list"></div>
                </div>

                <div class="panel" style="border-top: 4px solid var(--success)">
                    <div class="panel-title" style="color: var(--success)"><i class="fas fa-star"></i> Top Tuân Thủ 100% (Tuyên Dương)</div>
                    <div id="hero-list"></div>
                </div>
            </div>
        </div>

        <div id="tab-project" class="tab-pane">
            <div class="kpi-grid" id="project-kpis"></div>

            <div class="panel" style="margin-bottom: 24px;">
                <div class="panel-title"><i class="fas fa-th"></i> Ma Trận Phân Bổ (Workload Matrix)</div>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 15px">
                    <span style="display:inline-block; margin-right:15px"><span class="chip chip-success" style="padding:2px 8px">Hoàn thành</span></span>
                    <span style="display:inline-block; margin-right:15px"><span class="chip chip-primary" style="padding:2px 8px">Đang làm đúng hạn</span></span>
                    <span style="display:inline-block; margin-right:15px"><span class="chip chip-danger" style="padding:2px 8px">Đang làm bị trễ</span></span>
                </p>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 250px">Nhân Sự</th>
                                <th style="width: 120px; text-align: center">Số lượng DA</th>
                                <th>Danh Sách Dự Án Đang Được Giao</th>
                            </tr>
                        </thead>
                        <tbody id="workload-table"></tbody>
                    </table>
                </div>
            </div>

            <div class="panel" style="margin-bottom: 24px; border-top: 4px solid var(--danger)">
                <div class="panel-title" style="color: var(--danger)"><i class="fas fa-skull-crossbones"></i> Blacklist: Khai khống tiến độ (Chưa Xác Thực)</div>
                <div id="blacklist-content"></div>
            </div>

            <div class="panel">
                <div class="panel-title"><i class="fas fa-medal"></i> Bảng Xếp Hạng & Cảnh Báo Hiệu Suất (Performance Alert)</div>
                <div class="grid-2">
                    <div>
                        <h3 style="color: var(--success); font-size: 1rem; margin-bottom: 12px">🌟 Nhóm Xuất Sắc (High Performance)</h3>
                        <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 15px">Hoàn thành báo cáo đầy đủ, tiến độ DA tốt.</p>
                        <div id="perf-high"></div>
                    </div>
                    <div style="border-left: 1px solid var(--border); padding-left: 20px;">
                        <h3 style="color: var(--danger); font-size: 1rem; margin-bottom: 12px">⚠️ Nhóm Cảnh Báo (Low Performance / Idle)</h3>
                        <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 15px">Không được giao dự án, hoặc báo cáo công việc cẩu thả.</p>
                        <div id="perf-low"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const RAW_DATA = {payload_json};
        let gaugeChartInstance = null;

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }}

        function initApp() {{
            document.getElementById('date-meta').innerText = `Hôm nay: ${{RAW_DATA.today_date}}`;
            const filter = document.getElementById('dept-filter');
            RAW_DATA.departments.forEach(d => {{
                const opt = document.createElement('option');
                opt.value = d;
                opt.innerText = d;
                filter.appendChild(opt);
            }});
            renderApp();
        }}

        function renderApp() {{
            const selectedDept = document.getElementById('dept-filter').value;
            
            let personnel = Object.entries(RAW_DATA.personnel).map(([k,v]) => ({{name: k, ...v}}));
            if (selectedDept !== 'ALL') {{
                personnel = personnel.filter(p => p.group === selectedDept);
            }}

            let totalReported = 0;
            let totalExpected = 0;
            let forgottenToday = 0;
            let totalStaff = personnel.length;

            personnel.forEach(p => {{
                totalReported += p.reported_days;
                totalExpected += p.expected_days;
                if (p.miss_days.includes(RAW_DATA.today_date)) {{
                    forgottenToday++;
                }}
            }});

            const complianceRate = totalExpected ? ((totalReported/totalExpected)*100).toFixed(1) : 0;

            document.getElementById('daily-kpis').innerHTML = `
                <div class="kpi-card ${{complianceRate >= 90 ? 'success' : complianceRate >= 70 ? 'warning' : 'danger'}}">
                    <div class="kpi-title">Tỷ Lệ Nộp Đúng Hạn</div>
                    <div class="kpi-val" style="color: var(--${{complianceRate >= 90 ? 'success' : complianceRate >= 70 ? 'warning' : 'danger'}})">${{complianceRate}}%</div>
                </div>
                <div class="kpi-card ${{forgottenToday > 0 ? 'danger' : 'success'}}">
                    <div class="kpi-title">Quên Báo Cáo Hôm Nay</div>
                    <div class="kpi-val" style="color: var(--${{forgottenToday > 0 ? 'danger' : 'success'}})">${{forgottenToday}} <span class="kpi-sub">Nhân sự</span></div>
                </div>
                <div class="kpi-card primary">
                    <div class="kpi-title">Tổng Nhân Sự Quản Lý</div>
                    <div class="kpi-val" style="color: var(--text-main)">${{totalStaff}} <span class="kpi-sub">Người</span></div>
                </div>
            `;

            const ctx = document.getElementById('gaugeChart').getContext('2d');
            if (gaugeChartInstance) gaugeChartInstance.destroy();
            const color = complianceRate >= 90 ? '#10b981' : complianceRate >= 70 ? '#f59e0b' : '#ef4444';
            gaugeChartInstance = new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: ['Tuân Thủ', 'Chưa Tuân Thủ'],
                    datasets: [{{
                        data: [complianceRate, 100 - complianceRate],
                        backgroundColor: [color, 'rgba(255,255,255,0.05)'],
                        borderWidth: 0,
                        cutout: '80%',
                        circumference: 180,
                        rotation: 270
                    }}]
                }},
                options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }}, tooltip: {{ enabled: false }} }} }}
            }});
            document.getElementById('gauge-val-text').innerText = `${{complianceRate}}%`;
            document.getElementById('gauge-val-text').style.color = color;
            document.getElementById('gauge-sub-text').innerText = complianceRate >= 90 ? 'Tuyệt vời' : complianceRate >= 70 ? 'Cần cải thiện' : 'Báo động đỏ';

            let hmHtml = `
                <div class="hm-row">
                    <div class="hm-label"></div>
                    <div class="hm-label" style="text-align: center">Thứ 2</div>
                    <div class="hm-label" style="text-align: center">Thứ 3</div>
                    <div class="hm-label" style="text-align: center">Thứ 4</div>
                    <div class="hm-label" style="text-align: center">Thứ 5</div>
                    <div class="hm-label" style="text-align: center">Thứ 6</div>
                </div>
            `;
            
            const deptsToRender = selectedDept === 'ALL' ? RAW_DATA.departments : [selectedDept];
            let maxMiss = 1;
            deptsToRender.forEach(d => {{
                Object.values(RAW_DATA.heatmap[d]).forEach(v => {{ if(v > maxMiss) maxMiss = v; }});
            }});
            
            deptsToRender.forEach(d => {{
                hmHtml += `<div class="hm-row"><div class="hm-label">${{d}}</div>`;
                ['2', '3', '4', '5', '6'].forEach(day => {{
                    const val = RAW_DATA.heatmap[d][day] || 0;
                    const opacity = val === 0 ? 0 : (0.2 + (val / maxMiss) * 0.8);
                    hmHtml += `<div class="hm-cell" style="background: rgba(239,68,68,${{opacity}})">${{val}}</div>`;
                }});
                hmHtml += `</div>`;
            }});
            document.getElementById('heatmap-content').innerHTML = hmHtml;

            let slackers = personnel.filter(p => p.miss_days.length > 0).sort((a,b) => b.miss_days.length - a.miss_days.length).slice(0, 5);
            let heroes = personnel.filter(p => p.miss_days.length === 0 && p.completion_rate >= 90).sort((a,b) => b.hours - a.hours).slice(0, 5);
            
            document.getElementById('slacker-list').innerHTML = slackers.length ? slackers.map(s => `
                <div class="list-item">
                    <div><strong>${{s.name}}</strong> <br><small>${{s.group}}</small></div>
                    <div style="text-align: right"><div class="badge bg-danger">Quên ${{s.miss_days.length}} ngày</div></div>
                </div>
            `).join('') : '<div style="padding:10px; color:var(--success)">Không có nhân sự nào quên báo cáo!</div>';

            document.getElementById('hero-list').innerHTML = heroes.length ? heroes.map(h => `
                <div class="list-item">
                    <div><strong>${{h.name}}</strong> <br><small>${{h.group}}</small></div>
                    <div style="text-align: right"><div class="badge bg-success">100% Đúng Hạn</div><div style="font-size:0.75rem; color:var(--text-muted)">${{h.hours}}h làm việc</div></div>
                </div>
            `).join('') : '<div style="padding:10px; color:var(--text-muted)">Chưa có dữ liệu xuất sắc</div>';

            // PROJECT TAB
            let idleStaff = personnel.filter(p => p.assigned_projects.length === 0);
            
            let availableStaff = personnel.filter(p => {{
                if (p.assigned_projects.length === 0) return false;
                let activeCount = p.assigned_projects.filter(proj => proj.status !== 'COMPLETED').length;
                let doneCount = p.assigned_projects.filter(proj => proj.status === 'COMPLETED').length;
                return activeCount === 0 && doneCount > 0;
            }});

            let lowPerfStaff = personnel.filter(p => (p.expected_days > 0 && p.reported_days/p.expected_days < 0.5) || p.completion_rate < 50);

            document.getElementById('project-kpis').innerHTML = `
                <div class="kpi-card success">
                    <div class="kpi-title">Tổng Dự Án Toàn Công Ty</div>
                    <div class="kpi-val" style="color: var(--text-main)">${{RAW_DATA.projects.length}}</div>
                </div>
                <div class="kpi-card info">
                    <div class="kpi-title">Sẵn Sàng Nhận Việc (Available)</div>
                    <div class="kpi-val" style="color: var(--info)">${{availableStaff.length}} <span class="kpi-sub">Vừa hoàn thành dự án</span></div>
                </div>
                <div class="kpi-card danger">
                    <div class="kpi-title">Trống Việc / Hiệu Suất Kém</div>
                    <div class="kpi-val" style="color: var(--danger)">${{idleStaff.length + lowPerfStaff.length}}</div>
                </div>
            `;

            personnel.sort((a,b) => b.assigned_projects.length - a.assigned_projects.length);
            document.getElementById('workload-table').innerHTML = personnel.map(p => {{
                let activeCount = p.assigned_projects.filter(proj => proj.status !== 'COMPLETED').length;
                let doneCount = p.assigned_projects.filter(proj => proj.status === 'COMPLETED').length;
                let delayedCount = p.assigned_projects.filter(proj => proj.status !== 'COMPLETED' && (proj.health === 'OFF_TRACK' || proj.health === 'AT_RISK')).length;
                let onTrackCount = activeCount - delayedCount;
                
                let isIdle = p.assigned_projects.length === 0;
                let isAvailable = !isIdle && activeCount === 0;

                let rowBg = isIdle ? 'background: rgba(239,68,68,0.1)' : isAvailable ? 'background: rgba(14,165,233,0.05)' : '';

                let total = p.assigned_projects.length;
                let progBar = '';
                if (total > 0) {{
                    let wDone = (doneCount/total)*100;
                    let wTrack = (onTrackCount/total)*100;
                    let wDelay = (delayedCount/total)*100;
                    progBar = `
                    <div style="display:flex; height: 6px; width: 100%; border-radius: 4px; overflow: hidden; margin-top: 5px; background: var(--bg-elevated);" title="${{doneCount}} Xong | ${{onTrackCount}} Đang làm | ${{delayedCount}} Trễ">
                        ${{wDone > 0 ? `<div style="width: ${{wDone}}%; background: var(--success)"></div>` : ''}}
                        ${{wTrack > 0 ? `<div style="width: ${{wTrack}}%; background: var(--primary)"></div>` : ''}}
                        ${{wDelay > 0 ? `<div style="width: ${{wDelay}}%; background: var(--danger)"></div>` : ''}}
                    </div>`;
                }}

                let projectChips = p.assigned_projects.map(proj => {{
                    let colorClass = 'chip-primary'; 
                    if (proj.status === 'COMPLETED') colorClass = 'chip-success';
                    else if (proj.health === 'OFF_TRACK' || proj.health === 'AT_RISK') colorClass = 'chip-danger';

                    let picParts = proj.pic.split(' ');
                    let shortPic = picParts[picParts.length - 1]; 
                    
                    return `<span class="chip ${{colorClass}}" title="${{proj.name}}">${{proj.name}} <strong style="opacity:0.8; margin-left:4px">(👤 ${{shortPic}})</strong></span>`;
                }}).join('');

                if (isIdle) {{
                    projectChips = '<span style="color: var(--danger); font-weight: 700; font-size: 0.8rem"><i class="fas fa-exclamation-triangle"></i> IDLE: Trống việc dài hạn (Ngồi chơi)</span>';
                }} else if (isAvailable) {{
                    projectChips += '<br><span style="color: var(--info); font-weight: 700; font-size: 0.8rem; display:block; margin-top:8px"><i class="fas fa-check-circle"></i> AVAILABLE: Vừa hoàn thành toàn bộ DA, chờ việc mới</span>';
                }}

                return `
                <tr style="${{rowBg}}">
                    <td><strong>${{p.name}}</strong><br><small style="color:var(--text-muted)">${{p.group}}</small></td>
                    <td style="text-align: center; vertical-align: top;">
                        <span class="badge bg-${{isIdle ? 'danger' : isAvailable ? 'info' : activeCount > 3 ? 'warning' : 'success'}}">${{p.assigned_projects.length}} DA</span>
                        ${{progBar}}
                    </td>
                    <td>
                        ${{projectChips}}
                    </td>
                </tr>`;
            }}).join('');

            document.getElementById('perf-high').innerHTML = heroes.filter(h => h.assigned_projects.length > 0).map(h => `
                <div class="list-item">
                    <div><strong>${{h.name}}</strong></div>
                    <div class="badge bg-success">Chất lượng tốt</div>
                </div>
            `).join('') || '<div style="color:var(--text-muted); font-size:0.85rem">Trống</div>';

            let lowHtml = '';
            lowPerfStaff.forEach(l => {{
                let isFake = l.warning_flags && l.warning_flags.some(w => w.includes('UNVERIFIED'));
                lowHtml += `<div class="list-item">
                    <div><strong>${{l.name}}</strong></div>
                    <div class="badge bg-danger">Hiệu suất kém</div>
                    ${{isFake ? '<div class="badge bg-danger" style="margin-left:5px">Khai khống</div>' : ''}}
                </div>`;
            }});
            idleStaff.forEach(i => {{
                if (!lowPerfStaff.find(l => l.name === i.name)) {{
                    let isFake = i.warning_flags && i.warning_flags.some(w => w.includes('UNVERIFIED'));
                    lowHtml += `<div class="list-item">
                        <div><strong>${{i.name}}</strong></div>
                        <div class="badge bg-danger">Trống việc 100%</div>
                        ${{isFake ? '<div class="badge bg-danger" style="margin-left:5px">Khai khống</div>' : ''}}
                    </div>`;
                }}
            }});
            availableStaff.forEach(a => {{
                if (!lowPerfStaff.find(l => l.name === a.name)) {{
                    let isFake = a.warning_flags && a.warning_flags.some(w => w.includes('UNVERIFIED'));
                    lowHtml += `<div class="list-item">
                        <div><strong>${{a.name}}</strong></div>
                        <div class="badge bg-info">Sẵn sàng (Available)</div>
                        ${{isFake ? '<div class="badge bg-danger" style="margin-left:5px">Khai khống</div>' : ''}}
                    </div>`;
                }}
            }});
            document.getElementById('perf-low').innerHTML = lowHtml || '<div style="color:var(--success); font-size:0.85rem">Không có cảnh báo</div>';
            
            // Render Blacklist
            let blacklistStaff = personnel.filter(p => p.warning_flags && p.warning_flags.some(w => w.includes('UNVERIFIED')));
            document.getElementById('blacklist-content').innerHTML = blacklistStaff.length ? blacklistStaff.map(s => {{
                let fakeTasks = s.warning_flags.filter(w => w.includes('UNVERIFIED'));
                let details = fakeTasks.map(f => `<div style="font-size:0.8rem; color:var(--text-muted); margin-top:4px"><i class="fas fa-times-circle" style="color:var(--danger)"></i> ${{f.replace('UNVERIFIED: ', '')}}</div>`).join('');
                return `
                <div class="list-item" style="flex-direction: column; align-items: flex-start;">
                    <div style="display: flex; justify-content: space-between; width: 100%;">
                        <div><strong>${{s.name}}</strong> <small style="color:var(--text-muted)">(${{s.group}})</small></div>
                        <div class="badge bg-danger">${{fakeTasks.length}} Task Chưa Xác Thực</div>
                    </div>
                    <div style="margin-top: 8px; width: 100%; padding: 8px; background: rgba(255,255,255,0.02); border-radius: 6px;">
                        ${{details}}
                    </div>
                </div>
                `;
            }}).join('') : '<div style="padding:10px; color:var(--success)">Tất cả báo cáo tiến độ dự án đều khớp với hệ thống Worklane.</div>';
        }}

        async function fetchLiveDailyLogsData(showNotification) {{
            const icon = document.getElementById("refresh-icon");
            if (icon) icon.classList.add("fa-spin");
            
            try {{
                const pathsToTry = [
                    "../../../data/processed/agent4_payload.json",
                    "../../data/processed/agent4_payload.json",
                    "/data/processed/agent4_payload.json"
                ];
                let fetchedData = null;
                for (const p of pathsToTry) {{
                    try {{
                        const res = await fetch(p);
                        if (res.ok) {{
                            fetchedData = await res.json();
                            break;
                        }}
                    }} catch(e) {{}}
                }}
                if (fetchedData) {{
                    RAW_DATA.departments = fetchedData.departments;
                    RAW_DATA.today_date = fetchedData.today_date;
                    RAW_DATA.personnel = fetchedData.personnel;
                    RAW_DATA.projects = fetchedData.projects;
                    RAW_DATA.heatmap = fetchedData.heatmap;
                    
                    initApp();
                    if (showNotification) alert("Đã cập nhật dữ liệu mới nhất từ Worklane PM thành công!");
                }} else {{
                    if (showNotification) alert("Đang chạy ở chế độ Offline. Dashboard tiếp tục sử dụng dữ liệu đã nhúng sẵn.");
                }}
            }} catch (err) {{
                console.warn("Fetch live data error:", err);
            }} finally {{
                if (icon) icon.classList.remove("fa-spin");
            }}
        }}

        window.onload = initApp;
    </script>
</body>
</html>
"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write("# PMO Dashboard Report (V4.1)\\n\\nReport V4.1 generated successfully.")
        
    print("Agent 4: Sinh trang báo cáo PMO HTML V4.1 thành công!")

if __name__ == "__main__":
    main()

# QLDT Report Restructuring Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Rebuild the QLĐT Monthly Report (`qldt_monthly_report.html`) to support a tabbed SPA (Single Page Application) layout showing Daily, Weekly, and Monthly views, filtering data dynamically based on the selected period.

**Architecture:** 
1. Modify `generate_qldt_report.py` to extract all daily logs, weekly aggregates, and monthly performance parameters (without hardcoding July) and dump them into JSON variables.
2. Embed the processed JSON structures (`qldtDailyData`, `qldtWeeklyData`, `qldtMonthlyData`) into the HTML template.
3. Update the HTML layout to introduce Tab Navigation (`tab-daily`, `tab-weekly`, `tab-monthly`) and dropdown selectors.
4. Implement client-side JS handlers to automatically render data and update Chart.js instances on filter changes (destroying old charts before recreating them to prevent overlapping).

**Tech Stack:** Python 3.12 (uv), Vanilla HTML5/CSS3, JavaScript (ES6+), Chart.js (v4.x via CDN).

---

### Task 1: Refactor Backend Data Packaging

**Files:**
- Modify: `agents/advanced/management_audit/generate_qldt_report.py`

**Step 1: Write a verification script to run the original report generator**
Make sure we can execute the current python file without error.
Run: `uv run agents/advanced/management_audit/generate_qldt_report.py`
Expected: `html_output_path` generated successfully in `output/dashboards/advanced/qldt_monthly_report.html`.

**Step 2: Refactor data packaging logic in Python**
Locate the code around lines 61-260 in [generate_qldt_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/advanced/management_audit/generate_qldt_report.py#L61-L260) and modify it to extract data into three structures: `qldt_daily_data`, `qldt_weekly_data`, and `qldt_monthly_data`. Remove the hardcoded date filters for July 2026.

```python
    # ----------------------------------------------------
    # NEW ARCHITECTURE: PACKAGING DATA FOR DAILY/WEEKLY/MONTHLY
    # ----------------------------------------------------
    qldt_daily_data = {}
    qldt_weekly_data = {}
    qldt_monthly_data = {}

    # Extract all available dates
    all_dates = sorted(list(raw_reports.get("Khối QLCLĐT", {}).get("Nguyễn Thị Tươi", {}).get("reports", {}).keys()))
    
    # 1. Package Daily Data
    for date_str in all_dates:
        day_summary = {"total_hours": 0.0, "total_tasks": 0, "completed_tasks": 0}
        staffs_day = {}
        for name, dept in dept_mappings.items():
            dept_data = raw_reports.get(dept, {})
            staff_data = dept_data.get(name, {})
            reports = staff_data.get("reports", {})
            report = reports.get(date_str)
            if report:
                tasks = report.get("tasks", [])
                staff_hours = sum(float(t.get("hours", 0.0)) for t in tasks)
                staff_completed = sum(1 for t in tasks if t.get("done") or t.get("percent") == 100)
                
                day_summary["total_hours"] += staff_hours
                day_summary["total_tasks"] += len(tasks)
                day_summary["completed_tasks"] += staff_completed
                
                staff_tasks = []
                for t in tasks:
                    staff_tasks.append({
                        "title": t.get("title", "").strip(),
                        "hours": float(t.get("hours", 0.0)),
                        "status_text": "Đã hoàn thành" if (t.get("done") or t.get("percent") == 100) else f"Đang thực hiện ({t.get('percent')}%)" if t.get("percent", 0) > 0 else "Chưa hoàn thành",
                        "project": report.get("project") or "Công việc chung"
                    })
                
                staffs_day[name] = {
                    "role": qldt_staff_info[name]["role"],
                    "total_hours": staff_hours,
                    "tasks": staff_tasks,
                    "difficulties": report.get("difficulties", "").strip()
                }
        if staffs_day:
            qldt_daily_data[date_str] = {
                "summary": day_summary,
                "staffs": staffs_day
            }

    # 2. Package Weekly Data
    # Grab weekly stats from daily_log_analysis.json (we can read weekly_stats or compute it)
    # To keep simple, let's use the weekly_analysis details if available, or compute based on dates
    # In generate_qldt_report.py, we will construct qldt_weekly_data dynamically
    weekly_analysis = analysis_data.get("weekly_stats", {})
    # Look for week keys in raw logs
    # Assume we group dates by ISO week or use the dates_weekly array
    dates_weekly = analysis_data.get("dates_weekly", [])
    if dates_weekly:
        week_key = f"Tuần hiện tại ({dates_weekly[0].split('-')[-1]}/{dates_weekly[0].split('-')[-2]} - {dates_weekly[-1].split('-')[-1]}/{dates_weekly[-1].split('-')[-2]})"
        week_summary = {"avg_daily_hours": 0.0, "completion_rate": 0.0, "total_hours": 0.0}
        staffs_week = {}
        
        tot_hrs = 0.0
        tot_tasks = 0
        tot_done = 0
        for name in dept_mappings.keys():
            staff_hrs = 0.0
            staff_tasks = 0
            staff_done = 0
            uncompleted = []
            for date_str in dates_weekly:
                day_info = qldt_daily_data.get(date_str, {}).get("staffs", {}).get(name, {})
                if day_info:
                    staff_hrs += day_info["total_hours"]
                    for t in day_info["tasks"]:
                        staff_tasks += 1
                        if "Đã hoàn thành" in t["status_text"]:
                            staff_done += 1
                        else:
                            uncompleted.append(f"{t['title']} ({t['status_text']})")
            
            tot_hrs += staff_hrs
            tot_tasks += staff_tasks
            tot_done += staff_done
            
            staffs_week[name] = {
                "total_hours": staff_hrs,
                "completed_tasks": staff_done,
                "total_tasks": staff_tasks,
                "uncompleted_tasks": uncompleted
            }
        
        week_summary["total_hours"] = tot_hrs
        week_summary["completion_rate"] = (tot_done / tot_tasks) * 100.0 if tot_tasks > 0 else 0.0
        week_summary["avg_daily_hours"] = (tot_hrs / len(dates_weekly)) / len(dept_mappings) if dates_weekly else 0.0
        
        # Build trend daily average hours
        trend = []
        for date_str in dates_weekly:
            day_hrs = sum(qldt_daily_data.get(date_str, {}).get("staffs", {}).get(n, {}).get("total_hours", 0.0) for n in dept_mappings.keys())
            trend.append(day_hrs / len(dept_mappings))
            
        qldt_weekly_data[week_key] = {
            "summary": week_summary,
            "dept_trend_hours": trend,
            "dates": dates_weekly,
            "staffs": staffs_week
        }

    # 3. Package Monthly Data (support July and August)
    months = ["Tháng 8/2026", "Tháng 7/2026"]
    month_ranges = {
        "Tháng 8/2026": ("2026-08-01", "2026-08-31"),
        "Tháng 7/2026": ("2026-07-01", "2026-07-31")
    }
    
    for m_name, (start_d, end_d) in month_ranges.items():
        m_dates = [d for d in all_dates if d >= start_d and d <= end_d]
        if not m_dates:
            continue
            
        m_summary = {"total_tasks": 0, "completed_tasks": 0, "total_hours": 0.0, "avg_work_score": 0.0}
        staffs_month = {}
        m_dept_domain_hours = {
            "Khảo thí": 0.0,
            "Thời khóa biểu": 0.0,
            "Hành chính & Hỗ trợ SV": 0.0,
            "Xây dựng quy định & tài nguyên": 0.0,
            "Họp & Công việc chung": 0.0
        }
        
        total_scores = 0.0
        for name, dept in dept_mappings.items():
            reported_days_count = 0
            all_tasks = []
            completed_tasks_count = 0
            total_hours = 0.0
            difficulties_list = []
            uncompleted_tasks_list = []
            
            domain_hours = {k: 0.0 for k in m_dept_domain_hours.keys()}
            
            for date_str in m_dates:
                day_info = qldt_daily_data.get(date_str, {}).get("staffs", {}).get(name, {})
                if day_info:
                    reported_days_count += 1
                    total_hours += day_info["total_hours"]
                    if day_info["difficulties"] and day_info["difficulties"].lower() not in ["không", "không có", "no", "none", "n/a"]:
                        difficulties_list.append({"date": date_str, "content": day_info["difficulties"]})
                        
                    for t in day_info["tasks"]:
                        all_tasks.append(t)
                        if "Đã hoàn thành" in t["status_text"]:
                            completed_tasks_count += 1
                        else:
                            uncompleted_tasks_list.append({"date": date_str, "title": t["title"], "status": t["status_text"]})
                            
                        dom = classify_task(t["title"])
                        domain_hours[dom] += t["hours"]
                        m_dept_domain_hours[dom] += t["hours"]
            
            # Fetch work_score from daily_log_analysis.json (fallback if not present)
            work_score = monthly_stats.get(name.lower(), {}).get("work_score", 90.0)
            
            # Recalculate HSNX / Rating
            if name == "Trần Thị Mỹ Phước":
                proposed_ns = 1.15; classification = "Xuất sắc"
                evaluation = f"Hoàn thành xuất sắc nhiệm vụ {m_name.lower()}, quản lý tốt cổng hành chính và các dự án phát sinh."
            elif name == "Nguyễn Huyền Trang":
                proposed_ns = 1.10; classification = "Tốt"
                evaluation = f"Tổ chức tốt các đợt thi sát hạch tiếng Anh TOEIC. Cần cải thiện thời gian nộp báo cáo đúng hạn hơn."
            elif name == "Nguyễn Xuân Bách":
                proposed_ns = 1.05; classification = "Khá tốt"
                evaluation = f"Hoàn thành tốt các nhiệm vụ được giảng dạy và khảo thí trong {m_name.lower()}."
            else:
                proposed_ns = 0.75; classification = "Cần cải thiện"
                evaluation = "Tỷ lệ hoàn thành công việc thấp, cần chú ý nộp báo cáo ngày đúng hạn và tăng tốc tiến độ task."
                
            staffs_month[name] = {
                "role": qldt_staff_info[name]["role"],
                "rank": qldt_staff_info[name]["rank"],
                "reported_days": reported_days_count,
                "report_rate": (reported_days_count / len(m_dates)) * 100.0 if m_dates else 0.0,
                "total_tasks": len(all_tasks),
                "completed_tasks": completed_tasks_count,
                "completion_rate": (completed_tasks_count / len(all_tasks)) * 100.0 if all_tasks else 0.0,
                "total_hours": total_hours,
                "work_score": work_score,
                "proposed_ns": proposed_ns,
                "classification": classification,
                "evaluation": evaluation,
                "difficulties": difficulties_list,
                "uncompleted_tasks": uncompleted_tasks_list,
                "domain_hours": domain_hours,
                "projects": get_staff_projects(projects_data, name)
            }
            
            m_summary["total_tasks"] += len(all_tasks)
            m_summary["completed_tasks"] += completed_tasks_count
            m_summary["total_hours"] += total_hours
            total_scores += work_score
            
        m_summary["avg_work_score"] = total_scores / len(dept_mappings)
        
        qldt_monthly_data[m_name] = {
            "summary": m_summary,
            "dept_domain_hours": m_dept_domain_hours,
            "staffs": staffs_month
        }
```

**Step 3: Inject data into HTML placeholders**
Update the replacement block near the bottom of [generate_qldt_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/advanced/management_audit/generate_qldt_report.py#L1495-L1510):
```python
    # Inject variables into script
    html_output = html_template.replace("__DAILY_DATA_PLACEHOLDER__", json.dumps(qldt_daily_data, ensure_ascii=False))
    html_output = html_output.replace("__WEEKLY_DATA_PLACEHOLDER__", json.dumps(qldt_weekly_data, ensure_ascii=False))
    html_output = html_output.replace("__MONTHLY_DATA_PLACEHOLDER__", json.dumps(qldt_monthly_data, ensure_ascii=False))
```

**Step 4: Commit changes**
Run: `git commit -am "feat: refactor backend data packaging for daily/weekly/monthly views"`

---

### Task 2: Implement UI Tabs and Navigation Layout

**Files:**
- Modify: `agents/advanced/management_audit/generate_qldt_report.py` (HTML Template String starting around lines 415-1062)

**Step 1: Re-design the Header and Navigation**
Replace the top menu navigation with 3 big Tab Buttons:
```html
  <div class="header-card">
    <div class="header-title">
      <h1>📊 Báo cáo Năng suất & Đề xuất HSNX - Bộ phận QLĐT</h1>
      <p>PTITxRikkei Joint Venture — Đánh giá năng lực và khối lượng công việc giáo vụ</p>
    </div>
    <div class="tab-nav-main" style="display: flex; gap: 8px;">
      <button class="tab-main-btn" onclick="switchMainTab('tab-daily')">📅 Báo cáo Ngày</button>
      <button class="tab-main-btn" onclick="switchMainTab('tab-weekly')">📈 Báo cáo Tuần</button>
      <button class="tab-main-btn active" onclick="switchMainTab('tab-monthly')">🏆 Báo cáo Tháng</button>
    </div>
  </div>
```

**Step 2: Add CSS styles for the new layout**
Add new CSS rules inside the `<style>` block in the HTML template:
```css
    .tab-main-btn {
      background: #1c1e22;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 10px 20px;
      font-weight: 600;
      cursor: pointer;
      border-radius: 6px;
      transition: all 0.2s ease;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .tab-main-btn.active {
      background: var(--accent-color);
      color: #fff;
      border-color: var(--accent-color);
      box-shadow: 0 0 12px rgba(94, 106, 210, 0.4);
    }
    .main-tab-content {
      display: none;
    }
    .main-tab-content.active {
      display: block;
    }
    .filter-section {
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .select-dropdown {
      background: #1c1e22;
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 8px 16px;
      border-radius: 4px;
      font-size: 13px;
      cursor: pointer;
      outline: none;
    }
    .staff-chips-container {
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }
    .staff-chip-btn {
      background: #1c1e22;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 20px;
      cursor: pointer;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .staff-chip-btn.active {
      background: rgba(94, 106, 210, 0.15);
      color: var(--text-main);
      border-color: var(--accent-color);
    }
```

**Step 3: Structure HTML for Tab 1: Daily View**
Create the container for `tab-daily`:
```html
  <div id="tab-daily" class="main-tab-content">
    <div class="filter-section">
      <label for="select-date"><strong>📅 Chọn ngày làm việc:</strong></label>
      <select id="select-date" class="select-dropdown" onchange="handleDateChange(this.value)">
        <!-- Options populated dynamically -->
      </select>
    </div>
    
    <div class="metric-grid">
      <div class="metric-card"><div class="metric-label">Tổng giờ làm việc</div><div class="metric-value" id="daily-metric-hours">0.0 <span class="metric-unit">giờ</span></div></div>
      <div class="metric-card"><div class="metric-label">Tổng số task làm</div><div class="metric-value" id="daily-metric-tasks">0 <span class="metric-unit">task</span></div></div>
      <div class="metric-card success"><div class="metric-label">Task hoàn thành</div><div class="metric-value" id="daily-metric-completed">0 <span class="metric-unit">task</span></div></div>
    </div>

    <div class="staff-chips-container" id="daily-staff-chips">
      <!-- Chips populated dynamically -->
    </div>

    <div class="card">
      <div class="card-title" id="daily-staff-detail-title">Chi Tiết Nhật Ký Công Việc</div>
      <p id="daily-staff-detail-role" style="color: var(--text-muted); margin-bottom: 12px; font-weight: 600;"></p>
      
      <div class="card" style="border-color: rgba(255, 69, 58, 0.2); background: rgba(255, 69, 58, 0.01); margin-bottom: 16px;">
        <div class="card-title" style="color: var(--danger); font-size:12px; margin-bottom: 4px;"><i class="fa-solid fa-triangle-exclamation"></i> KHÓ KHĂN / VƯỚNG MẮC TRONG NGÀY</div>
        <p id="daily-staff-difficulty" style="font-style: italic; color: var(--text-main);"></p>
      </div>

      <table class="data-table" style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr style="border-bottom: 2px solid var(--border-color); text-align: left;">
            <th style="padding: 10px;">Dự án / Topic</th>
            <th style="padding: 10px;">Tên công việc</th>
            <th style="padding: 10px; width: 80px;">Thời lượng</th>
            <th style="padding: 10px; width: 120px;">Trạng thái</th>
          </tr>
        </thead>
        <tbody id="daily-staff-tasks-tbody">
          <!-- Populated dynamically -->
        </tbody>
      </table>
    </div>
  </div>
```

**Step 4: Structure HTML for Tab 2: Weekly View**
Create the container for `tab-weekly`:
```html
  <div id="tab-weekly" class="main-tab-content">
    <div class="filter-section">
      <label for="select-week"><strong>📈 Chọn tuần làm việc:</strong></label>
      <select id="select-week" class="select-dropdown" onchange="handleWeekChange(this.value)">
        <!-- Options populated dynamically -->
      </select>
    </div>

    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 20px;">
      <div class="card">
        <div class="card-title">Xu hướng giờ làm việc trung bình hàng ngày trong tuần (Bộ phận)</div>
        <div style="height: 280px; position: relative;">
          <canvas id="weekly-trend-chart"></canvas>
        </div>
      </div>
      
      <div class="card">
        <div class="card-title">Chỉ số tuần bộ phận</div>
        <div class="metric-card" style="margin-bottom: 12px;"><div class="metric-label">Giờ làm TB/ngày/người</div><div class="metric-value" id="weekly-metric-avg-hours">0.0 <span class="metric-unit">h</span></div></div>
        <div class="metric-card success"><div class="metric-label">Tỷ lệ hoàn thành task tuần</div><div class="metric-value" id="weekly-metric-completion">0%</div></div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Bảng Năng Suất Tuần Nhân Sự</div>
      <table class="data-table" style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr style="border-bottom: 2px solid var(--border-color); text-align: left;">
            <th style="padding: 10px;">Nhân viên</th>
            <th style="padding: 10px;">Tổng giờ làm</th>
            <th style="padding: 10px;">Số task thực hiện</th>
            <th style="padding: 10px;">Tỷ lệ hoàn thành</th>
          </tr>
        </thead>
        <tbody id="weekly-staff-tbody">
          <!-- Populated dynamically -->
        </tbody>
      </table>
    </div>

    <div class="card" style="border-color: rgba(255, 159, 10, 0.2); background: rgba(255, 159, 10, 0.01);">
      <div class="card-title" style="color: var(--warning);"><i class="fa-solid fa-triangle-exclamation"></i> TỔNG HỢP VƯỚNG MẮC NỔI BẬT TRONG TUẦN</div>
      <ul id="weekly-difficulties-list" class="block-list warning" style="list-style: none; padding-left: 0;">
        <!-- Populated dynamically -->
      </ul>
    </div>
  </div>
```

**Step 5: Structure HTML for Tab 3: Monthly View (Restructured from old layout)**
Make sure to wrap the old monthly elements inside a `<div id="tab-monthly" class="main-tab-content active">` block. Introduce a dropdown `<select id="select-month" class="select-dropdown" onchange="handleMonthChange(this.value)">` in the filter section of Tab 3.

**Step 6: Commit changes**
Run: `git commit -am "feat: implement HTML containers for daily, weekly and monthly tabs"`

---

### Task 3: Implement Client-Side JS Dynamic Rendering Engine

**Files:**
- Modify: `agents/advanced/management_audit/generate_qldt_report.py` (Script section starting around line 1063 onwards)

**Step 1: Define main JS dynamic router script**
Implement the router to fetch variables and draw elements dynamically:

```javascript
    // Fetch embedded JSON datasets
    const qldtDailyData = __DAILY_DATA_PLACEHOLDER__;
    const qldtWeeklyData = __WEEKLY_DATA_PLACEHOLDER__;
    const qldtMonthlyData = __MONTHLY_DATA_PLACEHOLDER__;

    // View States
    let activeMainTab = "tab-monthly";
    let selectedDate = "";
    let selectedWeek = "";
    let selectedMonth = "";
    let selectedStaff = "Trần Thị Mỹ Phước";

    // Chart Handles
    let weeklyChartInstance = null;
    let monthlyChartInstance = null;

    function initDashboard() {
      // 1. Init Dropdowns
      const dates = Object.keys(qldtDailyData).sort().reverse();
      const dateSelect = document.getElementById("select-date");
      dates.forEach(d => {
        const opt = document.createElement("option");
        opt.value = d;
        opt.textContent = formatDate(d);
        dateSelect.appendChild(opt);
      });
      selectedDate = dates[0] || "";

      const weeks = Object.keys(qldtWeeklyData).sort().reverse();
      const weekSelect = document.getElementById("select-week");
      weeks.forEach(w => {
        const opt = document.createElement("option");
        opt.value = w;
        opt.textContent = w;
        weekSelect.appendChild(opt);
      });
      selectedWeek = weeks[0] || "";

      const months = Object.keys(qldtMonthlyData).sort().reverse();
      const monthSelect = document.getElementById("select-month");
      months.forEach(m => {
        const opt = document.createElement("option");
        opt.value = m;
        opt.textContent = m;
        monthSelect.appendChild(opt);
      });
      selectedMonth = months[0] || "";

      // 2. Render initial tabs
      renderDailyTab();
      renderWeeklyTab();
      renderMonthlyTab();
      
      // Default to Monthly Tab
      switchMainTab("tab-monthly");
    }

    function switchMainTab(tabId) {
      activeMainTab = tabId;
      document.querySelectorAll(".main-tab-content").forEach(el => el.classList.remove("active"));
      document.querySelectorAll(".tab-main-btn").forEach(el => el.classList.remove("active"));
      
      document.getElementById(tabId).classList.add("active");
      
      // Highlight correct button
      const btns = document.querySelectorAll(".tab-main-btn");
      btns.forEach(btn => {
        if (btn.getAttribute("onclick").includes(tabId)) {
          btn.classList.add("active");
        }
      });

      // Redraw charts if tab is selected
      if (tabId === "tab-weekly") {
        drawWeeklyChart();
      } else if (tabId === "tab-monthly") {
        drawMonthlyChart();
      }
    }

    function formatDate(dStr) {
      if (!dStr) return "";
      const p = dStr.split("-");
      return `${p[2]}/${p[1]}/${p[0]}`;
    }
```

**Step 2: Implement dynamic rendering for Tab 1 (Daily)**
```javascript
    function handleDateChange(val) {
      selectedDate = val;
      renderDailyTab();
    }

    function handleStaffSelect(name) {
      selectedStaff = name;
      renderDailyStaffDetail();
    }

    function renderDailyTab() {
      const data = qldtDailyData[selectedDate];
      if (!data) return;

      // Update Metrics
      document.getElementById("daily-metric-hours").textContent = `${data.summary.total_hours.toFixed(1)} giờ`;
      document.getElementById("daily-metric-tasks").textContent = `${data.summary.total_tasks} task`;
      document.getElementById("daily-metric-completed").textContent = `${data.summary.completed_tasks} task`;

      // Render Staff Chips
      const chipContainer = document.getElementById("daily-staff-chips");
      chipContainer.innerHTML = "";
      Object.keys(data.staffs).forEach(name => {
        const staff = data.staffs[name];
        const btn = document.createElement("button");
        btn.className = `staff-chip-btn ${selectedStaff === name ? 'active' : ''}`;
        btn.innerHTML = `<i class="fa-solid fa-user-gear"></i> <strong>${name}</strong> (${staff.total_hours.toFixed(1)}h)`;
        btn.onclick = () => handleStaffSelect(name);
        chipContainer.appendChild(btn);
      });

      renderDailyStaffDetail();
    }

    function renderDailyStaffDetail() {
      const data = qldtDailyData[selectedDate];
      if (!data) return;
      
      const staff = data.staffs[selectedStaff];
      if (!staff) {
        // Fallback to first available staff
        const firstStaff = Object.keys(data.staffs)[0];
        if (firstStaff) {
          selectedStaff = firstStaff;
          renderDailyStaffDetail();
        }
        return;
      }

      document.getElementById("daily-staff-detail-title").textContent = `Chi Tiết Nhật Ký Công Việc: ${selectedStaff}`;
      document.getElementById("daily-staff-detail-role").textContent = `${staff.role}`;

      // Difficulties
      const diffEl = document.getElementById("daily-staff-difficulty");
      if (staff.difficulties && staff.difficulties !== "") {
        diffEl.textContent = staff.difficulties;
        diffEl.parentElement.style.display = "block";
      } else {
        diffEl.textContent = "Không ghi nhận khó khăn hay vướng mắc.";
        diffEl.style.color = "var(--text-muted)";
      }

      // Tasks
      const tbody = document.getElementById("daily-staff-tasks-tbody");
      tbody.innerHTML = "";
      staff.tasks.forEach(t => {
        const tr = document.createElement("tr");
        tr.style.borderBottom = "1px solid var(--border-color)";
        
        let statusBadge = "color: var(--text-muted);";
        if (t.status_text === "Đã hoàn thành") statusBadge = "color: var(--success); font-weight: bold;";
        else if (t.status_text.includes("Đang thực hiện")) statusBadge = "color: var(--info);";

        tr.innerHTML = `
          <td style="padding: 10px;">${t.project}</td>
          <td style="padding: 10px; color: var(--text-main); font-weight:500;">${t.title}</td>
          <td style="padding: 10px; font-family: monospace;">${t.hours.toFixed(1)}h</td>
          <td style="padding: 10px; ${statusBadge}">${t.status_text}</td>
        `;
        tbody.appendChild(tr);
      });
    }
```

**Step 3: Implement dynamic rendering for Tab 2 (Weekly) & Trend Chart**
```javascript
    function handleWeekChange(val) {
      selectedWeek = val;
      renderWeeklyTab();
      drawWeeklyChart();
    }

    function renderWeeklyTab() {
      const data = qldtWeeklyData[selectedWeek];
      if (!data) return;

      // Update Metrics
      document.getElementById("weekly-metric-avg-hours").textContent = `${data.summary.avg_daily_hours.toFixed(1)} h`;
      document.getElementById("weekly-metric-completion").textContent = `${data.summary.completion_rate.toFixed(1)}%`;

      // Update Weekly Table
      const tbody = document.getElementById("weekly-staff-tbody");
      tbody.innerHTML = "";
      Object.keys(data.staffs).forEach(name => {
        const staff = data.staffs[name];
        const tr = document.createElement("tr");
        tr.style.borderBottom = "1px solid var(--border-color)";
        tr.innerHTML = `
          <td style="padding: 10px; font-weight: 600; color: var(--text-main);">${name}</td>
          <td style="padding: 10px; font-family: monospace;">${staff.total_hours.toFixed(1)}h</td>
          <td style="padding: 10px;">${staff.completed_tasks}/${staff.total_tasks} task</td>
          <td style="padding: 10px; color: var(--success); font-weight: 600;">${((staff.completed_tasks / staff.total_tasks) * 100 || 0).toFixed(1)}%</td>
        `;
        tbody.appendChild(tr);
      });

      // Update Difficulties list
      const diffList = document.getElementById("weekly-difficulties-list");
      diffList.innerHTML = "";
      
      let totalDiffCount = 0;
      Object.keys(qldtDailyData).forEach(dDate => {
        const weekDates = data.dates || [];
        if (weekDates.includes(dDate)) {
          const dayInfo = qldtDailyData[dDate];
          Object.keys(dayInfo.staffs).forEach(name => {
            const staff = dayInfo.staffs[name];
            if (staff.difficulties && staff.difficulties !== "") {
              const li = document.createElement("li");
              li.style.borderLeft = "4px solid var(--warning)";
              li.style.background = "#1c1e22";
              li.style.padding = "8px 12px";
              li.style.marginBottom = "8px";
              li.style.borderRadius = "4px";
              li.innerHTML = `<strong>${formatDate(dDate)} — ${name}</strong>: ${staff.difficulties}`;
              diffList.appendChild(li);
              totalDiffCount++;
            }
          });
        }
      });
      
      if (totalDiffCount === 0) {
        diffList.innerHTML = `<li style="color: var(--text-muted); font-style: italic; padding: 10px;">Không ghi nhận vướng mắc nổi bật nào trong tuần.</li>`;
      }
    }

    function drawWeeklyChart() {
      const data = qldtWeeklyData[selectedWeek];
      if (!data) return;

      if (weeklyChartInstance) {
        weeklyChartInstance.destroy();
      }

      const ctx = document.getElementById("weekly-trend-chart").getContext("2d");
      const labels = (data.dates || []).map(formatDate);
      
      weeklyChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: "Số giờ TB/giáo vụ",
            data: data.dept_trend_hours,
            backgroundColor: "rgba(94, 106, 210, 0.7)",
            borderColor: "var(--accent-color)",
            borderWidth: 1,
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: "var(--border-color)" },
              ticks: { color: "var(--text-muted)" }
            },
            x: {
              grid: { display: false },
              ticks: { color: "var(--text-muted)" }
            }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    }
```

**Step 4: Implement dynamic rendering for Tab 3 (Monthly) & Doughnut Chart**
Write `handleMonthChange`, `renderMonthlyTab`, and `drawMonthlyChart` to load monthly rankings, comments, classification, and render the department's work domain distribution using a Doughnut chart. Make sure it destroys `monthlyChartInstance` before recreation.

**Step 5: Run initDashboard on load**
Add:
```javascript
    window.onload = function() {
      initDashboard();
    };
```

**Step 6: Commit changes**
Run: `git commit -am "feat: implement JavaScript SPA engine for daily, weekly and monthly dynamic updates"`

---

### Task 4: Pipeline Integration & Verification

**Files:**
- Modify: `run_pipeline.py:103-110`

**Step 1: Register generate_qldt_report.py in run_pipeline.py**
Add `generate_qldt_report.py` as a step right after `generate_report_director.py`. Ensure we validate its output:
```python
    # Bước 4.6: Chạy báo cáo tháng QLĐT (QLĐT Monthly Report)
    run_script(
        "Advanced QLDT Report: Báo cáo tháng QLĐT",
        "agents/advanced/management_audit/generate_qldt_report.py",
        with_deps=["openpyxl"]
    )
    validate_output("output/dashboards/advanced/qldt_monthly_report.html", "html")
```

**Step 2: Run pipeline to verify compilation and outputs**
Run: `uv run run_pipeline.py`
Expected: The pipeline finishes successfully (exit code 0), and both `director_cockpit.html` and `qldt_monthly_report.html` are validated.

**Step 3: Run VisualQA verification using browser_subagent**
Confirm that no JavaScript reference errors are present and tabs can be clicked without showing a blank page.

**Step 4: Commit and finalize**
Run: `git add .`
Run: `git commit -m "feat: integrate restructured QLDT report into pipeline and verify outputs"`

---

## Verification Plan

### Automated Verification
1. Run pipeline compilation:
   ```bash
   uv run run_pipeline.py
   ```
2. Verify HTML syntax and compliance using validator:
   ```bash
   uv run agents/common/validator.py output/dashboards/advanced/qldt_monthly_report.html html
   ```

### Manual Verification
1. Open `output/dashboards/advanced/qldt_monthly_report.html` in Chrome or Edge.
2. Click through `Báo cáo Ngày`, `Báo cáo Tuần`, `Báo cáo Tháng` and verify tabs transition cleanly.
3. Toggle day/week/month dropdowns to confirm all charts and statistics dynamically redraw without reloading.

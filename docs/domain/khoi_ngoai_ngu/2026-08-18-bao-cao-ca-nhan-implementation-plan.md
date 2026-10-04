# Báo cáo Hồ sơ Cá nhân Implementation Plan (Updated)

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Cập nhật tính năng Báo cáo Hồ sơ Cá nhân: (1) Thêm thanh thống kê tóm tắt số lượng công việc (tổng, hoàn thành, đang làm, trễ hạn, tỷ lệ hoàn thành), (2) Chỉ tính toán chỉ số tuân thủ và cảnh báo kỷ luật đến ngày hiện tại (loại bỏ các ngày tương lai).

**Architecture:**
1. Chỉnh sửa logic Python backend để lọc ngày $\le$ ngày hiện tại trong tính toán tỷ lệ nộp báo cáo và danh sách ngày thiếu (`miss`) của tuần/tháng.
2. Chỉnh sửa logic JS client-side tương ứng để lọc ngày $\le$ ngày hiện tại khi Live Refresh.
3. Cập nhật HTML để chèn khối `#profile-tasks-summary` và cập nhật logic `renderProfile` để tính toán và hiển thị thanh tóm tắt công việc cá nhân.

**Tech Stack:** HTML5, CSS3, Vanilla JS, Python.

---

### Task 1: Cập nhật logic lọc ngày hiện tại trong Python Backend (pipeline_nn.py)

**Files:**
*   Modify: `c:/Users/DELL/Desktop/AI-Agent/AI_Report_NN/scratch/pipeline_nn.py:255-290` (Hàm process - lọc tuần và tháng)

**Step 1: Viết mã nguồn thay đổi tại hàm process**
Lọc các ngày trong tuần và tháng đảm bảo $\le$ ngày hiện tại (`today`):
```python
        today_str = datetime.date.today().isoformat()
        ws = {}
        for wk, winfo in WEEKS.items():
            dd = winfo["dates"]
            # Chỉ tính toán các ngày đã/đang diễn ra (<= today)
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
                "rep": rep, "tot": len(valid_dd), "hrs": round(hrs,1), 
                "kpi_hrs": round(kpi_hrs,1), "adhoc_hrs": round(adhoc_hrs,1), 
                "avg": avg, "target_met": target_met, "pct_target": pct_target,
                "tsk": tsk, "dn": dn,
                "miss": [d for d in valid_dd if d not in person_daily.get(name, {})]
            }
        
        # Lọc cho tháng/toàn bộ giai đoạn
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
```

---

### Task 2: Cập nhật JS Client-Side lọc ngày hiện tại (pipeline_nn.py)

**Files:**
*   Modify: `c:/Users/DELL/Desktop/AI-Agent/AI_Report_NN/scratch/pipeline_nn.py:1010-1045` (reprocessClientData)

**Step 1: Viết mã nguồn Javascript trong reprocessClientData**
Cập nhật tương tự phần Python cho phần Live Refresh phía Client:
```javascript
        const today = new Date().toISOString().split('T')[0];
        
        // Reprocess Personnel monthly & weekly
        for (const [name, p] of Object.entries(D.personnel)) {
            const tgtHrs = p.target_hours;
            let aHrs = 0, aKpi = 0, aAdhoc = 0, aRep = 0, aTsk = 0, aDn = 0;

            D.weekOrder.forEach(wk => {
                const dd = D.weeks[wk].dates;
                const validDd = dd.filter(d => d <= today);
                
                let wHrs = 0, wKpi = 0, wAdhoc = 0, wRep = 0, wTsk = 0, wDn = 0;
                validDd.forEach(d => {
                    if (personDaily[name][d]) {
                        wRep++;
                        wHrs += personDaily[name][d].hours;
                        wKpi += personDaily[name][d].kpi_hours;
                        wAdhoc += personDaily[name][d].adhoc_hours;
                        wTsk += personDaily[name][d].tasks;
                        wDn += personDaily[name][d].done;
                    }
                });

                const wAvg = wRep > 0 ? floatVal(wHrs / wRep) : 0;
                p.weekly[wk] = {
                    rep: wRep, tot: validDd.length, hrs: floatVal(wHrs), kpi_hrs: floatVal(wKpi), adhoc_hrs: floatVal(wAdhoc),
                    avg: wAvg, target_met: wAvg >= tgtHrs, pct_target: floatVal(wAvg / tgtHrs * 100),
                    tsk: wTsk, dn: wDn, miss: validDd.filter(d => !personDaily[name][d])
                };

                aHrs += wHrs; aKpi += wKpi; aAdhoc += wAdhoc; aRep += wRep; aTsk += wTsk; aDn += wDn;
            });

            const validAllDates = allDates.filter(d => d <= today);
            const allDatesCount = validAllDates.length;
            const aAvg = aRep > 0 ? floatVal(aHrs / aRep) : 0;
            const aPctTarget = floatVal(aAvg / tgtHrs * 100);
            const subRate = floatVal(aRep / allDatesCount * 100);
            const activeT = wloadActive[name] || 0;
            const overdueT = wloadOverdue[name] || 0;
```

---

### Task 3: Chèn Container và phát triển thanh Tóm tắt Công việc Cá nhân

**Files:**
*   Modify: `c:/Users/DELL/Desktop/AI-Agent/AI_Report_NN/scratch/pipeline_nn.py:805-820` (HTML tab-profile)
*   Modify: `c:/Users/DELL/Desktop/AI-Agent/AI_Report_NN/scratch/pipeline_nn.py:1755-1895` (renderProfile)

**Step 1: Chèn container thống kê công việc**
Thêm `#profile-tasks-summary` trên đầu bảng công việc cá nhân:
```html
            <div class="section">
                <div class="section-title">
                    <div class="section-title-text">📋 Danh sách Công việc Dự án được giao</div>
                </div>
                <div class="kpi-grid" id="profile-tasks-summary" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); margin-bottom: 16px; gap: 12px;"></div>
                <div class="table-wrap"><table id="profile-tasks-table"><thead></thead><tbody></tbody></table></div>
            </div>
```

**Step 2: Cập nhật hàm renderProfile**
*   Lọc ngày Tháng 8 đến ngày hiện tại:
    ```javascript
        const todayStr = new Date().toISOString().split('T')[0];
        const periodDates = allDates.filter(d => {
            if (month === 'all') return d <= todayStr;
            if (month === '07') return d.startsWith('2026-07') && d <= todayStr;
            if (month === '08') return d.startsWith('2026-08') && d <= todayStr;
            return d <= todayStr;
        });
    ```
*   Tính toán các chỉ số thống kê công việc và hiển thị HTML:
    ```javascript
        const completedT = personTasks.filter(t => ['Hoàn thành', 'Done', 'Completed'].includes(t.state)).length;
        const inProgressT = personTasks.filter(t => !['Hoàn thành', 'Done', 'Completed', 'Cancelled', 'Đã hủy'].includes(t.state) && !t.overdue).length;
        const taskCompRate = personTasks.length > 0 ? (completedT / personTasks.length * 100).toFixed(1) : 0;

        document.getElementById('profile-tasks-summary').innerHTML = `
            <div class="kpi-card" style="padding: 12px 16px;"><div class="kpi-icon" style="font-size:1.1rem;margin-bottom:4px;">📋</div><div class="kpi-label" style="font-size:0.65rem;margin-bottom:2px;">Tổng số Task</div><div class="kpi-value" style="font-size:1.3rem;font-weight:700;">${personTasks.length}</div></div>
            <div class="kpi-card" style="padding: 12px 16px;"><div class="kpi-icon" style="font-size:1.1rem;margin-bottom:4px;">✅</div><div class="kpi-label" style="font-size:0.65rem;margin-bottom:2px;">Hoàn thành</div><div class="kpi-value" style="font-size:1.3rem;font-weight:700;color:var(--success);">${completedT}</div></div>
            <div class="kpi-card" style="padding: 12px 16px;"><div class="kpi-icon" style="font-size:1.1rem;margin-bottom:4px;">⚡</div><div class="kpi-label" style="font-size:0.65rem;margin-bottom:2px;">Đang làm</div><div class="kpi-value" style="font-size:1.3rem;font-weight:700;color:var(--info);">${inProgressT}</div></div>
            <div class="kpi-card" style="padding: 12px 16px;"><div class="kpi-icon" style="font-size:1.1rem;margin-bottom:4px;">🔴</div><div class="kpi-label" style="font-size:0.65rem;margin-bottom:2px;">Trễ hạn</div><div class="kpi-value" style="font-size:1.3rem;font-weight:700;color:var(--danger);">${overdueT}</div></div>
            <div class="kpi-card" style="padding: 12px 16px;"><div class="kpi-icon" style="font-size:1.1rem;margin-bottom:4px;">📊</div><div class="kpi-label" style="font-size:0.65rem;margin-bottom:2px;">Tỷ lệ hoàn thành</div><div class="kpi-value" style="font-size:1.3rem;font-weight:700;color:var(--success);">${taskCompRate}%</div></div>
        `;
    ```

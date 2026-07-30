# Design Document: QLĐT Director Executive Resource Dashboard

## 1. Overview & Objectives
- **Target Audience**: Nguyễn Duy Quang (Director of Training).
- **Core Goal**: Provide a clear, actionable dashboard to monitor staff workload, project PIC/Members, and daily logs over various timeframes (Daily/Weekly/Monthly) without cluttering the interface.
- **Constraints**: Maintain clean separation from main pipeline output. Save exclusively in `custom_reports/4_daily_logs_report_director.html`. Handles large datasets (39 staff, 36 projects).

## 2. UI/UX Architecture (Executive Cockpit v5.0)

```
+---------------------------------------------------------------------------------+
| [Header: PMO Executive Cockpit]                     [DAILY/WEEKLY/MONTHLY] [Date] |
+---------------------------------------------------------------------------------+
| [Active Projs: X]  [Completion: X%]  [Overloaded: X]  [Idle: X]                 |
+---------------------------------------------------------------------------------+
| [Stacked Workload (Blocks)]  [Top 5 Overdue Projs]  [Productivity Trend]        |
+---------------------------------------------------------------------------------+
| [Search Bar]  [Dept: All/CNTT/QTKD...]  [Status: All/Overloaded/Idle...]        |
+---------------------------------------------------------------------------------+
| [Staff Table: Name | Block | Workload Status | Active Tasks | Hours | Comp ]    |
| - Staff 1                                                                       |
| - Staff 2                                                                       |
+---------------------------------------------------------------------------------+
| (Slide-over Drawer Panel - Opens from Right upon Staff/Project Click)           |
| +-----------------------------------------------------------------------------+ |
| | [Name] [Avatar] [Role/Rank] [Workload Status]                               | |
| | [Personal Doughnut Chart]                                                   | |
| | [Worklane Active Projects Mini Cards]                                       | |
| | [Detailed Daily Logs Table]                                                 | |
| +-----------------------------------------------------------------------------+ |
+---------------------------------------------------------------------------------+
```

## 3. Data Mitigation Strategies for Large Scale Datasets
1. **Department Tabs (Quick-filters)**: Limits rows displayed by separating staff into CNTT, QTKD, QLCLĐT, and Ngoại ngữ.
2. **Workload State Filters**: Instant toggle buttons to isolate `Overloaded` and `Idle` staff.
3. **Top 5 Chart Limiter**: The overdue project bar chart will dynamically compute and display only the **top 5 most critical projects**.
4. **Slide-over Drawer Panel**: Drilldown detail cards are housed inside a slide-over panel that opens from the right edge, keeping the primary cockpit view flat and clean.

## 4. Workload Logic Engine
- **Red Alert (Overloaded - Deadline)**: $\ge 3$ tasks overdue or urgent (due within $\le 5$ days).
- **Orange Alert (Overloaded - Volume)**: $> 8$ active tasks OR accumulated log hours $> 45\text{h/week}$ (or $> 170\text{h/month}$).
- **Yellow Alert (Overloaded - Role)**: Serving as PIC for $\ge 3$ active projects.
- **Blue Alert (Idle/Available)**: $0$ active tasks on Worklane AND average logs hours $< 2\text{h/day}$ in the selected period.
- **Green Alert (Balanced)**: All other active personnel.

## 5. Accentless Matching Engine
- To prevent mismatching between normalized accentless daily logs data (`le thanh ngoc`) and accented Worklane name strings (`Lê Thành Ngọc`), matching is executed client-side via:
  ```javascript
  function stripAccents(str) {
    if (!str) return "";
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
  }
  ```

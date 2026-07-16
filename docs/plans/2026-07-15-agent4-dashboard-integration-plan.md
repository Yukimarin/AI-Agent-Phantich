# Agent 4 Dashboard Native Tailwind Integration Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Rebuild Tab 3 (Daily Logs & Projects) directly inside the Unified Dashboard of Agent 5 using Tailwind CSS and native dynamic Chart.js visualizations for consistency and robust light/dark mode support.

**Architecture:** Load raw analysis data from `data/daily_log_analysis.json` and `data/project_data.json` in `generate_unified_dashboard.py`. Generate standard Tailwind HTML panels and dynamic JavaScript code for Chart.js, rendering everything into `5_unified_dashboard.html`.

**Tech Stack:** Python, Tailwind CSS, Chart.js, Font Awesome.

---

### Task 1: Load Raw Analysis Data
**Files:**
- Modify: `scratch/generate_unified_dashboard.py`

**Step 1: Write the load verification code**
Modify `generate_unified_dashboard.py` to load `data/daily_log_analysis.json` and `data/project_data.json` and print statistics at startup to verify raw data availability.

**Step 2: Run verification script**
Run: `uv run python scratch/generate_unified_dashboard.py`
Expected: Output showing successful reading of both JSON files with data sizes.

**Step 3: Commit**
```bash
git add scratch/generate_unified_dashboard.py
git commit -m "feat: load raw analysis and project data in generate_unified_dashboard.py"
```

---

### Task 2: Build Tailwind HTML Layout for Tab 3
**Files:**
- Modify: `scratch/generate_unified_dashboard.py`

**Step 1: Write HTML template generation code**
Build a helper function `render_tab3_html()` inside `generate_unified_dashboard.py` that outputs the Tailwind-styled layout for Tab 3 (Alert cards, Overview metrics, Weekly/Monthly sub-tabs, Project health panels, and tables).

**Step 2: Run build to test output structure**
Run: `uv run python scratch/generate_unified_dashboard.py`
Expected: `output/5_unified_dashboard.html` compiles successfully and contains the generated HTML container.

**Step 3: Commit**
```bash
git add scratch/generate_unified_dashboard.py
git commit -m "feat: build native Tailwind HTML layout for Tab 3 in generate_unified_dashboard.py"
```

---

### Task 3: Build Chart.js Script Block for Tab 3
**Files:**
- Modify: `scratch/generate_unified_dashboard.py`

**Step 1: Add JS chart initializers**
Add JavaScript initializers for `taskStatusChart` (Doughnut), `monthlyPerformanceChart` (Bar Chart with dynamic dataset filtering), and `missingLogsTrendChart` (Line Chart of missing reports) inside the template script block.

**Step 2: Run generation script**
Run: `uv run python scratch/generate_unified_dashboard.py`
Expected: Successful generation of HTML with correct Chart.js configs.

**Step 3: Commit**
```bash
git add scratch/generate_unified_dashboard.py
git commit -m "feat: integrate Chart.js configurations for Tab 3 in generate_unified_dashboard.py"
```

---

### Task 4: Integrate Interactivity and Filters
**Files:**
- Modify: `scratch/generate_unified_dashboard.py`

**Step 1: Implement filtering and sub-tab logic**
Write JS helper functions `switchTabLogs()`, `switchViewModeLogs()`, `filterGroupLogs()`, and `applyFiltersLogs()` to filter both tables and charts dynamically in Tab 3 based on user filters.

**Step 2: Compile the unified dashboard**
Run: `uv run python scratch/generate_unified_dashboard.py`
Expected: Dashboard generates with fully working interactive scripts.

**Step 3: Commit**
```bash
git add scratch/generate_unified_dashboard.py
git commit -m "feat: implement interactive search, tab-switching and filtering for Tab 3"
```

---

### Task 5: Run Full Pipeline and Verification
**Files:**
- Test: `scratch/run_pipeline.py`

**Step 1: Execute pipeline**
Run: `uv run --with mysql-connector-python --with openpyxl --with numpy --with pandas --with markdown scratch/run_pipeline.py`
Expected: Complete execution without errors, culminating in a fully rendered `output/5_unified_dashboard.html`.

**Step 2: Commit**
```bash
git commit -am "feat: verified dynamic unified dashboard with 3 Tailwind tabs"
```


---
Trở về: [[docs/knowledge_map|Bản đồ Tri thức dự án]]

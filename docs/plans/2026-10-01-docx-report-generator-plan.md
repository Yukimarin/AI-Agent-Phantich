# DOCX Report Generator Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Automate the generation of a `.docx` report by capturing screenshots from `k26_violation_dashboard.html` and injecting them into `k26_violation_analysis_report.md`.

**Architecture:** A Python script using `playwright` to render the local HTML file, wait for Chart.js, capture element screenshots, inject them into Markdown, and convert via `pypandoc`.

**Tech Stack:** Python, `playwright`, `pypandoc`

---

### Task 1: Environment Setup

**Files:**
- Create: `scratch/setup_env.ps1`

**Step 1: Write setup script**
```powershell
pip install playwright pypandoc
playwright install chromium
```

**Step 2: Run setup script**
Run: `powershell -File scratch/setup_env.ps1`
Expected: Successfully installs packages and Chromium binary.

**Step 3: Commit**
```bash
git add docs/plans/2026-10-01-docx-report-generator-plan.md
git commit -m "docs: add implementation plan for docx generator"
```

### Task 2: Implement the Screenshot Capture Logic

**Files:**
- Create: `scratch/generate_docx.py`

**Step 1: Write minimal screenshot logic**
```python
import asyncio
from playwright.async_api import async_playwright
import os

async def capture_screenshots():
    os.makedirs('temp_images', exist_ok=True)
    html_path = f"file:///{os.path.abspath('output/dashboards/management/k26_violation_dashboard.html').replace(chr(92), '/')}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(html_path)
        
        # Unhide all tab panels to make elements visible
        await page.evaluate("document.querySelectorAll('.tab-panel').forEach(el => el.classList.add('active'));")
        # Wait for Chart.js animation
        await page.wait_for_timeout(2000)
        
        # Capture elements
        await page.locator('#chart-class-severity').screenshot(path='temp_images/chart_overview.png')
        await page.locator('#chart-severity-pie').screenshot(path='temp_images/chart_pie.png')
        await page.locator('#panel-comparison .table-container').first.screenshot(path='temp_images/table_compare.png')
        await page.locator('#panel-absent .table-container').first.screenshot(path='temp_images/table_absent.png')
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(capture_screenshots())
```

**Step 2: Run capture logic**
Run: `python scratch/generate_docx.py`
Expected: Creates `temp_images/` with 4 `.png` files.

**Step 3: Commit**
```bash
git add scratch/generate_docx.py
git commit -m "feat: implement playwright screenshot capture"
```

### Task 3: Implement Markdown Injection & DOCX Generation

**Files:**
- Modify: `scratch/generate_docx.py`

**Step 1: Add injection and conversion logic**
Append to `scratch/generate_docx.py` inside a new function `generate_docx()`:
```python
import pypandoc

def generate_docx():
    # Ensure pandoc is available
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        pypandoc.download_pandoc()

    with open('output/reports/k26_violation_analysis_report.md', 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Inject images (using absolute paths or relative depending on pandoc execution context)
    md_text = md_text.replace(
        '### 1. Tỷ lệ vi phạm Môn Kỹ năng học tập chủ động (SSK101)', 
        '### 1. Tỷ lệ vi phạm Môn Kỹ năng học tập chủ động (SSK101)\n\n![Overview](temp_images/chart_overview.png)'
    )
    md_text = md_text.replace(
        '### 2. Phân loại sinh viên vi phạm',
        '### 2. Phân loại sinh viên vi phạm\n\n![Pie](temp_images/chart_pie.png)'
    )
    md_text = md_text.replace(
        '### 3. Xu hướng chuyển dịch hành vi',
        '### 3. Xu hướng chuyển dịch hành vi\n\n![Comparison](temp_images/table_compare.png)'
    )
    md_text = md_text.replace(
        '### 5. Danh sách đặc biệt',
        '### 5. Danh sách đặc biệt\n\n![Absent](temp_images/table_absent.png)'
    )

    with open('temp_images/injected_report.md', 'w', encoding='utf-8') as f:
        f.write(md_text)

    # Convert to DOCX
    pypandoc.convert_file('temp_images/injected_report.md', 'docx', outputfile='output/reports/Bao_Cao_Vi_Pham_K26.docx')
    print("DOCX successfully generated at output/reports/Bao_Cao_Vi_Pham_K26.docx")
```
Update `__main__` to call `generate_docx()` after `capture_screenshots()`.

**Step 2: Test script end-to-end**
Run: `python scratch/generate_docx.py`
Expected: Prints success message and creates `output/reports/Bao_Cao_Vi_Pham_K26.docx`.

**Step 3: Commit**
```bash
git add scratch/generate_docx.py
git commit -m "feat: inject markdown and compile docx via pypandoc"
```

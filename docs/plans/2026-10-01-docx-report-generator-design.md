# DOCX Report Generator Design

## Overview
Automate the generation of a `.docx` report containing both the detailed Markdown analysis of K26 violations and screenshots of the corresponding dynamic charts and tables from the HTML dashboard.

## Requirements
- Output: A beautifully formatted `.docx` file.
- Input: `k26_violation_analysis_report.md` (text content) and `k26_violation_dashboard.html` (visual data).
- Process must be fully automated via a Python script.

## Technical Architecture

### 1. Environment & Dependencies
- **Playwright (Python)**: Used to launch a headless browser, wait for Chart.js rendering and animations to complete, and capture high-quality screenshots of specific DOM elements.
- **Pypandoc**: A Python wrapper for `pandoc` to convert the injected Markdown into a native Word document (`.docx`).

### 2. Screenshot Strategy & Element Mapping
The script will manipulate the DOM before screenshotting to ensure all tabs are visible (removing `display: none` from `.tab-panel`).
- **Overview Tab**: 
  - Class Distribution Chart (`#chart-class-severity`) -> Captured for "Thực trạng" section.
  - Severity Pie Chart (`#chart-severity-pie`) -> Captured for "Phân nhóm" section.
  - Comparison Trend (`#chart-comparison`) -> Captured for "Chuyển biến" section.
- **Absent Tab**:
  - Never Attended Table -> Captured for "Danh sách đặc biệt" section.

### 3. Execution Pipeline
1. **Setup**: Create a temporary directory `temp_images/` for screenshots.
2. **Capture**: Run Playwright to open `k26_violation_dashboard.html`, execute JS to unhide all panels, wait for canvases to render, and save screenshots of target elements.
3. **Inject**: Read `k26_violation_analysis_report.md`. Use string replacement to inject Markdown image tags (`![Image](temp_images/...)`) immediately after their corresponding headers.
4. **Compile**: Save the combined text to a temporary `.md` file, then invoke `pypandoc.convert_file(..., to='docx')` to produce the final `.docx` report.
5. **Cleanup**: Remove `temp_images/` and the temporary `.md` file.

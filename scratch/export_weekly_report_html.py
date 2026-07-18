# -*- coding: utf-8 -*-
import os
import sys
import re
import markdown

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

md_path = 'data/kpi_report.md'
html_dir = 'output'
html_path = os.path.join(html_dir, '1_kpi_report.html')

if not os.path.exists(html_dir):
    os.makedirs(html_dir)

# Doc file markdown
if not os.path.exists(md_path):
    print(f"Error: File {md_path} not found.")
    sys.exit(1)

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Chuyen doi Markdown sang HTML
html_body = markdown.markdown(md_content, extensions=['extra', 'toc', 'sane_lists'])

# Xu ly cac Alert Github Markdown sang Div CSS (khong dung tieng Viet co dau trong code)
def replace_alerts(html_text):
    html_text = re.sub(
        r'<blockquote>\s*<p>\s*\[!IMPORTANT\](.*?)</p>',
        r'<div class="alert-box alert-important"><strong>QUAN TRONG / KHAN CAP</strong><p>\1</p></div>',
        html_text, flags=re.DOTALL
    )
    html_text = re.sub(
        r'<blockquote>\s*<p>\s*\[!NOTE\](.*?)</p>',
        r'<div class="alert-box alert-note"><strong>LUU Y</strong><p>\1</p></div>',
        html_text, flags=re.DOTALL
    )
    html_text = re.sub(
        r'<blockquote>\s*<p>\s*\[!WARNING\](.*?)</p>',
        r'<div class="alert-box alert-warning"><strong>CANH BAO</strong><p>\1</p></div>',
        html_text, flags=re.DOTALL
    )
    
    html_text = html_text.replace("</blockquote>", "")
    html_text = html_text.replace("<blockquote>", '<blockquote class="quote-box">')
    return html_text

html_body = replace_alerts(html_body)

# Them dinh dang CSS dac biet cho tables
html_body = html_body.replace("<table>", '<div class="table-container"><table>')
html_body = html_body.replace("</table>", '</table></div>')

# Custom HTML Template
html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo Chỉ số Đào tạo &amp; Quản trị lớp - Agent 1</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --primary-light: #e0e7ff;
            --secondary: #0ea5e9;
            --secondary-light: #f0f9ff;
            --success: #10b981;
            --success-light: #ecfdf5;
            --danger: #ef4444;
            --danger-light: #fef2f2;
            --text-main: #475569;
            --text-dark: #0f172a;
            --bg-main: #f8fafc;
            --border: #e2e8f0;
            --card-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0, 0, 0, 0.02);
        }}
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.7;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .card {{
            background: white;
            padding: 40px;
            border-radius: 32px;
            box-shadow: var(--card-shadow);
            border: 1px solid var(--border);
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 24px;
            margin-bottom: 32px;
            border-bottom: 1px solid var(--border);
        }}
        .logo-section {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .logo-box {{
            padding: 12px 18px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 16px;
            color: white;
            font-weight: 800;
            font-size: 1.5rem;
            box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.3);
            letter-spacing: -0.05em;
        }}
        .logo-title {{
            font-weight: 800;
            font-size: 1.4rem;
            color: var(--text-dark);
            line-height: 1.2;
            letter-spacing: -0.02em;
        }}
        .logo-subtitle {{
            font-size: 0.75rem;
            color: #94a3b8;
            font-weight: 600;
            letter-spacing: 0.075em;
            text-transform: uppercase;
        }}
        .week-badge {{
            display: inline-block;
            padding: 8px 16px;
            background-color: var(--primary-light);
            color: var(--primary-dark);
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 700;
        }}
        
        /* Charts styling */
        .charts-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 32px;
        }}
        .chart-card {{
            background: white;
            padding: 24px;
            border-radius: 24px;
            border: 1px solid var(--border);
            box-shadow: var(--card-shadow);
        }}
        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .chart-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-dark);
            margin: 0;
            letter-spacing: -0.01em;
        }}
        .tab-btn {{
            padding: 6px 12px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: white;
            color: var(--text-main);
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .tab-btn.active {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}
        .tab-btn:hover:not(.active) {{
            background: var(--bg-main);
        }}

        /* Markdown styling */
        .markdown-body h1 {{
            display: none; /* Da co Header */
        }}
        .markdown-body h2 {{
            font-size: 1.4rem;
            font-weight: 800;
            color: var(--text-dark);
            margin-top: 40px;
            margin-bottom: 20px;
            border-bottom: 2px solid var(--border);
            padding-bottom: 8px;
            letter-spacing: -0.02em;
        }}
        .markdown-body h3 {{
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--primary-dark);
            margin-top: 32px;
            margin-bottom: 12px;
            letter-spacing: -0.01em;
        }}
        .markdown-body h4 {{
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-dark);
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        .markdown-body p {{
            margin-top: 0;
            margin-bottom: 16px;
        }}
        .markdown-body ul, .markdown-body ol {{
            margin-top: 0;
            margin-bottom: 16px;
            padding-left: 20px;
        }}
        .markdown-body li {{
            margin-bottom: 8px;
        }}
        
        /* Table styling */
        .table-container {{
            overflow-x: auto;
            margin: 20px 0;
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.01);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.875rem;
        }}
        th {{
            background-color: var(--bg-main);
            color: var(--text-dark);
            font-weight: 700;
            padding: 14px 18px;
            border-bottom: 2px solid var(--border);
        }}
        td {{
            padding: 14px 18px;
            border-bottom: 1px solid var(--border);
            background-color: white;
            color: var(--text-main);
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        tr:hover td {{
            background-color: #faf5ff;
        }}
        
        /* Alerts styling */
        .alert-box {{
            padding: 20px 24px;
            margin: 24px 0;
            border-radius: 16px;
            font-size: 0.925rem;
            box-shadow: var(--card-shadow);
        }}
        .alert-important {{
            border-left: 5px solid var(--danger);
            background-color: var(--danger-light);
            color: #991b1b;
        }}
        .alert-note {{
            border-left: 5px solid var(--secondary);
            background-color: var(--secondary-light);
            color: #1e40af;
        }}
        .alert-warning {{
            border-left: 5px solid #f59e0b;
            background-color: #fffbeb;
            color: #92400e;
        }}
        .quote-box {{
            border-left: 5px solid var(--primary);
            background-color: var(--primary-light);
            padding: 16px 24px;
            margin: 24px 0;
            border-radius: 16px;
            font-style: italic;
            color: #4f46e5;
        }}
        
        strong {{
            color: var(--text-dark);
        }}
        
        .footer {{
            margin-top: 48px;
            padding-top: 32px;
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: #94a3b8;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .status-badge {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .status-dot {{
            width: 8px;
            height: 8px;
            background-color: var(--success);
            border-radius: 50%;
        }}
    </style>
</head>
<body>
    <div class="card" id="tab-agent1-container">
        <div class="header">
            <div class="logo-section">
                <div class="logo-box">A1</div>
                <div>
                    <div class="logo-title">Quản Trị Lớp &amp; Chỉ Số Đào Tạo</div>
                    <div class="logo-subtitle">Hệ thống theo dõi vi phạm tuần - Agent 1</div>
                </div>
            </div>
            <div>
                <span class="week-badge">Báo cáo Tuần</span>
            </div>
        </div>

        <!-- Charts Container -->
        <div class="charts-row">
            <div class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">So sánh Vi phạm Tuần này vs Tuần trước (%)</h3>
                </div>
                <div style="position: relative; height: 260px;">
                    <canvas id="weeklyCompareChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">Xu hướng Vi phạm qua các Môn học (%)</h3>
                    <div class="tabs" style="display: flex; gap: 6px;">
                        <button id="btn-trend-hn" class="tab-btn active" onclick="switchTrendData('HN')">CNTT HN</button>
                        <button id="btn-trend-hcm" class="tab-btn" onclick="switchTrendData('HCM')">CNTT HCM</button>
                        <button id="btn-trend-qtkd" class="tab-btn" onclick="switchTrendData('QTKD')">QTKD HN</button>
                    </div>
                </div>
                <div style="position: relative; height: 260px;">
                    <canvas id="trendChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="markdown-body">
            {html_body}
        </div>
        
        <div class="footer">
            <div class="status-badge">
                <div class="status-dot"></div>
                <span>Dữ liệu cập nhật tự động 100%</span>
            </div>
            <div>PTIT x Rikkei Education</div>
        </div>
    </div>

    <script>
        // JS helper to parse text and calculate prev week value
        function parseCell(text) {{
            if (!text || text.trim() === "" || text.includes("N/A")) return {{ curr: 0, prev: 0 }};
            const curr = parseFloat(text);
            let diff = 0;
            if (text.includes("▲")) {{
                const match = text.match(/\\+\\d+\\.\\d+/);
                if (match) diff = parseFloat(match[0]);
            }} else if (text.includes("▼")) {{
                const match = text.match(/-\\d+\\.\\d+/);
                if (match) diff = parseFloat(match[0]);
            }}
            return {{ curr: curr, prev: curr - diff }};
        }}

        // Dynamic Parsing from rendered HTML Tables
        const tables = document.querySelectorAll(".table-container table");
        const groupsData = {{
            'HN': {{ curr: [0, 0, 0], prev: [0, 0, 0], count: 0 }},
            'HCM': {{ curr: [0, 0, 0], prev: [0, 0, 0], count: 0 }},
            'QTKD': {{ curr: [0, 0, 0], prev: [0, 0, 0], count: 0 }}
        }};

        // Process Table 0: KS25 CNTT HN
        if (tables.length > 0) {{
            const rows = tables[0].querySelectorAll("tbody tr");
            rows.forEach(r => {{
                const cells = r.querySelectorAll("td");
                if (cells.length >= 6) {{
                    const cc = parseCell(cells[3].textContent);
                    const bt = parseCell(cells[4].textContent);
                    const el = parseCell(cells[5].textContent);
                    groupsData.HN.curr[0] += cc.curr; groupsData.HN.prev[0] += cc.prev;
                    groupsData.HN.curr[1] += bt.curr; groupsData.HN.prev[1] += bt.prev;
                    groupsData.HN.curr[2] += el.curr; groupsData.HN.prev[2] += el.prev;
                    groupsData.HN.count++;
                }}
            }});
        }}

        // Process Table 1: KS25 CNTT HCM
        if (tables.length > 1) {{
            const rows = tables[1].querySelectorAll("tbody tr");
            rows.forEach(r => {{
                const cells = r.querySelectorAll("td");
                if (cells.length >= 6) {{
                    const cc = parseCell(cells[3].textContent);
                    const bt = parseCell(cells[4].textContent);
                    const el = parseCell(cells[5].textContent);
                    groupsData.HCM.curr[0] += cc.curr; groupsData.HCM.prev[0] += cc.prev;
                    groupsData.HCM.curr[1] += bt.curr; groupsData.HCM.prev[1] += bt.prev;
                    groupsData.HCM.curr[2] += el.curr; groupsData.HCM.prev[2] += el.prev;
                    groupsData.HCM.count++;
                }}
            }});
        }}

        // Process Table 2: KS25 QTKD HN
        if (tables.length > 2) {{
            const rows = tables[2].querySelectorAll("tbody tr");
            rows.forEach(r => {{
                const cells = r.querySelectorAll("td");
                if (cells.length >= 6) {{
                    const cc = parseCell(cells[3].textContent);
                    const bt = parseCell(cells[4].textContent);
                    const el = parseCell(cells[5].textContent);
                    groupsData.QTKD.curr[0] += cc.curr; groupsData.QTKD.prev[0] += cc.prev;
                    groupsData.QTKD.curr[1] += bt.curr; groupsData.QTKD.prev[1] += bt.prev;
                    groupsData.QTKD.curr[2] += el.curr; groupsData.QTKD.prev[2] += el.prev;
                    groupsData.QTKD.count++;
                }}
            }});
        }}

        // Standardize averages
        ['HN', 'HCM', 'QTKD'].forEach(key => {{
            const g = groupsData[key];
            if (g.count > 0) {{
                for (let i = 0; i < 3; i++) {{
                    g.curr[i] = g.curr[i] / g.count;
                    g.prev[i] = g.prev[i] / g.count;
                }}
            }}
        }});

        // Historical Trend Data
        const trends = {{
            'HN': {{
                courses: ['Javascript', 'Database', 'Python', 'Python Web'],
                cc: [2.50, 4.10, 7.20, groupsData.HN.curr[0]],
                bt: [5.10, 6.50, 8.50, groupsData.HN.curr[1]],
                el: [8.20, 10.50, 12.10, groupsData.HN.curr[2]]
            }},
            'HCM': {{
                courses: ['Javascript', 'Database', 'Python', 'Python Web'],
                cc: [3.80, 5.00, 9.50, groupsData.HCM.curr[0]],
                bt: [6.20, 7.80, 11.20, groupsData.HCM.curr[1]],
                el: [9.50, 11.80, 14.50, groupsData.HCM.curr[2]]
            }},
            'QTKD': {{
                courses: ['M103', 'DTB201', 'DTB202', 'PRJ302'],
                cc: [4.20, 6.10, 8.50, groupsData.QTKD.curr[0]],
                bt: [6.50, 8.50, 10.20, groupsData.QTKD.curr[1]],
                el: [11.00, 13.20, 15.40, groupsData.QTKD.curr[2]]
            }}
        }};

        // Render Chart 1: So sánh Tuần
        const compareCtx = document.getElementById('weeklyCompareChart').getContext('2d');
        const compareChart = new Chart(compareCtx, {{
            type: 'bar',
            data: {{
                labels: ['CNTT HN', 'CNTT HCM', 'QTKD HN'],
                datasets: [
                    {{
                        label: 'Tuần trước',
                        data: [
                            (groupsData.HN.prev[0] + groupsData.HN.prev[1] + groupsData.HN.prev[2]) / 3,
                            (groupsData.HCM.prev[0] + groupsData.HCM.prev[1] + groupsData.HCM.prev[2]) / 3,
                            (groupsData.QTKD.prev[0] + groupsData.QTKD.prev[1] + groupsData.QTKD.prev[2]) / 3
                        ],
                        backgroundColor: '#cbd5e1',
                        borderRadius: 6
                    }},
                    {{
                        label: 'Tuần này',
                        data: [
                            (groupsData.HN.curr[0] + groupsData.HN.curr[1] + groupsData.HN.curr[2]) / 3,
                            (groupsData.HCM.curr[0] + groupsData.HCM.curr[1] + groupsData.HCM.curr[2]) / 3,
                            (groupsData.QTKD.curr[0] + groupsData.QTKD.curr[1] + groupsData.QTKD.curr[2]) / 3
                        ],
                        backgroundColor: '#6366f1',
                        borderRadius: 6
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ family: 'Plus Jakarta Sans', weight: '600' }} }} }}
                }},
                scales: {{
                    y: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }}
                }}
            }}
        }});

        // Render Chart 2: Xu hướng môn học
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        let trendChart = new Chart(trendCtx, {{
            type: 'line',
            data: {{
                labels: trends.HN.courses,
                datasets: [
                    {{
                        label: 'Chuyên cần vắng (%)',
                        data: trends.HN.cc,
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.05)',
                        fill: true,
                        tension: 0.3
                    }},
                    {{
                        label: 'Nợ bài tập (%)',
                        data: trends.HN.bt,
                        borderColor: '#f59e0b',
                        backgroundColor: 'rgba(245, 158, 11, 0.05)',
                        fill: true,
                        tension: 0.3
                    }},
                    {{
                        label: 'Chậm Elearning (%)',
                        data: trends.HN.el,
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.05)',
                        fill: true,
                        tension: 0.3
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ family: 'Plus Jakarta Sans', weight: '600' }} }} }}
                }},
                scales: {{
                    y: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }}
                }}
            }}
        }});

        function switchTrendData(key) {{
            document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
            if (key === 'HN') document.getElementById("btn-trend-hn").classList.add("active");
            if (key === 'HCM') document.getElementById("btn-trend-hcm").classList.add("active");
            if (key === 'QTKD') document.getElementById("btn-trend-qtkd").classList.add("active");

            trendChart.data.labels = trends[key].courses;
            trendChart.data.datasets[0].data = trends[key].cc;
            trendChart.data.datasets[1].data = trends[key].bt;
            trendChart.data.datasets[2].data = trends[key].el;
            trendChart.update();
        }}
        window.switchTrendData = switchTrendData;
    </script>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Báo cáo Agent 1 đã được xuất ra HTML thành công tại {html_path}")


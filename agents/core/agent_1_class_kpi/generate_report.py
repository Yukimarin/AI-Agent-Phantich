import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import markdown
import re

with open("output/reports/core/agent_1_student_discipline.md", "r", encoding="utf-8") as f:
    md_content = f.read()

with open("data/processed/historical_trends.json", "r", encoding="utf-8") as f:
    trends_json = f.read()

html_body = markdown.markdown(md_content, extensions=['extra', 'toc', 'sane_lists'])

def replace_alerts(html_text):
    html_text = re.sub(
        r'<blockquote>\s*<p>\s*\[!IMPORTANT\](?:</p>)?(.*?)</blockqu' + 'ote>',
        r'<div class="alert-box alert-important"><strong>Ghi chú:</strong>\1</div>',
        html_text, flags=re.DOTALL
    )
    html_text = re.sub(
        r'<blockquote>\s*<p>\s*\[!NOTE\](?:</p>)?(.*?)</blockqu' + 'ote>',
        r'<div class="alert-box alert-note"><strong>LƯU Ý</strong>\1</div>',
        html_text, flags=re.DOTALL
    )
    html_text = re.sub(
        r'<blockquote>\s*<p>\s*\[!WARNING\](?:</p>)?(.*?)</blockqu' + 'ote>',
        r'<div class="alert-box alert-warning"><strong>CẢNH BÁO</strong>\1</div>',
        html_text, flags=re.DOTALL
    )
    
    html_text = html_text.replace("<blockquote>", '<blockquote class="quote-box">')
    return html_text

html_body = replace_alerts(html_body)

html_body = html_body.replace("<table>", '<div class="table-container"><table>')
html_body = html_body.replace("</table>", '</table></div>')

html_template = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo Chỉ số Đào tạo &amp; Quản trị lớp - Agent 1</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            mermaid.initialize({{ startOnLoad: false, theme: 'dark' }});
            document.querySelectorAll("code.language-mermaid").forEach(function(block) {{
                let div = document.createElement("div");
                div.className = "mermaid";
                div.textContent = block.textContent;
                block.parentNode.replaceWith(div);
            }});
            mermaid.init(undefined, document.querySelectorAll(".mermaid"));
        }});
    </script>
    <style>
        :root {{
            --bg-main: #0f172a; --bg-card: #1e293b; --bg-elevated: #334155;
            --text-main: #f8fafc; --text-muted: #94a3b8;
            --primary: #3b82f6; --success: #10b981; --warning: #f59e0b; --danger: #ef4444; --info: #0ea5e9;
            --border: rgba(255,255,255,0.08);
            --font-family: 'Plus Jakarta Sans', sans-serif;
            --card-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.3), 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: var(--font-family); }}
        body {{
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.7;
            padding: 40px 20px;
            font-size: 14px;
        }}
        .container {{ max-width: 1440px; margin: 0 auto; }}
        
        .card {{
            background: var(--bg-card);
            padding: 40px;
            border-radius: 24px;
            box-shadow: var(--card-shadow);
            border: 1px solid var(--border);
        }}
        header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 24px;
            margin-bottom: 32px;
            border-bottom: 1px solid var(--border);
        }}
        h1 {{ font-size: 1.6rem; font-weight: 700; display: flex; align-items: center; gap: 12px; margin-bottom: 4px; }}
        .meta {{ color: var(--text-muted); font-size: 0.9rem; }}
        .week-badge {{
            display: inline-block;
            padding: 8px 16px;
            background-color: rgba(59, 130, 246, 0.15);
            color: var(--primary);
            border: 1px solid var(--primary);
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
            background: var(--bg-card);
            padding: 24px;
            border-radius: 16px;
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
            color: var(--text-main);
            margin: 0;
            display: flex; align-items: center; gap: 8px;
        }}
        .tab-btn {{
            padding: 6px 12px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--bg-elevated);
            color: var(--text-muted);
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
            background: rgba(255,255,255,0.1);
        }}

        /* Markdown styling */
        .markdown-body h1 {{
            display: none;
        }}
        .markdown-body h2 {{
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text-main);
            margin-top: 40px;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 8px;
            display: flex; align-items: center; gap: 10px;
        }}
        .markdown-body h3 {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--info);
            margin-top: 32px;
            margin-bottom: 12px;
        }}
        .markdown-body h4 {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-main);
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        /* Table styling */
        .table-container {{
            overflow-x: auto;
            margin: 20px 0;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: var(--bg-card);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.85rem;
        }}
        th {{
            background: rgba(0,0,0,0.2);
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            padding: 14px 18px;
            border-bottom: 1px solid var(--border);
        }}
        td {{
            padding: 14px 18px;
            border-bottom: 1px solid var(--border);
            color: var(--text-main);
        }}
        tr:hover td {{
            background-color: rgba(255,255,255,0.02);
        }}
        
        /* Alerts styling */
        .alert-box {{
            padding: 16px 20px;
            margin: 24px 0;
            border-radius: 12px;
            font-size: 0.9rem;
        }}
        .alert-important {{
            border-left: 4px solid var(--danger);
            background-color: rgba(239, 68, 68, 0.1);
            color: #fca5a5;
        }}
        .alert-important strong {{ color: var(--danger); }}
        .alert-note {{
            border-left: 4px solid var(--info);
            background-color: rgba(14, 165, 233, 0.1);
            color: #7dd3fc;
        }}
        .alert-note strong {{ color: var(--info); }}
        .alert-warning {{
            border-left: 4px solid var(--warning);
            background-color: rgba(245, 158, 11, 0.1);
            color: #fcd34d;
        }}
        .alert-warning strong {{ color: var(--warning); }}
        
        .quote-box {{
            border-left: 4px solid var(--primary);
            background-color: rgba(59, 130, 246, 0.1);
            padding: 16px 24px;
            margin: 24px 0;
            border-radius: 12px;
            font-style: italic;
            color: #93c5fd;
        }}
        
        .staff-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .staff-card {{
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 16px;
            transition: all 0.3s ease;
        }}
        .staff-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            border-color: rgba(255,255,255,0.2);
        }}
        
        .footer {{
            margin-top: 48px;
            padding-top: 32px;
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: var(--text-muted);
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
            box-shadow: 0 0 8px var(--success);
        }}
        
        /* Code blocks */
        pre {{
            background: var(--bg-elevated);
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid var(--border);
        }}
        code {{
            font-family: monospace;
            background: var(--bg-elevated);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.85em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card" id="tab-agent1-container">
            <header>
                <div>
                    <h1><i class="fas fa-chart-line" style="color: var(--primary)"></i> Quản Trị Lớp &amp; Chỉ Số Đào Tạo</h1>
                    <div class="meta">Hệ thống theo dõi vi phạm tuần - Agent 1</div>
                </div>
                <div>
                    <span class="week-badge"><i class="fas fa-calendar-alt"></i> Báo cáo Tuần</span>
                </div>
            </header>

            <!-- Charts Container -->
            <div class="charts-row">
                <div class="chart-card">
                    <div class="chart-header">
                        <h3 class="chart-title"><i class="fas fa-balance-scale"></i> So sánh Vi phạm Tuần này vs Tuần trước (%)</h3>
                        <div class="tabs" style="display: flex; gap: 6px;">
                            <button id="btn-compare-hn" class="tab-btn active" onclick="switchCompareData('HN')">CNTT HN (Python Web)</button>
                            <button id="btn-compare-hcm" class="tab-btn" onclick="switchCompareData('HCM')">CNTT HCM (Python Web)</button>
                            <button id="btn-compare-qtkd" class="tab-btn" onclick="switchCompareData('QTKD')">QTKD HN (PRJ302)</button>
                        </div>
                    </div>
                    <div style="position: relative; height: 260px;">
                        <canvas id="weeklyCompareChart"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <h3 class="chart-title"><i class="fas fa-chart-area"></i> Xu hướng Vi phạm qua các Môn học (%)</h3>
                        <div class="tabs" style="display: flex; gap: 6px;">
                            <button id="btn-trend-ks24_hn" class="tab-btn" onclick="switchTrendData('KS24_HN')">CNTT HN (KS24)</button>
                            <button id="btn-trend-hn" class="tab-btn active" onclick="switchTrendData('HN')">CNTT HN (KS25)</button>
                            <button id="btn-trend-hcm" class="tab-btn" onclick="switchTrendData('HCM')">CNTT HCM (KS25)</button>
                            <button id="btn-trend-qtkd" class="tab-btn" onclick="switchTrendData('QTKD')">QTKD HN (KS25)</button>
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
    </div>

    <script>
        const trends = {trends_json};

        // Set Chart.js defaults for dark mode
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';

        const compareCtx = document.getElementById('weeklyCompareChart').getContext('2d');
        let compareChart = new Chart(compareCtx, {{
            type: 'bar',
            data: {{
                labels: ['Vắng Chuyên Cần', 'Nợ Bài Tập', 'Chậm Elearning'],
                datasets: [
                    {{
                        label: 'Tuần trước',
                        data: trends.compare.HN.prev,
                        backgroundColor: '#334155',
                        borderRadius: 6
                    }},
                    {{
                        label: 'Tuần này',
                        data: trends.compare.HN.curr,
                        backgroundColor: '#3b82f6',
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
                    y: {{ beginAtZero: true }}
                }}
            }}
        }});

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
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        fill: true,
                        tension: 0.3,
                        pointBackgroundColor: '#1e293b',
                        pointBorderColor: '#ef4444',
                        pointBorderWidth: 2
                    }},
                    {{
                        label: 'Nợ bài tập (%)',
                        data: trends.HN.bt,
                        borderColor: '#f59e0b',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        fill: true,
                        tension: 0.3,
                        pointBackgroundColor: '#1e293b',
                        pointBorderColor: '#f59e0b',
                        pointBorderWidth: 2
                    }},
                    {{
                        label: 'Chậm Elearning (%)',
                        data: trends.HN.el,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.3,
                        pointBackgroundColor: '#1e293b',
                        pointBorderColor: '#3b82f6',
                        pointBorderWidth: 2
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
                    y: {{ beginAtZero: true }}
                }}
            }}
        }});

        function switchTrendData(region) {{
            document.querySelectorAll('#trendChart').forEach(e => e.parentElement.parentElement.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active')));
            document.getElementById('btn-trend-' + region.toLowerCase()).classList.add('active');
            
            trendChart.data.labels = trends[region].courses;
            trendChart.data.datasets[0].data = trends[region].cc;
            trendChart.data.datasets[1].data = trends[region].bt;
            trendChart.data.datasets[2].data = trends[region].el;
            trendChart.update();
        }}
        
        function switchCompareData(region) {{
            document.querySelectorAll('#weeklyCompareChart').forEach(e => e.parentElement.parentElement.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active')));
            document.getElementById('btn-compare-' + region.toLowerCase()).classList.add('active');
            
            compareChart.data.datasets[0].data = trends.compare[region].prev;
            compareChart.data.datasets[1].data = trends.compare[region].curr;
            compareChart.update();
        }}
        window.switchTrendData = switchTrendData;
        window.switchCompareData = switchCompareData;
        
        // Add font-awesome icons to standard markdown headers
        document.querySelectorAll('.markdown-body h2').forEach(h2 => {{
            if (h2.textContent.includes('THỐNG KÊ XU HƯỚNG')) {{
                h2.innerHTML = '<i class="fas fa-history" style="color: var(--primary)"></i> ' + h2.innerHTML;
            }} else if (h2.textContent.includes('THỐNG KÊ CHỈ SỐ VI PHẠM')) {{
                h2.innerHTML = '<i class="fas fa-exclamation-triangle" style="color: var(--warning)"></i> ' + h2.innerHTML;
            }} else if (h2.textContent.includes('ĐÁNH GIÁ NĂNG LỰC')) {{
                h2.innerHTML = '<i class="fas fa-medal" style="color: var(--success)"></i> ' + h2.innerHTML;
            }} else if (h2.textContent.includes('ĐÁNH GIÁ CHI TIẾT')) {{
                h2.innerHTML = '<i class="fas fa-user-check" style="color: var(--info)"></i> ' + h2.innerHTML;
            }}
        }});
    </script>
</body>
</html>
"""

final_html = html_template.format(html_body=html_body, trends_json=trends_json)

os.makedirs("output/dashboards/core", exist_ok=True)
with open("output/dashboards/core/agent_1_student_discipline.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Agent 1: Báo cáo đã được xuất ra HTML thành công tại output/dashboards/core/agent_1_student_discipline.html")

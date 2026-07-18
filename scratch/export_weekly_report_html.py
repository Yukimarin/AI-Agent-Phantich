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
    <title>Bao cao Chi so Dao tao &amp; Quan tri lop - Agent 1</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #7c3aed;
            --primary-light: #f5f3ff;
            --secondary: #3b82f6;
            --secondary-light: #eff6ff;
            --text-main: #334155;
            --text-dark: #0f172a;
            --bg-main: #f8fafc;
            --border: #e2e8f0;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.625;
            padding: 40px 20px;
            max-width: 1100px;
            margin: 0 auto;
        }}
        .card {{
            background: white;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.02);
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
            padding: 12px 16px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 12px;
            color: white;
            font-weight: 800;
            font-size: 1.25rem;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
        }}
        .logo-title {{
            font-weight: 800;
            font-size: 1.25rem;
            color: var(--text-dark);
            line-height: 1.2;
        }}
        .logo-subtitle {{
            font-size: 0.7rem;
            color: #94a3b8;
            font-weight: 600;
            letter-spacing: 0.05em;
        }}
        .week-badge {{
            display: inline-block;
            padding: 6px 14px;
            background-color: var(--primary-light);
            color: var(--primary);
            border: 1px solid #ddd6fe;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        /* Markdown styling */
        .markdown-body h1 {{
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--text-dark);
            margin-top: 32px;
            margin-bottom: 24px;
            background: linear-gradient(135deg, #1e1b4b, var(--primary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            border-bottom: 2px solid var(--border);
            padding-bottom: 12px;
        }}
        .markdown-body h2 {{
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-dark);
            margin-top: 32px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .markdown-body h3 {{
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--primary);
            margin-top: 24px;
            margin-bottom: 12px;
        }}
        .markdown-body h4 {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-dark);
            margin-top: 16px;
            margin-bottom: 8px;
        }}
        .markdown-body p {{
            margin-top: 0;
            margin-bottom: 16px;
        }}
        .markdown-body ul, .markdown-body ol {{
            margin-top: 0;
            margin-bottom: 16px;
            padding-left: 24px;
        }}
        .markdown-body li {{
            margin-bottom: 6px;
        }}
        
        /* Table styling */
        .table-container {{
            overflow-x: auto;
            margin: 24px 0;
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.01);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}
        th {{
            background: linear-gradient(to right, var(--primary), #6d28d9);
            color: white;
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 14px 16px;
        }}
        td {{
            padding: 12px 16px;
            font-size: 0.9rem;
            border-bottom: 1px solid var(--border);
            background-color: white;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        tr:hover td {{
            background-color: #fcfbfe;
        }}
        
        /* Alerts styling */
        .alert-box {{
            padding: 18px 24px;
            margin: 24px 0;
            border-radius: 0 12px 12px 0;
            font-size: 0.925rem;
        }}
        .alert-important {{
            border-left: 4px solid #ef4444;
            background-color: #fef2f2;
            color: #991b1b;
        }}
        .alert-note {{
            border-left: 4px solid var(--secondary);
            background-color: var(--secondary-light);
            color: #1e40af;
        }}
        .alert-warning {{
            border-left: 4px solid #f59e0b;
            background-color: #fffbeb;
            color: #92400e;
        }}
        .quote-box {{
            border-left: 4px solid var(--primary);
            background-color: var(--primary-light);
            padding: 14px 20px;
            margin: 24px 0;
            border-radius: 0 12px 12px 0;
            font-style: italic;
            color: #5b21b6;
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
            font-size: 0.75rem;
            font-weight: 500;
        }}
        .status-badge {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .status-dot {{
            width: 6px;
            height: 6px;
            background-color: #22c55e;
            border-radius: 50%;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="logo-section">
                <div class="logo-box">A1</div>
                <div>
                    <div class="logo-title">Quan Tri Lop &amp; Chi So Dao Tao</div>
                    <div class="logo-subtitle">HE THONG THEO DOI VI PHAC TUAN - AGENT 1</div>
                </div>
            </div>
            <div>
                <span class="week-badge">Bao cao Tuan</span>
            </div>
        </div>
        
        <div class="markdown-body">
            {html_body}
        </div>
        
        <div class="footer">
            <div class="status-badge">
                <div class="status-dot"></div>
                <span>Du lieu cap nhat tu dong 100%</span>
            </div>
            <div>PTITxRikkei Joint Venture</div>
        </div>
    </div>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Bao cao Agent 1 da duoc xuat ra HTML thanh cong tai {html_path}")

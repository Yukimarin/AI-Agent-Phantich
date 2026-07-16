import markdown
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

md_path = 'data/student_risk_report.md'
html_path = 'output/student_risk_report.html'

if not os.path.exists(md_path):
    print(f"Error: {md_path} not found.")
    sys.exit(1)

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

html_body = markdown.markdown(md_content)

full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo Chi tiết Sinh viên có nguy cơ trượt môn (Từng lớp)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
            color: #334155;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
            line-height: 1.6;
        }}
        .card {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);
            border: 1px solid #e2e8f0;
        }}
        h1 {{
            color: #0f172a;
            font-size: 1.75rem;
            font-weight: 800;
            border-bottom: 2px solid #7c3aed;
            padding-bottom: 12px;
            margin-bottom: 24px;
        }}
        h2 {{
            color: #0f172a;
            font-size: 1.25rem;
            font-weight: 700;
            margin-top: 32px;
            margin-bottom: 16px;
        }}
        h3 {{
            color: #7c3aed;
            font-size: 1.1rem;
            font-weight: 700;
            margin-top: 24px;
            margin-bottom: 12px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
            font-size: 0.85rem;
        }}
        th {{
            background-color: #f1f5f9;
            color: #475569;
            font-weight: 700;
            padding: 12px 16px;
            border-bottom: 1px solid #e2e8f0;
            text-align: left;
        }}
        td {{
            padding: 12px 16px;
            border-bottom: 1px solid #e2e8f0;
            background-color: white;
        }}
        tr:hover td {{
            background-color: #f8fafc;
        }}
        strong {{
            color: #0f172a;
        }}
        hr {{
            border: 0;
            border-top: 1px solid #e2e8f0;
            margin: 32px 0;
        }}
    </style>
</head>
<body>
    <div class="card">
        {html_body}
    </div>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Generated standalone risk HTML at {html_path}")

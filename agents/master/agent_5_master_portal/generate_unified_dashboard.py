import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def extract_body_style_and_js(filepath, prefix=""):
    if not os.path.exists(filepath):
        print(f"Warning: File {filepath} không tồn tại để trích xuất.")
        return "", "", ""
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Trích xuất nội dung bên trong body
    body_match = re.search(r"<body[^>]*?>(.*?)</body>", content, re.DOTALL | re.IGNORECASE)
    body_html = body_match.group(1) if body_match else ""
    
    # Loại bỏ thẻ script khỏi body_html để tránh thực thi đúp
    body_html = re.sub(r"<script[^>]*?>.*?</script>", "", body_html, flags=re.DOTALL | re.IGNORECASE)
    
    # Trích xuất styles
    style_matches = re.findall(r"<style[^>]*?>(.*?)</style>", content, re.DOTALL | re.IGNORECASE)
    combined_style = "\n".join(style_matches)
    
    # Cô lập CSS bằng prefix để tránh xung đột dùng CSS nesting
    if prefix and combined_style:
        # Thay thế :root, html, body bằng & để giữ phạm vi cục bộ của các biến CSS và style chung
        combined_style = combined_style.replace(':root', '&')
        combined_style = combined_style.replace('html', '&')
        combined_style = combined_style.replace('body', '&')
        # Bao bọc toàn bộ CSS bằng prefix selector để cô lập hoàn toàn
        combined_style = f"{prefix} {{\n{combined_style}\n}}"
            
    # Trích xuất các script độc lập
    script_matches = re.findall(r"<script[^>]*?>(.*?)</script>", content, re.DOTALL | re.IGNORECASE)
    scripts = []
    for s in script_matches:
        s_strip = s.strip()
        # Bỏ qua các script trống hoặc cấu hình Tailwind CDN
        if s_strip and "tailwind.config" not in s_strip:
            # Tự động kích hoạt onload nếu đã load xong DOM (phục vụ môi trường SPA)
            if "window.onload =" in s_strip:
                onload_match = re.search(r"window\.onload\s*=\s*([a-zA-Z0-9_]+);?", s_strip)
                if onload_match:
                    func_name = onload_match.group(1)
                    s_strip = s_strip.replace(onload_match.group(0), f"{func_name}(); window.onload = {func_name};")
            scripts.append(s_strip)
            
    combined_js = ""
    if scripts:
        # Gộp tất cả các block script của file con vào chung 1 block và bọc bằng IIFE duy nhất để chia sẻ biến
        single_script = "\n".join(scripts)
        combined_js = f"(function() {{\n{single_script}\n}})();"
        
    return body_html, combined_style, combined_js

def parse_kpi_report():
    kpi_list = []
    filepath = "output/reports/core/agent_5_master_portal.md"
    if not os.path.exists(filepath):
        print("Không tìm thấy agent_5_master_portal.md")
        return kpi_list
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    lines = content.split("\n")
    table_started = False
    current_dept = "Khối CNTT"
    
    for line in lines:
        if "### 1." in line:
            if "CNTT" in line:
                current_dept = "Khối CNTT"
            elif "QTKD" in line:
                current_dept = "Khối QTKD"
            elif "Ngoại ngữ" in line:
                current_dept = "Khối Ngoại ngữ và kỹ năng mềm"
            elif "QLCLĐT" in line or "QLĐT" in line:
                current_dept = "Khối QLCLĐT"
            table_started = False
            continue
            
        if "| Họ và tên |" in line:
            table_started = True
            continue
            
        if table_started:
            if not line.strip() or not line.startswith("|"):
                continue
            if "---" in line:
                continue
            
            line_clean = re.sub(r"\[\[[^\]]*?\|(.*?)\]\]", r"\1", line)
            parts = [p.strip() for p in line_clean.split("|")[1:-1]]
            if len(parts) >= 7:
                name = parts[0].replace("**", "")
                role = parts[1]
                classes = parts[2]
                try:
                    score_discipline = float(parts[3])
                    score_academic = float(parts[4])
                    score_logs = float(parts[5])
                    score_total = float(parts[6].replace("**", ""))
                except ValueError:
                    continue
                
                kpi_list.append({
                    "name": name,
                    "role": role,
                    "classes": classes,
                    "score_discipline": score_discipline,
                    "score_academic": score_academic,
                    "score_logs": score_logs,
                    "score_total": score_total,
                    "dept": current_dept
                })
    return sorted(kpi_list, key=lambda x: x["score_total"], reverse=True)

def main():
    output_path = "output/dashboards/core/agent_5_master_portal.html"

    print("Trích xuất và biên dịch SPA Dashboard Native không dùng Iframe...")

    # Trích xuất nội dung các tab con
    body_a1, style_a1, js_a1 = extract_body_style_and_js("output/dashboards/core/agent_1_student_discipline.html", "#tab-agent1-container")
    body_a2, style_a2, js_a2 = extract_body_style_and_js("output/dashboards/core/agent_2_academic_prediction.html", "#tab-agent2-pred-container")
    body_a3, style_a3, js_a3 = extract_body_style_and_js("output/dashboards/core/agent_3_ops_discipline.html", "#tab-agent3-container")
    body_a4, style_a4, js_a4 = extract_body_style_and_js("output/dashboards/core/agent_4_daily_logs.html", "#tab-agent4-container")

    kpis = parse_kpi_report()
    
    # Tính toán thống kê theo phòng ban
    dept_stats = {}
    for item in kpis:
        dept = item["dept"]
        if dept not in dept_stats:
            dept_stats[dept] = {"count": 0, "sum": 0.0, "max_score": 0.0, "best_staff": ""}
        dept_stats[dept]["count"] += 1
        dept_stats[dept]["sum"] += item["score_total"]
        if item["score_total"] > dept_stats[dept]["max_score"]:
            dept_stats[dept]["max_score"] = item["score_total"]
            dept_stats[dept]["best_staff"] = item["name"]
            
    # Tạo các card HTML thống kê phòng ban
    dept_cards_html = ""
    colors = {
        "Khối CNTT": "from-blue-500 to-blue-700 dark:from-blue-650 dark:to-blue-850",
        "Khối QTKD": "from-emerald-500 to-emerald-700 dark:from-emerald-650 dark:to-emerald-850",
        "Khối Ngoại ngữ và kỹ năng mềm": "from-amber-500 to-amber-700 dark:from-amber-650 dark:to-amber-850",
        "Khối QLCLĐT": "from-purple-500 to-purple-700 dark:from-purple-650 dark:to-purple-850"
    }
    icons = {
        "Khối CNTT": "fa-laptop-code",
        "Khối QTKD": "fa-chart-line",
        "Khối Ngoại ngữ và kỹ năng mềm": "fa-language",
        "Khối QLCLĐT": "fa-shield-halved"
    }
    
    for dept_name in ["Khối CNTT", "Khối QTKD", "Khối Ngoại ngữ và kỹ năng mềm", "Khối QLCLĐT"]:
        stats = dept_stats.get(dept_name, {"count": 0, "sum": 0.0, "max_score": 0.0, "best_staff": "N/A"})
        avg_score = stats["sum"] / stats["count"] if stats["count"] > 0 else 0.0
        color = colors.get(dept_name, "from-slate-500 to-slate-700")
        icon = icons.get(dept_name, "fa-users")
        short_name = dept_name.replace("Khối ", "")
        
        dept_cards_html += f"""
        <div class="bg-gradient-to-br {color} rounded-3xl p-5 text-white shadow-sm flex items-center justify-between transition-transform hover:scale-[1.02] duration-300">
            <div>
                <p class="text-[10px] font-black uppercase tracking-wider opacity-90">{short_name}</p>
                <h3 class="text-2xl font-black mt-1 font-mono">{avg_score:.2f} <span class="text-xs font-normal opacity-85">KPI TB</span></h3>
                <div class="flex flex-col gap-0.5 mt-2 text-[10px] opacity-90 font-medium">
                    <span><i class="fas fa-user-friends mr-1"></i>{stats["count"]} Thầy/Cô</span>
                    <span class="truncate max-w-[150px]"><i class="fas fa-award mr-1"></i>Tốt nhất: {stats["best_staff"]}</span>
                </div>
            </div>
            <div class="w-10 h-10 bg-white/15 rounded-xl flex items-center justify-center text-white text-lg">
                <i class="fas {icon}"></i>
            </div>
        </div>
        """
    
    # Tạo các dòng bảng xếp hạng Leaderboard
    leaderboard_html = ""
    for idx, item in enumerate(kpis):
        rank_icon = str(idx + 1)
        if idx == 0: rank_icon = "🥇"
        elif idx == 1: rank_icon = "🥈"
        elif idx == 2: rank_icon = "🥉"
        
        role_clean = item["role"].strip()
        if "Trợ giảng" in role_clean or "Thực tập sinh" in role_clean or role_clean == "TG":
            role_badge = f'<span class="bg-purple-50 dark:bg-purple-950/40 text-purple-700 dark:text-purple-400 text-[10px] font-bold px-2 py-0.5 rounded">{role_clean}</span>'
        elif "Leader" in role_clean:
            role_badge = f'<span class="bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-400 text-[10px] font-bold px-2 py-0.5 rounded">Leader</span>'
        elif "Giáo vụ" in role_clean:
            role_badge = f'<span class="bg-teal-50 dark:bg-teal-950/40 text-teal-700 dark:text-teal-400 text-[10px] font-bold px-2 py-0.5 rounded">Giáo vụ</span>'
        else:
            role_badge = f'<span class="bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-400 text-[10px] font-bold px-2 py-0.5 rounded">{role_clean}</span>'

            
        color_class = "text-emerald-600 dark:text-emerald-400 font-bold"
        if item["score_total"] < 65:
            color_class = "text-red-600 dark:text-red-400 font-bold"
        elif item["score_total"] < 80:
            color_class = "text-amber-600 dark:text-amber-400 font-bold"
            
        leaderboard_html += f"""
        <tr data-dept="{item["dept"]}" class="staff-row border-b border-slate-100 dark:border-slate-800/50 hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors">
            <td class="py-3.5 px-3 font-mono font-bold text-center text-slate-700 dark:text-slate-350">{rank_icon}</td>
            <td class="py-3.5 px-3 font-bold text-slate-800 dark:text-slate-200">{item["name"]}</td>
            <td class="py-3.5 px-3">{role_badge}</td>
            <td class="py-3.5 px-3 text-xs text-slate-400 dark:text-slate-500 font-bold font-mono text-[10px]">{item["dept"]}</td>
            <td class="py-3.5 px-3 text-xs text-slate-500 max-w-xs truncate" title="{item["classes"]}">{item["classes"]}</td>
            <td class="py-3.5 px-3 font-mono {color_class}">{item["score_total"]:.2f}</td>
            <td class="py-3.5 px-3">
                <div class="w-full bg-slate-100 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div class="bg-indigo-500 dark:bg-indigo-400 h-full rounded-full" style="width: {item["score_total"]}%"></div>
                </div>
            </td>
        </tr>
        """

    master_html = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ thống Phân tích &amp; Giám sát Chỉ số Đào tạo PTIT</title>
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        slate: {{
                            850: '#0e1223',
                            950: '#020617'
                        }}
                    }}
                }}
            }}
        }}
    </script>

    <!-- Font Awesome, Google Fonts, Chart.js -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body, html, .tab-button, #tab-kpi-container, #tab-kpi-container * {{
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        .font-mono, .font-mono *, code, pre {{
            font-family: 'Fira Code', monospace !important;
        }}
        body, html {{
            background-color: #f8fafc;
            color: #0f172a;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        .dark body, .dark html {{
            background-color: #0b0f19;
            color: #f8fafc;
        }}
        .font-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
        }}
        
        /* Thống nhất style Bảng trong Tab KPI */
        #tab-kpi-container table {{
            border-collapse: collapse !important;
            width: 100% !important;
            border-radius: 1.25rem !important;
            overflow: hidden !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
            border: 1px solid #e2e8f0 !important;
        }}
        .dark #tab-kpi-container table {{
            border: 1px solid #1e293b !important;
        }}
        #tab-kpi-container th {{
            background-color: #f1f5f9 !important;
            color: #475569 !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            font-size: 0.75rem !important;
            letter-spacing: 0.05em !important;
            padding: 0.875rem 1rem !important;
            border-bottom: 2px solid #e2e8f0 !important;
        }}
        .dark #tab-kpi-container th {{
            background-color: #0b0f19 !important;
            color: #94a3b8 !important;
            border-bottom: 2px solid #1e293b !important;
        }}
        #tab-kpi-container td {{
            padding: 0.875rem 1rem !important;
            border-bottom: 1px solid #e2e8f0 !important;
            font-size: 0.875rem !important;
            color: #334155 !important;
            background-color: #ffffff !important;
        }}
        .dark #tab-kpi-container td {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            color: #cbd5e1 !important;
            background-color: #151c2c !important;
        }}
        #tab-kpi-container tr:hover td {{
            background-color: rgba(99, 102, 241, 0.04) !important;
        }}
        .dark #tab-kpi-container tr:hover td {{
            background-color: rgba(99, 102, 241, 0.08) !important;
        }}
        
        /* Thống nhất style Card trong Tab KPI */
        #tab-kpi-container .card, 
        #tab-kpi-container .dashboard-card, 
        #tab-kpi-container .chart-container, 
        #tab-kpi-container .bg-white.rounded-3xl.p-6, 
        #tab-kpi-container .bg-slate-900.border {{
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 1.25rem !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
            padding: 1.5rem !important;
        }}
        .dark #tab-kpi-container .card, 
        .dark #tab-kpi-container .dashboard-card, 
        .dark #tab-kpi-container .chart-container, 
        .dark #tab-kpi-container .bg-white.rounded-3xl.p-6, 
        .dark #tab-kpi-container .bg-slate-900.border {{
            background-color: #151c2c !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            box-shadow: none !important;
        }}
        
        .glass {{
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-color: rgba(255, 255, 255, 0.5);
        }}
        .dark .glass {{
            background: rgba(14, 18, 35, 0.8);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-color: rgba(30, 41, 59, 0.6);
        }}
        
        .active-tab-btn {{
            background-color: #1e40af !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(30, 64, 175, 0.2);
        }}
        .dark .active-tab-btn {{
            background-color: #6366f1 !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        }}
        
        /* Ẩn các tiêu đề lặp của các tab con để giao diện SPA gọn gàng */
        .spa-tab-content h1, 
        .spa-tab-content .pb-6.mb-8.border-b {{
            display: none !important;
        }}
        
        /* Nhúng CSS con đã được cô lập */
        {style_a1}
        {style_a2}
        {style_a3}
        {style_a4}
    </style>
</head>
<body class="min-h-screen pb-10">

    <!-- Header chung -->
    <header class="glass sticky top-0 z-50 py-3.5 shadow-sm border-b transition-all duration-300">
        <div class="max-w-[1440px] mx-auto px-6 flex items-center justify-between flex-wrap gap-4">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-indigo-600 dark:bg-indigo-500 rounded-xl flex items-center justify-center text-white shadow-lg font-black text-lg">
                    P
                </div>
                <div>
                    <h1 class="text-md font-black tracking-tight leading-none text-slate-900 dark:text-slate-100 font-title">PTITxRikkei Joint Venture</h1>
                    <p class="text-[9px] text-slate-400 dark:text-slate-500 font-bold uppercase mt-1 tracking-wider">Hệ thống Phân tích &amp; Giám sát Đào tạo</p>
                </div>
            </div>
            
            <div class="flex items-center gap-4">
                <button onclick="toggleDarkMode()" class="w-10 h-10 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 flex items-center justify-center hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors shadow-sm" title="Đổi chế độ sáng/tối">
                    <i id="theme-icon" class="fas fa-moon"></i>
                </button>
            </div>
        </div>
        
        <!-- Tab Navigation Menu -->
        <div class="max-w-[1440px] mx-auto px-6 mt-4">
            <div class="bg-slate-100 dark:bg-slate-900/60 p-1 rounded-2xl flex flex-wrap gap-1 border border-slate-200/60 dark:border-slate-800">
                <button onclick="switchTab('tab-kpi')" id="btn-tab-kpi" class="tab-button px-4 py-2 rounded-xl text-xs font-bold text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 active-tab-btn">
                    <i class="fas fa-calculator mr-1.5"></i> KPI Tổng Hợp (Agent 5)
                </button>
                <button onclick="switchTab('tab-agent1')" id="btn-tab-agent1" class="tab-button px-4 py-2 rounded-xl text-xs font-bold text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400">
                    <i class="fas fa-user-slash mr-1.5"></i> Kỷ Luật SV (Agent 1)
                </button>
                <button onclick="switchTab('tab-agent2-pred')" id="btn-tab-agent2-pred" class="tab-button px-4 py-2 rounded-xl text-xs font-bold text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400">
                    <i class="fas fa-chart-pie mr-1.5"></i> Dự Báo &amp; Care List (Agent 2)
                </button>
                <button onclick="switchTab('tab-agent3')" id="btn-tab-agent3" class="tab-button px-4 py-2 rounded-xl text-xs font-bold text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400">
                    <i class="fas fa-user-clock mr-1.5"></i> Tác Nghiệp GV/TG (Agent 3)
                </button>
                <button onclick="switchTab('tab-agent4')" id="btn-tab-agent4" class="tab-button px-4 py-2 rounded-xl text-xs font-bold text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400">
                    <i class="fas fa-clipboard-list mr-1.5"></i> Báo Cáo Ngày (Agent 4)
                </button>
            </div>
        </div>
    </header>

    <!-- CONTAINER CHUNG -->
    <main class="max-w-[1440px] mx-auto px-6 mt-6">

        <!-- ========================================== -->
        <!-- TAB 1: KPI TỔNG HỢP (KPI LEADERBOARD) -->
        <!-- ========================================== -->
        <div id="tab-kpi-container" class="spa-tab-content transition-opacity duration-300">
            <!-- Thống kê KPI các Phòng ban -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                {dept_cards_html}
            </div>

            <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm mb-6">
                <div class="flex flex-col md:flex-row md:items-center justify-between mb-6 gap-4">
                    <div>
                        <h4 class="font-bold text-slate-850 dark:text-slate-200">Bảng xếp hạng năng lực giảng dạy theo phòng ban</h4>
                        <p class="text-xs text-slate-400 mt-1">Lọc danh sách thầy/cô theo khối phòng ban tương ứng trong Trung tâm</p>
                    </div>
                    <div class="flex items-center gap-1.5 flex-wrap bg-slate-100 dark:bg-slate-950 p-1 rounded-2xl border border-slate-200 dark:border-slate-800">
                        <button onclick="filterDept('all')" class="dept-filter-btn px-3 py-1.5 rounded-xl text-xs font-bold bg-indigo-600 text-white dark:bg-indigo-500 transition-all shadow-sm">Tất cả</button>
                        <button onclick="filterDept('Khối CNTT')" class="dept-filter-btn px-3 py-1.5 rounded-xl text-xs font-bold text-slate-500 dark:text-slate-400 hover:bg-slate-200/50 dark:hover:bg-slate-850 transition-all">Khối CNTT</button>
                        <button onclick="filterDept('Khối QTKD')" class="dept-filter-btn px-3 py-1.5 rounded-xl text-xs font-bold text-slate-500 dark:text-slate-400 hover:bg-slate-200/50 dark:hover:bg-slate-850 transition-all">Khối QTKD</button>
                        <button onclick="filterDept('Khối Ngoại ngữ và kỹ năng mềm')" class="dept-filter-btn px-3 py-1.5 rounded-xl text-xs font-bold text-slate-500 dark:text-slate-400 hover:bg-slate-200/50 dark:hover:bg-slate-850 transition-all font-title">Ngoại ngữ &amp; KNM</button>
                        <button onclick="filterDept('Khối QLCLĐT')" class="dept-filter-btn px-3 py-1.5 rounded-xl text-xs font-bold text-slate-500 dark:text-slate-400 hover:bg-slate-200/50 dark:hover:bg-slate-850 transition-all">Khối QLCLĐT</button>
                    </div>
                </div>
                <div class="overflow-x-auto max-h-[550px] overflow-y-auto rounded-2xl border border-slate-150 dark:border-slate-850">
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-slate-100/50 dark:bg-slate-950 text-slate-400 dark:text-slate-500 uppercase text-xs font-bold border-b border-slate-200 dark:border-slate-850 sticky top-0 z-10">
                            <tr>
                                <th class="py-3 px-3 text-center">Hạng</th>
                                <th class="py-3 px-3">Họ &amp; Tên</th>
                                <th class="py-3 px-3">Vai trò</th>
                                <th class="py-3 px-3">Phòng ban</th>
                                <th class="py-3 px-3">Lớp phụ trách</th>
                                <th class="py-3 px-3">KPI</th>
                                <th class="py-3 px-3 w-28">Thanh KPI</th>
                            </tr>
                        </thead>
                        <tbody class="text-sm divide-y divide-slate-100 dark:divide-slate-800/50">
                            {leaderboard_html}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm">
                <div class="flex items-center justify-between flex-wrap gap-4">
                    <div>
                        <h4 class="font-bold text-slate-850 dark:text-slate-200 text-sm">Báo cáo đánh giá chi tiết Obsidian Wiki-Link</h4>
                        <p class="text-xs text-slate-400 mt-1">Xem đầy đủ nhận xét điểm mạnh, điểm yếu, và đề xuất cải thiện chi tiết của từng GV/TG</p>
                    </div>
                    <a href="output/reports/core/agent_5_master_portal.md" target="_blank" class="px-4 py-2.5 bg-slate-100 hover:bg-slate-250 dark:bg-slate-800 dark:hover:bg-slate-700 text-xs font-bold rounded-xl transition-all shadow-sm">
                        <i class="fas fa-file-alt mr-1.5 text-indigo-500"></i> Xem file agent_5_master_portal.md
                    </a>
                </div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 2: KỶ LUẬT HỌC VIÊN (AGENT 1) -->
        <!-- ========================================== -->
        <div id="tab-agent1-container" class="spa-tab-content hidden transition-opacity duration-300">
            {body_a1}
        </div>

        <!-- ========================================== -->
        <!-- TAB 3: DỰ BÁO HỌC LỰC & CARE LIST (AGENT 2) -->
        <!-- ========================================== -->
        <div id="tab-agent2-pred-container" class="spa-tab-content hidden transition-opacity duration-300">
            {body_a2}
        </div>

        <!-- ========================================== -->
        <!-- TAB 4: KỶ LUẬT TÁC NGHIỆP GV/TG (AGENT 3) -->
        <!-- ========================================== -->
        <div id="tab-agent3-container" class="spa-tab-content hidden transition-opacity duration-300">
            {body_a3}
        </div>

        <!-- ========================================== -->
        <!-- TAB 5: NHẬT KÝ BÁO CÁO NGÀY (AGENT 4) -->
        <!-- ========================================== -->
        <div id="tab-agent4-container" class="spa-tab-content hidden transition-opacity duration-300">
            {body_a4}
        </div>

    </main>

    <!-- JS của các Tab con được cách ly IIFE và bảo vệ bằng try-catch -->
    <script>
        (function() {{
            const _origDocAdd = document.addEventListener;
            const _origWinAdd = window.addEventListener;
            
            document.addEventListener = function(type, listener, options) {{
                if (type === "DOMContentLoaded") {{
                    setTimeout(listener, 1);
                }} else {{
                    _origDocAdd.call(document, type, listener, options);
                }}
            }};
            window.addEventListener = function(type, listener, options) {{
                if (type === "load") {{
                    setTimeout(listener, 1);
                }} else {{
                    _origWinAdd.call(window, type, listener, options);
                }}
            }};
            
            try {{
                {js_a1}
            }} catch (e) {{
                console.error("Lỗi khi chạy JS của Agent 1:", e);
            }}
            
            try {{
                {js_a2}
            }} catch (e) {{
                console.error("Lỗi khi chạy JS của Agent 2:", e);
            }}
            
            try {{
                {js_a3}
            }} catch (e) {{
                console.error("Lỗi khi chạy JS của Agent 3:", e);
            }}
            
            try {{
                {js_a4}
            }} catch (e) {{
                console.error("Lỗi khi chạy JS của Agent 4:", e);
            }}
            
            // Khôi phục lại hàm addEventListener chuẩn của trình duyệt
            document.addEventListener = _origDocAdd;
            window.addEventListener = _origWinAdd;
        }})();
    </script>

    <!-- Script điều khiển Master Portal chính -->
    <script>
        document.addEventListener("DOMContentLoaded", () => {{
            if (localStorage.getItem('theme') === 'dark' ||
                (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
                document.documentElement.classList.add('dark');
                updateThemeIcon(true);
            }} else {{
                document.documentElement.classList.remove('dark');
                updateThemeIcon(false);
            }}
        }});

        function toggleDarkMode() {{
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            updateThemeIcon(isDark);
            
            // Kích hoạt sự kiện đổi theme cho biểu đồ Chart.js tự vẽ lại
            document.dispatchEvent(new CustomEvent('themechanged', {{ detail: {{ isDark: isDark }} }}));
        }}

        function updateThemeIcon(isDark) {{
            const icon = document.getElementById("theme-icon");
            if (isDark) {{
                icon.className = "fas fa-sun text-amber-400";
            }} else {{
                icon.className = "fas fa-moon text-indigo-500";
            }}
        }}

        function switchTab(tabId) {{
            const tabs = [
                "tab-kpi", "tab-agent1", "tab-agent2-pred", 
                "tab-agent3", "tab-agent4"
            ];
            
            tabs.forEach(t => {{
                const container = document.getElementById(t + "-container");
                const btn = document.getElementById("btn-" + t);
                if (container) container.classList.add("hidden");
                if (btn) btn.classList.remove("active-tab-btn");
            }});
            
            const activeContainer = document.getElementById(tabId + "-container");
            const activeBtn = document.getElementById("btn-" + tabId);
            if (activeContainer) activeContainer.classList.remove("hidden");
            if (activeBtn) activeBtn.classList.add("active-tab-btn");
        }}

        function filterDept(dept) {{
            const rows = document.querySelectorAll(".staff-row");
            rows.forEach(row => {{
                const rDept = row.getAttribute("data-dept");
                if (dept === "all" || rDept === dept) {{
                    row.style.display = "";
                }} else {{
                    row.style.display = "none";
                }}
            }});
            
            const btns = document.querySelectorAll(".dept-filter-btn");
            btns.forEach(btn => {{
                btn.classList.remove("bg-indigo-600", "text-white", "dark:bg-indigo-500");
                btn.classList.add("text-slate-500", "dark:text-slate-400", "hover:bg-slate-200/50");
            }});
            
            event.currentTarget.classList.remove("text-slate-500", "dark:text-slate-400", "hover:bg-slate-200/50");
            event.currentTarget.classList.add("bg-indigo-600", "text-white", "dark:bg-indigo-500");
        }}
        function toggleRiskRows(panelId) {{
            const panel = document.getElementById('risk-panel-' + panelId);
            const icon = document.getElementById('icon-' + panelId);
            if (panel) {{
                const isHidden = panel.classList.toggle('hidden');
                if (icon) {{
                    if (isHidden) {{
                        icon.style.transform = 'rotate(0deg)';
                    }} else {{
                        icon.style.transform = 'rotate(180deg)';
                    }}
                }}
            }}
        }}
    </script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(master_html)

    print(f"SPA Dashboard Master Portal đã được sinh thành công tại: {output_path}")

if __name__ == "__main__":
    main()

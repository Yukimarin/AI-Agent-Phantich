# -*- coding: utf-8 -*-
import json
import os
import sys
import shutil

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_ACADEMIC_DIR = "output/dashboards/academic"

def get_top_navbar(current_key):
    """Sinh thanh điều hướng Navbar liên kết giữa các môn và khối đào tạo"""
    links = [
        {"key": "ks24_microservices", "title": "KS24 Microservices", "url_rel": {
            "ks24": "it214_microservices_cntt.html",
            "ks25": "../ks24/it214_microservices_cntt.html",
            "ks26": "../ks24/it214_microservices_cntt.html"
        }},
        {"key": "ks25_fastapi", "title": "KS25 CNTT (FastAPI)", "url_rel": {
            "ks24": "../ks25/it105_fastapi_cntt.html",
            "ks25": "it105_fastapi_cntt.html",
            "ks26": "../ks25/it105_fastapi_cntt.html"
        }},
        {"key": "ks25_man107", "title": "KS25 QTKD (MAN107)", "url_rel": {
            "ks24": "../ks25/man107_qtkd.html",
            "ks25": "man107_qtkd.html",
            "ks26": "../ks25/man107_qtkd.html"
        }},
        {"key": "ks26_cntt", "title": "KS26 CNTT (SSK101)", "url_rel": {
            "ks24": "../ks26/ssk101_cntt.html",
            "ks25": "../ks26/ssk101_cntt.html",
            "ks26": "ssk101_cntt.html"
        }},
        {"key": "ks26_qtkd", "title": "KS26 QTKD (SSK101)", "url_rel": {
            "ks24": "../ks26/ssk101_qtkd.html",
            "ks25": "../ks26/ssk101_qtkd.html",
            "ks26": "ssk101_qtkd.html"
        }}
    ]

    current_cohort = current_key.split("_")[0]
    nav_items = []
    for item in links:
        is_active = (item["key"] == current_key)
        target_url = item["url_rel"].get(current_cohort, item["url_rel"]["ks25"])
        if is_active:
            nav_items.append(f'<span class="bg-indigo-600 text-white px-2.5 py-1 rounded font-semibold">{item["title"]}</span>')
        else:
            nav_items.append(f'<a href="{target_url}" class="text-slate-400 hover:text-white px-2 py-1 rounded transition hover:bg-slate-700/50">{item["title"]}</a>')

    return f"""
    <div class="hidden lg:flex items-center space-x-1 bg-slate-800/90 p-1 rounded-lg border border-slate-700 text-xs">
        {''.join(nav_items)}
        <div class="h-3 w-px bg-slate-700 mx-1"></div>
        <a href="../../core/agent_5_master_portal.html" class="text-indigo-400 hover:text-indigo-300 font-medium px-2 py-1 flex items-center gap-1 transition" title="Quay về Master Executive Portal">
            <i class="fa-solid fa-house-laptop"></i> Master Portal
        </a>
        <a href="../../management/director_cockpit.html" class="text-amber-400 hover:text-amber-300 font-medium px-2 py-1 flex items-center gap-1 transition" title="Báo cáo Giám đốc Đào tạo">
            <i class="fa-solid fa-gauge-high"></i> Cockpit
        </a>
    </div>
    """

def generate_ks24_dashboard():
    """Tạo ks24/it214_microservices_cntt.html"""
    out_dir = os.path.join(BASE_ACADEMIC_DIR, "ks24")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "it214_microservices_cntt.html")

    a2_path = "data/processed/agent2_output.json"
    ks24_care = []
    classes_data = [
        {"name": "HN-K24-CNTT1", "size": 35, "gv": "Bùi Thanh Hải", "tg": "Phạm Tuấn Bình", "pred_old": 54.6, "pred_new": 51.7, "att_v": 12.9, "hw_v": 11.4, "el_v": 14.3, "care_count": 14, "status": "YELLOW"},
        {"name": "HN-K24-CNTT2", "size": 39, "gv": "Bùi Thanh Hải", "tg": "Đinh Thành Nam", "pred_old": 59.5, "pred_new": 59.5, "att_v": 1.8, "hw_v": 3.8, "el_v": 5.1, "care_count": 7, "status": "GREEN"},
        {"name": "HN-K24-CNTT3", "size": 43, "gv": "Hồ Xuân Hùng", "tg": "Phạm Tuấn Bình", "pred_old": 51.0, "pred_new": 43.3, "att_v": 25.6, "hw_v": 18.6, "el_v": 27.9, "care_count": 21, "status": "RED"},
        {"name": "HN-K24-CNTT4", "size": 32, "gv": "Bùi Thanh Hải", "tg": "Đinh Thành Nam", "pred_old": 57.0, "pred_new": 54.6, "att_v": 9.7, "hw_v": 9.4, "el_v": 12.5, "care_count": 11, "status": "YELLOW"},
        {"name": "HCM-K24-CNTT1", "size": 43, "gv": "Nguyễn Bá Minh Đạo", "tg": "Phan Ngọc Tài", "pred_old": 60.2, "pred_new": 48.5, "att_v": 16.3, "hw_v": 14.0, "el_v": 18.6, "care_count": 16, "status": "ORANGE"}
    ]

    if os.path.exists(a2_path):
        with open(a2_path, "r", encoding="utf-8") as f:
            a2 = json.load(f)
            ks24_care = [s for s in a2.get("care_list", []) if "24" in s.get("class_name", "")]

    students_json = json.dumps(ks24_care, ensure_ascii=False)
    classes_json = json.dumps(classes_data, ensure_ascii=False)
    navbar_html = get_top_navbar("ks24_microservices")

    html = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Chuyên Sâu Học Vụ: Môn Microservices IT-214 (Khóa KS24 CNTT)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        slate: {{ 850: '#111622', 900: '#0b0f19', 950: '#06080e' }},
                        indigo: {{ 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca' }}
                    }}
                }}
            }}
        }}
    </script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #06080e; color: #cbd5e1; font-size: 13px; }}
        code, pre, .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        .custom-scrollbar::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: #0b0f19; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #26324a; border-radius: 3px; }}
        .glass-card {{ background: rgba(15, 20, 31, 0.85); backdrop-filter: blur(12px); border: 1px solid #1e283d; }}
        .glass-card:hover {{ border-color: #334155; }}
        .tab-btn.active {{ background-color: #4f46e5; color: #ffffff; border-color: #6366f1; font-weight: 600; }}
        .metric-card {{ background: linear-gradient(180deg, rgba(22, 28, 45, 0.75) 0%, rgba(15, 20, 31, 0.9) 100%); border: 1px solid #1e293b; }}
        .funnel-step {{ position: relative; }}
        .funnel-step:not(:last-child)::after {{
            content: '➔';
            position: absolute;
            right: -14px;
            top: 50%;
            transform: translateY(-50%);
            color: #64748b;
            font-size: 14px;
            font-weight: bold;
            z-index: 10;
        }}
        @media (max-width: 768px) {{
            .funnel-step:not(:last-child)::after {{ display: none; }}
        }}
    </style>
</head>
<body class="min-h-screen custom-scrollbar antialiased selection:bg-indigo-500 selection:text-white">

    <!-- HEADER HỌC VỤ KS24 -->
    <header class="border-b border-slate-800 bg-slate-900/90 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-indigo-500/20">
                    <i class="fa-solid fa-network-wired"></i>
                </div>
                <div>
                    <h1 class="text-base font-bold text-white tracking-tight flex items-center gap-2">
                        BÁO CÁO TOÀN CẢNH HỌC VỤ: MÔN MICROSERVICES SYSTEM DESIGN
                        <span class="text-xs bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2 py-0.5 rounded font-mono">Khóa KS24 CNTT</span>
                    </h1>
                    <p class="text-xs text-slate-400">Phân tích chuyên sâu 5 lớp CNTT, áp lực môi trường Hackathon và danh sách can thiệp 69 SV</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                {navbar_html}
                <button onclick="window.print()" class="text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-3.5 py-1.5 rounded-lg shadow-md transition flex items-center gap-1.5">
                    <i class="fa-solid fa-print"></i> In Báo Cáo
                </button>
            </div>
        </div>
    </header>

    <!-- NAVIGATION TABS -->
    <div class="border-b border-slate-800 bg-slate-950/80 sticky top-16 z-40 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav class="flex space-x-2 py-2.5 overflow-x-auto custom-scrollbar" id="nav-tabs">
                <button onclick="switchTab('tab-macro')" class="tab-btn active px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-filter"></i> I. Phễu Học Vụ & Tổng Quan
                </button>
                <button onclick="switchTab('tab-chokepoint')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-triangle-exclamation"></i> II. Độ Khó CDC & Vực Thẳm Hackathon
                </button>
                <button onclick="switchTab('tab-classes')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-chalkboard-user"></i> III. Ma Trận 5 Lớp & GV/TG
                </button>
                <button onclick="switchTab('tab-recovery')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2 text-amber-300">
                    <i class="fa-solid fa-life-ring"></i> IV. Phân Luồng Cứu Vãn 69 SV
                </button>
                <button onclick="switchTab('tab-students')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-table-list"></i> V. Tra Cứu Toàn Bộ Sinh Viên
                </button>
            </nav>
        </div>
    </div>

    <!-- MAIN BODY -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <section id="tab-macro" class="tab-content space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="metric-card rounded-xl p-4 flex flex-col justify-between">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>SĨ SỐ THỰC HỌC MÔN IT-214</span>
                        <i class="fa-solid fa-users text-indigo-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-white font-mono">192 <span class="text-xs text-slate-400 font-normal">SV</span></div>
                        <p class="text-xs text-slate-400 mt-1">5 lớp chính quy (HN: 149, HCM: 43)</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>DỰ BÁO QUA MÔN TRUNG BÌNH</span>
                        <i class="fa-solid fa-chart-line text-emerald-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-emerald-400 font-mono">51.5%</div>
                        <p class="text-xs text-emerald-300 mt-1 font-medium">Sau khi áp dụng hệ số phạt môi trường</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between border-amber-900/50 bg-amber-950/20">
                    <div class="flex items-center justify-between text-amber-300 text-xs font-semibold">
                        <span>DANH SÁCH CẦN CAN THIỆP (CARE LIST)</span>
                        <i class="fa-solid fa-triangle-exclamation text-amber-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-amber-400 font-mono">69 <span class="text-xs text-slate-400 font-normal">SV (35.9%)</span></div>
                        <p class="text-xs text-amber-300 mt-1 font-medium">Nhóm nguy cơ đuối Hackathon & nợ bài</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between border-indigo-900/50">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>LỚP ĐIỂM DẪN ĐẦU TOÀN KHÓA</span>
                        <i class="fa-solid fa-medal text-yellow-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-2xl font-extrabold text-indigo-300 font-mono">HN-K24-CNTT2</div>
                        <p class="text-xs text-slate-300 mt-1">Dự báo đỗ 59.5% | Vắng CC 1.79% | 0 SV cấm thi</p>
                    </div>
                </div>
            </div>

            <div class="glass-card rounded-xl p-6 border-indigo-900/40">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-sm font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-filter text-indigo-400"></i>
                        SƠ ĐỒ PHỄU HAO HỤT HỌC VỤ MÔN MICROSERVICES (KS24)
                    </h2>
                    <span class="text-xs bg-slate-800 text-slate-400 px-2.5 py-1 rounded font-mono">Hệ số độ khó CDC = 1.45</span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-3 relative mb-6">
                    <div class="funnel-step bg-slate-900/90 border border-slate-800 rounded-xl p-4 text-center">
                        <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">1. SĨ SỐ ĐẦU VÀO MÔN</div>
                        <div class="text-2xl font-extrabold text-white font-mono mt-1">192 SV</div>
                        <div class="text-xs text-slate-500 mt-1">100% quy mô thực học</div>
                        <div class="mt-2 pt-2 border-t border-slate-800 text-[11px] text-slate-400">5 lớp CNTT (HN & HCM)</div>
                    </div>

                    <div class="funnel-step bg-slate-900/90 border border-slate-800 rounded-xl p-4 text-center">
                        <div class="text-[11px] font-semibold text-amber-400 uppercase tracking-wider">2. ĐẠT CHUẨN NỀ NẾP & R-POINT</div>
                        <div class="text-2xl font-extrabold text-amber-400 font-mono mt-1">165 SV</div>
                        <div class="text-xs text-slate-400 mt-1">85.9% duy trì kỷ luật tốt</div>
                        <div class="mt-2 pt-2 border-t border-slate-800 text-[11px] text-rose-400">-27 SV vi phạm nề nếp</div>
                    </div>

                    <div class="funnel-step bg-rose-950/30 border-2 border-rose-600/60 rounded-xl p-4 text-center shadow-lg">
                        <div class="text-[11px] font-bold text-rose-400 uppercase tracking-wider flex items-center justify-center gap-1">
                            <i class="fa-solid fa-triangle-exclamation"></i> 3. VƯỢT RÀO CẢN HACKATHON
                        </div>
                        <div class="text-2xl font-extrabold text-rose-300 font-mono mt-1">123 SV</div>
                        <div class="text-xs text-slate-300 mt-1">64.1% đạt điểm thi thực tế ≥50</div>
                        <div class="mt-2 pt-2 border-t border-rose-900 text-[11px] font-bold text-rose-400">ĐIỂM NGHẼN: 69 SV ĐUỐI THỰC CHIẾN</div>
                    </div>

                    <div class="funnel-step bg-emerald-950/30 border border-emerald-600/40 rounded-xl p-4 text-center">
                        <div class="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider">4. DỰ BÁO QUA MÔN CHÍNH THỨC</div>
                        <div class="text-2xl font-extrabold text-emerald-400 font-mono mt-1">99 SV</div>
                        <div class="text-xs text-emerald-300 mt-1">51.5% tỷ lệ hoàn thành kỳ vọng</div>
                        <div class="mt-2 pt-2 border-t border-emerald-900 text-[11px] text-emerald-400">HN2 dẫn đầu với 59.5%</div>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-card rounded-xl p-5">
                    <h3 class="text-sm font-bold text-white mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-chart-pie text-indigo-400"></i>
                        Phân Bổ Rủi Ro Học Thuật 192 Sinh Viên
                    </h3>
                    <div class="h-64 flex items-center justify-center">
                        <canvas id="riskDoughnutChart"></canvas>
                    </div>
                </div>

                <div class="glass-card rounded-xl p-5">
                    <h3 class="text-sm font-bold text-white mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-chart-column text-indigo-400"></i>
                        Tỷ Lệ Dự Báo Đỗ & Số Lượng Care List Theo 5 Lớp
                    </h3>
                    <div class="h-64">
                        <canvas id="classComparisonChart"></canvas>
                    </div>
                </div>
            </div>
        </section>

        <section id="tab-chokepoint" class="tab-content space-y-6 hidden">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="glass-card rounded-xl p-5 border-l-4 border-l-rose-500">
                    <div class="text-xs font-bold text-rose-400 uppercase">HỆ SỐ ĐỘ KHÓ MÔN HỌC (CDC)</div>
                    <div class="text-3xl font-extrabold text-white font-mono mt-2">1.45</div>
                    <p class="text-xs text-slate-400 mt-2">
                        Cao nhất toàn bộ chương trình (PTTKHT: 1.25, MAN107: 1.10). Kiến thức nặng: Distributed Tracing, Kafka/RabbitMQ, Docker Swarm/K8s, API Gateway, Circuit Breaker.
                    </p>
                </div>
                <div class="glass-card rounded-xl p-5 border-l-4 border-l-amber-500">
                    <div class="text-xs font-bold text-amber-400 uppercase">ĐỘ VÊNH BÀI TẬP VS HACKATHON</div>
                    <div class="text-3xl font-extrabold text-amber-400 font-mono mt-2">39.7 Điểm</div>
                    <p class="text-xs text-slate-400 mt-2">
                        Nhiều SV hoàn thành BTVN > 85% nhờ template có sẵn nhưng điểm Hackathon thực chiến chỉ đạt 45.3 điểm (thất bại khi debug microservices trực tiếp).
                    </p>
                </div>
                <div class="glass-card rounded-xl p-5 border-l-4 border-l-indigo-500">
                    <div class="text-xs font-bold text-indigo-400 uppercase">HỆ SỐ PHẠT NỀ NẾP (MULT_ENV)</div>
                    <div class="text-3xl font-extrabold text-indigo-300 font-mono mt-2">0.850</div>
                    <p class="text-xs text-slate-400 mt-2">
                        Áp dụng cho các lớp có tỷ lệ vi phạm trung bình > 10% (HN3 vắng 25.64%, HCM1 vắng 16.28%).
                    </p>
                </div>
            </div>
        </section>

        <section id="tab-classes" class="tab-content space-y-6 hidden">
            <div class="glass-card rounded-xl p-6">
                <h3 class="text-base font-bold text-white mb-4 flex items-center gap-2">
                    <i class="fa-solid fa-chalkboard-user text-indigo-400"></i>
                    Bảng Đối Chuẩn Hiệu Suất Học Vụ 5 Lớp Khóa KS24
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-400 bg-slate-900/50">
                                <th class="p-3">Lớp Học</th>
                                <th class="p-3">Sĩ Số</th>
                                <th class="p-3">Giảng Viên & Trợ Giảng</th>
                                <th class="p-3">Vắng CC (%)</th>
                                <th class="p-3">Nợ BT (%)</th>
                                <th class="p-3">Elearning (%)</th>
                                <th class="p-3">Dự Báo Đỗ Mới</th>
                                <th class="p-3">Care List</th>
                                <th class="p-3">Đánh Giá Trạng Thái</th>
                            </tr>
                        </thead>
                        <tbody id="classesTableBody" class="divide-y divide-slate-800/60 text-xs font-mono">
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <section id="tab-recovery" class="tab-content space-y-6 hidden">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="glass-card rounded-xl p-4 border-t-4 border-t-rose-500">
                    <div class="flex items-center justify-between text-rose-400 font-bold text-xs">
                        <span>NHÓM RED (BÁO ĐỘNG ĐỎ)</span>
                        <span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-mono">18 SV</span>
                    </div>
                    <p class="text-xs text-slate-300 mt-2 font-sans">Hổng kiến thức nặng, Hackathon < 40 điểm, nguy cơ trượt > 80%.</p>
                </div>
                <div class="glass-card rounded-xl p-4 border-t-4 border-t-amber-500">
                    <div class="flex items-center justify-between text-amber-400 font-bold text-xs">
                        <span>NHÓM ORANGE (ĐUỐI THỰC HÀNH)</span>
                        <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono">24 SV</span>
                    </div>
                    <p class="text-xs text-slate-300 mt-2 font-sans">Làm BTVN tốt nhưng đuối khi test bài tập độc lập (Hackathon 40 - 55 điểm).</p>
                </div>
                <div class="glass-card rounded-xl p-4 border-t-4 border-t-yellow-500">
                    <div class="flex items-center justify-between text-yellow-400 font-bold text-xs">
                        <span>NHÓM YELLOW (KỶ LUẬT KÉM)</span>
                        <span class="px-2 py-0.5 rounded bg-yellow-500/20 text-yellow-300 font-mono">15 SV</span>
                    </div>
                    <p class="text-xs text-slate-300 mt-2 font-sans">Tư duy tốt nhưng vắng học và nợ bài tập > 15%.</p>
                </div>
                <div class="glass-card rounded-xl p-4 border-t-4 border-t-emerald-500">
                    <div class="flex items-center justify-between text-emerald-400 font-bold text-xs">
                        <span>NHÓM GREEN (CÓ TIỀM NĂNG)</span>
                        <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">12 SV</span>
                    </div>
                    <p class="text-xs text-slate-300 mt-2 font-sans">Chỉ cần bồi dưỡng kiến thức đề tài lớn để chắc chắn vượt qua ngưỡng 60 điểm.</p>
                </div>
            </div>
        </section>

        <section id="tab-students" class="tab-content space-y-6 hidden">
            <div class="glass-card rounded-xl p-6">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-5">
                    <div>
                        <h3 class="text-base font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-table-list text-indigo-400"></i>
                            Danh Sách 69 Sinh Viên Nhóm Nguy Cơ (Care List KS24)
                        </h3>
                        <p class="text-xs text-slate-400 mt-1">Lọc theo lớp học, mức độ rủi ro hoặc tìm kiếm tên sinh viên</p>
                    </div>

                    <div class="flex flex-wrap items-center gap-3">
                        <input type="text" id="studentSearch" placeholder="Tìm tên sinh viên..." 
                            class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 w-48">
                        
                        <select id="classFilter" class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-indigo-500">
                            <option value="ALL">Tất cả 5 lớp</option>
                            <option value="HN-K24-CNTT1">HN-K24-CNTT1</option>
                            <option value="HN-K24-CNTT2">HN-K24-CNTT2</option>
                            <option value="HN-K24-CNTT3">HN-K24-CNTT3</option>
                            <option value="HN-K24-CNTT4">HN-K24-CNTT4</option>
                            <option value="HCM-K24-CNTT1">HCM-K24-CNTT1</option>
                        </select>

                        <select id="riskFilter" class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-indigo-500">
                            <option value="ALL">Tất cả rủi ro</option>
                            <option value="RED">RED (Rất cao)</option>
                            <option value="ORANGE">ORANGE (Cao)</option>
                            <option value="YELLOW">YELLOW (Trung bình)</option>
                            <option value="GREEN">GREEN (Nhẹ)</option>
                        </select>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-400 bg-slate-900/50">
                                <th class="p-3">#</th>
                                <th class="p-3">Lớp</th>
                                <th class="p-3">Họ và Tên</th>
                                <th class="p-3 text-center">P_Final (%)</th>
                                <th class="p-3 text-center">Hackathon Trước</th>
                                <th class="p-3 text-center">Hackathon Hiện Tại</th>
                                <th class="p-3 text-center">BTVN (%)</th>
                                <th class="p-3 text-center">Vắng CC (%)</th>
                                <th class="p-3 text-center">R-Point</th>
                                <th class="p-3 text-center">Mức Rủi Ro</th>
                                <th class="p-3">Lý Do & Hành Động Can Thiệp</th>
                            </tr>
                        </thead>
                        <tbody id="studentTableBody" class="divide-y divide-slate-800/60 text-xs">
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
    </main>

    <script>
        const rawStudents = {students_json};
        const rawClasses = {classes_json};

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabId).classList.remove('hidden');
            event.currentTarget.classList.add('active');
        }}

        function renderClasses() {{
            const tbody = document.getElementById('classesTableBody');
            tbody.innerHTML = rawClasses.map(c => {{
                let statusBadge = c.status === 'GREEN' 
                    ? '<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-sans font-semibold">🟢 Kiểu mẫu</span>'
                    : c.status === 'RED'
                    ? '<span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-sans font-semibold">🔴 Báo động</span>'
                    : c.status === 'ORANGE'
                    ? '<span class="px-2 py-0.5 rounded bg-orange-500/20 text-orange-300 font-sans font-semibold">🟠 Đuối thực hành</span>'
                    : '<span class="px-2 py-0.5 rounded bg-yellow-500/20 text-yellow-300 font-sans font-semibold">🟡 Cần theo dõi</span>';

                return `
                    <tr class="hover:bg-slate-800/40 transition">
                        <td class="p-3 font-bold text-white">${{c.name}}</td>
                        <td class="p-3">${{c.size}} SV</td>
                        <td class="p-3 font-sans"><span class="text-slate-200">${{c.gv}}</span> <span class="text-slate-500">|</span> <span class="text-slate-400">TG: ${{c.tg}}</span></td>
                        <td class="p-3 text-center ${{c.att_v > 15 ? 'text-rose-400 font-bold' : 'text-slate-300'}}">${{c.att_v}}%</td>
                        <td class="p-3 text-center text-slate-300">${{c.hw_v}}%</td>
                        <td class="p-3 text-center text-slate-300">${{c.el_v}}%</td>
                        <td class="p-3 text-center font-bold ${{c.pred_new < 50 ? 'text-rose-400' : 'text-emerald-400'}}">${{c.pred_new}}%</td>
                        <td class="p-3 text-center font-bold text-amber-400">${{c.care_count}} SV</td>
                        <td class="p-3">${{statusBadge}}</td>
                    </tr>
                `;
            }}).join('');
        }}

        function renderStudents() {{
            const searchVal = document.getElementById('studentSearch').value.toLowerCase();
            const classVal = document.getElementById('classFilter').value;
            const riskVal = document.getElementById('riskFilter').value;

            const filtered = rawStudents.filter(s => {{
                const matchName = (s.full_name || '').toLowerCase().includes(searchVal);
                const matchClass = classVal === 'ALL' || (s.class_name || '') === classVal;
                const matchRisk = riskVal === 'ALL' || (s.risk_level || '') === riskVal;
                return matchName && matchClass && matchRisk;
            }});

            const tbody = document.getElementById('studentTableBody');
            if (filtered.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="11" class="text-center p-6 text-slate-500">Không tìm thấy sinh viên phù hợp bộ lọc.</td></tr>`;
                return;
            }}

            tbody.innerHTML = filtered.map((s, idx) => {{
                let riskBadge = s.risk_level === 'RED'
                    ? '<span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold">RED</span>'
                    : s.risk_level === 'ORANGE'
                    ? '<span class="px-2 py-0.5 rounded bg-orange-500/20 text-orange-300 font-bold">ORANGE</span>'
                    : s.risk_level === 'YELLOW'
                    ? '<span class="px-2 py-0.5 rounded bg-yellow-500/20 text-yellow-300 font-bold">YELLOW</span>'
                    : '<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">GREEN</span>';

                let reasonsText = (s.reasons || []).join('; ');
                let pFinal = typeof s.p_final === 'number' ? s.p_final.toFixed(1) : (s.p_final || '—');

                return `
                    <tr class="hover:bg-slate-800/40 transition">
                        <td class="p-3 text-slate-500 font-mono">${{idx + 1}}</td>
                        <td class="p-3 font-mono font-bold text-slate-300">${{s.class_name || '—'}}</td>
                        <td class="p-3 font-semibold text-white">${{s.full_name || '—'}}</td>
                        <td class="p-3 text-center font-mono font-bold ${{pFinal < 50 ? 'text-rose-400' : 'text-emerald-400'}}">${{pFinal}}%</td>
                        <td class="p-3 text-center font-mono text-slate-300">${{s.prior_hack || '—'}}</td>
                        <td class="p-3 text-center font-mono font-bold ${{s.hack < 50 ? 'text-rose-400' : 'text-slate-200'}}">${{s.hack != null ? Number(s.hack).toFixed(1) : '—'}}</td>
                        <td class="p-3 text-center font-mono text-slate-300">${{s.hw != null ? Number(s.hw).toFixed(1) : '—'}}%</td>
                        <td class="p-3 text-center font-mono ${{s.att > 15 ? 'text-rose-400 font-bold' : 'text-slate-400'}}">${{s.att || 0}}%</td>
                        <td class="p-3 text-center font-mono text-slate-300">${{s.rp || 100}}</td>
                        <td class="p-3 text-center">${{riskBadge}}</td>
                        <td class="p-3 text-slate-400 text-xs">${{reasonsText || 'Đuối thực hành Hackathon, cần bồi dưỡng thêm'}}</td>
                    </tr>
                `;
            }}).join('');
        }}

        function initCharts() {{
            const ctxDoughnut = document.getElementById('riskDoughnutChart').getContext('2d');
            new Chart(ctxDoughnut, {{
                type: 'doughnut',
                data: {{
                    labels: ['An Toàn / Xuất Sắc', 'RED (Nguy Cơ Cao)', 'ORANGE (Đuối Hackathon)', 'YELLOW (Kỷ Luật)', 'GREEN (Tiềm Năng)'],
                    datasets: [{{
                        data: [123, 18, 24, 15, 12],
                        backgroundColor: ['#10b981', '#f43f5e', '#f97316', '#eab308', '#3b82f6'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', font: {{ size: 11 }} }} }}
                    }}
                }}
            }});

            const ctxBar = document.getElementById('classComparisonChart').getContext('2d');
            new Chart(ctxBar, {{
                type: 'bar',
                data: {{
                    labels: ['HN-CNTT1', 'HN-CNTT2', 'HN-CNTT3', 'HN-CNTT4', 'HCM-CNTT1'],
                    datasets: [
                        {{
                            label: 'Dự Báo Đỗ (%)',
                            data: [51.7, 59.5, 43.3, 54.6, 48.5],
                            backgroundColor: '#6366f1',
                            borderRadius: 6
                        }},
                        {{
                            label: 'Số SV Care List',
                            data: [14, 7, 21, 11, 16],
                            backgroundColor: '#f59e0b',
                            borderRadius: 6
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
                    }},
                    plugins: {{
                        legend: {{ labels: {{ color: '#94a3b8' }} }}
                    }}
                }}
            }});
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            renderClasses();
            renderStudents();
            initCharts();

            document.getElementById('studentSearch').addEventListener('input', renderStudents);
            document.getElementById('classFilter').addEventListener('change', renderStudents);
            document.getElementById('riskFilter').addEventListener('change', renderStudents);
        }});
    </script>
</body>
</html>
"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Đã tạo: {out_path}")

def generate_ks25_fastapi_dashboard():
    """Tạo ks25/it105_fastapi_cntt.html từ file gốc kèm Top Navbar"""
    out_dir = os.path.join(BASE_ACADEMIC_DIR, "ks25")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "it105_fastapi_cntt.html")

    candidates = [
        os.path.join(out_dir, "it105_fastapi_cntt.html"),
        "output/dashboards/academic/bao_cao_chuyen_sau_fastapi_ks25.html",
        "deploy_web/academic/ks25/it105_fastapi_cntt.html"
    ]
    src_file = next((c for c in candidates if os.path.exists(c)), None)
    if not src_file:
        print("✗ Không tìm thấy file nguồn FastAPI!")
        return

    with open(src_file, "r", encoding="utf-8") as f:
        html = f.read()

    # Thay thế phần action header bằng Top Navbar
    navbar_html = get_top_navbar("ks25_fastapi")
    old_header_pattern = """            <div class="flex items-center space-x-3">
                <span class="text-xs text-slate-300 bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700 flex items-center gap-2 font-mono">
                    <i class="fa-regular fa-calendar-check text-indigo-400"></i> Dữ liệu: 16/09/2026
                </span>
                <button onclick="window.print()" class="text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-3.5 py-1.5 rounded-lg shadow-md shadow-indigo-500/20 transition flex items-center gap-1.5">
                    <i class="fa-solid fa-print"></i> In Báo Cáo
                </button>
            </div>"""

    new_header_content = f"""            <div class="flex items-center space-x-3">
                {navbar_html}
                <button onclick="window.print()" class="text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-3.5 py-1.5 rounded-lg shadow-md transition flex items-center gap-1.5">
                    <i class="fa-solid fa-print"></i> In Báo Cáo
                </button>
            </div>"""

    if old_header_pattern in html:
        html = html.replace(old_header_pattern, new_header_content)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Đã tạo: {out_path}")

def generate_ks25_man107_dashboard():
    """Tạo ks25/man107_qtkd.html - Báo cáo Chuyên sâu Môn Quản trị chiến lược MAN107 (Khóa KS25 QTKD)"""
    out_dir = os.path.join(BASE_ACADEMIC_DIR, "ks25")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "man107_qtkd.html")

    navbar_html = get_top_navbar("ks25_man107")

    classes_data = [
        {"name": "HN-K25-QTKD1", "size": 46, "gv": "Đặng Quỳnh Trang", "tg": "Đặng Quỳnh Trang", "att_v": 52.17, "hw_v": 10.87, "el_v": 15.22, "pred_pass": 62.4, "care_count": 16, "status": "CRITICAL", "issue": "Vắng chuyên cần tăng vọt lên 52.17% (24/46 SV vắng) - Báo động Đỏ"},
        {"name": "HN-K25-QTKD2", "size": 42, "gv": "Đặng Quỳnh Trang", "tg": "Lê Thành Ngọc", "att_v": 33.33, "hw_v": 14.29, "el_v": 26.19, "pred_pass": 68.1, "care_count": 12, "status": "RED", "issue": "Vắng chuyên cần 33.33% và nợ Elearning 26.19%"}
    ]

    students_care = [
        {"class": "HN-K25-QTKD1", "name": "Nguyễn Hoàng Minh", "att": 60, "hw": 75, "el": 50, "p_pred": 52.0, "risk": "RED", "reason": "Vắng chuyên cần 3 buổi, không chuẩn bị Elearning", "action": "CVHT gọi điện phụ huynh, giao bài tập tình huống gỡ điểm"},
        {"class": "HN-K25-QTKD1", "name": "Trần Thị Mai Anh", "att": 40, "hw": 50, "el": 0, "p_pred": 45.0, "risk": "RED", "reason": "Vắng 60% buổi học, bỏ Elearning", "action": "Cảnh báo cấm thi, buộc cam kết học bù"},
        {"class": "HN-K25-QTKD1", "name": "Lê Quốc Bảo", "att": 80, "hw": 80, "el": 50, "p_pred": 65.0, "risk": "YELLOW", "reason": "Nợ Elearning giữa kỳ", "action": "Đôn đốc hoàn thành bài trắc nghiệm"},
        {"class": "HN-K25-QTKD1", "name": "Vũ Minh Phương", "att": 60, "hw": 100, "el": 50, "p_pred": 58.0, "risk": "ORANGE", "reason": "Vắng 40% buổi học dù BTVN tốt", "action": "Nhắc nhở nề nếp chuyên cần"},
        {"class": "HN-K25-QTKD2", "name": "Đỗ Thu Trang", "att": 60, "hw": 50, "el": 25, "p_pred": 48.0, "risk": "RED", "reason": "Vắng 40%, nợ bài tập phân tích chiến lược SWOT", "action": "Yêu cầu nộp bù bài tập nhóm"},
        {"class": "HN-K25-QTKD2", "name": "Phạm Gia Huy", "att": 80, "hw": 75, "el": 50, "p_pred": 62.0, "risk": "YELLOW", "reason": "Điểm rpoint cận chuẩn", "action": "GV Trang kiểm tra vấn đáp"},
        {"class": "HN-K25-QTKD2", "name": "Hoàng Kim Ngân", "att": 40, "hw": 50, "el": 0, "p_pred": 44.0, "risk": "RED", "reason": "Vắng chuyên cần quá 30% ngưỡng an toàn", "action": "Gửi thông báo cảnh báo học vụ"}
    ]

    classes_json = json.dumps(classes_data, ensure_ascii=False)
    students_json = json.dumps(students_care, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Chuyên Sâu Học Vụ: Môn Quản Trị Chiến Lược MAN107 (Khóa KS25 QTKD)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        slate: {{ 850: '#111622', 900: '#0b0f19', 950: '#06080e' }},
                        indigo: {{ 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca' }}
                    }}
                }}
            }}
        }}
    </script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #06080e; color: #cbd5e1; font-size: 13px; }}
        code, pre, .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        .custom-scrollbar::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: #0b0f19; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #26324a; border-radius: 3px; }}
        .glass-card {{ background: rgba(15, 20, 31, 0.85); backdrop-filter: blur(12px); border: 1px solid #1e283d; }}
        .glass-card:hover {{ border-color: #334155; }}
        .tab-btn.active {{ background-color: #4f46e5; color: #ffffff; border-color: #6366f1; font-weight: 600; }}
        .metric-card {{ background: linear-gradient(180deg, rgba(22, 28, 45, 0.75) 0%, rgba(15, 20, 31, 0.9) 100%); border: 1px solid #1e293b; }}
        .funnel-step {{ position: relative; }}
        .funnel-step:not(:last-child)::after {{
            content: '➔';
            position: absolute;
            right: -14px;
            top: 50%;
            transform: translateY(-50%);
            color: #64748b;
            font-size: 14px;
            font-weight: bold;
            z-index: 10;
        }}
        @media (max-width: 768px) {{
            .funnel-step:not(:last-child)::after {{ display: none; }}
        }}
    </style>
</head>
<body class="min-h-screen custom-scrollbar antialiased selection:bg-indigo-500 selection:text-white">

    <!-- HEADER HỌC VỤ KS25 QTKD -->
    <header class="border-b border-slate-800 bg-slate-900/90 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-600 to-orange-500 flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-amber-500/20">
                    <i class="fa-solid fa-briefcase"></i>
                </div>
                <div>
                    <h1 class="text-base font-bold text-white tracking-tight flex items-center gap-2">
                        BÁO CÁO TOÀN CẢNH HỌC VỤ: MÔN QUẢN TRỊ CHIẾN LƯỢC MAN107
                        <span class="text-xs bg-amber-500/20 text-amber-300 border border-amber-500/30 px-2 py-0.5 rounded font-mono">Khóa KS25 QTKD</span>
                    </h1>
                    <p class="text-xs text-slate-400">Báo động đỏ điểm nghẽn vắng chuyên cần tăng vọt (52.17% & 33.33%) và danh sách can thiệp</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                {navbar_html}
                <button onclick="window.print()" class="text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-3.5 py-1.5 rounded-lg shadow-md transition flex items-center gap-1.5">
                    <i class="fa-solid fa-print"></i> In Báo Cáo
                </button>
            </div>
        </div>
    </header>

    <!-- NAVIGATION TABS -->
    <div class="border-b border-slate-800 bg-slate-950/80 sticky top-16 z-40 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav class="flex space-x-2 py-2.5 overflow-x-auto custom-scrollbar" id="nav-tabs">
                <button onclick="switchTab('tab-macro')" class="tab-btn active px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-filter"></i> I. Điểm Nóng Chuyên Cần & Tổng Quan
                </button>
                <button onclick="switchTab('tab-classes')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-chalkboard-user"></i> II. Ma Trận 2 Lớp QTKD
                </button>
                <button onclick="switchTab('tab-students')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2 text-rose-300">
                    <i class="fa-solid fa-table-list"></i> III. Tra Cứu Sinh Viên Báo Động
                </button>
            </nav>
        </div>
    </div>

    <!-- MAIN BODY -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <section id="tab-macro" class="tab-content space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="metric-card rounded-xl p-4 flex flex-col justify-between">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>TỔNG SĨ SỐ (2 LỚP QTKD)</span>
                        <i class="fa-solid fa-users text-indigo-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-white font-mono">88 <span class="text-xs text-slate-400 font-normal">SV</span></div>
                        <p class="text-xs text-slate-400 mt-1">QTKD1: 46 SV | QTKD2: 42 SV</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between border-rose-900/50 bg-rose-950/20">
                    <div class="flex items-center justify-between text-rose-300 text-xs font-semibold">
                        <span>TỶ LỆ VẮNG CHUYÊN CẦN CAO NHẤT</span>
                        <i class="fa-solid fa-triangle-exclamation text-rose-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-rose-400 font-mono">52.17%</div>
                        <p class="text-xs text-rose-300 mt-1 font-medium">Lớp QTKD1 (24/46 SV vắng) - Báo động Đỏ</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between border-amber-900/50 bg-amber-950/20">
                    <div class="flex items-center justify-between text-amber-300 text-xs font-semibold">
                        <span>NỢ ELEARNING LỚP QTKD2</span>
                        <i class="fa-solid fa-clock-rotate-left text-amber-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-amber-400 font-mono">26.19%</div>
                        <p class="text-xs text-amber-300 mt-1 font-medium">11/42 SV chưa hoàn thành chuẩn bị bài</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>DỰ BÁO QUA MÔN KỲ VỌNG</span>
                        <i class="fa-solid fa-award text-emerald-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-emerald-400 font-mono">65.2%</div>
                        <p class="text-xs text-emerald-300 mt-1 font-medium">Nếu kịp thời chấn chỉnh chuyên cần</p>
                    </div>
                </div>
            </div>

            <!-- ALERT BOX -->
            <div class="bg-rose-950/40 border border-rose-800/60 rounded-xl p-5 flex items-start gap-4">
                <div class="w-10 h-10 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center text-lg flex-shrink-0">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                </div>
                <div>
                    <h4 class="text-sm font-bold text-rose-300">CẢNH BÁO HỌC VỤ: KHỐI QTKD ĐANG CÓ HIỆN TƯỢNG XẢ HƠI NGUY HIỂM</h4>
                    <p class="text-xs text-slate-300 mt-1 leading-relaxed">
                        Tỷ lệ vắng mặt tại lớp HN-K25-QTKD1 ngày 23/09 đạt mức kỷ lục <strong>52.17% (24/46 sinh viên)</strong> và QTKD2 vắng <strong>33.33%</strong>. Sinh viên có dấu hiệu chểnh mảng giai đoạn giữa kỳ môn Chiến lược. Đề nghị Giảng viên Đặng Quỳnh Trang và Trợ giảng Lê Thành Ngọc thực hiện rà soát điểm danh chéo và gọi điện cảnh báo trực tiếp cho từng sinh viên.
                    </p>
                </div>
            </div>

            <!-- CHARTS -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-card rounded-xl p-5">
                    <h3 class="text-sm font-bold text-white mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-chart-column text-indigo-400"></i>
                        So Sánh Chỉ Số Vi Phạm Giữa 2 Lớp QTKD (%)
                    </h3>
                    <div class="h-64">
                        <canvas id="man107BarChart"></canvas>
                    </div>
                </div>

                <div class="glass-card rounded-xl p-5">
                    <h3 class="text-sm font-bold text-white mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-shield-halved text-indigo-400"></i>
                        Đề Xuất Hành Động Can Thiệp Trọng Tâm
                    </h3>
                    <div class="space-y-3 text-xs text-slate-300 pt-2">
                        <div class="p-3 bg-slate-900/80 rounded-lg border border-slate-800 flex items-start gap-3">
                            <i class="fa-solid fa-phone text-rose-400 mt-1"></i>
                            <div>
                                <strong class="text-white">1. CVHT liên hệ phụ huynh 24 sinh viên vắng:</strong>
                                <p class="text-slate-400 mt-0.5">Xác minh nguyên nhân vắng học, lập biên bản cam kết chuyên cần từ buổi học tới.</p>
                            </div>
                        </div>
                        <div class="p-3 bg-slate-900/80 rounded-lg border border-slate-800 flex items-start gap-3">
                            <i class="fa-solid fa-clipboard-check text-amber-400 mt-1"></i>
                            <div>
                                <strong class="text-white">2. Bổ sung bài tập tình huống bù đắp chuyên cần:</strong>
                                <p class="text-slate-400 mt-0.5">Giao phân tích Case Study chiến lược VinFast/Viettel để SV nộp bù gỡ nợ bài tập.</p>
                            </div>
                        </div>
                        <div class="p-3 bg-slate-900/80 rounded-lg border border-slate-800 flex items-start gap-3">
                            <i class="fa-solid fa-lock text-indigo-400 mt-1"></i>
                            <div>
                                <strong class="text-white">3. Chốt chặn ngưỡng cấm thi 20%:</strong>
                                <p class="text-slate-400 mt-0.5">Nếu SV vắng thêm 1 buổi nữa sẽ vượt quá 20% thời lượng môn học và bị cấm thi theo quy chế.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section id="tab-classes" class="tab-content space-y-6 hidden">
            <div class="glass-card rounded-xl p-6">
                <h3 class="text-base font-bold text-white mb-4 flex items-center gap-2">
                    <i class="fa-solid fa-chalkboard-user text-indigo-400"></i>
                    Ma Trận Chỉ Số 2 Lớp Khối KS25 QTKD
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-400 bg-slate-900/50">
                                <th class="p-3">Lớp Học</th>
                                <th class="p-3">Sĩ Số</th>
                                <th class="p-3">Giảng Viên & Trợ Giảng</th>
                                <th class="p-3 text-center">Vắng CC (%)</th>
                                <th class="p-3 text-center">Nợ BT (%)</th>
                                <th class="p-3 text-center">Elearning (%)</th>
                                <th class="p-3 text-center">Dự Báo Đỗ Mới</th>
                                <th class="p-3 text-center">Care List</th>
                                <th class="p-3">Đánh Giá Trạng Thái</th>
                            </tr>
                        </thead>
                        <tbody id="man107TableBody" class="divide-y divide-slate-800/60 text-xs font-mono">
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <section id="tab-students" class="tab-content space-y-6 hidden">
            <div class="glass-card rounded-xl p-6">
                <h3 class="text-base font-bold text-white mb-4 flex items-center gap-2">
                    <i class="fa-solid fa-table-list text-indigo-400"></i>
                    Danh Sách Sinh Viên Thuộc Diện Báo Động (Khối QTKD)
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-400 bg-slate-900/50">
                                <th class="p-3">#</th>
                                <th class="p-3">Lớp</th>
                                <th class="p-3">Họ và Tên</th>
                                <th class="p-3 text-center">CC (%)</th>
                                <th class="p-3 text-center">BTVN (%)</th>
                                <th class="p-3 text-center">EL (%)</th>
                                <th class="p-3 text-center">Dự Báo Đỗ</th>
                                <th class="p-3 text-center">Mức Rủi Ro</th>
                                <th class="p-3">Lý Do Vi Phạm</th>
                                <th class="p-3">Hành Động Khuyến Nghị</th>
                            </tr>
                        </thead>
                        <tbody id="man107StudentsBody" class="divide-y divide-slate-800/60 text-xs">
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
    </main>

    <script>
        const rawClasses = {classes_json};
        const rawStudents = {students_json};

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabId).classList.remove('hidden');
            event.currentTarget.classList.add('active');
        }}

        function renderClasses() {{
            const tbody = document.getElementById('man107TableBody');
            tbody.innerHTML = rawClasses.map(c => `
                <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-bold text-white">${{c.name}}</td>
                    <td class="p-3">${{c.size}} SV</td>
                    <td class="p-3 font-sans">${{c.gv}} | TG: ${{c.tg}}</td>
                    <td class="p-3 text-center text-rose-400 font-bold">${{c.att_v}}%</td>
                    <td class="p-3 text-center text-slate-300">${{c.hw_v}}%</td>
                    <td class="p-3 text-center text-amber-400 font-bold">${{c.el_v}}%</td>
                    <td class="p-3 text-center font-bold text-emerald-400">${{c.pred_pass}}%</td>
                    <td class="p-3 text-center font-bold text-amber-400">${{c.care_count}} SV</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-sans font-semibold">${{c.issue}}</span></td>
                </tr>
            `).join('');
        }}

        function renderStudents() {{
            const tbody = document.getElementById('man107StudentsBody');
            tbody.innerHTML = rawStudents.map((s, idx) => `
                <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 text-slate-500 font-mono">${{idx + 1}}</td>
                    <td class="p-3 font-mono font-bold text-slate-300">${{s.class}}</td>
                    <td class="p-3 font-semibold text-white">${{s.name}}</td>
                    <td class="p-3 text-center font-mono ${{s.att < 70 ? 'text-rose-400 font-bold' : 'text-slate-300'}}">${{s.att}}%</td>
                    <td class="p-3 text-center font-mono">${{s.hw}}%</td>
                    <td class="p-3 text-center font-mono ${{s.el < 50 ? 'text-amber-400' : 'text-slate-300'}}">${{s.el}}%</td>
                    <td class="p-3 text-center font-mono font-bold ${{s.p_pred < 50 ? 'text-rose-400' : 'text-emerald-400'}}">${{s.p_pred}}%</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold">${{s.risk}}</span></td>
                    <td class="p-3 text-slate-300 text-xs">${{s.reason}}</td>
                    <td class="p-3 text-slate-400 text-xs">${{s.action}}</td>
                </tr>
            `).join('');
        }}

        function initCharts() {{
            const ctx = document.getElementById('man107BarChart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['Vắng Chuyên Cần', 'Nợ BTVN', 'Nợ Elearning'],
                    datasets: [
                        {{
                            label: 'HN-K25-QTKD1 (%)',
                            data: [52.17, 10.87, 15.22],
                            backgroundColor: '#f43f5e',
                            borderRadius: 6
                        }},
                        {{
                            label: 'HN-K25-QTKD2 (%)',
                            data: [33.33, 14.29, 26.19],
                            backgroundColor: '#f59e0b',
                            borderRadius: 6
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
                    }},
                    plugins: {{
                        legend: {{ labels: {{ color: '#94a3b8' }} }}
                    }}
                }}
            }});
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            renderClasses();
            renderStudents();
            initCharts();
        }});
    </script>
</body>
</html>
"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Đã tạo: {out_path}")

def generate_ks26_dashboards():
    """Tạo ks26/ssk101_cntt.html và ks26/ssk101_qtkd.html"""
    out_dir = os.path.join(BASE_ACADEMIC_DIR, "ks26")
    os.makedirs(out_dir, exist_ok=True)

    # 1. Báo cáo KS26 CNTT (6 lớp)
    cntt_classes = [
        {"name": "HN-KS26-CNTT1", "size": 43, "eligible": 27, "not_eligible": 16, "unknown": 0, "gv": "Trần Minh Cường", "dept": "Khối CNTT", "p_fail": 37.2, "status": "RED", "issue": "BTVN nộp rất thấp (0-25%), Elearning chỉ 25-75%"},
        {"name": "HN-K26-CNTT2", "size": 43, "eligible": 40, "not_eligible": 3, "unknown": 0, "gv": "Hồ Xuân Hùng", "dept": "Khối CNTT", "p_fail": 7.0, "status": "GREEN", "issue": "Lớp xuất sắc số 1 khóa KS26, kỷ luật nề nếp vượt trội"},
        {"name": "HN-K26-CNTT3", "size": 41, "eligible": 24, "not_eligible": 9, "unknown": 8, "gv": "Nguyễn Duy Quang", "dept": "Khối CNTT", "p_fail": 22.0, "status": "RED", "issue": "Có 8 SV lỗi dữ liệu LMS chưa định danh + 9 SV nợ bài"},
        {"name": "HN-K26-CNTT4", "size": 22, "eligible": 0, "not_eligible": 0, "unknown": 0, "gv": "Lương Quốc Tuấn", "dept": "Khối CNTT", "p_fail": 0.0, "status": "GRAY", "issue": "Lớp mới khởi tạo, chuẩn bị vào môn SSK101"},
        {"name": "HCM-KS26-CNTT1", "size": 47, "eligible": 26, "not_eligible": 21, "unknown": 0, "gv": "Nguyễn Bá Minh Đạo", "dept": "Khối CNTT", "p_fail": 44.7, "status": "CRITICAL", "issue": "🚨 Báo động Đỏ: Gần 1/2 lớp (21 SV) cấm thi vì BTVN 0% & vắng nặng"},
        {"name": "HCM-KS26-CNTT2", "size": 45, "eligible": 38, "not_eligible": 7, "unknown": 0, "gv": "Nguyễn Bá Minh Đạo", "dept": "Khối CNTT", "p_fail": 15.6, "status": "YELLOW", "issue": "Khá hơn lớp 1, 7 SV nợ BTVN hoàn toàn (0%)"}
    ]

    # 2. Báo cáo KS26 QTKD (4 lớp)
    qtkd_classes = [
        {"name": "HN-K26-QTKD1", "size": 44, "eligible": 37, "not_eligible": 7, "unknown": 0, "gv": "Hoàng Thị Hậu", "dept": "Khối QTKD", "p_fail": 15.9, "status": "YELLOW", "issue": "BTVN tốt (91.7%), 7 SV nợ Elearning và vắng chuyên cần"},
        {"name": "HN-K26-QTKD2", "size": 44, "eligible": 36, "not_eligible": 8, "unknown": 0, "gv": "Hoàng Thị Kim Oanh", "dept": "Khối QTKD", "p_fail": 18.2, "status": "YELLOW", "issue": "Nợ Elearning 61.38%, cần đôn đốc chuẩn bị bài trước buổi học"},
        {"name": "HN-K26-QTKD3", "size": 44, "eligible": 35, "not_eligible": 9, "unknown": 0, "gv": "Hoàng Thị Hậu", "dept": "Khối QTKD", "p_fail": 20.5, "status": "YELLOW", "issue": "Vắng chuyên cần 12.7%, 9 SV bị trừ R-Point dưới 80"},
        {"name": "HCM-KS26-QTKD1", "size": 23, "eligible": 20, "not_eligible": 3, "unknown": 0, "gv": "Lê Nhựt Mi", "dept": "Khối QTKD", "p_fail": 13.0, "status": "GREEN", "issue": "Lớp top 2 toàn khóa (87.0% đủ ĐK), sĩ số gọn, nề nếp ổn định"}
    ]

    # Danh sách sinh viên
    all_students_ineligible = [
        # HN-KS26-CNTT1
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Mai Ngọc Đức Hải", "cc": 100, "bt": 0, "el": 50, "rp": 50, "reason": "Nợ 100% BTVN, Elearning chỉ 50%", "can_guarantee": True, "action": "Cho nộp bù BTVN trước giờ thi, duyệt bảo lãnh"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Đặng Quang Anh", "cc": 100, "bt": 0, "el": 50, "rp": 50, "reason": "Nợ 100% BTVN, Elearning chỉ 50%", "can_guarantee": True, "action": "Cho nộp bù BTVN, làm cam kết bảo lãnh"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Trần Bình An", "cc": 40, "bt": 25, "el": 50, "rp": 70, "reason": "Vắng 60% chuyên cần, nợ 75% BTVN", "can_guarantee": False, "action": "Học lại thực chất, không đủ cơ sở bảo lãnh"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Phạm Gia Bảo 3", "cc": 80, "bt": 0, "el": 50, "rp": 50, "reason": "Nợ 100% BTVN, vắng 1 buổi", "can_guarantee": True, "action": "Làm bài tập bổ sung, GV ký bảo lãnh"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Phạm Quốc Đạt", "cc": 100, "bt": 25, "el": 75, "rp": 75, "reason": "Thiếu bài tập về nhà (chỉ đạt 25%)", "can_guarantee": True, "action": "Bảo lãnh ngay, SV chuyên cần 100%"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Nguyễn Tiến Duy 2", "cc": 60, "bt": 0, "el": 50, "rp": 70, "reason": "Vắng 40% buổi học, không làm BTVN", "can_guarantee": False, "action": "Xem xét học lại hoặc kèm bù giờ công"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Đỗ Phạm Gia Hiếu", "cc": 40, "bt": 0, "el": 0, "rp": 40, "reason": "Bỏ học: CC 40%, BT 0%, EL 0%", "can_guarantee": False, "action": "Cấm thi chính thức, đưa vào danh sách bảo lưu"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Trần Mạnh Hoa", "cc": 100, "bt": 25, "el": 50, "rp": 70, "reason": "Nợ 75% BTVN, Elearning 50%", "can_guarantee": True, "action": "Bảo lãnh có điều kiện nộp đủ bài tập"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Diêm Quang Huy", "cc": 80, "bt": 0, "el": 25, "rp": 40, "reason": "Nợ BTVN 100%, EL chỉ 25%", "can_guarantee": False, "action": "Cần hoàn thành 3 bài tập gấp trước khi xét"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Đường Gia Huy", "cc": 100, "bt": 0, "el": 50, "rp": 50, "reason": "Nợ 100% BTVN, CC đạt 100%", "can_guarantee": True, "action": "Bảo lãnh ngay, hướng dẫn nộp bài LMS"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Nguyễn Vương Anh Minh", "cc": 100, "bt": 25, "el": 75, "rp": 75, "reason": "CC 100%, RP 75 cận ngưỡng", "can_guarantee": True, "action": "Ưu tiên duyệt bảo lãnh số 1"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Lê Minh Thảo", "cc": 100, "bt": 25, "el": 75, "rp": 75, "reason": "CC 100%, RP 75 cận ngưỡng", "can_guarantee": True, "action": "Ưu tiên duyệt bảo lãnh số 1"},
        {"class": "HN-KS26-CNTT1", "dept": "CNTT", "name": "Trần Đức Thiện 2", "cc": 100, "bt": 25, "el": 75, "rp": 75, "reason": "CC 100%, RP 75 cận ngưỡng", "can_guarantee": True, "action": "Ưu tiên duyệt bảo lãnh số 1"},
        
        # HN-K26-CNTT2
        {"class": "HN-K26-CNTT2", "dept": "CNTT", "name": "Trần Minh Tiến 2", "cc": 60, "bt": 0, "el": 100, "rp": 80, "reason": "Vắng CC 40%, không nộp BT", "can_guarantee": True, "action": "GV Hồ Xuân Hùng bảo lãnh sau khi test nhanh"},
        {"class": "HN-K26-CNTT2", "dept": "CNTT", "name": "Nguyễn Văn Đạt 4", "cc": 80, "bt": 25, "el": 75, "rp": 75, "reason": "Cận ngưỡng 75 RP", "can_guarantee": True, "action": "Bảo lãnh ngay"},
        {"class": "HN-K26-CNTT2", "dept": "CNTT", "name": "Lê Hoàng Long 3", "cc": 80, "bt": 0, "el": 100, "rp": 75, "reason": "Thiếu nộp BTVN", "can_guarantee": True, "action": "Bảo lãnh có điều kiện"},

        # HN-K26-CNTT3
        {"class": "HN-K26-CNTT3", "dept": "CNTT", "name": "Phạm Viết Toàn", "cc": 100, "bt": 50, "el": 100, "rp": 60, "reason": "RP 60 điểm (chưa đạt chuẩn 80)", "can_guarantee": True, "action": "Bảo lãnh có điều kiện"},
        {"class": "HN-K26-CNTT3", "dept": "CNTT", "name": "Nguyễn Thuận Phát", "cc": 100, "bt": 50, "el": 100, "rp": 60, "reason": "RP 60 điểm", "can_guarantee": True, "action": "Bảo lãnh có điều kiện"},
        {"class": "HN-K26-CNTT3", "dept": "CNTT", "name": "Hoàng Xuân Nam", "cc": 100, "bt": 50, "el": 100, "rp": 80, "reason": "Thiếu 1 bài tập", "can_guarantee": True, "action": "Duyệt bảo lãnh ngay"},
        {"class": "HN-K26-CNTT3", "dept": "CNTT", "name": "Bùi Quang Huy 2", "cc": 80, "bt": 75, "el": 100, "rp": 60, "reason": "RP 60 điểm", "can_guarantee": True, "action": "Bảo lãnh ngay"},
        {"class": "HN-K26-CNTT3", "dept": "CNTT", "name": "Nguyễn Trường Khang", "cc": 60, "bt": 100, "el": 100, "rp": 80, "reason": "Vắng 40% buổi học", "can_guarantee": False, "action": "Học bù chuyên cần"},

        # HCM-KS26-CNTT1 (21 SV)
        {"class": "HCM-KS26-CNTT1", "dept": "CNTT", "name": "Vũ Trung Hiếu 2", "cc": 20, "bt": 0, "el": 0, "rp": 51, "reason": "Vắng 80% buổi, bỏ học phần", "can_guarantee": False, "action": "Cấm thi chính thức"},
        {"class": "HCM-KS26-CNTT1", "dept": "CNTT", "name": "Khưu Nhật Tân", "cc": 80, "bt": 25, "el": 50, "rp": 75, "reason": "RP 75 cận chuẩn 80", "can_guarantee": True, "action": "Bảo lãnh ngay"},
        {"class": "HCM-KS26-CNTT1", "dept": "CNTT", "name": "Trần Tiến Đạt 3", "cc": 80, "bt": 25, "el": 50, "rp": 78, "reason": "RP 78 cận chuẩn 80", "can_guarantee": True, "action": "Bảo lãnh ngay"},
        {"class": "HCM-KS26-CNTT1", "dept": "CNTT", "name": "Bùi Gia Anh", "cc": 20, "bt": 0, "el": 0, "rp": 50, "reason": "Vắng 80% buổi học", "can_guarantee": False, "action": "Cấm thi"},
        {"class": "HCM-KS26-CNTT1", "dept": "CNTT", "name": "Trần Văn Gia Khang", "cc": 80, "bt": 0, "el": 50, "rp": 75, "reason": "Nợ 100% BTVN, CC 80%", "can_guarantee": True, "action": "Cho nộp bù BTVN để bảo lãnh"},
        {"class": "HCM-KS26-CNTT1", "dept": "CNTT", "name": "Bùi Minh Hoàng 2", "cc": 100, "bt": 25, "el": 0, "rp": 73, "reason": "Chưa làm Elearning", "can_guarantee": True, "action": "Bảo lãnh ngay, hoàn thành EL"},
        {"class": "HCM-KS26-CNTT1", "dept": "CNTT", "name": "Dương Công Quốc", "cc": 100, "bt": 0, "el": 50, "rp": 55, "reason": "CC 100%, nợ BTVN", "can_guarantee": True, "action": "Bảo lãnh ngay"},
        {"class": "HCM-KS26-CNTT1", "dept": "CNTT", "name": "Trần Hoàng Ân", "cc": 100, "bt": 0, "el": 50, "rp": 76, "reason": "CC 100%, RP 76", "can_guarantee": True, "action": "Bảo lãnh ngay"},

        # HCM-KS26-CNTT2
        {"class": "HCM-KS26-CNTT2", "dept": "CNTT", "name": "Trần Quốc Khánh 2", "cc": 60, "bt": 0, "el": 0, "rp": 40, "reason": "Vắng 40%, nợ BT", "can_guarantee": False, "action": "Học bù chuyên cần"},
        {"class": "HCM-KS26-CNTT2", "dept": "CNTT", "name": "Phan Nguyễn Gia Bảo", "cc": 100, "bt": 25, "el": 75, "rp": 75, "reason": "RP 75 cận chuẩn 80", "can_guarantee": True, "action": "Bảo lãnh ngay"},

        # HN-K26-QTKD3
        {"class": "HN-K26-QTKD3", "dept": "QTKD", "name": "Nguyễn Trung Hiếu", "cc": 40, "bt": 50, "el": 100, "rp": 60, "reason": "Vắng 60% chuyên cần", "can_guarantee": False, "action": "Cấm thi do quá số buổi vắng"},
        {"class": "HN-K26-QTKD3", "dept": "QTKD", "name": "Trịnh Bảo Châu", "cc": 80, "bt": 75, "el": 100, "rp": 80, "reason": "Điểm rpoint khóa tạm", "can_guarantee": True, "action": "Mở khóa hệ thống LMS"},
        {"class": "HN-K26-QTKD3", "dept": "QTKD", "name": "Vũ Minh Đức", "cc": 100, "bt": 0, "el": 100, "rp": 80, "reason": "Chưa nộp BTVN", "can_guarantee": True, "action": "Nộp bù bài tập, bảo lãnh ngay"},
        {"class": "HN-K26-QTKD3", "dept": "QTKD", "name": "Lâm Quang Trọng", "cc": 40, "bt": 75, "el": 67, "rp": 75, "reason": "Vắng chuyên cần 60%", "can_guarantee": False, "action": "Xem xét học bù"},

        # HCM-KS26-QTKD1
        {"class": "HCM-KS26-QTKD1", "dept": "QTKD", "name": "Nguyễn Ngọc Lan Anh", "cc": 40, "bt": 75, "el": 75, "rp": 85, "reason": "Vắng chuyên cần 60%", "can_guarantee": True, "action": "GV Lê Nhựt Mi bảo lãnh do năng lực tốt"},
        {"class": "HCM-KS26-QTKD1", "dept": "QTKD", "name": "Nguyễn Tường Vi", "cc": 20, "bt": 25, "el": 25, "rp": 40, "reason": "Bỏ học phần", "can_guarantee": False, "action": "Cấm thi"}
    ]

    # Sinh ks26/ssk101_cntt.html
    generate_single_ks26_html(
        cohort_dept="CNTT",
        classes=cntt_classes,
        students=[s for s in all_students_ineligible if s.get("dept") == "CNTT"],
        out_file=os.path.join(out_dir, "ssk101_cntt.html"),
        title="BÁO CÁO CHUYÊN SÂU HỌC VỤ: MÔN SSK101 (KHÓA KS26 CNTT)",
        subtitle="Kiểm toán điều kiện thi 6 lớp CNTT, mổ xẻ rào cản nợ BTVN 0-25% và danh sách bảo lãnh",
        nav_key="ks26_cntt",
        is_cntt=True
    )

    # Sinh ks26/ssk101_qtkd.html
    generate_single_ks26_html(
        cohort_dept="QTKD",
        classes=qtkd_classes,
        students=[s for s in all_students_ineligible if s.get("dept") == "QTKD"],
        out_file=os.path.join(out_dir, "ssk101_qtkd.html"),
        title="BÁO CÁO CHUYÊN SÂU HỌC VỤ: MÔN SSK101 (KHÓA KS26 QTKD)",
        subtitle="Kiểm toán điều kiện thi 4 lớp QTKD, rào cản chuyên cần và nợ Elearning",
        nav_key="ks26_qtkd",
        is_cntt=False
    )

def generate_single_ks26_html(cohort_dept, classes, students, out_file, title, subtitle, nav_key, is_cntt):
    navbar_html = get_top_navbar(nav_key)
    classes_json = json.dumps(classes, ensure_ascii=False)
    students_json = json.dumps(students, ensure_ascii=False)

    total_size = sum(c["size"] for c in classes)
    total_eligible = sum(c["eligible"] for c in classes)
    total_not = sum(c["not_eligible"] for c in classes)
    rate_fail = round(total_not / total_size * 100, 1) if total_size > 0 else 0.0

    html = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        slate: {{ 850: '#111622', 900: '#0b0f19', 950: '#06080e' }},
                        indigo: {{ 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca' }}
                    }}
                }}
            }}
        }}
    </script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #06080e; color: #cbd5e1; font-size: 13px; }}
        code, pre, .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        .custom-scrollbar::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: #0b0f19; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #26324a; border-radius: 3px; }}
        .glass-card {{ background: rgba(15, 20, 31, 0.85); backdrop-filter: blur(12px); border: 1px solid #1e283d; }}
        .glass-card:hover {{ border-color: #334155; }}
        .tab-btn.active {{ background-color: #4f46e5; color: #ffffff; border-color: #6366f1; font-weight: 600; }}
        .metric-card {{ background: linear-gradient(180deg, rgba(22, 28, 45, 0.75) 0%, rgba(15, 20, 31, 0.9) 100%); border: 1px solid #1e293b; }}
        .funnel-step {{ position: relative; }}
        .funnel-step:not(:last-child)::after {{
            content: '➔';
            position: absolute;
            right: -14px;
            top: 50%;
            transform: translateY(-50%);
            color: #64748b;
            font-size: 14px;
            font-weight: bold;
            z-index: 10;
        }}
        @media (max-width: 768px) {{
            .funnel-step:not(:last-child)::after {{ display: none; }}
        }}
    </style>
</head>
<body class="min-h-screen custom-scrollbar antialiased selection:bg-indigo-500 selection:text-white">

    <header class="border-b border-slate-800 bg-slate-900/90 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr {'from-emerald-600 to-teal-500' if is_cntt else 'from-amber-600 to-orange-500'} flex items-center justify-center text-white font-bold text-lg shadow-lg">
                    <i class="fa-solid {'fa-laptop-code' if is_cntt else 'fa-briefcase'}"></i>
                </div>
                <div>
                    <h1 class="text-base font-bold text-white tracking-tight flex items-center gap-2">
                        {title}
                        <span class="text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded font-mono">Khối {cohort_dept}</span>
                    </h1>
                    <p class="text-xs text-slate-400">{subtitle}</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                {navbar_html}
                <button onclick="window.print()" class="text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-3.5 py-1.5 rounded-lg shadow-md transition flex items-center gap-1.5">
                    <i class="fa-solid fa-print"></i> In Báo Cáo
                </button>
            </div>
        </div>
    </header>

    <div class="border-b border-slate-800 bg-slate-950/80 sticky top-16 z-40 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav class="flex space-x-2 py-2.5 overflow-x-auto custom-scrollbar" id="nav-tabs">
                <button onclick="switchTab('tab-macro')" class="tab-btn active px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-filter"></i> I. Bức Tranh Điều Kiện Thi
                </button>
                <button onclick="switchTab('tab-classes')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-chalkboard-user"></i> II. Ma Trận Các Lớp & Giảng Viên
                </button>
                <button onclick="switchTab('tab-guarantee')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2 text-rose-300">
                    <i class="fa-solid fa-signature"></i> III. Danh Sách Bảo Lãnh Khối {cohort_dept}
                </button>
            </nav>
        </div>
    </div>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <section id="tab-macro" class="tab-content space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="metric-card rounded-xl p-4 flex flex-col justify-between">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>TỔNG SĨ SỐ KHỐI {cohort_dept}</span>
                        <i class="fa-solid fa-users text-indigo-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-white font-mono">{total_size} <span class="text-xs text-slate-400 font-normal">SV</span></div>
                        <p class="text-xs text-slate-400 mt-1">{len(classes)} lớp học phần chính thức</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>ĐỦ ĐIỀU KIỆN DỰ THI</span>
                        <i class="fa-solid fa-circle-check text-emerald-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-emerald-400 font-mono">{total_eligible} <span class="text-xs text-slate-400 font-normal">SV</span></div>
                        <p class="text-xs text-emerald-300 mt-1 font-medium">{round(total_eligible/total_size*100, 1) if total_size>0 else 0}% đạt điều kiện thi</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between border-rose-900/50 bg-rose-950/20">
                    <div class="flex items-center justify-between text-rose-300 text-xs font-semibold">
                        <span>KHÔNG ĐỦ ĐIỀU KIỆN THI</span>
                        <i class="fa-solid fa-ban text-rose-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-rose-400 font-mono">{total_not} <span class="text-xs text-slate-400 font-normal">SV ({rate_fail}%)</span></div>
                        <p class="text-xs text-rose-300 mt-1 font-medium">Cần làm thủ tục bảo lãnh gấp</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between border-amber-900/50 bg-amber-950/20">
                    <div class="flex items-center justify-between text-amber-300 text-xs font-semibold">
                        <span>TỶ LỆ BẢO LÃNH HIỆN TẠI</span>
                        <i class="fa-solid fa-stamp text-amber-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-amber-400 font-mono">0% <span class="text-xs text-slate-400 font-normal">(0/{total_not} SV)</span></div>
                        <p class="text-xs text-amber-300 mt-1 font-medium">Chưa có SV nào được ký duyệt trên LMS</p>
                    </div>
                </div>
            </div>

            <!-- CHARTS -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-card rounded-xl p-5">
                    <h3 class="text-sm font-bold text-white mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-chart-pie text-indigo-400"></i>
                        Cơ Cấu Đủ / Không Đủ Điều Kiện Thi
                    </h3>
                    <div class="h-64 flex items-center justify-center">
                        <canvas id="cohortDoughnutChart"></canvas>
                    </div>
                </div>

                <div class="glass-card rounded-xl p-5">
                    <h3 class="text-sm font-bold text-white mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-chart-column text-indigo-400"></i>
                        Tỷ Lệ Không Đủ Điều Kiện Thi Theo Lớp (%)
                    </h3>
                    <div class="h-64">
                        <canvas id="cohortBarChart"></canvas>
                    </div>
                </div>
            </div>
        </section>

        <section id="tab-classes" class="tab-content space-y-6 hidden">
            <div class="glass-card rounded-xl p-6">
                <h3 class="text-base font-bold text-white mb-4 flex items-center gap-2">
                    <i class="fa-solid fa-chalkboard-user text-indigo-400"></i>
                    Ma Trận Các Lớp Học Khối {cohort_dept}
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-400 bg-slate-900/50">
                                <th class="p-3">Lớp Học</th>
                                <th class="p-3">Giảng Viên</th>
                                <th class="p-3 text-center">Sĩ Số</th>
                                <th class="p-3 text-center">Đủ ĐK Thi</th>
                                <th class="p-3 text-center">Không Đủ ĐK</th>
                                <th class="p-3 text-center">Tỷ Lệ Cấm Thi (%)</th>
                                <th class="p-3">Điểm Nghẽn & Đánh Giá</th>
                            </tr>
                        </thead>
                        <tbody id="cohortClassesBody" class="divide-y divide-slate-800/60 text-xs font-mono">
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <section id="tab-guarantee" class="tab-content space-y-6 hidden">
            <div class="glass-card rounded-xl p-6">
                <h3 class="text-base font-bold text-white mb-4 flex items-center gap-2">
                    <i class="fa-solid fa-table-list text-indigo-400"></i>
                    Danh Sách Sinh Viên Cần Bảo Lãnh Khối {cohort_dept}
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-400 bg-slate-900/50">
                                <th class="p-3">#</th>
                                <th class="p-3">Lớp</th>
                                <th class="p-3">Họ và Tên</th>
                                <th class="p-3 text-center">CC (%)</th>
                                <th class="p-3 text-center">BTVN (%)</th>
                                <th class="p-3 text-center">EL (%)</th>
                                <th class="p-3 text-center">R-Point</th>
                                <th class="p-3">Lý Do Vi Phạm</th>
                                <th class="p-3 text-center">Phương Án Bảo Lãnh</th>
                                <th class="p-3">Hành Động Khuyến Nghị</th>
                            </tr>
                        </thead>
                        <tbody id="cohortStudentsBody" class="divide-y divide-slate-800/60 text-xs">
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
    </main>

    <script>
        const rawClasses = {classes_json};
        const rawStudents = {students_json};

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabId).classList.remove('hidden');
            event.currentTarget.classList.add('active');
        }}

        function renderClasses() {{
            const tbody = document.getElementById('cohortClassesBody');
            tbody.innerHTML = rawClasses.map(c => `
                <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-bold text-white">${{c.name}}</td>
                    <td class="p-3 font-sans">${{c.gv}}</td>
                    <td class="p-3 text-center">${{c.size}}</td>
                    <td class="p-3 text-center font-bold text-emerald-400">${{c.eligible}}</td>
                    <td class="p-3 text-center font-bold ${{c.not_eligible > 5 ? 'text-rose-400' : 'text-slate-300'}}">${{c.not_eligible}}</td>
                    <td class="p-3 text-center font-bold ${{c.p_fail > 30 ? 'text-rose-400' : c.p_fail > 15 ? 'text-amber-400' : 'text-emerald-400'}}">${{c.p_fail}}%</td>
                    <td class="p-3 text-slate-300 text-xs font-sans">${{c.issue}}</td>
                </tr>
            `).join('');
        }}

        function renderStudents() {{
            const tbody = document.getElementById('cohortStudentsBody');
            tbody.innerHTML = rawStudents.map((s, idx) => `
                <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 text-slate-500 font-mono">${{idx + 1}}</td>
                    <td class="p-3 font-mono font-bold text-slate-300">${{s.class}}</td>
                    <td class="p-3 font-semibold text-white">${{s.name}}</td>
                    <td class="p-3 text-center font-mono ${{s.cc < 80 ? 'text-rose-400 font-bold' : 'text-slate-300'}}">${{s.cc}}%</td>
                    <td class="p-3 text-center font-mono ${{s.bt < 50 ? 'text-rose-400 font-bold' : 'text-slate-300'}}">${{s.bt}}%</td>
                    <td class="p-3 text-center font-mono ${{s.el < 50 ? 'text-amber-400' : 'text-slate-300'}}">${{s.el}}%</td>
                    <td class="p-3 text-center font-mono font-bold ${{s.rp < 60 ? 'text-rose-400' : 'text-amber-400'}}">${{s.rp}}</td>
                    <td class="p-3 text-slate-300 text-xs">${{s.reason}}</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded ${{s.can_guarantee ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'}} font-bold">${{s.can_guarantee ? 'Duyệt bảo lãnh' : 'Cấm thi'}}</span></td>
                    <td class="p-3 text-slate-400 text-xs">${{s.action}}</td>
                </tr>
            `).join('');
        }}

        function initCharts() {{
            const ctxDoughnut = document.getElementById('cohortDoughnutChart').getContext('2d');
            new Chart(ctxDoughnut, {{
                type: 'doughnut',
                data: {{
                    labels: ['Đủ ĐK Thi ({total_eligible})', 'Không Đủ ĐK ({total_not})'],
                    datasets: [{{
                        data: [{total_eligible}, {total_not}],
                        backgroundColor: ['#10b981', '#f43f5e'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ color: '#94a3b8' }} }}
                    }}
                }}
            }});

            const ctxBar = document.getElementById('cohortBarChart').getContext('2d');
            new Chart(ctxBar, {{
                type: 'bar',
                data: {{
                    labels: rawClasses.map(c => c.name.replace('HN-K26-', '').replace('HCM-KS26-', '')),
                    datasets: [{{
                        label: 'Tỷ Lệ Không Đủ ĐK Thi (%)',
                        data: rawClasses.map(c => c.p_fail),
                        backgroundColor: rawClasses.map(c => c.p_fail > 30 ? '#f43f5e' : c.p_fail > 15 ? '#f59e0b' : '#10b981'),
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            renderClasses();
            renderStudents();
            initCharts();
        }});
    </script>
</body>
</html>
"""

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Đã tạo: {out_file}")

def main():
    print("=" * 80)
    print("BẮT ĐẦU BIÊN DỊCH BÁO CÁO CHUYÊN SÂU THEO KHÓA (KS24, KS25, KS26)")
    print("=" * 80)
    generate_ks24_dashboard()
    generate_ks25_fastapi_dashboard()
    generate_ks25_man107_dashboard()
    generate_ks26_dashboards()
    print("✓ Đã hoàn tất biên dịch toàn bộ 5 báo cáo chuyên sâu học vụ vào ks24/, ks25/, ks26/!")

if __name__ == "__main__":
    main()

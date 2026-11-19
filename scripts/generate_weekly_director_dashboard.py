# -*- coding: utf-8 -*-
"""
Script: generate_weekly_director_dashboard.py
Mục đích: Tạo Dashboard Báo Cáo Giao Ban Đào Tạo Tuần chuyên biệt cho Giám đốc Đào tạo (Weekly Director Report V3)
Cập nhật theo yêu cầu chi tiết của Giám đốc Đào tạo:
  1. Tách riêng KS25 CNTT (FastAPI) và KS25 QTKD (MAN107).
  2. Bỏ toàn bộ cột Trợ giảng ở các bảng thống kê chỉ số (do Excel không ghi trợ giảng).
  3. Tối ưu kích cỡ chữ to rõ nét, có nút bật 'Chế độ Chụp Ảnh Báo Cáo' (Screenshot / Presentation Mode).
  4. Tab 3 KS26:
     - Bảng tổng hợp điều kiện thi & bảo lãnh theo từng lớp: Tổng SV, Đủ ĐK, Không đủ ĐK, Cần bảo lãnh, Đã làm đơn chưa duyệt (5 SV), Đã duyệt (4 SV), Tỷ lệ kỳ vọng.
     - Phân nhóm 371 SV theo 4 dải vi phạm [20-40%), [40-60%), [60-80%), [80-100%] cho CC, EL, BT.
     - Bảng tra cứu danh sách chi tiết sinh viên theo từng lớp và từng nhóm vi phạm để giao việc.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from weekly_latest_blocks import (build_academic_action_cards_html, build_ks26_current_courses_html, build_ks26_diagnosis_html,
                                  build_ks26_multicourse_html, build_latest_academic_html,
                                  build_latest_ks26_html, build_latest_worklane_html)

BASE_MGMT_DIR = "output/dashboards/management"
DEPLOY_DIR = "deploy_web"

def generate_weekly_director_dashboard():
    os.makedirs(BASE_MGMT_DIR, exist_ok=True)
    out_file = os.path.join(BASE_MGMT_DIR, "weekly_director_report.html")

    # Load dữ liệu kiểm toán phòng ban và công việc chung chung
    dept_file = "scratch/audit_departments_and_generic.json"
    audit_data = {}
    if os.path.exists(dept_file):
        with open(dept_file, "r", encoding="utf-8") as f:
            audit_data = json.load(f)

    dept_stats = audit_data.get("dept_stats", {})
    under_filtered = audit_data.get("under_filtered", [])
    generic_staff = audit_data.get("generic_staff", [])

    # Load dữ liệu KS26 V2 chuẩn hóa
    ks26_file = "scratch/ks26_v2_final.json"
    ks26_data = {}
    if os.path.exists(ks26_file):
        with open(ks26_file, "r", encoding="utf-8") as f:
            ks26_data = json.load(f)

    ks26_students = ks26_data.get("students", [])
    ks26_class_table = ks26_data.get("class_table", {})
    lms_9_students = ks26_data.get("lms_9_students", [])

    # Dữ liệu JSON nhúng vào HTML
    ks26_students_json = json.dumps(ks26_students, ensure_ascii=False)
    ks26_class_table_json = json.dumps(ks26_class_table, ensure_ascii=False)
    lms_9_students_json = json.dumps(lms_9_students, ensure_ascii=False)
    under_filtered_json = json.dumps(under_filtered, ensure_ascii=False)
    generic_staff_json = json.dumps(generic_staff, ensure_ascii=False)
    dept_stats_json = json.dumps(dept_stats, ensure_ascii=False)

    # Khối cập nhật mới nhất — sinh từ dữ liệu đã tính (không ghi cứng số)
    latest_academic_html = build_latest_academic_html()
    academic_action_cards_html = build_academic_action_cards_html()
    latest_worklane_html = build_latest_worklane_html()
    latest_ks26_html = build_latest_ks26_html()
    ks26_current_courses_html = build_ks26_current_courses_html()
    ks26_multicourse_html = build_ks26_multicourse_html()
    ks26_diagnosis_html = build_ks26_diagnosis_html()

    html = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Giao Ban Đào Tạo Tuần - Giám Đốc Đào Tạo</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{ 50: '#eef2ff', 100: '#e0e7ff', 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca', 900: '#312e81' }},
                        dark: {{ bg: '#0b0f19', card: '#111827', border: '#1f2937', hover: '#1e293b' }}
                    }}
                }}
            }}
        }}
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0b0f19; color: #f3f4f6; font-size: 14px; }}
        .glass-panel {{ background: rgba(17, 24, 39, 0.85); backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.1); }}
        .glass-card {{ background: rgba(30, 41, 59, 0.55); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.08); }}
        .tab-btn.active {{ background: #4f46e5; color: #ffffff; box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.4); font-weight: 700; }}
        .tab-btn:not(.active) {{ color: #94a3b8; }}
        .tab-btn:not(.active):hover {{ background: rgba(255, 255, 255, 0.08); color: #f8fafc; }}
        ::-webkit-scrollbar {{ width: 7px; height: 7px; }}
        ::-webkit-scrollbar-track {{ background: #0f172a; }}
        ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #6366f1; }}
        .badge-danger {{ background: rgba(239, 68, 68, 0.18); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }}
        .badge-warning {{ background: rgba(245, 158, 11, 0.18); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }}
        .badge-success {{ background: rgba(16, 185, 129, 0.18); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }}
        .badge-info {{ background: rgba(59, 130, 246, 0.18); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }}
        
        /* Chế độ chụp ảnh báo cáo (Screenshot Mode) */
        body.screenshot-mode {{ font-size: 16px !important; }}
        body.screenshot-mode .text-xs {{ font-size: 13px !important; }}
        body.screenshot-mode .text-sm {{ font-size: 15px !important; }}
        body.screenshot-mode .text-base {{ font-size: 17px !important; }}
        body.screenshot-mode th, body.screenshot-mode td {{ padding: 16px 20px !important; font-size: 14px !important; }}
        body.screenshot-mode header {{ position: relative !important; }}
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- TOP HEADER TỐI CAO -->
    <header class="sticky top-0 z-50 glass-panel border-b border-slate-800 px-6 py-4 shadow-2xl">
        <div class="max-w-[1750px] mx-auto flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
            
            <div class="flex items-center gap-4">
                <div class="w-13 h-13 p-3 rounded-2xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 flex items-center justify-center text-white text-2xl shadow-lg shadow-indigo-500/30">
                    <i class="fa-solid fa-chart-line"></i>
                </div>
                <div>
                    <div class="flex flex-wrap items-center gap-2.5">
                        <h1 class="text-xl lg:text-2xl font-black text-white tracking-tight">BÁO CÁO GIAO BAN ĐÀO TẠO TUẦN</h1>
                        <span class="px-3 py-1 rounded-full text-xs font-extrabold bg-rose-500/20 text-rose-300 border border-rose-500/40 flex items-center gap-1.5 shadow-sm">
                            <span class="w-2 h-2 rounded-full bg-rose-400 animate-pulse"></span> GIÁM ĐỐC ĐÀO TẠO
                        </span>
                        <span class="px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-slate-200 border border-slate-700 font-mono">
                            Tuần 05/10 &ndash; 12/10/2026
                        </span>
                    </div>
                    <p class="text-xs lg:text-sm text-slate-300 mt-1">
                        Phạm vi: <strong class="text-white">16 Lớp Học Kỳ II</strong> &bull; <strong class="text-white">42 Cán bộ GV/TG</strong> &bull; <strong class="text-white">1,236 Học viên PTIT</strong> &bull; Số liệu chốt 09/10/2026
                    </p>
                </div>
            </div>

            <!-- Actions & Fast Navigation -->
            <div class="flex flex-wrap items-center gap-2.5">
                <button onclick="toggleScreenshotMode()" id="btn-screenshot" class="px-3.5 py-2.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-amber-300 border border-amber-500/30 transition flex items-center gap-2 shadow-md">
                    <i class="fa-solid fa-camera"></i> <span id="screenshot-text">Phóng To Chụp Ảnh</span>
                </button>
                <a href="../academic/index.html" class="px-3.5 py-2.5 rounded-xl text-xs font-semibold bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-2">
                    <i class="fa-solid fa-graduation-cap text-indigo-400"></i> Cổng Học Vụ
                </a>
                <a href="../core/agent_5_master_portal.html" class="px-3.5 py-2.5 rounded-xl text-xs font-semibold bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-2">
                    <i class="fa-solid fa-house-laptop text-emerald-400"></i> Master Portal
                </a>
                <button onclick="copyBriefingSummary()" class="px-4 py-2.5 rounded-xl text-xs font-extrabold bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white transition flex items-center gap-2 shadow-lg shadow-indigo-600/30 active:scale-95" id="btn-copy">
                    <i class="fa-solid fa-copy"></i> Sao chép Tóm tắt Giao ban (Zalo/Slack)
                </button>
            </div>

        </div>
    </header>

    <!-- NAVIGATION TABS -->
    <div class="bg-slate-900/95 border-b border-slate-800 px-6 py-3 sticky top-[81px] z-40 backdrop-blur-md">
        <div class="max-w-[1750px] mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
            <div class="flex flex-wrap items-center gap-2">
                <button onclick="switchTab('tab-academic')" id="btn-tab-academic" class="tab-btn active px-4 py-2.5 rounded-xl text-xs lg:text-sm font-bold transition flex items-center gap-2">
                    <i class="fa-solid fa-book-open"></i> Tab 1: Kỷ Luật & Học Vụ (KS24, KS25 CNTT, KS25 QTKD, KS26)
                </button>
                <button onclick="switchTab('tab-daily')" id="btn-tab-daily" class="tab-btn px-4 py-2.5 rounded-xl text-xs lg:text-sm font-bold transition flex items-center gap-2">
                    <i class="fa-solid fa-user-clock"></i> Tab 2: Kiểm Toán Báo Cáo Ngày & Hiệu Suất 40h
                </button>
                <button onclick="switchTab('tab-ks26')" id="btn-tab-ks26" class="tab-btn px-4 py-2.5 rounded-xl text-xs lg:text-sm font-bold transition flex items-center gap-2">
                    <i class="fa-solid fa-shield-halved text-amber-400"></i> Tab 3: Chuyên Đề KS26 & 9 Đơn Bảo Lãnh LMS
                </button>
            </div>
            <div class="text-xs text-slate-400 font-mono hidden xl:block">
                <i class="fa-solid fa-database mr-1 text-slate-500"></i> Dữ liệu: PTIT_Chiso.xlsx + Worklane MCP + LMS Admin
            </div>
        </div>
    </div>

    <!-- MAIN BODY CONTAINER -->
    <main class="max-w-[1750px] mx-auto px-6 py-6 flex-1 w-full space-y-8">

        <!-- ========================================================================================= -->
        <!-- TAB 1: CHỈ SỐ HỌC VỤ & KỶ LUẬT                                                             -->
        <!-- ========================================================================================= -->
        <div id="tab-academic-content" class="space-y-8">
{latest_academic_html}

            {academic_action_cards_html}

            {ks26_current_courses_html}

            <!-- 3.2 KS26 ĐA MÔN — sinh từ result.json (weekly_latest_blocks.build_ks26_multicourse_html) -->
{ks26_multicourse_html}

            <!-- 3.3 KS26 CHẨN ĐOÁN LỚP — số từ M4 result.json, nhận định từ nhan_dinh.json -->
{ks26_diagnosis_html}

        </div>

        <!-- ========================================================================================= -->
        <!-- TAB 2: KIỂM TOÁN BÁO CÁO NGÀY & HIỆU SUẤT 40H                                             -->
        <!-- ========================================================================================= -->
        <div id="tab-daily-content" class="hidden space-y-8">
{latest_worklane_html}

            <!-- BANNER GIỚI THIỆU -->
            <div class="glass-panel p-5 rounded-2xl border-l-4 border-rose-500 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 class="text-base lg:text-lg font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-clock text-rose-400"></i> KIỂM TOÁN BÁO CÁO NGÀY WORKLANE & ĐỊNH MỨC 40H/TUẦN (28/09 &ndash; 02/10/2026)
                    </h2>
                    <p class="text-xs lg:text-sm text-slate-300 mt-1">
                        Tuần làm việc chuẩn 5 ngày (W39). Phân tích hiệu suất từng phòng ban, danh sách 17 nhân sự thiếu giờ và bóc tách các đầu việc khai báo chung chung.
                    </p>
                </div>
                <div class="flex items-center gap-3 text-xs">
                    <span class="px-3 py-1.5 rounded-lg bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 font-bold">16/42 NS Đạt &ge; 40h</span>
                    <span class="px-3 py-1.5 rounded-lg bg-rose-500/15 text-rose-300 border border-rose-500/30 font-bold">26/42 NS Chưa Đạt &lt; 40h</span>
                </div>
            </div>

            <!-- 1. THỐNG KÊ HIỆU SUẤT TỪNG PHÒNG BAN -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                <div class="flex items-center justify-between pb-3 border-b border-slate-800">
                    <div>
                        <h3 class="text-base lg:text-lg font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-sitemap text-indigo-400"></i> 1. Hiệu Suất Theo Từng Phòng Ban / Khối Đào Tạo
                        </h3>
                        <p class="text-xs text-slate-400">Đánh giá tiêu chí: Có đủ 40h/tuần/nhân sự không? Thiếu bao nhiêu giờ? Tỷ lệ báo cáo đạt chuẩn KPI Master.</p>
                    </div>
                </div>

                <div class="overflow-x-auto rounded-xl border border-slate-800">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                            <tr>
                                <th class="py-3.5 px-5">Tên Phòng Ban / Khối</th>
                                <th class="py-3.5 px-5 text-center">Tổng NS</th>
                                <th class="py-3.5 px-5 text-center">Giờ Chuẩn</th>
                                <th class="py-3.5 px-5 text-center">Giờ Khai Báo</th>
                                <th class="py-3.5 px-5 text-center">Giờ Thiếu Hụt</th>
                                <th class="py-3.5 px-5 text-center">Đạt Giờ (%)</th>
                                <th class="py-3.5 px-5 text-center">Đạt KPI Master (%)</th>
                                <th class="py-3.5 px-5 text-center">Kết Luận Điều Hành</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800">
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span> Khối CNTT Hà Nội
                                </td>
                                <td class="py-3.5 px-5 text-center text-slate-300 font-semibold">13 NS</td>
                                <td class="py-3.5 px-5 text-center text-slate-400 font-mono">520.0h</td>
                                <td class="py-3.5 px-5 text-center text-slate-200 font-mono font-bold">384.3h</td>
                                <td class="py-3.5 px-5 text-center text-rose-400 font-mono font-bold">-140.3h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">73.9%</td>
                                <td class="py-3.5 px-5 text-center font-bold text-indigo-400">81.7%</td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">❌ Không đủ (8/13 NS thiếu)</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-emerald-950/10">
                                <td class="py-3.5 px-5 font-bold text-white flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Khối Quản trị Kinh doanh
                                </td>
                                <td class="py-3.5 px-5 text-center text-slate-300 font-semibold">9 NS</td>
                                <td class="py-3.5 px-5 text-center text-slate-400 font-mono">360.0h</td>
                                <td class="py-3.5 px-5 text-center text-emerald-300 font-mono font-bold">354.5h</td>
                                <td class="py-3.5 px-5 text-center text-slate-300 font-mono font-bold">-8.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-emerald-400">98.5%</td>
                                <td class="py-3.5 px-5 text-center font-bold text-emerald-400">92.8%</td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-success">✅ Gần đạt chuẩn (Top 1)</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span> Khối Ngoại ngữ & KNM
                                </td>
                                <td class="py-3.5 px-5 text-center text-slate-300 font-semibold">7 NS</td>
                                <td class="py-3.5 px-5 text-center text-slate-400 font-mono">280.0h</td>
                                <td class="py-3.5 px-5 text-center text-slate-200 font-mono font-bold">208.0h</td>
                                <td class="py-3.5 px-5 text-center text-rose-400 font-mono font-bold">-87.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">74.3%</td>
                                <td class="py-3.5 px-5 text-center font-bold text-indigo-400">77.8%</td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">❌ Không đủ (3/7 NS thiếu)</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-rose-950/15">
                                <td class="py-3.5 px-5 font-bold text-rose-300 flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Khối QLCLĐT Hà Nội
                                </td>
                                <td class="py-3.5 px-5 text-center text-slate-300 font-semibold">4 NS</td>
                                <td class="py-3.5 px-5 text-center text-slate-400 font-mono">160.0h</td>
                                <td class="py-3.5 px-5 text-center text-rose-300 font-mono font-bold">65.5h</td>
                                <td class="py-3.5 px-5 text-center text-rose-400 font-mono font-bold">-94.5h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">40.9%</td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">60.3%</td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">❌ Báo động (Thiếu 94.5h)</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-cyan-500"></span> Khối CNTT HCM
                                </td>
                                <td class="py-3.5 px-5 text-center text-slate-300 font-semibold">7 NS</td>
                                <td class="py-3.5 px-5 text-center text-slate-400 font-mono">280.0h</td>
                                <td class="py-3.5 px-5 text-center text-slate-200 font-mono font-bold">219.3h</td>
                                <td class="py-3.5 px-5 text-center text-rose-400 font-mono font-bold">-60.8h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">78.3%</td>
                                <td class="py-3.5 px-5 text-center font-bold text-emerald-400">89.3%</td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">❌ Không đủ (7/7 NS thiếu nhẹ)</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-pink-500"></span> LMS AI
                                </td>
                                <td class="py-3.5 px-5 text-center text-slate-300 font-semibold">2 NS</td>
                                <td class="py-3.5 px-5 text-center text-slate-400 font-mono">80.0h</td>
                                <td class="py-3.5 px-5 text-center text-slate-200 font-mono font-bold">32.0h</td>
                                <td class="py-3.5 px-5 text-center text-rose-400 font-mono font-bold">-48.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">40.0%</td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">18.8%</td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">❌ Không đủ (Leader 0h)</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 2. DANH SÁCH NHÂN SỰ THIẾU 40H (ĐÃ LOẠI TRỪ LEADER, HUẤN, ĐỎ, NAM) -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                <div class="flex flex-col md:flex-row md:items-center justify-between pb-3 border-b border-slate-800 gap-3">
                    <div>
                        <h3 class="text-base lg:text-lg font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-user-xmark text-rose-400"></i> 2. Danh Sách Nhân Sự Chưa Đạt 40h/Tuần
                        </h3>
                        <p class="text-xs text-slate-400">
                            Bộ lọc chuẩn: <strong class="text-slate-200">Đã loại trừ toàn bộ Leader, Thầy Ngô Quang Huấn, Cô Lê Thị Đỏ, Thầy Đinh Thành Nam</strong>.
                        </p>
                    </div>
                    <span class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-rose-500/10 text-rose-400 border border-rose-500/30">
                        Chính xác: 17 Nhân sự
                    </span>
                </div>

                <div class="overflow-x-auto rounded-xl border border-slate-800">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                            <tr>
                                <th class="py-3.5 px-5 text-center w-12">STT</th>
                                <th class="py-3.5 px-5">Họ và Tên</th>
                                <th class="py-3.5 px-5">Phòng Ban / Khối</th>
                                <th class="py-3.5 px-5">Vai Trò</th>
                                <th class="py-3.5 px-5 text-center">Định Mức</th>
                                <th class="py-3.5 px-5 text-center">Khai Báo</th>
                                <th class="py-3.5 px-5 text-center">Thiếu Hụt</th>
                                <th class="py-3.5 px-5 text-center">Tỷ Lệ (%)</th>
                                <th class="py-3.5 px-5 text-center">Báo Cáo</th>
                                <th class="py-3.5 px-5 text-left">Đánh Giá & Giải Trình</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800">
                            <tr class="hover:bg-slate-800/40 bg-rose-950/20">
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">1</td>
                                <td class="py-3.5 px-5 font-bold text-rose-300">Nguyễn Huyền Trang</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối QLCLĐT Hà Nội</td>
                                <td class="py-3.5 px-5 text-slate-400">Giáo vụ</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">0.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">-40.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">0.0%</td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">0/5 ngày</td>
                                <td class="py-3.5 px-5 text-rose-300 font-semibold">🚨 Bỏ trống hoàn toàn cả tuần, không có báo cáo nào. Cần giải trình gấp.</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">2</td>
                                <td class="py-3.5 px-5 font-bold text-white">Phạm Ngọc Kiên</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT Hà Nội</td>
                                <td class="py-3.5 px-5 text-slate-400">Trợ giảng</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-amber-400">15.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">-25.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">37.5%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">5/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Nộp đủ 5 ngày nhưng mỗi ngày chỉ khai 2.5 - 3.5h, nhiều việc vụn vặt không đạt barem.</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">3</td>
                                <td class="py-3.5 px-5 font-bold text-white">Phạm Tuấn Bình</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT Hà Nội</td>
                                <td class="py-3.5 px-5 text-slate-400">Giảng viên</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-amber-400">24.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">-16.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">60.0%</td>
                                <td class="py-3.5 px-5 text-center text-rose-400 font-bold">3/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Quên nộp báo cáo 2 ngày làm việc trong tuần (thứ Ba và thứ Năm).</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">4</td>
                                <td class="py-3.5 px-5 font-bold text-white">Nguyễn Xuân Bách</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối QLCLĐT Hà Nội</td>
                                <td class="py-3.5 px-5 text-slate-400">Giảng viên</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-amber-400">25.5h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">-14.5h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">63.8%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">4/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Thiếu 1 ngày báo cáo; các việc dự giờ, chỉnh slide chưa ghi rõ mã lớp.</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">5</td>
                                <td class="py-3.5 px-5 font-bold text-white">Bùi Thanh Hải</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT Hà Nội</td>
                                <td class="py-3.5 px-5 text-slate-400">Giảng viên</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-amber-400">28.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">-12.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">70.0%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">4/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Khai thiếu 1 ngày; giờ giảng dạy thực tế trên lớp chưa cập nhật đủ vào Worklane.</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">6</td>
                                <td class="py-3.5 px-5 font-bold text-white">Ngọ Văn Quý</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT Hà Nội</td>
                                <td class="py-3.5 px-5 text-slate-400">Giảng viên</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-amber-400">29.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">-11.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">72.5%</td>
                                <td class="py-3.5 px-5 text-center text-rose-400 font-bold">3/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Bỏ quên báo cáo 2 ngày trong tuần, cần bổ sung giải trình.</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">7</td>
                                <td class="py-3.5 px-5 font-bold text-white">Nguyễn Quảng An</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT Hà Nội</td>
                                <td class="py-3.5 px-5 text-slate-400">Giảng viên</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-amber-400">32.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">-8.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">80.0%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">4/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Thiếu báo cáo ngày thứ Sáu (25/09).</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">8</td>
                                <td class="py-3.5 px-5 font-bold text-white">Lê Thành Ngọc</td>
                                <td class="py-3.5 px-5 text-slate-300">LMS AI</td>
                                <td class="py-3.5 px-5 text-slate-400">Giảng viên</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-amber-400">32.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">-8.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">80.0%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">4/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Thiếu báo cáo ngày thứ Năm (24/09).</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">9</td>
                                <td class="py-3.5 px-5 font-bold text-white">Trần Quốc Tuấn</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT HCM</td>
                                <td class="py-3.5 px-5 text-slate-400">Giảng viên</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-amber-400">33.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">-7.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">82.5%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">5/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Nộp đủ 5 ngày nhưng khai bình quân 6.6h/ngày; lặp lại việc 'Chăm sóc SV' 5 ngày.</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">10</td>
                                <td class="py-3.5 px-5 font-bold text-white">Phan Ngọc Tài</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT HCM</td>
                                <td class="py-3.5 px-5 text-slate-400">Trợ giảng thử việc</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-amber-400">33.5h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">-6.5h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-amber-400">83.8%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">5/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Trợ giảng thử việc, nộp đủ 5 ngày nhưng chưa tròn 8h/ngày.</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">11</td>
                                <td class="py-3.5 px-5 font-bold text-white">Lưu Hoàng Xuân Nguyên</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT HCM</td>
                                <td class="py-3.5 px-5 text-slate-400">Trợ giảng</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-200">35.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">-5.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-slate-200">87.5%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">5/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Thiếu 5.0h so với định mức 40h tuần.</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">12</td>
                                <td class="py-3.5 px-5 font-bold text-white">Lê Nhựt Mi</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối QTKD</td>
                                <td class="py-3.5 px-5 text-slate-400">Giảng viên</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-200">38.5h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-400">-1.5h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-emerald-400">96.3%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">5/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Thiếu nhẹ 1.5h (Đạt mức khá tốt).</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">13</td>
                                <td class="py-3.5 px-5 font-bold text-white">Lâm Tùng Dương</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT Hà Nội</td>
                                <td class="py-3.5 px-5 text-slate-400">Giảng viên</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-200">38.8h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-400">-1.2h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-emerald-400">96.9%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">5/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Thiếu nhẹ 1.2h (Đạt mức khá tốt).</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">14</td>
                                <td class="py-3.5 px-5 font-bold text-white">Nguyễn Đức Minh</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT HCM</td>
                                <td class="py-3.5 px-5 text-slate-400">Giảng viên</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-200">39.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-400">-1.0h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-emerald-400">97.5%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">5/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Thiếu nhẹ 1.0h (Đạt mức tốt).</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">15</td>
                                <td class="py-3.5 px-5 font-bold text-white">Lê Hà Thanh Sang</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT HCM</td>
                                <td class="py-3.5 px-5 text-slate-400">Giảng viên</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-200">39.2h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-400">-0.8h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-emerald-400">98.1%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">5/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Thiếu nhẹ 0.8h (Đạt mức tốt).</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">16</td>
                                <td class="py-3.5 px-5 font-bold text-white">Lê Thị Bảo Yến</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối QTKD</td>
                                <td class="py-3.5 px-5 text-slate-400">Trợ giảng</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-200">39.5h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-400">-0.5h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-emerald-400">98.8%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">5/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Thiếu nhẹ 0.5h (Đạt chuẩn).</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 text-center font-bold text-slate-400">17</td>
                                <td class="py-3.5 px-5 font-bold text-white">Phạm Viết Hùng</td>
                                <td class="py-3.5 px-5 text-slate-300">Khối CNTT HCM</td>
                                <td class="py-3.5 px-5 text-slate-400">Trợ giảng</td>
                                <td class="py-3.5 px-5 text-center font-mono">40.0h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-200">39.5h</td>
                                <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-400">-0.5h</td>
                                <td class="py-3.5 px-5 text-center font-bold text-emerald-400">98.8%</td>
                                <td class="py-3.5 px-5 text-center text-slate-300">5/5 ngày</td>
                                <td class="py-3.5 px-5 text-slate-300">Thiếu nhẹ 0.5h (Đạt chuẩn).</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 3. DANH SÁCH NHÂN SỰ KHAI BÁO VIỆC CHUNG CHUNG -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                <div class="flex flex-col md:flex-row md:items-center justify-between pb-3 border-b border-slate-800 gap-3">
                    <div>
                        <h3 class="text-base lg:text-lg font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-list-check text-amber-400"></i> 3. Danh Sách Nhân Sự Khai Báo Công Việc Chung Chung & Ngoài Barem
                        </h3>
                        <p class="text-xs text-slate-400">
                            Bóc tách chi tiết: <strong class="text-slate-200">Ngày khai báo &bull; Tên công việc nguyên văn &bull; Số giờ khai &bull; Lý do chưa đạt chuẩn KPI Master</strong>.
                        </p>
                    </div>
                    <input type="text" id="search-generic" placeholder="Tìm tên nhân sự / công việc..." onkeyup="filterGenericTasks()" class="px-3.5 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-indigo-500 w-72">
                </div>

                <div class="space-y-4" id="generic-tasks-container">
                    <!-- Dynamic staff cards with generic task details -->
                </div>
            </div>

        </div>

        <!-- ========================================================================================= -->
        <!-- TAB 3: CHUYÊN ĐỀ KS26 & 9 ĐƠN BẢO LÃNH LMS                                                -->
        <!-- ========================================================================================= -->
        <div id="tab-ks26-content" class="hidden space-y-8">
{latest_ks26_html}

            <!-- BANNER GIỚI THIỆU -->
            <div class="glass-panel p-5 rounded-2xl border-l-4 border-amber-500 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 class="text-base lg:text-lg font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-shield-halved text-amber-400"></i> BÁO CÁO ĐIỀU KIỆN DỰ THI VÀ PHÂN NHÓM HỌC VỤ KHÓA KS26
                    </h2>
                    <p class="text-xs lg:text-sm text-slate-300 mt-1">
                        Cập nhật theo chỉ đạo của Giám đốc Đào tạo: Đối soát thực tế <strong class="text-amber-300">9 sinh viên đã làm đơn bảo lãnh trên LMS Admin</strong>, phân loại chi tiết sinh viên không đủ điều kiện theo từng lớp và danh sách 374 sinh viên.
                    </p>
                </div>
                <div class="flex items-center gap-3 text-xs font-bold">
                    <span class="px-3.5 py-1.5 rounded-lg bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                        Đủ ĐK Trực Tiếp: 248 SV
                    </span>
                    <span class="px-3.5 py-1.5 rounded-lg bg-indigo-500/15 text-indigo-300 border border-indigo-500/30">
                        9 Đơn Trên LMS (4 Duyệt, 5 Chờ)
                    </span>
                </div>
            </div>

            <!-- CHUYÊN ĐỀ MỚI: CHUYỂN DỊCH HÀNH VI & KẾ HOẠCH TÁC CHIẾN 5-15P -->
            <div class="glass-panel p-6 rounded-2xl border border-indigo-500/40 bg-gradient-to-r from-indigo-950/40 via-slate-900/60 to-slate-900/80 shadow-xl space-y-4">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                    <div>
                        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-extrabold uppercase tracking-wider mb-2 border border-emerald-500/30">
                            <i class="fa-solid fa-bolt"></i> Chuyên Đề Quản Trị Mới (30/09/2026)
                        </div>
                        <h3 class="text-lg lg:text-xl font-extrabold text-white flex items-center gap-2.5">
                            <i class="fa-solid fa-chart-line text-indigo-400"></i> Chẩn Đoán Chuyển Dịch Hành Vi K26 & Kế Hoạch Tác Chiến 5-15 Phút Tại Lớp
                        </h3>
                        <p class="text-xs lg:text-sm text-slate-300 mt-1 max-w-3xl">
                            Đối soát 2 chiều giữa <strong>Môn đầu tiên (SSK101)</strong> và <strong>Các môn mới đang học (IT108, SKL01, ENG105, SSK102, SSK103)</strong>. Thay vì họp online dàn trải, Quản lý Đào tạo và CVHT sẽ <strong>vào trực tiếp từng lớp 5–15 phút</strong> giải quyết dứt điểm theo đúng người phụ trách (PIC) và Deadline.
                        </p>
                    </div>
                    <div class="flex flex-wrap items-center gap-3">
                        <a href="bao_cao_k26_chuyen_dich_hanh_vi.html" target="_blank" class="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs lg:text-sm flex items-center gap-2 shadow-lg shadow-indigo-600/30 transition-all border border-indigo-400/30">
                            <i class="fa-solid fa-arrow-up-right-from-square"></i> Mở Báo Cáo Chuyên Đề & Biểu Đồ
                        </a>
                        <a href="K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx" download class="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs lg:text-sm flex items-center gap-2 shadow-lg shadow-emerald-600/30 transition-all border border-emerald-400/30">
                            <i class="fa-solid fa-file-excel"></i> Tải Excel Tác Chiến 14 Sheet
                        </a>
                    </div>
                </div>

                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 border-t border-slate-800/80">
                    <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                        <div class="text-[11px] font-bold text-slate-400 uppercase">Tỷ Lệ Cải Thiện Toàn Khóa</div>
                        <div class="text-xl font-extrabold text-emerald-400 mt-0.5">95.2% <span class="text-xs text-slate-400 font-medium">(356/374 SV)</span></div>
                        <div class="text-[11px] text-emerald-300/80 mt-1">Đã sạch lỗi hoặc giảm vi phạm</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                        <div class="text-[11px] font-bold text-slate-400 uppercase">TH3: Sạch 100% Vi Phạm</div>
                        <div class="text-xl font-extrabold text-indigo-300 mt-0.5">351 SV <span class="text-xs text-slate-400 font-medium">(93.9%)</span></div>
                        <div class="text-[11px] text-slate-400 mt-1">Miễn can thiệp — Biểu dương</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                        <div class="text-[11px] font-bold text-slate-400 uppercase">TH1: Nguy Cơ Bỏ Học (Đỏ)</div>
                        <div class="text-xl font-extrabold text-rose-400 mt-0.5">5 SV <span class="text-xs text-slate-400 font-medium">(1.3%)</span></div>
                        <div class="text-[11px] text-rose-300/80 mt-1">Gặp riêng cuối giờ + Gọi PH (48h)</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                        <div class="text-[11px] font-bold text-slate-400 uppercase">TH4: Sốc Môn Mới Chuyên Ngành</div>
                        <div class="text-xl font-extrabold text-amber-400 mt-0.5">13 SV <span class="text-xs text-slate-400 font-medium">(3.5%)</span></div>
                        <div class="text-[11px] text-amber-300/80 mt-1">GV bộ môn + Trợ giảng phụ đạo</div>
                    </div>
                </div>
            </div>

            <!-- BẢNG TỔNG HỢP TỪNG LỚP THEO YÊU CẦU GIÁM ĐỐC ĐÀO TẠO -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                <div class="flex items-center justify-between pb-3 border-b border-slate-800">
                    <div>
                        <h3 class="text-base lg:text-lg font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-table-list text-indigo-400"></i> 1. Bảng Tổng Hợp Điều Kiện Thi & Tình Trạng Bảo Lãnh Từng Lớp KS26
                        </h3>
                        <p class="text-xs text-slate-400">
                            Công thức quản trị: <strong class="text-slate-200">Không đủ điều kiện = Tổng sinh viên &minus; Sinh viên đủ điều kiện trực tiếp</strong>.
                        </p>
                    </div>
                </div>

                <div class="overflow-x-auto rounded-xl border border-slate-800">
                    <table class="w-full text-left text-sm" id="class-summary-table">
                        <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                            <tr>
                                <th class="py-3.5 px-5">Tên Lớp</th>
                                <th class="py-3.5 px-5 text-center">Tổng SV</th>
                                <th class="py-3.5 px-5 text-center text-emerald-400">Đủ ĐK Thi</th>
                                <th class="py-3.5 px-5 text-center text-rose-400">Không Đủ ĐK</th>
                                <th class="py-3.5 px-5 text-center text-amber-400">Cần / Có Thể Bảo Lãnh</th>
                                <th class="py-3.5 px-5 text-center text-indigo-300">Đã Làm Đơn (Chờ Duyệt)</th>
                                <th class="py-3.5 px-5 text-center text-emerald-300">Đã Duyệt Bảo Lãnh</th>
                                <th class="py-3.5 px-5 text-center">Tỷ Lệ Dự Thi Kỳ Vọng</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800" id="class-summary-tbody">
                            <!-- Populated by JavaScript -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- PHÂN NHÓM 371 SINH VIÊN THEO 4 DẢI VI PHẠM -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-5">
                <div class="flex items-center justify-between pb-3 border-b border-slate-800">
                    <div>
                        <h3 class="text-base lg:text-lg font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-layer-group text-indigo-400"></i> 2. Phân Nhóm Sinh Viên KS26 Theo 4 Dải Tỷ Lệ Vi Phạm (Tuần Đầu Tiên)
                        </h3>
                        <p class="text-xs text-slate-400">Đã kiểm tra tính đúng đắn trên từng sinh viên theo 4 dải: [20-40%), [40-60%), [60-80%), [80-100%].</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <!-- Biểu đồ phân nhóm -->
                    <div class="lg:col-span-1 bg-slate-900/70 p-4 rounded-xl border border-slate-800 flex flex-col items-center justify-center">
                        <h4 class="text-xs font-bold text-slate-300 mb-3 uppercase tracking-wider text-center">Phân Bố Vi Phạm Giữa 3 Tiêu Chí</h4>
                        <div class="w-full h-64">
                            <canvas id="ks26BucketsChart"></canvas>
                        </div>
                    </div>

                    <!-- Bảng Ma trận 4 dải -->
                    <div class="lg:col-span-2 overflow-x-auto rounded-xl border border-slate-800">
                        <table class="w-full text-left text-sm">
                            <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                                <tr>
                                    <th class="py-3.5 px-5">Dải Vi Phạm</th>
                                    <th class="py-3.5 px-5 text-center">Vắng Chuyên Cần</th>
                                    <th class="py-3.5 px-5 text-center">Chưa Chuẩn Bị Elearning</th>
                                    <th class="py-3.5 px-5 text-center">Nợ / Thiếu Bài Tập</th>
                                    <th class="py-3.5 px-5 text-left">Mức Độ Cảnh Báo & Hành Động</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-800">
                                <tr class="hover:bg-slate-800/40">
                                    <td class="py-3.5 px-5 font-bold text-amber-300">[20% - 40%)</td>
                                    <td class="py-3.5 px-5 text-center font-bold text-slate-200">33 SV <span class="text-xs text-slate-400">(8.8%)</span></td>
                                    <td class="py-3.5 px-5 text-center font-bold text-amber-400">17 SV <span class="text-xs text-slate-400">(4.5% - Chậm 1 bài)</span></td>
                                    <td class="py-3.5 px-5 text-center font-bold text-slate-200">0 SV <span class="text-xs text-slate-400">(0.0%)</span></td>
                                    <td class="py-3.5 px-5 text-slate-300"><span class="px-2.5 py-1 rounded text-xs font-bold badge-warning">🟡 Cảnh báo Nhẹ:</span> Nhắc nhở chung trên Group Zalo lớp</td>
                                </tr>
                                <tr class="hover:bg-slate-800/40">
                                    <td class="py-3.5 px-5 font-bold text-amber-400">[40% - 60%)</td>
                                    <td class="py-3.5 px-5 text-center font-bold text-slate-200">33 SV <span class="text-xs text-slate-400">(8.8%)</span></td>
                                    <td class="py-3.5 px-5 text-center font-bold text-slate-200">97 SV <span class="text-xs text-slate-400">(25.9% - Chậm 2 bài)</span></td>
                                    <td class="py-3.5 px-5 text-center font-bold text-slate-200">0 SV <span class="text-xs text-slate-400">(0.0%)</span></td>
                                    <td class="py-3.5 px-5 text-slate-300"><span class="px-2.5 py-1 rounded text-xs font-bold badge-warning">🟠 Cảnh báo TB:</span> Trợ giảng gọi điện trực tiếp tìm hiểu lý do</td>
                                </tr>
                                <tr class="hover:bg-slate-800/40">
                                    <td class="py-3.5 px-5 font-bold text-rose-400">[60% - 80%)</td>
                                    <td class="py-3.5 px-5 text-center font-bold text-slate-200">11 SV <span class="text-xs text-slate-400">(2.9%)</span></td>
                                    <td class="py-3.5 px-5 text-center font-bold text-rose-400">3 SV <span class="text-xs text-slate-400">(0.8% - Chậm 3 bài)</span></td>
                                    <td class="py-3.5 px-5 text-center font-bold text-slate-200">0 SV <span class="text-xs text-slate-400">(0.0%)</span></td>
                                    <td class="py-3.5 px-5 text-slate-300"><span class="px-2.5 py-1 rounded text-xs font-bold badge-danger">🔴 Nguy cơ Cao:</span> Bắt buộc làm đơn cam kết học bù</td>
                                </tr>
                                <tr class="hover:bg-slate-800/40 bg-rose-950/20">
                                    <td class="py-3.5 px-5 font-black text-rose-500">[80% - 100%]</td>
                                    <td class="py-3.5 px-5 text-center font-bold text-rose-400">10 SV <span class="text-xs text-slate-400">(2.7%)</span></td>
                                    <td class="py-3.5 px-5 text-center font-bold text-rose-400">1 SV <span class="text-xs text-slate-400">(0.3% - Chậm 4 bài)</span></td>
                                    <td class="py-3.5 px-5 text-center font-black text-rose-400 text-base">69 SV <span class="text-xs text-rose-300">(18.4% - Nợ bài tuần 1)</span></td>
                                    <td class="py-3.5 px-5 text-rose-300 font-semibold"><span class="px-2.5 py-1 rounded text-xs font-bold badge-danger">⛔ Báo động Đỏ:</span> Nợ bài tập tuần đầu, cần đôn đốc nộp bù</td>
                                </tr>
                                <tr class="bg-slate-900 font-bold border-t-2 border-slate-700">
                                    <td class="py-3.5 px-5 text-white">Tổng SV vi phạm &ge; 20%</td>
                                    <td class="py-3.5 px-5 text-center text-indigo-400 font-black">87 SV <span class="text-xs text-slate-400 font-normal">(23.3%)</span></td>
                                    <td class="py-3.5 px-5 text-center text-amber-400 font-black">118 SV <span class="text-xs text-slate-400 font-normal">(31.6%)</span></td>
                                    <td class="py-3.5 px-5 text-center text-rose-400 font-black">69 SV <span class="text-xs text-slate-400 font-normal">(18.4%)</span></td>
                                    <td class="py-3.5 px-5 text-slate-400 font-normal">*(305 SV đã hoàn thành bài tập tuần đầu đạt 0% vi phạm)*</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 3. DANH SÁCH CHI TIẾT SINH VIÊN THEO TỪNG NHÓM VI PHẠM CỦA TỪNG LỚP -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                <div class="flex flex-col xl:flex-row xl:items-center justify-between pb-3 border-b border-slate-800 gap-3">
                    <div>
                        <h3 class="text-base lg:text-lg font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-users-viewfinder text-emerald-400"></i> 3. Tra Cứu Danh Sách Chi Tiết Sinh Viên KS26 Theo Từng Lớp & Nhóm Vi Phạm
                        </h3>
                        <p class="text-xs text-slate-400">
                            Công cụ tra cứu dành cho Giám đốc Đào tạo và CVHT: Lọc theo lớp, theo tiêu chí vi phạm, dải vi phạm và tình trạng bảo lãnh.
                        </p>
                    </div>
                    
                    <!-- Filters Grid -->
                    <div class="flex flex-wrap items-center gap-2.5">
                        <select id="filter-class" onchange="applyStudentFilters()" class="px-3.5 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-indigo-500 font-semibold">
                            <option value="ALL">-- Tất cả các lớp (10 lớp) --</option>
                            <option value="HN-KS26-CNTT1">HN-KS26-CNTT1</option>
                            <option value="HN-K26-CNTT2">HN-K26-CNTT2</option>
                            <option value="HN-K26-CNTT3">HN-K26-CNTT3</option>
                            <option value="HN-K26-QTKD1">HN-K26-QTKD1</option>
                            <option value="HN-K26-QTKD2">HN-K26-QTKD2</option>
                            <option value="HN-K26-QTKD3">HN-K26-QTKD3</option>
                            <option value="HCM-KS26-CNTT1">HCM-KS26-CNTT1</option>
                            <option value="HCM-KS26-CNTT2">HCM-KS26-CNTT2</option>
                            <option value="HCM-KS26-QTKD1">HCM-KS26-QTKD1</option>
                        </select>

                        <select id="filter-metric" onchange="applyStudentFilters()" class="px-3.5 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-indigo-500 font-semibold">
                            <option value="ALL">-- Tất cả tiêu chí vi phạm --</option>
                            <option value="att">Chuyên cần (Nghỉ học)</option>
                            <option value="el">Chưa chuẩn bị Elearning</option>
                            <option value="hw">Nợ bài tập về nhà</option>
                        </select>

                        <select id="filter-bucket" onchange="applyStudentFilters()" class="px-3.5 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-indigo-500 font-semibold">
                            <option value="ALL">-- Tất cả dải vi phạm --</option>
                            <option value="20-40">[20% - 40%)</option>
                            <option value="40-60">[40% - 60%)</option>
                            <option value="60-80">[60% - 80%)</option>
                            <option value="80-100">[80% - 100%]</option>
                            <option value="violate">&ge; 20% (Có vi phạm)</option>
                        </select>

                        <select id="filter-guarantee" onchange="applyStudentFilters()" class="px-3.5 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-indigo-500 font-semibold">
                            <option value="ALL">-- Tất cả trạng thái thi --</option>
                            <option value="LMS_9">🔥 9 ĐƠN BẢO LÃNH LMS (Chờ Duyệt)</option>
                            <option value="PENDING">Đã Làm Đơn (Chờ Duyệt - 9 SV)</option>
                            <option value="CAN_GUARANTEE">Cần / Có Thể Bảo Lãnh (125 SV)</option>
                            <option value="NOT_ELIGIBLE">Không Đủ Điều Kiện (126 SV)</option>
                            <option value="ELIGIBLE">Đủ Điều Kiện Thi (248 SV)</option>
                        </select>

                        <input type="text" id="search-student" placeholder="Tìm tên / mã SV..." onkeyup="applyStudentFilters()" class="px-3.5 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-indigo-500 w-48">
                    </div>
                </div>

                <!-- Quick Filter Buttons & Direct Excel Download -->
                <div class="flex flex-wrap items-center gap-2 pt-1 pb-2 border-b border-slate-800">
                    <span class="text-xs text-slate-400 font-bold flex items-center gap-1 mr-1">
                        <i class="fa-solid fa-bolt text-amber-400"></i> Lọc theo nhóm mục 2:
                    </span>
                    <button onclick="quickFilterGroup('ALL')" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-slate-800 hover:bg-slate-700 text-white transition-colors">Tất Cả (374 SV)</button>
                    <button onclick="quickFilterGroup('HW')" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/40 transition-colors">📕 Nợ BTVN (69 SV)</button>
                    <button onclick="quickFilterGroup('EL')" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 transition-colors">📙 Chậm Elearning (118 SV)</button>
                    <button onclick="quickFilterGroup('ATT')" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 border border-indigo-500/40 transition-colors">📘 Vắng Chuyên Cần (87 SV)</button>
                    <button onclick="quickFilterGroup('GUARANTEE')" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 transition-colors">🟡 Nhóm Cần Bảo Lãnh (125 SV)</button>
                    <button onclick="quickFilterGroup('LMS_9')" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 border border-purple-500/40 transition-colors">⏳ 9 Đơn LMS</button>
                    <button onclick="quickFilterGroup('D80_100')" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-red-600/20 hover:bg-red-600/30 text-red-300 border border-red-600/40 transition-colors">⛔ Dải [80-100%]</button>
                    <button onclick="quickFilterGroup('D40_60')" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-orange-500/20 hover:bg-orange-500/30 text-orange-300 border border-orange-500/40 transition-colors">🟠 Dải [40-60%)</button>

                    <div class="ml-auto flex items-center gap-2">
                        <a href="K26_Danh_Sach_Theo_Tung_Nhom_Vi_Pham.xlsx" download class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-1.5 shadow-md shadow-emerald-950/50 transition-all">
                            <i class="fa-solid fa-file-excel text-sm"></i> Tải File Excel Chia Theo Từng Nhóm Vi Phạm
                        </a>
                    </div>
                </div>

                <div class="text-xs text-slate-400 font-semibold flex items-center justify-between">
                    <span id="filtered-count-text">Hiển thị: 374 / 374 Sinh viên</span>
                </div>

                <div class="overflow-x-auto rounded-xl border border-slate-800 max-h-[600px] overflow-y-auto">
                    <table class="w-full text-left text-sm" id="table-students-detail">
                        <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800 sticky top-0 z-20">
                            <tr>
                                <th class="py-3 px-4 text-center w-12">STT</th>
                                <th class="py-3 px-4">Họ và Tên SV</th>
                                <th class="py-3 px-4">Mã SV / Email</th>
                                <th class="py-3 px-4">Lớp</th>
                                <th class="py-3 px-4 text-center">Vi Phạm CC (%)</th>
                                <th class="py-3 px-4 text-center">Vi Phạm BTVN (%)</th>
                                <th class="py-3 px-4 text-center">Elearning (Số Bài Chậm)</th>
                                <th class="py-3 px-4 text-center">Trạng Thái Thi & Bảo Lãnh</th>
                                <th class="py-3 px-4">Đánh Giá & Đề Xuất Hành Động</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800" id="students-detail-tbody">
                            <!-- Populated dynamically by JS -->
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

    </main>

    <!-- FOOTER -->
    <footer class="border-t border-slate-800 bg-slate-950 px-6 py-4 mt-8">
        <div class="max-w-[1750px] mx-auto flex flex-col md:flex-row items-center justify-between text-xs text-slate-400 gap-2">
            <div>
                &copy; 2026 Rikkei Education &bull; Ban Đào Tạo PTIT &bull; Báo Cáo Điều Hành Trực Tiếp Giám Đốc Đào Tạo
            </div>
            <div class="flex items-center gap-4">
                <span>Hệ thống: <strong class="text-emerald-400"><i class="fa-solid fa-circle-check"></i> Hoạt động ổn định</strong></span>
                <span>Biên dịch: <strong class="text-slate-300">Antigravity AI PMO Agent</strong></span>
            </div>
        </div>
    </footer>

    <!-- SCRIPT LOGIC -->
    <script>
        const KS26_STUDENTS = {ks26_students_json};
        const KS26_CLASS_TABLE = {ks26_class_table_json};
        const LMS_9_STUDENTS = {lms_9_students_json};
        const UNDER_FILTERED = {under_filtered_json};
        const GENERIC_STAFF = {generic_staff_json};
        const DEPT_STATS = {dept_stats_json};

        // Screenshot mode toggle
        function toggleScreenshotMode() {{
            document.body.classList.toggle('screenshot-mode');
            const isShot = document.body.classList.contains('screenshot-mode');
            const text = document.getElementById('screenshot-text');
            const btn = document.getElementById('btn-screenshot');
            if (isShot) {{
                text.innerText = 'Trở Về Cỡ Chữ Chuẩn';
                btn.classList.add('bg-amber-500', 'text-slate-950');
            }} else {{
                text.innerText = 'Phóng To Chụp Ảnh';
                btn.classList.remove('bg-amber-500', 'text-slate-950');
            }}
        }}

        // Tab Switching
        function switchTab(tabId) {{
            document.querySelectorAll('[id$=\"-content\"]').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

            if (tabId === 'tab-academic') {{
                document.getElementById('tab-academic-content').classList.remove('hidden');
                document.getElementById('btn-tab-academic').classList.add('active');
            }} else if (tabId === 'tab-daily') {{
                document.getElementById('tab-daily-content').classList.remove('hidden');
                document.getElementById('btn-tab-daily').classList.add('active');
            }} else if (tabId === 'tab-ks26') {{
                document.getElementById('tab-ks26-content').classList.remove('hidden');
                document.getElementById('btn-tab-ks26').classList.add('active');
                initBucketsChart();
            }}
        }}

        // Render Class Summary Table
        function renderClassSummaryTable() {{
            const tbody = document.getElementById('class-summary-tbody');
            if (!tbody) return;
            tbody.innerHTML = '';

            let totals = {{ total: 0, eligible: 0, not_eligible: 0, can_guarantee: 0, pending: 0, approved: 0 }};

            Object.values(KS26_CLASS_TABLE).forEach(c => {{
                totals.total += c.total;
                totals.eligible += c.eligible;
                totals.not_eligible += c.not_eligible;
                totals.can_guarantee += c.can_guarantee;
                totals.pending += c.pending;
                totals.approved += c.approved;

                const expRate = c.total > 0 ? (((c.eligible + c.pending + c.approved) / c.total) * 100).toFixed(1) : '0.0';

                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-800/40';
                tr.innerHTML = `
                    <td class="py-3.5 px-5 font-bold text-white flex items-center gap-2">
                        <span class="w-2.5 h-2.5 rounded-full ${{c.dept === 'CNTT' ? 'bg-indigo-500' : 'bg-amber-500'}}"></span>
                        ${{c.class}}
                    </td>
                    <td class="py-3.5 px-5 text-center font-mono font-bold text-slate-300">${{c.total}}</td>
                    <td class="py-3.5 px-5 text-center font-mono font-bold text-emerald-400">${{c.eligible}} <span class="text-xs text-slate-400 font-normal">(${{c.total > 0 ? ((c.eligible / c.total) * 100).toFixed(1) : '0.0'}}%)</span></td>
                    <td class="py-3.5 px-5 text-center font-mono font-bold text-rose-400">${{c.not_eligible}} <span class="text-xs text-slate-400 font-normal">(${{c.total > 0 ? ((c.not_eligible / c.total) * 100).toFixed(1) : '0.0'}}%)</span></td>
                    <td class="py-3.5 px-5 text-center font-mono font-bold text-amber-300">${{c.can_guarantee}} <span class="text-xs text-slate-400 font-normal">(${{c.total > 0 ? ((c.can_guarantee / c.total) * 100).toFixed(1) : '0.0'}}%)</span></td>
                    <td class="py-3.5 px-5 text-center font-mono font-bold text-indigo-300">${{c.pending}} <span class="text-xs text-slate-400 font-normal">(${{c.total > 0 ? ((c.pending / c.total) * 100).toFixed(1) : '0.0'}}%)</span></td>
                    <td class="py-3.5 px-5 text-center font-mono font-bold text-emerald-300">${{c.approved}} <span class="text-xs text-slate-400 font-normal">(${{c.total > 0 ? ((c.approved / c.total) * 100).toFixed(1) : '0.0'}}%)</span></td>
                    <td class="py-3.5 px-5 text-center font-mono font-extrabold ${{parseFloat(expRate) >= 80 ? 'text-emerald-400' : 'text-amber-400'}}">${{expRate}}%</td>
                `;
                tbody.appendChild(tr);
            }});

            // Total row
            const totalExp = totals.total > 0 ? (((totals.eligible + totals.pending + totals.approved) / totals.total) * 100).toFixed(1) : '0.0';
            const trTotal = document.createElement('tr');
            trTotal.className = 'bg-slate-900 font-extrabold border-t-2 border-slate-700 text-sm';
            trTotal.innerHTML = `
                <td class="py-4 px-5 text-white uppercase tracking-wider">TỔNG TOÀN KHÓA KS26</td>
                <td class="py-4 px-5 text-center font-mono text-white text-base">${{totals.total}} <span class="text-xs text-slate-400 font-normal">(100%)</span></td>
                <td class="py-4 px-5 text-center font-mono text-emerald-400 text-base">${{totals.eligible}} <span class="text-xs text-emerald-300 font-normal">(${{totals.total > 0 ? ((totals.eligible / totals.total) * 100).toFixed(1) : '0.0'}}%)</span></td>
                <td class="py-4 px-5 text-center font-mono text-rose-400 text-base">${{totals.not_eligible}} <span class="text-xs text-rose-300 font-normal">(${{totals.total > 0 ? ((totals.not_eligible / totals.total) * 100).toFixed(1) : '0.0'}}%)</span></td>
                <td class="py-4 px-5 text-center font-mono text-amber-300 text-base">${{totals.can_guarantee}} <span class="text-xs text-amber-200 font-normal">(${{totals.total > 0 ? ((totals.can_guarantee / totals.total) * 100).toFixed(1) : '0.0'}}%)</span></td>
                <td class="py-4 px-5 text-center font-mono text-indigo-300 text-base">${{totals.pending}} <span class="text-xs text-indigo-200 font-normal">(${{totals.total > 0 ? ((totals.pending / totals.total) * 100).toFixed(1) : '0.0'}}%)</span></td>
                <td class="py-4 px-5 text-center font-mono text-emerald-300 text-base">${{totals.approved}} <span class="text-xs text-emerald-200 font-normal">(${{totals.total > 0 ? ((totals.approved / totals.total) * 100).toFixed(1) : '0.0'}}%)</span></td>
                <td class="py-4 px-5 text-center font-mono text-emerald-400 text-base">${{totalExp}}%</td>
            `;
            tbody.appendChild(trTotal);
        }}

        // Render Student Detail Table with Filtering
        function renderStudentsDetailTable(list) {{
            const tbody = document.getElementById('students-detail-tbody');
            const countText = document.getElementById('filtered-count-text');
            if (!tbody) return;
            tbody.innerHTML = '';
            countText.innerText = `Hiển thị: ${{list.length}} / ${{KS26_STUDENTS.length}} Sinh viên`;

            list.forEach((s, idx) => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-800/40';

                let statusBadge = '';
                if (s.guarantee_status === 'ĐÃ DUYỆT BẢO LÃNH') {{
                    statusBadge = '<span class=\"px-2.5 py-1 rounded text-xs font-bold badge-success\">✅ ĐÃ DUYỆT BẢO LÃNH</span>';
                }} else if (s.guarantee_status === 'ĐÃ LÀM ĐƠN (CHỜ DUYỆT)') {{
                    statusBadge = '<span class=\"px-2.5 py-1 rounded text-xs font-bold badge-info\">⏳ ĐÃ LÀM ĐƠN (CHỜ DUYỆT)</span>';
                }} else if (s.guarantee_status === 'ĐƯỢC XEM XÉT BẢO LÃNH' || s.guarantee_status === 'CẦN / CÓ THỂ BẢO LÃNH') {{
                    statusBadge = '<span class=\"px-2.5 py-1 rounded text-xs font-bold badge-warning\">🟡 CẦN / CÓ THỂ BẢO LÃNH</span>';
                }} else if (s.guarantee_status && s.guarantee_status.includes('KHÔNG ĐƯỢC BẢO LÃNH')) {{
                    statusBadge = '<span class=\"px-2.5 py-1 rounded text-xs font-bold badge-danger\">⛔ CẤM THI (0% CC)</span>';
                }} else if (s.eligible) {{
                    statusBadge = '<span class=\"px-2.5 py-1 rounded text-xs font-bold badge-success\">ĐỦ ĐIỀU KIỆN</span>';
                }} else {{
                    statusBadge = '<span class=\"px-2.5 py-1 rounded text-xs font-bold badge-danger\">KHÔNG ĐỦ ĐK</span>';
                }}

                tr.innerHTML = `
                    <td class="py-3 px-4 text-center font-mono text-slate-500">${{idx + 1}}</td>
                    <td class="py-3 px-4 font-bold text-white">${{s.name}}</td>
                    <td class="py-3 px-4 font-mono text-xs text-slate-400">${{s.code || 'Chưa cập nhật'}}</td>
                    <td class="py-3 px-4 font-mono font-semibold text-slate-300">${{s.class}}</td>
                    <td class="py-3 px-4 text-center font-mono ${{s.att_violate > 0 ? 'text-rose-400 font-bold' : 'text-emerald-400 font-semibold'}}">${{s.att_violate}}%</td>
                    <td class="py-3 px-4 text-center font-mono ${{s.hw_violate > 0 ? 'text-rose-400 font-bold' : 'text-emerald-400 font-semibold'}}">${{s.hw_violate}}%</td>
                    <td class="py-3 px-4 text-center font-mono ${{s.el_late_count > 0 ? 'text-amber-400 font-bold' : 'text-emerald-400 font-semibold'}}">${{s.el_text || (s.el_late_count > 0 ? 'Chậm ' + s.el_late_count + ' bài' : '0 bài')}}</td>
                    <td class="py-3 px-4 text-center">${{statusBadge}}</td>
                    <td class="py-3 px-4 text-xs text-slate-300">${{s.guarantee_note}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function quickFilterGroup(type) {{
            const filterClass = document.getElementById('filter-class');
            const filterMetric = document.getElementById('filter-metric');
            const filterBucket = document.getElementById('filter-bucket');
            const filterGuar = document.getElementById('filter-guarantee');
            const search = document.getElementById('search-student');

            filterClass.value = 'ALL';
            search.value = '';

            if (type === 'ALL') {{
                filterMetric.value = 'ALL';
                filterBucket.value = 'ALL';
                filterGuar.value = 'ALL';
            }} else if (type === 'HW') {{
                filterMetric.value = 'hw';
                filterBucket.value = '80-100';
                filterGuar.value = 'ALL';
            }} else if (type === 'EL') {{
                filterMetric.value = 'el';
                filterBucket.value = 'violate';
                filterGuar.value = 'ALL';
            }} else if (type === 'ATT') {{
                filterMetric.value = 'att';
                filterBucket.value = 'violate';
                filterGuar.value = 'ALL';
            }} else if (type === 'GUARANTEE') {{
                filterMetric.value = 'ALL';
                filterBucket.value = 'ALL';
                filterGuar.value = 'CAN_GUARANTEE';
            }} else if (type === 'LMS_9') {{
                filterMetric.value = 'ALL';
                filterBucket.value = 'ALL';
                filterGuar.value = 'LMS_9';
            }} else if (type === 'D80_100') {{
                filterMetric.value = 'ALL';
                filterBucket.value = '80-100';
                filterGuar.value = 'ALL';
            }} else if (type === 'D40_60') {{
                filterMetric.value = 'ALL';
                filterBucket.value = '40-60';
                filterGuar.value = 'ALL';
            }}
            applyStudentFilters();
        }}

        function applyStudentFilters() {{
            const cls = document.getElementById('filter-class').value;
            const metric = document.getElementById('filter-metric').value;
            const bucket = document.getElementById('filter-bucket').value;
            const guar = document.getElementById('filter-guarantee').value;
            const search = document.getElementById('search-student').value.toLowerCase().trim();

            const filtered = KS26_STUDENTS.filter(s => {{
                // 1. Class filter
                if (cls !== 'ALL' && s.class !== cls) return false;

                // 2. Metric & Bucket filter
                if (metric !== 'ALL' || bucket !== 'ALL') {{
                    let targetVal = 0;
                    let targetBucket = '';
                    if (metric === 'att') {{ targetVal = s.att_violate; targetBucket = s.att_bucket; }}
                    else if (metric === 'el') {{ targetVal = s.el_violate; targetBucket = s.el_bucket; }}
                    else if (metric === 'hw') {{ targetVal = s.hw_violate; targetBucket = s.hw_bucket; }}
                    else {{
                        // Check if any metric matches bucket
                        targetVal = Math.max(s.att_violate, s.el_violate, s.hw_violate);
                    }}

                    if (bucket === 'violate') {{
                        if (metric === 'ALL') {{
                            if (s.att_violate < 20 && s.el_violate < 20 && s.hw_violate < 20) return false;
                        }} else {{
                            if (targetVal < 20) return false;
                        }}
                    }} else if (bucket !== 'ALL') {{
                        if (metric === 'ALL') {{
                            if (s.att_bucket !== bucket && s.el_bucket !== bucket && s.hw_bucket !== bucket) return false;
                        }} else {{
                            if (targetBucket !== bucket) return false;
                        }}
                    }}
                }}

                // 3. Guarantee Status filter
                if (guar === 'LMS_9') {{
                    if (s.guarantee_status !== 'ĐÃ DUYỆT BẢO LÃNH' && s.guarantee_status !== 'ĐÃ LÀM ĐƠN (CHỜ DUYỆT)' && !s.has_lms_guarantee) return false;
                }} else if (guar === 'APPROVED') {{
                    if (s.guarantee_status !== 'ĐÃ DUYỆT BẢO LÃNH') return false;
                }} else if (guar === 'PENDING') {{
                    if (s.guarantee_status !== 'ĐÃ LÀM ĐƠN (CHỜ DUYỆT)') return false;
                }} else if (guar === 'CAN_GUARANTEE') {{
                    if (s.guarantee_status !== 'ĐƯỢC XEM XÉT BẢO LÃNH' && s.guarantee_status !== 'CẦN / CÓ THỂ BẢO LÃNH' && s.guarantee_status !== 'ĐÃ LÀM ĐƠN (CHỜ DUYỆT)') return false;
                }} else if (guar === 'NOT_ELIGIBLE') {{
                    if (s.eligible) return false;
                }} else if (guar === 'ELIGIBLE') {{
                    if (!s.eligible) return false;
                }}

                // 4. Search text filter
                if (search) {{
                    const matchName = s.name.toLowerCase().includes(search);
                    const matchCode = (s.code || '').toLowerCase().includes(search);
                    const matchClass = s.class.toLowerCase().includes(search);
                    if (!matchName && !matchCode && !matchClass) return false;
                }}

                return true;
            }});

            renderStudentsDetailTable(filtered);
        }}

        // Render Generic Staff Tasks Cards
        function renderGenericStaffCards(staffList) {{
            const container = document.getElementById('generic-tasks-container');
            if (!container) return;
            container.innerHTML = '';

            staffList.forEach((st, idx) => {{
                const card = document.createElement('div');
                card.className = 'bg-slate-900/70 rounded-xl p-4 border border-slate-800 space-y-3';

                let tasksHtml = '';
                st.generic_tasks.forEach(t => {{
                    tasksHtml += `
                        <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-800/80 flex flex-col md:flex-row md:items-center justify-between gap-2 text-xs lg:text-sm">
                            <div class="space-y-1">
                                <div class="flex items-center gap-2">
                                    <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-xs font-semibold">${{t.date}}</span>
                                    <strong class="text-white">${{t.title}}</strong>
                                </div>
                                <div class="text-xs text-amber-400 flex items-center gap-1.5">
                                    <i class="fa-solid fa-circle-info text-amber-500"></i> Lý do: ${{t.reason}}
                                </div>
                            </div>
                            <div class="text-right whitespace-nowrap font-mono font-bold text-indigo-300 bg-indigo-950/50 px-3 py-1.5 rounded border border-indigo-500/30 text-xs">
                                ${{t.hours}} giờ
                            </div>
                        </div>
                    `;
                }});

                card.innerHTML = `
                    <div class="flex flex-col md:flex-row md:items-center justify-between pb-2 border-b border-slate-800 gap-2">
                        <div class="flex items-center gap-3">
                            <span class="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-300 flex items-center justify-center text-xs font-extrabold font-mono">
                                ${{idx + 1}}
                            </span>
                            <div>
                                <h4 class="text-sm lg:text-base font-bold text-white">${{st.name}}</h4>
                                <p class="text-xs text-slate-400">${{st.group}} &bull; ${{st.role}} (Rank ${{st.rank}})</p>
                            </div>
                        </div>
                        <span class="px-3 py-1 rounded-full text-xs font-bold badge-warning">
                            ${{st.generic_tasks.length}} công việc chưa đạt chuẩn
                        </span>
                    </div>
                    <div class="space-y-2">
                        ${{tasksHtml}}
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function filterGenericTasks() {{
            const search = document.getElementById('search-generic').value.toLowerCase().trim();
            if (!search) {{
                renderGenericStaffCards(GENERIC_STAFF);
                return;
            }}
            const filtered = GENERIC_STAFF.filter(st => {{
                const matchName = st.name.toLowerCase().includes(search) || st.group.toLowerCase().includes(search);
                const matchTask = st.generic_tasks.some(t => t.title.toLowerCase().includes(search) || t.reason.toLowerCase().includes(search));
                return matchName || matchTask;
            }});
            renderGenericStaffCards(filtered);
        }}

        // Init Chart for Buckets
        let bucketsChartInstance = null;
        function initBucketsChart() {{
            if (bucketsChartInstance) return;
            const ctx = document.getElementById('ks26BucketsChart');
            if (!ctx) return;

            bucketsChartInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['[20-40%)', '[40-60%)', '[60-80%)', '[80-100%]'],
                    datasets: [
                        {{
                            label: 'Chuyên cần (Vắng)',
                            data: [33, 33, 11, 10],
                            backgroundColor: 'rgba(99, 102, 241, 0.85)',
                            borderRadius: 6
                        }},
                        {{
                            label: 'Chậm Elearning',
                            data: [17, 97, 3, 1],
                            backgroundColor: 'rgba(245, 158, 11, 0.85)',
                            borderRadius: 6
                        }},
                        {{
                            label: 'Nợ Bài tập về nhà',
                            data: [0, 0, 0, 69],
                            backgroundColor: 'rgba(239, 68, 68, 0.85)',
                            borderRadius: 6
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            labels: {{ color: '#cbd5e1', font: {{ size: 11, weight: 'bold' }} }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                            ticks: {{ color: '#94a3b8', font: {{ size: 11, weight: 'bold' }} }}
                        }},
                        y: {{
                            grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                            ticks: {{ color: '#94a3b8', font: {{ size: 11 }} }}
                        }}
                    }}
                }}
            }});
        }}

        // Copy Briefing Summary for Zalo/Slack
        function copyBriefingSummary() {{
            const summaryText = `BÁO CÁO GIAO BAN ĐÀO TẠO TUẦN (18/11/2026 - KỲ W47) - KÍNH GỬI GIÁM ĐỐC ĐÀO TẠO

1. KHÓA KS24 (DevOps & Phân Luồng OJT):
- Chỉ số: Kỷ luật cơ bản ổn định, chuyên cần một số lớp đồ án cần theo dõi (HN-CNTT3 vắng 31.58%, HN-CNTT1 vắng 26.67%).
- Học vụ K24: Hoàn tất phương án phân luồng 342 SV (188 SV thực học OJT, 81 SV xuống khóa K25, 8 SV xuống K26, 39 bảo lưu, 25 bỏ học/đình chỉ).

2.1. KHÓA KS25 - KHỐI CNTT (Phân tích thiết kế HT & Agile):
- HN: HN-CNTT1 vắng 36.84%, bài tập 18.42%, EL 23.68% (cần tăng cường trợ giảng đôn đốc). Các lớp CNTT2, CNTT3, CNTT4 duy trì nề nếp ổn định.
- HCM: Môn Agile Scrum nề nếp tốt, các chỉ số trong ngưỡng an toàn.

2.2. KHÓA KS25 - KHỐI QTKD (Ứng dụng AI Agent - Cập nhật 18/11):
- Quy mô: 2 lớp chính quy, 86 SV (Thầy Lê Thành Ngọc & Cô Nguyễn Thị Như Quỳnh).
- Số liệu ngày 18/11:
  * HN-K25-QTKD1 (46 SV): Vi phạm chuyên cần 23.91%, Nợ bài tập 2.17%, Trễ Elearning 19.57%.
  * HN-K25-QTKD2 (40 SV): Vi phạm chuyên cần 12.50%, Nợ bài tập 0.00%, Trễ Elearning 27.50% (cần xử lý nhóm trễ EL).

3. KHÓA KS26 (Tân Sinh Viên - 39 Lớp-môn LMS - Tuần W47, chốt 18/11):
- Đã hoàn tất thi kết thúc môn IT108, bước vào giai đoạn môn SEL101 (QTKD) và IT206 (CNTT).
- Khối QTKD (SEL101): HN-K26-QTKD2 (43 SV) đạt Chuẩn mực (CC 9.30%, BT 2.33%, EL 9.30%); HCM-K26-QTKD1 đạt 0% CC/BT; HN-K26-QTKD1 cần đôn đốc Elearning (23.26%); HN-K26-QTKD3 cần nhắc EL (11.90%).
- Khối CNTT (IT206): HN-KS26-CNTT4 hôm nay (18/11) thi kết thúc môn IT206-K26: 19/21 SV (90.48%) đủ điều kiện dự thi, 2/21 SV (9.52%) bị cấm thi (RK2600025 Phí Anh Minh vắng 66.7%, RK2600042 Nguyễn Duy Hưng vắng 38.9%). HN-KS26-CNTT1 cần chấn chỉnh CC (30.23%).
- Điểm nóng SSK101: Tồn đọng BTVN và EL ở giai đoạn cuối môn (HCM-CNTT1 BT 52.17%, EL 95.65%; HCM-CNTT2 BT 51.11%, EL 91.11%).

4. KIỂM TOÁN WORKLANE 40H/TUẦN:
- Đã kiểm toán hồi cứu tuần 09/11 - 12/11 và đồng bộ Worklane nhân sự.

Xem chi tiết tại Dashboard: output/dashboards/management/weekly_director_report.html`;

            navigator.clipboard.writeText(summaryText).then(() => {{
                const btn = document.getElementById('btn-copy');
                const originalHtml = btn.innerHTML;
                btn.innerHTML = '<i class=\"fa-solid fa-check\"></i> Đã sao chép thành công!';
                btn.classList.remove('from-indigo-600', 'to-purple-600');
                btn.classList.add('from-emerald-600', 'to-teal-600');
                setTimeout(() => {{
                    btn.innerHTML = originalHtml;
                    btn.classList.remove('from-emerald-600', 'to-teal-600');
                    btn.classList.add('from-indigo-600', 'to-purple-600');
                }}, 2500);
            }}).catch(err => {{
                alert('Không thể tự động sao chép. Vui lòng thử lại!');
            }});
        }}

        // KS26 Multi-course View Switcher
        function switchKS26View(mode) {{
            const cardsCont = document.getElementById('ks26-cards-container');
            const subCont = document.getElementById('ks26-subject-tables-container');
            const flatCont = document.getElementById('ks26-flat-table-container');
            const subFilters = document.getElementById('ks26-subject-filters');
            
            const btnCards = document.getElementById('btn-ks26-view-cards');
            const btnSub = document.getElementById('btn-ks26-view-subject');
            const btnTable = document.getElementById('btn-ks26-view-table');

            [btnCards, btnSub, btnTable].forEach(b => {{
                if (b) {{
                    b.classList.remove('bg-indigo-600', 'text-white');
                    b.classList.add('text-slate-400');
                }}
            }});

            if (cardsCont) cardsCont.classList.add('hidden');
            if (subCont) subCont.classList.add('hidden');
            if (flatCont) flatCont.classList.add('hidden');
            if (subFilters) subFilters.classList.add('hidden');

            if (mode === 'cards' && cardsCont) {{
                cardsCont.classList.remove('hidden');
                btnCards.classList.add('bg-indigo-600', 'text-white');
                btnCards.classList.remove('text-slate-400');
            }} else if (mode === 'subject' && subCont) {{
                subCont.classList.remove('hidden');
                if (subFilters) subFilters.classList.remove('hidden');
                btnSub.classList.add('bg-indigo-600', 'text-white');
                btnSub.classList.remove('text-slate-400');
            }} else if (mode === 'table' && flatCont) {{
                flatCont.classList.remove('hidden');
                btnTable.classList.add('bg-indigo-600', 'text-white');
                btnTable.classList.remove('text-slate-400');
            }}
        }}

        function filterKS26Subject(subjectCode) {{
            const blocks = document.querySelectorAll('.ks26-subject-block');
            const buttons = document.querySelectorAll('.ks26-sub-filter');

            buttons.forEach(btn => {{
                if (btn.getAttribute('data-subject') === subjectCode) {{
                    btn.classList.add('bg-indigo-500/20', 'text-indigo-300', 'border-indigo-500/40', 'font-bold');
                    btn.classList.remove('bg-slate-900', 'text-slate-400');
                }} else {{
                    btn.classList.remove('bg-indigo-500/20', 'text-indigo-300', 'border-indigo-500/40', 'font-bold');
                    btn.classList.add('bg-slate-900', 'text-slate-400');
                }}
            }});

            blocks.forEach(block => {{
                if (subjectCode === 'ALL' || block.getAttribute('data-subject') === subjectCode) {{
                    block.classList.remove('hidden');
                }} else {{
                    block.classList.add('hidden');
                }}
            }});
        }}

        // Initialize on load
        document.addEventListener('DOMContentLoaded', () => {{
            renderClassSummaryTable();
            renderStudentsDetailTable(KS26_STUDENTS);
            renderGenericStaffCards(GENERIC_STAFF);
        }});
    </script>
</body>
</html>
"""

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Đã tạo thành công: {out_file}")

    # Đồng bộ sang deploy_web/
    deploy_file = os.path.join(DEPLOY_DIR, "weekly_director_report.html")
    deploy_mgmt = os.path.join(DEPLOY_DIR, "management", "weekly_director_report.html")
    os.makedirs(os.path.join(DEPLOY_DIR, "management"), exist_ok=True)
    with open(deploy_file, "w", encoding="utf-8") as f:
        f.write(html)
    with open(deploy_mgmt, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Đã đồng bộ sang: {deploy_file} & {deploy_mgmt}")

if __name__ == "__main__":
    generate_weekly_director_dashboard()

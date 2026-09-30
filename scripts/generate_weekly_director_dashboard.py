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
                            Tuần 21/09 &ndash; 25/09/2026
                        </span>
                    </div>
                    <p class="text-xs lg:text-sm text-slate-300 mt-1">
                        Phạm vi: <strong class="text-white">16 Lớp Học Kỳ II</strong> &bull; <strong class="text-white">42 Cán bộ GV/TG</strong> &bull; <strong class="text-white">1,236 Học viên PTIT</strong> &bull; Số liệu chốt 25/09/2026
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

            <!-- BANNER GIỚI THIỆU -->
            <div class="glass-panel p-5 rounded-2xl border-l-4 border-indigo-500 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 class="text-base lg:text-lg font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-chart-pie text-indigo-400"></i> TỔNG HỢP BIẾN ĐỘNG CHỈ SỐ HỌC VỤ VÀ NỀ NẾP SO VỚI TUẦN TRƯỚC
                    </h2>
                    <p class="text-xs lg:text-sm text-slate-300 mt-1">
                        Bảng thống kê chuẩn Agent 1 (Đã bỏ cột Trợ giảng theo đúng file Excel). Phân tích chi tiết Điểm nóng & Đề xuất giải pháp cho từng khối.
                    </p>
                </div>
                <div class="flex items-center gap-3 text-xs">
                    <span class="px-3 py-1.5 rounded-lg badge-danger font-bold"><i class="fa-solid fa-triangle-exclamation mr-1.5"></i>🚨 Tăng vi phạm</span>
                    <span class="px-3 py-1.5 rounded-lg badge-success font-bold"><i class="fa-solid fa-check-circle mr-1.5"></i>✅ Ổn định / Giảm</span>
                </div>
            </div>

            <!-- ------------------------------------------------------------- -->
            <!-- 1. KHÓA KS24 (KỲ IV CHUYÊN NGÀNH)                             -->
            <!-- ------------------------------------------------------------- -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-5">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between pb-4 border-b border-slate-800 gap-3">
                    <div class="flex items-center gap-3">
                        <span class="px-3.5 py-1.5 rounded-xl text-xs font-black bg-blue-500/20 text-blue-300 border border-blue-500/40 font-mono">
                            KHÓA KS24
                        </span>
                        <div>
                            <h3 class="text-base lg:text-lg font-bold text-white">1. Khóa KS24-CNTT (Hà Nội & HCM-CNTT1) &mdash; Môn Kiến Trúc Microservices</h3>
                            <p class="text-xs text-slate-400">Quy mô: 5 lớp chính quy &bull; 181 sinh viên &bull; GV: Bùi Thanh Hải, Hồ Xuân Hùng, Nguyễn Bá Minh Đạo</p>
                        </div>
                    </div>
                    <span class="text-xs font-bold px-3 py-1.5 rounded-lg bg-amber-500/10 text-amber-300 border border-amber-500/30">
                        <i class="fa-solid fa-fire mr-1"></i> Hệ số độ khó môn học CDC = 1.35 (Đồ án Microservices)
                    </span>
                </div>

                <!-- Đánh giá chỉ số so với tuần trước -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Chuyên cần toàn khóa</span>
                        <div class="flex items-baseline gap-2 mt-1.5">
                            <span class="text-2xl font-black text-white">17.57%</span>
                            <span class="text-xs font-bold text-rose-400">▲ +2.89% (Tăng vắng)</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">Xuất hiện tình trạng sinh viên tự ý nghỉ học để làm đồ án ở nhà.</p>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Nợ Bài tập / Đồ án</span>
                        <div class="flex items-baseline gap-2 mt-1.5">
                            <span class="text-2xl font-black text-white">10.45%</span>
                            <span class="text-xs font-bold text-rose-400">▲ +2.05% (Tăng nợ)</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">Bước vào các tuần kiểm tra Checkpoint đồ án Microservices.</p>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Vi phạm Elearning</span>
                        <div class="flex items-baseline gap-2 mt-1.5">
                            <span class="text-2xl font-black text-white">13.32%</span>
                            <span class="text-xs font-bold text-slate-400">-- (Duy trì cao)</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">Hai lớp CNTT1 và CNTT3 vi phạm lý thuyết EL trên 20%.</p>
                    </div>
                </div>

                <!-- Phân tích Điểm Nóng & Giải Pháp KS24 -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs lg:text-sm">
                    <div class="bg-rose-950/20 p-4 rounded-xl border border-rose-500/30 space-y-2">
                        <div class="font-bold text-rose-400 uppercase tracking-wider flex items-center gap-2">
                            <i class="fa-solid fa-triangle-exclamation"></i> Điểm nóng tại lớp nào & Vấn đề gì?
                        </div>
                        <p class="text-slate-200 leading-relaxed">
                            <strong class="text-white">Lớp HN-K24-CNTT3 (GV Hồ Xuân Hùng)</strong>: Điểm nóng báo động nhất toàn khóa. Tỷ lệ vắng chuyên cần <strong class="text-rose-400">tăng vọt +7.69% lên 33.33%</strong> (1/3 lớp nghỉ học buổi gần nhất); nợ bài tập tăng <strong class="text-rose-400">+5.13% lên 17.95%</strong>; vi phạm Elearning 20.51%.<br>
                            <strong class="text-white">Lớp HN-K24-CNTT1 (GV Bùi Thanh Hải)</strong>: Nợ bài tập 16.13% và Elearning tới 22.58%. Nhóm 14 SV đang bị nghẽn cấu hình Docker và Kubernetes.
                        </p>
                    </div>
                    <div class="bg-emerald-950/20 p-4 rounded-xl border border-emerald-500/30 space-y-2">
                        <div class="font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-2">
                            <i class="fa-solid fa-lightbulb"></i> Giải pháp điều hành & Hành động cụ thể
                        </div>
                        <ul class="text-slate-200 list-disc list-inside space-y-1.5 leading-relaxed">
                            <li><strong>Workshop kỹ thuật:</strong> Thầy Bùi Thanh Hải tổ chức 1 buổi online 90 phút ngoài giờ hỗ trợ thông đồ án và gỡ lỗi deploy Docker/K8s cho 14 sinh viên vướng mắc.</li>
                            <li><strong>Chấn chỉnh lớp CNTT3:</strong> Thầy Hồ Xuân Hùng điểm danh nghiêm 5 phút đầu buổi; dành 20 phút cuối ca thông checkpoint đồ án trực tiếp tại lớp.</li>
                            <li><strong>Cố vấn học tập (CVHT):</strong> Hotline trực tiếp cho phụ huynh sinh viên vắng liên tiếp 2 buổi trong vòng 24h để cam kết chuyên cần.</li>
                        </ul>
                    </div>
                </div>

                <!-- Bảng thống kê Agent 1 KS24 (ĐÃ BỎ CỘT TRỢ GIẢNG) -->
                <div class="overflow-x-auto rounded-xl border border-slate-800">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                            <tr>
                                <th class="py-3.5 px-5">Tên Lớp</th>
                                <th class="py-3.5 px-5">Giảng viên</th>
                                <th class="py-3.5 px-5 text-center">Chuyên cần</th>
                                <th class="py-3.5 px-5 text-center">Bài tập</th>
                                <th class="py-3.5 px-5 text-center">Elearning</th>
                                <th class="py-3.5 px-5 text-center">Xu hướng</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800">
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K24-CNTT1</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Bùi Thanh Hải</td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">16.13% <span class="text-xs text-rose-400 font-semibold">(▲ +3.23%)</span></td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">16.13% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">22.58% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K24-CNTT2</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Bùi Thanh Hải</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">10.26% <span class="text-xs text-rose-400 font-semibold">(▲ +2.57%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">10.26% <span class="text-xs text-rose-400 font-semibold">(▲ +2.57%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">7.69% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-rose-950/15">
                                <td class="py-3.5 px-5 font-extrabold text-rose-300 flex items-center gap-2">
                                    <i class="fa-solid fa-fire text-rose-500"></i> HN-K24-CNTT3
                                </td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Hồ Xuân Hùng</td>
                                <td class="py-3.5 px-5 text-center font-extrabold text-rose-400">33.33% <span class="text-xs text-rose-400 font-bold">(▲ +7.69%)</span></td>
                                <td class="py-3.5 px-5 text-center font-extrabold text-rose-400">17.95% <span class="text-xs text-rose-400 font-bold">(▲ +5.13%)</span></td>
                                <td class="py-3.5 px-5 text-center font-extrabold text-rose-400">20.51% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K24-CNTT4</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Bùi Thanh Hải</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">12.90% <span class="text-xs text-rose-400 font-semibold">(▲ +3.22%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-emerald-400">3.23% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">9.68% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HCM-K24-CNTT1</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Nguyễn Bá Minh Đạo</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">16.28% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">4.65% <span class="text-xs text-rose-400 font-semibold">(▲ +2.32%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">9.30% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- ------------------------------------------------------------- -->
            <!-- 2.1 KHÓA KS25 - KHỐI CNTT (FASTAPI & PTTKHT)                   -->
            <!-- ------------------------------------------------------------- -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-5">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between pb-4 border-b border-slate-800 gap-3">
                    <div class="flex items-center gap-3">
                        <span class="px-3.5 py-1.5 rounded-xl text-xs font-black bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 font-mono">
                            KS25 - CNTT
                        </span>
                        <div>
                            <h3 class="text-base lg:text-lg font-bold text-white">2.1 Khóa KS25 - Khối Công Nghệ Thông Tin &mdash; Môn IT105 FastAPI & PTTKHT</h3>
                            <p class="text-xs text-slate-400">Quy mô: 8 lớp chính quy (5 lớp Hà Nội, 3 lớp TP. HCM) &bull; GV: Nguyễn Quảng An, Phạm Tuấn Bình, Nguyễn Đức Minh, Trần Quốc Tuấn</p>
                        </div>
                    </div>
                    <span class="text-xs font-bold px-3 py-1.5 rounded-lg bg-indigo-500/10 text-indigo-300 border border-indigo-500/30">
                        FastAPI Web Framework & Phân Tích Thiết Kế Hệ Thống
                    </span>
                </div>

                <!-- Đánh giá chỉ số so với tuần trước -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Khối CNTT Hà Nội (5 Lớp)</span>
                        <div class="flex items-baseline gap-2 mt-1.5">
                            <span class="text-2xl font-black text-white">16.17% vắng</span>
                            <span class="text-xs font-bold text-rose-400">▲ +3.19%</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">Elearning tăng vi phạm +3.31% lên 12.97%. Bài tập hoàn thành xuất sắc (4/5 lớp đạt 0.00% nợ bài).</p>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Khối CNTT TP. HCM (3 Lớp)</span>
                        <div class="flex items-baseline gap-2 mt-1.5">
                            <span class="text-2xl font-black text-white">21.53% vắng</span>
                            <span class="text-xs font-bold text-rose-400">▲ +2.17%</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">Lớp CNTT7 vắng 34.78%, lớp CNTT6 duy trì nề nếp tốt (vắng 11.63%, EL 6.98%).</p>
                    </div>
                </div>

                <!-- Điểm nóng & Giải pháp KS25 CNTT -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs lg:text-sm">
                    <div class="bg-rose-950/20 p-4 rounded-xl border border-rose-500/30 space-y-2">
                        <div class="font-bold text-rose-400 uppercase tracking-wider flex items-center gap-2">
                            <i class="fa-solid fa-triangle-exclamation"></i> Điểm nóng Khối CNTT
                        </div>
                        <p class="text-slate-200 leading-relaxed">
                            <strong class="text-white">Lớp HCM-K25-CNTT7 (GV Nguyễn Đức Minh)</strong>: Vắng chuyên cần ở mức cao 34.78% (▲ +2.17%), Elearning 19.57%. Cần tăng cường chấn chỉnh nề nếp.<br>
                            <strong class="text-white">Lớp HN-K25-CNTT1 (GV Nguyễn Quảng An)</strong>: Vắng chuyên cần 23.68%, Elearning tăng vi phạm lên 23.68%.
                        </p>
                    </div>
                    <div class="bg-emerald-950/20 p-4 rounded-xl border border-emerald-500/30 space-y-2">
                        <div class="font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-2">
                            <i class="fa-solid fa-lightbulb"></i> Giải pháp điều hành
                        </div>
                        <ul class="text-slate-200 list-disc list-inside space-y-1.5 leading-relaxed">
                            <li><strong>Chấn chỉnh lớp HCM-CNTT7:</strong> Thầy Nguyễn Đức Minh đôn đốc sinh viên hoàn thành Elearning trước buổi học; kiểm soát chặt nề nếp chuyên cần.</li>
                            <li><strong>Kiểm soát chuyên cần HN:</strong> Thầy Nguyễn Quảng An chốt điểm danh trực tiếp trên phần mềm đầu giờ, không chấp nhận điểm danh bù cuối buổi.</li>
                        </ul>
                    </div>
                </div>

                <!-- Bảng thống kê Agent 1 KS25 CNTT (ĐÃ BỎ CỘT TRỢ GIẢNG) -->
                <div class="overflow-x-auto rounded-xl border border-slate-800">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                            <tr>
                                <th class="py-3.5 px-5">Tên Lớp</th>
                                <th class="py-3.5 px-5">Giảng viên</th>
                                <th class="py-3.5 px-5 text-center">Chuyên cần</th>
                                <th class="py-3.5 px-5 text-center">Bài tập</th>
                                <th class="py-3.5 px-5 text-center">Elearning</th>
                                <th class="py-3.5 px-5 text-center">Xu hướng</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800">
                            <!-- Hà Nội -->
                            <tr class="bg-slate-950/60 text-xs font-bold text-indigo-400 uppercase tracking-wider">
                                <td colspan="6" class="py-2.5 px-5"><i class="fa-solid fa-layer-group mr-1.5"></i> Cụm Khối CNTT Hà Nội (5 Lớp)</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-rose-950/20">
                                <td class="py-3.5 px-5 font-bold text-rose-300 flex items-center gap-2">
                                    <i class="fa-solid fa-triangle-exclamation text-rose-500"></i> HN-K25-CNTT1
                                </td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Nguyễn Quảng An</td>
                                <td class="py-3.5 px-5 text-center font-extrabold text-rose-400">31.58% <span class="text-xs text-rose-400 font-bold">(▲ +7.90%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-rose-400">15.79% <span class="text-xs text-rose-400 font-semibold">(▲ +7.90%)</span></td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">23.68% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K25-CNTT2</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Nguyễn Quảng An</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">18.60% <span class="text-xs text-emerald-400 font-semibold">(▼ -2.33%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">4.65% <span class="text-xs text-rose-400 font-semibold">(▲ +4.65%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">11.63% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-warning">🟡 Cảnh báo</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K25-CNTT3</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Phạm Tuấn Bình</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">13.95% <span class="text-xs text-rose-400 font-semibold">(▲ +2.32%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-emerald-400">0.00% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">11.63% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-warning">🟡 Theo dõi</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K25-CNTT4</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Phạm Tuấn Bình</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-emerald-400">4.76% <span class="text-xs text-rose-400 font-semibold">(▲ +2.38%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">2.38% <span class="text-xs text-rose-400 font-semibold">(▲ +2.38%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-emerald-400">7.14% <span class="text-xs text-rose-400 font-semibold">(▲ +2.38%)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-success">✅ Tốt</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-rose-950/15">
                                <td class="py-3.5 px-5 font-bold text-rose-300">HN-K25-CNTT5</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Nguyễn Quảng An</td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">24.44% <span class="text-xs text-rose-400 font-semibold">(▲ +2.22%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">4.44% <span class="text-xs text-rose-400 font-semibold">(▲ +4.44%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">13.33% <span class="text-xs text-rose-400 font-semibold">(▲ +0.20%)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>

                            <!-- TP. HCM -->
                            <tr class="bg-slate-950/60 text-xs font-bold text-cyan-400 uppercase tracking-wider">
                                <td colspan="6" class="py-2.5 px-5"><i class="fa-solid fa-layer-group mr-1.5"></i> Cụm Khối CNTT TP. HCM (4 Lớp)</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HCM-K25-CNTT5</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Nguyễn Đức Minh</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">13.64% <span class="text-xs text-rose-400 font-semibold">(▲ +2.28%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-emerald-400">0.00% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">18.18% <span class="text-xs text-rose-400 font-semibold">(▲ +2.27%)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HCM-K25-CNTT6</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Trần Quốc Tuấn</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">11.63% <span class="text-xs text-emerald-400 font-semibold">(▼ -0.27%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-emerald-400">0.00% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-emerald-400">6.98% <span class="text-xs text-emerald-400 font-semibold">(▼ -0.16%)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-success">✅ Ổn định</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HCM-K25-CNTT7</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Nguyễn Đức Minh</td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">34.78% <span class="text-xs text-rose-400 font-semibold">(▲ +2.17%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">8.70% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-rose-400">19.57% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- ------------------------------------------------------------- -->
            <!-- 2.2 KHÓA KS25 - KHỐI QTKD (MAN107 QUẢN TRỊ HỌC)                -->
            <!-- ------------------------------------------------------------- -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-5">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between pb-4 border-b border-slate-800 gap-3">
                    <div class="flex items-center gap-3">
                        <span class="px-3.5 py-1.5 rounded-xl text-xs font-black bg-amber-500/20 text-amber-300 border border-amber-500/40 font-mono">
                            KS25 - QTKD
                        </span>
                        <div>
                            <h3 class="text-base lg:text-lg font-bold text-white">2.2 Khóa KS25 - Khối Quản Trị Kinh Doanh &mdash; Môn MAN107 Quản Trị Học</h3>
                            <p class="text-xs text-slate-400">Quy mô: 2 lớp chính quy (đã sáp nhập lớp QTKD3) &bull; 88 sinh viên &bull; GV phụ trách: Đặng Quỳnh Trang</p>
                        </div>
                    </div>
                    <span class="text-xs font-bold px-3 py-1.5 rounded-lg bg-amber-500/10 text-amber-300 border border-amber-500/30">
                        <i class="fa-solid fa-arrows-split-up-and-left mr-1"></i> Tái cơ cấu: Lớp QTKD3 đã giải thể và sáp nhập sang QTKD1 & QTKD2
                    </span>
                </div>

                <!-- Đánh giá chỉ số so với tuần trước -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Chuyên cần vắng toàn khối</span>
                        <div class="flex items-baseline gap-2 mt-1.5">
                            <span class="text-2xl font-black text-rose-400">46.59%</span>
                            <span class="text-xs font-bold text-slate-400">-- (Duy trì rất cao)</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">Lớp QTKD1 tiếp nhận 13 SV từ QTKD3 (33 ➔ 46 SV), tỷ lệ vắng lên đến 56.52%.</p>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Nợ Bài tập tình huống</span>
                        <div class="flex items-baseline gap-2 mt-1.5">
                            <span class="text-2xl font-black text-slate-200">11.36%</span>
                            <span class="text-xs font-bold text-slate-400">-- (Ổn định)</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">Nợ bài tập duy trì ở mức kiểm soát được (QTKD1: 10.87%, QTKD2: 11.90%).</p>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Vi phạm Elearning</span>
                        <div class="flex items-baseline gap-2 mt-1.5">
                            <span class="text-2xl font-black text-slate-200">19.32%</span>
                            <span class="text-xs font-bold text-slate-400">-- (Ổn định)</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">Lớp QTKD2 có 26.19% SV chưa hoàn thành lý thuyết trước buổi học.</p>
                    </div>
                </div>

                <!-- Điểm nóng & Giải pháp KS25 QTKD -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs lg:text-sm">
                    <div class="bg-rose-950/20 p-4 rounded-xl border border-rose-500/30 space-y-2">
                        <div class="font-bold text-rose-400 uppercase tracking-wider flex items-center gap-2">
                            <i class="fa-solid fa-triangle-exclamation"></i> Điểm nóng Khối QTKD
                        </div>
                        <p class="text-slate-200 leading-relaxed">
                            <strong class="text-white">Lớp HN-K25-QTKD1 (GV Đặng Quỳnh Trang)</strong>: Tỷ lệ vắng mặt chuyên cần kỷ lục <strong class="text-rose-400">56.52%</strong> (hơn 1 nửa lớp vắng học), nợ bài tập 10.87%, vi phạm Elearning 13.04%. Sau sáp nhập từ 33 lên 46 SV, lớp chưa ổn định nền nếp tổ chức.
                        </p>
                    </div>
                    <div class="bg-emerald-950/20 p-4 rounded-xl border border-emerald-500/30 space-y-2">
                        <div class="font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-2">
                            <i class="fa-solid fa-lightbulb"></i> Giải pháp điều hành
                        </div>
                        <ul class="text-slate-200 list-disc list-inside space-y-1.5 leading-relaxed">
                            <li><strong>Ổn định tổ chức:</strong> Lãnh đạo Viện cùng cô Đặng Quỳnh Trang rà soát danh sách điểm danh; chia nhỏ 46 SV thành các nhóm thuyết trình case-study tình huống bắt buộc có mặt trên lớp để kéo sinh viên quay trở lại giảng đường.</li>
                            <li><strong>Phân luồng học vụ:</strong> CVHT lập danh sách sinh viên vắng trên 3 buổi chuyển phòng QLCLĐT để gửi cảnh báo học vụ chính thức về gia đình.</li>
                        </ul>
                    </div>
                </div>

                <!-- Bảng thống kê Agent 1 KS25 QTKD (ĐÃ BỎ CỘT TRỢ GIẢNG) -->
                <div class="overflow-x-auto rounded-xl border border-slate-800">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                            <tr>
                                <th class="py-3.5 px-5">Tên Lớp</th>
                                <th class="py-3.5 px-5">Giảng viên</th>
                                <th class="py-3.5 px-5 text-center">Chuyên cần</th>
                                <th class="py-3.5 px-5 text-center">Bài tập</th>
                                <th class="py-3.5 px-5 text-center">Elearning</th>
                                <th class="py-3.5 px-5 text-center">Xu hướng</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800">
                            <tr class="hover:bg-slate-800/40 bg-rose-950/15">
                                <td class="py-3.5 px-5 font-extrabold text-rose-300 flex items-center gap-2">
                                    <i class="fa-solid fa-triangle-exclamation text-rose-500"></i> HN-K25-QTKD1
                                </td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Đặng Quỳnh Trang</td>
                                <td class="py-3.5 px-5 text-center font-extrabold text-rose-400">56.52% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">10.87% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">13.04% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-success">✅ Ổn định</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K25-QTKD2</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Đặng Quỳnh Trang</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-rose-400">35.71% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">11.90% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-rose-400">26.19% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-success">✅ Ổn định</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Bảng thống kê Môn mới: BI (Business Intelligence) Khởi động 29/09/2026 -->
                <div class="mt-4 pt-4 border-t border-slate-800 space-y-3">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-1 rounded-md text-xs font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-mono">MÔN MỚI</span>
                            <h4 class="text-sm font-bold text-white flex items-center gap-1.5">
                                <i class="fa-solid fa-chart-pie text-emerald-400"></i> Môn Business Intelligence (BI) &mdash; Khởi động ngày 29/09/2026
                            </h4>
                        </div>
                        <span class="text-xs text-emerald-400 font-bold bg-emerald-950/40 px-3 py-1 rounded-full border border-emerald-500/30">
                            🎉 100% Chuyên Cần Buổi 1
                        </span>
                    </div>

                    <div class="overflow-x-auto rounded-xl border border-slate-800">
                        <table class="w-full text-left text-sm">
                            <thead class="bg-slate-900/90 text-slate-300 uppercase font-bold text-xs border-b border-slate-800">
                                <tr>
                                    <th class="py-3 px-5">Tên Lớp</th>
                                    <th class="py-3 px-5">Giảng viên</th>
                                    <th class="py-3 px-5 text-center">Chuyên cần</th>
                                    <th class="py-3 px-5 text-center">Bài tập</th>
                                    <th class="py-3 px-5 text-center">Elearning</th>
                                    <th class="py-3 px-5 text-center">Trạng thái</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-800">
                                <tr class="hover:bg-slate-800/40 bg-emerald-950/10">
                                    <td class="py-3 px-5 font-bold text-white">HN-K25-QTKD1 (46 SV)</td>
                                    <td class="py-3 px-5 text-slate-300 font-medium">Hoàng Thị Kim Oanh</td>
                                    <td class="py-3 px-5 text-center font-bold text-emerald-400">0.00% <span class="text-xs text-emerald-400 font-bold">(Đủ 100%)</span></td>
                                    <td class="py-3 px-5 text-center font-bold text-emerald-400">0.00%</td>
                                    <td class="py-3 px-5 text-center font-semibold text-slate-200">6.52%</td>
                                    <td class="py-3 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-success">🟢 Chuẩn mực</span></td>
                                </tr>
                                <tr class="hover:bg-slate-800/40 bg-emerald-950/10">
                                    <td class="py-3 px-5 font-bold text-white">HN-K25-QTKD2 (42 SV)</td>
                                    <td class="py-3 px-5 text-slate-300 font-medium">Lê Thành Ngọc</td>
                                    <td class="py-3 px-5 text-center font-bold text-emerald-400">0.00% <span class="text-xs text-emerald-400 font-bold">(Đủ 100%)</span></td>
                                    <td class="py-3 px-5 text-center font-bold text-emerald-400">0.00%</td>
                                    <td class="py-3 px-5 text-center font-semibold text-slate-200">7.14%</td>
                                    <td class="py-3 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-success">🟢 Chuẩn mực</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ------------------------------------------------------------- -->
            <!-- 3. KHÓA KS26 (TÂN SINH VIÊN)                                  -->
            <!-- ------------------------------------------------------------- -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-5">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between pb-4 border-b border-slate-800 gap-3">
                    <div class="flex items-center gap-3">
                        <span class="px-3.5 py-1.5 rounded-xl text-xs font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-mono">
                            KHÓA KS26
                        </span>
                        <div>
                            <h3 class="text-base lg:text-lg font-bold text-white">3. Khóa KS26 Tân Sinh Viên &mdash; Môn SSK101 Kỹ Năng Học Tập Chủ Động</h3>
                            <p class="text-xs text-slate-400">Quy mô: 10 lớp chính quy &bull; 396 sinh viên (374 SV khảo sát chi tiết) &bull; Tuần học đầu tiên</p>
                        </div>
                    </div>
                    <span class="text-xs font-bold px-3 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
                        <i class="fa-solid fa-graduation-cap mr-1"></i> Giai đoạn thích nghi phương pháp học Đại học
                    </span>
                </div>

                <!-- Đánh giá chỉ số so với tuần trước -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Chuyên cần tuần đầu (Toàn khóa)</span>
                        <div class="flex items-baseline gap-2 mt-1.5">
                            <span class="text-2xl font-black text-white">28.4% vắng</span>
                            <span class="text-xs font-bold text-rose-400">▲ +7.7% so với khai giảng</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">Sinh viên đã bắt đầu có tình trạng vắng rải rác ở ca sáng sớm.</p>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Chuẩn bị bài trực tuyến Elearning</span>
                        <div class="flex items-baseline gap-2 mt-1.5">
                            <span class="text-2xl font-black text-rose-400">47.4% vi phạm</span>
                            <span class="text-xs font-bold text-rose-400">▲ Điểm nghẽn lớn nhất</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">Sinh viên chưa hoàn thành lý thuyết trước giờ lên lớp.</p>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                        <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Nộp Bài tập về nhà</span>
                        <div class="flex items-baseline gap-2 mt-1.5">
                            <span class="text-2xl font-black text-amber-400">69.5% có nợ bài</span>
                            <span class="text-xs font-bold text-amber-400">Cần cứu xét bảo lãnh</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">Nhiều sinh viên chưa quen thao tác nộp bài trên LMS AI.</p>
                    </div>
                </div>

                <!-- Điểm nóng & Giải pháp KS26 -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs lg:text-sm">
                    <div class="bg-rose-950/20 p-4 rounded-xl border border-rose-500/30 space-y-2">
                        <div class="font-bold text-rose-400 uppercase tracking-wider flex items-center gap-2">
                            <i class="fa-solid fa-triangle-exclamation"></i> Điểm nóng Khóa KS26
                        </div>
                        <p class="text-slate-200 leading-relaxed">
                            <strong class="text-white">Lớp HCM-K26-CNTT1 (GV Nguyễn Bá Minh Đạo)</strong>: Báo động đỏ toàn diện với vi phạm Elearning lên tới <strong class="text-rose-400">95.74%</strong> (tăng vọt +29.78%), nợ bài tập 27.66%, vắng chuyên cần 31.91%.<br>
                            <strong class="text-white">Lớp HCM-K26-CNTT2</strong>: Vi phạm Elearning <strong class="text-rose-400">91.11%</strong>.<br>
                            <strong class="text-white">Lớp HN-K26-CNTT1 (GV Trần Minh Cường)</strong>: Vắng chuyên cần <strong class="text-rose-400">50.00%</strong> (tăng +7.5%), Elearning 60.0%.<br>
                            <strong class="text-white">Lớp HN-K26-CNTT3</strong>: 8 sinh viên bị lỗi định danh LMS khiến bài nộp không ghi nhận.
                        </p>
                    </div>
                    <div class="bg-emerald-950/20 p-4 rounded-xl border border-emerald-500/30 space-y-2">
                        <div class="font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-2">
                            <i class="fa-solid fa-lightbulb"></i> Giải pháp điều hành
                        </div>
                        <ul class="text-slate-200 list-disc list-inside space-y-1.5 leading-relaxed">
                            <li><strong>Phê duyệt các đơn bảo lãnh LMS:</strong> Xem xét phê duyệt các đơn bảo lãnh có điều kiện hoàn thành bài bù để nâng tỷ lệ dự thi toàn khóa.</li>
                            <li><strong>Xử lý dứt điểm kỹ thuật LMS:</strong> Đội ngũ LMS AI hỗ trợ đồng bộ ngay tài khoản cho 8 sinh viên lớp HN-CNTT3.</li>
                            <li><strong>Thiết lập nề nếp tại HCM:</strong> Thầy Nguyễn Bá Minh Đạo dành 15 phút đầu giờ hướng dẫn trực tiếp quy trình click học Elearning trên điện thoại/laptop cho sinh viên HCM1 & HCM2.</li>
                        </ul>
                    </div>
                </div>

                <!-- Bảng thống kê Agent 1 KS26 (ĐÃ BỎ CỘT TRỢ GIẢNG) -->
                <div class="overflow-x-auto rounded-xl border border-slate-800">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                            <tr>
                                <th class="py-3.5 px-5">Tên Lớp</th>
                                <th class="py-3.5 px-5">Giảng viên</th>
                                <th class="py-3.5 px-5 text-center">Chuyên cần</th>
                                <th class="py-3.5 px-5 text-center">Bài tập</th>
                                <th class="py-3.5 px-5 text-center">Elearning</th>
                                <th class="py-3.5 px-5 text-center">Xu hướng</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800">
                            <!-- Hà Nội -->
                            <tr class="bg-slate-950/60 text-xs font-bold text-emerald-400 uppercase tracking-wider">
                                <td colspan="6" class="py-2.5 px-5"><i class="fa-solid fa-layer-group mr-1.5"></i> Cụm Khóa KS26 Hà Nội</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-rose-950/15">
                                <td class="py-3.5 px-5 font-extrabold text-rose-300 flex items-center gap-2">
                                    <i class="fa-solid fa-fire text-rose-500"></i> HN-K26-CNTT1
                                </td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Trần Minh Cường</td>
                                <td class="py-3.5 px-5 text-center font-extrabold text-rose-400">50.00% <span class="text-xs text-rose-400 font-bold">(▲ +7.50%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">15.00% <span class="text-xs text-emerald-400 font-semibold">(▼ -2.50%)</span></td>
                                <td class="py-3.5 px-5 text-center font-extrabold text-rose-400">60.00% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K26-CNTT2</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Hồ Xuân Hùng</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">25.58% <span class="text-xs text-rose-400 font-semibold">(▲ +2.32%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-emerald-400">0.00% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-emerald-400">4.65% <span class="text-xs text-rose-400 font-semibold">(▲ +4.65%)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K26-CNTT3</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Nguyễn Duy Quang</td>
                                <td class="py-3.5 px-5 text-center font-bold text-rose-400">43.90% <span class="text-xs text-rose-400 font-semibold">(▲ +4.88%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">2.44% <span class="text-xs text-rose-400 font-semibold">(▲ +2.44%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-emerald-400">0.00% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K26-QTKD1</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Hoàng Thị Hậu</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">22.73% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">9.09% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-rose-400">29.55% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-success">✅ Ổn định</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K26-QTKD2</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Hoàng Thị Kim Oanh</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">25.00% <span class="text-xs text-rose-400 font-semibold">(▲ +6.82%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">9.09% <span class="text-xs text-emerald-400 font-semibold">(▼ -2.27%)</span></td>
                                <td class="py-3.5 px-5 text-center font-extrabold text-rose-400">61.36% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-3.5 px-5 font-bold text-white">HN-K26-QTKD3</td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Hoàng Thị Hậu</td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">27.27% <span class="text-xs text-rose-400 font-semibold">(▲ +25.00%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-slate-200">13.64% <span class="text-xs text-rose-400 font-semibold">(▲ +9.09%)</span></td>
                                <td class="py-3.5 px-5 text-center font-semibold text-rose-400">34.09% <span class="text-xs text-slate-400">(--)</span></td>
                                <td class="py-3.5 px-5 text-center"><span class="px-3 py-1 rounded text-xs font-bold badge-danger">🚨 Tăng</span></td>
                            </tr>

                            <!-- TP. HCM -->
                            <tr class="bg-slate-950/60 text-xs font-bold text-purple-400 uppercase tracking-wider">
                                <td colspan="6" class="py-2.5 px-5"><i class="fa-solid fa-layer-group mr-1.5"></i> Cụm Khóa KS26 TP. HCM</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-rose-950/20">
                                <td class="py-3.5 px-5 font-extrabold text-rose-300 flex items-center gap-2">
                                    <i class="fa-solid fa-radiation text-rose-500 animate-pulse"></i> HCM-K26-CNTT1
                                </td>
                                <td class="py-3.5 px-5 text-slate-300 font-medium">Nguyễn Bá Minh Đạo</td>
                                <td class="py-3.5 px-5 text-center font-extrabold text-rose-400">31.91% <span class="text-xs text-rose-400 font-bold">(▲ +8.51%)</span></td>
                                <td class="py-3.5 px-5 text-center font-extrabold text-rose-400">27.66% <span class="text-xs text-rose-400 font-bold">(▲ +10.64%)</span></td>
                                <td class="py-3.5 px-5 text-center font-black text-rose-500 text-base">95.74% <span class="text-xs text-rose-400 font-bold">(▲ +29.78%)</span></td>
                                    <!-- ------------------------------------------------------------- -->
            <!-- 3.2 TIẾN ĐỘ ĐÀO TẠO ĐA MÔN HỌC ĐỒNG THỜI KHÓA KS26 (TỪ 28/09/2026) -->
            <!-- ------------------------------------------------------------- -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-6">
                <!-- Header Section -->
                <div class="flex flex-col lg:flex-row lg:items-center justify-between pb-4 border-b border-slate-800 gap-3">
                    <div class="flex items-center gap-3">
                        <span class="px-3.5 py-1.5 rounded-xl text-xs font-black bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-mono">
                            KS26 - ĐA MÔN ĐỒNG THỜI
                        </span>
                        <div>
                            <h3 class="text-base lg:text-lg font-bold text-white">3.2 Tiến Độ Đào Tạo Đa Môn Học Đồng Thời Khóa KS26 (Từ 28/09/2026)</h3>
                            <p class="text-xs text-slate-400">Quy mô: 10 lớp chính quy (416 SV) &bull; Đào tạo song song 5 môn: Chuyên ngành CNTT, Kỹ năng làm việc nhóm, Tiếng Anh, Tư duy phân tích & Tin học ứng dụng</p>
                        </div>
                    </div>
                    <span class="text-xs font-bold px-3 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
                        <i class="fa-solid fa-check-double mr-1"></i> Hiệu chuẩn chuẩn hóa theo LMS Frontend (>10% CC & BTVN đến hạn)
                    </span>
                </div>

                <!-- Ghi chú nghiệp vụ tính chỉ số chuẩn hóa -->
                <div class="bg-indigo-950/20 p-4 rounded-xl border border-indigo-500/30 text-xs space-y-1 text-slate-300 leading-relaxed">
                    <div class="font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-1.5 mb-1">
                        <i class="fa-solid fa-circle-info"></i> Quy chuẩn tính chỉ số vi phạm theo Frontend LMS:
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
                        <div class="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80">
                            <span class="font-bold text-white block mb-0.5">📌 Vi phạm Chuyên cần > 10%:</span>
                            <span>Tính SV vắng vượt 10% tổng buổi môn. Ở buổi 1 môn 22 buổi (IT108), vắng 1 buổi = 4.5% &le; 10% &rarr; <strong>Tỷ lệ vi phạm CC > 10% là 0.00%</strong>.</span>
                        </div>
                        <div class="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80">
                            <span class="font-bold text-white block mb-0.5">📌 Vi phạm Bài tập > 10%:</span>
                            <span>Tính trên số bài tập thực tế đã giao và đến hạn nộp trong tuần. Buổi 1 chưa đến hạn &rarr; <strong>Tỷ lệ vi phạm BTVN > 10% là 0.00%</strong> (không chia cho 21 bài cả môn).</span>
                        </div>
                        <div class="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80">
                            <span class="font-bold text-white block mb-0.5">📌 Elearning:</span>
                            <span>Tỷ lệ SV nộp muộn hoặc chưa hoàn thành bài lý thuyết trước buổi học (ví dụ: HN1 có 2/43 SV vi phạm &rarr; <strong>4.65%</strong>).</span>
                        </div>
                    </div>
                </div>

                <!-- STATS CARDS THEO 5 MÔN HỌC -->
                <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
                    <div class="bg-slate-900/70 p-3.5 rounded-xl border border-indigo-500/30">
                        <div class="flex items-center justify-between text-xs font-bold text-indigo-300 mb-1">
                            <span>💻 IT108 - CNTT</span>
                            <span class="px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-200">6 Lớp</span>
                        </div>
                        <div class="text-lg font-black text-white">0.00% <span class="text-xs font-normal text-slate-400">CC>10%</span></div>
                        <p class="text-[11px] text-slate-400 mt-1">EL TB: 7.05% &bull; Điểm nóng HN4 (22.2%)</p>
                    </div>

                    <div class="bg-slate-900/70 p-3.5 rounded-xl border border-cyan-500/30">
                        <div class="flex items-center justify-between text-xs font-bold text-cyan-300 mb-1">
                            <span>🤝 SKL01 - Teamwork</span>
                            <span class="px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-200">2 Lớp</span>
                        </div>
                        <div class="text-lg font-black text-white">3.58% <span class="text-xs font-normal text-slate-400">CC>10%</span></div>
                        <p class="text-[11px] text-slate-400 mt-1">EL TB: 10.64% &bull; HN1 đôn đốc EL (16.3%)</p>
                    </div>

                    <div class="bg-slate-900/70 p-3.5 rounded-xl border border-emerald-500/30">
                        <div class="flex items-center justify-between text-xs font-bold text-emerald-300 mb-1">
                            <span>🗣️ ENG105 - Tiếng Anh</span>
                            <span class="px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-200">4 Lớp</span>
                        </div>
                        <div class="text-lg font-black text-white">0.00% <span class="text-xs font-normal text-slate-400">CC>10%</span></div>
                        <p class="text-[11px] text-slate-400 mt-1">HN3 & QTKD3 đạt 0% &bull; HCM-QTKD1 30.4%</p>
                    </div>

                    <div class="bg-slate-900/70 p-3.5 rounded-xl border border-amber-500/30">
                        <div class="flex items-center justify-between text-xs font-bold text-amber-300 mb-1">
                            <span>📊 SSK103 - Tư duy PT</span>
                            <span class="px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-200">2 Lớp</span>
                        </div>
                        <div class="text-lg font-black text-white">4.55% <span class="text-xs font-normal text-slate-400">CC>10%</span></div>
                        <p class="text-[11px] text-slate-400 mt-1">HN-QTKD1: 4 SV vắng &bull; QTKD2 chuẩn bị học</p>
                    </div>

                    <div class="bg-slate-900/70 p-3.5 rounded-xl border border-purple-500/30">
                        <div class="flex items-center justify-between text-xs font-bold text-purple-300 mb-1">
                            <span>🖥️ SSK102 - Tin học UD</span>
                            <span class="px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-200">2 Lớp</span>
                        </div>
                        <div class="text-lg font-black text-rose-400">13.44% <span class="text-xs font-normal text-slate-400">CC>10%</span></div>
                        <p class="text-[11px] text-slate-400 mt-1">Điểm nóng HN-QTKD3 vắng 18.2% (8 SV)</p>
                    </div>
                </div>

                <!-- CONTROLS: VIEW TOGGLE & SUBJECT FILTER PILLS -->
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 pt-2">
                    <!-- View Mode Toggle -->
                    <div class="flex items-center gap-1.5 bg-slate-900 p-1 rounded-xl border border-slate-800 text-xs font-bold">
                        <button type="button" id="btn-ks26-view-cards" onclick="switchKS26View('cards')" class="px-3 py-1.5 rounded-lg bg-indigo-600 text-white transition-all shadow-sm">
                            <i class="fa-solid fa-grip mr-1"></i> 🗂️ Thẻ Lớp Học Đa Môn (Khuyên dùng)
                        </button>
                        <button type="button" id="btn-ks26-view-subject" onclick="switchKS26View('subject')" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition-all">
                            <i class="fa-solid fa-book-open mr-1"></i> 📚 Phân Bảng Theo Môn Học
                        </button>
                        <button type="button" id="btn-ks26-view-table" onclick="switchKS26View('table')" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition-all">
                            <i class="fa-solid fa-table-list mr-1"></i> 📋 Bảng Phẳng (Không Gộp Cột)
                        </button>
                    </div>

                    <!-- Subject Filters (Active in Subject View) -->
                    <div id="ks26-subject-filters" class="hidden flex flex-wrap items-center gap-1.5 text-xs font-medium">
                        <span class="text-slate-400 text-[11px] mr-1">Lọc môn:</span>
                        <button type="button" onclick="filterKS26Subject('ALL')" class="ks26-sub-filter px-2.5 py-1 rounded-lg bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 font-bold" data-subject="ALL">Tất Cả Môn</button>
                        <button type="button" onclick="filterKS26Subject('IT108')" class="ks26-sub-filter px-2.5 py-1 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800" data-subject="IT108">💻 IT108 (6)</button>
                        <button type="button" onclick="filterKS26Subject('SKL01')" class="ks26-sub-filter px-2.5 py-1 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800" data-subject="SKL01">🤝 SKL01 (2)</button>
                        <button type="button" onclick="filterKS26Subject('ENG105')" class="ks26-sub-filter px-2.5 py-1 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800" data-subject="ENG105">🗣️ ENG105 (4)</button>
                        <button type="button" onclick="filterKS26Subject('SSK103')" class="ks26-sub-filter px-2.5 py-1 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800" data-subject="SSK103">📊 SSK103 (2)</button>
                        <button type="button" onclick="filterKS26Subject('SSK102')" class="ks26-sub-filter px-2.5 py-1 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800" data-subject="SSK102">🖥️ SSK102 (2)</button>
                    </div>
                </div>

                <!-- ============================================================= -->
                <!-- VIEW CONTAINER 1: CLASS CARDS GRID (DEFAULT - SIÊU DỄ NHÌN)   -->
                <!-- ============================================================= -->
                <div id="ks26-cards-container" class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    <!-- CARD 1: HN-KS26-CNTT1 -->
                    <div class="bg-slate-900/90 rounded-xl border border-slate-800 p-4 space-y-3 hover:border-slate-700 transition-all">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-white text-base">HN-KS26-CNTT1</span>
                                <span class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono text-xs font-semibold">43 SV</span>
                            </div>
                            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">Hà Nội &bull; CNTT</span>
                        </div>
                        <!-- Subject 1 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-indigo-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-indigo-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-code text-[11px]"></i> Nhập môn CNTT (IT108-K26)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Trịnh Quốc Hai</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-slate-200">4.65%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">22 buổi &bull; Buổi 1</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-success text-[10px]">🟢 Chuẩn mực</span>
                            </div>
                        </div>
                        <!-- Subject 2 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-cyan-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-cyan-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-users text-[11px]"></i> Kỹ năng làm việc nhóm (SKL01)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Hoàng Thị Hậu</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-slate-200">4.65%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-amber-400">16.28%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">Kỹ năng mềm</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-warning text-[10px]">🟡 Đôn đốc EL</span>
                            </div>
                        </div>
                    </div>

                    <!-- CARD 2: HN-KS26-CNTT2 -->
                    <div class="bg-slate-900/90 rounded-xl border border-slate-800 p-4 space-y-3 hover:border-slate-700 transition-all">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-white text-base">HN-KS26-CNTT2</span>
                                <span class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono text-xs font-semibold">40 SV</span>
                            </div>
                            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">Hà Nội &bull; CNTT</span>
                        </div>
                        <!-- Subject 1 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-indigo-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-indigo-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-code text-[11px]"></i> Nhập môn CNTT (IT108-K26)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Trịnh Quốc Hai</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-slate-500">--</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-slate-500">--</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-slate-500">--</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">22 buổi</span>
                                <span class="px-2 py-0.5 rounded font-bold bg-slate-800 text-slate-400 border border-slate-700 text-[10px]">⏳ Chuẩn bị học</span>
                            </div>
                        </div>
                        <!-- Subject 2 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-cyan-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-cyan-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-users text-[11px]"></i> Kỹ năng làm việc nhóm (SKL01)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Hoàng Thị Hậu</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-slate-200">2.50%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-emerald-400">5.00%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">Kỹ năng mềm</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-success text-[10px]">🟢 Khởi đầu tốt</span>
                            </div>
                        </div>
                    </div>

                    <!-- CARD 3: HN-KS26-CNTT3 -->
                    <div class="bg-slate-900/90 rounded-xl border border-slate-800 p-4 space-y-3 hover:border-slate-700 transition-all">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-white text-base">HN-KS26-CNTT3</span>
                                <span class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono text-xs font-semibold">42 SV</span>
                            </div>
                            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">Hà Nội &bull; CNTT</span>
                        </div>
                        <!-- Subject 1 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-indigo-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-indigo-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-code text-[11px]"></i> Nhập môn CNTT (IT108-K26)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Lương Quốc Tuấn</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">22 buổi &bull; Buổi 1</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-success text-[10px]">🟢 Xuất sắc (0%)</span>
                            </div>
                        </div>
                        <!-- Subject 2 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-emerald-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-emerald-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-comments text-[11px]"></i> Tiếng Anh Giao tiếp (ENG105)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Lò Thị Ngọc Anh</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">Ngoại ngữ</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-success text-[10px]">🟢 Hoàn hảo (0%)</span>
                            </div>
                        </div>
                    </div>

                    <!-- CARD 4: HN-KS26-CNTT4 -->
                    <div class="bg-slate-900/90 rounded-xl border border-slate-800 p-4 space-y-3 hover:border-slate-700 transition-all">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-white text-base">HN-KS26-CNTT4</span>
                                <span class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono text-xs font-semibold">27 SV</span>
                            </div>
                            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">Hà Nội &bull; CNTT</span>
                        </div>
                        <!-- Subject 1 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-indigo-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-indigo-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-code text-[11px]"></i> Nhập môn CNTT (IT108-K26)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Lương Quốc Tuấn</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-extrabold text-rose-400">22.22%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">22 buổi &bull; Buổi 1</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-danger text-[10px]">🚨 Nhắc EL (6 SV)</span>
                            </div>
                        </div>
                    </div>

                    <!-- CARD 5: HCM-KS26-CNTT1 -->
                    <div class="bg-slate-900/90 rounded-xl border border-slate-800 p-4 space-y-3 hover:border-slate-700 transition-all">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-white text-base">HCM-KS26-CNTT1</span>
                                <span class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono text-xs font-semibold">46 SV</span>
                            </div>
                            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">TP. HCM &bull; CNTT</span>
                        </div>
                        <!-- Subject 1 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-indigo-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-indigo-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-code text-[11px]"></i> Nhập môn CNTT (IT108-K26)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Lê Hà Thanh Sang</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-slate-200">6.52%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">22 buổi &bull; Buổi 1</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-success text-[10px]">🟢 Nề nếp tốt</span>
                            </div>
                        </div>
                    </div>

                    <!-- CARD 6: HCM-KS26-CNTT2 -->
                    <div class="bg-slate-900/90 rounded-xl border border-slate-800 p-4 space-y-3 hover:border-slate-700 transition-all">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-white text-base">HCM-KS26-CNTT2</span>
                                <span class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono text-xs font-semibold">45 SV</span>
                            </div>
                            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">TP. HCM &bull; CNTT</span>
                        </div>
                        <!-- Subject 1 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-indigo-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-indigo-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-code text-[11px]"></i> Nhập môn CNTT (IT108-K26)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Lê Hà Thanh Sang</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-slate-200">8.89%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">22 buổi &bull; Buổi 1</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-success text-[10px]">🟢 Ổn định</span>
                            </div>
                        </div>
                        <!-- Subject 2 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-emerald-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-emerald-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-comments text-[11px]"></i> Tiếng Anh Giao tiếp (ENG105)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Huỳnh Thị Kim Khánh</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-amber-400">11.11%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">Ngoại ngữ</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-warning text-[10px]">🟡 Theo dõi EL</span>
                            </div>
                        </div>
                    </div>

                    <!-- CARD 7: HN-KS26-QTKD1 -->
                    <div class="bg-slate-900/90 rounded-xl border border-slate-800 p-4 space-y-3 hover:border-slate-700 transition-all">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-white text-base">HN-KS26-QTKD1</span>
                                <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono text-xs font-semibold">44 SV</span>
                            </div>
                            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">Hà Nội &bull; QTKD</span>
                        </div>
                        <!-- Subject 1 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-amber-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-amber-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-chart-line text-[11px]"></i> Tư duy phân tích (SSK103)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Nguyễn Ngọc Vân Khanh</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-slate-200">9.09%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-slate-200">6.82%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">Kỹ năng nền tảng</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-warning text-[10px]">🟡 4 SV vắng</span>
                            </div>
                        </div>
                    </div>

                    <!-- CARD 8: HN-KS26-QTKD2 -->
                    <div class="bg-slate-900/90 rounded-xl border border-slate-800 p-4 space-y-3 hover:border-slate-700 transition-all">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-white text-base">HN-KS26-QTKD2</span>
                                <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono text-xs font-semibold">44 SV</span>
                            </div>
                            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">Hà Nội &bull; QTKD</span>
                        </div>
                        <!-- Subject 1 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-amber-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-amber-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-chart-line text-[11px]"></i> Tư duy phân tích (SSK103)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Nguyễn Ngọc Vân Khanh</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-slate-500">--</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-slate-500">--</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-slate-500">--</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">Kỹ năng nền tảng</span>
                                <span class="px-2 py-0.5 rounded font-bold bg-slate-800 text-slate-400 border border-slate-700 text-[10px]">⏳ Chuẩn bị học</span>
                            </div>
                        </div>
                    </div>

                    <!-- CARD 9: HN-KS26-QTKD3 -->
                    <div class="bg-slate-900/90 rounded-xl border border-slate-800 p-4 space-y-3 hover:border-slate-700 transition-all">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-white text-base">HN-KS26-QTKD3</span>
                                <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono text-xs font-semibold">44 SV</span>
                            </div>
                            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">Hà Nội &bull; QTKD</span>
                        </div>
                        <!-- Subject 1 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-emerald-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-emerald-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-comments text-[11px]"></i> Tiếng Anh Giao tiếp (ENG105)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Nguyễn Hồng Nhung</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">Ngoại ngữ</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-success text-[10px]">🟢 Hoàn hảo (0%)</span>
                            </div>
                        </div>
                        <!-- Subject 2 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-purple-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-purple-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-desktop text-[11px]"></i> Tin học ứng dụng (SSK102)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Nguyễn Thị Hồng Minh</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-extrabold text-rose-400">18.18%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-slate-200">9.09%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">Đại cương</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-danger text-[10px]">🚨 8 SV vắng</span>
                            </div>
                        </div>
                    </div>

                    <!-- CARD 10: HCM-KS26-QTKD1 -->
                    <div class="bg-slate-900/90 rounded-xl border border-slate-800 p-4 space-y-3 hover:border-slate-700 transition-all">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-white text-base">HCM-KS26-QTKD1</span>
                                <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono text-xs font-semibold">46 SV</span>
                            </div>
                            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700">TP. HCM &bull; QTKD</span>
                        </div>
                        <!-- Subject 1 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-emerald-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-emerald-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-comments text-[11px]"></i> Tiếng Anh Giao tiếp (ENG105)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Huỳnh Thị Kim Khánh</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-extrabold text-rose-400">30.43%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">Ngoại ngữ</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-danger text-[10px]">🚨 Cảnh báo EL</span>
                            </div>
                        </div>
                        <!-- Subject 2 -->
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-purple-500/20 space-y-1.5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="font-semibold text-purple-300 flex items-center gap-1.5">
                                    <i class="fa-solid fa-desktop text-[11px]"></i> Tin học ứng dụng (SSK102)
                                </span>
                                <span class="text-slate-400 font-medium">GV: Lê Hà Thanh Sang</span>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-center text-xs">
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">CC > 10%</span>
                                    <span class="font-bold text-slate-200">8.70%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">BT > 10%</span>
                                    <span class="font-bold text-emerald-400">0.00%</span>
                                </div>
                                <div class="bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                    <span class="text-[10px] text-slate-400 block">Elearning</span>
                                    <span class="font-bold text-slate-200">8.70%</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-[11px] pt-0.5">
                                <span class="text-slate-400">Đại cương</span>
                                <span class="px-2 py-0.5 rounded font-bold badge-warning text-[10px]">🟡 2 SV vắng</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ============================================================= -->
                <!-- VIEW CONTAINER 2: SUBJECT-BY-SUBJECT CLEAN TABLES             -->
                <!-- ============================================================= -->
                <div id="ks26-subject-tables-container" class="hidden space-y-6">
                    <!-- TABLE 1: IT108 -->
                    <div class="ks26-subject-block space-y-2" data-subject="IT108">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                                <i class="fa-solid fa-code"></i> 1. Nhập Môn Công Nghệ Thông Tin (IT108-K26) &bull; 6 Lớp Phụ Trách
                            </span>
                            <span class="text-[11px] text-slate-400">Thời lượng: 22 buổi</span>
                        </div>
                        <div class="overflow-x-auto rounded-xl border border-slate-800">
                            <table class="w-full text-left text-xs lg:text-sm">
                                <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                                    <tr>
                                        <th class="py-2.5 px-4">Tên Lớp</th>
                                        <th class="py-2.5 px-3 text-center">Sĩ số</th>
                                        <th class="py-2.5 px-4">Cơ sở</th>
                                        <th class="py-2.5 px-4">Giảng viên</th>
                                        <th class="py-2.5 px-4 text-center">CC (>10%)</th>
                                        <th class="py-2.5 px-4 text-center">BT (>10%)</th>
                                        <th class="py-2.5 px-4 text-center">Elearning</th>
                                        <th class="py-2.5 px-4 text-center">Trạng thái</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800">
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HN-KS26-CNTT1</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">43</td>
                                        <td class="py-2.5 px-4 text-slate-300">Hà Nội</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Trịnh Quốc Hai</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-slate-200">4.65%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Chuẩn mực</span></td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HN-KS26-CNTT2</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">40</td>
                                        <td class="py-2.5 px-4 text-slate-300">Hà Nội</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Trịnh Quốc Hai</td>
                                        <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                        <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                        <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold bg-slate-800 text-slate-400 border border-slate-700">⏳ Chuẩn bị học</span></td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HN-KS26-CNTT3</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">42</td>
                                        <td class="py-2.5 px-4 text-slate-300">Hà Nội</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Lương Quốc Tuấn</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Xuất sắc (0%)</span></td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HN-KS26-CNTT4</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">27</td>
                                        <td class="py-2.5 px-4 text-slate-300">Hà Nội</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Lương Quốc Tuấn</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-extrabold text-rose-400">22.22%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-danger">🚨 Nhắc EL (6 SV)</span></td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HCM-KS26-CNTT1</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">46</td>
                                        <td class="py-2.5 px-4 text-slate-300">TP. HCM</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Lê Hà Thanh Sang</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-slate-200">6.52%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Nề nếp tốt</span></td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HCM-KS26-CNTT2</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">45</td>
                                        <td class="py-2.5 px-4 text-slate-300">TP. HCM</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Lê Hà Thanh Sang</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-slate-200">8.89%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Ổn định</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- TABLE 2: SKL01 -->
                    <div class="ks26-subject-block space-y-2" data-subject="SKL01">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold text-cyan-300 uppercase tracking-wider flex items-center gap-1.5">
                                <i class="fa-solid fa-users"></i> 2. Kỹ Năng Làm Việc Nhóm (SKL01) &bull; 2 Lớp Phụ Trách
                            </span>
                            <span class="text-[11px] text-slate-400">Kỹ năng mềm</span>
                        </div>
                        <div class="overflow-x-auto rounded-xl border border-slate-800">
                            <table class="w-full text-left text-xs lg:text-sm">
                                <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                                    <tr>
                                        <th class="py-2.5 px-4">Tên Lớp</th>
                                        <th class="py-2.5 px-3 text-center">Sĩ số</th>
                                        <th class="py-2.5 px-4">Cơ sở</th>
                                        <th class="py-2.5 px-4">Giảng viên</th>
                                        <th class="py-2.5 px-4 text-center">CC (>10%)</th>
                                        <th class="py-2.5 px-4 text-center">BT (>10%)</th>
                                        <th class="py-2.5 px-4 text-center">Elearning</th>
                                        <th class="py-2.5 px-4 text-center">Trạng thái</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800">
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HN-KS26-CNTT1</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">43</td>
                                        <td class="py-2.5 px-4 text-slate-300">Hà Nội</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Hoàng Thị Hậu</td>
                                        <td class="py-2.5 px-4 text-center font-semibold text-slate-200">4.65%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-amber-400">16.28%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-warning">🟡 Đôn đốc EL</span></td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HN-KS26-CNTT2</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">40</td>
                                        <td class="py-2.5 px-4 text-slate-300">Hà Nội</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Hoàng Thị Hậu</td>
                                        <td class="py-2.5 px-4 text-center font-semibold text-slate-200">2.50%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">5.00%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Khởi đầu tốt</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- TABLE 3: ENG105 -->
                    <div class="ks26-subject-block space-y-2" data-subject="ENG105">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold text-emerald-300 uppercase tracking-wider flex items-center gap-1.5">
                                <i class="fa-solid fa-comments"></i> 3. Tiếng Anh Giao Tiếp (ENG105-K26) &bull; 4 Lớp Phụ Trách
                            </span>
                            <span class="text-[11px] text-slate-400">Ngoại ngữ</span>
                        </div>
                        <div class="overflow-x-auto rounded-xl border border-slate-800">
                            <table class="w-full text-left text-xs lg:text-sm">
                                <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                                    <tr>
                                        <th class="py-2.5 px-4">Tên Lớp</th>
                                        <th class="py-2.5 px-3 text-center">Sĩ số</th>
                                        <th class="py-2.5 px-4">Cơ sở</th>
                                        <th class="py-2.5 px-4">Giảng viên</th>
                                        <th class="py-2.5 px-4 text-center">CC (>10%)</th>
                                        <th class="py-2.5 px-4 text-center">BT (>10%)</th>
                                        <th class="py-2.5 px-4 text-center">Elearning</th>
                                        <th class="py-2.5 px-4 text-center">Trạng thái</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800">
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HN-KS26-CNTT3</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">42</td>
                                        <td class="py-2.5 px-4 text-slate-300">Hà Nội</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Lò Thị Ngọc Anh</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Hoàn hảo (0%)</span></td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HCM-KS26-CNTT2</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">45</td>
                                        <td class="py-2.5 px-4 text-slate-300">TP. HCM</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Huỳnh Thị Kim Khánh</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-semibold text-amber-400">11.11%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-warning">🟡 Theo dõi EL</span></td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HN-KS26-QTKD3</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">44</td>
                                        <td class="py-2.5 px-4 text-slate-300">Hà Nội</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Nguyễn Hồng Nhung</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Hoàn hảo (0%)</span></td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HCM-KS26-QTKD1</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">46</td>
                                        <td class="py-2.5 px-4 text-slate-300">TP. HCM</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Huỳnh Thị Kim Khánh</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-extrabold text-rose-400">30.43%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-danger">🚨 Cảnh báo EL</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- TABLE 4: SSK103 -->
                    <div class="ks26-subject-block space-y-2" data-subject="SSK103">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
                                <i class="fa-solid fa-chart-line"></i> 4. Tư Duy Phân Tích (SSK103) &bull; 2 Lớp Phụ Trách
                            </span>
                            <span class="text-[11px] text-slate-400">Kỹ năng nền tảng</span>
                        </div>
                        <div class="overflow-x-auto rounded-xl border border-slate-800">
                            <table class="w-full text-left text-xs lg:text-sm">
                                <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                                    <tr>
                                        <th class="py-2.5 px-4">Tên Lớp</th>
                                        <th class="py-2.5 px-3 text-center">Sĩ số</th>
                                        <th class="py-2.5 px-4">Cơ sở</th>
                                        <th class="py-2.5 px-4">Giảng viên</th>
                                        <th class="py-2.5 px-4 text-center">CC (>10%)</th>
                                        <th class="py-2.5 px-4 text-center">BT (>10%)</th>
                                        <th class="py-2.5 px-4 text-center">Elearning</th>
                                        <th class="py-2.5 px-4 text-center">Trạng thái</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800">
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HN-KS26-QTKD1</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">44</td>
                                        <td class="py-2.5 px-4 text-slate-300">Hà Nội</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Nguyễn Ngọc Vân Khanh</td>
                                        <td class="py-2.5 px-4 text-center font-semibold text-slate-200">9.09%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-semibold text-slate-200">6.82%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-warning">🟡 4 SV vắng</span></td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HN-KS26-QTKD2</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">44</td>
                                        <td class="py-2.5 px-4 text-slate-300">Hà Nội</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Nguyễn Ngọc Vân Khanh</td>
                                        <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                        <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                        <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold bg-slate-800 text-slate-400 border border-slate-700">⏳ Chuẩn bị học</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- TABLE 5: SSK102 -->
                    <div class="ks26-subject-block space-y-2" data-subject="SSK102">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold text-purple-300 uppercase tracking-wider flex items-center gap-1.5">
                                <i class="fa-solid fa-desktop"></i> 5. Tin Học Ứng Dụng (SSK102) &bull; 2 Lớp Phụ Trách
                            </span>
                            <span class="text-[11px] text-slate-400">Đại cương tin học</span>
                        </div>
                        <div class="overflow-x-auto rounded-xl border border-slate-800">
                            <table class="w-full text-left text-xs lg:text-sm">
                                <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                                    <tr>
                                        <th class="py-2.5 px-4">Tên Lớp</th>
                                        <th class="py-2.5 px-3 text-center">Sĩ số</th>
                                        <th class="py-2.5 px-4">Cơ sở</th>
                                        <th class="py-2.5 px-4">Giảng viên</th>
                                        <th class="py-2.5 px-4 text-center">CC (>10%)</th>
                                        <th class="py-2.5 px-4 text-center">BT (>10%)</th>
                                        <th class="py-2.5 px-4 text-center">Elearning</th>
                                        <th class="py-2.5 px-4 text-center">Trạng thái</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800">
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HN-KS26-QTKD3</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">44</td>
                                        <td class="py-2.5 px-4 text-slate-300">Hà Nội</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Nguyễn Thị Hồng Minh</td>
                                        <td class="py-2.5 px-4 text-center font-extrabold text-rose-400">18.18%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-semibold text-slate-200">9.09%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-danger">🚨 8 SV vắng</span></td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/40">
                                        <td class="py-2.5 px-4 font-bold text-white">HCM-KS26-QTKD1</td>
                                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">46</td>
                                        <td class="py-2.5 px-4 text-slate-300">TP. HCM</td>
                                        <td class="py-2.5 px-4 text-slate-300 font-medium">Lê Hà Thanh Sang</td>
                                        <td class="py-2.5 px-4 text-center font-semibold text-slate-200">8.70%</td>
                                        <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                        <td class="py-2.5 px-4 text-center font-semibold text-slate-200">8.70%</td>
                                        <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-warning">🟡 2 SV vắng</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- ============================================================= -->
                <!-- VIEW CONTAINER 3: FLAT MATRIX TABLE (KHÔNG GỘP CỘT/ROWSPAN)  -->
                <!-- ============================================================= -->
                <div id="ks26-flat-table-container" class="hidden overflow-x-auto rounded-xl border border-slate-800">
                    <table class="w-full text-left text-xs lg:text-sm">
                        <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800">
                            <tr>
                                <th class="py-3 px-4">Tên Lớp</th>
                                <th class="py-3 px-3 text-center">Sĩ số</th>
                                <th class="py-3 px-3 text-center">Cơ sở</th>
                                <th class="py-3 px-4">Môn Học</th>
                                <th class="py-3 px-4">Giảng viên</th>
                                <th class="py-3 px-4 text-center">CC (>10%)</th>
                                <th class="py-3 px-4 text-center">BT (>10%)</th>
                                <th class="py-3 px-4 text-center">Elearning</th>
                                <th class="py-3 px-4 text-center">Đánh giá & Trạng thái</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800">
                            <!-- HN1 -->
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-bold text-white">HN-KS26-CNTT1</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">43</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HN</td>
                                <td class="py-2.5 px-4 text-indigo-300 font-semibold">Nhập môn CNTT (IT108)</td>
                                <td class="py-2.5 px-4 text-slate-300">Trịnh Quốc Hai</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-slate-200">4.65%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Chuẩn mực</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-slate-900/30">
                                <td class="py-2.5 px-4 font-bold text-slate-400">HN-KS26-CNTT1</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">43</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HN</td>
                                <td class="py-2.5 px-4 text-cyan-300 font-semibold">Làm việc nhóm (SKL01)</td>
                                <td class="py-2.5 px-4 text-slate-300">Hoàng Thị Hậu</td>
                                <td class="py-2.5 px-4 text-center font-semibold text-slate-200">4.65%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-amber-400">16.28%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-warning">🟡 Đôn đốc EL</span></td>
                            </tr>

                            <!-- HN2 -->
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-bold text-white">HN-KS26-CNTT2</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">40</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HN</td>
                                <td class="py-2.5 px-4 text-indigo-300 font-semibold">Nhập môn CNTT (IT108)</td>
                                <td class="py-2.5 px-4 text-slate-300">Trịnh Quốc Hai</td>
                                <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold bg-slate-800 text-slate-400 border border-slate-700">⏳ Chuẩn bị học</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-slate-900/30">
                                <td class="py-2.5 px-4 font-bold text-slate-400">HN-KS26-CNTT2</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">40</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HN</td>
                                <td class="py-2.5 px-4 text-cyan-300 font-semibold">Làm việc nhóm (SKL01)</td>
                                <td class="py-2.5 px-4 text-slate-300">Hoàng Thị Hậu</td>
                                <td class="py-2.5 px-4 text-center font-semibold text-slate-200">2.50%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">5.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Khởi đầu tốt</span></td>
                            </tr>

                            <!-- HN3 -->
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-bold text-white">HN-KS26-CNTT3</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">42</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HN</td>
                                <td class="py-2.5 px-4 text-indigo-300 font-semibold">Nhập môn CNTT (IT108)</td>
                                <td class="py-2.5 px-4 text-slate-300">Lương Quốc Tuấn</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Xuất sắc (0%)</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-slate-900/30">
                                <td class="py-2.5 px-4 font-bold text-slate-400">HN-KS26-CNTT3</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">42</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HN</td>
                                <td class="py-2.5 px-4 text-emerald-300 font-semibold">Tiếng Anh (ENG105)</td>
                                <td class="py-2.5 px-4 text-slate-300">Lò Thị Ngọc Anh</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Hoàn hảo (0%)</span></td>
                            </tr>

                            <!-- HN4 -->
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-bold text-white">HN-KS26-CNTT4</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">27</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HN</td>
                                <td class="py-2.5 px-4 text-indigo-300 font-semibold">Nhập môn CNTT (IT108)</td>
                                <td class="py-2.5 px-4 text-slate-300">Lương Quốc Tuấn</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-extrabold text-rose-400">22.22%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-danger">🚨 Nhắc EL</span></td>
                            </tr>

                            <!-- HCM1 -->
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-bold text-white">HCM-KS26-CNTT1</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">46</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HCM</td>
                                <td class="py-2.5 px-4 text-indigo-300 font-semibold">Nhập môn CNTT (IT108)</td>
                                <td class="py-2.5 px-4 text-slate-300">Lê Hà Thanh Sang</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-slate-200">6.52%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Nề nếp tốt</span></td>
                            </tr>

                            <!-- HCM2 -->
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-bold text-white">HCM-KS26-CNTT2</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">45</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HCM</td>
                                <td class="py-2.5 px-4 text-indigo-300 font-semibold">Nhập môn CNTT (IT108)</td>
                                <td class="py-2.5 px-4 text-slate-300">Lê Hà Thanh Sang</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-slate-200">8.89%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Ổn định</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-slate-900/30">
                                <td class="py-2.5 px-4 font-bold text-slate-400">HCM-KS26-CNTT2</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">45</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HCM</td>
                                <td class="py-2.5 px-4 text-emerald-300 font-semibold">Tiếng Anh (ENG105)</td>
                                <td class="py-2.5 px-4 text-slate-300">Huỳnh Thị Kim Khánh</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-semibold text-amber-400">11.11%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-warning">🟡 Theo dõi EL</span></td>
                            </tr>

                            <!-- QTKD1 -->
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-bold text-white">HN-KS26-QTKD1</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">44</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HN</td>
                                <td class="py-2.5 px-4 text-amber-300 font-semibold">Tư duy phân tích (SSK103)</td>
                                <td class="py-2.5 px-4 text-slate-300">Nguyễn Ngọc Vân Khanh</td>
                                <td class="py-2.5 px-4 text-center font-semibold text-slate-200">9.09%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-semibold text-slate-200">6.82%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-warning">🟡 4 SV vắng</span></td>
                            </tr>

                            <!-- QTKD2 -->
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-bold text-white">HN-KS26-QTKD2</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">44</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HN</td>
                                <td class="py-2.5 px-4 text-amber-300 font-semibold">Tư duy phân tích (SSK103)</td>
                                <td class="py-2.5 px-4 text-slate-300">Nguyễn Ngọc Vân Khanh</td>
                                <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                <td class="py-2.5 px-4 text-center text-slate-500">--</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold bg-slate-800 text-slate-400 border border-slate-700">⏳ Chuẩn bị học</span></td>
                            </tr>

                            <!-- QTKD3 -->
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-bold text-white">HN-KS26-QTKD3</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">44</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HN</td>
                                <td class="py-2.5 px-4 text-emerald-300 font-semibold">Tiếng Anh (ENG105)</td>
                                <td class="py-2.5 px-4 text-slate-300">Nguyễn Hồng Nhung</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-success">🟢 Hoàn hảo (0%)</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-slate-900/30">
                                <td class="py-2.5 px-4 font-bold text-slate-400">HN-KS26-QTKD3</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">44</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HN</td>
                                <td class="py-2.5 px-4 text-purple-300 font-semibold">Tin học ứng dụng (SSK102)</td>
                                <td class="py-2.5 px-4 text-slate-300">Nguyễn Thị Hồng Minh</td>
                                <td class="py-2.5 px-4 text-center font-extrabold text-rose-400">18.18%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-semibold text-slate-200">9.09%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-danger">🚨 8 SV vắng</span></td>
                            </tr>

                            <!-- HCM-QTKD1 -->
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-bold text-white">HCM-KS26-QTKD1</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">46</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HCM</td>
                                <td class="py-2.5 px-4 text-emerald-300 font-semibold">Tiếng Anh (ENG105)</td>
                                <td class="py-2.5 px-4 text-slate-300">Huỳnh Thị Kim Khánh</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-extrabold text-rose-400">30.43%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-danger">🚨 Cảnh báo EL</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-slate-900/30">
                                <td class="py-2.5 px-4 font-bold text-slate-400">HCM-KS26-QTKD1</td>
                                <td class="py-2.5 px-3 text-center font-mono text-slate-300">46</td>
                                <td class="py-2.5 px-3 text-center text-slate-400">HCM</td>
                                <td class="py-2.5 px-4 text-purple-300 font-semibold">Tin học ứng dụng (SSK102)</td>
                                <td class="py-2.5 px-4 text-slate-300">Lê Hà Thanh Sang</td>
                                <td class="py-2.5 px-4 text-center font-semibold text-slate-200">8.70%</td>
                                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center font-semibold text-slate-200">8.70%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded text-xs font-bold badge-warning">🟡 2 SV vắng</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>td class="py-2.5 px-5 text-slate-300 font-medium">Nguyễn Thị Hồng Minh</td>
                                <td class="py-2.5 px-5 text-center font-extrabold text-rose-400">18.18%</td>
                                <td class="py-2.5 px-5 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-5 text-center font-semibold text-slate-200">9.09%</td>
                                <td class="py-2.5 px-5 text-center"><span class="px-2.5 py-1 rounded text-xs font-bold badge-danger">🚨 8 SV vắng</span></td>
                            </tr>

                            <!-- HCM-KS26-QTKD1 -->
                            <tr class="hover:bg-slate-800/40">
                                <td rowspan="2" class="py-3.5 px-5 font-bold text-white border-r border-slate-800/60 align-top">HCM-KS26-QTKD1</td>
                                <td rowspan="2" class="py-3.5 px-5 text-center font-mono text-slate-300 border-r border-slate-800/60 align-top">46</td>
                                <td class="py-2.5 px-5 text-emerald-300 font-semibold">Tiếng Anh Giao tiếp (ENG105)</td>
                                <td class="py-2.5 px-5 text-slate-300 font-medium">Huỳnh Thị Kim Khánh</td>
                                <td class="py-2.5 px-5 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-5 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-5 text-center font-extrabold text-rose-400">30.43%</td>
                                <td class="py-2.5 px-5 text-center"><span class="px-2.5 py-1 rounded text-xs font-bold badge-danger">🚨 Cảnh báo EL</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40 bg-slate-900/30">
                                <td class="py-2.5 px-5 text-purple-300 font-semibold">Tin học ứng dụng (SSK102)</td>
                                <td class="py-2.5 px-5 text-slate-300 font-medium">Lê Hà Thanh Sang</td>
                                <td class="py-2.5 px-5 text-center font-semibold text-slate-200">8.70%</td>
                                <td class="py-2.5 px-5 text-center font-bold text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-5 text-center font-semibold text-slate-200">8.70%</td>
                                <td class="py-2.5 px-5 text-center"><span class="px-2.5 py-1 rounded text-xs font-bold badge-warning">🟡 2 SV vắng</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

        <!-- ========================================================================================= -->
        <!-- TAB 2: KIỂM TOÁN BÁO CÁO NGÀY & HIỆU SUẤT 40H                                             -->
        <!-- ========================================================================================= -->
        <div id="tab-daily-content" class="hidden space-y-8">

            <!-- BANNER GIỚI THIỆU -->
            <div class="glass-panel p-5 rounded-2xl border-l-4 border-rose-500 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 class="text-base lg:text-lg font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-clock text-rose-400"></i> KIỂM TOÁN BÁO CÁO NGÀY WORKLANE & ĐỊNH MỨC 40H/TUẦN (21/09 &ndash; 25/09/2026)
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
            const summaryText = `BÁO CÁO GIAO BAN ĐÀO TẠO TUẦN (21/09 - 25/09/2026) - KÍNH GỬI GIÁM ĐỐC ĐÀO TẠO

1. KHÓA KS24 (Microservices - 181 SV):
- Chỉ số: Chuyên cần vắng 17.57% (▲ +2.89%), Nợ bài tập 10.45% (▲ +2.05%), Elearning vi phạm 13.32%.
- Điểm nóng: HN-K24-CNTT3 vắng 33.33% (▲ +7.69%), nợ bài 17.95%; HN-CNTT1 nợ bài 16.13%, EL 22.58% (kẹt 14 SV đồ án).
- Giải pháp: Tổ chức workshop 90p thông đồ án ngoài giờ; GV điểm danh nghiêm đầu ca và dành 20p cuối ca ký checkpoint đồ án.

2.1. KHÓA KS25 - KHỐI CNTT (FastAPI & PTTKHT - 8 lớp):
- Chỉ số: HN vắng 16.17% (▲ +3.19%), bài tập tốt; HCM vắng 21.53%.
- Điểm nóng: HCM-K25-CNTT7 vắng 34.78% (▲ +2.17%) và Elearning 19.57%.
- Giải pháp: Chấn chỉnh nề nếp chuyên cần và đôn đốc Elearning trước buổi học cho lớp CNTT7; HN chốt điểm danh đầu ca.

2.2. KHÓA KS25 - KHỐI QTKD (MAN107 - 2 lớp):
- Chỉ số: Chuyên cần vắng duy trì rất cao 46.59% sau sáp nhập lớp QTKD3; bài tập nợ 11.36%, EL 19.32%.
- Điểm nóng: HN-K25-QTKD1 vắng kỷ lục 56.52% (tiếp nhận 13 SV từ QTKD3, sĩ số từ 33 lên 46 SV).
- Giải pháp: Lãnh đạo Viện cùng GV họp ổn định sĩ số, tổ chức thuyết trình tình huống bắt buộc có mặt trên lớp.

3. KHÓA KS26 (SSK101 - 396 SV):
- Bảng tổng hợp điều kiện thi: Đủ ĐK trực tiếp: 248 SV | Không đủ ĐK: 126 SV | Cần bảo lãnh tiềm năng: 100 SV.
- Hệ thống LMS Admin (https://lms-admin.rikkei.edu.vn/exam-guarantees) hiện có 9 ĐƠN BẢO LÃNH:
  * Đã duyệt: 4 SV (Phạm Viết Toàn, Nguyễn Thuận Phát, Trần Minh Tiến 2, Nguyễn Ngọc Lan Anh).
  * Chờ duyệt: 5 SV (Hoàng Xuân Nam, Bùi Quang Huy 2, Đặng Quang Anh, Mai Ngọc Đức Hải, Khưu Nhật Tân).
- Phân nhóm 374 SV theo 4 dải: Nợ BTVN [80-100%]: 103 SV (27.5%); Chưa học EL: 151 SV vi phạm >= 20%.

4. BÁO CÁO NGÀY & KIỂM TOÁN HIỆU SUẤT 40H:
- Phòng ban: Khối QTKD đạt chuẩn cao nhất (98.5% giờ, 92.8% KPI Master). Khối CNTT HN (73.9%), Ngoại ngữ (74.3%), CNTT HCM (78.3%), QLCLĐT (40.9%) chưa đạt đủ 40h/NS.
- Nhân sự thiếu 40h (sau loại trừ Leader, Huấn, Đỏ, Nam): 17 NS.
  * Bỏ trống 100%: Nguyễn Huyền Trang (0.0h / 40h, 0/5 ngày).
  * Nhóm thiếu nhiều: Phạm Ngọc Kiên (15h/40h), Phạm Tuấn Bình (24h/40h), Nguyễn Xuân Bách (25.5h/40h), Bùi Thanh Hải (28h/40h), Ngọ Văn Quý (29h/40h).
- Việc chung chung: 32 nhân sự có task ngoài barem (chăm sóc SV không mã lớp, tự nghiên cứu, test LMS chưa nghiệm thu).

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

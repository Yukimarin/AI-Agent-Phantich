import json
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kiểm Toán Hiệu Suất & Giờ Công Worklane - Giám Đốc Đào Tạo</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        slate: {
                            850: '#151e2e',
                            900: '#0f172a',
                            950: '#080c14'
                        },
                        indigo: {
                            600: '#4f46e5',
                            700: '#4338ca'
                        }
                    }
                }
            }
        }
    </script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #080c14;
            color: #e2e8f0;
        }
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #0f172a;
        }
        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #475569;
        }
        .drawer-transition {
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .leader-card-hover:hover {
            border-color: #6366f1;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.15);
        }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen antialiased flex flex-col">

    <!-- Top Navigation Bar -->
    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 sticky top-0 z-20 px-6 py-3.5 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-rose-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/20">
                <i class="fa-solid fa-shield-halved text-lg"></i>
            </div>
            <div>
                <div class="flex items-center space-x-2">
                    <h1 class="text-base font-bold text-white tracking-wide">BÁO CÁO KIỂM TOÁN HIỆU SUẤT & GIỜ CÔNG WORKLANE</h1>
                    <span class="px-2 py-0.5 text-xs font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/30 rounded-full">Bảo mật</span>
                </div>
                <p class="text-xs text-slate-400">Kính gửi: <span class="text-indigo-300 font-medium">Thầy Nguyễn Duy Quang - Giám đốc Trung tâm Đào tạo Công nghệ & Kinh tế số</span></p>
            </div>
        </div>

        <div class="flex items-center space-x-3 text-xs">
            <!-- Period Switcher Buttons -->
            <div class="flex items-center bg-slate-800/90 p-1 rounded-xl border border-slate-700/80 shadow-inner">
                <button id="btnPeriodSept" onclick="switchPeriod('sept_01_08')" class="px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center space-x-1.5 bg-indigo-600 text-white shadow-sm">
                    <i class="fa-solid fa-bolt text-amber-300"></i>
                    <span>Kỳ 01/09 - 08/09/2026 (Mới)</span>
                </button>
                <button id="btnPeriodAug" onclick="switchPeriod('august')" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition flex items-center space-x-1.5">
                    <i class="fa-regular fa-calendar text-slate-400"></i>
                    <span>Tháng 08/2026 (Lịch sử)</span>
                </button>
            </div>

            <div class="bg-slate-800/80 border border-slate-700/80 rounded-lg px-3 py-1.5 flex items-center space-x-2 text-slate-300">
                <i class="fa-regular fa-calendar text-indigo-400"></i>
                <span id="lblPeriodDates">Kỳ 01/09 - 08/09/2026 (4 ngày làm việc)</span>
            </div>
            <button onclick="window.print()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg border border-slate-700 transition flex items-center space-x-1.5">
                <i class="fa-solid fa-print"></i>
                <span>In Báo Cáo</span>
            </button>
            <a id="btnMarkdownReport" href="../../docs/reports/2026-09-09-kiem-toan-worklane-01-08-thang-9-theo-kpi-master-moi.md" target="_blank" class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition font-medium shadow-sm flex items-center space-x-1.5">
                <i class="fa-regular fa-file-lines"></i>
                <span>Báo Cáo Markdown</span>
            </a>
        </div>
    </header>

    <!-- Main Container (Single-Pane of Glass) -->
    <main class="flex-1 p-6 max-w-[1600px] w-full mx-auto space-y-5">

        <!-- Banner thông báo Barem chuẩn hóa -->
        <div class="bg-gradient-to-r from-indigo-950/80 via-slate-900 to-slate-900 border border-indigo-500/30 rounded-2xl px-5 py-3 flex flex-wrap items-center justify-between gap-3 text-xs shadow-sm">
            <div class="flex items-center space-x-2.5">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span class="font-bold text-slate-200">ĐÃ ÁP DỤNG BỘ 3 KPI MASTER CHUẨN HÓA MỚI NHẤT:</span>
            </div>
            <div class="flex flex-wrap items-center gap-2">
                <span class="px-2.5 py-1 bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 rounded-lg font-medium">
                    <i class="fa-solid fa-laptop-code mr-1"></i> CNTT: Bản FINAL (249 định mức • 18 Review)
                </span>
                <span class="px-2.5 py-1 bg-amber-500/20 text-amber-300 border border-amber-500/40 rounded-lg font-medium">
                    <i class="fa-solid fa-chart-line mr-1"></i> QTKD: Bản Draft 8/2026 (124 định mức)
                </span>
                <span class="px-2.5 py-1 bg-teal-500/20 text-teal-300 border border-teal-500/40 rounded-lg font-medium">
                    <i class="fa-solid fa-language mr-1"></i> Ngoại Ngữ: Bản Master 09/09 (118 định mức • 270 Mappings)
                </span>
            </div>
        </div>

        <!-- 1. Cố định: Overview Toàn Trung tâm (Trung tâm Đào tạo Công nghệ & Kinh tế số - 41 NS) -->
        <div class="bg-slate-900/60 border border-slate-800/90 rounded-2xl p-5 shadow-sm space-y-3">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                    <span class="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
                    <h2 class="text-xs font-bold uppercase tracking-wider text-slate-300">Tổng Quan Toàn Trung Tâm Đào Tạo Công Nghệ & Kinh Tế Số</h2>
                    <span class="px-2 py-0.5 text-[11px] font-semibold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 rounded-md">6 Khối • 3 Cơ sở • 41 Nhân sự</span>
                </div>
                <span id="lblOverviewSubtitle" class="text-[11px] text-slate-500">Dữ liệu kiểm toán chuẩn hóa theo bộ 3 KPI Master mới</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <!-- Card 1: Tuân thủ -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 relative overflow-hidden">
                    <div class="absolute -right-2 -bottom-2 w-16 h-16 bg-emerald-500/10 rounded-full blur-xl"></div>
                    <div class="flex items-center justify-between text-slate-400 text-xs mb-1">
                        <span>TUÂN THỦ BÁO CÁO NGÀY</span>
                        <i class="fa-solid fa-clipboard-check text-emerald-400"></i>
                    </div>
                    <div class="flex items-baseline space-x-2">
                        <span id="valComplianceRate" class="text-2xl font-bold text-white">86.0%</span>
                        <span class="text-xs text-slate-400">(41 NS)</span>
                    </div>
                    <div class="text-[11px] text-slate-400 mt-2 flex items-center space-x-1">
                        <i class="fa-solid fa-circle-check text-emerald-400"></i>
                        <span id="valHoursRatio">Khai báo: 1067.9h / Chuẩn: 604.0h</span>
                    </div>
                </div>

                <!-- Card 2: Dôi dư -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 relative overflow-hidden">
                    <div class="absolute -right-2 -bottom-2 w-16 h-16 bg-rose-500/10 rounded-full blur-xl"></div>
                    <div class="flex items-center justify-between text-slate-400 text-xs mb-1">
                        <span>TỔNG GIỜ DÔI DƯ NGHI VẤN</span>
                        <i class="fa-solid fa-clock-rotate-left text-rose-400"></i>
                    </div>
                    <div class="flex items-baseline space-x-2">
                        <span id="valExcessHours" class="text-2xl font-bold text-rose-400">+468.4h</span>
                        <span class="text-xs text-slate-400">so barem Master</span>
                    </div>
                    <div class="text-[11px] text-rose-300 mt-2 flex items-center space-x-1">
                        <i class="fa-solid fa-triangle-exclamation text-rose-400"></i>
                        <span>Cần nghiệm thu giờ thực chất & định mức</span>
                    </div>
                </div>

                <!-- Card 3: Hạ Rank -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 relative overflow-hidden">
                    <div class="absolute -right-2 -bottom-2 w-16 h-16 bg-amber-500/10 rounded-full blur-xl"></div>
                    <div class="flex items-center justify-between text-slate-400 text-xs mb-1">
                        <span>DIỆN XEM XÉT HẠ RANK</span>
                        <i class="fa-solid fa-user-gear text-amber-400"></i>
                    </div>
                    <div class="flex items-baseline space-x-2">
                        <span id="valReviewRank" class="text-2xl font-bold text-amber-400">15 NS</span>
                        <span class="text-xs text-slate-400">vượt 1.5x - 3x định mức</span>
                    </div>
                    <div class="text-[11px] text-amber-300 mt-2 flex items-center space-x-1">
                        <i class="fa-solid fa-triangle-exclamation text-amber-400"></i>
                        <span>Chậm tiến độ nghiệp vụ cốt lõi</span>
                    </div>
                </div>

                <!-- Card 4: Cắt Giờ Ảo -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 relative overflow-hidden">
                    <div class="absolute -right-2 -bottom-2 w-16 h-16 bg-indigo-500/10 rounded-full blur-xl"></div>
                    <div class="flex items-center justify-between text-slate-400 text-xs mb-1">
                        <span>DIỆN CẮT GIỜ CÔNG ẢO</span>
                        <i class="fa-solid fa-scissors text-indigo-400"></i>
                    </div>
                    <div class="flex items-baseline space-x-2">
                        <span id="valDeductHours" class="text-2xl font-bold text-indigo-400">22 NS</span>
                        <span class="text-xs text-slate-400">khai bù giờ/tự do</span>
                    </div>
                    <div class="text-[11px] text-indigo-300 mt-2 flex items-center space-x-1">
                        <i class="fa-solid fa-filter text-indigo-400"></i>
                        <span>Chỉ nghiệm thu theo barem chuẩn</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. KHỐI BIỂU ĐỒ SO SÁNH TIẾN ĐỘ THÁNG 8 VS THÁNG 9 (CHART.JS SAAS VISUALIZATION) -->
        <div class="bg-slate-900/70 border border-slate-800/90 rounded-2xl p-5 shadow-lg space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-3">
                <div class="flex items-center space-x-2.5">
                    <div class="w-8 h-8 rounded-lg bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center text-indigo-400">
                        <i class="fa-solid fa-chart-column text-sm"></i>
                    </div>
                    <div>
                        <h3 class="text-xs font-bold uppercase tracking-wider text-slate-200">
                            Phân Tích So Sánh Tiến Độ Hiệu Suất (Tháng 08/2026 vs Kỳ 01/09 - 08/09/2026)
                        </h3>
                        <p class="text-[11px] text-slate-400">Chuẩn hóa theo Tỷ lệ vênh (%) và Giờ dôi dư trung bình/ngày/nhân sự trên 6 Khối đào tạo</p>
                    </div>
                </div>
                <!-- 3 Quick Insight Badges -->
                <div class="flex flex-wrap items-center gap-2 text-[11px]">
                    <span class="px-2.5 py-1 bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 rounded-lg flex items-center gap-1 font-semibold">
                        <i class="fa-solid fa-arrow-trend-down text-emerald-400"></i> Ngoại Ngữ: Dôi dư TB chỉ 0.62h/ngày (Thấp nhất viện)
                    </span>
                    <span class="px-2.5 py-1 bg-blue-500/15 text-blue-300 border border-blue-500/30 rounded-lg flex items-center gap-1 font-semibold">
                        <i class="fa-solid fa-arrow-down-long text-blue-400"></i> CNTT HCM: Giảm vênh 58.4% (Từ 2.80h ➔ 1.51h/ngày)
                    </span>
                    <span class="px-2.5 py-1 bg-rose-500/15 text-rose-300 border border-rose-500/30 rounded-lg flex items-center gap-1 font-semibold">
                        <i class="fa-solid fa-arrow-trend-up text-rose-400"></i> CNTT HN: Dôi dư 4.51h/ngày (Cần cắt giờ ảo)
                    </span>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 pt-2">
                <!-- Biểu đồ 1: Tỷ lệ vênh % -->
                <div class="bg-slate-850 p-4 rounded-xl border border-slate-800 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-slate-200 flex items-center gap-2">
                            <span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
                            Tỷ Lệ Vênh Giờ So Với Barem Master (%)
                        </span>
                        <div class="flex items-center space-x-3 text-[11px] text-slate-400 font-medium">
                            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded bg-indigo-500"></span> Tháng 8</span>
                            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded bg-amber-400"></span> Tháng 9</span>
                        </div>
                    </div>
                    <div class="relative h-64 w-full">
                        <canvas id="chartExcessPct"></canvas>
                    </div>
                </div>

                <!-- Biểu đồ 2: Giờ dôi dư TB/ngày/nhân sự -->
                <div class="bg-slate-850 p-4 rounded-xl border border-slate-800 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-slate-200 flex items-center gap-2">
                            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                            Giờ Dôi Dư Trung Bình / Ngày / Nhân Sự (h/ngày/NS)
                        </span>
                        <div class="flex items-center space-x-3 text-[11px] text-slate-400 font-medium">
                            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded bg-slate-600"></span> Tháng 8</span>
                            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded bg-emerald-400"></span> Tháng 9</span>
                        </div>
                    </div>
                    <div class="relative h-64 w-full">
                        <canvas id="chartDailyRate"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- 3. Bộ Lọc Điều Khiển (Campus, Khối, Phân Loại, Tìm kiếm) -->
        <div class="bg-slate-900/60 border border-slate-800/90 rounded-2xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
            <div class="flex flex-wrap items-center gap-3">
                <!-- Lọc Cơ sở -->
                <div class="flex items-center space-x-2 text-xs">
                    <label class="text-slate-400 font-medium"><i class="fa-solid fa-building text-slate-500 mr-1"></i>Cơ sở:</label>
                    <select id="campusFilter" onchange="filterTable()" class="bg-slate-800 border border-slate-700 text-slate-200 rounded-lg px-3 py-1.5 text-xs focus:ring-1 focus:ring-indigo-500 focus:outline-none">
                        <option value="ALL">Tất cả Cơ sở (3 Cơ sở)</option>
                        <option value="Cơ sở Hà Nội - Ngọc Trục">Cơ sở Hà Nội - Ngọc Trục</option>
                        <option value="Cơ sở Hà Nội - HPC">Cơ sở Hà Nội - HPC</option>
                        <option value="Cơ sở Hồ Chí Minh">Cơ sở Hồ Chí Minh</option>
                    </select>
                </div>

                <!-- Lọc Khối Đào Tạo -->
                <div class="flex items-center space-x-2 text-xs">
                    <label class="text-slate-400 font-medium"><i class="fa-solid fa-layer-group text-slate-500 mr-1"></i>Khối Đào Tạo:</label>
                    <select id="groupFilter" onchange="filterTable()" class="bg-slate-800 border border-slate-700 text-slate-200 rounded-lg px-3 py-1.5 text-xs focus:ring-1 focus:ring-indigo-500 focus:outline-none">
                        <option value="ALL">Tất cả các Khối (6 Khối)</option>
                        <option value="Khối CNTT Hà Nội">Khối CNTT Hà Nội (13 NS - Leader Hồ Xuân Hùng)</option>
                        <option value="Khối Quản trị Kinh doanh">Khối Quản trị Kinh doanh (9 NS - Leader Hoàng Thị Kim Oanh)</option>
                        <option value="Khối Ngoại ngữ và KNM">Khối Ngoại ngữ và KNM (4 NS - Leader Giáp Thị Minh Hằng)</option>
                        <option value="Khối QLCLĐT Hà Nội">Khối QLCLĐT Hà Nội (4 NS - Leader Nguyễn Thị Tươi)</option>
                        <option value="Khối CNTT HCM">Khối CNTT HCM (9 NS - Leader Nguyễn Bá Minh Đạo)</option>
                        <option value="LMS AI">LMS AI (2 NS - Leader Trần Minh Cường)</option>
                    </select>
                </div>

                <!-- Lọc Phân Loại Đề Xuất -->
                <div class="flex items-center space-x-2 text-xs">
                    <label class="text-slate-400 font-medium"><i class="fa-solid fa-tag text-slate-500 mr-1"></i>Đề xuất:</label>
                    <select id="categoryFilter" onchange="filterTable()" class="bg-slate-800 border border-slate-700 text-slate-200 rounded-lg px-3 py-1.5 text-xs focus:ring-1 focus:ring-indigo-500 focus:outline-none">
                        <option value="ALL">Tất cả phân loại</option>
                        <option value="CẦN RÀ SOÁT RANK">Cần rà soát hạ Rank</option>
                        <option value="CẢNH BÁO BÙ GIỜ">Cắt giảm giờ công ảo / Khai bù</option>
                        <option value="CHƯA NỘP BÁO CÁO">Chưa nộp báo cáo (0%)</option>
                        <option value="CHUẨN MỰC">Khai báo chuẩn mực</option>
                    </select>
                </div>
            </div>

            <!-- Tìm Kiếm Tức Thì -->
            <div class="relative w-full sm:w-64 text-xs">
                <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-500"></i>
                <input id="searchInput" type="text" oninput="filterTable()" placeholder="Tìm tên nhân sự, vai trò..." class="w-full bg-slate-800 border border-slate-700 text-slate-200 rounded-lg pl-8 pr-3 py-1.5 text-xs focus:ring-1 focus:ring-indigo-500 focus:outline-none placeholder-slate-500">
            </div>
        </div>

        <!-- 4. Dynamic Leader Accountability Container -->
        <div id="leaderAccountabilityContainer"></div>

        <!-- 5. Danh Sách Nhân Sự Chi Tiết (Staff Master Table) -->
        <div class="bg-slate-900 border border-slate-800/90 rounded-2xl shadow-sm overflow-hidden space-y-0">
            <div class="p-4 bg-slate-850 border-b border-slate-800 flex items-center justify-between">
                <div class="flex items-center space-x-2">
                    <i class="fa-solid fa-table-list text-indigo-400"></i>
                    <h3 id="tableTitle" class="text-xs font-bold uppercase tracking-wider text-slate-200">
                        Danh sách nhân sự trực thuộc khối đào tạo
                    </h3>
                </div>
                <div class="text-xs text-slate-400">
                    Hiển thị <span id="displayedCount" class="font-bold text-white">41</span> nhân sự
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs text-slate-300">
                    <thead class="bg-slate-950/80 text-slate-400 font-semibold border-b border-slate-800 uppercase tracking-wider text-[10px]">
                        <tr>
                            <th class="py-3 px-4 min-w-[200px]">Họ và Tên</th>
                            <th class="py-3 px-3">Vai Trò & Rank</th>
                            <th class="py-3 px-3">Khối / Cơ Sở</th>
                            <th class="py-3 px-3 text-center">Báo Cáo Ngày</th>
                            <th class="py-3 px-3 text-right">Giờ Khai</th>
                            <th class="py-3 px-3 text-right">Chuẩn KPI</th>
                            <th class="py-3 px-3 text-right">Dôi Dư</th>
                            <th class="py-3 px-4">Đề Xuất Kiểm Toán</th>
                            <th class="py-3 px-3 text-center">Thao Tác</th>
                        </tr>
                    </thead>
                    <tbody id="staffTableBody" class="divide-y divide-slate-800/60 font-normal">
                        <!-- Rendered via JavaScript -->
                    </tbody>
                </table>
            </div>
        </div>

    </main>

    <!-- 6. Slide-Over Offcanvas Drawer -->
    <div id="drawerBackdrop" onclick="closeDrawer()" class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-40 opacity-0 pointer-events-none transition-opacity duration-200"></div>

    <aside id="staffDrawer" class="fixed top-0 right-0 h-full w-full max-w-2xl bg-slate-900 border-l border-slate-800 z-50 transform translate-x-full drawer-transition shadow-2xl flex flex-col">
        <!-- Header Drawer -->
        <div class="p-5 bg-slate-850 border-b border-slate-800 flex items-start justify-between">
            <div class="flex items-center space-x-3.5">
                <div id="drawerAvatar" class="w-12 h-12 rounded-xl bg-indigo-600/30 border border-indigo-500/50 flex items-center justify-center text-indigo-300 font-black text-lg">
                    NV
                </div>
                <div class="space-y-1">
                    <div class="flex flex-wrap items-center gap-2">
                        <h3 id="drawerStaffName" class="text-base font-bold text-white tracking-tight">Nguyễn Văn A</h3>
                        <span id="drawerStaffRank" class="px-2 py-0.5 text-[11px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded-full">Rank 3</span>
                    </div>
                    <p id="drawerStaffGroup" class="text-xs text-slate-400">Khối CNTT Hà Nội • Cơ sở Hà Nội - HPC</p>
                    <p id="drawerStaffLeader" class="text-[11px] text-slate-500"><i class="fa-solid fa-user-tie mr-1"></i>Leader: Hồ Xuân Hùng</p>
                </div>
            </div>
            <button onclick="closeDrawer()" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>

        <!-- 3 Thẻ Metric Nhanh Trong Drawer -->
        <div class="p-5 bg-slate-900/50 border-b border-slate-800 grid grid-cols-3 gap-3 text-center">
            <div class="bg-slate-850 p-2.5 rounded-xl border border-slate-800">
                <span class="text-[10px] text-slate-400 uppercase block font-medium">Báo cáo ngày</span>
                <span id="drawerCompliance" class="text-base font-bold text-emerald-400">100%</span>
                <span id="drawerReportDays" class="text-[10px] text-slate-500 block">4/4 ngày</span>
            </div>
            <div class="bg-slate-850 p-2.5 rounded-xl border border-slate-800">
                <span class="text-[10px] text-slate-400 uppercase block font-medium">Khai / Chuẩn</span>
                <span id="drawerHoursRatio" class="text-base font-bold text-white">32h / 20h</span>
                <span class="text-[10px] text-slate-500 block">KPI Master</span>
            </div>
            <div class="bg-slate-850 p-2.5 rounded-xl border border-slate-800">
                <span class="text-[10px] text-slate-400 uppercase block font-medium">Dôi dư giờ</span>
                <span id="drawerExcessHours" class="text-base font-bold text-rose-400">+12.0h</span>
                <span class="text-[10px] text-rose-300 block">Nghi vấn</span>
            </div>
        </div>

        <!-- Banner Đề Xuất Xử Lý Cụ Thể Của Leader -->
        <div class="p-4 bg-slate-850/80 border-b border-slate-800">
            <div class="flex items-start space-x-2.5">
                <i class="fa-solid fa-gavel text-amber-400 mt-0.5"></i>
                <div class="text-xs space-y-1">
                    <span id="drawerRecCategory" class="font-bold text-amber-300 uppercase tracking-wide">CẦN RÀ SOÁT RANK</span>
                    <p id="drawerActionNote" class="text-slate-300 leading-relaxed"></p>
                </div>
            </div>
        </div>

        <!-- Drawer Tabs Navigation -->
        <div class="px-5 pt-3 bg-slate-900 border-b border-slate-800 flex items-center space-x-2 text-xs">
            <button id="btnTabExcess" onclick="switchDrawerTab('tabExcess')" class="px-3 py-1.5 rounded-lg bg-indigo-600 text-white transition flex items-center space-x-1.5 shadow-sm font-medium">
                <i class="fa-solid fa-clock-rotate-left"></i>
                <span>Task Vượt Chuẩn (<span id="drawerExcessCount">0</span>)</span>
            </button>
            <button id="btnTabFree" onclick="switchDrawerTab('tabFree')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-750 text-slate-300 transition flex items-center space-x-1.5 font-medium">
                <i class="fa-solid fa-scissors"></i>
                <span>Task Ngoài Barem (<span id="drawerFreeCount">0</span>)</span>
            </button>
            <button id="btnTabUnverified" onclick="switchDrawerTab('tabUnverified')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-750 text-slate-300 transition flex items-center space-x-1.5 font-medium">
                <i class="fa-solid fa-ticket"></i>
                <span>Vênh Ticket (<span id="drawerUnverifiedCount">0</span>)</span>
            </button>
            <button id="btnTabAllLogs" onclick="switchDrawerTab('tabAllLogs')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-750 text-slate-300 transition flex items-center space-x-1.5 font-medium">
                <i class="fa-regular fa-calendar-days"></i>
                <span>Nhật Ký Đầy Đủ</span>
            </button>
        </div>

        <!-- Tab Panels Content -->
        <div class="p-5 flex-1 overflow-y-auto space-y-3 text-xs">
            <div id="panelTabExcess" class="space-y-2"></div>
            <div id="panelTabFree" class="space-y-2 hidden"></div>
            <div id="panelTabUnverified" class="space-y-2 hidden"></div>
            <div id="panelTabAllLogs" class="space-y-2 hidden"></div>
        </div>

        <!-- Drawer Footer (Nút hành động) -->
        <div class="p-4 bg-slate-850 border-t border-slate-800 flex items-center justify-between gap-3">
            <button onclick="copyStaffAuditReport()" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition flex items-center space-x-1.5 shadow-sm">
                <i class="fa-regular fa-copy"></i>
                <span>Sao Chép Phiếu Làm Việc 1-1</span>
            </button>
            <button onclick="markReviewed()" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs transition border border-slate-700">
                <i class="fa-solid fa-check mr-1"></i> Xác Nhận Đã Đọc
            </button>
        </div>
    </aside>

    <!-- Embedded Data & Interactive JavaScript -->
    <script>
        const auditData = __JSON_EMBEDDED__;
        const comparisonData = __COMPARISON_JSON__;

        let currentPeriod = "sept_01_08";
        let currentData = (auditData.periods && auditData.periods[currentPeriod]) ? auditData.periods[currentPeriod] : auditData;
        let staffList = Object.values(currentData.staff_details || {});
        let currentSelectedStaff = null;
        let activeTab = "tabExcess";

        const LEADER_DIRECTORY_BASE = {
            "Khối CNTT Hà Nội": {
                name: "Hồ Xuân Hùng",
                role: "Leader Khối CNTT Hà Nội",
                rank: 5,
                groupKey: "Khối CNTT Hà Nội",
                campuses: "HN - Ngọc Trục (6 NS) & HN - HPC (6 NS)",
                totalSubs: 12
            },
            "Khối Quản trị Kinh doanh": {
                name: "Hoàng Thị Kim Oanh",
                role: "Leader Khối Quản trị Kinh doanh",
                rank: 5,
                groupKey: "Khối Quản trị Kinh doanh",
                campuses: "Hà Nội - Ngọc Trục (6 NS) & TP. Hồ Chí Minh (2 NS)",
                totalSubs: 8
            },
            "Khối Ngoại ngữ và KNM": {
                name: "Giáp Thị Minh Hằng",
                role: "Leader Khối Ngoại ngữ & KNM",
                rank: 5,
                groupKey: "Khối Ngoại ngữ và KNM",
                campuses: "Cơ sở Hà Nội - HPC",
                totalSubs: 3
            },
            "Khối QLCLĐT Hà Nội": {
                name: "Nguyễn Thị Tươi",
                role: "Leader Khối QLCLĐT Hà Nội",
                rank: 4,
                groupKey: "Khối QLCLĐT Hà Nội",
                campuses: "Hà Nội - HPC (2 NS) & TP. Hồ Chí Minh (1 NS)",
                totalSubs: 3
            },
            "Khối CNTT HCM": {
                name: "Nguyễn Bá Minh Đạo",
                role: "Leader Khối CNTT HCM",
                rank: 5,
                groupKey: "Khối CNTT HCM",
                campuses: "Cơ sở TP. Hồ Chí Minh (8 NS)",
                totalSubs: 8
            },
            "LMS AI": {
                name: "Trần Minh Cường",
                role: "Leader Nhóm Dự án LMS AI",
                rank: 5,
                groupKey: "LMS AI",
                campuses: "Hà Nội - HPC (1 NS) & TP. Hồ Chí Minh (1 NS)",
                totalSubs: 2
            }
        };

        function switchPeriod(periodKey) {
            currentPeriod = periodKey;
            if (auditData.periods && auditData.periods[periodKey]) {
                currentData = auditData.periods[periodKey];
            } else {
                currentData = auditData;
            }
            staffList = Object.values(currentData.staff_details || {});

            const btnSept = document.getElementById("btnPeriodSept");
            const btnAug = document.getElementById("btnPeriodAug");
            const lblDates = document.getElementById("lblPeriodDates");
            const btnMd = document.getElementById("btnMarkdownReport");

            if (periodKey === 'sept_01_08') {
                btnSept.className = "px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center space-x-1.5 bg-indigo-600 text-white shadow-sm";
                btnAug.className = "px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition flex items-center space-x-1.5";
                lblDates.textContent = "Kỳ 01/09 - 08/09/2026 (4 ngày làm việc)";
                btnMd.href = "../../docs/reports/2026-09-09-kiem-toan-worklane-01-08-thang-9-theo-kpi-master-moi.md";
            } else {
                btnAug.className = "px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center space-x-1.5 bg-indigo-600 text-white shadow-sm";
                btnSept.className = "px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition flex items-center space-x-1.5";
                lblDates.textContent = "Tháng 08/2026 (20 ngày làm việc)";
                btnMd.href = "../../docs/reports/2026-09-04-kiem-toan-hieu-suat-va-khai-bao-worklane.md";
            }

            const s = currentData.summary || {};
            document.getElementById("valComplianceRate").textContent = (s.overall_compliance_rate || 0) + "%";
            document.getElementById("valHoursRatio").textContent = `Khai báo: ${s.total_declared_hours || 0}h / Chuẩn: ${s.total_standard_hours || 0}h`;
            document.getElementById("valExcessHours").textContent = "+" + (s.total_excess_hours || 0) + "h";
            document.getElementById("valReviewRank").textContent = (s.count_review_rank || 0) + " NS";
            document.getElementById("valDeductHours").textContent = (s.count_deduct_hours || 0) + " NS";

            filterTable();
        }

        function getLeaderSubordinates(leaderName, groupKey) {
            return staffList.filter(s => {
                const isUnderLeader = s.campus_leader && s.campus_leader.includes(leaderName);
                const notLeader = s.name !== leaderName;
                return isUnderLeader && notLeader;
            });
        }

        function getDynamicLeaderInfo(groupKey) {
            const base = LEADER_DIRECTORY_BASE[groupKey];
            if (!base) return null;
            const leaderStaff = staffList.find(s => s.name === base.name);
            const subs = getLeaderSubordinates(base.name, base.groupKey);
            const excessHoursTotal = Math.round(subs.reduce((acc, s) => acc + s.excess_hours, 0) * 10) / 10;
            const reviewRankStaff = subs.filter(s => s.recommendation_category === "CẦN RÀ SOÁT RANK");
            const deductHoursStaff = subs.filter(s => s.recommendation_category === "CẢNH BÁO BÙ GIỜ");

            let compliance = 0.0;
            let reportedDays = "0 ngày";
            if (leaderStaff) {
                compliance = leaderStaff.compliance_rate;
                reportedDays = `${leaderStaff.reported_days}/${leaderStaff.expected_days} ngày`;
            }

            let statusBadge = "🔴 Chưa làm gương (0%)";
            let statusClass = "bg-red-500/20 text-red-300 border-red-500/40";
            if (compliance >= 100) {
                statusBadge = `🟢 Làm gương xuất sắc (${reportedDays})`;
                statusClass = "bg-emerald-500/20 text-emerald-300 border-emerald-500/40";
            } else if (compliance >= 70) {
                statusBadge = `🟡 Đạt (${reportedDays})`;
                statusClass = "bg-amber-500/20 text-amber-300 border-amber-500/40";
            } else if (compliance > 0) {
                statusBadge = `🟠 Chưa đều (${reportedDays})`;
                statusClass = "bg-orange-500/20 text-orange-300 border-orange-500/40";
            }

            let leaderReview = "";
            let actionForDirector = "";

            if (base.name === "Hồ Xuân Hùng") {
                leaderReview = compliance === 0 
                    ? "Leader chưa nộp báo cáo ngày trên Worklane trong kỳ này, cần tăng cường làm gương kỷ luật tác nghiệp cho 12 nhân sự trực thuộc." 
                    : `Leader đạt ${compliance}% báo cáo ngày, cần chỉ đạo sát sao việc chuyển đổi sang 18 loại Review theo Barem FINAL.`;
                actionForDirector = "Giám đốc Đào tạo cần nhắc nhở trực tiếp và yêu cầu Leader cắt bỏ các task tự soạn slide của 9 nhân sự rà soát Rank.";
            } else if (base.name === "Giáp Thị Minh Hằng") {
                leaderReview = `Leader làm gương chuẩn mực (${compliance}%), bám sát điều hành dự án tiếng Anh & tiếng Nhật theo Barem 118 định mức mới.`;
                actionForDirector = "Phổ biến Barem Ngoại ngữ 118 định mức cho cô Lò Thị Ngọc Anh và cô Lê Thị Đỏ để chuẩn hóa thời lượng thẩm định đề thi.";
            } else if (base.name === "Hoàng Thị Kim Oanh") {
                leaderReview = `Kỷ luật tuyệt đối (${compliance}%), 100% nhân sự trực thuộc nộp đầy đủ báo cáo ngày môn MAN107.`;
                actionForDirector = "Rà soát các task nghiên cứu tự do của nhân sự để chuyển thành sản phẩm nghiệm thu rõ ràng.";
            } else if (base.name === "Nguyễn Bá Minh Đạo") {
                leaderReview = `Khai báo đúng khối lượng giảng dạy thực tế, tỷ lệ vênh thấp nhất toàn viện (+37.4%).`;
                actionForDirector = "Biểu dương tinh thần tác nghiệp kỷ luật và sát thực tế của đội ngũ CNTT TP. Hồ Chí Minh.";
            } else if (base.name === "Nguyễn Thị Tươi") {
                leaderReview = `Leader đạt ${compliance}%, quản lý 3 nhân sự giáo vụ và kiểm toán chất lượng.`;
                actionForDirector = "Chuẩn hóa định mức công việc giáo vụ và giám sát lớp học.";
            } else {
                leaderReview = `Leader tập trung R&D LMS AI. Cần hoàn thiện barem định mức riêng cho khối công nghệ AI.`;
                actionForDirector = "Ban hành barem định mức riêng cho các đầu việc lập trình và tích hợp LMS AI.";
            }

            return {
                ...base,
                compliance,
                reportedDays,
                statusBadge,
                statusClass,
                leaderReview,
                actionForDirector,
                subs,
                excessHoursTotal,
                reviewRankStaff,
                deductHoursStaff
            };
        }

        function renderLeaderAccountability(selectedGroup, selectedCampus) {
            const container = document.getElementById("leaderAccountabilityContainer");
            container.innerHTML = "";

            if (selectedGroup !== "ALL" && LEADER_DIRECTORY_BASE[selectedGroup]) {
                const l = getDynamicLeaderInfo(selectedGroup);
                const rankReviewTags = l.reviewRankStaff.map(s => `
                    <button onclick="openDrawerByName('${s.name}')" title="${s.name} - Rank ${s.rank}" class="inline-flex items-center gap-1.5 max-w-full truncate px-2.5 py-1 rounded-lg bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/30 text-xs font-semibold transition shadow-sm">
                        <i class="fa-solid fa-user-gear text-[10px] flex-shrink-0"></i> 
                        <span class="truncate">${s.name} (R${s.rank})</span>
                    </button>
                `).join('') || '<span class="text-xs text-slate-500 italic">Không có nhân sự nào</span>';

                const deductTags = l.deductHoursStaff.map(s => `
                    <button onclick="openDrawerByName('${s.name}')" title="${s.name} - Dôi dư +${s.excess_hours}h" class="inline-flex items-center gap-1.5 max-w-full truncate px-2.5 py-1 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/30 text-xs font-semibold transition shadow-sm">
                        <i class="fa-solid fa-scissors text-[10px] flex-shrink-0"></i> 
                        <span class="truncate">${s.name} (+${s.excess_hours}h)</span>
                    </button>
                `).join('') || '<span class="text-xs text-slate-500 italic">Không có nhân sự nào</span>';

                const leaderPills = Object.keys(LEADER_DIRECTORY_BASE).map(g => {
                    const item = LEADER_DIRECTORY_BASE[g];
                    const isCurrent = g === selectedGroup;
                    const pillClass = isCurrent 
                        ? "bg-indigo-600 text-white font-bold border-indigo-500 shadow-sm" 
                        : "bg-slate-800 hover:bg-slate-700 text-slate-300 border-slate-700";
                    return `<button onclick="selectGroupFilter('${g}')" class="px-2.5 py-1 rounded-lg text-xs border transition flex items-center gap-1 ${pillClass}">
                        <span>${item.name}</span>
                        <span class="text-[10px] opacity-80">(${item.totalSubs} NS)</span>
                    </button>`;
                }).join('');

                container.innerHTML = `
                    <div class="bg-slate-900 border border-indigo-500/40 rounded-2xl p-5 shadow-xl space-y-4 relative overflow-hidden">
                        <div class="absolute top-0 right-0 w-80 h-80 bg-indigo-600/5 rounded-full blur-3xl pointer-events-none"></div>
                        
                        <div class="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-800/90">
                            <button onclick="resetGroupFilter()" class="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-indigo-300 hover:text-white rounded-lg text-xs font-semibold border border-indigo-500/40 transition flex items-center gap-2 shadow-sm">
                                <i class="fa-solid fa-arrow-left"></i>
                                <span>Quay lại tổng quan 6 Leader</span>
                            </button>
                            <div class="flex flex-wrap items-center gap-1.5">
                                <span class="text-[11px] text-slate-400 font-medium mr-1 hidden sm:inline">Chuyển nhanh:</span>
                                ${leaderPills}
                            </div>
                        </div>

                        <!-- Header Chi Tiết Leader - Bố Cục Chống Tràn Dòng -->
                        <div class="flex flex-wrap items-start justify-between gap-4 pt-1">
                            <div class="flex items-center space-x-4">
                                <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-600 to-indigo-800 text-white font-black text-xl flex items-center justify-center shadow-lg border border-indigo-400/30 flex-shrink-0">
                                    ${l.name.split(' ').slice(-1)[0][0]}
                                </div>
                                <div class="space-y-1">
                                    <div class="flex flex-wrap items-center gap-2">
                                        <h3 class="text-lg font-bold text-white tracking-tight">${l.name}</h3>
                                        <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Rank ${l.rank}</span>
                                        <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${l.statusClass} border shadow-sm">${l.statusBadge}</span>
                                    </div>
                                    <p class="text-xs text-slate-400">
                                        <strong>${l.role}</strong> • Cơ sở phụ trách: <span class="text-slate-300">${l.campuses}</span>
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-1">
                            <div class="bg-slate-850 p-4 rounded-xl border border-slate-800 space-y-2">
                                <div class="flex items-center justify-between text-xs text-slate-400">
                                    <span class="font-semibold uppercase tracking-wider text-indigo-300">1. Quy mô nhân sự</span>
                                    <i class="fa-solid fa-users-gear text-indigo-400"></i>
                                </div>
                                <div class="flex items-baseline space-x-2">
                                    <span class="text-2xl font-bold text-white">${l.subs.length}</span>
                                    <span class="text-xs text-slate-400">nhân sự trực thuộc</span>
                                </div>
                                <p class="text-[11px] text-slate-400 leading-snug">
                                    Phân bố tại: <strong class="text-slate-200">${l.campuses}</strong>
                                </p>
                            </div>

                            <div class="bg-slate-850 p-4 rounded-xl border border-slate-800 space-y-2">
                                <div class="flex items-center justify-between text-xs text-slate-400">
                                    <span class="font-semibold uppercase tracking-wider text-emerald-300">2. Tính gương mẫu của Leader</span>
                                    <i class="fa-solid fa-medal ${l.compliance > 70 ? 'text-emerald-400' : 'text-rose-400'}"></i>
                                </div>
                                <div class="flex items-baseline space-x-2">
                                    <span class="text-2xl font-bold ${l.compliance > 70 ? 'text-emerald-400' : 'text-rose-400'}">${l.compliance}%</span>
                                    <span class="text-xs text-slate-400">(${l.reportedDays})</span>
                                </div>
                                <p class="text-[11px] text-slate-300 leading-snug">
                                    ${l.leaderReview}
                                </p>
                            </div>

                            <div class="bg-slate-850 p-4 rounded-xl border border-slate-800 space-y-2">
                                <div class="flex items-center justify-between text-xs text-slate-400">
                                    <span class="font-semibold uppercase tracking-wider text-rose-300">3. Nhân sự trực thuộc</span>
                                    <i class="fa-solid fa-triangle-exclamation text-rose-400"></i>
                                </div>
                                <div class="flex items-baseline space-x-2">
                                    <span class="text-2xl font-bold text-rose-400">+${l.excessHoursTotal}h</span>
                                    <span class="text-xs text-slate-400">tổng dôi dư</span>
                                </div>
                                <div class="text-[11px] text-slate-300">
                                    <span class="text-amber-400 font-bold">${l.reviewRankStaff.length}</span> người rà soát Rank • 
                                    <span class="text-rose-400 font-bold">${l.deductHoursStaff.length}</span> người cắt giờ ảo
                                </div>
                            </div>
                        </div>

                        <div class="bg-slate-850/60 p-4 rounded-xl border border-slate-800 space-y-3">
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="space-y-2">
                                    <div class="text-xs font-semibold text-amber-300 flex items-center gap-1.5">
                                        <i class="fa-solid fa-user-gear"></i> Nhân sự cần rà soát Rank (${l.reviewRankStaff.length}):
                                    </div>
                                    <div class="flex flex-wrap gap-2 pt-0.5">
                                        ${rankReviewTags}
                                    </div>
                                </div>

                                <div class="space-y-2">
                                    <div class="text-xs font-semibold text-rose-300 flex items-center gap-1.5">
                                        <i class="fa-solid fa-scissors"></i> Nhân sự cần cắt giảm giờ kê khai bù (${l.deductHoursStaff.length}):
                                    </div>
                                    <div class="flex flex-wrap gap-2 pt-0.5">
                                        ${deductTags}
                                    </div>
                                </div>
                            </div>

                            <div class="pt-3 border-t border-slate-800 text-xs text-slate-300 leading-relaxed flex items-start space-x-2">
                                <i class="fa-solid fa-bullhorn text-indigo-400 mt-0.5"></i>
                                <span><strong>Khuyến nghị cho Giám đốc Đào tạo:</strong> ${l.actionForDirector}</span>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                let cardsHtml = "";
                Object.keys(LEADER_DIRECTORY_BASE).forEach(gKey => {
                    const l = getDynamicLeaderInfo(gKey);
                    cardsHtml += `
                        <div onclick="selectGroupFilter('${l.groupKey}')" class="bg-slate-900 border border-slate-800 rounded-2xl p-5 cursor-pointer transition leader-card-hover h-full flex flex-col justify-between space-y-4 relative group">
                            <div class="space-y-3">
                                <!-- Header Thẻ: Bố cục 2 tầng chống tràn dòng tên thầy cô dài -->
                                <div class="flex items-start space-x-3">
                                    <div class="w-11 h-11 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center font-black text-indigo-400 text-base shadow-sm group-hover:border-indigo-500 transition flex-shrink-0">
                                        ${l.name.split(' ').slice(-1)[0][0]}
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <h4 class="text-sm font-bold text-white group-hover:text-indigo-300 transition truncate" title="${l.name}">${l.name}</h4>
                                        <div class="flex flex-wrap items-center gap-1.5 mt-1">
                                            <span class="text-[10px] px-1.5 py-0.5 rounded font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Rank ${l.rank}</span>
                                            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold border ${l.statusClass} truncate max-w-[200px]" title="${l.statusBadge}">
                                                ${l.statusBadge}
                                            </span>
                                        </div>
                                        <p class="text-[11px] text-slate-400 font-medium mt-1 truncate">${l.groupKey}</p>
                                    </div>
                                </div>

                                <!-- 3 Hộp Chỉ Số Then Chốt -->
                                <div class="grid grid-cols-3 gap-2 bg-slate-850 p-2.5 rounded-xl text-center border border-slate-800/80">
                                    <div>
                                        <span class="text-[10px] text-slate-400 block uppercase font-medium">Nhân sự</span>
                                        <span class="text-sm font-bold text-white">${l.subs.length} NS</span>
                                    </div>
                                    <div>
                                        <span class="text-[10px] text-slate-400 block uppercase font-medium">Báo cáo ngày</span>
                                        <span class="text-sm font-bold ${l.compliance > 70 ? 'text-emerald-400' : 'text-rose-400'}">${l.compliance}%</span>
                                    </div>
                                    <div>
                                        <span class="text-[10px] text-slate-400 block uppercase font-medium">Dôi dư giờ</span>
                                        <span class="text-sm font-bold text-rose-400">+${l.excessHoursTotal}h</span>
                                    </div>
                                </div>

                                <!-- Thống kê diện rà soát -->
                                <div class="flex items-center justify-between text-xs bg-slate-850/50 px-3 py-2 rounded-lg border border-slate-800/60">
                                    <span>Rà soát Rank: <strong class="text-amber-400 font-bold">${l.reviewRankStaff.length} NS</strong></span>
                                    <span>Cắt giờ ảo: <strong class="text-rose-400 font-bold">${l.deductHoursStaff.length} NS</strong></span>
                                </div>

                                <!-- Nhận xét nhanh về tính gương mẫu -->
                                <p class="text-xs text-slate-400 leading-relaxed line-clamp-2">
                                    ${l.leaderReview}
                                </p>
                            </div>

                            <!-- Nút Thao Tác Trực Quan Đặt Dưới Cùng Cân Đối -->
                            <div class="pt-2 border-t border-slate-850">
                                <button class="w-full py-2 bg-slate-800 group-hover:bg-indigo-600 text-slate-300 group-hover:text-white rounded-lg text-xs font-semibold transition border border-slate-700 group-hover:border-indigo-500 flex items-center justify-center gap-1.5 shadow-sm">
                                    <span>Xem chi tiết nhân sự của Leader</span>
                                    <i class="fa-solid fa-arrow-right text-[11px]"></i>
                                </button>
                            </div>
                        </div>
                    `;
                });

                container.innerHTML = `
                    <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
                        <div class="flex flex-wrap items-center justify-between gap-2">
                            <div class="flex items-center space-x-2">
                                <i class="fa-solid fa-users-viewfinder text-indigo-400 text-base"></i>
                                <h3 class="text-xs font-bold uppercase tracking-wider text-slate-200">
                                    Kiểm Toán Trách Nhiệm Người Đứng Đầu (6 Leader Các Khối Đào Tạo)
                                </h3>
                            </div>
                            <span class="text-[11px] text-indigo-300/90 italic">Click vào thẻ của bất kỳ Leader nào để xem chi tiết danh sách nhân sự trực thuộc</span>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            ${cardsHtml}
                        </div>
                    </div>
                `;
            }
        }

        function selectGroupFilter(groupKey) {
            document.getElementById("groupFilter").value = groupKey;
            filterTable();
            const container = document.getElementById("leaderAccountabilityContainer");
            if (container) {
                container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }

        function resetGroupFilter() {
            document.getElementById("groupFilter").value = "ALL";
            filterTable();
            const container = document.getElementById("leaderAccountabilityContainer");
            if (container) {
                container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }

        function filterTable() {
            const campusVal = document.getElementById("campusFilter").value;
            const groupVal = document.getElementById("groupFilter").value;
            const catVal = document.getElementById("categoryFilter").value;
            const searchVal = document.getElementById("searchInput").value.toLowerCase().trim();

            const filtered = staffList.filter(s => {
                const matchCampus = (campusVal === "ALL") || (s.campus === campusVal);
                const matchGroup = (groupVal === "ALL") || (s.group === groupVal || s.group.includes(groupVal));
                const matchCat = (catVal === "ALL") || (s.recommendation_category === catVal);
                const matchSearch = (!searchVal) || (s.name.toLowerCase().includes(searchVal));
                return matchCampus && matchGroup && matchCat && matchSearch;
            });

            renderLeaderAccountability(groupVal, campusVal);

            const countEl = document.getElementById("displayedCount");
            countEl.textContent = filtered.length;

            let titleStr = "Danh sách nhân sự trực thuộc khối đào tạo";
            if (groupVal !== "ALL") {
                const l = LEADER_DIRECTORY_BASE[groupVal];
                titleStr = `Danh sách nhân sự trực thuộc ${l ? l.name : ''} (${groupVal})`;
            } else if (campusVal !== "ALL") {
                titleStr = `Danh sách nhân sự tại ${campusVal}`;
            }
            document.getElementById("tableTitle").textContent = titleStr;

            const tbody = document.getElementById("staffTableBody");
            tbody.innerHTML = "";

            if (filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="9" class="py-8 text-center text-slate-500 text-xs">Không tìm thấy nhân sự nào phù hợp với bộ lọc hiện tại.</td></tr>`;
                return;
            }

            const sorted = [...filtered].sort((a, b) => {
                const order = { "CẦN RÀ SOÁT RANK": 1, "CẢNH BÁO BÙ GIỜ": 2, "CHƯA NỘP BÁO CÁO": 3, "CHUẨN MỰC": 4 };
                return (order[a.recommendation_category] || 99) - (order[b.recommendation_category] || 99) || (b.excess_hours - a.excess_hours);
            });

            sorted.forEach(s => {
                let badgeHtml = "";
                if (s.recommendation_category === "CẦN RÀ SOÁT RANK") {
                    badgeHtml = `<span class="px-2.5 py-0.5 text-[11px] font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/40 rounded-full inline-flex items-center gap-1">
                                    <i class="fa-solid fa-user-gear text-[10px]"></i> Cần rà soát hạ Rank
                                 </span>`;
                } else if (s.recommendation_category === "CẢNH BÁO BÙ GIỜ") {
                    badgeHtml = `<span class="px-2.5 py-0.5 text-[11px] font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/40 rounded-full inline-flex items-center gap-1">
                                    <i class="fa-solid fa-scissors text-[10px]"></i> Cắt giảm giờ công ảo
                                 </span>`;
                } else if (s.recommendation_category === "CHƯA NỘP BÁO CÁO") {
                    badgeHtml = `<span class="px-2.5 py-0.5 text-[11px] font-semibold bg-slate-800 text-slate-400 border border-slate-700 rounded-full inline-flex items-center gap-1">
                                    <i class="fa-regular fa-circle-xmark text-[10px]"></i> Bỏ trống báo cáo (0%)
                                 </span>`;
                } else {
                    badgeHtml = `<span class="px-2.5 py-0.5 text-[11px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 rounded-full inline-flex items-center gap-1">
                                    <i class="fa-solid fa-check text-[10px]"></i> Chuẩn mực
                                 </span>`;
                }

                const diffHours = s.excess_hours;
                const diffColor = diffHours > 40 ? "text-rose-400 font-bold" : (diffHours > 15 ? "text-amber-400 font-semibold" : "text-slate-300");

                const tr = document.createElement("tr");
                tr.className = "hover:bg-slate-800/60 cursor-pointer transition";
                tr.onclick = () => openDrawer(s);

                tr.innerHTML = `
                    <td class="py-2.5 px-4 min-w-[200px]">
                        <div class="font-bold text-white hover:text-indigo-400 transition truncate" title="${s.name}">${s.name}</div>
                        <div class="text-[10px] text-slate-500"><i class="fa-solid fa-user-tie text-[9px] mr-1"></i>${s.campus_leader || ''}</div>
                    </td>
                    <td class="py-2.5 px-3">
                        <div class="text-slate-300 font-medium">${s.role}</div>
                        <div class="text-[11px] font-semibold text-indigo-400">Rank ${s.rank}</div>
                    </td>
                    <td class="py-2.5 px-3">
                        <div class="text-slate-300 font-medium">${s.group}</div>
                        <div class="text-[10px] text-slate-400">${s.campus}</div>
                    </td>
                    <td class="py-2.5 px-3 text-center">
                        <span class="font-bold ${s.compliance_rate >= 80 ? 'text-emerald-400' : (s.compliance_rate > 0 ? 'text-amber-400' : 'text-slate-500')}">
                            ${s.compliance_rate}%
                        </span>
                        <div class="text-[10px] text-slate-500">${s.reported_days}/${s.expected_days} ngày</div>
                    </td>
                    <td class="py-2.5 px-3 text-right font-medium text-slate-200">${s.total_declared_hours}h</td>
                    <td class="py-2.5 px-3 text-right font-medium text-emerald-400/90">${s.total_standard_hours}h</td>
                    <td class="py-2.5 px-3 text-right ${diffColor}">+${diffHours}h</td>
                    <td class="py-2.5 px-4">${badgeHtml}</td>
                    <td class="py-2.5 px-3 text-center">
                        <button class="px-2.5 py-1 bg-slate-800 hover:bg-indigo-600 text-slate-300 hover:text-white rounded text-[11px] transition font-medium border border-slate-700">
                            Chi tiết <i class="fa-solid fa-angle-right ml-0.5"></i>
                        </button>
                    </td>
                `;

                tbody.appendChild(tr);
            });
        }

        function openDrawerByName(staffName) {
            const staff = staffList.find(s => s.name === staffName);
            if (staff) openDrawer(staff);
        }

        function switchDrawerTab(tabId) {
            activeTab = tabId;
            const tabs = ['tabExcess', 'tabFree', 'tabUnverified', 'tabAllLogs'];
            tabs.forEach(t => {
                const btn = document.getElementById('btn' + t.charAt(0).toUpperCase() + t.slice(1));
                const panel = document.getElementById('panel' + t.charAt(0).toUpperCase() + t.slice(1));
                if (t === tabId) {
                    btn.className = "px-3 py-1.5 rounded-lg bg-indigo-600 text-white transition flex items-center space-x-1.5 shadow-sm font-medium";
                    panel.classList.remove('hidden');
                } else {
                    btn.className = "px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-750 text-slate-300 transition flex items-center space-x-1.5 font-medium";
                    panel.classList.add('hidden');
                }
            });
        }

        function openDrawer(staff) {
            currentSelectedStaff = staff;

            document.getElementById("drawerStaffName").textContent = staff.name;
            document.getElementById("drawerStaffRank").textContent = `Rank ${staff.rank} • ${staff.role}`;
            document.getElementById("drawerStaffGroup").textContent = `${staff.group} • ${staff.campus}`;
            document.getElementById("drawerStaffLeader").innerHTML = `<i class="fa-solid fa-user-tie mr-1"></i>Leader: ${staff.campus_leader}`;

            const initials = staff.name.split(' ').map(w => w[0]).join('').slice(-2).toUpperCase();
            document.getElementById("drawerAvatar").textContent = initials;

            document.getElementById("drawerCompliance").textContent = staff.compliance_rate + "%";
            document.getElementById("drawerReportDays").textContent = `${staff.reported_days}/${staff.expected_days} ngày`;
            document.getElementById("drawerHoursRatio").textContent = `${staff.total_declared_hours}h / ${staff.total_standard_hours}h`;
            document.getElementById("drawerExcessHours").textContent = `+${staff.excess_hours}h`;

            const catEl = document.getElementById("drawerRecCategory");
            catEl.textContent = staff.recommendation_label;
            if (staff.recommendation_category === "CẦN RÀ SOÁT RANK") {
                catEl.className = "font-bold text-amber-400 uppercase tracking-wide";
            } else if (staff.recommendation_category === "CẢNH BÁO BÙ GIỜ") {
                catEl.className = "font-bold text-rose-400 uppercase tracking-wide";
            } else {
                catEl.className = "font-bold text-emerald-400 uppercase tracking-wide";
            }
            document.getElementById("drawerActionNote").textContent = staff.action_note;

            document.getElementById("drawerExcessCount").textContent = (staff.excess_tasks || []).length;
            document.getElementById("drawerFreeCount").textContent = (staff.free_floating_tasks || []).length;
            document.getElementById("drawerUnverifiedCount").textContent = (staff.unverified_tasks || []).length;

            renderExcessTab(staff.excess_tasks || []);
            renderFreeTab(staff.free_floating_tasks || []);
            renderUnverifiedTab(staff.unverified_tasks || []);
            renderAllLogsTab(staff.recent_tasks || []);

            switchDrawerTab('tabExcess');

            document.getElementById("drawerBackdrop").classList.remove("opacity-0", "pointer-events-none");
            document.getElementById("staffDrawer").classList.remove("translate-x-full");
        }

        function renderExcessTab(tasks) {
            const panel = document.getElementById("panelTabExcess");
            if (tasks.length === 0) {
                panel.innerHTML = `<div class="p-6 text-center text-slate-500 text-xs bg-slate-850 rounded-xl border border-slate-800">
                    <i class="fa-solid fa-circle-check text-emerald-400 text-lg mb-1 block"></i>
                    Không có task nào vượt trên 1.5x định mức chuẩn.
                </div>`;
                return;
            }
            panel.innerHTML = tasks.map((t, idx) => `
                <div class="bg-slate-850 p-3.5 rounded-xl border border-slate-800 space-y-2">
                    <div class="flex items-start justify-between gap-2">
                        <div class="font-medium text-slate-200">
                            <span class="text-indigo-400 font-mono text-[11px] mr-1">[${t.date}]</span>
                            ${t.title}
                        </div>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 whitespace-nowrap">
                            +${t.deviation_hours}h (${t.deviation_pct}%)
                        </span>
                    </div>
                    <div class="flex items-center justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-800">
                        <span>Khai: <strong class="text-white">${t.declared_hours}h</strong> vs Chuẩn: <strong class="text-emerald-400">${t.standard_hours}h</strong></span>
                        <span class="text-slate-500 italic">${t.matched_category}</span>
                    </div>
                    <div class="text-[11px] text-amber-300/90 bg-amber-950/30 p-2 rounded border border-amber-900/40">
                        <i class="fa-solid fa-triangle-exclamation text-amber-400 mr-1"></i> ${t.reason}
                    </div>
                </div>
            `).join('');
        }

        function renderFreeTab(tasks) {
            const panel = document.getElementById("panelTabFree");
            if (tasks.length === 0) {
                panel.innerHTML = `<div class="p-6 text-center text-slate-500 text-xs bg-slate-850 rounded-xl border border-slate-800">
                    <i class="fa-solid fa-circle-check text-emerald-400 text-lg mb-1 block"></i>
                    Không có task nào nằm ngoài barem Master.
                </div>`;
                return;
            }
            panel.innerHTML = tasks.map((t, idx) => `
                <div class="bg-slate-850 p-3.5 rounded-xl border border-slate-800 space-y-2">
                    <div class="flex items-start justify-between gap-2">
                        <div class="font-medium text-slate-200">
                            <span class="text-indigo-400 font-mono text-[11px] mr-1">[${t.date}]</span>
                            ${t.title}
                        </div>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30 whitespace-nowrap">
                            Khai ${t.declared_hours}h
                        </span>
                    </div>
                    <div class="text-[11px] text-rose-300/90 bg-rose-950/30 p-2 rounded border border-rose-900/40">
                        <i class="fa-solid fa-scissors text-rose-400 mr-1"></i> ${t.reason}
                    </div>
                </div>
            `).join('');
        }

        function renderUnverifiedTab(tasks) {
            const panel = document.getElementById("panelTabUnverified");
            if (tasks.length === 0) {
                panel.innerHTML = `<div class="p-6 text-center text-slate-500 text-xs bg-slate-850 rounded-xl border border-slate-800">
                    <i class="fa-solid fa-circle-check text-emerald-400 text-lg mb-1 block"></i>
                    Không phát hiện tình trạng báo Done ở Daily Log nhưng Ticket Worklane chưa hoàn thành.
                </div>`;
                return;
            }
            panel.innerHTML = tasks.map((t, idx) => `
                <div class="bg-slate-850 p-3.5 rounded-xl border border-slate-800 space-y-2">
                    <div class="font-medium text-slate-200">
                        <span class="text-indigo-400 font-mono text-[11px] mr-1">[${t.date}]</span>
                        ${t.title}
                    </div>
                    <div class="text-[11px] text-amber-300/90 bg-amber-950/30 p-2 rounded border border-amber-900/40">
                        <i class="fa-solid fa-ticket text-amber-400 mr-1"></i>
                        Ticket: <strong>${t.issue_title}</strong> (Trạng thái Worklane: <span class="text-rose-400 font-bold">${t.issue_state}</span>)
                    </div>
                </div>
            `).join('');
        }

        function renderAllLogsTab(tasks) {
            const panel = document.getElementById("panelTabAllLogs");
            if (tasks.length === 0) {
                panel.innerHTML = `<div class="p-6 text-center text-slate-500 text-xs bg-slate-850 rounded-xl border border-slate-800">Không có nhật ký công việc nào được ghi nhận.</div>`;
                return;
            }
            panel.innerHTML = tasks.map((t, idx) => `
                <div class="bg-slate-850 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between text-xs">
                    <div class="space-y-0.5 max-w-[75%]">
                        <div class="text-slate-200 font-medium truncate" title="${t.title}">
                            <span class="text-indigo-400 font-mono text-[11px] mr-1">[${t.date}]</span>
                            ${t.title}
                        </div>
                        <div class="text-[10px] text-slate-500">${t.matched_category}</div>
                    </div>
                    <div class="text-right flex-shrink-0">
                        <div class="font-bold text-white">${t.declared_hours}h</div>
                        <div class="text-[10px] text-emerald-400 font-medium">Chuẩn: ${t.standard_hours}h</div>
                    </div>
                </div>
            `).join('');
        }

        function closeDrawer() {
            document.getElementById("drawerBackdrop").classList.add("opacity-0", "pointer-events-none");
            document.getElementById("staffDrawer").classList.add("translate-x-full");
            currentSelectedStaff = null;
        }

        function copyStaffAuditReport() {
            if (!currentSelectedStaff) return;
            const s = currentSelectedStaff;
            const periodLabel = currentPeriod === 'sept_01_08' ? 'KỲ 01/09 - 08/09/2026' : 'THÁNG 08/2026';
            let text = `PHIẾU LÀM VIỆC 1-1 KIỂM TOÁN HIỆU SUẤT (${periodLabel})\\n`;
            text += `===============================================\\n`;
            text += `Họ và tên: ${s.name} (Rank ${s.rank} - ${s.role})\\n`;
            text += `Khối: ${s.group} - ${s.campus}\\n`;
            text += `Leader quản lý: ${s.campus_leader}\\n`;
            text += `Giờ khai báo: ${s.total_declared_hours}h | Chuẩn KPI: ${s.total_standard_hours}h | Dôi dư: +${s.excess_hours}h\\n`;
            text += `Kết luận kiểm toán: ${s.recommendation_label}\\n`;
            text += `Đề xuất xử lý của Leader: ${s.action_note}\\n\\n`;
            text += `DANH SÁCH CÁC TASK VƯỢT ĐỊNH MỨC:\\n`;
            (s.excess_tasks || []).forEach((t, i) => {
                text += `${i+1}. [${t.date}] ${t.title} (Khai ${t.declared_hours}h vs Chuẩn ${t.standard_hours}h) -> ${t.reason}\\n`;
            });
            
            navigator.clipboard.writeText(text).then(() => {
                alert(`Đã sao chép phiếu làm việc 1-1 của ${s.name} vào Clipboard!`);
            });
        }

        function markReviewed() {
            alert("Đã ghi nhận xác nhận của Leader cho nhân sự này.");
        }

        let chartExcessInstance = null;
        let chartDailyInstance = null;

        // Khởi tạo Biểu đồ Chart.js So Sánh T8 vs T9
        function initComparisonCharts() {
            if (!comparisonData || !comparisonData.comparison) return;

            if (chartExcessInstance) {
                chartExcessInstance.destroy();
                chartExcessInstance = null;
            }
            if (chartDailyInstance) {
                chartDailyInstance.destroy();
                chartDailyInstance = null;
            }

            const labels = comparisonData.comparison.map(c => c.short_label);
            const augPctData = comparisonData.comparison.map(c => c.august.excess_pct);
            const septPctData = comparisonData.comparison.map(c => c.september.excess_pct);

            const augRateData = comparisonData.comparison.map(c => c.august.excess_per_day_staff);
            const septRateData = comparisonData.comparison.map(c => c.september.excess_per_day_staff);

            // Chart 1: Tỷ lệ vênh %
            const el1 = document.getElementById('chartExcessPct');
            if (el1) {
                chartExcessInstance = new Chart(el1.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Tháng 8 (Vênh %)',
                                data: augPctData,
                                backgroundColor: 'rgba(99, 102, 241, 0.75)',
                                borderColor: '#6366f1',
                                borderWidth: 1,
                                borderRadius: 6
                            },
                            {
                                label: 'Tháng 9 (Vênh %)',
                                data: septPctData,
                                backgroundColor: 'rgba(251, 191, 36, 0.85)',
                                borderColor: '#f59e0b',
                                borderWidth: 1,
                                borderRadius: 6
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                                titleColor: '#e2e8f0',
                                bodyColor: '#cbd5e1',
                                borderColor: '#334155',
                                borderWidth: 1,
                                padding: 10,
                                callbacks: {
                                    label: function(context) {
                                        return `${context.dataset.label}: ${context.raw > 0 ? '+' : ''}${context.raw}%`;
                                    }
                                }
                            }
                        },
                        scales: {
                            x: {
                                grid: { display: false },
                                ticks: { color: '#94a3b8', font: { size: 11, weight: '500' } }
                            },
                            y: {
                                grid: { color: 'rgba(51, 65, 85, 0.4)' },
                                ticks: {
                                    color: '#94a3b8',
                                    callback: function(val) { return val + '%'; }
                                }
                            }
                        }
                    }
                });
            }

            // Chart 2: Giờ dôi dư TB/ngày/nhân sự
            const el2 = document.getElementById('chartDailyRate');
            if (el2) {
                chartDailyInstance = new Chart(el2.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Tháng 8 (h/ngày/NS)',
                                data: augRateData,
                                backgroundColor: 'rgba(71, 85, 105, 0.75)',
                                borderColor: '#64748b',
                                borderWidth: 1,
                                borderRadius: 6
                            },
                            {
                                label: 'Tháng 9 (h/ngày/NS)',
                                data: septRateData,
                                backgroundColor: 'rgba(34, 197, 94, 0.85)',
                                borderColor: '#10b981',
                                borderWidth: 1,
                                borderRadius: 6
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                                titleColor: '#e2e8f0',
                                bodyColor: '#cbd5e1',
                                borderColor: '#334155',
                                borderWidth: 1,
                                padding: 10,
                                callbacks: {
                                    label: function(context) {
                                        return `${context.dataset.label}: +${context.raw}h / ngày / NS`;
                                    }
                                }
                            }
                        },
                        scales: {
                            x: {
                                grid: { display: false },
                                ticks: { color: '#94a3b8', font: { size: 11, weight: '500' } }
                            },
                            y: {
                                grid: { color: 'rgba(51, 65, 85, 0.4)' },
                                ticks: {
                                    color: '#94a3b8',
                                    callback: function(val) { return val + 'h'; }
                                }
                            }
                        }
                    }
                });
            }
        }

        // Khởi chạy an toàn 1 lần duy nhất
        let isChartsInit = false;
        function safeInit() {
            if (isChartsInit) return;
            isChartsInit = true;
            initComparisonCharts();
            filterTable();
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', safeInit);
        } else {
            safeInit();
        }
    </script>
</body>
</html>
"""

def generate_dashboard_v4():
    json_path = r"data/processed/worklane_audit_detailed.json"
    comp_path = r"data/processed/worklane_comparison_t8_t9.json"
    
    if not os.path.exists(json_path):
        print(f"Lỗi: Không tìm thấy file {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    comp_data = {}
    if os.path.exists(comp_path):
        with open(comp_path, "r", encoding="utf-8") as f:
            comp_data = json.load(f)

    json_embedded = json.dumps(data, ensure_ascii=False)
    comp_embedded = json.dumps(comp_data, ensure_ascii=False)

    html = HTML_TEMPLATE.replace("__JSON_EMBEDDED__", json_embedded)
    html = html.replace("__COMPARISON_JSON__", comp_embedded)

    out_dir = r"output/dashboards/audit"
    os.makedirs(out_dir, exist_ok=True)
    out_html_path = os.path.join(out_dir, "worklane_staff_audit.html")
    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard V4 with Comparison Charts generated successfully at: {out_html_path}")

if __name__ == "__main__":
    generate_dashboard_v4()

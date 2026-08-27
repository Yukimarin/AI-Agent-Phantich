import os
import sys
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("Agent 3: Khởi chạy trình sinh báo cáo HTML trực quan v7.4 (Tích hợp QTKD Leader & Bảng Rich Text Email)...")
    
    json_path = "data/processed/agent3_output.json"
    output_path = "output/dashboards/core/agent_3_ops_discipline.html"
    
    if not os.path.exists(json_path):
        print(f"Error: Không tìm thấy file dữ liệu JSON {json_path}")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        violations = json.load(f)
        
    json_data_str = json.dumps(violations, ensure_ascii=False)
    
    # HTML template với thiết kế v7.4
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo Kỷ luật tác nghiệp GV/TG (Agent 3)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-main: #090d16;
            --bg-card: #0f172a;
            --bg-elevated: #1e293b;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --primary: #3b82f6;
            --primary-light: rgba(59, 130, 246, 0.15);
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #f43f5e;
            --border: rgba(255, 255, 255, 0.08);
            --font-family: 'Plus Jakarta Sans', sans-serif;
            --card-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), 0 1px 3px rgba(0, 0, 0, 0.2);
        }}
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
        }}
        .card-dark {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            box-shadow: var(--card-shadow);
            border-radius: 20px;
        }}
        /* Offcanvas Sidebar Styles */
        #offcanvasRight {{
            position: fixed;
            top: 0;
            right: 0;
            width: 520px;
            height: 100%;
            background-color: #0f172a;
            border-left: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: -10px 0 30px rgba(0, 0, 0, 0.5);
            transform: translateX(100%);
            transition: transform 0.3s ease-in-out;
            z-index: 100;
        }}
        #offcanvasRight.open {{
            transform: translateX(0);
        }}
    </style>
</head>
<body class="py-10 px-4 md:px-8">
    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <header class="bg-[#1e293b]/45 backdrop-blur-md rounded-3xl p-8 shadow-2xl border border-white/10 flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
            <div>
                <div class="flex items-center gap-3">
                    <span class="px-3 py-1 bg-rose-500/10 text-rose-400 font-bold text-xs rounded-full uppercase tracking-wider border border-rose-500/20">Agent 3: Ops Auditor</span>
                    <span class="px-3 py-1 bg-blue-500/15 text-blue-400 font-bold text-xs rounded-full border border-blue-500/30" id="currentPeriodBadge">Khối Đào tạo</span>
                </div>
                <h1 class="text-3xl font-extrabold mt-3 text-slate-100 flex items-center gap-3">
                    <i class="fa-solid fa-triangle-exclamation text-rose-500"></i> Báo cáo Kỷ luật tác nghiệp GV/TG (Toàn khối)
                </h1>
                <p class="text-sm text-slate-400 mt-2">Đối chiếu tự động vi phạm trên hệ thống Worklane PM (báo cáo ngày & trễ task) và QLĐT (tài nguyên & BTVN chậm) của toàn bộ nhân sự (HN, HCM, QTKD, Ngoại ngữ, v.v.).</p>
            </div>
            <div class="bg-white/5 backdrop-blur-md rounded-2xl p-4 border border-white/5 flex items-center gap-4">
                <div class="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center text-2xl text-rose-400">
                    <i class="fa-solid fa-clock"></i>
                </div>
                <div>
                    <div class="text-xs text-slate-400">Cập nhật lúc</div>
                    <div class="font-bold text-sm text-slate-200">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
                </div>
            </div>
        </header>

        <!-- Quick Switch Tab Switcher (Tuần vs Tháng) -->
        <div class="flex items-center gap-4 mb-6 bg-white/5 p-2 rounded-2xl border border-white/5 max-w-md">
            <button id="tabWeek" onclick="switchCycleTab('weekly')" class="flex-1 py-3 text-center rounded-xl font-bold transition-all text-sm bg-rose-600 text-white shadow-lg">
                <i class="fa-solid fa-calendar-week mr-2"></i> Xem theo Tuần
            </button>
            <button id="tabMonth" onclick="switchCycleTab('monthly')" class="flex-1 py-3 text-center rounded-xl font-bold transition-all text-sm text-slate-400 hover:text-slate-200">
                <i class="fa-solid fa-calendar-days mr-2"></i> Xem theo Tháng
            </button>
        </div>

        <!-- Filters & Action Section -->
        <div class="card-dark p-6 mb-8 grid grid-cols-1 md:grid-cols-4 gap-6 items-end">
            <div>
                <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Loại Chu kỳ</label>
                <select id="cycleType" onchange="onCycleTypeChange()" class="w-full bg-[#1e293b]/60 border border-white/10 rounded-xl px-4 py-3 font-semibold text-slate-200 focus:outline-none focus:ring-2 focus:ring-rose-500">
                    <option value="weekly">Xem theo Tuần</option>
                    <option value="monthly">Xem theo Tháng</option>
                    <option value="all">Xem tất cả</option>
                </select>
            </div>
            
            <div id="cycleValueContainer">
                <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Chọn Thời gian (Mới nhất ở đầu)</label>
                <select id="cycleValue" onchange="renderDashboard()" class="w-full bg-[#1e293b]/60 border border-white/10 rounded-xl px-4 py-3 font-semibold text-slate-200 focus:outline-none focus:ring-2 focus:ring-rose-500">
                    <!-- Dynamic values -->
                </select>
            </div>

            <div>
                <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Vai Trò</label>
                <select id="roleFilter" onchange="renderDashboard()" class="w-full bg-[#1e293b]/60 border border-white/10 rounded-xl px-4 py-3 font-semibold text-slate-200 focus:outline-none focus:ring-2 focus:ring-rose-500">
                    <option value="all">Tất cả vai trò</option>
                    <option value="GV">Giảng viên (GV)</option>
                    <option value="TG">Trợ giảng (TG)</option>
                </select>
            </div>

            <div>
                <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Tìm kiếm giảng viên / trợ giảng</label>
                <div class="relative">
                    <input type="text" id="searchPersonnel" oninput="renderDashboard()" placeholder="Nhập tên nhân sự toàn khối..." class="w-full bg-[#1e293b]/60 border border-white/10 rounded-xl pl-10 pr-4 py-3 font-semibold text-slate-200 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-rose-500">
                    <i class="fa-solid fa-magnifying-glass absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-500"></i>
                </div>
            </div>
        </div>

        <!-- Global Action Row -->
        <div class="flex justify-between items-center mb-8 flex-wrap gap-4">
            <h2 class="font-bold text-slate-400 text-sm uppercase tracking-wider">Bảng điều khiển & Giám sát</h2>
            <div class="flex gap-3 flex-wrap">
                <select id="groupEmailSelect" onchange="if(this.value !== '') {{ openBranchEmailModal(this.value); this.value = ''; }}" class="bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-2xl px-4 py-2.5 text-sm focus:outline-none cursor-pointer border border-rose-500/20 shadow-lg">
                    <option value="">📧 Soạn Email theo Cơ sở & Khối...</option>
                    <option value="CNTT_HCM">Khối CNTT - HCM (CC Thầy Đạo)</option>
                    <option value="CNTT_NT">Khối CNTT - Ngọc Trục (CC Thầy Hùng)</option>
                    <option value="CNTT_HPC">Khối CNTT - HPC (CC Thầy Hai)</option>
                    <option value="QTKD">Khối QTKD (CC Cô Oanh)</option>
                    <option value="NGOAI_NGU">Khối Ngoại ngữ (CC Cô Hằng)</option>
                    <option value="QLCLDT">Khối QLCLĐT (CC Cô Tươi)</option>
                </select>
                <button onclick="openGroupEmailModal()" class="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold rounded-2xl transition-all flex items-center gap-2 text-sm border border-white/5 shadow-lg">
                    <i class="fa-solid fa-envelope-open-text"></i> Soạn Email toàn khối (Bản tin chung)
                </button>
            </div>
        </div>

        <!-- Overview & Trend Chart Row -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            <!-- Overview KPI Cards -->
            <div class="lg:col-span-1 grid grid-cols-1 gap-6" id="statsContainer">
                <!-- Dynamic stats card -->
            </div>

            <!-- Trend Line Chart -->
            <div class="card-dark p-6 lg:col-span-2 flex flex-col justify-between">
                <h2 class="font-bold text-slate-100 text-sm uppercase tracking-wider mb-4 flex items-center gap-2 text-slate-400">
                    <i class="fa-solid fa-chart-line text-blue-400"></i> Sự tiến bộ của các thầy/cô trong khối (Xu hướng giảm lỗi)
                </h2>
                <div class="relative h-48 w-full">
                    <canvas id="trendChartCanvas"></canvas>
                </div>
            </div>
        </div>

        <!-- Top 5 Tuân thủ Tốt và Kém (Gộp chung QLĐT & Worklane) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <!-- Top 5 Tuân thủ Tốt nhất -->
            <div class="card-dark overflow-hidden">
                <div class="p-6 border-b border-white/5 bg-emerald-500/5 flex items-center justify-between">
                    <h2 class="font-bold text-slate-100 text-lg flex items-center gap-2">
                        <i class="fa-solid fa-circle-check text-emerald-400"></i> Top 5 GV/TG Tuân thủ tốt nhất
                    </h2>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse text-sm">
                        <thead>
                            <tr class="bg-white/5 text-slate-400 font-bold text-xs uppercase border-b border-white/5">
                                <th class="px-4 py-3">Nhân sự</th>
                                <th class="px-4 py-3 text-center">Lỗi QLĐT</th>
                                <th class="px-4 py-3 text-center">Vắng Báo cáo ngày</th>
                                <th class="px-4 py-3 text-center">Task trễ hạn</th>
                                <th class="px-4 py-3 text-center">Điểm</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-white/5" id="topGoodBody">
                            <!-- Dynamic rows -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Top 5 Tuân thủ Kém nhất -->
            <div class="card-dark overflow-hidden">
                <div class="p-6 border-b border-white/5 bg-rose-500/5 flex items-center justify-between">
                    <h2 class="font-bold text-slate-100 text-lg flex items-center gap-2">
                        <i class="fa-solid fa-circle-xmark text-rose-400"></i> Top 5 GV/TG Tuân thủ chưa tốt
                    </h2>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse text-sm">
                        <thead>
                            <tr class="bg-white/5 text-slate-400 font-bold text-xs uppercase border-b border-white/5">
                                <th class="px-4 py-3">Nhân sự</th>
                                <th class="px-4 py-3 text-center">Lỗi QLĐT</th>
                                <th class="px-4 py-3 text-center">Vắng Báo cáo ngày</th>
                                <th class="px-4 py-3 text-center">Task trễ hạn</th>
                                <th class="px-4 py-3 text-center">Điểm</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-white/5" id="topBadBody">
                            <!-- Dynamic rows -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Main Personnel compliance table (Click row to open Offcanvas details drawer) -->
        <!-- Grouped Personnel compliance tables (Dynamic render by Block & Facility) -->
        <div id="groupedComplianceTablesContainer" class="space-y-8 mb-8">
            <!-- Tables will be generated dynamically by JS -->
        </div>
    </div>

    <!-- Offcanvas Overlay -->
    <div id="offcanvasOverlay" class="fixed inset-0 bg-slate-950/80 z-40 hidden transition-opacity duration-200" onclick="closeOffcanvas()"></div>

    <!-- Offcanvas Details Drawer -->
    <div id="offcanvasRight" class="flex flex-col justify-between">
        <div class="p-6 overflow-y-auto h-full flex flex-col justify-between">
            <div>
                <!-- Offcanvas Header -->
                <div class="flex justify-between items-center pb-4 border-b border-white/5">
                    <div>
                        <h3 class="text-xl font-bold text-slate-100 flex items-center gap-2" id="drawerTitle">
                            <i class="fa-solid fa-address-card text-rose-500"></i> Chi tiết vi phạm của nhân sự
                        </h3>
                        <p class="text-xs text-slate-400 mt-1" id="drawerSubtitle">Vai trò - Rank</p>
                    </div>
                    <div class="cursor-pointer p-2 bg-white/5 hover:bg-white/10 rounded-full transition-colors" onclick="closeOffcanvas()">
                        <i class="fa-solid fa-xmark text-slate-400"></i>
                    </div>
                </div>

                <!-- Offcanvas Body -->
                <div class="my-6 space-y-6">
                    <!-- QLĐT Block -->
                    <div id="drawerQldtBlock">
                        <h4 class="text-sm font-bold text-rose-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                            <i class="fa-solid fa-graduation-cap"></i> Vi phạm Đào tạo (QLĐT)
                        </h4>
                        <div class="space-y-3 max-h-60 overflow-y-auto" id="drawerQldtList">
                            <!-- Dynamic QLĐT details -->
                        </div>
                    </div>

                    <!-- Worklane Block -->
                    <div id="drawerWlBlock">
                        <h4 class="text-sm font-bold text-blue-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                            <i class="fa-solid fa-square-poll-horizontal"></i> Vi phạm Công việc (Worklane)
                        </h4>
                        <div class="space-y-3 max-h-60 overflow-y-auto" id="drawerWlList">
                            <!-- Dynamic Worklane details -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- Email Generator Inside Drawer -->
            <div class="border-t border-white/5 pt-6 bg-[#0f172a]/95 sticky bottom-0">
                <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                    <i class="fa-solid fa-envelope-open-text text-amber-500"></i> Nhắc nhở lỗi (Email Generator)
                </h4>
                <button onclick="triggerEmail()" class="w-full py-3.5 bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 font-bold rounded-xl transition-all border border-rose-500/20 text-xs flex items-center justify-center gap-2">
                    <i class="fa-solid fa-paper-plane"></i> Soạn Email nhắc nhở gộp chung
                </button>
            </div>
        </div>
    </div>

    <!-- Email Modal -->
    <div id="emailModal" class="opacity-0 pointer-events-none fixed w-full h-full top-0 left-0 flex items-center justify-center z-50 transition-opacity duration-200">
        <div class="absolute w-full h-full bg-slate-950/80" onclick="closeEmailModal()"></div>
        <div class="bg-[#0f172a] border border-white/10 w-11/12 md:max-w-3xl mx-auto rounded-3xl shadow-2xl z-50 overflow-y-auto max-h-[90vh]">
            <div class="py-6 text-left px-6">
                <div class="flex justify-between items-center pb-4 border-b border-white/5">
                    <h3 class="text-xl font-bold text-slate-100 flex items-center gap-2">
                        <i class="fa-solid fa-envelope-open-text text-rose-500"></i> Trình soạn thư nhắc lỗi
                    </h3>
                    <div class="cursor-pointer p-2 bg-white/5 hover:bg-white/10 rounded-full transition-colors" onclick="closeEmailModal()">
                        <i class="fa-solid fa-xmark text-slate-400"></i>
                    </div>
                </div>
                <div class="my-6">
                    <div class="mb-4 bg-white/5 rounded-xl p-4 text-xs text-slate-300">
                        <div class="mb-1"><span class="font-bold text-slate-400">Người nhận:</span> <span id="modalEmailRecipient" class="font-semibold text-rose-400"></span></div>
                        <div class="mb-1 hidden" id="modalCcRow"><span class="font-bold text-slate-400">Đồng kính gửi (CC Leader):</span> <span id="modalEmailCC" class="font-semibold text-blue-400"></span></div>
                        <div><span class="font-bold text-slate-400">Tiêu đề:</span> <span id="modalEmailSubject" class="font-semibold text-slate-200"></span></div>
                    </div>
                    
                    <!-- Rich Text Preview Container (Nền trắng để PMO bôi đen copy-paste nguyên bảng Rich Text) -->
                    <div class="border border-slate-300 rounded-2xl p-6 bg-white text-slate-800 text-sm font-sans max-h-[45vh] overflow-y-auto select-all" id="emailText" contenteditable="true">
                        <!-- Pre-formatted email content with real HTML tables -->
                    </div>
                </div>
                <div class="flex justify-end gap-3 pt-4 border-t border-white/5">
                    <button onclick="copyEmailText()" class="px-5 py-2.5 bg-white/5 hover:bg-white/10 text-slate-200 font-bold rounded-xl transition-colors flex items-center gap-2">
                        <i class="fa-solid fa-copy"></i> Sao chép Rich Text
                    </button>
                    <a id="modalMailtoBtn" href="#" class="px-5 py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-xl transition-colors flex items-center gap-2">
                        <i class="fa-solid fa-paper-plane"></i> Gửi Mail qua Outlook
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- JS Logic -->
    <script>
        const rawViolations = {json_data_str};
        let activeInstructor = '';
        let displayList = [];
        
        window.onload = function() {{
            populateFilters();
            renderDashboard();
        }};

        function switchCycleTab(type) {{
            const tabWeek = document.getElementById("tabWeek");
            const tabMonth = document.getElementById("tabMonth");
            const cycleSelectType = document.getElementById("cycleType");
            
            if (type === 'weekly') {{
                tabWeek.className = "flex-1 py-3 text-center rounded-xl font-bold transition-all text-sm bg-rose-600 text-white shadow-lg";
                tabMonth.className = "flex-1 py-3 text-center rounded-xl font-bold transition-all text-sm text-slate-400 hover:text-slate-200";
                cycleSelectType.value = "weekly";
            }} else {{
                tabWeek.className = "flex-1 py-3 text-center rounded-xl font-bold transition-all text-sm text-slate-400 hover:text-slate-200";
                tabMonth.className = "flex-1 py-3 text-center rounded-xl font-bold transition-all text-sm bg-rose-600 text-white shadow-lg";
                cycleSelectType.value = "monthly";
            }}
            onCycleTypeChange();
        }}

        function populateFilters() {{
            const cycleType = document.getElementById("cycleType").value;
            const cycleSelect = document.getElementById("cycleValue");
            cycleSelect.innerHTML = "";

            if (cycleType === "weekly") {{
                const weekObjs = [];
                const seenWeeks = new Set();
                rawViolations.forEach(v => {{
                    if (v.week_label && !seenWeeks.has(v.week_label)) {{
                        seenWeeks.add(v.week_label);
                        weekObjs.push({{ label: v.week_label, monday: v.week_monday || '' }});
                    }}
                }});
                weekObjs.sort((a, b) => b.monday.localeCompare(a.monday));
                weekObjs.forEach(w => {{
                    cycleSelect.options.add(new Option(w.label, w.label));
                }});
            }} else if (cycleType === "monthly") {{
                const months = [...new Set(rawViolations.map(v => v.month_label).filter(Boolean))].sort().reverse();
                months.forEach(m => {{
                    cycleSelect.options.add(new Option(m, m));
                }});
            }}
            
            document.getElementById("cycleValueContainer").style.display = (cycleType === "all") ? "none" : "block";
        }}

        function onCycleTypeChange() {{
            populateFilters();
            renderDashboard();
        }}

        function getGrade(score) {{
            if (score === 100) return {{ text: "Xuất sắc", class: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" }};
            if (score === 95) return {{ text: "Khá", class: "bg-blue-500/10 text-blue-400 border-blue-500/20" }};
            if (score === 85) return {{ text: "Trung bình", class: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20" }};
            return {{ text: "Yếu", class: "bg-rose-500/10 text-rose-400 border-rose-500/20" }};
        }}

        function removeAccents(str) {{
            if (!str) return "";
            str = str.toString();
            const s1 = "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẬặẸẹẺẻẼẽẾếỀềỂểỄễỆệỊịỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỶỷỸỹỸỳ";
            const s2 = "AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy";
            let s = "";
            for (let i = 0; i < str.length; i++) {{
                const c = str.charAt(i);
                const idx = s1.indexOf(c);
                s += (idx !== -1) ? s2.charAt(idx) : c;
            }}
            return s.toLowerCase().trim().replace(/\\s+/g, ' ');
        }}

        function generateHeuristicsEmail(name) {{
            const nameClean = removeAccents(name);
            const words = nameClean.split(" ");
            if (words.length >= 2) {{
                const ten = words[words.length - 1];
                let hoLot = "";
                for (let i = 0; i < words.length - 1; i++) {{
                    hoLot += words[i].charAt(0);
                }}
                return ten + hoLot + "@rikkei.edu.vn";
            }}
            return nameClean.replace(/\\s+/g, '') + "@rikkei.edu.vn";
        }}

        const teacherCcMap = {{
            // HCM
            "Nguyễn Bá Minh Đạo": "daonbm@rikkeiacademy.net",
            "Lê Hà Thanh Sang": "daonbm@rikkeiacademy.net",
            "Trần Quốc Tuấn": "daonbm@rikkeiacademy.net",
            "Nguyễn Đức Minh": "daonbm@rikkeiacademy.net",
            "Đặng Minh Luân": "daonbm@rikkeiacademy.net",
            "Lưu Hoàng Xuân Nguyên": "daonbm@rikkeiacademy.net",
            "Phan Ngọc Tài": "daonbm@rikkeiacademy.net",
            "Nguyễn Ngọc Sơn": "daonbm@rikkeiacademy.net",
            "Phạm Viết Hùng": "daonbm@rikkeiacademy.net",
            
            // HN-NT
            "Hồ Xuân Hùng": "hunghx@rikkei.edu.vn",
            "Lâm Tùng Dương": "hunghx@rikkei.edu.vn",
            "Lương Quốc Tuấn": "hunghx@rikkei.edu.vn",
            "Ngọ Văn Quý": "hunghx@rikkei.edu.vn",
            "Nguyễn Quảng An": "hunghx@rikkei.edu.vn",
            "Lại Trung Lâm": "hunghx@rikkei.edu.vn",
            "Phạm Ngọc Kiên": "hunghx@rikkei.edu.vn",
            
            // HN-HPC
            "Trịnh Quốc Hai": "haitq@rikkeiacademy.com",
            "Bùi Thanh Hải": "haitq@rikkeiacademy.com",
            "Nguyễn Xuân Bách": "haitq@rikkeiacademy.com",
            "Phạm Tuấn Bình": "haitq@rikkeiacademy.com",
            "Nguyễn Công Hưởng": "haitq@rikkeiacademy.com",
            "Đinh Thành Nam": "haitq@rikkeiacademy.com",
            "Mai Xuân Chinh": "haitq@rikkeiacademy.com"
        }};

        function getLeaderCC(teacherName, groupName) {{
            if (teacherCcMap[teacherName]) {{
                return teacherCcMap[teacherName];
            }}
            if (groupName === "Khối QLCLĐT" || groupName === "Khối QLCDT") return "tuoint@rikkei.edu.vn";
            if (groupName === "Khối Ngoại ngữ tiếng Nhật") return "hanggtm@rikkeieducation.com";
            if (groupName === "Khối Ngoại ngữ tiếng Anh") return "anhltn1@rikkeiacademy.net";
            if (groupName === "Khối QTKD") return "oanhhtk@rikkeieducation.top";
            return "";
        }}

        function updateTrendChart() {{
            const cycleType = document.getElementById("cycleType").value;
            const trendData = {{}};
            
            rawViolations.forEach(v => {{
                const key = cycleType === 'weekly' ? v.week_label : v.month_label;
                const sortKey = cycleType === 'weekly' ? v.week_monday : v.month_label;
                if (key && sortKey) {{
                    if (!trendData[key]) {{
                        trendData[key] = {{ label: key, sortKey: sortKey, count: 0 }};
                    }}
                    trendData[key].count += 1;
                }}
            }});
            
            const sortedTrends = Object.values(trendData).sort((a, b) => a.sortKey.localeCompare(b.sortKey));
            const labels = sortedTrends.map(t => t.label.replace('Tuần ', 'W'));
            const dataPoints = sortedTrends.map(t => t.count);

            if (window.trendChart) {{
                window.trendChart.destroy();
            }}

            const ctx = document.getElementById('trendChartCanvas').getContext('2d');
            window.trendChart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: 'Số vi phạm của khối',
                        data: dataPoints,
                        borderColor: '#f43f5e',
                        backgroundColor: 'rgba(244, 63, 94, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        pointBackgroundColor: '#f43f5e',
                        pointRadius: 4,
                        fill: true
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            backgroundColor: '#1e293b',
                            titleColor: '#f8fafc',
                            bodyColor: '#cbd5e1',
                            borderColor: 'rgba(255,255,255,0.08)',
                            borderWidth: 1
                        }}
                    }},
                    scales: {{
                        x: {{
                            grid: {{ display: false }},
                            ticks: {{ color: '#94a3b8', font: {{ family: 'Plus Jakarta Sans', size: 9 }} }}
                        }},
                        y: {{
                            grid: {{ color: 'rgba(255,255,255,0.05)' }},
                            ticks: {{ color: '#94a3b8', font: {{ family: 'Plus Jakarta Sans', size: 9 }}, stepSize: 2 }}
                        }}
                    }}
                }}
            }});
        }}

        function renderDashboard() {{
            const cycleType = document.getElementById("cycleType").value;
            const cycleValue = document.getElementById("cycleValue").value;
            const roleFilter = document.getElementById("roleFilter").value;
            const searchVal = document.getElementById("searchPersonnel").value.toLowerCase().trim();

            let filtered = rawViolations;
            if (cycleType === "weekly" && cycleValue) {{
                filtered = filtered.filter(v => v.week_label === cycleValue);
            }} else if (cycleType === "monthly" && cycleValue) {{
                filtered = filtered.filter(v => v.month_label === cycleValue);
            }}

            if (roleFilter !== "all") {{
                filtered = filtered.filter(v => v.Role === roleFilter);
            }}

            updateTrendChart();

            // 2. Overview KPI Cards
            const totalErrors = filtered.length;
            const qldtErrors = filtered.filter(v => v.Category === 'QLDT').length;
            const dailyMisses = filtered.filter(v => v.Error.includes('DAILY')).length;
            const taskOvs = filtered.filter(v => v.Error.includes('TASK')).length;

            const statsContainer = document.getElementById("statsContainer");
            statsContainer.innerHTML = `
                <div class="card-dark p-6 flex justify-between items-center">
                    <div>
                        <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Tổng vi phạm tác nghiệp</div>
                        <div class="text-2xl font-black text-rose-500">${{totalErrors}} lỗi</div>
                    </div>
                    <i class="fa-solid fa-triangle-exclamation text-3xl text-rose-500/25"></i>
                </div>
                <div class="card-dark p-6 flex justify-between items-center">
                    <div>
                        <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Lỗi đào tạo (QLĐT)</div>
                        <div class="text-2xl font-black text-blue-400">${{qldtErrors}} ca</div>
                    </div>
                    <i class="fa-solid fa-graduation-cap text-3xl text-blue-500/25"></i>
                </div>
                <div class="card-dark p-6 flex justify-between items-center">
                    <div>
                        <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Quên nộp báo cáo ngày</div>
                        <div class="text-2xl font-black text-amber-500">${{dailyMisses}} lần</div>
                    </div>
                    <i class="fa-solid fa-calendar-day text-3xl text-amber-500/25"></i>
                </div>
            `;

            // Gom nhóm thống kê theo từng nhân sự
            const summary = {{}};
            filtered.forEach(v => {{
                const name = v.Instructor;
                if (!summary[name]) {{
                    summary[name] = {{
                        name: name,
                        role: v.Role,
                        rank: v.Rank || 'N/A',
                        email: v.Email || '',
                        group: v.Group || 'Khối HN-CNTT',
                        qldtCount: 0,
                        missCount: 0,
                        overdueCount: 0,
                        qldtList: [],
                        missList: [],
                        overdueList: [],
                        totalErrors: 0,
                        score: 100
                    }};
                }}
                
                const s = summary[name];
                if (v.Category === 'QLDT') {{
                    s.qldtCount += 1;
                    s.qldtList.push(v);
                }} else if (v.Error === 'WL-DAILY-LOG-MISSING') {{
                    s.missCount += 1;
                    s.missList.push(v);
                }} else if (v.Error === 'WL-TASK-OVERDUE') {{
                    s.overdueCount += 1;
                    s.overdueList.push(v);
                }}
                s.totalErrors += 1;
            }});

            const summaryList = Object.values(summary).map(item => {{
                let score = 100;
                if (item.totalErrors === 1) score = 100;
                else if (item.totalErrors === 2) score = 95;
                else if (item.totalErrors === 3) score = 85;
                else if (item.totalErrors >= 4) score = 70;
                item.score = score;
                return item;
            }});

            displayList = summaryList.filter(item => {{
                if (searchVal && !item.name.toLowerCase().includes(searchVal)) return false;
                if (roleFilter !== "all" && item.role !== roleFilter) return false;
                return true;
            }});

            // 3. Render Top 5 song song
            const goodBody = document.getElementById("topGoodBody");
            const badBody = document.getElementById("topBadBody");
            goodBody.innerHTML = "";
            badBody.innerHTML = "";

            const goodList = [...displayList].sort((a, b) => a.totalErrors - b.totalErrors).slice(0, 5);
            const badList = [...displayList].sort((a, b) => b.totalErrors - a.totalErrors).slice(0, 5);

            function renderTopRows(list, container) {{
                if (list.length === 0) {{
                    container.innerHTML = `<tr><td colspan="5" class="px-4 py-8 text-center text-slate-500">Không có dữ liệu</td></tr>`;
                    return;
                }}
                list.forEach(item => {{
                    const grade = getGrade(item.score);
                    const roleBadge = item.role === "GV" ? 
                        '<span class="px-1.5 py-0.5 text-[9px] font-bold rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 ml-2">GV</span>' : 
                        '<span class="px-1.5 py-0.5 text-[9px] font-bold rounded bg-purple-500/10 text-purple-400 border border-purple-500/20 ml-2">TG</span>';
                    
                    let qldtCell = `<span class="text-slate-500">0 lỗi</span>`;
                    let missCell = `<span class="text-slate-500">0 lần</span>`;
                    let overdueCell = `<span class="text-slate-500">0 task</span>`;

                    if (item.qldtList.length > 0) qldtCell = `<span class="text-rose-400 font-bold">${{item.qldtList.length}} lỗi</span>`;
                    if (item.missList.length > 0) missCell = `<span class="text-rose-400 font-bold">${{item.missList.length}} lần</span>`;
                    if (item.overdueList.length > 0) overdueCell = `<span class="text-blue-400 font-bold">${{item.overdueList.length}} task</span>`;

                    container.innerHTML += `
                        <tr class="hover:bg-white/5 transition-colors border-b border-white/5 cursor-pointer" onclick="openOffcanvas('${{item.name}}')">
                            <td class="px-4 py-3 font-bold text-slate-200 flex items-center">${{item.name}} ${{roleBadge}}</td>
                            <td class="px-4 py-3 text-center">${{qldtCell}}</td>
                            <td class="px-4 py-3 text-center">${{missCell}}</td>
                            <td class="px-4 py-3 text-center">${{overdueCell}}</td>
                            <td class="px-4 py-3 text-center">
                                <span class="px-2 py-0.5 text-[10px] font-bold rounded-full border ${{grade.class}}">${{item.score}}đ</span>
                            </td>
                        </tr>
                    `;
                }});
            }}
            renderTopRows(goodList, goodBody);
            renderTopRows(badList, badBody);

            // 4. Render Bảng thống kê theo Cơ sở & Khối (Grouped Tables)
            const mainContainer = document.getElementById("groupedComplianceTablesContainer");
            mainContainer.innerHTML = "";

            const groupsConfig = [
                {{
                    key: "CNTT_HCM",
                    title: "1. Khối CNTT - HCM",
                    leader: "Thầy Nguyễn Bá Minh Đạo",
                    matchFn: (g) => g === "Khối HCM-CNTT"
                }},
                {{
                    key: "CNTT_NT",
                    title: "2. Khối CNTT - Ngọc Trục",
                    leader: "Thầy Hồ Xuân Hùng",
                    matchFn: (g) => g === "Khối HN-CNTT Ngọc Trục"
                }},
                {{
                    key: "CNTT_HPC",
                    title: "3. Khối CNTT - HPC",
                    leader: "Thầy Trịnh Quốc Hai",
                    matchFn: (g) => g === "Khối HN-CNTT HPC"
                }},
                {{
                    key: "QTKD",
                    title: "4. Khối QTKD",
                    leader: "Cô Hoàng Thị Kim Oanh",
                    matchFn: (g) => g === "Khối QTKD"
                }},
                {{
                    key: "NGOAI_NGU",
                    title: "5. Khối Ngoại ngữ và Kỹ năng mềm",
                    leader: "Cô Giáp Thị Minh Hằng / Lò Thị Ngọc Anh",
                    matchFn: (g) => g.includes("Ngoại ngữ")
                }},
                {{
                    key: "QLCLDT",
                    title: "6. Khối QLCLĐT",
                    leader: "Cô Nguyễn Thị Tươi",
                    matchFn: (g) => g.includes("QLCL") || g.includes("QLCDT")
                }}
            ];

            groupsConfig.forEach(group => {{
                const members = displayList.filter(item => group.matchFn(item.group));
                const violators = members.filter(item => item.totalErrors > 0);
                
                // Nút soạn email cho nhóm
                let emailBtnHtml = "";
                if (violators.length > 0) {{
                    const groupTitleClean = group.title.split('. ')[1];
                    emailBtnHtml = `
                        <button onclick="openBranchEmailModal('${{group.key}}')" class="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-xl transition-all text-xs flex items-center gap-1.5 border border-rose-500/20 shadow-md">
                            <i class="fa-solid fa-envelope-open-text"></i> Soạn Email vi phạm ${{groupTitleClean}}
                        </button>
                    `;
                }} else {{
                    emailBtnHtml = `
                        <span class="px-3 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-xl text-xs font-bold flex items-center gap-1">
                            <i class="fa-solid fa-circle-check"></i> Khối không có vi phạm
                        </span>
                    `;
                }}

                let tableRowsHtml = "";
                if (members.length === 0) {{
                    tableRowsHtml = `
                        <tr>
                            <td colspan="9" class="px-6 py-6 text-center text-slate-500 text-xs">
                                Không có nhân sự nào thuộc khối này trong chu kỳ hiện tại.
                            </td>
                        </tr>
                    `;
                }} else {{
                    members.sort((a, b) => b.totalErrors - a.totalErrors).forEach(item => {{
                        const roleBadge = item.role === "GV" ? 
                            '<span class="px-2 py-0.5 text-[10px] font-bold rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">Giảng viên</span>' : 
                            '<span class="px-2 py-0.5 text-[10px] font-bold rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">Trợ giảng</span>';
                        
                        const grade = getGrade(item.score);
                        const actionBtn = `<button onclick="openOffcanvas('${{item.name}}')" class="px-3 py-1.5 bg-white/5 hover:bg-rose-500/15 text-slate-300 hover:text-rose-400 border border-white/5 rounded-xl transition-all text-xs font-bold flex items-center gap-1.5"><i class="fa-solid fa-eye"></i> Chi tiết</button>`;
                        const emailBtn = `<button onclick="openEmailModal('${{item.name}}')" class="p-2 bg-white/5 hover:bg-rose-500/15 text-slate-300 hover:text-rose-400 border border-white/5 rounded-xl transition-all" title="Soạn email cá nhân"><i class="fa-solid fa-envelope"></i></button>`;

                        let qldtCell = `<span class="text-slate-500">0 lỗi</span>`;
                        let missCell = `<span class="text-slate-500">0 lần</span>`;
                        let overdueCell = `<span class="text-slate-500">0 task</span>`;

                        if (item.qldtCount > 0) qldtCell = `<span class="text-rose-400 font-bold">${{item.qldtCount}} lỗi</span>`;
                        if (item.missCount > 0) missCell = `<span class="text-rose-400 font-bold">${{item.missCount}} lần</span>`;
                        if (item.overdueCount > 0) overdueCell = `<span class="text-blue-400 font-bold">${{item.overdueCount}} task</span>`;

                        tableRowsHtml += `
                            <tr class="hover:bg-white/5 transition-colors border-b border-white/5 cursor-pointer" onclick="openOffcanvas('${{item.name}}')">
                                <td class="px-6 py-4 font-bold text-slate-200 text-base">${{item.name}}</td>
                                <td class="px-6 py-4 text-center">${{roleBadge}}</td>
                                <td class="px-6 py-4 text-center font-semibold text-slate-400">Rank ${{item.rank}}</td>
                                <td class="px-6 py-4 text-center">${{qldtCell}}</td>
                                <td class="px-6 py-4 text-center">${{missCell}}</td>
                                <td class="px-6 py-4 text-center">${{overdueCell}}</td>
                                <td class="px-6 py-4 text-center font-mono font-black text-rose-500 text-lg">${{item.totalErrors}} vi phạm</td>
                                <td class="px-6 py-4 text-center">
                                    <span class="px-2.5 py-1 text-xs font-bold rounded-full border ${{grade.class}}">${{item.score}}đ</span>
                                </td>
                                <td class="px-6 py-4 flex justify-center gap-2" onclick="event.stopPropagation()">
                                    ${{actionBtn}}
                                    ${{emailBtn}}
                                </td>
                            </tr>
                        `;
                    }});
                }}

                mainContainer.innerHTML += `
                    <div class="card-dark overflow-hidden border border-white/5 shadow-xl">
                        <div class="p-6 border-b border-white/5 flex flex-wrap items-center justify-between gap-4 bg-gradient-to-r from-slate-900/50 to-slate-900/20">
                            <div class="flex items-center gap-3">
                                <i class="fa-solid fa-hotel text-blue-400 text-lg"></i>
                                <div>
                                    <h3 class="font-bold text-slate-100 text-base">${{group.title}}</h3>
                                    <span class="text-xs text-slate-400 font-medium">Người quản lý: <strong class="text-slate-300">${{group.leader}}</strong></span>
                                </div>
                            </div>
                            <div>
                                ${{emailBtnHtml}}
                            </div>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left border-collapse text-sm">
                                <thead>
                                    <tr class="bg-white/5 text-slate-400 font-bold text-xs uppercase border-b border-white/5">
                                        <th class="px-6 py-4">Nhân sự</th>
                                        <th class="px-6 py-4 text-center">Vai trò</th>
                                        <th class="px-6 py-4 text-center">Rank</th>
                                        <th class="px-6 py-4 text-center">Lỗi QLĐT</th>
                                        <th class="px-6 py-4 text-center">BC ngày</th>
                                        <th class="px-6 py-4 text-center">Task trễ</th>
                                        <th class="px-6 py-4 text-center">Tổng vi phạm</th>
                                        <th class="px-6 py-4 text-center">Điểm</th>
                                        <th class="px-6 py-4 text-center">Hành động</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-white/5">
                                    ${{tableRowsHtml}}
                                </tbody>
                            </table>
                        </div>
                    </div>
                `;
            }});
        }}

        function openOffcanvas(name) {{
            activeInstructor = name;
            const cycleType = document.getElementById("cycleType").value;
            const cycleValue = document.getElementById("cycleValue").value;
            
            let filtered = rawViolations.filter(v => v.Instructor === name);
            if (cycleType === "weekly" && cycleValue) {{
                filtered = filtered.filter(v => v.week_label === cycleValue);
            }} else if (cycleType === "monthly" && cycleValue) {{
                filtered = filtered.filter(v => v.month_label === cycleValue);
            }}

            const role = filtered.length > 0 ? filtered[0].Role : 'N/A';
            const rank = filtered.length > 0 ? (filtered[0].Rank || 'N/A') : 'N/A';
            const roleText = role === "GV" ? "Giảng viên" : (role === "TG" ? "Trợ giảng" : "GV/TG");

            document.getElementById("drawerTitle").innerHTML = `<i class="fa-solid fa-address-card text-rose-500"></i> ${{name}}`;
            document.getElementById("drawerSubtitle").innerText = `${{roleText}} - Rank ${{rank}}`;

            // QLĐT List
            const qldtList = document.getElementById("drawerQldtList");
            const qldtBlock = document.getElementById("drawerQldtBlock");
            qldtList.innerHTML = "";
            
            const qldtViolations = filtered.filter(v => v.Category === 'QLDT');
            if (qldtViolations.length === 0) {{
                qldtBlock.classList.add("hidden");
            }} else {{
                qldtBlock.classList.remove("hidden");
                qldtViolations.forEach(v => {{
                    qldtList.innerHTML += `
                        <div class="p-3 bg-white/5 rounded-xl border border-white/5 text-xs">
                            <div class="flex justify-between font-bold text-slate-200 mb-1">
                                <span class="text-rose-400">${{v.Session}} (${{v.Course}})</span>
                                <span class="font-mono text-slate-400">${{v.Date}}</span>
                            </div>
                            <div class="text-slate-400 mb-1">Lớp: ${{v.Class}} | Ca: ${{v.Ca}}</div>
                            <div class="text-slate-300 font-semibold mb-1">${{v.SessionName}}</div>
                            <div class="text-rose-300 font-medium">${{v.Details}}</div>
                        </div>
                    `;
                }});
            }}

            // Worklane List
            const wlList = document.getElementById("drawerWlList");
            const wlBlock = document.getElementById("drawerWlBlock");
            wlList.innerHTML = "";
            
            const wlViolations = filtered.filter(v => v.Category === 'WORKLANE');
            if (wlViolations.length === 0) {{
                wlBlock.classList.add("hidden");
            }} else {{
                wlBlock.classList.remove("hidden");
                wlViolations.forEach(v => {{
                    const badge = v.Error.includes('DAILY') ? 
                        '<span class="px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 text-[10px] font-bold">Báo cáo ngày</span>' : 
                        '<span class="px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 text-[10px] font-bold">Task trễ</span>';
                    
                    wlList.innerHTML += `
                        <div class="p-3 bg-white/5 rounded-xl border border-white/5 text-xs">
                            <div class="flex justify-between items-center font-bold text-slate-200 mb-1">
                                ${{badge}}
                                <span class="font-mono text-slate-400">${{v.Date}}</span>
                            </div>
                            <div class="text-slate-300 mb-1">Nguồn/Dự án: ${{v.Class}}</div>
                            <div class="text-slate-300 font-semibold mb-1">${{v.SessionName}}</div>
                            <div class="text-blue-300 font-medium">${{v.Details}}</div>
                        </div>
                    `;
                }});
            }}

            document.getElementById("offcanvasOverlay").classList.remove("hidden");
            document.getElementById("offcanvasRight").classList.add("open");
        }}

        function closeOffcanvas() {{
            document.getElementById("offcanvasOverlay").classList.add("hidden");
            document.getElementById("offcanvasRight").classList.remove("open");
        }}

        function triggerEmail() {{
            openEmailModal(activeInstructor);
        }}

        function openEmailModal(name) {{
            const cycleType = document.getElementById("cycleType").value;
            const cycleValue = document.getElementById("cycleValue").value;
            
            let filtered = rawViolations.filter(v => v.Instructor === name);
            if (cycleType === "weekly" && cycleValue) {{
                filtered = filtered.filter(v => v.week_label === cycleValue);
            }} else if (cycleType === "monthly" && cycleValue) {{
                filtered = filtered.filter(v => v.month_label === cycleValue);
            }}

            if (filtered.length === 0) return;

            const role = filtered[0].Role;
            const roleText = role === "GV" ? "Giảng viên" : "Trợ giảng";
            const timeLabel = cycleType === "weekly" ? `Tuần ${{cycleValue}}` : `Tháng ${{cycleValue}}`;
            
            const email = filtered[0].Email || generateHeuristicsEmail(name);
            const group = filtered[0].Group || 'Khối HN-CNTT';
            const ccEmail = "";
            
            const count = filtered.length;

            const recipient = `${{roleText}} ${{name}}`;
            const subject = `[PMO] Thông báo vi phạm tác nghiệp (QLĐT & Worklane) - ${{timeLabel}} - ${{roleText}} ${{name}}`;

            const wlViolations = filtered.filter(v => v.Category === "WORKLANE");
            const qldtViolations = filtered.filter(v => v.Category === "QLDT");

            // 1. TẠO BẢNG RICH TEXT HTML ĐỂ COPY-PASTE DỄ DÀNG
            let htmlTable = `<table style="width:100%; border-collapse:collapse; margin:15px 0; font-family:sans-serif; font-size:13px; color:#1e293b;">
                <thead>
                    <tr style="background-color:#f1f5f9; border-bottom:2px solid #cbd5e1; text-align:left;">
                        <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold;">Hệ thống</th>
                        <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold;">Lớp / Dự án</th>
                        <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold;">Buổi / Đầu việc</th>
                        <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold;">Nội dung lỗi vi phạm</th>
                        <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold; text-align:center;">Ngày</th>
                    </tr>
                </thead>
                <tbody>`;

            qldtViolations.forEach(v => {{
                htmlTable += `<tr style="border-bottom:1px solid #e2e8f0;">
                    <td style="padding:10px; border:1px solid #e2e8f0; font-weight:bold; color:#e11d48;">QLĐT</td>
                    <td style="padding:10px; border:1px solid #e2e8f0;">${{v.Class}}</td>
                    <td style="padding:10px; border:1px solid #e2e8f0;">${{v.Session}} (${{v.SessionName}})</td>
                    <td style="padding:10px; border:1px solid #e2e8f0; color:#475569;">${{v.Details}}</td>
                    <td style="padding:10px; border:1px solid #e2e8f0; text-align:center; font-family:monospace;">${{v.Date}}</td>
                </tr>`;
            }});

            wlViolations.forEach(v => {{
                htmlTable += `<tr style="border-bottom:1px solid #e2e8f0;">
                    <td style="padding:10px; border:1px solid #e2e8f0; font-weight:bold; color:#2563eb;">Worklane</td>
                    <td style="padding:10px; border:1px solid #e2e8f0;">${{v.Class}}</td>
                    <td style="padding:10px; border:1px solid #e2e8f0;">${{v.SessionName}}</td>
                    <td style="padding:10px; border:1px solid #e2e8f0; color:#475569;">${{v.Details}}</td>
                    <td style="padding:10px; border:1px solid #e2e8f0; text-align:center; font-family:monospace;">${{v.Date}}</td>
                </tr>`;
            }});
            htmlTable += `</tbody></table>`;

            // 2. BẢNG TEXT MARKDOWN CHO MAILTO LINK (KHÔNG VỠ CHỮ)
            let mdTable = "";
            qldtViolations.forEach(v => {{
                mdTable += `[QLĐT] Lớp ${{v.Class}}, ${{v.Session}}: ${{v.Details}} (${{v.Date}})\\n`;
            }});
            wlViolations.forEach(v => {{
                mdTable += `[Worklane] Dự án ${{v.Class}}: ${{v.Details}} (${{v.Date}})\\n`;
            }});

            // Nội dung Rich Text hiển thị trong Modal (dễ bôi đen copy nguyên định dạng)
            const richTextBody = `<div style="font-family:sans-serif; color:#1e293b; line-height:1.6;">
                <p>Kính gửi ${{roleText}} <strong>${{name}}</strong>,</p>
                <p>Phòng QLCL Đào tạo gửi Thầy/Cô thông tin vi phạm kỷ luật tác nghiệp ghi nhận được trên hệ thống QLĐT và Worklane PM trong <strong>${{timeLabel}}</strong>:</p>
                <p><strong>Danh sách chi tiết vi phạm:</strong></p>
                ${{htmlTable}}
                <p>Tổng số lỗi vi phạm: <strong style="color:#e11d48;">${{count}} lỗi</strong>.</p>
                <p style="background-color:#fffbeb; border-left:4px solid #f59e0b; padding:10px; font-weight:bold; color:#b45309;">
                    ⚠️ Kính đề nghị Thầy/Cô giải trình và phản hồi trong 2 ngày kể từ khi nhận email.
                </p>
                <br>
                <p>Trân trọng,</p>
                <p><strong>Phòng QLCL Đào tạo</strong></p>
            </div>`;

            // Plain text cho mailto link (không lỗi format)
            const plainTextBody = `Kính gửi ${{roleText}} ${{name}},\\n\\nPhòng QLCL Đào tạo gửi Thầy/Cô thông tin vi phạm kỷ luật tác nghiệp ghi nhận được trên hệ thống QLĐT và Worklane PM trong ${{timeLabel}}:\\n\\nChi tiết vi phạm:\\n${{mdTable}}\\nTổng số lỗi vi phạm: ${{count}} lỗi.\\n\\nKính đề nghị Thầy/Cô giải trình và phản hồi trong 2 ngày kể từ khi nhận email.\\n\\nTrân trọng,\\nPhòng QLCL Đào tạo`;

            document.getElementById("modalEmailRecipient").innerText = recipient + " <" + email + ">";
            
            if (ccEmail) {{
                document.getElementById("modalCcRow").classList.remove("hidden");
                document.getElementById("modalEmailCC").innerText = ccEmail;
            }} else {{
                document.getElementById("modalCcRow").classList.add("hidden");
            }}
            
            // Render HTML trực tiếp vào khung email để PMO copy bảng biểu
            document.getElementById("emailText").innerHTML = richTextBody;
            
            let mailtoUrl = `mailto:${{email}}?subject=${{encodeURIComponent(subject)}}&body=${{encodeURIComponent(plainTextBody.replace(/\\\\n/g, '\\n'))}}`;
            if (ccEmail) {{
                mailtoUrl = `mailto:${{email}}?cc=${{ccEmail}}&subject=${{encodeURIComponent(subject)}}&body=${{encodeURIComponent(plainTextBody.replace(/\\\\n/g, '\\n'))}}`;
            }}
            document.getElementById("modalMailtoBtn").href = mailtoUrl;

            const modal = document.getElementById("emailModal");
            modal.classList.remove('opacity-0');
            modal.classList.remove('pointer-events-none');
        }}

        function openBranchEmailModal(branchKey) {{
            const cycleType = document.getElementById("cycleType").value;
            const cycleValue = document.getElementById("cycleValue").value;
            const timeLabel = cycleType === "weekly" ? `Tuần ${{cycleValue}}` : (cycleType === "monthly" ? `Tháng ${{cycleValue}}` : "Tất cả thời gian");
            
            let branchName = "";
            let leaderName = "";
            let leaderEmail = "";
            let matchFn = null;
            
            if (branchKey === "CNTT_HCM") {{
                branchName = "Khối CNTT - HCM";
                leaderName = "Thầy Nguyễn Bá Minh Đạo";
                leaderEmail = "daonbm@rikkeiacademy.net";
                matchFn = (g) => g === "Khối HCM-CNTT";
            }} else if (branchKey === "CNTT_NT") {{
                branchName = "Khối CNTT - Ngọc Trục";
                leaderName = "Thầy Hồ Xuân Hùng";
                leaderEmail = "hunghx@rikkei.edu.vn";
                matchFn = (g) => g === "Khối HN-CNTT Ngọc Trục";
            }} else if (branchKey === "CNTT_HPC") {{
                branchName = "Khối CNTT - HPC";
                leaderName = "Thầy Trịnh Quốc Hai";
                leaderEmail = "haitq@rikkeiacademy.com";
                matchFn = (g) => g === "Khối HN-CNTT HPC";
            }} else if (branchKey === "QTKD") {{
                branchName = "Khối QTKD";
                leaderName = "Cô Hoàng Thị Kim Oanh";
                leaderEmail = "oanhhtk@rikkeieducation.top";
                matchFn = (g) => g === "Khối QTKD";
            }} else if (branchKey === "NGOAI_NGU") {{
                branchName = "Khối Ngoại ngữ";
                leaderName = "Cô Giáp Thị Minh Hằng / Lò Thị Ngọc Anh";
                leaderEmail = "hanggtm@rikkeieducation.com, anhltn1@rikkeiacademy.net";
                matchFn = (g) => g.includes("Ngoại ngữ");
            }} else if (branchKey === "QLCLDT") {{
                branchName = "Khối QLCLĐT";
                leaderName = "Cô Nguyễn Thị Tươi";
                leaderEmail = "tuoint@rikkei.edu.vn";
                matchFn = (g) => g.includes("QLCL") || g.includes("QLCDT");
            }}
            
            // Lọc ra các nhân sự thuộc khối này và có lỗi (totalErrors > 0), loại bỏ các leader khỏi danh sách vi phạm
            const leaderNames = ["Nguyễn Bá Minh Đạo", "Hồ Xuân Hùng", "Trịnh Quốc Hai", "Hoàng Thị Kim Oanh", "Giáp Thị Minh Hằng", "Lò Thị Ngọc Anh", "Nguyễn Thị Tươi"];
            const branchMembers = displayList.filter(item => matchFn(item.group) && item.totalErrors > 0 && !leaderNames.includes(item.name));
            
            if (branchMembers.length === 0) {{
                alert(`Không có nhân sự nào có vi phạm trong ${{branchName}} thuộc ${{timeLabel}}.`);
                return;
            }}
            
            let emails = branchMembers.map(m => m.email || generateHeuristicsEmail(m.name)).filter(Boolean);
            const recipient = emails.join(", ");
            const ccEmail = "";
            const subject = `[PMO] Thông báo vi phạm tác nghiệp - ${{branchName}} - ${{timeLabel}}`;
            
            // Xây dựng danh sách văn bản và bảng HTML
            let plainTextList = "";
            let htmlRows = "";
            
            branchMembers.forEach(item => {{
                const gradeText = item.score === 100 ? "Xuất sắc" : (item.score === 95 ? "Khá" : (item.score === 85 ? "Trung bình" : "🚨 Cảnh báo"));
                plainTextList += `- ${{item.name}} (${{item.role}}): ${{item.qldtCount}} lỗi QLĐT, ${{item.missCount}} lần vắng BC ngày, ${{item.overdueCount}} task trễ. Điểm: ${{item.score}}/100 (${{gradeText}})\\n`;
                
                htmlRows += `<tr style="border-bottom:1px solid #e2e8f0;">
                    <td style="padding:10px; border:1px solid #e2e8f0; font-weight:bold;">${{item.name}}</td>
                    <td style="padding:10px; border:1px solid #e2e8f0; text-align:center;">${{item.role}}</td>
                    <td style="padding:10px; border:1px solid #e2e8f0; text-align:center; color:#e11d48; font-weight:bold;">${{item.qldtCount}}</td>
                    <td style="padding:10px; border:1px solid #e2e8f0; text-align:center; color:#f59e0b; font-weight:bold;">${{item.missCount}}</td>
                    <td style="padding:10px; border:1px solid #e2e8f0; text-align:center; color:#3b82f6; font-weight:bold;">${{item.overdueCount}}</td>
                    <td style="padding:10px; border:1px solid #e2e8f0; text-align:center; font-weight:bold;">${{item.score}}/100</td>
                    <td style="padding:10px; border:1px solid #e2e8f0; text-align:center;">${{gradeText}}</td>
                </tr>`;
            }});
            
            // Chi tiết lỗi của từng người
            let detailsHtml = "<div style='margin-top:20px; border-top:1px solid #cbd5e1; pt-15px;'>";
            let detailsPlain = "\\n\\nChi tiết lỗi vi phạm:\\n";
            
            branchMembers.forEach(item => {{
                detailsHtml += `<h4 style="margin:10px 0 5px 0; color:#0f172a;">👤 ${{item.name}} (${{item.role}}):</h4>`;
                detailsHtml += `<ul style="margin:0; padding-left:20px; font-size:12px; color:#475569;">`;
                
                detailsPlain += `\\n* ${{item.name}} (${{item.role}}):\\n`;
                
                if (item.qldtList.length > 0) {{
                    item.qldtList.forEach(l => {{
                        detailsHtml += `<li>🔴 [QLĐT] Lớp ${{l.Class}}, Ca ${{l.Ca}}, ${{l.Date}}: ${{l.Details}}</li>`;
                        detailsPlain += `  - [QLĐT] Lớp ${{l.Class}}, Ca ${{l.Ca}}, ${{l.Date}}: ${{l.Details}}\\n`;
                    }});
                }}
                if (item.missList.length > 0) {{
                    item.missList.forEach(l => {{
                        detailsHtml += `<li>🟡 [BC ngày] Ngày ${{l.Date}}: ${{l.Details}}</li>`;
                        detailsPlain += `  - [BC ngày] Ngày ${{l.Date}}: ${{l.Details}}\\n`;
                    }});
                }}
                if (item.overdueList.length > 0) {{
                    item.overdueList.forEach(l => {{
                        detailsHtml += `<li>🔵 [Worklane] Task trễ hạn: ${{l.Details}}</li>`;
                        detailsPlain += `  - [Worklane] Task trễ hạn: ${{l.Details}}\\n`;
                    }});
                }}
                detailsHtml += `</ul>`;
            }});
            detailsHtml += "</div>";
            
            const richTextBody = `<div style="font-family:sans-serif; color:#1e293b; line-height:1.6;">
                <p>Kính gửi các Thầy/Cô ${{branchName}},</p>
                <p>Phòng QLCL Đào tạo gửi các Thầy/Cô bảng tổng hợp vi phạm tác nghiệp ghi nhận được trên hệ thống QLĐT và Worklane PM trong <strong>${{timeLabel}}</strong>:</p>
                
                <table style="width:100%; border-collapse:collapse; margin:15px 0; font-family:sans-serif; font-size:13px; color:#1e293b;">
                    <thead>
                        <tr style="background-color:#f8fafc; border-bottom:2px solid #cbd5e1; text-align:left;">
                            <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold;">Thầy/Cô</th>
                            <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold; text-align:center;">Vai trò</th>
                            <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold; text-align:center;">Lỗi QLĐT</th>
                            <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold; text-align:center;">BC ngày</th>
                            <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold; text-align:center;">Task trễ</th>
                            <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold; text-align:center;">Điểm</th>
                            <th style="padding:10px; border:1px solid #cbd5e1; font-weight:bold; text-align:center;">Xếp loại</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${{htmlRows}}
                    </tbody>
                </table>
                
                ${{detailsHtml}}
                
                <p><strong>Hành động yêu cầu:</strong></p>
                <p>1. Xem chi tiết các lỗi được liệt kê ở trên.</p>
                <p style="background-color:#fffbeb; border-left:4px solid #f59e0b; padding:10px; font-weight:bold; color:#b45309;">
                    ⚠️ Kính đề nghị các Thầy/Cô giải trình và phản hồi trong vòng 2 ngày kể từ khi nhận email này.
                </p>
                <p>Trân trọng,</p>
                <p><strong>Phòng QLCL Đào tạo</strong></p>
            </div>`;
            
            const plainTextBody = `Kính gửi các Thầy/Cô ${{branchName}},\\n\\nPhòng QLCL Đào tạo gửi các Thầy/Cô bảng tổng hợp vi phạm tác nghiệp trong ${{timeLabel}}:\\n\\n${{plainTextList}}${{detailsPlain}}\\nKính đề nghị các Thầy/Cô có tên trên thực hiện phản hồi giải trình trong vòng 2 ngày.\\n\\nTrân trọng,\\nPhòng QLCL Đào tạo`;
            
            document.getElementById("modalEmailRecipient").innerText = recipient;
            document.getElementById("modalCcRow").classList.add("hidden");
            document.getElementById("modalEmailCC").innerText = "";
            document.getElementById("modalEmailSubject").innerText = subject;
            document.getElementById("emailText").innerHTML = richTextBody;
            
            document.getElementById("modalMailtoBtn").href = `mailto:${{recipient}}?subject=${{encodeURIComponent(subject)}}&body=${{encodeURIComponent(plainTextBody.replace(/\\\\n/g, '\\n'))}}`;
            
            const modal = document.getElementById("emailModal");
            modal.classList.remove('opacity-0');
            modal.classList.remove('pointer-events-none');
        }}

        function openGroupEmailModal() {{
            const cycleType = document.getElementById("cycleType").value;
            const cycleValue = document.getElementById("cycleValue").value;
            const timeLabel = cycleType === "weekly" ? `Tuần ${{cycleValue}}` : (cycleType === "monthly" ? `Tháng ${{cycleValue}}` : "Tất cả thời gian");
            
            let mdTable = "| Họ và tên | Vai trò | Rank | Khối | Lỗi QLĐT | BC ngày | Task trễ | Điểm | Xếp loại |\\n| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- |\\n";
            
            displayList.forEach(item => {{
                const gradeText = item.score === 100 ? "Xuất sắc" : (item.score === 95 ? "Khá" : (item.score === 85 ? "Trung bình" : "🚨 Cảnh báo"));
                mdTable += `| **${{item.name}}** | ${{item.role}} | ${{item.rank}} | ${{item.group}} | ${{item.qldtCount}} | ${{item.missCount}} | ${{item.overdueCount}} | ${{item.score}}/100 | ${{gradeText}} |\\n`;
            }});
            
            const recipient = "teachers-daotao@rikkei.edu.vn";
            const subject = `[PMO] Bản tin Kỷ luật tác nghiệp Khối Đào tạo - ${{timeLabel}}`;
            
            const richTextBody = `<div style="font-family:sans-serif; color:#1e293b; line-height:1.6;">
                <p>Kính gửi các Thầy/Cô Khối Đào tạo,</p>
                <p>Phòng QLCL Đào tạo gửi các Thầy/Cô bảng xếp hạng kỷ luật tác nghiệp ghi nhận được trên hệ thống QLĐT và Worklane PM trong <strong>${{timeLabel}}</strong>:</p>
                <pre style="background-color:#f8fafc; border:1px solid #cbd5e1; padding:15px; font-family:monospace; font-size:12px; overflow-x:auto; border-radius:8px;">${{mdTable.replace(/\\\\n/g, '\\n')}}</pre>
                <p><strong>Hành động yêu cầu:</strong></p>
                <p>1. Tải tệp đính kèm <strong>"agent_3_ops_discipline.html"</strong> trong email này về máy tính, mở trực tiếp bằng trình duyệt để tra cứu chi tiết lỗi vi phạm cụ thể của mình (Thầy/Cô chỉ cần nhập tên vào ô tìm kiếm).</p>
                <p style="background-color:#fffbeb; border-left:4px solid #f59e0b; padding:10px; font-weight:bold; color:#b45309;">
                    ⚠️ Kính đề nghị Thầy/Cô giải trình và phản hồi trong 2 ngày kể từ khi nhận email.
                </p>
                <br>
                <p>Trân trọng,</p>
                <p><strong>Phòng QLCL Đào tạo</strong></p>
            </div>`;

            const plainTextBody = `Kính gửi các Thầy/Cô Khối Đào tạo,\\n\\nPhòng QLCL Đào tạo gửi các Thầy/Cô bảng xếp hạng kỷ luật tác nghiệp ghi nhận được trên hệ thống QLĐT và Worklane PM trong ${{timeLabel}}:\\n\\n${{mdTable}}\\nKính đề nghị các Thầy/Cô có tên trên thực hiện:\\n1. Tải tệp đính kèm "agent_3_ops_discipline.html" trong email này về máy tính, mở trực tiếp bằng trình duyệt để tra cứu chi tiết lỗi vi phạm cụ thể của mình (Thầy/Cô chỉ cần nhập tên vào ô tìm kiếm).\\n2. Tiến hành phản hồi giải trình trong vòng 2 ngày kể từ khi nhận email.\\n\\nTrân trọng,\\nPhòng QLCL Đào tạo`;

            document.getElementById("modalEmailRecipient").innerText = recipient;
            document.getElementById("modalCcRow").classList.add("hidden");
            document.getElementById("modalEmailSubject").innerText = subject;
            document.getElementById("emailText").innerHTML = richTextBody;
            
            document.getElementById("modalMailtoBtn").href = `mailto:${{recipient}}?subject=${{encodeURIComponent(subject)}}&body=${{encodeURIComponent(plainTextBody.replace(/\\\\n/g, '\\n'))}}`;

            const modal = document.getElementById("emailModal");
            modal.classList.remove('opacity-0');
            modal.classList.remove('pointer-events-none');
        }}

        function closeEmailModal() {{
            const modal = document.getElementById("emailModal");
            modal.classList.add('opacity-0');
            modal.classList.add('pointer-events-none');
        }}

        function copyEmailText() {{
            const emailDiv = document.getElementById('emailText');
            const html = emailDiv.innerHTML;
            const text = emailDiv.innerText;

            try {{
                const blobHtml = new Blob([html], {{ type: 'text/html' }});
                const blobText = new Blob([text], {{ type: 'text/plain' }});
                const data = [new ClipboardItem({{
                    'text/html': blobHtml,
                    'text/plain': blobText
                }})];

                navigator.clipboard.write(data).then(() => {{
                    alert('✓ Đã sao chép nội dung thư (bao gồm Bảng biểu Rich Text)! Bạn chỉ cần mở Lark Mail hoặc Outlook và nhấn Ctrl+V để dán.');
                }}).catch(err => {{
                    console.error('Lỗi Clipboard API, chạy fallback:', err);
                    runFallbackCopy(emailDiv);
                }});
            }} catch (e) {{
                console.error('Lỗi ClipboardItem, chạy fallback:', e);
                runFallbackCopy(emailDiv);
            }}
        }}

        function runFallbackCopy(emailDiv) {{
            const range = document.createRange();
            range.selectNodeContents(emailDiv);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
            
            try {{
                document.execCommand('copy');
                alert('✓ Đã sao chép nội dung thư (phương thức dự phòng)! Hãy Ctrl+V vào Lark Mail hoặc Outlook.');
            }} catch (err) {{
                alert('Không thể tự động sao chép. Bạn vui lòng bôi đen nội dung email và nhấn Ctrl+C để sao chép.');
            }}
            selection.removeAllRanges();
        }}
    </script>
</body>
</html>
"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Agent 3: Sinh báo cáo HTML trực quan thành công tại {output_path}!")

if __name__ == "__main__":
    main()

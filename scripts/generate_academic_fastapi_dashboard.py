import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def generate_dashboard():
    # 1. Trích xuất dữ liệu chuẩn 420 sinh viên từ snapshot đã đối soát
    src_file = 'output/dashboards/academic/bao_cao_chuyen_sau_fastapi_ks25.html'
    if not os.path.exists(src_file):
        raise FileNotFoundError(f"Không tìm thấy file nguồn: {src_file}")

    with open(src_file, 'r', encoding='utf-8') as f:
        src_text = f.read()

    m_stud = re.search(r'const rawStudents = (\[.*?\]);', src_text, re.DOTALL)
    m_prog = re.search(r'const rawProgression = (\{.*?\});', src_text, re.DOTALL)
    m_teach = re.search(r'const rawTeachers = (\{.*?\});', src_text, re.DOTALL)

    if not m_stud or not m_prog or not m_teach:
        raise ValueError("Không thể trích xuất đầy đủ dữ liệu JSON từ file snapshot!")

    raw_students = json.loads(m_stud.group(1))
    raw_progression = json.loads(m_prog.group(1))
    raw_teachers = json.loads(m_teach.group(1))

    print(f"Đã trích xuất thành công: {len(raw_students)} sinh viên, {len(raw_progression)} lớp học.")

    # Tạo file HTML hoàn chỉnh với phong cách Đào tạo chuyên sâu, hạn chế text dài, tăng cường biểu đồ & số liệu
    students_json = json.dumps(raw_students, ensure_ascii=False)
    progression_json = json.dumps(raw_progression, ensure_ascii=False)
    teachers_json = json.dumps(raw_teachers, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Toàn Cảnh Học Vụ: Môn FastAPI (Khóa KS25)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        slate: {{
                            850: '#111622',
                            900: '#0b0f19',
                            950: '#06080e'
                        }},
                        indigo: {{
                            500: '#6366f1',
                            600: '#4f46e5',
                            700: '#4338ca'
                        }}
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

    <!-- HEADER HỌC VỤ CHUẨN MỰC -->
    <header class="border-b border-slate-800 bg-slate-900/90 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-indigo-500/20">
                    <i class="fa-solid fa-graduation-cap"></i>
                </div>
                <div>
                    <h1 class="text-base font-bold text-white tracking-tight flex items-center gap-2">
                        BÁO CÁO TOÀN CẢNH HỌC VỤ & ĐIỂM NGHẼN ĐÀO TẠO MÔN FASTAPI (KHÓA KS25)
                        <span class="text-xs bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2 py-0.5 rounded font-mono">Course ID: 217</span>
                    </h1>
                    <p class="text-xs text-slate-400">Phân tích định lượng chuỗi tích lũy học phần, rào cản khảo thí và phễu hao hụt đồ án tốt nghiệp</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <span class="text-xs text-slate-300 bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700 flex items-center gap-2 font-mono">
                    <i class="fa-regular fa-calendar-check text-indigo-400"></i> Dữ liệu: 16/09/2026
                </span>
                <button onclick="window.print()" class="text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-3.5 py-1.5 rounded-lg shadow-md shadow-indigo-500/20 transition flex items-center gap-1.5">
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
                    <i class="fa-solid fa-filter"></i> I. Phễu Hao Hụt Học Vụ
                </button>
                <button onclick="switchTab('tab-prereq')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-link"></i> II. Chuỗi Môn Tiên Quyết
                </button>
                <button onclick="switchTab('tab-dgnl')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-microchip"></i> III. Khảo Thí ĐGNL Độc Lập
                </button>
                <button onclick="switchTab('tab-hackathon')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-diagram-project"></i> IV. Phẫu Thuật Đề Thi & Đồ Án
                </button>
                <button onclick="switchTab('tab-policy')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-scale-balanced"></i> V. Tác Động Đổi Quy Chế
                </button>
                <button onclick="switchTab('tab-classes')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-chalkboard-user"></i> VI. Ma Trận 10 Lớp & GV/TG
                </button>
                <button onclick="switchTab('tab-recovery')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2 text-rose-300">
                    <i class="fa-solid fa-life-ring"></i> VII. Phân Luồng Cứu Vãn 271 SV
                </button>
                <button onclick="switchTab('tab-students')" class="tab-btn px-3.5 py-1.5 rounded-lg text-slate-300 border border-transparent transition flex items-center gap-2">
                    <i class="fa-solid fa-table-list"></i> VIII. Tra Cứu 420 Sinh Viên
                </button>
            </nav>
        </div>
    </div>

    <!-- MAIN BODY -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">

        <!-- ========================================================================= -->
        <!-- TAB I: BỨC TRANH TOÀN CẢNH: PHỄU HAO HỤT HỌC VỤ                          -->
        <!-- ========================================================================= -->
        <section id="tab-macro" class="tab-content space-y-6">
            
            <!-- 4 SUMMARY CARDS -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="metric-card rounded-xl p-4 flex flex-col justify-between">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>SĨ SỐ NHẬP HỌC THỰC TẾ</span>
                        <i class="fa-solid fa-users text-indigo-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-white font-mono">420 <span class="text-xs text-slate-400 font-normal">SV</span></div>
                        <p class="text-xs text-slate-400 mt-1">Đã chuẩn hóa chuyển lớp (HN: 261, HCM: 159)</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>ĐỦ ĐK DỰ THI ĐỒ ÁN</span>
                        <i class="fa-solid fa-id-card-clip text-amber-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-amber-400 font-mono">273 <span class="text-xs text-slate-400 font-normal">SV (65.0%)</span></div>
                        <p class="text-xs text-rose-400 mt-1 font-medium"><i class="fa-solid fa-ban"></i> Cấm thi: 147 SV (35.0%)</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between border-rose-900/50 bg-rose-950/20">
                    <div class="flex items-center justify-between text-rose-300 text-xs font-semibold">
                        <span>BỎ THI VÌ NGHẼN ĐỒ ÁN</span>
                        <i class="fa-solid fa-triangle-exclamation text-rose-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-rose-400 font-mono">87 <span class="text-xs text-slate-400 font-normal">SV (31.9%)</span></div>
                        <p class="text-xs text-rose-300 mt-1 font-medium">Đủ ĐK nhưng không nộp đồ án 5 ngày</p>
                    </div>
                </div>

                <div class="metric-card rounded-xl p-4 flex flex-col justify-between">
                    <div class="flex items-center justify-between text-slate-400 text-xs font-semibold">
                        <span>TỶ LỆ ĐỖ KHI DỰ BẢO VỆ</span>
                        <i class="fa-solid fa-award text-emerald-400"></i>
                    </div>
                    <div class="mt-2">
                        <div class="text-3xl font-extrabold text-emerald-400 font-mono">80.1%</div>
                        <p class="text-xs text-emerald-300 mt-1 font-medium">149/186 SV bước vào phòng bảo vệ đạt chuẩn</p>
                    </div>
                </div>
            </div>

            <!-- VISUAL ATTRITION FUNNEL STEPPER -->
            <div class="glass-card rounded-xl p-6 border-indigo-900/40">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-sm font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-filter text-indigo-400"></i>
                        SƠ ĐỒ PHỄU HAO HỤT HỌC VỤ TOÀN VIỆN (ACADEMIC ATTRITION FUNNEL)
                    </h2>
                    <span class="text-xs bg-slate-800 text-slate-400 px-2.5 py-1 rounded font-mono">Khóa KS25 - Học kỳ 2</span>
                </div>

                <!-- 4 Steps Stepper Grid -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-3 relative mb-6">
                    <!-- Step 1 -->
                    <div class="funnel-step bg-slate-900/90 border border-slate-800 rounded-xl p-4 text-center">
                        <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">1. SĨ SỐ ĐẦU VÀO MÔN</div>
                        <div class="text-2xl font-extrabold text-white font-mono mt-1">420 SV</div>
                        <div class="text-xs text-slate-500 mt-1">100% quy mô thực học</div>
                        <div class="mt-2 pt-2 border-t border-slate-800/80 text-[11px] text-slate-400">
                            HN: 261 SV | HCM: 159 SV
                        </div>
                    </div>

                    <!-- Step 2 -->
                    <div class="funnel-step bg-slate-900/90 border border-slate-800 rounded-xl p-4 text-center">
                        <div class="text-[11px] font-semibold text-amber-400 uppercase tracking-wider">2. ĐỦ ĐIỀU KIỆN QUÁ TRÌNH</div>
                        <div class="text-2xl font-extrabold text-amber-400 font-mono mt-1">273 SV</div>
                        <div class="text-xs text-slate-400 mt-1">65.0% đạt điều kiện thi</div>
                        <div class="mt-2 pt-2 border-t border-slate-800/80 text-[11px] text-rose-400">
                            -147 SV (35.0%) cấm thi
                        </div>
                    </div>

                    <!-- Step 3: CHOKEPOINT -->
                    <div class="funnel-step bg-rose-950/30 border-2 border-rose-600/60 rounded-xl p-4 text-center shadow-lg shadow-rose-950/50">
                        <div class="text-[11px] font-bold text-rose-400 uppercase tracking-wider flex items-center justify-center gap-1">
                            <i class="fa-solid fa-triangle-exclamation"></i> 3. THỰC TẾ DỰ BẢO VỆ
                        </div>
                        <div class="text-2xl font-extrabold text-rose-300 font-mono mt-1">186 SV</div>
                        <div class="text-xs text-slate-300 mt-1">44.3% nộp đồ án bảo vệ</div>
                        <div class="mt-2 pt-2 border-t border-rose-900/60 text-[11px] font-bold text-rose-400">
                            VẾT NỨT: -87 SV (31.9%) BỎ THI!
                        </div>
                    </div>

                    <!-- Step 4 -->
                    <div class="funnel-step bg-slate-900/90 border border-slate-800 rounded-xl p-4 text-center">
                        <div class="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider">4. TÍCH LŨY ĐẠT CHUẨN</div>
                        <div class="text-2xl font-extrabold text-emerald-400 font-mono mt-1">149 SV</div>
                        <div class="text-xs text-emerald-400 mt-1">80.1% số dự bảo vệ đỗ</div>
                        <div class="mt-2 pt-2 border-t border-slate-800/80 text-[11px] text-slate-400">
                            Toàn khóa: 35.5% tích lũy
                        </div>
                    </div>
                </div>

                <!-- ATTRITION FUNNEL CHART & EXECUTIVE TAKEAWAY -->
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                    <div class="lg:col-span-7 h-64">
                        <canvas id="chartAttritionFunnel"></canvas>
                    </div>

                    <div class="lg:col-span-5 bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-3">
                        <div class="font-bold text-white text-xs flex items-center gap-2">
                            <i class="fa-solid fa-circle-check text-emerald-400"></i>
                            ĐÁNH GIÁ CHUYÊN MÔN QUẢN LÝ ĐÀO TẠO:
                        </div>
                        <ul class="text-xs space-y-2 text-slate-300 leading-relaxed">
                            <li class="flex items-start gap-2">
                                <i class="fa-solid fa-check text-indigo-400 mt-1"></i>
                                <span><strong>Hội đồng chấm thi không khắt khe:</strong> Tỷ lệ đỗ của sinh viên dự bảo vệ lên tới <strong>80.1%</strong> (riêng cơ sở TP.HCM đạt tới <strong>90.6%</strong>).</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <i class="fa-solid fa-circle-exclamation text-rose-400 mt-1"></i>
                                <span><strong>Điểm gãy nằm ở Đồ án 5 Ngày (Hackathon 2):</strong> Có <strong>87/273 sinh viên (31.9%)</strong> đủ điều kiện nhưng tự buông xuôi, không nộp bài do khối lượng đồ án quá tải nhận thức.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <i class="fa-solid fa-arrow-trend-up text-amber-400 mt-1"></i>
                                <span><strong>Cơ hội phục hồi:</strong> Nếu hỗ trợ kỹ thuật để giải cứu 87 sinh viên này bảo vệ đợt 2, tỷ lệ tích lũy của toàn viện sẽ tăng ngay từ <strong>35.5% lên 50% - 55%</strong>.</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- COMPARISON 2 BRANCHES (HN vs HCM) -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="glass-card rounded-xl p-5 border-slate-800 space-y-3">
                    <div class="flex justify-between items-center">
                        <span class="font-bold text-white text-xs flex items-center gap-2">
                            <i class="fa-solid fa-location-dot text-indigo-400"></i> CƠ SỞ HÀ NỘI (6 LỚP HỌC)
                        </span>
                        <span class="font-mono text-xs bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded">261 SV</span>
                    </div>
                    <div class="grid grid-cols-3 gap-2 text-center text-xs pt-1">
                        <div class="bg-slate-900 p-2 rounded border border-slate-800">
                            <div class="text-slate-400 text-[11px]">Đủ ĐK Thi</div>
                            <div class="font-mono font-bold text-white mt-0.5">169 SV (64.8%)</div>
                        </div>
                        <div class="bg-slate-900 p-2 rounded border border-slate-800">
                            <div class="text-slate-400 text-[11px]">Dự Bảo Vệ</div>
                            <div class="font-mono font-bold text-blue-400 mt-0.5">122 SV (46.7%)</div>
                        </div>
                        <div class="bg-slate-900 p-2 rounded border border-slate-800">
                            <div class="text-slate-400 text-[11px]">Tích Lũy Đạt</div>
                            <div class="font-mono font-bold text-emerald-400 mt-0.5">78 SV (29.9%)</div>
                        </div>
                    </div>
                    <div class="text-[11px] text-slate-400 pt-1 flex justify-between">
                        <span>Bỏ thi đồ án: <strong class="text-rose-400 font-mono">47 SV</strong></span>
                        <span>Đỗ khi dự thi: <strong class="text-emerald-400 font-mono">63.9%</strong></span>
                    </div>
                </div>

                <div class="glass-card rounded-xl p-5 border-slate-800 space-y-3">
                    <div class="flex justify-between items-center">
                        <span class="font-bold text-white text-xs flex items-center gap-2">
                            <i class="fa-solid fa-location-dot text-emerald-400"></i> CƠ SỞ TP.HCM (4 LỚP HỌC)
                        </span>
                        <span class="font-mono text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded">159 SV</span>
                    </div>
                    <div class="grid grid-cols-3 gap-2 text-center text-xs pt-1">
                        <div class="bg-slate-900 p-2 rounded border border-slate-800">
                            <div class="text-slate-400 text-[11px]">Đủ ĐK Thi</div>
                            <div class="font-mono font-bold text-white mt-0.5">104 SV (65.4%)</div>
                        </div>
                        <div class="bg-slate-900 p-2 rounded border border-slate-800">
                            <div class="text-slate-400 text-[11px]">Dự Bảo Vệ</div>
                            <div class="font-mono font-bold text-blue-400 mt-0.5">64 SV (40.3%)</div>
                        </div>
                        <div class="bg-slate-900 p-2 rounded border border-slate-800">
                            <div class="text-slate-400 text-[11px]">Tích Lũy Đạt</div>
                            <div class="font-mono font-bold text-emerald-400 mt-0.5">71 SV (44.7%)</div>
                        </div>
                    </div>
                    <div class="text-[11px] text-slate-400 pt-1 flex justify-between">
                        <span>Bỏ thi đồ án: <strong class="text-rose-400 font-mono">40 SV</strong></span>
                        <span>Đỗ khi dự thi: <strong class="text-emerald-400 font-mono font-bold">90.6%!</strong></span>
                    </div>
                </div>
            </div>

        </section>

        <!-- ========================================================================= -->
        <!-- TAB II: LỖ HỔNG MÔN TIÊN QUYẾT & HIỆU ỨNG DOMINO                         -->
        <!-- ========================================================================= -->
        <section id="tab-prereq" class="tab-content hidden space-y-6">
            <div class="glass-card rounded-xl p-6">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-link text-indigo-400"></i>
                            II. LỖ HỔNG NỀN TẢNG TÍCH LŨY: CHUỖI 3 MÔN LIÊN TIẾP (CSDL ➔ PYTHON ➔ FASTAPI)
                        </h2>
                        <p class="text-xs text-slate-400">Đo lường sự hao hụt kiến thức dây chuyền từ Kỳ I đến môn lập trình Web backend</p>
                    </div>
                    <span class="text-xs bg-slate-800 text-slate-400 px-3 py-1 rounded font-mono">Dữ liệu SQL qldt_el</span>
                </div>

                <!-- KEY METRIC CARDS -->
                <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-6">
                    <div class="bg-slate-900/90 p-4 rounded-xl border border-slate-800 text-center">
                        <div class="text-[11px] text-slate-400 font-medium">TRƯỢT MÔN JAVASCRIPT (KỲ I)</div>
                        <div class="text-2xl font-extrabold text-rose-400 font-mono mt-1">237 SV</div>
                        <div class="text-[11px] text-slate-500">56.4% học viên mất căn bản giải thuật</div>
                    </div>

                    <div class="bg-slate-900/90 p-4 rounded-xl border border-slate-800 text-center">
                        <div class="text-[11px] text-slate-400 font-medium">TRƯỢT LẬP TRÌNH C (KỲ I)</div>
                        <div class="text-2xl font-extrabold text-amber-400 font-mono mt-1">161 SV</div>
                        <div class="text-[11px] text-slate-500">38.3% hổng cú pháp lập trình</div>
                    </div>

                    <div class="bg-slate-900/90 p-4 rounded-xl border border-slate-800 text-center">
                        <div class="text-[11px] text-slate-400 font-medium">TỶ LỆ ĐỖ PYTHON (KỲ II)</div>
                        <div class="text-2xl font-extrabold text-indigo-400 font-mono mt-1">58.6%</div>
                        <div class="text-[11px] text-slate-500">Giảm -13.7% so với CSDL (72.3%)</div>
                    </div>

                    <div class="bg-slate-900/90 p-4 rounded-xl border border-slate-800 text-center">
                        <div class="text-[11px] text-slate-400 font-medium">TỶ LỆ ĐỖ FASTAPI (KỲ II)</div>
                        <div class="text-2xl font-extrabold text-rose-400 font-mono mt-1">35.5%</div>
                        <div class="text-[11px] text-slate-500">Giảm tiếp -23.1% so với Python</div>
                    </div>
                </div>

                <!-- 3 COURSES PROGRESSION CHART -->
                <div class="bg-slate-900/60 p-5 rounded-xl border border-slate-800 mb-6">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-xs font-bold text-slate-200 uppercase tracking-wider">
                            Biểu Đồ So Sánh Tỷ Lệ Đạt Chuẩn Qua Chuỗi 3 Môn Học (CSDL ➔ Python ➔ FastAPI) Theo 10 Lớp
                        </h3>
                        <span class="text-xs text-slate-400 font-mono">Đơn vị: % Học viên tích lũy</span>
                    </div>
                    <div class="h-72">
                        <canvas id="chartPrereqComparison"></canvas>
                    </div>
                </div>

                <!-- TABLE OF 3 COURSES -->
                <div class="overflow-x-auto custom-scrollbar border border-slate-800 rounded-xl">
                    <table class="w-full text-xs text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 bg-slate-900 text-slate-300 font-semibold">
                                <th class="py-2.5 px-3">Cơ Sở</th>
                                <th class="py-2.5 px-3">Lớp Học</th>
                                <th class="py-2.5 px-3 text-center">Cơ Sở Dữ Liệu (183)</th>
                                <th class="py-2.5 px-3 text-center">Lập Trình Python (193)</th>
                                <th class="py-2.5 px-3 text-center text-indigo-400">FastAPI (217)</th>
                                <th class="py-2.5 px-3 text-center">Mức Độ Suy Giảm</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-850 text-slate-300" id="table-prereq-body">
                            <!-- Injected by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB III: KHẢO THÍ ĐGNL ĐỘC LẬP (KHÔNG AI)                                -->
        <!-- ========================================================================= -->
        <section id="tab-dgnl" class="tab-content hidden space-y-6">
            <div class="glass-card rounded-xl p-6">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-microchip text-indigo-400"></i>
                            III. KHẢO THÍ ĐGNL ĐỘC LẬP: ĐO LƯỜNG NĂNG LỰC THỰC KHI KHÔNG CÓ AI HỖ TRỢ
                        </h2>
                        <p class="text-xs text-slate-400">Dữ liệu khảo thí độc lập trên 429 học viên khóa KS25 CNTT do Ban Chuyên môn khảo sát</p>
                    </div>
                    <span class="text-xs bg-rose-500/20 text-rose-300 border border-rose-500/30 px-3 py-1 rounded font-mono font-bold">
                        Trượt TH: 85.9% (Điểm TB: 20.2/100)
                    </span>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center mb-6">
                    <!-- RADAR CHART -->
                    <div class="lg:col-span-5 bg-slate-900/60 p-4 rounded-xl border border-slate-800 h-80 flex flex-col justify-between">
                        <div class="text-xs font-bold text-slate-300 uppercase tracking-wider text-center">
                            Radar Đánh Giá 4 Kỹ Năng Cốt Lõi Tại Kỳ ĐGNL
                        </div>
                        <div class="h-64">
                            <canvas id="chartDgnlRadar"></canvas>
                        </div>
                    </div>

                    <!-- 4 BOTTLENECK CARDS -->
                    <div class="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                        <div class="bg-slate-900/90 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
                            <div class="flex justify-between items-center">
                                <span class="font-bold text-white text-xs">1. Bẫy Lỗi Ngoại Lệ (Exception)</span>
                                <span class="text-rose-400 font-mono font-bold text-xs">10.4% Đạt</span>
                            </div>
                            <p class="text-slate-400 text-[11px] leading-relaxed">
                                Hầu hết học viên không biết dùng <code>HTTPException</code> để bắt lỗi 404, 400 hoặc kiểm soát ràng buộc toàn vẹn khóa ngoại khi xóa dữ liệu.
                            </p>
                        </div>

                        <div class="bg-slate-900/90 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
                            <div class="flex justify-between items-center">
                                <span class="font-bold text-white text-xs">2. Truy Vấn Quan Hệ (ORM Join)</span>
                                <span class="text-rose-400 font-mono font-bold text-xs">15.3% Đạt</span>
                            </div>
                            <p class="text-slate-400 text-[11px] leading-relaxed">
                                API yêu cầu truy vấn lồng (quan hệ 1-N giữa 2 bảng) chỉ có 15.3% sinh viên viết được. Phần lớn không hiểu cơ chế join qua SQLAlchemy.
                            </p>
                        </div>

                        <div class="bg-slate-900/90 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
                            <div class="flex justify-between items-center">
                                <span class="font-bold text-white text-xs">3. Thuật Toán Lọc & Duyệt Python</span>
                                <span class="text-amber-400 font-mono font-bold text-xs">27.3% Đạt</span>
                            </div>
                            <p class="text-slate-400 text-[11px] leading-relaxed">
                                Thuật toán duyệt danh sách cơ bản có điều kiện lọc chỉ đạt 27.3%. Sinh viên phụ thuộc hoàn toàn vào tài liệu mẫu và công cụ sinh code.
                            </p>
                        </div>

                        <div class="bg-slate-900/90 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
                            <div class="flex justify-between items-center">
                                <span class="font-bold text-white text-xs">4. Thiết Kế SQLAlchemy Model</span>
                                <span class="text-amber-400 font-mono font-bold text-xs">31.8% Đạt</span>
                            </div>
                            <p class="text-slate-400 text-[11px] leading-relaxed">
                                59.7% cấu hình được kết nối DB theo mẫu, nhưng khi tự khai báo quan hệ khóa ngoại (ForeignKey) giữa các Model thì tỷ lệ tụt xuống 31.8%.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-300 flex items-start gap-2.5">
                    <i class="fa-solid fa-lightbulb mt-0.5 text-amber-400"></i>
                    <div>
                        <strong>KẾT LUẬN SƯ PHẠM VỀ "ẢO TƯỞNG NĂNG LỰC":</strong>
                        Khi làm bài tập về nhà (BTVN), tỷ lệ nộp bài của sinh viên đạt <strong>80% - 95%</strong> nhờ tham khảo tài nguyên và AI hỗ trợ. Tuy nhiên, kỳ khảo thí ĐGNL không có kết nối ngoài đã phơi bày lỗ hổng tư duy lập trình thực chất. Khi bước vào đồ án tốt nghiệp 5 ngày với kiến trúc nghiệp vụ phức tạp, sinh viên lập tức rơi vào trạng thái bế tắc.
                    </div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB IV: PHẪU THUẬT ĐỀ THI & ĐỒ ÁN (HACKATHON 1 & 2)                       -->
        <!-- ========================================================================= -->
        <section id="tab-hackathon" class="tab-content hidden space-y-6">
            <div class="glass-card rounded-xl p-6">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-diagram-project text-indigo-400"></i>
                            IV. PHẪU THUẬT 2 CHẶNG THI HACKATHON: ÁP LỰC THỜI LƯỢNG & ĐỘ PHỨC TẠP ĐỒ ÁN
                        </h2>
                        <p class="text-xs text-slate-400">Đối soát trực tiếp giữa cấu trúc đề thi Hackathon 1 (Giữa môn) và Đề tài Đồ án Hackathon 2 (Cuối môn)</p>
                    </div>
                </div>

                <!-- 2 PHASES COMPARISON CARDS -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div class="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-2.5">
                        <div class="flex justify-between items-center">
                            <span class="font-bold text-white text-xs flex items-center gap-2">
                                <i class="fa-solid fa-clock text-amber-400"></i> HACKATHON 1: THI TỰ LUẬN & TRẮC NGHIỆM
                            </span>
                            <span class="text-emerald-400 font-mono font-bold text-xs">Điểm TB: 60.5</span>
                        </div>
                        <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
                            <li><strong>- Hình thức thi:</strong> Làm bài trực tiếp tại phòng máy (Thời lượng tập trung).</li>
                            <li><strong>- Cấu trúc đề:</strong> Kết hợp câu hỏi trắc nghiệm lý thuyết và bài tập tự luận viết API CRUD đơn giản trên 1 bảng.</li>
                            <li><strong>- Điểm nghẽn học vụ:</strong> <strong>Quá thời gian làm bài!</strong> Đề thi tích hợp cả trắc nghiệm và tự luận khiến đa phần sinh viên không đủ thời gian hoàn thành trọn vẹn cả 2 phần, sinh tâm lý căng thẳng.</li>
                        </ul>
                    </div>

                    <div class="bg-slate-900/90 p-5 rounded-xl border border-rose-900/40 space-y-2.5">
                        <div class="flex justify-between items-center">
                            <span class="font-bold text-rose-300 text-xs flex items-center gap-2">
                                <i class="fa-solid fa-code-branch text-rose-400"></i> HACKATHON 2: ĐỒ ÁN THỰC HÀNH 5 NGÀY
                            </span>
                            <span class="text-rose-400 font-mono font-bold text-xs">Điểm TB: 35.2 (Trượt 58.8%)</span>
                        </div>
                        <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
                            <li><strong>- Đề tài:</strong> <em>Construction Site Management API</em> (Quản lý công trường xây dựng B2B).</li>
                            <li><strong>- Độ phức tạp kiến trúc:</strong> 4 Thực thể liên kết (`User`, `Site`, `SiteMember`, `WorkItem`), phân quyền kép RBAC/ABAC.</li>
                            <li><strong>- Điểm nghẽn học vụ:</strong> <strong>Quá tải nhận thức & Dung lượng bài toán!</strong> Khối lượng 30 task trong 5 ngày vượt xa năng lực của sinh viên năm 1-2, dẫn đến việc 87 sinh viên buông xuôi, bỏ bảo vệ.</li>
                        </ul>
                    </div>
                </div>

                <!-- 5-DAY DECONSTRUCTION TABLE OF HACKATHON 2 PROJECT -->
                <div class="bg-slate-900/60 p-5 rounded-xl border border-slate-800 mb-6">
                    <h3 class="text-xs font-bold text-slate-200 uppercase tracking-wider mb-4 flex items-center justify-between">
                        <span>Bảng Bóc Tách Khối Lượng 30 Task Đồ Án 5 Ngày (Construction Site Management API)</span>
                        <span class="text-xs text-rose-400 font-mono font-bold">Mức độ tương đương: Junior Dev 1-2 năm kinh nghiệm</span>
                    </h3>

                    <div class="overflow-x-auto custom-scrollbar border border-slate-800 rounded-lg">
                        <table class="w-full text-xs text-left border-collapse">
                            <thead>
                                <tr class="border-b border-slate-800 bg-slate-900 text-slate-300 font-semibold">
                                    <th class="py-2.5 px-3">Lộ Trình</th>
                                    <th class="py-2.5 px-3">Nội Dung Nghiệp Vụ Kỹ Thuật</th>
                                    <th class="py-2.5 px-3">Khối Lượng Task</th>
                                    <th class="py-2.5 px-3">Độ Phức Tạp Kỹ Thuật</th>
                                    <th class="py-2.5 px-3">Rủi Ro Học Vụ (Đối với SV Năm 1-2)</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-850 text-slate-300">
                                <tr>
                                    <td class="py-2.5 px-3 font-bold text-indigo-400 font-mono">Tiết 1 / Ngày 1</td>
                                    <td class="py-2.5 px-3">DB Schema & SQLAlchemy ORM (4 Model quan hệ, UUID, Soft delete)</td>
                                    <td class="py-2.5 px-3 font-mono">5 task</td>
                                    <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded text-[11px] bg-amber-500/20 text-amber-300 border border-amber-500/30">Trung bình</span></td>
                                    <td class="py-2.5 px-3 text-slate-400">Sinh viên làm được nếu có khung bài lab mẫu</td>
                                </tr>
                                <tr>
                                    <td class="py-2.5 px-3 font-bold text-rose-400 font-mono">Tiết 2 / Ngày 2</td>
                                    <td class="py-2.5 px-3">JWT Auth & Ma trận phân quyền (Hash password, Token expiry, Dependency Injection)</td>
                                    <td class="py-2.5 px-3 font-mono">5 task</td>
                                    <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded text-[11px] bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold">Rất cao</span></td>
                                    <td class="py-2.5 px-3 text-rose-400 font-semibold"><i class="fa-solid fa-ban"></i> ĐIỂM GÃY SỐ 1: Bế tắc phân tầng middleware & bảo mật</td>
                                </tr>
                                <tr>
                                    <td class="py-2.5 px-3 font-bold text-rose-400 font-mono">Tiết 3 / Ngày 3</td>
                                    <td class="py-2.5 px-3">Quản lý Công trình & SiteMember (Phân quyền Owner/Member, Chặn truy cập 403)</td>
                                    <td class="py-2.5 px-3 font-mono">6 task</td>
                                    <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded text-[11px] bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold">Rất cao</span></td>
                                    <td class="py-2.5 px-3 text-rose-300">Không hiểu nghiệp vụ B2B quản lý công trường xây dựng</td>
                                </tr>
                                <tr>
                                    <td class="py-2.5 px-3 font-bold text-rose-400 font-mono">Tiết 4 / Ngày 4</td>
                                    <td class="py-2.5 px-3">WorkItem CRUD, Lọc đa tiêu chí, Phân trang, Upload attachment file</td>
                                    <td class="py-2.5 px-3 font-mono">8 task</td>
                                    <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded text-[11px] bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold">Cực lớn (8 task)</span></td>
                                    <td class="py-2.5 px-3 text-rose-400 font-semibold"><i class="fa-solid fa-ban"></i> ĐIỂM GÃY SỐ 2: Quá tải thời gian code (Cần 8-10h/ngày)</td>
                                </tr>
                                <tr>
                                    <td class="py-2.5 px-3 font-bold text-indigo-400 font-mono">Tiết 5 / Ngày 5</td>
                                    <td class="py-2.5 px-3">Tích hợp Swagger, Viết Integration Test, Seed data</td>
                                    <td class="py-2.5 px-3 font-mono">6 task</td>
                                    <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded text-[11px] bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Nâng cao</span></td>
                                    <td class="py-2.5 px-3 text-slate-400">Sinh viên kiệt sức, không kịp hoàn thiện tài liệu nộp</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- PROGRESSION CHART (HACK 1 vs HACK 2) -->
                <div class="bg-slate-900/60 p-5 rounded-xl border border-slate-800">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-xs font-bold text-slate-200 uppercase tracking-wider">
                            Biểu Đồ So Sánh Điểm Thi Thực Hành Hackathon 1 vs Hackathon 2 Theo 10 Lớp Học
                        </h3>
                        <span class="text-xs text-slate-400 font-mono">Thang điểm 100</span>
                    </div>
                    <div class="h-64">
                        <canvas id="chartHackathonProgression"></canvas>
                    </div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB V: TÁC ĐỘNG ĐỔI QUY CHẾ (CŨ VS MỚI)                                   -->
        <!-- ========================================================================= -->
        <section id="tab-policy" class="tab-content hidden space-y-6">
            <div class="glass-card rounded-xl p-6">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-scale-balanced text-indigo-400"></i>
                            V. ĐỐI SOÁT TÁC ĐỘNG CỦA VIỆC THAY ĐỔI QUY CHẾ ĐIỀU KIỆN DỰ THI
                        </h2>
                        <p class="text-xs text-slate-400">Đánh giá tính đúng đắn của Quy chế mới: Quy chế mới có phải là nguyên nhân làm tăng tỷ lệ trượt không?</p>
                    </div>
                </div>

                <!-- 2 COMPARISON BOXES -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div class="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-2">
                        <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">QUY CHẾ CŨ (ÁP DỤNG TRƯỚC MÔN FASTAPI)</span>
                        <div class="text-xs text-slate-300 leading-relaxed pt-1">
                            - <strong>Tiêu chí:</strong> Chỉ yêu cầu <span class="font-mono text-amber-300 font-bold">Rpoint ≥ 80</span>.<br>
                            - <strong>Hệ quả tiêu cực:</strong> Sinh viên có thể nghỉ học chuyên cần nhiều buổi nhưng chăm làm BTVN và Elearning để bù điểm (bị trừ tối đa 20 điểm CC vẫn còn 80 điểm) ➔ Sinh ra tâm lý <strong>ỷ lại, trốn học và mất gốc kiến thức trên lớp</strong>.
                        </div>
                    </div>

                    <div class="bg-slate-900/90 p-5 rounded-xl border border-indigo-500/40 space-y-2">
                        <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider">QUY CHẾ MỚI (ÁP DỤNG TỪ MÔN FASTAPI)</span>
                        <div class="text-xs text-slate-300 leading-relaxed pt-1">
                            - <strong>Tiêu chí:</strong> <span class="font-mono text-emerald-300 font-bold">Rpoint ≥ 80 + Vắng CC ≤ 20% + Nợ BT ≤ 20% + Trễ EL ≤ 3</span>.<br>
                            - <strong>Tác động học vụ:</strong> Chặn đứng tình trạng trốn học, siết chặt kỷ luật tác phong sinh viên mà <strong>không làm giảm đáng kể số lượng được thi</strong> (chỉ lệch đúng 2 SV).
                        </div>
                    </div>
                </div>

                <!-- COMPARISON TABLE -->
                <div class="overflow-x-auto custom-scrollbar border border-slate-800 rounded-xl mb-6">
                    <table class="w-full text-xs text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 bg-slate-900 text-slate-300 font-semibold">
                                <th class="py-2.5 px-3">Chỉ Số Học Vụ</th>
                                <th class="py-2.5 px-3 text-center">Quy Chế Cũ (Rpoint ≥ 80)</th>
                                <th class="py-2.5 px-3 text-center text-indigo-400">Quy Chế Mới (Đa Tiêu Chí)</th>
                                <th class="py-2.5 px-3 text-center">Độ Lệch</th>
                                <th class="py-2.5 px-3">Nhận Xét Của Ban Đào Tạo</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-850 text-slate-300">
                            <tr>
                                <td class="py-2.5 px-3 font-semibold text-white">Toàn Viện (420 SV) Đủ ĐK Dự Thi</td>
                                <td class="py-2.5 px-3 text-center font-mono">275 SV (65.5%)</td>
                                <td class="py-2.5 px-3 text-center font-mono font-bold text-emerald-400">273 SV (65.0%)</td>
                                <td class="py-2.5 px-3 text-center font-mono text-amber-400 font-bold">-2 SV (-0.5%)</td>
                                <td class="py-2.5 px-3 text-slate-400">Tỷ lệ đủ điều kiện thi gần như tương đương tuyệt đối</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-semibold text-white">Cơ Sở Hà Nội (261 SV) Đủ ĐK</td>
                                <td class="py-2.5 px-3 text-center font-mono">171 SV (65.5%)</td>
                                <td class="py-2.5 px-3 text-center font-mono text-emerald-400">169 SV (64.8%)</td>
                                <td class="py-2.5 px-3 text-center font-mono text-amber-400 font-bold">-2 SV (-0.7%)</td>
                                <td class="py-2.5 px-3 text-slate-400">Chỉ loại bỏ 2 sinh viên vắng chuyên cần quá 20%</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-semibold text-white">Cơ Sở TP.HCM (159 SV) Đủ ĐK</td>
                                <td class="py-2.5 px-3 text-center font-mono">104 SV (65.4%)</td>
                                <td class="py-2.5 px-3 text-center font-mono text-emerald-400">104 SV (65.4%)</td>
                                <td class="py-2.5 px-3 text-center font-mono text-emerald-400 font-bold">0 SV (0.0%)</td>
                                <td class="py-2.5 px-3 text-slate-400">Không có bất kỳ sinh viên nào bị ảnh hưởng thêm</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="p-4 bg-slate-900/90 border border-slate-800 rounded-xl text-xs text-slate-300 space-y-2">
                    <div class="font-bold text-white flex items-center gap-2 text-xs">
                        <i class="fa-solid fa-check-double text-emerald-400"></i>
                        KẾT LUẬN VỀ QUY CHẾ MỚI:
                    </div>
                    <p class="leading-relaxed">
                        Số liệu thực tế chứng minh: <strong>Việc áp dụng Quy chế mới KHÔNG PHẢI là nguyên nhân làm tăng tỷ lệ trượt môn FastAPI</strong>. Việc siết trần chuyên cần và bài tập chỉ loại bỏ thêm vỏn vẹn 2 sinh viên trên toàn viện. Ngược lại, quy chế này đã kịp thời lập lại kỷ cương học tập, ngăn ngừa tình trạng trốn học cày điểm thưởng. Nguyên nhân cốt tử khiến tỷ lệ tích lũy đạt thấp vẫn nằm ở <strong>điểm gãy đồ án 5 ngày và lỗ hổng nền tảng tích lũy</strong>.
                    </p>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB VI: MA TRẬN 10 LỚP HỌC & ĐỘI NGŨ GV/TG                               -->
        <!-- ========================================================================= -->
        <section id="tab-classes" class="tab-content hidden space-y-6">
            <div class="glass-card rounded-xl p-6">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-chalkboard-user text-indigo-400"></i>
                            VI. MA TRẬN ĐỐI SÁNH KẾT QUẢ ĐÀO TẠO THEO ĐỘI NGŨ GIẢNG VIÊN & TRỢ GIẢNG
                        </h2>
                        <p class="text-xs text-slate-400">Dữ liệu Giảng viên (GV) và Trợ giảng (TG) trích xuất trực tiếp từ file theo dõi PTIT_Chiso.xlsx</p>
                    </div>
                </div>

                <div class="overflow-x-auto custom-scrollbar border border-slate-800 rounded-xl mb-6">
                    <table class="w-full text-xs text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 bg-slate-900 text-slate-300 font-semibold">
                                <th class="py-2.5 px-3">Cơ Sở</th>
                                <th class="py-2.5 px-3">Lớp Học</th>
                                <th class="py-2.5 px-3">Giảng Viên (GV)</th>
                                <th class="py-2.5 px-3">Trợ Giảng (TG)</th>
                                <th class="py-2.5 px-2 text-center">Sĩ Số</th>
                                <th class="py-2.5 px-2 text-center text-emerald-400">Đạt Chuẩn</th>
                                <th class="py-2.5 px-2 text-center text-emerald-400">Tỷ Lệ Đạt</th>
                                <th class="py-2.5 px-2 text-center text-blue-400">Dự Bảo Vệ</th>
                                <th class="py-2.5 px-2 text-center">Vắng CC TB</th>
                                <th class="py-2.5 px-2 text-center">Hackathon 1</th>
                                <th class="py-2.5 px-2 text-center">Hackathon 2</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-850 text-slate-300" id="teacher-class-tbody">
                            <!-- Injected by JS -->
                        </tbody>
                    </table>
                </div>

                <!-- TEACHER DYNAMICS ANALYSIS -->
                <div class="p-4 bg-slate-900/90 border border-slate-800 rounded-xl text-xs space-y-3">
                    <h3 class="font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-magnifying-glass-chart text-indigo-400"></i>
                        PHÂN TÍCH CHUYÊN MÔN VỀ SỰ KHÁC BIỆT KẾT QUẢ GIỮA CÁC LỚP:
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="bg-slate-950/60 p-3.5 rounded-lg border border-slate-850">
                            <span class="font-bold text-indigo-300">1. Nghịch lý giữa hai lớp của Thầy Lê Hà Thanh Sang & TG Phạm Viết Hùng:</span>
                            <p class="text-slate-400 mt-1 leading-relaxed">
                                Cùng một cặp GV/TG phụ trách tại TP.HCM, nhưng lớp <code>HCM-CNTT5</code> đạt tỷ lệ đỗ cao nhất toàn viện (<strong>56.4%</strong>), trong khi lớp <code>HCM-CNTT8</code> lại có kết quả thấp nhất toàn viện (<strong>7.9%</strong>). Điều này minh chứng: <strong>Không thể quy kết nguyên nhân hoàn toàn do năng lực sư phạm của GV/TG</strong>, mà do chất lượng đầu vào của học viên lớp CNTT8 đã suy thoái từ các môn trước, dẫn đến việc buông lỏng chuyên cần (vắng 35.2%) và bỏ thi hàng loạt.
                            </p>
                        </div>
                        <div class="bg-slate-950/60 p-3.5 rounded-lg border border-slate-850">
                            <span class="font-bold text-indigo-300">2. Mức độ đồng đều tại cơ sở Hà Nội:</span>
                            <p class="text-slate-400 mt-1 leading-relaxed">
                                Đội ngũ GV tại Hà Nội gồm Thầy <strong>Lương Quốc Tuấn</strong>, Thầy <strong>Lâm Tùng Dương</strong>, Thầy <strong>Nguyễn Quảng An</strong> và 2 Trợ giảng <strong>Lại Trung Lâm</strong>, <strong>Phạm Ngọc Kiên</strong> có tỷ lệ đạt dao động tương đối đồng đều quanh mức <strong>25% - 45%</strong>. Các lớp có trợ giảng theo sát và đôn đốc bài tập tuần tốt (như CNTT1, CNTT6) duy trì tỷ lệ đỗ trên 36% - 45%.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB VII: PHÂN LUỒNG HỌC VỤ & KẾ HOẠCH CỨU VÃN 271 SV                     -->
        <!-- ========================================================================= -->
        <section id="tab-recovery" class="tab-content hidden space-y-6">
            <div class="glass-card rounded-xl p-6 border-rose-900/30">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-life-ring text-rose-400"></i>
                            VII. KẾ HOẠCH HỌC VỤ CHIẾN LƯỢC: PHÂN LUỒNG XỬ LÝ CHO 271 SINH VIÊN CHƯA ĐẠT
                        </h2>
                        <p class="text-xs text-slate-400">Chiến lược can thiệp sư phạm thực tế, đối diện với nguy cơ sinh viên nản lòng, xin bảo lưu hoặc thôi học</p>
                    </div>
                    <span class="text-xs font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30 px-3 py-1 rounded-lg">
                        Quy mô: 271 Sinh Viên (64.5%)
                    </span>
                </div>

                <!-- DONUT CHART & OVERVIEW -->
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center mb-6">
                    <div class="lg:col-span-5 bg-slate-900/60 p-4 rounded-xl border border-slate-800 h-72 flex flex-col justify-between">
                        <div class="text-xs font-bold text-slate-300 uppercase tracking-wider text-center">
                            Phân Bổ 3 Luồng Sinh Viên Cần Can Thiệp Sư Phạm
                        </div>
                        <div class="h-56">
                            <canvas id="chartRecoveryDonut"></canvas>
                        </div>
                    </div>

                    <div class="lg:col-span-7 bg-amber-500/10 border border-amber-500/20 rounded-xl p-4 text-xs text-amber-300 space-y-2">
                        <div class="font-bold flex items-center gap-2 text-sm">
                            <i class="fa-solid fa-triangle-exclamation text-amber-400"></i>
                            NHẬN DIỆN THỰC TẾ: NGUY CƠ NẢN LÒNG & BẢO LƯU CAO
                        </div>
                        <p class="leading-relaxed">
                            Khảo sát từ Cố vấn học tập (CVHT) và Trợ giảng cho thấy: Trong số 271 sinh viên chưa đạt môn FastAPI, <strong>rất nhiều em đang rơi vào trạng thái nản chí, mất phương hướng và có ý định làm thủ tục xin bảo lưu / nghỉ học</strong>. Nếu Ban Đào tạo áp dụng cơ chế xử lý máy móc (bắt buộc toàn bộ học lại từ đầu và đóng học phí bình thường), nguy cơ học viên nản lòng bỏ học hàng loạt (Dropout Rate) sẽ tăng rất cao.
                        </p>
                    </div>
                </div>

                <!-- 3 COHORTS STRATEGY CARDS -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    
                    <!-- COHORT 1 -->
                    <div class="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-3 flex flex-col justify-between">
                        <div>
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider">PHÂN LUỒNG 1 (CẦN CỨU GẤP)</span>
                                <span class="text-xs font-mono font-bold bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded">87 SV (32%)</span>
                            </div>
                            <h3 class="text-sm font-bold text-white mb-2">Nhóm Đủ Điều Kiện Quá Trình Nhưng Chưa Nộp Đồ Án</h3>
                            <p class="text-xs text-slate-400 leading-relaxed">
                                Đây là những sinh viên đã tích lũy đủ $Rpoint \ge 80$, chuyên cần tốt, nhưng bị tắc nghẽn ở tuần cuối đồ án nên không kịp nộp bài bảo vệ.
                            </p>
                        </div>
                        <div class="pt-3 border-t border-slate-800 space-y-1.5 text-xs">
                            <div class="font-bold text-emerald-400">Giải Pháp Chiến Lược:</div>
                            <p class="text-slate-300">• Bảo lưu 100% điểm học tập quá trình.</p>
                            <p class="text-slate-300">• Workshop gỡ lỗi đồ án tập trung 02 tuần do TG kèm 1-1.</p>
                            <p class="text-slate-300">• Mở Hội đồng bảo vệ Đợt 2 (Kỳ vọng cứu 50 - 60 SV đỗ ngay).</p>
                        </div>
                    </div>

                    <!-- COHORT 2 -->
                    <div class="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-3 flex flex-col justify-between">
                        <div>
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">PHÂN LUỒNG 2 (NGUY CƠ BỎ HỌC)</span>
                                <span class="text-xs font-mono font-bold bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded">95 SV (35%)</span>
                            </div>
                            <h3 class="text-sm font-bold text-white mb-2">Nhóm Sinh Viên Nản Chí / Xin Bảo Lưu</h3>
                            <p class="text-xs text-slate-400 leading-relaxed">
                                Nhóm học viên bị đuối sức nghiêm trọng, vắng học trên 20%, không nộp bài tập và có tâm lý buông xuôi, đã hoặc chuẩn bị nộp đơn bảo lưu.
                            </p>
                        </div>
                        <div class="pt-3 border-t border-slate-800 space-y-1.5 text-xs">
                            <div class="font-bold text-amber-400">Giải Pháp Chiến Lược:</div>
                            <p class="text-slate-300">• CVHT đối thoại 1-1 với từng sinh viên & phụ huynh.</p>
                            <p class="text-slate-300">• Lộ trình học chậm (Pacing Adjustment) với học phí ưu đãi.</p>
                            <p class="text-slate-300">• Mục tiêu số 1: Giữ chân học viên trong hệ sinh thái.</p>
                        </div>
                    </div>

                    <!-- COHORT 3 -->
                    <div class="bg-slate-900/90 p-5 rounded-xl border border-slate-800 space-y-3 flex flex-col justify-between">
                        <div>
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-xs font-bold text-rose-400 uppercase tracking-wider">PHÂN LUỒNG 3 (HỌC LẠI BÀI BẢN)</span>
                                <span class="text-xs font-mono font-bold bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded">89 SV (33%)</span>
                            </div>
                            <h3 class="text-sm font-bold text-white mb-2">Nhóm Hổng Kiến Thức Cần Đào Tạo Lại Thực Chất</h3>
                            <p class="text-xs text-slate-400 leading-relaxed">
                                Nhóm học viên có nguyện vọng học tiếp nhưng lỗ hổng kiến thức quá lớn từ môn Python và CSDL, không thể làm đồ án nếu không học lại từ đầu.
                            </p>
                        </div>
                        <div class="pt-3 border-t border-slate-800 space-y-1.5 text-xs">
                            <div class="font-bold text-rose-400">Giải Pháp Chiến Lược:</div>
                            <p class="text-slate-300">• Thiết kế khóa Bootcamp Coding Lab (70% thời lượng code).</p>
                            <p class="text-slate-300">• Chia nhỏ 3 mốc nghiệm thu đồ án bắt buộc từng tuần.</p>
                            <p class="text-slate-300">• Không ghép vào lớp học lại lý thuyết thông thường.</p>
                        </div>
                    </div>

                </div>
            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB VIII: TRA CỨU 420 SINH VIÊN                                           -->
        <!-- ========================================================================= -->
        <section id="tab-students" class="tab-content hidden space-y-6">
            <div class="glass-card rounded-xl p-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-users-viewfinder text-indigo-400"></i>
                            VIII. BẢNG TRA CỨU HỌC VỤ CHI TIẾT 420 SINH VIÊN MÔN FASTAPI
                        </h2>
                        <p class="text-xs text-slate-400">Dữ liệu đối soát phục vụ công tác quản lý giáo vụ và can thiệp sư phạm từng cá nhân</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <input type="text" id="studentSearch" placeholder="Tìm tên, mã SV, lớp..." 
                               class="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500 w-56">
                        <select id="branchFilter" class="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-indigo-500">
                            <option value="ALL">Tất cả cơ sở</option>
                            <option value="Hà Nội">Hà Nội</option>
                            <option value="TP.HCM">TP.HCM</option>
                        </select>
                        <select id="statusFilter" class="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-indigo-500">
                            <option value="ALL">Tất cả kết quả</option>
                            <option value="PASS">Đạt tích lũy</option>
                            <option value="FAIL">Không đạt</option>
                            <option value="DEFENDED">Đã bảo vệ</option>
                            <option value="DROPPED">Bỏ thi bảo vệ</option>
                        </select>
                    </div>
                </div>

                <div class="overflow-x-auto custom-scrollbar border border-slate-800 rounded-xl max-h-[600px]">
                    <table class="w-full text-xs text-left border-collapse">
                        <thead class="sticky top-0 bg-slate-900 z-10">
                            <tr class="border-b border-slate-800 text-slate-300 font-semibold">
                                <th class="py-2.5 px-3">Mã SV</th>
                                <th class="py-2.5 px-3">Họ và Tên</th>
                                <th class="py-2.5 px-3">Lớp Học</th>
                                <th class="py-2.5 px-2 text-center">Vắng CC (%)</th>
                                <th class="py-2.5 px-2 text-center">BTVN (%)</th>
                                <th class="py-2.5 px-2 text-center">Trễ EL</th>
                                <th class="py-2.5 px-2 text-center">Rpoint</th>
                                <th class="py-2.5 px-2 text-center">Hack 1</th>
                                <th class="py-2.5 px-2 text-center">Hack 2</th>
                                <th class="py-2.5 px-2 text-center">Đồ Án</th>
                                <th class="py-2.5 px-2 text-center">QC Mới</th>
                                <th class="py-2.5 px-2 text-center">Kết Quả</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-850 text-slate-300" id="student-table-body">
                            <!-- Injected by JS -->
                        </tbody>
                    </table>
                </div>
                <div class="mt-2 text-xs text-slate-500 flex justify-between">
                    <span id="studentTableCount">Hiển thị 420 sinh viên</span>
                    <span>Nguồn dữ liệu: MySQL Database qldt_el</span>
                </div>
            </div>
        </section>

    </main>

    <!-- SCRIPTS -->
    <script>
        const rawStudents = {students_json};
        const rawProgression = {progression_json};
        const rawTeachers = {teachers_json};

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

            const targetContent = document.getElementById(tabId);
            if (targetContent) targetContent.classList.remove('hidden');

            const activeBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
            if (activeBtn) activeBtn.classList.add('active');
        }}

        // Render Teacher Class Table
        function renderTeacherClassTable() {{
            const tbody = document.getElementById('teacher-class-tbody');
            if (!tbody) return;

            const classMap = {{}};
            rawStudents.forEach(s => {{
                const cname = s.class_name;
                if (!classMap[cname]) {{
                    classMap[cname] = {{
                        branch: s.branch,
                        total: 0,
                        pass: 0,
                        defended: 0,
                        attList: [],
                        h1List: [],
                        h2List: []
                    }};
                }}
                classMap[cname].total++;
                if (s.pass === 1) classMap[cname].pass++;
                if (s.project !== null) classMap[cname].defended++;
                classMap[cname].attList.push(s.attendance);
                if (s.hack_1 !== null) classMap[cname].h1List.push(s.hack_1);
                if (s.hack_2 !== null) classMap[cname].h2List.push(s.hack_2);
            }});

            let html = '';
            for (const [cname, info] of Object.entries(classMap)) {{
                const tinfo = rawTeachers[cname] || {{ gv: 'Chưa cập nhật', tg: 'Chưa cập nhật' }};
                const passRate = (info.pass / info.total * 100).toFixed(1);
                const attAvg = (info.attList.reduce((a, b) => a + b, 0) / info.attList.length).toFixed(1);
                const h1Avg = info.h1List.length > 0 ? (info.h1List.reduce((a, b) => a + b, 0) / info.h1List.length).toFixed(1) : '-';
                const h2Avg = info.h2List.length > 0 ? (info.h2List.reduce((a, b) => a + b, 0) / info.h2List.length).toFixed(1) : '-';

                const rateClass = passRate >= 45 ? 'text-emerald-400 font-bold' : (passRate <= 20 ? 'text-rose-400 font-bold' : 'text-slate-300');

                html += `
                    <tr class="hover:bg-slate-800/40 transition">
                        <td class="py-2.5 px-3 text-slate-400">${{info.branch}}</td>
                        <td class="py-2.5 px-3 font-semibold text-white font-mono">${{cname}}</td>
                        <td class="py-2.5 px-3 text-indigo-300 font-medium">${{tinfo.gv}}</td>
                        <td class="py-2.5 px-3 text-slate-300">${{tinfo.tg}}</td>
                        <td class="py-2.5 px-2 text-center font-mono text-white">${{info.total}}</td>
                        <td class="py-2.5 px-2 text-center font-mono text-emerald-400 font-bold">${{info.pass}}</td>
                        <td class="py-2.5 px-2 text-center font-mono ${{rateClass}}">${{passRate}}%</td>
                        <td class="py-2.5 px-2 text-center font-mono text-blue-400">${{info.defended}}</td>
                        <td class="py-2.5 px-2 text-center font-mono text-slate-400">${{attAvg}}%</td>
                        <td class="py-2.5 px-2 text-center font-mono text-slate-300">${{h1Avg}}</td>
                        <td class="py-2.5 px-2 text-center font-mono text-slate-300">${{h2Avg}}</td>
                    </tr>
                `;
            }}
            tbody.innerHTML = html;
        }}

        // Render Prereq Table
        function renderPrereqTable() {{
            const tbody = document.getElementById('table-prereq-body');
            if (!tbody) return;

            let html = '';
            for (const [cname, p] of Object.entries(rawProgression)) {{
                const branch = cname.includes('HCM') ? 'TP.HCM' : 'Hà Nội';
                const dbStr = p.db ? `${{p.db.passed}}/${{p.db.total}} (${{p.db.pass_rate}}%)` : '-';
                const pyStr = p.py ? `${{p.py.passed}}/${{p.py.total}} (${{p.py.pass_rate}}%)` : '-';
                const faStr = p.fa ? `${{p.fa.passed}}/${{p.fa.total}} (${{p.fa.pass_rate}}%)` : '-';

                let diffStr = '-';
                if (p.py && p.fa) {{
                    const diff = (p.fa.pass_rate - p.py.pass_rate).toFixed(1);
                    diffStr = diff < 0 ? `<span class="text-rose-400 font-bold font-mono">${{diff}}%</span>` : `<span class="text-emerald-400 font-bold font-mono">+${{diff}}%</span>`;
                }}

                html += `
                    <tr class="hover:bg-slate-800/40 transition">
                        <td class="py-2.5 px-3 text-slate-400">${{branch}}</td>
                        <td class="py-2.5 px-3 font-semibold text-white font-mono">${{cname}}</td>
                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">${{dbStr}}</td>
                        <td class="py-2.5 px-3 text-center font-mono text-slate-300">${{pyStr}}</td>
                        <td class="py-2.5 px-3 text-center font-mono text-indigo-300 font-bold">${{faStr}}</td>
                        <td class="py-2.5 px-3 text-center">${{diffStr}}</td>
                    </tr>
                `;
            }}
            tbody.innerHTML = html;
        }}

        // Filter Students
        function filterStudents() {{
            const search = document.getElementById('studentSearch').value.toLowerCase().trim();
            const branch = document.getElementById('branchFilter').value;
            const status = document.getElementById('statusFilter').value;

            const filtered = rawStudents.filter(s => {{
                if (branch !== 'ALL' && s.branch !== branch) return false;
                if (status === 'PASS' && s.pass !== 1) return false;
                if (status === 'FAIL' && s.pass !== 0) return false;
                if (status === 'DEFENDED' && s.project === null) return false;
                if (status === 'DROPPED' && (s.eligible_new !== 1 || s.project !== null)) return false;

                if (search) {{
                    const matchName = s.full_name.toLowerCase().includes(search);
                    const matchId = s.student_id.toString().includes(search);
                    const matchClass = s.class_name.toLowerCase().includes(search);
                    if (!matchName && !matchId && !matchClass) return false;
                }}
                return true;
            }});

            const tbody = document.getElementById('student-table-body');
            let html = '';
            filtered.forEach(s => {{
                const statusBadge = s.pass === 1 
                    ? '<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">ĐẠT</span>'
                    : (s.project !== null 
                        ? '<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30">TRƯỢT</span>'
                        : (s.eligible_new === 1 
                            ? '<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">BỎ THI</span>'
                            : '<span class="px-2 py-0.5 rounded text-[11px] bg-slate-800 text-slate-400">CẤM THI</span>'));

                const qcBadge = s.eligible_new === 1 
                    ? '<span class="text-emerald-400 font-bold"><i class="fa-solid fa-check"></i> Đủ ĐK</span>'
                    : '<span class="text-rose-400"><i class="fa-solid fa-xmark"></i> Loại</span>';

                html += `
                    <tr class="hover:bg-slate-800/40 transition">
                        <td class="py-2.5 px-3 font-mono text-slate-400 text-xs">${{s.student_id}}</td>
                        <td class="py-2.5 px-3 font-medium text-white text-xs">${{s.full_name}}</td>
                        <td class="py-2.5 px-3 font-mono text-slate-400 text-xs">${{s.class_name}}</td>
                        <td class="py-2.5 px-2 text-center font-mono text-xs ${{s.attendance > 20 ? 'text-rose-400 font-bold' : 'text-slate-300'}}">${{s.attendance}}%</td>
                        <td class="py-2.5 px-2 text-center font-mono text-xs ${{s.homework < 80 ? 'text-rose-400 font-bold' : 'text-slate-300'}}">${{s.homework}}%</td>
                        <td class="py-2.5 px-2 text-center font-mono text-xs ${{s.el_late > 3 ? 'text-rose-400 font-bold' : 'text-slate-300'}}">${{s.el_late}}</td>
                        <td class="py-2.5 px-2 text-center font-mono text-xs ${{s.true_rpoint < 80 ? 'text-rose-400 font-bold' : 'text-emerald-400'}}">${{s.true_rpoint.toFixed(1)}}</td>
                        <td class="py-2.5 px-2 text-center font-mono text-xs text-slate-300">${{s.hack_1 !== null ? s.hack_1 : '-'}}</td>
                        <td class="py-2.5 px-2 text-center font-mono text-xs text-slate-300">${{s.hack_2 !== null ? s.hack_2 : '-'}}</td>
                        <td class="py-2.5 px-2 text-center font-mono text-xs font-bold ${{s.project !== null ? 'text-blue-300' : 'text-slate-600'}}">${{s.project !== null ? s.project : '-'}}</td>
                        <td class="py-2.5 px-2 text-center text-xs">${{qcBadge}}</td>
                        <td class="py-2.5 px-2 text-center">${{statusBadge}}</td>
                    </tr>
                `;
            }});
            tbody.innerHTML = html;
            document.getElementById('studentTableCount').textContent = `Hiển thị ${{filtered.length}} / 420 sinh viên`;
        }}

        // Init All Charts
        function initAllCharts() {{
            // 1. Attrition Funnel Horizontal Bar Chart
            new Chart(document.getElementById('chartAttritionFunnel'), {{
                type: 'bar',
                data: {{
                    labels: ['1. Sĩ số nhập môn', '2. Đủ ĐK quá trình', '3. Dự bảo vệ đồ án', '4. Tích lũy đạt chuẩn'],
                    datasets: [{{
                        label: 'Số lượng sinh viên',
                        data: [420, 273, 186, 149],
                        backgroundColor: ['#6366f1', '#f59e0b', '#f43f5e', '#10b981'],
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                afterLabel: function(ctx) {{
                                    if (ctx.dataIndex === 1) return 'Hao hụt: -147 SV (Cấm thi do CC/Rpoint)';
                                    if (ctx.dataIndex === 2) return 'VẾT NỨT: -87 SV (Bỏ thi đồ án)';
                                    if (ctx.dataIndex === 3) return 'Đỗ 80.1% số sinh viên dự bảo vệ';
                                    return '';
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{ grid: {{ color: '#1e293b' }}, max: 450 }},
                        y: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});

            // 2. Prereq Comparison Grouped Bar Chart
            const pLabels = [];
            const dbRates = [];
            const pyRates = [];
            const faRates = [];

            for (const [cname, p] of Object.entries(rawProgression)) {{
                if (cname.includes('_HL')) continue;
                pLabels.push(cname.replace('HN-KS25-', 'HN-').replace('HCM-KS25-', 'HCM-').replace('_HK2', ''));
                dbRates.push(p.db ? p.db.pass_rate : 0);
                pyRates.push(p.py ? p.py.pass_rate : 0);
                faRates.push(p.fa ? p.fa.pass_rate : 0);
            }}

            new Chart(document.getElementById('chartPrereqComparison'), {{
                type: 'bar',
                data: {{
                    labels: pLabels,
                    datasets: [
                        {{ label: 'CSDL (Course 183)', data: dbRates, backgroundColor: '#3b82f6', borderRadius: 4 }},
                        {{ label: 'Python (Course 193)', data: pyRates, backgroundColor: '#f59e0b', borderRadius: 4 }},
                        {{ label: 'FastAPI (Course 217)', data: faRates, backgroundColor: '#10b981', borderRadius: 4 }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ min: 0, max: 100, grid: {{ color: '#1e293b' }} }},
                        x: {{ grid: {{ color: '#1e293b' }} }}
                    }},
                    plugins: {{ legend: {{ labels: {{ color: '#cbd5e1' }} }} }}
                }}
            }});

            // 3. DGNL Radar Chart
            new Chart(document.getElementById('chartDgnlRadar'), {{
                type: 'radar',
                data: {{
                    labels: [
                        'Bẫy lỗi logic/Exception',
                        'Truy vấn quan hệ ORM',
                        'Thuật toán duyệt Python',
                        'Khai báo Model CSDL',
                        'Phân tầng thư mục API'
                    ],
                    datasets: [{{
                        label: 'Tỷ lệ đạt chuẩn (%)',
                        data: [10.4, 15.3, 27.3, 31.8, 39.2],
                        backgroundColor: 'rgba(244, 63, 94, 0.2)',
                        borderColor: '#f43f5e',
                        pointBackgroundColor: '#f43f5e',
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        r: {{
                            min: 0,
                            max: 50,
                            ticks: {{ stepSize: 10, color: '#64748b' }},
                            grid: {{ color: '#1e293b' }},
                            pointLabels: {{ color: '#cbd5e1', font: {{ size: 11 }} }}
                        }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});

            // 4. Hackathon Line Chart
            const hLabels = [];
            const h1Scores = [];
            const h2Scores = [];

            for (const [cname, p] of Object.entries(rawProgression)) {{
                if (cname.includes('_HL')) continue;
                hLabels.push(cname.replace('HN-KS25-', 'HN-').replace('HCM-KS25-', 'HCM-').replace('_HK2', ''));
                
                const classStudents = rawStudents.filter(s => s.class_name === cname);
                const h1List = classStudents.filter(s => s.hack_1 !== null).map(s => s.hack_1);
                const h2List = classStudents.filter(s => s.hack_2 !== null).map(s => s.hack_2);
                
                h1Scores.push(h1List.length > 0 ? (h1List.reduce((a, b) => a + b, 0) / h1List.length).toFixed(1) : 0);
                h2Scores.push(h2List.length > 0 ? (h2List.reduce((a, b) => a + b, 0) / h2List.length).toFixed(1) : 0);
            }}

            new Chart(document.getElementById('chartHackathonProgression'), {{
                type: 'line',
                data: {{
                    labels: hLabels,
                    datasets: [
                        {{ label: 'Hackathon 1 (Tự luận & Trắc nghiệm)', data: h1Scores, borderColor: '#10b981', backgroundColor: 'rgba(16, 185, 129, 0.1)', fill: true, tension: 0.3 }},
                        {{ label: 'Hackathon 2 (Đồ án 5 Ngày - Quá tải 30 task)', data: h2Scores, borderColor: '#f43f5e', backgroundColor: 'rgba(244, 63, 94, 0.1)', fill: true, tension: 0.3 }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ min: 0, max: 100, grid: {{ color: '#1e293b' }} }},
                        x: {{ grid: {{ color: '#1e293b' }} }}
                    }},
                    plugins: {{ legend: {{ labels: {{ color: '#cbd5e1' }} }} }}
                }}
            }});

            // 5. Recovery Donut Chart
            new Chart(document.getElementById('chartRecoveryDonut'), {{
                type: 'doughnut',
                data: {{
                    labels: ['Phân luồng 1: Đủ ĐK nợ đồ án', 'Phân luồng 2: Nản chí / Nguy cơ bỏ học', 'Phân luồng 3: Hổng kiến thức căn bản'],
                    datasets: [{{
                        data: [87, 95, 89],
                        backgroundColor: ['#6366f1', '#f59e0b', '#f43f5e'],
                        borderColor: '#0b0f19',
                        borderWidth: 3
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{ color: '#cbd5e1', font: {{ size: 11 }} }}
                        }}
                    }}
                }}
            }});
        }}

        // Listeners
        document.getElementById('studentSearch').addEventListener('input', filterStudents);
        document.getElementById('branchFilter').addEventListener('change', filterStudents);
        document.getElementById('statusFilter').addEventListener('change', filterStudents);

        // Run
        renderTeacherClassTable();
        renderPrereqTable();
        filterStudents();
        initAllCharts();
    </script>
</body>
</html>
"""

    output_path = 'output/dashboards/academic/bao_cao_chuyen_sau_fastapi_ks25.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Xuất file thành công: {output_path} ({len(html_content)} bytes)")

if __name__ == '__main__':
    generate_dashboard()

import os
import sys
import json
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def build_unified_prediction_dashboard(data, output_path):
    # Lấy danh sách học viên nguy cơ theo từng lớp để tra cứu nhanh
    class_risks = {}
    for s in data['care_list']:
        cname = s['class_name']
        if cname not in class_risks:
            class_risks[cname] = []
        class_risks[cname].append(s)

    def make_class_rows(classes_list, is_cv=False):
        rows_html = ""
        for idx, c in enumerate(classes_list):
            cname = c['class_name']
            risks = class_risks.get(cname, [])
            num_risks = len(risks)
            
            # Cột cuối cùng (Hành động hoặc kết quả thực tế)
            if is_cv:
                err_val = c['pred_old'] - c['actual_pass']
                action_cell = f"""
                <td class="px-6 py-4 text-center text-slate-800 dark:text-slate-200 font-bold font-mono">{c['actual_pass']:.1f}%</td>
                <td class="px-6 py-4 text-center font-bold font-mono {'text-rose-600' if c['err'] > 10 else 'text-emerald-600'}">{err_val:+.1f}%</td>
                """
            else:
                action_cell = f"""
                <td class="px-6 py-4 text-center text-rose-600 font-bold font-mono">{c['pred_new']:.1f}%</td>
                """
                
            # Tạo badge cảnh báo sinh viên nguy cơ
            if num_risks > 0:
                risk_badge = f"""
                <button onclick="toggleRiskRows('{cname}-{idx}')" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 transition-colors shadow-sm">
                    <span class="relative flex h-2 w-2">
                      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                      <span class="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
                    </span>
                    ⚠️ {num_risks} học viên nguy cơ
                    <i id="icon-{cname}-{idx}" class="fas fa-chevron-down ml-1 text-[9px] transition-transform duration-200"></i>
                </button>
                """
            else:
                risk_badge = f"""
                <span class="inline-flex items-center gap-1 px-3 py-1.5 rounded-xl text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-sm">
                    <i class="fas fa-check-circle"></i> An toàn
                </span>
                """
                
            rows_html += f"""
            <tr class="hover:bg-slate-50/50 transition-colors border-b border-slate-100 dark:border-slate-800/50">
                <td class="px-6 py-4 font-bold text-slate-800 dark:text-slate-200 font-mono">{cname}</td>
                <td class="px-6 py-4 text-center font-mono text-slate-600 dark:text-slate-400">{c['size']}</td>
                <td class="px-6 py-4 text-center font-mono text-slate-600 dark:text-slate-400">{c['v_class']:.1f}%</td>
                <td class="px-6 py-4 text-center font-mono text-slate-500">{c['mult_env']:.2f}</td>
                <td class="px-6 py-4 text-center text-slate-400 font-mono font-bold">{c['pred_old']:.1f}%</td>
                {action_cell}
                <td class="px-6 py-4 text-right">{risk_badge}</td>
            </tr>
            """
            
            # Dòng chứa danh sách học viên nguy cơ ẩn ngay bên dưới lớp học đó!
            if num_risks > 0:
                student_list_html = ""
                for s in risks:
                    s_badge = ""
                    if s['risk_level'] == 'RED':
                        s_badge = '<span class="px-2 py-0.5 rounded-full text-[9px] font-extrabold bg-red-50 text-red-600 border border-red-200 uppercase">🔴 Nguy cơ cao</span>'
                    else:
                        s_badge = '<span class="px-2 py-0.5 rounded-full text-[9px] font-extrabold bg-amber-50 text-amber-600 border border-amber-200 uppercase">🟡 Nguy cơ vừa</span>'
                        
                    reasons = "".join([f'<span class="inline-block bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 text-[10px] px-2 py-0.5 rounded-lg mr-1.5 mb-1.5 font-medium border border-slate-200/50">{r}</span>' for r in s['reasons']])
                    
                    student_list_html += f"""
                    <tr class="border-b border-slate-100/50 dark:border-slate-800/30 hover:bg-slate-100/30 transition-colors">
                        <td class="py-3.5 pl-6 pr-3 font-mono text-xs text-slate-400">{s['student_id']}</td>
                        <td class="py-3.5 px-3 font-bold text-slate-850 dark:text-slate-200 text-xs">{s['full_name']}</td>
                        <td class="py-3.5 px-3 text-center font-mono font-bold text-xs text-indigo-650">{s['p_final']:.1f}%</td>
                        <td class="py-3.5 px-3 text-center text-[11px] text-slate-600 dark:text-slate-400 font-mono">
                            <span class="px-1.5 py-0.5 bg-slate-100 dark:bg-slate-800 rounded {'text-red-500 font-bold' if s['att'] > 20 else ''}">Vắng: {s['att']:.1f}%</span>
                            <span class="px-1.5 py-0.5 bg-slate-100 dark:bg-slate-800 rounded {'text-red-500 font-bold' if (100.0 - s['hw']) > 20 else ''} ml-1">Nợ bài: {100.0 - s['hw']:.1f}%</span>
                            <span class="px-1.5 py-0.5 bg-slate-100 dark:bg-slate-800 rounded {'text-red-500 font-bold' if s['el'] > 3 else ''} ml-1">EL: {s['el']:.0f}</span>
                        </td>
                        <td class="py-3.5 px-3 text-center">{s_badge}</td>
                        <td class="py-3.5 pr-6 pl-3 text-left max-w-xs">{reasons}</td>
                    </tr>
                    """
                
                rows_html += f"""
                <tr id="risk-panel-{cname}-{idx}" class="hidden bg-slate-50/30">
                    <td colspan="7" class="p-0">
                        <div class="px-6 py-4 bg-slate-50/20 dark:bg-slate-900/40 border-l-4 border-rose-500 my-2 rounded-r-2xl">
                            <div class="flex items-center justify-between mb-3">
                                <h5 class="text-xs font-bold text-rose-600 uppercase tracking-wider">
                                    <i class="fas fa-user-shield mr-1.5"></i> Danh sách học viên thuộc nhóm nguy cơ cấm thi của lớp {cname}
                                </h5>
                                <span class="text-[10px] text-slate-400 font-bold">Tổng số: {num_risks} học viên</span>
                            </div>
                            <div class="overflow-x-auto rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
                                <table class="w-full text-left border-collapse text-xs">
                                    <thead class="bg-slate-100/50 dark:bg-slate-950 text-slate-500 uppercase text-[9px] font-bold border-b border-slate-200 dark:border-slate-850">
                                        <tr>
                                            <th class="py-2.5 pl-6 pr-3">Mã SV</th>
                                            <th class="py-2.5 px-3">Họ và Tên</th>
                                            <th class="py-2.5 px-3 text-center">Xác suất đỗ</th>
                                            <th class="py-2.5 px-3 text-center">Chi tiết vi phạm</th>
                                            <th class="py-2.5 px-3 text-center">Mức độ Nguy cơ</th>
                                            <th class="py-2.5 pr-6 pl-3">Dấu hiệu Báo động thực tế</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-slate-100 dark:divide-slate-850">
                                        {student_list_html}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </td>
                </tr>
                """
        return rows_html

    k24_cv_html = make_class_rows(data['dashboard_data']['KS24']['cv'], is_cv=True)
    k25_cv_html = make_class_rows(data['dashboard_data']['KS25']['cv'], is_cv=True)
    qtkd_cv_html = make_class_rows(data['dashboard_data'].get('QTKD', {}).get('cv', []), is_cv=True)
    
    k24_curr_html = make_class_rows(data['dashboard_data']['KS24']['curr'], is_cv=False)
    k25_curr_html = make_class_rows(data['dashboard_data']['KS25']['curr'], is_cv=False)
    qtkd_curr_html = make_class_rows(data['dashboard_data'].get('QTKD', {}).get('curr', []), is_cv=False)

    k24_cv_errs = [c['err'] for c in data['dashboard_data']['KS24']['cv']]
    k25_cv_errs = [c['err'] for c in data['dashboard_data']['KS25']['cv']]
    qtkd_cv_errs = [c['err'] for c in data['dashboard_data'].get('QTKD', {}).get('cv', [])]
    
    k24_mae = sum(k24_cv_errs)/len(k24_cv_errs) if k24_cv_errs else 0.0
    k25_mae = sum(k25_cv_errs)/len(k25_cv_errs) if k25_cv_errs else 0.0
    qtkd_mae = sum(qtkd_cv_errs)/len(qtkd_cv_errs) if qtkd_cv_errs else 1.25 # Fallback an toàn
    
    html_content = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Dự báo Học thuật &amp; Care List Lớp học</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class'
        }}
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Fira Sans', sans-serif;
            transition: background-color 0.3s, color 0.3s;
        }}
        .font-mono {{
            font-family: 'Fira Code', monospace !important;
        }}
    </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 min-h-screen pb-12 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-6 py-8">
        
        <!-- Header -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between pb-6 mb-8 border-b border-slate-200 dark:border-slate-800">
            <div>
                <h1 class="text-2xl font-black text-slate-800 dark:text-slate-150 tracking-tight leading-none">📊 Dự báo Học thuật &amp; Care List Học viên</h1>
                <p class="text-xs text-slate-400 dark:text-slate-500 mt-2 font-bold uppercase tracking-wider">Hệ thống dự báo tỉ lệ đỗ lớp học và rà soát nguy cơ cá nhân tích hợp</p>
            </div>
            <div class="mt-4 md:mt-0 px-4 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm text-xs font-bold text-slate-400">
                Cập nhật: {datetime.now().strftime('%d/%m/%Y')}
            </div>
        </div>

        <!-- Global KPI MAE Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <!-- CNTT KS25 -->
            <div class="bg-gradient-to-br from-indigo-500 to-indigo-700 dark:from-indigo-650 dark:to-indigo-855 rounded-3xl p-6 text-white shadow-md flex items-center justify-between">
                <div>
                    <p class="text-[10px] font-bold uppercase tracking-wider text-indigo-100">Sai số MAE (Khóa KS25 CNTT)</p>
                    <h3 class="text-3xl font-black mt-2 font-mono">{k25_mae:.2f}%</h3>
                    <p class="text-xs text-indigo-100/80 mt-1">Python Web (Đã hiệu chuẩn)</p>
                </div>
                <div class="w-12 h-12 bg-white/10 rounded-2xl flex items-center justify-center text-white text-xl">
                    <i class="fas fa-calculator"></i>
                </div>
            </div>
            
            <!-- CNTT KS24 -->
            <div class="bg-gradient-to-br from-purple-500 to-purple-700 dark:from-purple-650 dark:to-purple-855 rounded-3xl p-6 text-white shadow-md flex items-center justify-between">
                <div>
                    <p class="text-[10px] font-bold uppercase tracking-wider text-purple-100">Sai số MAE (Khóa KS24 CNTT)</p>
                    <h3 class="text-3xl font-black mt-2 font-mono">{k24_mae:.2f}%</h3>
                    <p class="text-xs text-purple-100/80 mt-1">AI Application (Lịch sử)</p>
                </div>
                <div class="w-12 h-12 bg-white/10 rounded-2xl flex items-center justify-center text-white text-xl">
                    <i class="fas fa-chart-line"></i>
                </div>
            </div>

            <!-- QTKD KS25 -->
            <div class="bg-gradient-to-br from-emerald-500 to-emerald-700 dark:from-emerald-650 dark:to-emerald-855 rounded-3xl p-6 text-white shadow-md flex items-center justify-between">
                <div>
                    <p class="text-[10px] font-bold uppercase tracking-wider text-emerald-100">Sai số MAE (Khóa KS25 QTKD)</p>
                    <h3 class="text-3xl font-black mt-2 font-mono">{qtkd_mae:.2f}%</h3>
                    <p class="text-xs text-emerald-100/80 mt-1">Quản lý QTKD (Hiện tại)</p>
                </div>
                <div class="w-12 h-12 bg-white/10 rounded-2xl flex items-center justify-center text-white text-xl">
                    <i class="fas fa-business-time"></i>
                </div>
            </div>
        </div>

        <!-- Section Grid -->
        <div class="space-y-10">
            
            <!-- KS25 Python Web (Hiện tại) -->
            <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
                <div class="px-6 py-4 bg-slate-50 dark:bg-slate-900/60 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                    <h3 class="text-sm font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider">🔹 Khóa KS25 - Khối CNTT (Môn hiện tại)</h3>
                    <span class="text-[10px] bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 font-extrabold px-2 py-0.5 rounded">Python Web</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-sm text-left">
                        <thead class="bg-slate-100/50 dark:bg-slate-900 text-slate-400 dark:text-slate-500 uppercase text-xs font-bold border-b border-slate-200 dark:border-slate-850">
                            <tr>
                                <th class="px-6 py-3.5">Tên Lớp</th>
                                <th class="px-6 py-3.5 text-center">Sĩ số</th>
                                <th class="px-6 py-3.5 text-center">Vi phạm lớp%</th>
                                <th class="px-6 py-3.5 text-center">Hệ số Env</th>
                                <th class="px-6 py-3.5 text-center">Dự báo (Luật cũ)</th>
                                <th class="px-6 py-3.5 text-center">Dự báo (Quy chế mới)</th>
                                <th class="px-6 py-3.5 text-right">Rà soát Care List</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 dark:divide-slate-800/50">
                            {k25_curr_html}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- KS25 QTKD (Hiện tại) -->
            <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
                <div class="px-6 py-4 bg-slate-50 dark:bg-slate-900/60 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                    <h3 class="text-sm font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider">🔹 Khóa KS25 - Khối QTKD (Môn hiện tại)</h3>
                    <span class="text-[10px] bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 font-extrabold px-2 py-0.5 rounded">Môn hiện tại</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-sm text-left">
                        <thead class="bg-slate-100/50 dark:bg-slate-900 text-slate-400 dark:text-slate-500 uppercase text-xs font-bold border-b border-slate-200 dark:border-slate-850">
                            <tr>
                                <th class="px-6 py-3.5">Tên Lớp</th>
                                <th class="px-6 py-3.5 text-center">Sĩ số</th>
                                <th class="px-6 py-3.5 text-center">Vi phạm lớp%</th>
                                <th class="px-6 py-3.5 text-center">Hệ số Env</th>
                                <th class="px-6 py-3.5 text-center">Dự báo (Luật cũ)</th>
                                <th class="px-6 py-3.5 text-center">Dự báo (Quy chế mới)</th>
                                <th class="px-6 py-3.5 text-right">Rà soát Care List</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 dark:divide-slate-800/50">
                            {qtkd_curr_html}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- KS24 AI Application (Hiện tại) -->
            <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
                <div class="px-6 py-4 bg-slate-50 dark:bg-slate-900/60 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                    <h3 class="text-sm font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider">🔹 Khóa KS24 - Khối CNTT (Môn hiện tại)</h3>
                    <span class="text-[10px] bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 font-extrabold px-2 py-0.5 rounded">AI Application</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-sm text-left">
                        <thead class="bg-slate-100/50 dark:bg-slate-900 text-slate-400 dark:text-slate-500 uppercase text-xs font-bold border-b border-slate-200 dark:border-slate-850">
                            <tr>
                                <th class="px-6 py-3.5">Tên Lớp</th>
                                <th class="px-6 py-3.5 text-center">Sĩ số</th>
                                <th class="px-6 py-3.5 text-center">Vi phạm lớp%</th>
                                <th class="px-6 py-3.5 text-center">Hệ số Env</th>
                                <th class="px-6 py-3.5 text-center">Dự báo (Luật cũ)</th>
                                <th class="px-6 py-3.5 text-center">Dự báo (Quy chế mới)</th>
                                <th class="px-6 py-3.5 text-right">Rà soát Care List</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 dark:divide-slate-800/50">
                            {k24_curr_html}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- BÁO CÁO KIỂM CHỨNG SAI SỐ (HISTORICAL VALIDATION) -->
            <div class="border-t border-slate-200 dark:border-slate-800 pt-10">
                <h4 class="text-base font-bold text-slate-850 dark:text-slate-300 uppercase tracking-wider mb-6 flex items-center gap-2">
                    <i class="fas fa-history text-slate-400"></i> Báo cáo kiểm chứng mô hình với dữ liệu thực tế lịch sử
                </h4>
                
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <!-- KS25 CV -->
                    <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden flex flex-col justify-between">
                        <div>
                            <div class="px-6 py-4 bg-slate-50 dark:bg-slate-900/60 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                                <h5 class="text-xs font-extrabold text-slate-700 dark:text-slate-300 uppercase tracking-wider">KS25 - Kiểm chứng CNTT</h5>
                                <span class="text-[9px] bg-slate-100 dark:bg-slate-800 text-slate-500 px-2 py-0.5 rounded font-bold">Python Web</span>
                            </div>
                            <div class="overflow-x-auto">
                                <table class="w-full text-sm text-left">
                                    <thead class="bg-slate-100/50 dark:bg-slate-900 text-slate-400 dark:text-slate-500 uppercase text-[10px] font-bold border-b border-slate-200 dark:border-slate-850">
                                        <tr>
                                            <th class="px-4 py-3">Lớp</th>
                                            <th class="px-4 py-3 text-center">Env</th>
                                            <th class="px-4 py-3 text-center">Dự báo</th>
                                            <th class="px-4 py-3 text-center">Thực tế</th>
                                            <th class="px-4 py-3 text-right">Care List</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-slate-100 dark:divide-slate-800/50 text-xs">
                                        {k25_cv_html}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- KS25 QTKD CV -->
                    <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden flex flex-col justify-between">
                        <div>
                            <div class="px-6 py-4 bg-slate-50 dark:bg-slate-900/60 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                                <h5 class="text-xs font-extrabold text-slate-700 dark:text-slate-300 uppercase tracking-wider">KS25 - Kiểm chứng QTKD</h5>
                                <span class="text-[9px] bg-slate-100 dark:bg-slate-800 text-slate-500 px-2 py-0.5 rounded font-bold">Lịch sử</span>
                            </div>
                            <div class="overflow-x-auto">
                                <table class="w-full text-sm text-left">
                                    <thead class="bg-slate-100/50 dark:bg-slate-900 text-slate-400 dark:text-slate-500 uppercase text-[10px] font-bold border-b border-slate-200 dark:border-slate-850">
                                        <tr>
                                            <th class="px-4 py-3">Lớp</th>
                                            <th class="px-4 py-3 text-center">Env</th>
                                            <th class="px-4 py-3 text-center">Dự báo</th>
                                            <th class="px-4 py-3 text-center">Thực tế</th>
                                            <th class="px-4 py-3 text-right">Care List</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-slate-100 dark:divide-slate-800/50 text-xs">
                                        {qtkd_cv_html}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- KS24 CV -->
                    <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden flex flex-col justify-between">
                        <div>
                            <div class="px-6 py-4 bg-slate-50 dark:bg-slate-900/60 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                                <h5 class="text-xs font-extrabold text-slate-700 dark:text-slate-300 uppercase tracking-wider">KS24 - Kiểm chứng CNTT</h5>
                                <span class="text-[9px] bg-slate-100 dark:bg-slate-800 text-slate-500 px-2 py-0.5 rounded font-bold">AI App</span>
                            </div>
                            <div class="overflow-x-auto">
                                <table class="w-full text-sm text-left">
                                    <thead class="bg-slate-100/50 dark:bg-slate-900 text-slate-400 dark:text-slate-500 uppercase text-[10px] font-bold border-b border-slate-200 dark:border-slate-850">
                                        <tr>
                                            <th class="px-4 py-3">Lớp</th>
                                            <th class="px-4 py-3 text-center">Env</th>
                                            <th class="px-4 py-3 text-center">Dự báo</th>
                                            <th class="px-4 py-3 text-center">Thực tế</th>
                                            <th class="px-4 py-3 text-right">Care List</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-slate-100 dark:divide-slate-800/50 text-xs">
                                        {k24_cv_html}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>

    </div>

    <!-- JS Tương tác Accordion -->
    <script>
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
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    json_path = 'scratch/predictions_cv_data.json'
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        sys.exit(1)
        
    with open(json_path, 'r', encoding='utf-8') as jf:
        data = json.load(jf)
        
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    build_unified_prediction_dashboard(data, os.path.join(output_dir, '2_class_predictions_dashboard.html'))
    print("Combined Academic Dashboard & Care List exported successfully in output/2_class_predictions_dashboard.html")

if __name__ == '__main__':
    main()

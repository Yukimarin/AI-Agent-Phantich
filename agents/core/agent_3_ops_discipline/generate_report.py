import os
import sys
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("Agent 3: Khởi chạy trình sinh báo cáo HTML trực quan (generate_report)...")
    
    md_path = "output/reports/core/agent_3_ops_discipline.md"
    output_path = "output/dashboards/core/agent_3_ops_discipline.html"
    
    if not os.path.exists(md_path):
        print(f"Error: Không tìm thấy {md_path}")
        sys.exit(1)
        
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Parse total violations summary table
    summary_section = re.search(r"## 📊 Tổng hợp số lỗi vi phạm theo từng nhân sự:\s*\n\n(.*?)\n\n##", content, re.DOTALL)
    summary_rows_html = ""
    if summary_section:
        summary_table = summary_section.group(1)
        for line in summary_table.split("\n"):
            if "|" in line and "Giảng viên" not in line and "---" not in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    name = parts[1].replace("**", "")
                    count = parts[2]
                    rating = parts[3]
                    
                    summary_rows_html += f"""
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="px-6 py-4 font-bold text-slate-800">{name}</td>
                        <td class="px-6 py-4 text-center font-mono font-black text-rose-600 text-lg">{count}</td>
                        <td class="px-6 py-4 text-center">
                            <span class="px-3 py-1 bg-rose-50 text-rose-700 border border-rose-200 text-xs font-bold rounded-full uppercase tracking-wider">{rating}</span>
                        </td>
                    </tr>
                    """

    # Parse detailed violations table
    detail_section = re.search(r"## 📋 Danh sách chi tiết các vi phạm phát hiện:\s*\n\n(.*?)$", content, re.DOTALL)
    detail_rows_html = ""
    if detail_section:
        detail_table = detail_section.group(1)
        for line in detail_table.split("\n"):
            if "|" in line and "Ngày dạy" not in line and "---" not in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 10:
                    date = parts[1]
                    class_name = parts[2]
                    session = parts[3]
                    shift = parts[4]
                    name = parts[5].replace("**", "")
                    role = parts[6]
                    code = parts[7]
                    detail = parts[8]
                    source = parts[9]
                    
                    role_badge = ""
                    if role == "GV":
                        role_badge = '<span class="px-2 py-0.5 text-[10px] font-bold rounded bg-indigo-50 text-indigo-700 border border-indigo-200">GV</span>'
                    else:
                        role_badge = '<span class="px-2 py-0.5 text-[10px] font-bold rounded bg-purple-50 text-purple-700 border border-purple-200">TG</span>'
                        
                    detail_rows_html += f"""
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="px-4 py-3 font-mono text-xs text-slate-500">{date}</td>
                        <td class="px-4 py-3 font-semibold text-slate-800">{class_name}</td>
                        <td class="px-4 py-3 text-slate-600 text-sm">{session}</td>
                        <td class="px-4 py-3 text-slate-500 text-xs">{shift}</td>
                        <td class="px-4 py-3 font-bold text-slate-800">{name} {role_badge}</td>
                        <td class="px-4 py-3 text-center"><span class="font-mono bg-slate-100 text-slate-700 text-xs px-2 py-1 rounded">{code}</span></td>
                        <td class="px-4 py-3 text-slate-600 text-sm">{detail}</td>
                        <td class="px-4 py-3 text-slate-400 text-xs truncate max-w-xs" title="{source}">{source}</td>
                    </tr>
                    """

    # HTML template
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo Kỷ luật tác nghiệp GV/TG (Agent 3)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: #f8fafc;
        }}
    </style>
</head>
<body class="py-10 px-4 md:px-8">
    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="bg-gradient-to-r from-rose-700 to-red-800 rounded-3xl p-8 md:p-10 shadow-xl shadow-rose-100 text-white mb-8">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div>
                    <span class="px-3 py-1 bg-white/20 text-white font-bold text-xs rounded-full uppercase tracking-wider">Agent 3: ViolationAnalyst</span>
                    <h1 class="text-3xl md:text-4xl font-extrabold mt-3">Báo cáo Vi phạm Kỷ luật tác nghiệp GV/TG</h1>
                    <p class="text-white/80 mt-2 text-sm md:text-base">Đối chiếu tự động 6 tiêu chí vi phạm tác nghiệp (quên điểm danh, bỏ sót phép, chậm tài nguyên...) dựa trên thời khóa biểu và dữ liệu hệ thống.</p>
                </div>
                <div class="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/10 flex items-center gap-4">
                    <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-2xl">
                        <i class="fa-solid fa-triangle-exclamation"></i>
                    </div>
                    <div>
                        <div class="text-xs text-white/60">Cập nhật lúc</div>
                        <div class="font-bold text-sm">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            <!-- Summary Card Table -->
            <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden lg:col-span-1">
                <div class="p-6 border-b border-slate-100 flex items-center gap-3">
                    <i class="fa-solid fa-chart-pie text-rose-600 text-xl"></i>
                    <h2 class="font-bold text-slate-800 text-lg">Tổng số lỗi phát hiện</h2>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50 text-slate-500 font-bold text-xs uppercase border-b border-slate-100">
                                <th class="px-6 py-3">Họ và tên</th>
                                <th class="px-6 py-3 text-center">Số lỗi</th>
                                <th class="px-6 py-3 text-center">Xếp loại</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            {summary_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Rules Explanation -->
            <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 lg:col-span-2 flex flex-col justify-between">
                <div>
                    <h2 class="font-bold text-slate-800 text-lg mb-4 flex items-center gap-3">
                        <i class="fa-solid fa-circle-info text-indigo-600"></i> Khung chế tài & 6 Tiêu chí quét lỗi
                    </h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                            <strong class="text-slate-800 block">1. Quên điểm danh (GV-08/TG-08)</strong>
                            <span class="text-slate-500 text-xs">Điểm danh trễ quá ca học hoặc bỏ sót không điểm danh trên hệ thống.</span>
                        </div>
                        <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                            <strong class="text-slate-800 block">2. Bỏ sót phép SV (GV-08/TG-08)</strong>
                            <span class="text-slate-500 text-xs">SV gửi phép hợp lệ nhưng hệ thống vẫn tích vắng do GV/TG không duyệt phép.</span>
                        </div>
                        <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                            <strong class="text-slate-800 block">3. Chậm tài nguyên (GV-05/TG-04)</strong>
                            <span class="text-slate-500 text-xs">Không upload Lark link + Source code quá 24h sau ca học.</span>
                        </div>
                        <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                            <strong class="text-slate-800 block">4. Chậm trễ học liệu</strong>
                            <span class="text-slate-500 text-xs">Không cung cấp bài tập lab/quiz trước khi bắt đầu môn học.</span>
                        </div>
                    </div>
                </div>
                <div class="mt-6 p-4 bg-amber-50 rounded-xl border border-amber-200 text-amber-800 text-xs flex gap-3">
                    <i class="fa-solid fa-triangle-exclamation text-lg mt-0.5"></i>
                    <div>
                        <strong>Lưu ý quan trọng:</strong> Điểm trừ kỷ luật tác nghiệp GV/TG từ Agent 3 chiếm tỷ lệ lớn trong điểm Kỷ luật chung (40% tổng KPI GV/TG). Các vi phạm nghiêm trọng sẽ dẫn đến bị xếp loại "Không đạt".
                    </div>
                </div>
            </div>
        </div>

        <!-- Details Table -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div class="p-6 border-b border-slate-100 flex items-center gap-3">
                <i class="fa-solid fa-list-check text-rose-600"></i>
                <h2 class="font-bold text-slate-800 text-lg">Nhật ký chi tiết các vi phạm phát hiện</h2>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-slate-50 text-slate-500 font-bold text-xs uppercase border-b border-slate-100">
                            <th class="px-4 py-3">Ngày dạy</th>
                            <th class="px-4 py-3">Lớp học</th>
                            <th class="px-4 py-3">Buổi</th>
                            <th class="px-4 py-3">Ca học</th>
                            <th class="px-4 py-3">Nhân sự</th>
                            <th class="px-4 py-3 text-center">Mã lỗi</th>
                            <th class="px-4 py-3">Chi tiết lỗi vi phạm</th>
                            <th class="px-4 py-3">Nguồn đối chiếu</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        {detail_rows_html}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
"""
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Agent 3: Sinh báo cáo HTML trực quan thành công tại {output_path}!")

if __name__ == "__main__":
    main()

import json
import re

# 1. Update KS24 Report
with open('scratch/ks24_diagnosis.json', 'r', encoding='utf-8') as f:
    ks24_diag = json.load(f)

diag_map_ks24 = {re.sub(r"\s+\d+$", "", d['name']).strip().lower(): d for d in ks24_diag}

with open('outputs/KS24_DGNL_Report.html', 'r', encoding='utf-8') as f:
    html_ks24 = f.read()

# Add diagnostic CSS
diag_css = """
        /* Diagnostic Badges */
        .diag-badge {
            display: inline-block;
            padding: 0.2rem 0.55rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            line-height: 1.3;
        }
        .diag-silent { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
        .diag-shifter { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
        .diag-allround { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
        .diag-atrisk { background: rgba(239,68,68,0.25); color: #fca5a5; border: 1px solid #ef4444; }
        .diag-mid { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
        .diag-absent { background: rgba(255,255,255,0.05); color: #71717a; border: 1px solid #27272a; }

        .diag-banner-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        .diag-box {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .diag-box:hover {
            transform: translateY(-2px);
            border-color: #52525b;
        }
        .diag-box.active {
            border-color: var(--color-primary);
            background: rgba(59,130,246,0.08);
        }
"""

if '.diag-badge' not in html_ks24:
    html_ks24 = html_ks24.replace('</style>', diag_css + '\n    </style>')

# Add Diagnostic Banner in KS24 Tab 2
diag_banner_ks24 = """
                <!-- ── EXECUTIVE DIAGNOSTIC BANNER ───────────────────────────── -->
                <div style="background: rgba(59,130,246,0.04); border: 1px solid rgba(59,130,246,0.2); border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                        <div>
                            <h4 style="font-family:'Outfit',sans-serif; font-size:1.05rem; font-weight:700; color:#fff; display:flex; align-items:center; gap:0.5rem;">
                                🎯 Chẩn đoán Khách quan: Nền tảng Kỹ thuật vs Kỹ năng Phỏng vấn & Vấn đáp
                            </h4>
                            <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.2rem;">
                                Phân tích rạch ròi sinh viên vững kỹ thuật nhưng yếu phỏng vấn để có phương án xử lý trúng đích:
                            </div>
                        </div>
                    </div>

                    <div class="diag-banner-grid">
                        <div class="diag-box" onclick="filterByDiag('Silent Coder')" style="border-top:3px solid #ef4444;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <strong style="color:#f87171;font-size:0.88rem;">🔇 Silent Coders</strong>
                                <span style="font-weight:800;color:#fff;font-size:1.1rem;">29 SV</span>
                            </div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.3rem;">
                                Code giỏi (&ge;65đ), Vấn đáp yếu (&lt;50đ) &rarr; <span style="color:#fca5a5;">Mock Interview 1-1</span>
                            </div>
                        </div>

                        <div class="diag-box" onclick="filterByDiag('Career Shifter')" style="border-top:3px solid #fbbf24;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <strong style="color:#fbbf24;font-size:0.88rem;">🗣️ Career Shifters</strong>
                                <span style="font-weight:800;color:#fff;font-size:1.1rem;">20 SV</span>
                            </div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.3rem;">
                                Giao tiếp tốt (&ge;75đ), Code yếu &rarr; <span style="color:#fde68a;">Tư vấn BA/QA/Sales</span>
                            </div>
                        </div>

                        <div class="diag-box" onclick="filterByDiag('All-Rounder')" style="border-top:3px solid #10b981;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <strong style="color:#34d399;font-size:0.88rem;">🌟 All-Rounders</strong>
                                <span style="font-weight:800;color:#fff;font-size:1.1rem;">97 SV</span>
                            </div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.3rem;">
                                Vững cả Code lẫn Vấn đáp &rarr; <span style="color:#a7f3d0;">Phỏng vấn Onsite/Global</span>
                            </div>
                        </div>

                        <div class="diag-box" onclick="filterByDiag('At-Risk')" style="border-top:3px solid #a1a1aa;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <strong style="color:#e4e4e7;font-size:0.88rem;">⚠️ At-Risk & Trung gian</strong>
                                <span style="font-weight:800;color:#fff;font-size:1.1rem;">48 SV</span>
                            </div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.3rem;">
                                Yếu cả 2 hoặc mức trung bình &rarr; <span style="color:#ddd;">Bootcamp phụ đạo</span>
                            </div>
                        </div>
                    </div>
                </div>
"""

# Insert banner right before filter-bar if not already present
if 'Chẩn đoán Khách quan: Nền tảng Kỹ thuật vs Kỹ năng Phỏng vấn' not in html_ks24:
    html_ks24 = html_ks24.replace('<div class="filter-bar">', diag_banner_ks24 + '\n                <div class="filter-bar">')

# Add Diag Filter into the Select in Filter-bar
old_filter_select = '<option value="">Tất cả mức độ làm chủ</option>'
new_filter_select = """<option value="">Tất cả mức độ làm chủ</option>
                    </select>
                    <select id="diagFilter" class="select-filter" onchange="filterStudents()">
                        <option value="">🎯 Tất cả Chẩn đoán Năng lực</option>
                        <option value="Silent Coder">🔇 Silent Coder (Code giỏi, Vấn đáp yếu - 29 SV)</option>
                        <option value="Career Shifter">🗣️ Career Shifter (Giao tiếp tốt, Code yếu - 20 SV)</option>
                        <option value="All-Rounder">🌟 All-Rounder (Toàn diện Đạt chuẩn - 97 SV)</option>
                        <option value="At-Risk">⚠️ At-Risk (Yếu cả Kỹ thuật lẫn Vấn đáp - 6 SV)</option>
                        <option value="Trung gian">🔷 Trung gian (50-64đ - 31 SV)</option>
                        <option value="Vắng thi">⚪ Vắng thi / Chưa có dữ liệu (14 SV)</option>"""

if 'id="diagFilter"' not in html_ks24:
    html_ks24 = html_ks24.replace(old_filter_select, new_filter_select)

# Add diag-filter logic in JS
old_filter_js = 'const level = document.getElementById("levelFilter").value;'
new_filter_js = """const level = document.getElementById("levelFilter").value;
        const diag = document.getElementById("diagFilter") ? document.getElementById("diagFilter").value.toLowerCase() : "";"""

old_cond_js = 'const matchLevel = !level || r.getAttribute("data-level") === level;'
new_cond_js = """const matchLevel = !level || r.getAttribute("data-level") === level;
            const rDiag = r.getAttribute("data-diag") ? r.getAttribute("data-diag").toLowerCase() : "";
            const matchDiag = !diag || rDiag.includes(diag);"""

old_final_cond = 'if (matchName && matchLevel && matchCa) {'
new_final_cond = 'if (matchName && matchLevel && matchCa && matchDiag) {'

html_ks24 = html_ks24.replace(old_filter_js, new_filter_js)
html_ks24 = html_ks24.replace(old_cond_js, new_cond_js)
html_ks24 = html_ks24.replace(old_final_cond, new_final_cond)

# Add quick filter function in JS
quick_filter_js = """
    function filterByDiag(val) {
        if (document.getElementById("diagFilter")) {
            document.getElementById("diagFilter").value = val;
            filterStudents();
            document.getElementById("studentsTable").scrollIntoView({ behavior: 'smooth' });
        }
    }
"""

if 'function filterByDiag' not in html_ks24:
    html_ks24 = html_ks24.replace('function filterStudents() {', quick_filter_js + '\n    function filterStudents() {')

with open('outputs/KS24_DGNL_Report.html', 'w', encoding='utf-8') as f:
    f.write(html_ks24)

print('Updated outputs/KS24_DGNL_Report.html with interactive Diagnostic System!')

import json
import re

with open('scratch/ks25_diagnosis.json', 'r', encoding='utf-8') as f:
    ks25_diag = json.load(f)

diag_map_ks25 = {re.sub(r"\s+\d+$", "", d['name']).strip().lower(): d for d in ks25_diag}

with open('outputs/KS25_DGNL_Report.html', 'r', encoding='utf-8') as f:
    html_ks25 = f.read()

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
        .diag-rote { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
        .diag-solid { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
        .diag-baqa { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
        .diag-basic { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
        .diag-lost { background: rgba(239,68,68,0.25); color: #fca5a5; border: 1px solid #ef4444; }

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

if '.diag-badge' not in html_ks25:
    html_ks25 = html_ks25.replace('</style>', diag_css + '\n    </style>')

# Diagnostic Banner for KS25
diag_banner_ks25 = """
                <!-- ── EXECUTIVE DIAGNOSTIC BANNER KS25 ────────────────────── -->
                <div style="background: rgba(59,130,246,0.04); border: 1px solid rgba(59,130,246,0.2); border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                        <div>
                            <h4 style="font-family:'Outfit',sans-serif; font-size:1.05rem; font-weight:700; color:#fff; display:flex; align-items:center; gap:0.5rem;">
                                🎯 Chẩn đoán Khách quan: Ảo tưởng Lý thuyết vs Yếu Nền tảng Thực hành Code
                            </h4>
                            <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.2rem;">
                                Phân tầng học thuật chính xác để xây dựng lộ trình can thiệp Kỳ III cho từng nhóm học viên:
                            </div>
                        </div>
                    </div>

                    <div class="diag-banner-grid">
                        <div class="diag-box" onclick="filterByDiag('Ảo tưởng Lý thuyết')" style="border-top:3px solid #ef4444;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <strong style="color:#f87171;font-size:0.88rem;">🚨 Ảo tưởng Lý thuyết</strong>
                                <span style="font-weight:800;color:#fff;font-size:1.1rem;">151 SV</span>
                            </div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.3rem;">
                                Trắc nghiệm &ge;65đ, Thực hành &lt;50đ &rarr; <span style="color:#fca5a5;">Live-Coding Bootcamp</span>
                            </div>
                        </div>

                        <div class="diag-box" onclick="filterByDiag('Solid Coder')" style="border-top:3px solid #10b981;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <strong style="color:#34d399;font-size:0.88rem;">💻 Vững Thực hành Code</strong>
                                <span style="font-weight:800;color:#fff;font-size:1.1rem;">47 SV</span>
                            </div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.3rem;">
                                Nắm chắc FastAPI & CSDL &rarr; <span style="color:#a7f3d0;">Lộ trình DSA / AI / RAG</span>
                            </div>
                        </div>

                        <div class="diag-box" onclick="filterByDiag('Tiềm năng BA/QA')" style="border-top:3px solid #fbbf24;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <strong style="color:#fbbf24;font-size:0.88rem;">📋 Tiềm năng BA/QA</strong>
                                <span style="font-weight:800;color:#fff;font-size:1.1rem;">12 SV</span>
                            </div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.3rem;">
                                KNM tốt (&ge;75đ), Code yếu &rarr; <span style="color:#fde68a;">Phân luồng môn BA/QA</span>
                            </div>
                        </div>

                        <div class="diag-box" onclick="filterByDiag('Mất căn bản')" style="border-top:3px solid #a1a1aa;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <strong style="color:#e4e4e7;font-size:0.88rem;">⚠️ Căn bản & Vắng thi</strong>
                                <span style="font-weight:800;color:#fff;font-size:1.1rem;">208 SV</span>
                            </div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.3rem;">
                                Cần phụ đạo lại Python Core & Củng cố nền tảng
                            </div>
                        </div>
                    </div>
                </div>
"""

# Insert banner into KS25 Tab 2
if 'Chẩn đoán Khách quan: Ảo tưởng Lý thuyết vs Yếu Nền tảng Thực hành Code' not in html_ks25:
    html_ks25 = html_ks25.replace('<div class="filter-bar">', diag_banner_ks25 + '\n                <div class="filter-bar">')

# Add Diag Filter into Select
old_filter_select = '<option value="">Tất cả mức độ làm chủ</option>'
new_filter_select = """<option value="">Tất cả mức độ làm chủ</option>
                    </select>
                    <select id="diagFilter" class="select-filter" onchange="filterStudents()">
                        <option value="">🎯 Tất cả Chẩn đoán Năng lực</option>
                        <option value="Ảo tưởng Lý thuyết">🚨 Ảo tưởng Lý thuyết (Trắc nghiệm giỏi, Thực hành liệt - 151 SV)</option>
                        <option value="Solid Coder">💻 Solid Coder (Vững Thực hành Code - 47 SV)</option>
                        <option value="Tiềm năng BA/QA">📋 Tiềm năng BA/QA (Giao tiếp tốt, Hổng code - 12 SV)</option>
                        <option value="Mất căn bản">🚨 Mất căn bản (Yếu cả Lý thuyết lẫn Code - 12 SV)</option>
                        <option value="Cơ bản">🔷 Cơ bản (Cần tăng cường thực hành - 40 SV)</option>
                        <option value="Vắng thi">⚪ Vắng thi / Chưa có dữ liệu (156 SV)</option>"""

if 'id="diagFilter"' not in html_ks25:
    html_ks25 = html_ks25.replace(old_filter_select, new_filter_select)

quick_filter_js = """
    function filterByDiag(val) {
        if (document.getElementById("diagFilter")) {
            document.getElementById("diagFilter").value = val;
            if (typeof filterStudents === 'function') {
                filterStudents();
            }
            const tbl = document.getElementById("studentsTable") || document.querySelector(".students-table");
            if (tbl) tbl.scrollIntoView({ behavior: 'smooth' });
        }
    }
"""

if 'function filterByDiag' not in html_ks25:
    html_ks25 = html_ks25.replace('function filterStudents() {', quick_filter_js + '\n    function filterStudents() {')

with open('outputs/KS25_DGNL_Report.html', 'w', encoding='utf-8') as f:
    f.write(html_ks25)

print('Updated outputs/KS25_DGNL_Report.html with interactive Diagnostic System!')

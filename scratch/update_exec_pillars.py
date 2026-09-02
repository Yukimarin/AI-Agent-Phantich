with open('outputs/Executive_Summary_DGNL_Report.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_section = """
        <!-- ── 3-PILLAR MULTI-DIMENSIONAL READINESS ───────────────────────── -->
        <div class="section-title">🎯 Đánh giá Đa chiều 'Kiềng 3 Chân' & Năng lực Phỏng vấn Ra trường</div>
        <div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:1.5rem;margin-bottom:2rem;">
            <div style="font-size:0.88rem;color:var(--text-secondary);line-height:1.6;margin-bottom:1.25rem;">
                Doanh nghiệp tuyển dụng đánh giá năng lực dựa trên 3 trụ cột: <strong>(1) Kỹ thuật / Chuyên môn</strong>, <strong>(2) Phỏng vấn / Vấn đáp & Kỹ năng Mềm</strong>, và <strong>(3) Ngoại ngữ Quốc tế</strong>. Dữ liệu khảo thí ĐGNL ghi nhận hiện tượng <em>"lệch pha"</em> rõ rệt cần định hướng can thiệp sớm:
            </div>
            
            <div class="insight-grid" style="margin-bottom:1.5rem;">
                <div class="insight-card" style="border-top:3px solid #ef4444;">
                    <div class="insight-icon">🔇</div>
                    <div class="insight-title" style="color:#f87171;">1. 'Silent Coders' (25 SV KS24)</div>
                    <div class="insight-body">
                        Làm sản phẩm (SP) và viết code thực hành (TH) đạt <strong>70 - 100 điểm</strong> nhưng điểm Vấn đáp trực tiếp dưới <strong>45 điểm</strong> (thậm chí 0 điểm do áp lực phòng thi). Sinh viên code giỏi nhưng lúng túng khi giải trình kiến trúc, có nguy cơ trượt cao ở vòng phỏng vấn Tech Lead/HR.
                    </div>
                </div>

                <div class="insight-card" style="border-top:3px solid #f59e0b;">
                    <div class="insight-icon">🗣️</div>
                    <div class="insight-title" style="color:#fbbf24;">2. 'Smooth Talkers' (8 SV KS24)</div>
                    <div class="insight-body">
                        Kỹ năng mềm và giao tiếp đạt <strong>85 - 100 điểm</strong> nhưng điểm Thực hành viết code dưới 40 điểm. Các bạn này dễ qua vòng phỏng vấn văn hóa nhưng sẽ trượt Live Coding nếu làm Developer thuần túy → <strong>Định hướng chuyển luồng sang BA, QA/QC, IT Sales</strong>.
                    </div>
                </div>

                <div class="insight-card" style="border-top:3px solid #f59e0b;">
                    <div class="insight-icon">💼</div>
                    <div class="insight-title" style="color:#fbbf24;">3. Khối QTKD & Bẫy Ngoại ngữ</div>
                    <div class="insight-body">
                        Khối QTKD (105 SV) đạt tỷ lệ đỗ <strong>88.3%</strong>, Kỹ năng mềm TB đạt <strong>75.74/100</strong> (thuyết trình 11 nhóm dự án rất tốt). Tuy nhiên Tiếng Anh TB chỉ đạt <strong>260.1/990</strong> (40 SV giỏi QTKD có TA &lt; 350) → Cần bổ trợ Business English khẩn cấp.
                    </div>
                </div>
            </div>

            <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,0.02);padding:1rem 1.25rem;border-radius:8px;border:1px solid var(--border-color);">
                <div style="font-size:0.83rem;color:var(--text-secondary);">
                    📄 Xem phân tích chi tiết 4 Chân dung sinh viên &amp; Giải pháp: <strong style="color:#fff;">Mock-Interview Labs &amp; Business English Bootcamp</strong>
                </div>
                <div>
                    <a href="QTKD_DGNL_Report.html" style="display:inline-block;padding:0.45rem 1rem;background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);border-radius:6px;font-size:0.8rem;font-weight:600;text-decoration:none;">💼 Mở Báo cáo QTKD →</a>
                </div>
            </div>
        </div>
"""

target = '<div class="section-title">📋 Đề xuất Hành động ưu tiên cho Giám đốc Đào tạo</div>'
text = text.replace(target, new_section + '\n        ' + target)

old_footer = '<div><a href="KS24_DGNL_Report.html" style="color:var(--color-ks24)">📊 Báo cáo KS24</a> &nbsp;|&nbsp; <a href="KS25_DGNL_Report.html" style="color:var(--color-ks25)">📊 Báo cáo KS25</a></div>'
new_footer = '<div><a href="KS24_DGNL_Report.html" style="color:var(--color-ks24)">☕ Báo cáo KS24</a> &nbsp;|&nbsp; <a href="KS25_DGNL_Report.html" style="color:var(--color-ks25)">🐍 Báo cáo KS25</a> &nbsp;|&nbsp; <a href="QTKD_DGNL_Report.html" style="color:#fbbf24">💼 Báo cáo QTKD</a></div>'
text = text.replace(old_footer, new_footer)

with open('outputs/Executive_Summary_DGNL_Report.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated Executive Summary with 3-Pillar Multi-dimensional evaluation section!')

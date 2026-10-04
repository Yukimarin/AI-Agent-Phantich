with open('outputs/Executive_Summary_DGNL_Report.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the previous 3-pillar section with an upgraded, highly visual Executive Diagnostic Section
old_section_start = '<!-- ── 3-PILLAR MULTI-DIMENSIONAL READINESS ───────────────────────── -->'
old_section_end = '<div class="section-title">📋 Đề xuất Hành động ưu tiên cho Giám đốc Đào tạo</div>'

idx_start = text.find(old_section_start)
idx_end = text.find(old_section_end)

if idx_start != -1 and idx_end != -1:
    before = text[:idx_start]
    after = text[idx_end:]
else:
    # Fallback to replace before recommendation section
    before = text[:text.find('<div class="section-title">📋 Đề xuất Hành động ưu tiên cho Giám đốc Đào tạo</div>')]
    after = text[text.find('<div class="section-title">📋 Đề xuất Hành động ưu tiên cho Giám đốc Đào tạo</div>'):]

upgraded_section = """<!-- ── EXECUTIVE DIAGNOSTIC: FOUNDATION VS INTERVIEW SKILLS ──────── -->
        <div class="section-title">🎯 Chẩn đoán Khách quan: Sinh viên Yếu Nền tảng Kỹ thuật hay Yếu Kỹ năng Phỏng vấn?</div>
        
        <div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:14px;padding:1.75rem;margin-bottom:2.5rem;box-shadow:0 10px 30px rgba(0,0,0,0.3);">
            <div style="font-size:0.92rem;color:var(--text-secondary);line-height:1.65;margin-bottom:1.5rem;border-left:4px solid #3b82f6;padding-left:1rem;">
                <strong style="color:#fff;">Kết luận Phân tích Định lượng:</strong> Kết quả khảo thí cho thấy <strong>sự phân hóa rõ rệt theo từng giai đoạn đào tạo</strong>. Đối với <strong>KS24 (cuối Kỳ III)</strong>, vấn đề nổi cộm là <em>Hội chứng Coder thầm lặng (Silent Coders)</em> — sinh viên làm được sản phẩm nhưng lúng túng khi phỏng vấn vấn đáp. Trong khi đó, đối với <strong>KS25 (giữa Kỳ II)</strong>, vấn đề gốc rễ là <em>Bệnh học vẹt lý thuyết trắc nghiệm</em> — sinh viên hiểu khái niệm nhưng thiếu phản xạ gõ code độc lập.
            </div>

            <!-- KS24 4-Quadrant Diagnostic Grid -->
            <div style="margin-bottom:2rem;">
                <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1rem;">
                    <span style="font-size:1.2rem;">☕</span>
                    <h4 style="font-family:'Outfit',sans-serif;font-size:1.05rem;color:var(--color-ks24);font-weight:700;">Khóa KS24 (194 SV đã dự thi) – Ma trận Chẩn đoán Kỹ thuật vs Phỏng vấn Vấn đáp</h4>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
                    <!-- Q1: Silent Coders -->
                    <div style="background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.3);border-radius:10px;padding:1.25rem;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                            <span style="font-weight:700;color:#f87171;font-size:0.95rem;">🔇 1. 'Silent Coders' (Code giỏi, Vấn đáp yếu)</span>
                            <span style="background:rgba(239,68,68,0.2);color:#f87171;padding:0.2rem 0.6rem;border-radius:999px;font-size:0.78rem;font-weight:800;">29 SV (14.9%)</span>
                        </div>
                        <div style="font-size:0.82rem;color:var(--text-secondary);line-height:1.55;margin-bottom:0.75rem;">
                            <strong>Chẩn đoán:</strong> Điểm Sản phẩm &amp; Thực hành đạt <strong>70 - 100đ</strong>, nhưng Vấn đáp trực tiếp <strong>&lt; 45đ</strong> (thậm chí 0–30đ do áp lực tâm lý phòng thi).
                        </div>
                        <div style="background:rgba(0,0,0,0.25);border-radius:6px;padding:0.6rem 0.8rem;font-size:0.8rem;color:#fca5a5;">
                            👉 <strong>Giải pháp: KHÔNG DẠY LẠI CODE</strong>. Bắt buộc tham gia <strong>Mock Interview Lab 1-1</strong> (phỏng vấn giả định với Tech Lead doanh nghiệp theo phương pháp STAR).
                        </div>
                    </div>

                    <!-- Q2: Career Shifters -->
                    <div style="background:rgba(245,158,11,0.06);border:1px solid rgba(245,158,11,0.3);border-radius:10px;padding:1.25rem;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                            <span style="font-weight:700;color:#fbbf24;font-size:0.95rem;">🗣️ 2. 'Career Shifters' (Giao tiếp tốt, Code yếu)</span>
                            <span style="background:rgba(245,158,11,0.2);color:#fbbf24;padding:0.2rem 0.6rem;border-radius:999px;font-size:0.78rem;font-weight:800;">20 SV (10.8%)</span>
                        </div>
                        <div style="font-size:0.82rem;color:var(--text-secondary);line-height:1.55;margin-bottom:0.75rem;">
                            <strong>Chẩn đoán:</strong> Điểm Kỹ năng Mềm $\ge 75 - 100đ$, Vấn đáp $\ge 50đ$, nhưng Thực hành viết code $\le 45đ$. Dễ qua vòng HR nhưng trượt Live Coding của Dev.
                        </div>
                        <div style="background:rgba(0,0,0,0.25);border-radius:6px;padding:0.6rem 0.8rem;font-size:0.8rem;color:#fde68a;">
                            👉 <strong>Giải pháp: TƯ VẤN CHUYỂN LUỒNG NGHỀ NGHIỆP</strong> sang các vị trí cầu nối: <strong>IT Business Analyst (BA), Software QA/QC Tester, IT Project Coordinator</strong>.
                        </div>
                    </div>

                    <!-- Q3: All-Rounders -->
                    <div style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.3);border-radius:10px;padding:1.25rem;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                            <span style="font-weight:700;color:#34d399;font-size:0.95rem;">🌟 3. 'All-Rounders' (Toàn diện Đạt chuẩn Doanh nghiệp)</span>
                            <span style="background:rgba(16,185,129,0.2);color:#34d399;padding:0.2rem 0.6rem;border-radius:999px;font-size:0.78rem;font-weight:800;">97 SV (50.0%)</span>
                        </div>
                        <div style="font-size:0.82rem;color:var(--text-secondary);line-height:1.55;margin-bottom:0.75rem;">
                            <strong>Chẩn đoán:</strong> Nền tảng Kỹ thuật vững ($\ge 65đ$) và Kỹ năng Vấn đáp tốt ($\ge 50đ$). Học viên có khả năng độc lập giải quyết bài toán và bảo vệ giải pháp.
                        </div>
                        <div style="background:rgba(0,0,0,0.25);border-radius:6px;padding:0.6rem 0.8rem;font-size:0.8rem;color:#a7f3d0;">
                            👉 <strong>Giải pháp:</strong> Tập trung nâng cao <strong>Tiếng Anh chuyên ngành</strong> &amp; Kiến trúc nâng cao (System Design, Security) để ứng tuyển doanh nghiệp Top 1.
                        </div>
                    </div>

                    <!-- Q4: At-Risk -->
                    <div style="background:rgba(255,255,255,0.03);border:1px solid var(--border-color);border-radius:10px;padding:1.25rem;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                            <span style="font-weight:700;color:#a1a1aa;font-size:0.95rem;">⚠️ 4. 'At-Risk Cohort' &amp; Nhóm Trung gian</span>
                            <span style="background:rgba(255,255,255,0.1);color:#fff;padding:0.2rem 0.6rem;border-radius:999px;font-size:0.78rem;font-weight:800;">48 SV (24.7%)</span>
                        </div>
                        <div style="font-size:0.82rem;color:var(--text-secondary);line-height:1.55;margin-bottom:0.75rem;">
                            <strong>Chẩn đoán:</strong> 6 SV mất gốc toàn diện (&lt;50đ cả 2 mặt) + 31 SV đạt mức trung gian (50-64đ) + 14 SV vắng thi/thiếu bài.
                        </div>
                        <div style="background:rgba(0,0,0,0.25);border-radius:6px;padding:0.6rem 0.8rem;font-size:0.8rem;color:#e4e4e7;">
                            👉 <strong>Giải pháp:</strong> Bắt buộc tham gia <strong>Java Core &amp; Spring Boot Bootcamp 3 tuần</strong> trước khi cho nhận đồ án tốt nghiệp Kỳ IV.
                        </div>
                    </div>
                </div>
            </div>

            <!-- KS25 Diagnostic Breakdown -->
            <div style="margin-bottom:1.5rem;">
                <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1rem;">
                    <span style="font-size:1.2rem;">🐍</span>
                    <h4 style="font-family:'Outfit',sans-serif;font-size:1.05rem;color:var(--color-ks25);font-weight:700;">Khóa KS25 (293 SV đã dự thi) – Chẩn đoán Ảo tưởng Lý thuyết vs Yếu Thực hành Code</h4>
                </div>
                <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:1rem;">
                    <div style="background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.25);border-radius:10px;padding:1.1rem;">
                        <div style="font-weight:700;color:#f87171;font-size:0.88rem;margin-bottom:0.3rem;">🚨 1. Ảo tưởng Lý thuyết (151 SV - 51.5%)</div>
                        <div style="font-size:0.8rem;color:var(--text-secondary);line-height:1.5;">
                            Trắc nghiệm rất cao ($\ge 65 - 90đ$) nhưng <strong>Thực hành viết code liệt &lt; 50đ</strong>. Học viên học vẹt định nghĩa nhưng không tự dựng được API khi mở IDE.
                        </div>
                    </div>
                    <div style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.25);border-radius:10px;padding:1.1rem;">
                        <div style="font-weight:700;color:#34d399;font-size:0.88rem;margin-bottom:0.3rem;">💻 2. Vững Thực hành Code (47 SV - 16.0%)</div>
                        <div style="font-size:0.8rem;color:var(--text-secondary);line-height:1.5;">
                            Nắm chắc kiến trúc API 4 lớp FastAPI và kết nối CSDL ($\ge 50 - 90đ$). Tiếp tục học thẳng lộ trình chuyên sâu (DSA, Machine Learning, RAG/LLM).
                        </div>
                    </div>
                    <div style="background:rgba(245,158,11,0.06);border:1px solid rgba(245,158,11,0.25);border-radius:10px;padding:1.1rem;">
                        <div style="font-weight:700;color:#fbbf24;font-size:0.88rem;margin-bottom:0.3rem;">📋 3. Tiềm năng BA/QA &amp; Căn bản (95 SV)</div>
                        <div style="font-size:0.8rem;color:var(--text-secondary);line-height:1.5;">
                            12 SV có KNM tốt ($\ge 75đ$) nhưng code yếu $\rightarrow$ Phân luồng môn BA/QA từ Kỳ III. 40 SV mức cơ bản + 12 SV mất căn bản Python cần phụ đạo.
                        </div>
                    </div>
                </div>
            </div>

            <!-- Navigation Links -->
            <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,0.02);padding:1rem 1.25rem;border-radius:8px;border:1px solid var(--border-color);flex-wrap:wrap;gap:0.75rem;">
                <div style="font-size:0.83rem;color:var(--text-secondary);">
                    📊 Tra cứu danh sách định danh học viên theo từng Persona:
                </div>
                <div style="display:flex;gap:0.75rem;">
                    <a href="KS24_DGNL_Report.html" style="display:inline-block;padding:0.4rem 0.85rem;background:rgba(16,185,129,0.15);color:#34d399;border:1px solid rgba(16,185,129,0.3);border-radius:6px;font-size:0.78rem;font-weight:600;text-decoration:none;">☕ Chi tiết KS24 →</a>
                    <a href="KS25_DGNL_Report.html" style="display:inline-block;padding:0.4rem 0.85rem;background:rgba(59,130,246,0.15);color:#60a5fa;border:1px solid rgba(59,130,246,0.3);border-radius:6px;font-size:0.78rem;font-weight:600;text-decoration:none;">🐍 Chi tiết KS25 →</a>
                    <a href="QTKD_DGNL_Report.html" style="display:inline-block;padding:0.4rem 0.85rem;background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);border-radius:6px;font-size:0.78rem;font-weight:600;text-decoration:none;">💼 Chi tiết QTKD →</a>
                </div>
            </div>
        </div>
"""

new_content = before + upgraded_section + '\n        ' + after

with open('outputs/Executive_Summary_DGNL_Report.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Executive Summary updated with comprehensive diagnostic section!')

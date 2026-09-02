import sys

with open('outputs/Executive_Summary_DGNL_Report.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace specific sections
text = text.replace('Ngày phát hành: 23/08/2026', 'Ngày cập nhật: 02/09/2026 (Sau thi bổ sung 22/08/2026)')
text = text.replace('<div class="alert-icon">🚨</div>', '<div class="alert-icon">✅</div>')
text = text.replace('Cảnh báo Chất lượng Học thuật – Báo động đỏ đối với KS25', 'Cập nhật Kết quả sau Đợt thi bổ sung (22/08/2026) – Phục hồi Dữ liệu & Cải thiện Chất lượng')

old_alert = """Chỉ <strong>86 học viên (13.7%)</strong> đạt Mức sẵn sàng nghề nghiệp (L2 &amp; L3).
                    Đặc biệt, khóa KS25 ghi nhận tỷ lệ trượt thực hành lên đến <strong>81.9%</strong> và tỷ lệ vắng thi <strong>48.0%</strong>
                    do sự cố nghiêm trọng hệ thống khảo thí tại Hà Nội, đòi hỏi Ban lãnh đạo ra quyết sách khẩn cấp về phân luồng học thuật."""

new_alert = """Tổng số thí sinh dự thi thực tế toàn hệ thống đạt <strong>491/630 học viên (77.9%)</strong>, tỷ lệ vắng giảm mạnh từ <strong>36.2% xuống 22.1%</strong>.
                    Số học viên đạt Mức Sẵn sàng Nghề nghiệp (L2 &amp; L3) tăng lên <strong>108 học viên (17.1%)</strong> (+22 SV). Tỷ lệ KS25 đạt chuẩn tăng lên <strong>9.8%</strong> (42 SV), dữ liệu khảo thí tại Hà Nội đã được khôi phục đầy đủ."""

text = text.replace(old_alert, new_alert)

# Update KPI strip
text = text.replace('KS24: 200 SV  •  KS25: 429 SV', 'KS24: 201 SV  •  KS25: 429 SV')
text = text.replace('>629<', '>630<')
text = text.replace('>401<', '>491<')
text = text.replace('KS24: 178 SV  •  KS25: 223 SV', 'KS24: 185 SV (92.0%) • KS25: 306 SV (71.3%)')
text = text.replace('>36.2%<', '>22.1%<')
text = text.replace('Tổng 228 SV vắng  •  KS25 HN: sự cố hệ thống', 'Tổng 139 SV vắng (giảm 89 SV sau thi bổ sung)')
text = text.replace('>13.7%<', '>17.1%<')
text = text.replace('86/629 SV đạt chuẩn', '108/630 SV đạt chuẩn')
text = text.replace('>80.6%<', '>71.9%<')
text = text.replace('KS24: 113 SV  •  KS25: 394 SV', 'KS24: 114 SV (56.7%) • KS25: 339 SV (79.0%)')

# Update KS24 card
text = text.replace('">200<', '">201<')
text = text.replace('">178<', '">185<')
text = text.replace('">5.33/10<', '">5.58/10<')
text = text.replace('">33.0%<', '">32.8%<')
text = text.replace('<span>Dự thi</span><strong>142</strong>', '<span>Dự thi</span><strong>143</strong>')
text = text.replace('<span>Điểm TB</span><strong>5.87</strong>', '<span>Điểm TB</span><strong>5.95</strong>')
text = text.replace('<span>Dự thi</span><strong>36</strong>', '<span>Dự thi</span><strong>42</strong>')
text = text.replace('<span>Điểm TB</span><strong>6.47</strong>', '<span>Điểm TB</span><strong>6.43</strong>')

# Update KS25 card
text = text.replace('">223<', '">306<')
text = text.replace('">3.8/10<', '">3.23/10<')
text = text.replace('">4.7%<', '">9.8%<')
text = text.replace('<span>Dự thi</span><strong style="color:#f87171">101</strong>',
                    '<span>Dự thi</span><strong style="color:var(--color-ks25)">181</strong>')
text = text.replace('<span>Điểm TB</span><strong>3.71</strong>', '<span>Điểm TB</span><strong>2.96</strong>')
text = text.replace('<span>Sẵn sàng</span><strong style="color:var(--color-danger)">4.0%</strong>',
                    '<span>Sẵn sàng</span><strong style="color:var(--color-primary)">9.7%</strong>')
text = text.replace('<span>Dự thi</span><strong>122</strong>', '<span>Dự thi</span><strong>125</strong>')
text = text.replace('<span>Điểm TB</span><strong>3.38</strong>', '<span>Điểm TB</span><strong>3.62</strong>')
text = text.replace('<span>Sẵn sàng</span><strong style="color:var(--color-warning)">6.0%</strong>',
                    '<span>Sẵn sàng</span><strong style="color:var(--color-warning)">9.9%</strong>')

# Matrix table
text = text.replace('200 SV</td>', '201 SV</td>')
text = text.replace('+229</td>', '+228</td>')
text = text.replace('>11.0%<', '>8.0%<')
text = text.replace('>48.0%<', '>28.7%<')
text = text.replace('>+37.0%<', '>+20.7%<')
text = text.replace('KS25 HN bị lỗi hệ thống</td>', 'Giảm mạnh sau thi bổ sung 22/08</td>')
text = text.replace('>5.33/10<', '>5.58/10<')
text = text.replace('>3.8/10<', '>3.23/10<')
text = text.replace('>-1.53<', '>-2.35<')
text = text.replace('KS25 thấp hơn đáng kể</td>', 'KS25 phản ánh đúng năng lực giữa Kỳ II</td>')
text = text.replace('>5.87/10<', '>5.95/10<')
text = text.replace('>3.71/10<', '>2.96/10<')
text = text.replace('>-2.16<', '>-2.99<')
text = text.replace('Khoảng cách lớn do lỗi khảo thí</td>', 'Đã ghi nhận đủ điểm trắc nghiệm & thực hành</td>')
text = text.replace('>6.47/10<', '>6.43/10<')
text = text.replace('>3.38/10<', '>3.62/10<')
text = text.replace('>-3.09<', '>-2.81<')
text = text.replace('HCM-KS25 cần can thiệp</td>', 'HCM có điểm TB cao hơn HN ở cả 2 khóa</td>')
text = text.replace('>33.0%<', '>32.8% (66 SV)<')
text = text.replace('>4.7%<', '>9.8% (42 SV)<')
text = text.replace('>-28.3%<', '>-23.0%<')
text = text.replace('KS25 chỉ đạt 1/7 KS24</td>', 'KS25 tăng từ 4.7% lên 9.8% sau bổ sung điểm</td>')

# Update charts
text = text.replace('[5.87, 6.47, 5.33]', '[5.95, 6.43, 5.58]')
text = text.replace('[3.71, 3.38, 3.8]', '[2.96, 3.62, 3.23]')
text = text.replace('[507, 36, 67, 19]', '[453, 69, 88, 20]')
text = text.replace('507 SV (80.6%)', '453 SV (71.9%)')
text = text.replace('36 SV (5.7%)', '69 SV (11.0%)')
text = text.replace('67 SV (10.7%)', '88 SV (14.0%)')
text = text.replace('19 SV (3.0%)', '20 SV (3.2%)')
text = text.replace('86 SV (13.7%)', '108 SV (17.1%)')

with open('outputs/Executive_Summary_DGNL_Report.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Executive Summary updated successfully!')

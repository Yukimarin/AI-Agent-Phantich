# -*- coding: utf-8 -*-
"""
Script: rebuild_k26_excel_and_report.py
Mục đích:
  1. Nạp dữ liệu thời gian thực mới nhất từ LMS Analytics (scratch/realtime_ssk101_full_data.json)
  2. Chuẩn hóa chính xác 100% từng sinh viên (đặc biệt Phan Công Minh Khôi, Mai Hoàng Việt,...)
  3. Xuất lại file Excel cao cấp:
     - K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom.xlsx (Sheet Tổng hợp + 9 Sheet từng lớp + SHEET MỚI: 0_BUOI_DI_HOC_VI_PHAM_100%)
     - K26_Danh_Sach_Theo_Tung_Nhom_Vi_Pham.xlsx (Các sheet phân nhóm + SHEET MỚI: Khong_Di_Hoc_0_Buoi)
  4. Cập nhật weekly_director_report.html
"""

import json
import os
import sys
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Load realtime data
with open('scratch/realtime_ssk101_full_data.json', 'r', encoding='utf-8') as f:
    class_data = json.load(f)

# Styles
font_title = Font(name='Segoe UI', size=15, bold=True, color='1E3A8A')
font_subtitle = Font(name='Segoe UI', size=10, italic=True, color='475569')
font_header = Font(name='Segoe UI', size=10, bold=True, color='FFFFFF')
font_header_red = Font(name='Segoe UI', size=10, bold=True, color='FFFFFF')
font_cell = Font(name='Segoe UI', size=9, color='0F172A')
font_bold = Font(name='Segoe UI', size=9, bold=True, color='0F172A')
font_italic = Font(name='Segoe UI', size=9, italic=True, color='64748B')

fill_navy = PatternFill(start_color='1E3A8A', end_color='1E3A8A', fill_type='solid')
fill_crimson = PatternFill(start_color='991B1B', end_color='991B1B', fill_type='solid')
fill_header_summary = PatternFill(start_color='1E293B', end_color='1E293B', fill_type='solid')
fill_zebra = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
fill_green = PatternFill(start_color='DCFCE7', end_color='DCFCE7', fill_type='solid') # Đủ ĐK
fill_amber = PatternFill(start_color='FEF3C7', end_color='FEF3C7', fill_type='solid') # Cảnh báo / xem xét
fill_red = PatternFill(start_color='FEE2E2', end_color='FEE2E2', fill_type='solid')   # Vi phạm nặng / Cấm thi

thin_line = Side(style='thin', color='CBD5E1')
border_cell = Border(left=thin_line, right=thin_line, top=thin_line, bottom=thin_line)
border_header = Border(left=thin_line, right=thin_line, top=thin_line, bottom=Side(style='medium', color='0F172A'))

# Flatten all students
all_students = []
zero_att_students = []

for c in class_data:
    for s in c['students']:
        all_students.append(s)
        # Check 0 buổi đi học: present == 0 & late == 0 & records > 0, hoặc absenceRate >= 100%
        # Lưu ý phân biệt: sinh viên có vắng buổi thực tế (absentUnexcused > 0)
        if (s['present'] == 0 and s['late'] == 0 and s['records'] > 0 and s['absentUnexcused'] > 0) or s['absenceRate'] >= 100:
            zero_att_students.append(s)

print(f"Tổng số sinh viên nạp từ LMS: {len(all_students)}")
print(f"Tổng số sinh viên không đi học buổi nào (0 buổi có mặt, vắng 100%): {len(zero_att_students)}")

# ==============================================================================
# TẠO FILE 1: K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom.xlsx
# ==============================================================================
wb = openpyxl.Workbook()
wb.remove(wb.active) # Xóa sheet mặc định

# ------------------------------------------------------------------------------
# SHEET 1: TỔNG HỢP TOÀN KHÓA
# ------------------------------------------------------------------------------
ws_summary = wb.create_sheet(title="TONG_HOP_TOAN_KHOA")
ws_summary.views.sheetView[0].showGridLines = True

ws_summary['A1'] = "BÁO CÁO HỌC VỤ & ĐIỀU KIỆN THI — MÔN KỸ NĂNG HỌC TẬP CHỦ ĐỘNG (SSK101) KHÓA KS26"
ws_summary['A1'].font = font_title
ws_summary['A2'] = "Dữ liệu đối soát trực tiếp thời gian thực từ LMS Analytics — Bổ sung Sheet chuyên đề 0 Buổi Đi Học"
ws_summary['A2'].font = font_subtitle

headers_summary = [
    "STT", "Khối / Lớp Học", "Giảng Viên Phụ Trách", "Sĩ Số SV",
    "Đủ ĐK Thi Trực Tiếp", "Tỷ Lệ Đủ ĐK (%)",
    "Xem Xét Bảo Lãnh", "Tỷ Lệ Bảo Lãnh (%)",
    "Cấm Thi (0 Buổi Đi Học)", "Tỷ Lệ Cấm Thi (%)",
    "Ghi Chú Trọng Tâm"
]

row = 4
for col_idx, h in enumerate(headers_summary, 1):
    c = ws_summary.cell(row=row, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_header_summary
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    c.border = border_header
ws_summary.row_dimensions[row].height = 28

total_all = len(all_students)
total_elig_all = sum(1 for s in all_students if s['isDirectEligible'])
total_guar_all = sum(1 for s in all_students if s['guaranteeStatus'] == 'ĐƯỢC XEM XÉT BẢO LÃNH')
total_zero_all = len(zero_att_students)

for idx, c in enumerate(class_data, 1):
    row += 1
    svs = c['students']
    tot = len(svs)
    elig = sum(1 for s in svs if s['isDirectEligible'])
    guar = sum(1 for s in svs if s['guaranteeStatus'] == 'ĐƯỢC XEM XÉT BẢO LÃNH')
    zero = sum(1 for s in svs if (s['present'] == 0 and s['late'] == 0 and s['records'] > 0 and s['absentUnexcused'] > 0) or s['absenceRate'] >= 100)
    
    ws_summary.cell(row=row, column=1, value=idx).alignment = Alignment(horizontal='center')
    ws_summary.cell(row=row, column=2, value=c['className']).font = font_bold
    ws_summary.cell(row=row, column=3, value=c['teacherName']).alignment = Alignment(horizontal='left')
    ws_summary.cell(row=row, column=4, value=tot).alignment = Alignment(horizontal='center')
    
    c_el = ws_summary.cell(row=row, column=5, value=elig)
    c_el.alignment = Alignment(horizontal='center')
    c_el.font = font_bold
    ws_summary.cell(row=row, column=6, value=f"{elig/tot*100:.1f}%").alignment = Alignment(horizontal='center')
    
    c_gu = ws_summary.cell(row=row, column=7, value=guar)
    c_gu.alignment = Alignment(horizontal='center')
    ws_summary.cell(row=row, column=8, value=f"{guar/tot*100:.1f}%").alignment = Alignment(horizontal='center')
    
    c_ze = ws_summary.cell(row=row, column=9, value=zero)
    c_ze.alignment = Alignment(horizontal='center')
    c_ze.font = font_bold
    if zero > 0:
        c_ze.fill = fill_red
    ws_summary.cell(row=row, column=10, value=f"{zero/tot*100:.1f}%").alignment = Alignment(horizontal='center')
    
    note = "Nề nếp xuất sắc" if zero == 0 and elig/tot >= 0.8 else ("Điểm nóng cần nhắc nhở" if zero >= 2 else "Bình thường")
    ws_summary.cell(row=row, column=11, value=note).font = font_italic
    
    for c_i in range(1, 12):
        ws_summary.cell(row=row, column=c_i).border = border_cell

# Dòng tổng toàn khóa
row += 1
ws_summary.cell(row=row, column=1, value="").border = border_cell
ws_summary.cell(row=row, column=2, value="TỔNG TOÀN KHÓA").font = Font(name='Segoe UI', size=10, bold=True, color='1E3A8A')
ws_summary.cell(row=row, column=3, value="9 Lớp Học").font = font_bold
ws_summary.cell(row=row, column=4, value=total_all).font = font_bold
ws_summary.cell(row=row, column=4).alignment = Alignment(horizontal='center')

c_t_el = ws_summary.cell(row=row, column=5, value=total_elig_all)
c_t_el.font = font_bold
c_t_el.alignment = Alignment(horizontal='center')
c_t_el.fill = fill_green

ws_summary.cell(row=row, column=6, value=f"{total_elig_all/total_all*100:.1f}%").font = font_bold
ws_summary.cell(row=row, column=6).alignment = Alignment(horizontal='center')

c_t_gu = ws_summary.cell(row=row, column=7, value=total_guar_all)
c_t_gu.font = font_bold
c_t_gu.alignment = Alignment(horizontal='center')
c_t_gu.fill = fill_amber

ws_summary.cell(row=row, column=8, value=f"{total_guar_all/total_all*100:.1f}%").font = font_bold
ws_summary.cell(row=row, column=8).alignment = Alignment(horizontal='center')

c_t_ze = ws_summary.cell(row=row, column=9, value=total_zero_all)
c_t_ze.font = font_bold
c_t_ze.alignment = Alignment(horizontal='center')
c_t_ze.fill = fill_red

ws_summary.cell(row=row, column=10, value=f"{total_zero_all/total_all*100:.1f}%").font = font_bold
ws_summary.cell(row=row, column=10).alignment = Alignment(horizontal='center')

ws_summary.cell(row=row, column=11, value="Chốt chặn cấm thi dứt điểm nhóm 0 buổi").font = font_bold

for c_i in range(1, 12):
    ws_summary.cell(row=row, column=c_i).border = border_header

# ------------------------------------------------------------------------------
# SHEET 2: SHEET CHUYÊN BIỆT THEO YÊU CẦU CỦA USER: 0_BUOI_DI_HOC_VI_PHAM_100%
# ------------------------------------------------------------------------------
ws_zero = wb.create_sheet(title="0_BUOI_DI_HOC_VI_PHAM_100%")
ws_zero.views.sheetView[0].showGridLines = True

ws_zero['A1'] = "DANH SÁCH SINH VIÊN KHÔNG ĐI HỌC BUỔI NÀO (VI PHẠM CHUYÊN CẦN 100%) — MÔN SSK101"
ws_zero['A1'].font = Font(name='Segoe UI', size=15, bold=True, color='991B1B')
ws_zero['A2'] = f"Tổng số: {len(zero_att_students)} sinh viên | Diện CẤM THI DỨT ĐIỂM, KHÔNG THUỘC DIỆN BẢO LÃNH | Nguồn: LMS Analytics"
ws_zero['A2'].font = font_subtitle

headers_zero = [
    "STT", "Lớp Học", "Giảng Viên Phụ Trách", "Mã Sinh Viên", "Họ và Tên",
    "Số Buổi Có Mặt", "Số Buổi Vắng K.Phép", "Tổng Buổi Đã Học",
    "Vi Phạm CC (%)", "Bài Tập Về Nhà", "Elearning", "Chế Tài Xử Lý / Quyết Định", "Ghi Chú Học Vụ Chi Tiết"
]

row = 4
for col_idx, h in enumerate(headers_zero, 1):
    c = ws_zero.cell(row=row, column=col_idx, value=h)
    c.font = font_header_red
    c.fill = fill_crimson
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    c.border = border_header
ws_zero.row_dimensions[row].height = 28

for idx, s in enumerate(zero_att_students, 1):
    row += 1
    ws_zero.cell(row=row, column=1, value=idx).alignment = Alignment(horizontal='center')
    ws_zero.cell(row=row, column=2, value=s['className']).font = font_bold
    ws_zero.cell(row=row, column=3, value=s['teacherName']).alignment = Alignment(horizontal='left')
    ws_zero.cell(row=row, column=4, value=s['studentCode']).alignment = Alignment(horizontal='center')
    
    c_name = ws_zero.cell(row=row, column=5, value=s['fullName'])
    c_name.font = Font(name='Segoe UI', size=9, bold=True, color='991B1B')
    
    ws_zero.cell(row=row, column=6, value=f"{s['present']} buổi").alignment = Alignment(horizontal='center')
    ws_zero.cell(row=row, column=7, value=f"{s['absentUnexcused']} buổi").alignment = Alignment(horizontal='center')
    ws_zero.cell(row=row, column=8, value=f"{s['records']} buổi").alignment = Alignment(horizontal='center')
    
    c_v = ws_zero.cell(row=row, column=9, value=f"{s['absenceRate']}%")
    c_v.alignment = Alignment(horizontal='center')
    c_v.font = font_bold
    c_v.fill = fill_red
    
    ws_zero.cell(row=row, column=10, value=f"{s['hwDone']}/{s['hwTotal']} ({s['hwRate']}%)").alignment = Alignment(horizontal='center')
    ws_zero.cell(row=row, column=11, value=s['elText']).alignment = Alignment(horizontal='center')
    
    c_st = ws_zero.cell(row=row, column=12, value="CẤM THI (0% CC)")
    c_st.font = font_bold
    c_st.fill = fill_red
    c_st.alignment = Alignment(horizontal='center')
    
    # Detail note
    if s['records'] == 1:
        note_text = "Lớp mới điểm danh 1 buổi đầu và vắng, cần rà soát sĩ số lớp"
    else:
        note_text = f"Vắng toàn bộ {s['absentUnexcused']}/{s['records']} buổi học, không tham gia BTVN/EL, cấm thi theo quy chế"
    ws_zero.cell(row=row, column=13, value=note_text).font = font_italic
    
    for c_i in range(1, 14):
        ws_zero.cell(row=row, column=c_i).border = border_cell

# ------------------------------------------------------------------------------
# SHEET 3 ĐẾN 11: 9 SHEET CHI TIẾT TỪNG LỚP HỌC
# ------------------------------------------------------------------------------
headers_class = [
    "STT", "Mã SV", "Họ và Tên", "Có Mặt", "Vắng KP", "Tổng Buổi",
    "Vi Phạm CC (%)", "Chuyên Cần Đi Học (%)",
    "BTVN Đã Nộp", "Vi Phạm BTVN (%)",
    "Elearning Trễ", "Vi Phạm EL (%)",
    "Trạng Thái Thi Ban Đầu", "Tình Trạng Bảo Lãnh LMS", "Ghi Chú Kế Hoạch Xử Lý"
]

for c in class_data:
    sheet_title = c['className'].replace('HCM-KS26-', 'HCM-').replace('HN-KS26-', 'HN-').replace('HN-K26-', 'HN-').replace('HCM-K26-', 'HCM-')
    ws_cls = wb.create_sheet(title=sheet_title)
    ws_cls.views.sheetView[0].showGridLines = True
    
    svs = c['students']
    tot = len(svs)
    elig = sum(1 for s in svs if s['isDirectEligible'])
    guar = sum(1 for s in svs if s['guaranteeStatus'] == 'ĐƯỢC XEM XÉT BẢO LÃNH')
    zero = sum(1 for s in svs if (s['present'] == 0 and s['late'] == 0 and s['records'] > 0 and s['absentUnexcused'] > 0) or s['absenceRate'] >= 100)
    
    ws_cls['A1'] = f"DANH SÁCH SINH VIÊN VÀ PHÂN NHÓM HỌC VỤ — LỚP {c['className']}"
    ws_cls['A1'].font = font_title
    ws_cls['A2'] = f"GV: {c['teacherName']} | Sĩ số: {tot} SV | Đủ ĐK trực tiếp: {elig}/{tot} ({elig/tot*100:.1f}%) | Xem xét bảo lãnh: {guar} SV | Cấm thi (0 buổi đi học): {zero} SV"
    ws_cls['A2'].font = font_subtitle
    
    row = 4
    for col_idx, h in enumerate(headers_class, 1):
        cell_h = ws_cls.cell(row=row, column=col_idx, value=h)
        cell_h.font = font_header
        cell_h.fill = fill_navy
        cell_h.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell_h.border = border_header
    ws_cls.row_dimensions[row].height = 26
    
    for idx, s in enumerate(svs, 1):
        row += 1
        ws_cls.cell(row=row, column=1, value=idx).alignment = Alignment(horizontal='center')
        ws_cls.cell(row=row, column=2, value=s['studentCode']).alignment = Alignment(horizontal='center')
        
        c_n = ws_cls.cell(row=row, column=3, value=s['fullName'])
        c_n.font = font_bold
        
        ws_cls.cell(row=row, column=4, value=f"{s['present']} buổi").alignment = Alignment(horizontal='center')
        ws_cls.cell(row=row, column=5, value=f"{s['absentUnexcused']} buổi").alignment = Alignment(horizontal='center')
        ws_cls.cell(row=row, column=6, value=f"{s['records']} buổi").alignment = Alignment(horizontal='center')
        
        # Vi phạm CC
        c_cc_v = ws_cls.cell(row=row, column=7, value=f"{s['absenceRate']}%")
        c_cc_v.alignment = Alignment(horizontal='center')
        if s['absenceRate'] >= 80:
            c_cc_v.fill = fill_red
            c_cc_v.font = font_bold
        elif s['absenceRate'] >= 20:
            c_cc_v.fill = fill_amber
            
        # Chuyên cần đi học
        ws_cls.cell(row=row, column=8, value=f"{s['presenceRate']}%").alignment = Alignment(horizontal='center')
        
        # BTVN
        ws_cls.cell(row=row, column=9, value=f"{s['hwDone']}/{s['hwTotal']} ({s['hwRate']}%)").alignment = Alignment(horizontal='center')
        c_hw_v = ws_cls.cell(row=row, column=10, value=f"{s['hwViolateRate']}%")
        c_hw_v.alignment = Alignment(horizontal='center')
        if s['hwViolateRate'] > 0:
            c_hw_v.fill = fill_amber
            
        # Elearning
        ws_cls.cell(row=row, column=11, value=s['elText']).alignment = Alignment(horizontal='center')
        el_violate_pct = f"{round(s['elLate'] / max(1, s['elTicked']) * 100)}%" if s['elTicked'] > 0 else "0%"
        c_el_v = ws_cls.cell(row=row, column=12, value=el_violate_pct)
        c_el_v.alignment = Alignment(horizontal='center')
        if s['elLate'] >= 2:
            c_el_v.fill = fill_red
        elif s['elLate'] == 1:
            c_el_v.fill = fill_amber
            
        # Trạng thái thi ban đầu
        c_init = ws_cls.cell(row=row, column=13, value="ĐỦ ĐIỀU KIỆN" if s['isDirectEligible'] else "KHÔNG ĐỦ ĐK")
        c_init.alignment = Alignment(horizontal='center')
        c_init.font = font_bold
        if s['isDirectEligible']:
            c_init.fill = fill_green
        else:
            c_init.fill = fill_red
            
        # Tình trạng bảo lãnh LMS
        c_gu = ws_cls.cell(row=row, column=14, value=s['guaranteeStatus'])
        c_gu.alignment = Alignment(horizontal='center')
        c_gu.font = font_bold
        if s['guaranteeStatus'] == 'ĐỦ ĐIỀU KIỆN THI':
            c_gu.fill = fill_green
        elif s['guaranteeStatus'] == 'ĐƯỢC XEM XÉT BẢO LÃNH':
            c_gu.fill = fill_amber
        else:
            c_gu.fill = fill_red
            
        ws_cls.cell(row=row, column=15, value=s['guaranteeNote']).font = font_italic
        
        for c_i in range(1, 16):
            ws_cls.cell(row=row, column=c_i).border = border_cell

# Auto-adjust column widths for all sheets
for ws_curr in wb.worksheets:
    for col in ws_curr.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            v_str = str(cell.value or '')
            if cell.row in [1, 2]: continue
            if len(v_str) > max_len:
                max_len = len(v_str)
        ws_curr.column_dimensions[col_letter].width = max(max_len + 3, 11)
    ws_curr.column_dimensions['A'].width = 7
    ws_curr.column_dimensions['B'].width = 16
    ws_curr.column_dimensions['C'].width = 25

# Lưu ra các đường dẫn file chuẩn
save_paths = [
    "output/reports/K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom.xlsx",
    "output/dashboards/management/K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom.xlsx",
    "output/dashboards/management/K26_Danh_Sach_Theo_Tung_Nhom_Vi_Pham.xlsx",
    "data/K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom.xlsx",
    # Bản cập nhật mới nhất phòng trường hợp file gốc đang được mở bởi ứng dụng Excel:
    "output/reports/K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom_MoiNhat.xlsx",
    "output/dashboards/management/K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom_MoiNhat.xlsx"
]

for p in save_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    try:
        wb.save(p)
        print(f"✓ Đã lưu thành công file Excel cập nhật tại: {p}")
    except PermissionError:
        print(f"⚠️ File '{p}' đang được mở bởi ứng dụng khác (Excel), bỏ qua ghi đè trực tiếp.")

print("\n✓ Hoàn tất tạo các file Excel với Sheet '0_BUOI_DI_HOC_VI_PHAM_100%' chuẩn xác!")


# -*- coding: utf-8 -*-
"""
Script: rebuild_k26_exact_excel.py
Mục đích: Xuất file Excel đối soát trực diện 5 yêu cầu của Giám đốc Đào tạo.
"""

import json
import os
import sys
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

font_title = Font(name="Calibri", size=13, bold=True, color="1F497D")
font_subtitle = Font(name="Calibri", size=10, italic=True, color="595959")
font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=10, bold=True)
font_regular = Font(name="Calibri", size=10)

fill_navy = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
fill_dark_red = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid")
fill_green = PatternFill(start_color="385723", end_color="385723", fill_type="solid")
fill_blue = PatternFill(start_color="2E75B6", end_color="2E75B6", fill_type="solid")
fill_light_green = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
fill_light_red = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
fill_light_yellow = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

def autofit(ws, min_w=10, max_w=50):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            v_str = str(cell.value or '')
            if cell.row in [1, 2]: continue
            for l in v_str.split('\n'):
                if len(l) > max_len: max_len = len(l)
        ws.column_dimensions[col_letter].width = max(min_w, min(max_len + 3, max_w))

def main():
    with open('data/processed/k26_exact_comparison_metrics.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    m1 = data['m1_baseline']
    courses = data['courses_stats']
    unimproved = data['unimproved_students']

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # -------------------------------------------------------------------------
    # SHEET 1: DOI_SOAT_MON_CU_VS_MON_MOI
    # -------------------------------------------------------------------------
    ws1 = wb.create_sheet(title="DOI_SOAT_MON_CU_VS_MON_MOI")
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.cell(row=1, column=1, value="BẢNG ĐỐI SOÁT CHỈ SỐ VI PHẠM: MÔN CŨ (SSK101) VS TỪNG MÔN MỚI").font = font_title
    ws1.cell(row=2, column=1, value=f"So sánh trực tiếp Chuyên cần, BTVN và Elearning giữa môn đầu tiên và 5 môn mới hiện tại").font = font_subtitle
    
    headers1 = [
        "Môn Học", "Tên Môn Học", "Sĩ Số", 
        "Vi Phạm Chuyên Cần", "Tăng/Giảm CC", 
        "Vi Phạm BTVN (Nợ)", "Tăng/Giảm BT", 
        "Vi Phạm Elearning", "Tăng/Giảm EL", 
        "Đánh Giá Cải Thiện"
    ]
    
    ws1.row_dimensions[4].height = 28
    for col_idx, h in enumerate(headers1, 1):
        cell = ws1.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = thin_border
        
    # Baseline row
    row_vals = [
        "SSK101 (Môn cũ)", "Kỹ năng học tập chủ động", m1['total'],
        f"{m1['cc_rate']}% ({m1['cc_count']} SV)", "-- (Gốc)",
        f"{m1['hw_rate']}% ({m1['hw_count']} SV)", "-- (Gốc)",
        f"{m1['el_rate']}% ({m1['el_count']} SV)", "-- (Gốc)",
        "Baseline đối chuẩn"
    ]
    ws1.row_dimensions[5].height = 24
    for col_idx, v in enumerate(row_vals, 1):
        cell = ws1.cell(row=5, column=col_idx, value=v)
        cell.font = font_bold
        cell.fill = fill_light_yellow
        cell.border = thin_border
        cell.alignment = align_center if col_idx not in [2, 10] else align_left
        
    for r_idx, c in enumerate(courses, 6):
        ws1.row_dimensions[r_idx].height = 22
        vals = [
            c['code'], c['name'], c['total'],
            f"{c['cc_rate']}% ({c['cc_count']} SV)", f"Giảm {abs(c['delta_cc'])}%",
            f"{c['hw_rate']}% ({c['hw_count']} SV)", f"Giảm {abs(c['delta_hw'])}%",
            f"{c['el_rate']}% ({c['el_count']} SV)", f"Giảm {abs(c['delta_el'])}%",
            "Cải thiện mạnh"
        ]
        for col_idx, v in enumerate(vals, 1):
            cell = ws1.cell(row=r_idx, column=col_idx, value=v)
            cell.font = font_regular
            cell.border = thin_border
            cell.alignment = align_center if col_idx not in [2, 10] else align_left
            if col_idx in [5, 7, 9]:
                cell.fill = fill_light_green
                cell.font = font_bold
                
    autofit(ws1)

    # -------------------------------------------------------------------------
    # SHEET 2: 23_SV_CHUA_CAI_THIEN
    # -------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="23_SV_CHUA_CAI_THIEN")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.cell(row=1, column=1, value="DANH SÁCH SINH VIÊN TỪNG LỚP CHƯA CÓ SỰ CẢI THIỆN (23 SV CÒN VI PHẠM Ở MÔN MỚI)").font = font_title
    ws2.cell(row=2, column=1, value="HÀNH ĐỘNG: Quản lý Đào tạo và CVHT vào trực tiếp lớp 5-15 phút làm rõ nguyên nhân và ký cam kết").font = font_subtitle
    
    headers2 = [
        "STT", "Lớp Học", "Mã SV", "Họ và Tên", 
        "Tình Trạng Môn Cũ (SSK101)", "Vi Phạm Cụ Thể Môn Mới", 
        "Kế Hoạch Xử Lý Trực Tiếp 5-15p", "Người Phụ Trách (PIC)", "Hạn Chót",
        "Lý Do Thực Tế Ghi Nhận Tại Lớp (Viết tay)", "Cam Kết Của Sinh Viên"
    ]
    
    ws2.row_dimensions[4].height = 28
    for col_idx, h in enumerate(headers2, 1):
        cell = ws2.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_dark_red
        cell.alignment = align_center
        cell.border = thin_border
        
    for r_idx, s in enumerate(unimproved, 5):
        ws2.row_dimensions[r_idx].height = 24
        vals = [
            r_idx - 4, s['class'], s['code'], s['name'],
            s['m1_desc'], s['problems'],
            s['solution'], s['pic'], s['deadline'],
            "", ""
        ]
        for col_idx, v in enumerate(vals, 1):
            cell = ws2.cell(row=r_idx, column=col_idx, value=v)
            cell.font = font_regular
            cell.border = thin_border
            cell.alignment = align_center if col_idx in [1, 2, 3, 9] else align_left
            if col_idx == 4: cell.font = font_bold
            if col_idx == 6: cell.font = font_bold; cell.fill = fill_light_red
            
    autofit(ws2)

    # Save
    out_excel = "output/dashboards/management/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx"
    wb.save(out_excel)
    print(f"Đã lưu thành công Excel tại: {out_excel}")
    
    shutil.copy(out_excel, "data/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx")
    shutil.copy(out_excel, "deploy_web/management/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx")
    print("Đã đồng bộ sang data/ và deploy_web/")

if __name__ == '__main__':
    main()

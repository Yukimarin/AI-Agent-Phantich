# -*- coding: utf-8 -*-
"""
Script: export_k26_behavioral_excel.py
Mục đích:
  1. Đọc kết quả phân loại từ data/processed/k26_behavioral_analysis.json.
  2. Tạo file Excel cao cấp 14 Sheet chuẩn tác chiến thực địa.
  3. Định dạng màu sắc chuyên nghiệp, viền nét mảnh, AutoFilter, độ rộng cột tự động.
  4. Xuất file ra output/dashboards/management/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx
     và đồng bộ sang data/ và deploy_web/management/.
"""

import json
import os
import sys
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

# Styles
font_title = Font(name="Calibri", size=13, bold=True, color="1F497D")
font_subtitle = Font(name="Calibri", size=10, italic=True, color="595959")
font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=10, bold=True)
font_regular = Font(name="Calibri", size=10)

# Fills
fill_navy = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
fill_blue_header = PatternFill(start_color="2E75B6", end_color="2E75B6", fill_type="solid")
fill_dark_red = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid")
fill_orange = PatternFill(start_color="ED7D31", end_color="ED7D31", fill_type="solid")
fill_green_header = PatternFill(start_color="385723", end_color="385723", fill_type="solid")

fill_th1 = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid") # Red tint
fill_th4 = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # Orange/Yellow tint
fill_th2 = PatternFill(start_color="EDEDED", end_color="EDEDED", fill_type="solid") # Gray tint
fill_th3 = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid") # Green tint
fill_zebra = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
align_right = Alignment(horizontal="right", vertical="center", wrap_text=True)

def autofit(ws, min_width=10, max_width=45):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            val_str = str(cell.value or '')
            if cell.row in [1, 2]: # Ignore titles
                continue
            lines = val_str.split('\n')
            for l in lines:
                if len(l) > max_len:
                    max_len = len(l)
        calc_w = max(min_width, min(max_len + 3, max_width))
        ws.column_dimensions[col_letter].width = calc_w

def main():
    print("=== BẮT ĐẦU XUẤT FILE EXCEL TÁC CHIẾN 14 SHEET ===")
    
    with open('data/processed/k26_behavioral_analysis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    overall = data['overall']
    classes = data['classes']
    students = data['all_students']
    
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)
    
    # ----------------------------------------------------
    # SHEET 1: BANG_CHI_SO_CAI_THIEN_TUNG_LOP
    # ----------------------------------------------------
    ws1 = wb.create_sheet(title="CHI_SO_CAI_THIEN_TUNG_LOP")
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.cell(row=1, column=1, value="BẢNG XẾP HẠNG TỶ LỆ CẢI THIỆN NỀ NẾP TỪNG LỚP KHÓA K26").font = font_title
    ws1.cell(row=2, column=1, value=f"So sánh Môn đầu tiên (SSK101) & Các môn mới đang học | Tổng quy mô: {overall['total_students']} SV | Tỷ lệ cải thiện toàn khóa: {overall['overall_improvement_rate']}%").font = font_subtitle
    
    headers1 = [
        "Hạng", "Lớp Học", "Giảng Viên / CVHT", "Sĩ Số", 
        "Tỷ Lệ Cải Thiện (%)", "Đã Sạch Lỗi TH3 (SV)", "% TH3", 
        "Đang Tiến Bộ TH2 (SV)", "% TH2", "Nguy Cơ Cao TH1 (SV)", "% TH1", 
        "Sốc Môn Mới TH4 (SV)", "% TH4", "Môn Mới Gây Nghẽn", "Ưu Tiên Tác Chiến Tại Lớp"
    ]
    
    ws1.row_dimensions[4].height = 28
    for col_idx, h in enumerate(headers1, 1):
        cell = ws1.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = thin_border
        
    for r_idx, c in enumerate(classes, 5):
        ws1.row_dimensions[r_idx].height = 22
        vals = [
            r_idx - 4,
            c['class'],
            c['teacher'],
            c['total'],
            f"{c['improvement_rate']}%",
            c['th3_count'],
            f"{c['th3_pct']}%",
            c['th2_count'],
            f"{c['th2_pct']}%",
            c['th1_count'],
            f"{c['th1_pct']}%",
            c['th4_count'],
            f"{c['th4_pct']}%",
            c['bottleneck_course'],
            c['priority']
        ]
        
        for col_idx, v in enumerate(vals, 1):
            cell = ws1.cell(row=r_idx, column=col_idx, value=v)
            cell.font = font_regular
            cell.border = thin_border
            
            if col_idx in [1, 4, 6, 8, 10, 12]:
                cell.alignment = align_center
            elif col_idx in [5, 7, 9, 11, 13]:
                cell.alignment = align_center
                cell.font = font_bold
            elif col_idx in [14, 15]:
                cell.alignment = align_left
            else:
                cell.alignment = align_left
                
            # Highlight priority
            if col_idx == 15:
                if '🚨' in str(v):
                    cell.fill = fill_th1
                elif '🟡' in str(v):
                    cell.fill = fill_th4
                else:
                    cell.fill = fill_th3
                    
            if col_idx == 5:
                rate_val = float(str(v).replace('%', ''))
                if rate_val >= 95:
                    cell.fill = fill_th3
                elif rate_val >= 90:
                    cell.fill = fill_th4
                else:
                    cell.fill = fill_th1
                    
    # Total row
    tot_row = 5 + len(classes)
    ws1.row_dimensions[tot_row].height = 24
    total_vals = [
        "--", "TOÀN KHÓA K26", "Tất cả giảng viên", overall['total_students'],
        f"{overall['overall_improvement_rate']}%",
        overall['th3_count'], f"{overall['th3_pct']}%",
        overall['th2_count'], f"{overall['th2_pct']}%",
        overall['th1_count'], f"{overall['th1_pct']}%",
        overall['th4_count'], f"{overall['th4_pct']}%",
        "IT108 / ENG105", "Vào trực tiếp 9 lớp 5-15p"
    ]
    for col_idx, v in enumerate(total_vals, 1):
        cell = ws1.cell(row=tot_row, column=col_idx, value=v)
        cell.font = font_bold
        cell.fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        cell.border = thin_border
        cell.alignment = align_center if col_idx not in [2, 3, 14, 15] else align_left
        
    autofit(ws1)

    # Helper for Action Sheets
    def build_action_sheet(sheet_title, page_title, subtitle, filter_group, header_fill):
        ws = wb.create_sheet(title=sheet_title)
        ws.views.sheetView[0].showGridLines = True
        
        ws.cell(row=1, column=1, value=page_title).font = font_title
        ws.cell(row=2, column=1, value=subtitle).font = font_subtitle
        
        headers = [
            "STT", "Mã SV", "Họ và Tên", "Lớp", 
            "Vi Phạm Môn 1 (CC - BT - EL)", "Vi Phạm Môn Mới", 
            "Bản Chất Vấn Đề", "Kế Hoạch Xử Lý Trực Tiếp 5-15p", 
            "Người Phụ Trách (PIC)", "Hạn Chót (Deadline)",
            "Lý Do Thực Tế Ghi Nhận Tại Lớp", "Cam Kết & Đề Xuất Của Sinh Viên"
        ]
        
        ws.row_dimensions[4].height = 28
        for col_idx, h in enumerate(headers, 1):
            cell = ws.cell(row=4, column=col_idx, value=h)
            cell.font = font_header
            cell.fill = header_fill
            cell.alignment = align_center
            cell.border = thin_border
            
        group_students = [s for s in students if s['group'] == filter_group]
        
        for r_idx, s in enumerate(group_students, 5):
            ws.row_dimensions[r_idx].height = 26
            m1_str = f"CC: {s['m1_att_violate']}% | BT: {s['m1_hw_violate']}% | EL: {s['m1_el_violate']}%"
            m2_str = f"CC: {s['new_att_violate']}% | BT: {s['new_hw_violate']}% | EL: {s['new_el_violate']}% (TB: {s['new_avg_violate']}%)"
            
            vals = [
                r_idx - 4,
                s['code'],
                s['name'],
                s['class'],
                m1_str,
                m2_str,
                s['problem'],
                s['solution'],
                s['pic'],
                s['deadline'],
                "", # Empty for user writing notes at class
                ""  # Empty for commitment
            ]
            
            for col_idx, v in enumerate(vals, 1):
                cell = ws.cell(row=r_idx, column=col_idx, value=v)
                cell.font = font_regular
                cell.border = thin_border
                
                if col_idx in [1, 2, 4, 10]:
                    cell.alignment = align_center
                else:
                    cell.alignment = align_left
                    
                if col_idx == 3:
                    cell.font = font_bold
                    
                if filter_group == 'TH1_PERSISTENT_RISK':
                    cell.fill = fill_th1 if r_idx % 2 == 1 else PatternFill(start_color="FFF0F0", end_color="FFF0F0", fill_type="solid")
                elif filter_group == 'TH4_NEW_EMERGENT_RISK':
                    cell.fill = fill_th4 if r_idx % 2 == 1 else PatternFill(start_color="FFFDF5", end_color="FFFDF5", fill_type="solid")
                    
        autofit(ws, min_width=12, max_width=50)

    # ----------------------------------------------------
    # SHEET 2: TH1_CAN_THIEP_NGAY
    # ----------------------------------------------------
    build_action_sheet(
        sheet_title="TH1_CAN_THIEP_NGAY",
        page_title="DANH SÁCH SINH VIÊN NHÓM TH1 — NGUY CƠ BỎ HỌC (BÁO ĐỘNG ĐỎ)",
        subtitle="HÀNH ĐỘNG TÁC CHIẾN: Gặp riêng 5 phút cuối giờ tại lớp. Lập biên bản cam kết nề nếp. Nếu không cải thiện -> Gọi điện trực tiếp cho Phụ huynh.",
        filter_group="TH1_PERSISTENT_RISK",
        header_fill=fill_dark_red
    )
    
    # ----------------------------------------------------
    # SHEET 3: TH4_SOC_MON_MOI
    # ----------------------------------------------------
    build_action_sheet(
        sheet_title="TH4_SOC_MON_MOI",
        page_title="DANH SÁCH SINH VIÊN NHÓM TH4 — SỐC MÔN MỚI (CẦN GV BỘ MÔN HỖ TRỢ)",
        subtitle="HÀNH ĐỘNG TÁC CHIẾN: Gặp 5 phút giữa giờ tại lớp. Làm rõ phần bài tập/lý thuyết bị nghẽn (IT108/ENG105). Phân công Trợ giảng / Bạn học kèm cặp.",
        filter_group="TH4_NEW_EMERGENT_RISK",
        header_fill=fill_orange
    )
    
    # ----------------------------------------------------
    # SHEET 4: TH2_DANG_TIEN_BO
    # ----------------------------------------------------
    build_action_sheet(
        sheet_title="TH2_DANG_TIEN_BO",
        page_title="DANH SÁCH SINH VIÊN NHÓM TH2 — ĐANG TIẾN BỘ RÕ RỆT (CẦN ĐÔN ĐỐC)",
        subtitle="HÀNH ĐỘNG TÁC CHIẾN: Gặp nhanh 3 phút đầu giờ. Biểu dương sự tiến bộ trước lớp, nhắc nhở nộp bài đúng hạn để giữ vững thành tích.",
        filter_group="TH2_IMPROVING",
        header_fill=fill_blue_header
    )
    
    # ----------------------------------------------------
    # SHEET 5: TH3_DA_KHAC_PHUC
    # ----------------------------------------------------
    build_action_sheet(
        sheet_title="TH3_DA_KHAC_PHUC",
        page_title="DANH SÁCH SINH VIÊN NHÓM TH3 — THÍCH NGHI XUẤT SẮC (SẠCH 100% VI PHẠM)",
        subtitle="HÀNH ĐỘNG: Miễn can thiệp kỷ luật. CVHT gửi thông báo chúc mừng và biểu dương nỗ lực thích nghi của các em qua nhóm Zalo lớp.",
        filter_group="TH3_RESOLVED",
        header_fill=fill_green_header
    )

    # ----------------------------------------------------
    # SHEETS 6 -> 14: 9 SHEETS CHI TIẾT TỪNG LỚP
    # ----------------------------------------------------
    # Priority sort order: TH1 -> TH4 -> TH2 -> TH3
    GROUP_ORDER = {
        'TH1_PERSISTENT_RISK': 1,
        'TH4_NEW_EMERGENT_RISK': 2,
        'TH2_IMPROVING': 3,
        'TH3_RESOLVED': 4
    }
    
    class_names = sorted(list(set(s['class'] for s in students)))
    
    for c_name in class_names:
        c_students = [s for s in students if s['class'] == c_name]
        c_students.sort(key=lambda s: (GROUP_ORDER.get(s['group'], 5), s['name']))
        
        # Clean title for sheet name (max 31 chars)
        clean_title = c_name.replace('HN-KS26-', '').replace('HCM-KS26-', '').replace('HN-K26-', '').replace('HCM-K26-', '')
        sheet_code = f"LỚP_{clean_title}"
        
        ws = wb.create_sheet(title=sheet_code)
        ws.views.sheetView[0].showGridLines = True
        
        ws.cell(row=1, column=1, value=f"DANH SÁCH TÁC CHIẾN LỚP {c_name} (SĨ SỐ: {len(c_students)} SV)").font = font_title
        ws.cell(row=2, column=1, value="Thứ tự ưu tiên gặp tại lớp: 🔴 TH1 (Gặp riêng cuối giờ) -> 🟠 TH4 (Hỗ trợ giữa giờ) -> 🟡 TH2 (Nhắc đầu giờ) -> 🟢 TH3 (Biểu dương)").font = font_subtitle
        
        headers = [
            "Ưu Tiên", "Mã SV", "Họ và Tên", "Phân Nhóm Hành Vi", 
            "Vi Phạm Môn 1", "Vi Phạm Môn Mới", "Vấn Đề Gặp Phải", 
            "Kế Hoạch 5-15p Tại Lớp", "Người Phụ Trách", "Hạn Chót", 
            "Ghi Chú Tại Lớp (Viết tay)", "Cam Kết Của SV"
        ]
        
        ws.row_dimensions[4].height = 28
        for col_idx, h in enumerate(headers, 1):
            cell = ws.cell(row=4, column=col_idx, value=h)
            cell.font = font_header
            cell.fill = fill_navy
            cell.alignment = align_center
            cell.border = thin_border
            
        for r_idx, s in enumerate(c_students, 5):
            ws.row_dimensions[r_idx].height = 24
            m1_str = f"CC {s['m1_att_violate']}% | BT {s['m1_hw_violate']}% | EL {s['m1_el_violate']}%"
            m2_str = f"CC {s['new_att_violate']}% | BT {s['new_hw_violate']}% | EL {s['new_el_violate']}%"
            
            vals = [
                GROUP_ORDER.get(s['group'], 5),
                s['code'],
                s['name'],
                s['group_name'],
                m1_str,
                m2_str,
                s['problem'],
                s['solution'],
                s['pic'],
                s['deadline'],
                "",
                ""
            ]
            
            for col_idx, v in enumerate(vals, 1):
                cell = ws.cell(row=r_idx, column=col_idx, value=v)
                cell.font = font_regular
                cell.border = thin_border
                
                if col_idx in [1, 2, 10]:
                    cell.alignment = align_center
                else:
                    cell.alignment = align_left
                    
                if col_idx == 3:
                    cell.font = font_bold
                    
                # Color code rows
                if s['group'] == 'TH1_PERSISTENT_RISK':
                    cell.fill = fill_th1
                elif s['group'] == 'TH4_NEW_EMERGENT_RISK':
                    cell.fill = fill_th4
                elif s['group'] == 'TH2_IMPROVING':
                    cell.fill = fill_th2
                elif s['group'] == 'TH3_RESOLVED':
                    if r_idx % 2 == 1:
                        cell.fill = fill_th3
                        
        autofit(ws, min_width=10, max_width=45)

    # Save Excel file
    output_path = "output/dashboards/management/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    print(f"Đã xuất thành công file Excel 14 Sheet tại: {output_path}")
    
    # Copy to data/ and deploy_web/
    os.makedirs("data", exist_ok=True)
    shutil.copy(output_path, "data/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx")
    
    os.makedirs("deploy_web/management", exist_ok=True)
    shutil.copy(output_path, "deploy_web/management/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx")
    print("Đã đồng bộ file Excel sang data/ và deploy_web/management/")

if __name__ == '__main__':
    main()

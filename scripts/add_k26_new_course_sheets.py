import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

FILE_PATH = "data/inputs/PTIT_Chiso.xlsx"
BACKUP_PATH = r"C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx"

# Styles matching existing sheets
font_title = Font(name="Calibri", size=14, bold=True, color="1F497D")
font_header = Font(name="Calibri", size=11, bold=True, color="000000")
font_bold = Font(name="Calibri", size=11, bold=True)
font_regular = Font(name="Calibri", size=11)
font_date = Font(name="Calibri", size=11, bold=True, color="1F497D")

fill_header = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
fill_date = PatternFill(start_color="B8CCE4", end_color="B8CCE4", fill_type="solid")
fill_zebra = PatternFill(start_color="F2F5F8", end_color="F2F5F8", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")

SHEET_CONFIGS = [
    {
        "sheet_name": "KS26_Nhapmon_CNTT",
        "title": "Tình hình PTIT_KS26_IT108 - Nhập Môn Công Nghệ Thông Tin",
        "date_str": "29/09/2026",
        "classes": [
            {"stt": 1, "code": "HN-KS26-CNTT1(43)", "gv": "Trịnh Quốc Hai", "cc": 4.65, "bt": 0.0, "el": 4.65},
            {"stt": 2, "code": "HN-KS26-CNTT2(40)", "gv": "Trịnh Quốc Hai", "cc": 2.50, "bt": 0.0, "el": 0.0},
            {"stt": 3, "code": "HN-KS26-CNTT3(42)", "gv": "Lương Quốc Tuấn", "cc": 2.38, "bt": 0.0, "el": 4.76},
            {"stt": 4, "code": "HN-KS26-CNTT4(29)", "gv": "Lương Quốc Tuấn", "cc": 31.03, "bt": 0.0, "el": 34.48},
            {"stt": 5, "code": "HCM-KS26-CNTT1(46)", "gv": "Lê Hà Thanh Sang", "cc": 10.87, "bt": 0.0, "el": 6.52},
            {"stt": 6, "code": "HCM-KS26-CNTT2(45)", "gv": "Lê Hà Thanh Sang", "cc": 13.33, "bt": 0.0, "el": 8.89}
        ]
    },
    {
        "sheet_name": "KS26_KN_Lamviecnhom",
        "title": "Tình hình PTIT_KS26_SKL01 - Kỹ năng làm việc nhóm",
        "date_str": "29/09/2026",
        "classes": [
            {"stt": 1, "code": "HN-KS26-CNTT1(43)", "gv": "Hoàng Thị Hậu", "cc": 4.65, "bt": 0.0, "el": 16.28},
            {"stt": 2, "code": "HN-KS26-CNTT2(40)", "gv": "Hoàng Thị Hậu", "cc": 2.50, "bt": 0.0, "el": 5.00},
            {"stt": 3, "code": "HN-KS26-CNTT3(42)", "gv": "Hoàng Thị Hậu", "cc": 0.0, "bt": 0.0, "el": 0.0},
            {"stt": 4, "code": "HCM-KS26-CNTT1(46)", "gv": "Lê Nhựt Mi", "cc": 0.0, "bt": 0.0, "el": 0.0},
            {"stt": 5, "code": "HCM-KS26-CNTT2(45)", "gv": "Lê Nhựt Mi", "cc": 0.0, "bt": 0.0, "el": 0.0}
        ]
    },
    {
        "sheet_name": "KS26_Basic_Speaking",
        "title": "Tình hình PTIT_KS26_ENG105 - Basic Speaking",
        "date_str": "29/09/2026",
        "classes": [
            {"stt": 1, "code": "HCM-K26-QTKD1(21)", "gv": "Huỳnh Thị Kim Khánh", "cc": 0.0, "bt": 0.0, "el": 0.0},
            {"stt": 2, "code": "HCM-KS26-CNTT1(46)", "gv": "Huỳnh Thị Kim Khánh", "cc": 0.0, "bt": 0.0, "el": 0.0},
            {"stt": 3, "code": "HCM-KS26-CNTT2(45)", "gv": "Huỳnh Thị Kim Khánh", "cc": 20.00, "bt": 0.0, "el": 0.0},
            {"stt": 4, "code": "HN-K26-QTKD1(44)", "gv": "Lò Thị Ngọc Anh", "cc": 13.64, "bt": 0.0, "el": 9.09},
            {"stt": 5, "code": "HN-K26-QTKD2(45)", "gv": "Nguyễn Hồng Nhung", "cc": 22.22, "bt": 0.0, "el": 0.0},
            {"stt": 6, "code": "HN-K26-QTKD3(44)", "gv": "Nguyễn Hồng Nhung", "cc": 25.00, "bt": 0.0, "el": 0.0},
            {"stt": 7, "code": "HN-KS26-CNTT2(40)", "gv": "Nguyễn Hồng Nhung", "cc": 7.50, "bt": 0.0, "el": 0.0},
            {"stt": 8, "code": "HN-KS26-CNTT3(42)", "gv": "Lò Thị Ngọc Anh", "cc": 7.14, "bt": 0.0, "el": 4.76}
        ]
    },
    {
        "sheet_name": "KS26_QTKD_Tuduyphantich",
        "title": "Tình hình PTIT_KS26_SSK103 - Tư duy phân tích",
        "date_str": "29/09/2026",
        "classes": [
            {"stt": 1, "code": "HN-K26-QTKD1(44)", "gv": "Nguyễn Ngọc Vân Khanh", "cc": 9.09, "bt": 0.0, "el": 6.82},
            {"stt": 2, "code": "HN-K26-QTKD2(44)", "gv": "Nguyễn Thị Hồng Minh", "cc": 0.0, "bt": 0.0, "el": 0.0},
            {"stt": 3, "code": "HN-K26-QTKD3(44)", "gv": "Nguyễn Ngọc Vân Khanh", "cc": 15.91, "bt": 0.0, "el": 20.45},
            {"stt": 4, "code": "HCM-K26-QTKD1(21)", "gv": "Lê Thị Bảo Yến", "cc": 0.0, "bt": 0.0, "el": 0.0}
        ]
    },
    {
        "sheet_name": "KS26_QTKD_Tinhocungdung",
        "title": "Tình hình PTIT_KS26_SSK102 - Tin học ứng dụng",
        "date_str": "29/09/2026",
        "classes": [
            {"stt": 1, "code": "HCM-K26-QTKD1(21)", "gv": "Lê Hà Thanh Sang", "cc": 0.0, "bt": 0.0, "el": 0.0},
            {"stt": 2, "code": "HN-K26-QTKD3(44)", "gv": "Nguyễn Thị Hồng Minh", "cc": 29.55, "bt": 0.0, "el": 18.18},
            {"stt": 3, "code": "HN-K26-QTKD1(44)", "gv": "Nguyễn Ngọc Vân Khanh", "cc": 0.0, "bt": 0.0, "el": 0.0},
            {"stt": 4, "code": "HN-K26-QTKD2(44)", "gv": "Nguyễn Ngọc Vân Khanh", "cc": 0.0, "bt": 0.0, "el": 0.0}
        ]
    }
]

def build_sheet(wb, config):
    sname = config["sheet_name"]
    if sname in wb.sheetnames:
        print(f"  Ghi đè sheet sẵn có: {sname}")
        ws = wb[sname]
        wb.remove(ws)
    
    ws = wb.create_sheet(title=sname)
    ws.views.sheetView[0].showGridLines = True

    # Row 1: Title
    ws.cell(row=1, column=1, value=config["title"]).font = font_title

    # Row 3: STT, Lớp, Giảng viên/Trợ giảng, Date
    ws.cell(row=3, column=1, value="STT").font = font_header
    ws.cell(row=3, column=1).alignment = align_center
    ws.cell(row=3, column=1).fill = fill_header

    ws.cell(row=3, column=2, value="Lớp").font = font_header
    ws.cell(row=3, column=2).alignment = align_left
    ws.cell(row=3, column=2).fill = fill_header

    ws.cell(row=3, column=3, value="Giảng viên/Trợ giảng").font = font_header
    ws.cell(row=3, column=3).alignment = align_left
    ws.cell(row=3, column=3).fill = fill_header

    ws.cell(row=3, column=4, value=config["date_str"]).font = font_date
    ws.cell(row=3, column=4).alignment = align_center
    ws.cell(row=3, column=4).fill = fill_date

    # Row 4: Metrics headers under date
    ws.cell(row=4, column=4, value="Chuyên cần").font = font_bold
    ws.cell(row=4, column=4).alignment = align_center
    ws.cell(row=4, column=4).fill = fill_header

    ws.cell(row=4, column=5, value="Bài tập").font = font_bold
    ws.cell(row=4, column=5).alignment = align_center
    ws.cell(row=4, column=5).fill = fill_header

    ws.cell(row=4, column=6, value="Elearning").font = font_bold
    ws.cell(row=4, column=6).alignment = align_center
    ws.cell(row=4, column=6).fill = fill_header

    # Border for headers
    for c in range(1, 7):
        for r in [3, 4]:
            ws.cell(row=r, column=c).border = thin_border

    # Populate classes with zebra empty row (Row 5, 7, 9...)
    cur_row = 5
    for item in config["classes"]:
        ws.cell(row=cur_row, column=1, value=item["stt"]).font = font_regular
        ws.cell(row=cur_row, column=1).alignment = align_center

        ws.cell(row=cur_row, column=2, value=item["code"]).font = font_bold
        ws.cell(row=cur_row, column=2).alignment = align_left

        ws.cell(row=cur_row, column=3, value=item["gv"]).font = font_regular
        ws.cell(row=cur_row, column=3).alignment = align_left

        # Metrics
        c_val = item["cc"]
        b_val = item["bt"]
        e_val = item["el"]

        cell_c = ws.cell(row=cur_row, column=4, value=c_val if c_val is not None else "")
        cell_c.font = font_regular
        cell_c.alignment = align_right

        cell_b = ws.cell(row=cur_row, column=5, value=b_val if b_val is not None else "")
        cell_b.font = font_regular
        cell_b.alignment = align_right

        cell_e = ws.cell(row=cur_row, column=6, value=e_val if e_val is not None else "")
        cell_e.font = font_regular
        cell_e.alignment = align_right

        for c in range(1, 7):
            ws.cell(row=cur_row, column=c).border = thin_border
            ws.cell(row=cur_row + 1, column=c).border = thin_border

        cur_row += 2

    # Column dimensions
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 24
    ws.column_dimensions['C'].width = 28
    ws.column_dimensions['D'].width = 14
    ws.column_dimensions['E'].width = 14
    ws.column_dimensions['F'].width = 14

    print(f"✓ Đã tạo thành công sheet [{sname}] ({len(config['classes'])} lớp)")

def main():
    print(f"Đang mở file {FILE_PATH}...")
    wb = openpyxl.load_workbook(FILE_PATH)

    for cfg in SHEET_CONFIGS:
        build_sheet(wb, cfg)

    # Also build aliases KS25_QTKD_Tuduyphantich and KS25_QTKD_Tinhocungdung if user requested
    aliases = [
        ("KS25_QTKD_Tuduyphantich", SHEET_CONFIGS[3]),
        ("KS25_QTKD_Tinhocungdung", SHEET_CONFIGS[4])
    ]
    for alias_name, orig_cfg in aliases:
        alias_cfg = dict(orig_cfg)
        alias_cfg["sheet_name"] = alias_name
        build_sheet(wb, alias_cfg)

    wb.save(FILE_PATH)
    print(f"\n🎉 ĐÃ CẬP NHẬT TOÀN BỘ CÁC SHEET MỚI VÀO: {FILE_PATH}")
    
    import shutil
    try:
        shutil.copy2(FILE_PATH, BACKUP_PATH)
        print(f"✓ Đã đồng bộ sang file backup {BACKUP_PATH}")
    except Exception as e:
        print(f"⚠️ Lưu ý: Không thể ghi đè file Desktop Backup do đang được mở bởi ứng dụng khác: {e}")

if __name__ == "__main__":
    main()

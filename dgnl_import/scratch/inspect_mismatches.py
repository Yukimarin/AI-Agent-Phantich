import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

main_file = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"

if os.path.exists(main_file):
    wb = openpyxl.load_workbook(main_file, data_only=True)
    sheet = wb["Danh sách ĐGNL CNTT"]
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    
    class_idx = headers.index('Mã lớp hiện tại')
    name_idx = headers.index('Họ và tên học viên')
    sp_idx = headers.index('Sản phẩm (Đ1)')
    vd_idx = headers.index('Vấn đáp (Đ1)')
    th_idx = headers.index('Thực hành (Đ1)')
    tn_idx = headers.index('Trắc nghiệm (Đ1)')
    final_idx = headers.index('Điểm final (Đ1)')
    note_idx = headers.index('Ghi chú')
    bb_idx = headers.index('Biên bản')
    git_idx = headers.index('Link bài thi tự luận')
    
    target_names = ["Nguyễn Quang Vinh", "Phan Thuận Thành", "Võ Thanh Khang", "Đỗ Minh Tuyến"]
    
    print("Mismatched Students in Main Excel:")
    for r in rows[1:]:
        name = str(r[name_idx]).strip()
        if name in target_names:
            print(f"\nName: {name} | Class: {r[class_idx]}")
            print(f"  Prod: {r[sp_idx]} | Oral: {r[vd_idx]} | Prac: {r[th_idx]} | MCQ: {r[tn_idx]} | Final: {r[final_idx]}")
            print(f"  Note: {r[note_idx]}")
            print(f"  Report (Biên bản): {r[bb_idx]}")
            print(f"  Git Link: {r[git_idx]}")
else:
    print("Excel not found.")

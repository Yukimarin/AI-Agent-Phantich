import os
import sys
import json
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

def build_foreign_language_kpi_excel():
    print("=== Khởi tạo trình xuất File Excel KPI Master Khối Ngoại ngữ ===")
    
    # 1. Tải danh mục tasks từ Worklane
    worklane_json_path = "data/processed/project_issues_worklane.json"
    if not os.path.exists(worklane_json_path):
        print(f"Error: Không tìm thấy {worklane_json_path}")
        return
        
    with open(worklane_json_path, "r", encoding="utf-8") as f:
        proj_issues = json.load(f)
        
    foreign_lang_staff = {
        "giáp thị minh hằng": {"name": "Giáp Thị Minh Hằng", "role": "Leader", "rank": 5, "subject": "Tiếng Nhật"},
        "lò thị ngọc anh": {"name": "Lò Thị Ngọc Anh", "role": "Giảng viên", "rank": 5, "subject": "Tiếng Anh"},
        "lê thị đỏ": {"name": "Lê Thị Đỏ", "role": "Giảng viên", "rank": 3, "subject": "Tiếng Nhật"}
    }
    
    raw_tasks = []
    for proj_id, pdata in proj_issues.items():
        pinfo = pdata.get('project_info', {})
        pname = pinfo.get('name', proj_id)
        issues = pdata.get('issues', {}).get('issues', [])
        for iss in issues:
            assignee = str(iss.get('assignee') or '')
            for k, meta in foreign_lang_staff.items():
                if k in assignee.lower():
                    raw_tasks.append({
                        "staff_name": meta["name"],
                        "role": meta["role"],
                        "rank": meta["rank"],
                        "subject": meta["subject"],
                        "project_name": pname,
                        "task_code": iss.get('code', ''),
                        "task_title": iss.get('title', ''),
                        "state": iss.get('state', 'Chưa rõ'),
                        "due_date": str(iss.get('dueDate') or '')[:10],
                        "spent_time": iss.get('spentTime'),
                        "estimated_time": iss.get('estimatedTime')
                    })
                    break
                    
    print(f"✓ Đã trích xuất {len(raw_tasks)} tasks thực tế của 3 nhân sự Khối Ngoại ngữ.")

    # 2. Định nghĩa Danh mục 22 Đầu việc chuẩn Khối Ngoại ngữ
    # [STT, Nhóm công việc, Tên đầu việc chuẩn, ĐVT, Vai trò, R1_h, R2_h, R3_h, R4_h, R5_h, Key_code, Ghi chú]
    standard_kpi_items = [
        # Nhóm 1: Phát triển Chương trình & Giáo án
        (1, "1. Phát triển CTĐT & Giáo án", "Xây dựng khung Chương trình Đào tạo (CTĐT) môn học", "Môn học", "Giảng viên", 
         None, None, 20.0, 16.0, 12.0, "NN-RND-CTDT", "Khung chương trình, syllabus, chuẩn đầu ra PLO"),
        (2, "1. Phát triển CTĐT & Giáo án", "Xây dựng Timeline chi tiết học kỳ & Phân phối buổi học", "Học kỳ", "Giảng viên", 
         6.0, 5.0, 4.0, 3.0, 2.5, "NN-RND-TIMELINE", "Kế hoạch tiến độ chi tiết từng tuần/buổi học"),
        (3, "1. Phát triển CTĐT & Giáo án", "Soạn Lesson Plan (Kế hoạch bài giảng chi tiết)", "Buổi học", "Giảng viên", 
         3.0, 2.5, 2.0, 1.5, 1.0, "NN-RND-LESSONPLAN", "Giáo án chi tiết các hoạt động, thời lượng từng phần"),
        (4, "1. Phát triển CTĐT & Giáo án", "Chuẩn hóa quy trình đào tạo & Bàn giao CTĐT", "Quy trình", "Giảng viên", 
         4.0, 3.5, 3.0, 2.5, 2.0, "NN-RND-QUYTRINH", "Quy chuẩn loại hình buổi học (Rikai, Luyện tập, Demo)"),
        
        # Nhóm 2: Sản xuất Học liệu Số
        (5, "2. Sản xuất Học liệu Số", "Soạn Slide bài giảng chuẩn theo Topic/Session", "Topic", "Giảng viên", 
         4.0, 3.0, 2.5, 2.0, 1.5, "NN-HL-SLIDE", "Kế thừa chuẩn CNTT/QTKD; Slide trực quan, tương tác"),
        (6, "2. Sản xuất Học liệu Số", "Quay và dựng Video bài giảng lý thuyết / Rikai", "Video", "Giảng viên", 
         4.0, 3.5, 3.0, 2.5, 2.0, "NN-HL-VIDEO", "Video 15-20p chuẩn studio; kịch bản, quay, hậu kỳ"),
        (7, "2. Sản xuất Học liệu Số", "Biên soạn bộ Quiz / Bài tập tương tác theo buổi", "Bộ Quiz", "Giảng viên", 
         2.0, 1.5, 1.0, 0.75, 0.5, "NN-HL-QUIZ", "Bộ 10-15 câu hỏi trắc nghiệm/điền từ củng cố bài học"),
        (8, "2. Sản xuất Học liệu Số", "Tạo bộ Flashcards từ vựng & Chữ Hán / Ngữ pháp", "Bộ thẻ", "Giảng viên", 
         2.0, 1.5, 1.0, 0.75, 0.5, "NN-HL-FLASHCARD", "Bộ thẻ nhớ điện tử tích hợp trên app/hệ thống"),
        (9, "2. Sản xuất Học liệu Số", "Upload, đóng gói và cấu hình học liệu lên LMS", "Khóa học", "Giảng viên, Trợ giảng", 
         4.0, 3.0, 2.5, 2.0, 1.5, "NN-HL-UPLOADLMS", "Đưa tài nguyên lên LMS, kiểm tra link, setting quyền"),
        (10, "2. Sản xuất Học liệu Số", "Rà soát học liệu & Lập danh mục tài nguyên môn học", "Danh mục", "Giảng viên, Trợ giảng", 
         3.0, 2.5, 2.0, 1.5, 1.0, "NN-HL-RASOAT", "Kiểm toán tính đồng bộ, bản quyền và độ hoàn thiện"),

        # Nhóm 3: Giảng dạy & Triển khai Lớp
        (11, "3. Giảng dạy & Triển khai Lớp", "Chuẩn bị buổi học trước giờ lên lớp", "Buổi học", "Giảng viên", 
         1.0, 0.75, 0.67, 0.5, 0.5, "NN-GD-CHUANBI", "Đọc giáo án, kiểm tra thiết bị, tài liệu lớp"),
        (12, "3. Giảng dạy & Triển khai Lớp", "Giảng dạy trên lớp chính khóa / Lớp Talent", "Ca học", "Giảng viên", 
         2.0, 2.0, 2.0, 2.0, 2.0, "NN-GD-GIANGDAY", "Định mức theo thời lượng ca học tiêu chuẩn (90-120p)"),
        (13, "3. Giảng dạy & Triển khai Lớp", "Giảng dạy lớp Demo & Tuần lễ Orientation Week", "Buổi", "Giảng viên", 
         2.5, 2.5, 2.5, 2.5, 2.5, "NN-GD-DEMO", "Buổi demo tuyển sinh, định hướng học tập đầu khóa"),
        (14, "3. Giảng dạy & Triển khai Lớp", "Hỗ trợ học viên, giải đáp học tập ngoài giờ", "Giờ", "Giảng viên, Trợ giảng", 
         1.0, 1.0, 1.0, 1.0, 1.0, "NN-GD-HOTRO", "Tư vấn kèm cặp học viên yếu, trả lời diễn đàn"),

        # Nhóm 4: Khảo thí & Đánh giá Năng lực
        (15, "4. Khảo thí & Đánh giá Năng lực", "Biên soạn Ngân hàng đề thi / Bộ đề khảo thí (40 câu)", "Đề thi", "Giảng viên", 
         6.0, 5.0, 4.0, 3.0, 2.5, "NN-KT-SOANDE", "Biên soạn bộ đề trắc nghiệm kèm đáp án và giải thích"),
        (16, "4. Khảo thí & Đánh giá Năng lực", "Thẩm định, rà soát và Phê duyệt đề thi", "Đề thi", "Giảng viên", 
         None, None, 1.5, 1.0, 0.75, "NN-KT-DUYETDE", "Phản biện chuyên môn, duyệt đề thi chính thức"),
        (17, "4. Khảo thí & Đánh giá Năng lực", "Coi thi khảo sát / Test đầu vào / Thi cuối kỳ", "Ca thi", "Giảng viên, Trợ giảng", 
         2.0, 2.0, 2.0, 2.0, 2.0, "NN-KT-COITHI", "Giám sát ca thi trực tiếp hoặc trên phòng máy"),
        (18, "4. Khảo thí & Đánh giá Năng lực", "Chấm bài thi tự luận / Đánh giá Nói - Viết", "Bài thi / SV", "Giảng viên", 
         0.5, 0.4, 0.33, 0.25, 0.2, "NN-KT-CHAMBAI", "Chấm test đầu vào, chấm Speaking/Writing rubric"),

        # Nhóm 5: Vận hành LMS AI & Quản lý Đối tác
        (19, "5. Vận hành LMS AI & Đối tác", "Cấu hình môn học & Test quy trình trên LMS AI", "Môn học", "Giảng viên", 
         8.0, 6.0, 4.5, 3.5, 3.0, "NN-VH-LMSAI", "Thiết lập flow môn học, kiểm thử tính năng AI trợ giảng"),
        (20, "5. Vận hành LMS AI & Đối tác", "Order tính năng & Nghiệm thu hiệu chỉnh LMS AI", "Yêu cầu", "Giảng viên", 
         None, None, 2.0, 1.5, 1.0, "NN-VH-ORDERAI", "Đưa yêu cầu cải tiến LMS và nghiệm thu chức năng"),
        (21, "5. Vận hành LMS AI & Đối tác", "Làm việc với đối tác bản quyền giáo trình", "Lần", "Giảng viên", 
         3.0, 3.0, 2.5, 2.0, 1.5, "NN-VH-BANQUYEN", "Xác minh license JF Marugoto, đàm phán sách"),
        (22, "5. Vận hành LMS AI & Đối tác", "Giám sát & Nghiệm thu đối tác liên kết (Prep/Jaxtina)", "Tháng", "Giảng viên", 
         None, None, 6.0, 5.0, 4.0, "NN-VH-DOITAC", "Đối soát tiến độ, chất lượng học viên với đối tác ngoài"),

        # Nhóm 6: Quản trị Chuyên môn & Nhân sự
        (23, "6. Quản trị Chuyên môn & Nhân sự", "Họp giao ban bộ môn / Giao ban toàn Viện", "Cuộc họp", "Giảng viên, Trợ giảng", 
         1.5, 1.5, 1.5, 1.5, 1.5, "NN-QT-GIAOBAN", "Định mức cố định 90 phút/cuộc họp giao ban"),
        (24, "6. Quản trị Chuyên môn & Nhân sự", "Rà soát CV & Phỏng vấn tuyển dụng GV Ngoại ngữ", "Ứng viên", "Giảng viên", 
         None, None, 1.5, 1.25, 1.0, "NN-QT-TUYENDUNG", "Lọc hồ sơ chuyên môn và phỏng vấn trực tiếp"),
        (25, "6. Quản trị Chuyên môn & Nhân sự", "Dự giờ, Đánh giá Teaching Demo và Feedback GV", "Buổi Demo", "Giảng viên", 
         None, None, 2.0, 1.5, 1.25, "NN-QT-DEMOFB", "Dự giờ dạy thử, đánh giá phương pháp sư phạm"),
        (26, "6. Quản trị Chuyên môn & Nhân sự", "Báo cáo định kỳ tiến độ dự án & Nhân sự bộ môn", "Báo cáo", "Giảng viên", 
         3.0, 2.5, 2.0, 1.5, 1.0, "NN-QT-BAOCAO", "Tổng hợp số liệu tiến độ, giờ công, nhân sự")
    ]

    # Hàm mapping tự động task Worklane sang Mã Key chuẩn
    def map_worklane_task(title, proj):
        t_low = title.lower()
        p_low = proj.lower()
        
        if "video" in t_low or "quay" in t_low:
            return "NN-HL-VIDEO", "Quay và dựng Video bài giảng lý thuyết / Rikai"
        elif "slide" in t_low or "silde" in t_low or "ppt" in t_low:
            return "NN-HL-SLIDE", "Soạn Slide bài giảng chuẩn theo Topic/Session"
        elif "quiz" in t_low or "câu hỏi" in t_low:
            return "NN-HL-QUIZ", "Biên soạn bộ Quiz / Bài tập tương tác theo buổi"
        elif "flashcard" in t_low or "thẻ" in t_low:
            return "NN-HL-FLASHCARD", "Tạo bộ Flashcards từ vựng & Chữ Hán / Ngữ pháp"
        elif "upload" in t_low or "lên hệ thống" in t_low or "đẩy quiz" in t_low:
            return "NN-HL-UPLOADLMS", "Upload, đóng gói và cấu hình học liệu lên LMS"
        elif "lesson plan" in t_low or "giáo án" in t_low:
            return "NN-RND-LESSONPLAN", "Soạn Lesson Plan (Kế hoạch bài giảng chi tiết)"
        elif "timeline" in t_low:
            return "NN-RND-TIMELINE", "Xây dựng Timeline chi tiết học kỳ & Phân phối buổi học"
        elif "khung chương trình" in t_low or "ctđt" in t_low or "chương trình đào tạo" in t_low:
            return "NN-RND-CTDT", "Xây dựng khung Chương trình Đào tạo (CTĐT) môn học"
        elif "quy trình" in t_low or "chuẩn hóa" in t_low:
            return "NN-RND-QUYTRINH", "Chuẩn hóa quy trình đào tạo & Bàn giao CTĐT"
        elif "lms ai" in t_low or "lms" in t_low:
            if "order" in t_low or "hiệu chỉnh" in t_low:
                return "NN-VH-ORDERAI", "Order tính năng & Nghiệm thu hiệu chỉnh LMS AI"
            return "NN-VH-LMSAI", "Cấu hình môn học & Test quy trình trên LMS AI"
        elif "đề thi" in t_low or "ngân hàng" in t_low:
            if "duyệt" in t_low:
                return "NN-KT-DUYETDE", "Thẩm định, rà soát và Phê duyệt đề thi"
            return "NN-KT-SOANDE", "Biên soạn Ngân hàng đề thi / Bộ đề khảo thí (40 câu)"
        elif "coi thi" in t_low:
            return "NN-KT-COITHI", "Coi thi khảo sát / Test đầu vào / Thi cuối kỳ"
        elif "chấm bài" in t_low or "chấm thi" in t_low:
            return "NN-KT-CHAMBAI", "Chấm bài thi tự luận / Đánh giá Nói - Viết"
        elif "giảng dạy" in t_low or "lớp talent" in t_low:
            return "NN-GD-GIANGDAY", "Giảng dạy trên lớp chính khóa / Lớp Talent"
        elif "demo" in t_low or "orientation" in t_low or "định hướng" in t_low:
            if "feedback" in t_low or "interview" in t_low:
                return "NN-QT-DEMOFB", "Dự giờ, Đánh giá Teaching Demo và Feedback GV"
            return "NN-GD-DEMO", "Giảng dạy lớp Demo & Tuần lễ Orientation Week"
        elif "phỏng vấn" in t_low or "tuyển dụng" in t_low or "cv" in t_low:
            return "NN-QT-TUYENDUNG", "Rà soát CV & Phỏng vấn tuyển dụng GV Ngoại ngữ"
        elif "họp" in t_low or "giao ban" in t_low:
            return "NN-QT-GIAOBAN", "Họp giao ban bộ môn / Giao ban toàn Viện"
        elif "bản quyền" in t_low or "license" in t_low or "marugoto" in t_low or "sách" in t_low:
            return "NN-VH-BANQUYEN", "Làm việc với đối tác bản quyền giáo trình"
        elif "báo cáo" in t_low:
            return "NN-QT-BAOCAO", "Báo cáo định kỳ tiến độ dự án & Nhân sự bộ môn"
        elif "prep" in p_low or "jaxtina" in p_low:
            return "NN-VH-DOITAC", "Giám sát & Nghiệm thu đối tác liên kết (Prep/Jaxtina)"
        else:
            return "NN-HL-RASOAT", "Rà soát học liệu & Lập danh mục tài nguyên môn học"

    # 3. Tạo Workbook
    wb = openpyxl.Workbook()
    wb.remove(wb.active) # Xóa sheet default
    
    # Định dạng Styles cao cấp
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid") # Deep Navy
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    
    sub_header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid") # Soft Blue
    sub_header_font = Font(name="Calibri", size=11, bold=True, color="1F4E79")
    
    group_fill = PatternFill(start_color="F2F4F7", end_color="F2F4F7", fill_type="solid")
    group_font = Font(name="Calibri", size=11, bold=True, color="002060")
    
    regular_font = Font(name="Calibri", size=10, color="000000")
    bold_font = Font(name="Calibri", size=10, bold=True, color="000000")
    na_font = Font(name="Calibri", size=10, italic=True, color="7F7F7F")
    
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")
    align_wrap = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # ═══════════════════════════════════════════════════════════════
    # SHEET 1: MA TRẬN ĐỊNH MỨC THEO RANK (KPI_MASTER_MA_TRAN)
    # ═══════════════════════════════════════════════════════════════
    ws1 = wb.create_sheet(title="KPI_MASTER_MA_TRAN")
    ws1.views.sheetView[0].showGridLines = True
    
    # Tiêu đề báo cáo
    ws1.merge_cells("A1:Q1")
    title_cell = ws1["A1"]
    title_cell.value = "BẢNG ĐỊNH MỨC KPI MASTER KHỐI NGOẠI NGỮ (TIẾNG NHẬT & TIẾNG ANH)"
    title_cell.font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    title_cell.fill = header_fill
    title_cell.alignment = align_center
    ws1.row_dimensions[1].height = 40
    
    ws1.merge_cells("A2:Q2")
    sub_cell = ws1["A2"]
    sub_cell.value = "Chuẩn hóa theo cấu trúc Master của CNTT & QTKD — Căn cứ 283+ tasks thực tế trên Worklane — Áp dụng cho Giảng viên & Trợ giảng"
    sub_cell.font = Font(name="Calibri", size=10, italic=True, color="1F4E79")
    sub_cell.fill = sub_header_fill
    sub_cell.alignment = align_center
    ws1.row_dimensions[2].height = 24
    
    # Dòng Header gộp cột (Dòng 4)
    ws1.row_dimensions[4].height = 26
    ws1.row_dimensions[5].height = 26
    
    # Thiết lập multi-level header
    ws1.merge_cells("A4:A5")
    ws1["A4"] = "STT"
    ws1.merge_cells("B4:B5")
    ws1["B4"] = "Nhóm công việc"
    ws1.merge_cells("C4:C5")
    ws1["C4"] = "Tên đầu công việc chuẩn"
    ws1.merge_cells("D4:D5")
    ws1["D4"] = "Đơn vị tính"
    ws1.merge_cells("E4:E5")
    ws1["E4"] = "Vai trò phụ trách"
    
    ws1.merge_cells("F4:J4")
    ws1["F4"] = "ĐỊNH MỨC THỜI GIAN (GIỜ)"
    ws1["F5"] = "R1 (TG)"
    ws1["G5"] = "R2 (TG)"
    ws1["H5"] = "R3 (GV)"
    ws1["I5"] = "R4 (GV)"
    ws1["J5"] = "R5 (Lead/GV)"
    
    ws1.merge_cells("K4:O4")
    ws1["K4"] = "ĐỊNH MỨC THỜI GIAN (PHÚT)"
    ws1["K5"] = "R1"
    ws1["L5"] = "R2"
    ws1["M5"] = "R3"
    ws1["N5"] = "R4"
    ws1["O5"] = "R5"
    
    ws1.merge_cells("P4:P5")
    ws1["P4"] = "Mã Key Worklane"
    ws1.merge_cells("Q4:Q5")
    ws1["Q4"] = "Ghi chú & Căn cứ thực tế"
    
    # Style header dòng 4 & 5
    for r in [4, 5]:
        for c in range(1, 18):
            cell = ws1.cell(row=r, column=c)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = align_center
            cell.border = thin_border
            
    # Đổ dữ liệu Sheet 1
    current_group = ""
    row_idx = 6
    for item in standard_kpi_items:
        stt, grp, name, unit, role, r1, r2, r3, r4, r5, key, note = item
        
        # Thêm header nhóm nếu đổi nhóm
        if grp != current_group:
            current_group = grp
            ws1.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=17)
            g_cell = ws1.cell(row=row_idx, column=1)
            g_cell.value = f"▶ {grp.upper()}"
            g_cell.font = group_font
            g_cell.fill = group_fill
            g_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
            for c in range(1, 18):
                ws1.cell(row=row_idx, column=c).border = thin_border
            ws1.row_dimensions[row_idx].height = 24
            row_idx += 1
            
        ws1.row_dimensions[row_idx].height = 22
        
        ws1.cell(row=row_idx, column=1, value=stt).alignment = align_center
        ws1.cell(row=row_idx, column=2, value=grp).alignment = align_left
        ws1.cell(row=row_idx, column=3, value=name).alignment = align_left
        ws1.cell(row=row_idx, column=4, value=unit).alignment = align_center
        ws1.cell(row=row_idx, column=5, value=role).alignment = align_center
        
        # Định mức giờ
        for col_i, val in enumerate([r1, r2, r3, r4, r5], start=6):
            c_cell = ws1.cell(row=row_idx, column=col_i)
            if val is not None:
                c_cell.value = val
                c_cell.font = regular_font
                c_cell.number_format = "0.0#"
            else:
                c_cell.value = "—"
                c_cell.font = na_font
            c_cell.alignment = align_right
            
        # Định mức phút
        for col_i, val in enumerate([r1, r2, r3, r4, r5], start=11):
            c_cell = ws1.cell(row=row_idx, column=col_i)
            if val is not None:
                c_cell.value = int(round(val * 60))
                c_cell.font = regular_font
                c_cell.number_format = "#,##0"
            else:
                c_cell.value = "—"
                c_cell.font = na_font
            c_cell.alignment = align_right
            
        ws1.cell(row=row_idx, column=16, value=key).alignment = align_center
        ws1.cell(row=row_idx, column=17, value=note).alignment = align_left
        
        for c in range(1, 18):
            cell = ws1.cell(row=row_idx, column=c)
            cell.border = thin_border
            if c not in range(6, 16):
                cell.font = regular_font
                
        row_idx += 1

    # ═══════════════════════════════════════════════════════════════
    # SHEET 2: DANH MỤC IMPORT WORKLANE CHUẨN FORM CNTT & QTKD
    # (Mỗi dòng tương ứng 1 Rank để nạp trực tiếp vào Worklane dropdown)
    # ═══════════════════════════════════════════════════════════════
    ws2 = wb.create_sheet(title="IMPORT_WORKLANE_DROPDOWN")
    ws2.views.sheetView[0].showGridLines = True
    
    # Header chuẩn như file Quản lý hiệu suất đào tạo.xlsx của CNTT
    import_headers = [
        "No", "Loại công việc", "Vị trí", "Rank", 
        "Thời gian tiêu chuẩn (phút)", "Thời gian tiêu chuẩn (giờ)", 
        "Đơn vị tính", "Nhóm công việc", "Key Worklane", "Ghi chú phân bổ"
    ]
    
    ws2.append(import_headers)
    ws2.row_dimensions[1].height = 28
    for c in range(1, len(import_headers) + 1):
        cell = ws2.cell(row=1, column=c)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border
        
    line_no = 1
    for item in standard_kpi_items:
        stt, grp, name, unit, role, r1, r2, r3, r4, r5, key, note = item
        ranks_vals = [(1, r1, "Trợ giảng"), (2, r2, "Trợ giảng"), (3, r3, "Giảng viên"), (4, r4, "Giảng viên"), (5, r5, "Leader/Giảng viên")]
        for r_num, r_val, r_role in ranks_vals:
            if r_val is not None:
                mins = int(round(r_val * 60))
                full_key = f"{key}-R{r_num}"
                row_data = [
                    line_no,
                    name,
                    r_role,
                    r_num,
                    mins,
                    r_val,
                    unit,
                    grp,
                    full_key,
                    note
                ]
                ws2.append(row_data)
                curr_r = ws2.max_row
                ws2.row_dimensions[curr_r].height = 20
                for c in range(1, len(import_headers) + 1):
                    c_cell = ws2.cell(row=curr_r, column=c)
                    c_cell.font = regular_font
                    c_cell.border = thin_border
                    if c in [1, 4]:
                        c_cell.alignment = align_center
                    elif c in [5, 6]:
                        c_cell.alignment = align_right
                    else:
                        c_cell.alignment = align_left
                line_no += 1

    # ═══════════════════════════════════════════════════════════════
    # SHEET 3: MAPPING TOÀN BỘ TASKS WORKLANE THỰC TẾ (283+ TASKS)
    # ═══════════════════════════════════════════════════════════════
    ws3 = wb.create_sheet(title="MAPPING_WORKLANE_TASKS")
    ws3.views.sheetView[0].showGridLines = True
    
    map_headers = [
        "STT", "Nhân sự", "Vai trò", "Rank", "Bộ môn", 
        "Dự án trên Worklane", "Mã Task", "Tiêu đề Task Worklane", 
        "Trạng thái", "Hạn hoàn thành (Due Date)", "Thời gian khai báo", 
        "Ánh xạ Mã KPI Master", "Tên Đầu việc Chuẩn tương ứng"
    ]
    
    ws3.append(map_headers)
    ws3.row_dimensions[1].height = 28
    for c in range(1, len(map_headers) + 1):
        cell = ws3.cell(row=1, column=c)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border
        
    for idx, t in enumerate(raw_tasks, start=1):
        map_key, map_name = map_worklane_task(t["task_title"], t["project_name"])
        spent_str = f"{t['spent_time']}h" if t['spent_time'] else "Chưa log"
        
        row_data = [
            idx,
            t["staff_name"],
            t["role"],
            f"R{t['rank']}",
            t["subject"],
            t["project_name"],
            t["task_code"],
            t["task_title"],
            t["state"],
            t["due_date"] if t["due_date"] else "Không đặt",
            spent_str,
            map_key,
            map_name
        ]
        ws3.append(row_data)
        curr_r = ws3.max_row
        ws3.row_dimensions[curr_r].height = 20
        for c in range(1, len(map_headers) + 1):
            c_cell = ws3.cell(row=curr_r, column=c)
            c_cell.font = regular_font
            c_cell.border = thin_border
            if c in [1, 3, 4, 5, 7, 9, 10, 11, 12]:
                c_cell.alignment = align_center
            else:
                c_cell.alignment = align_left

    # 4. Auto-fit độ rộng các cột cho cả 3 Sheet
    for ws in [ws1, ws2, ws3]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            # Không đo các dòng merged ở header ws1
            start_check_row = 4 if ws == ws1 else 1
            for cell in col[start_check_row:]:
                if cell.value:
                    val_str = str(cell.value)
                    # Bỏ qua các dòng gộp nhóm dài
                    if ws == ws1 and val_str.startswith("▶"):
                        continue
                    max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 3, 11)
            
    # Tinh chỉnh một số cột đặc thù
    ws1.column_dimensions["A"].width = 6
    ws1.column_dimensions["B"].width = 28
    ws1.column_dimensions["C"].width = 44
    ws1.column_dimensions["P"].width = 20
    ws1.column_dimensions["Q"].width = 38
    
    ws2.column_dimensions["B"].width = 42
    ws2.column_dimensions["H"].width = 28
    ws2.column_dimensions["I"].width = 20
    ws2.column_dimensions["J"].width = 35
    
    ws3.column_dimensions["B"].width = 20
    ws3.column_dimensions["F"].width = 32
    ws3.column_dimensions["H"].width = 50
    ws3.column_dimensions["L"].width = 20
    ws3.column_dimensions["M"].width = 44

    # 5. Lưu File Excel
    output_excel_path = "output/reports/KPI_Master_Khoi_Ngoai_Ngu.xlsx"
    os.makedirs(os.path.dirname(output_excel_path), exist_ok=True)
    wb.save(output_excel_path)
    print(f"✓ ĐÃ XUẤT THÀNH CÔNG FILE EXCEL: {output_excel_path}")
    print(f"  - Sheet 1: KPI_MASTER_MA_TRAN (Ma trận 26 đầu việc chuẩn phân theo R1 ➔ R5)")
    print(f"  - Sheet 2: IMPORT_WORKLANE_DROPDOWN (Danh mục chuẩn form CNTT/QTKD để import dropdown)")
    print(f"  - Sheet 3: MAPPING_WORKLANE_TASKS (Bảng ánh xạ {len(raw_tasks)} tasks thực tế từ Worklane)")

if __name__ == "__main__":
    build_foreign_language_kpi_excel()

# Complete Suite Builder for Standardized Educational Reports
import openpyxl
import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

def clean_str(val):
    if val is None: return ""
    return str(val).strip()

def clean_name(name):
    if name is None: return ""
    name = str(name).strip()
    name = re.sub(r"\s+\d+$", "", name)
    return name.lower()

def parse_float(val):
    if val is None or str(val).strip() == "": return 0.0
    try:
        return float(val)
    except:
        return 0.0

def load_data():
    excel_path = "inputs/Danh sách thi ĐGNL.xlsx" if os.path.exists("inputs/Danh sách thi ĐGNL.xlsx") else r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx"
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    
    # 1. Bảng điểm (Đợt 1)
    sh_bd = wb["Bảng điểm (Đợt 1)"]
    headers_bd = [cell.value for cell in sh_bd[1]]
    
    c_bd_name = headers_bd.index("Họ và tên học viên")
    c_bd_class = headers_bd.index("Mã lớp hiện tại")
    c_bd_branch = headers_bd.index("Cơ sở đào tạo")
    c_bd_sp = headers_bd.index("Đ1_Sản phẩm_CNTT")
    c_bd_vd = headers_bd.index("Đ1_Vấn đáp_CNTT")
    c_bd_th = headers_bd.index("Đ1_Thực hành_CNTT")
    c_bd_tn = headers_bd.index("Đ1_Trắc nghiệm_CNTT")
    c_bd_cntt = headers_bd.index("Đ1_Điểm CNTT (Final)")
    c_bd_qtkd = headers_bd.index("Đ1_Điểm QTKD (Final)")
    c_bd_read = headers_bd.index("Đ1_Reading")
    c_bd_listen = headers_bd.index("Đ1_Listening")
    c_bd_ta = headers_bd.index("Đ1_Tiếng Anh (Final)")
    c_bd_knm = headers_bd.index("Đ1_Kỹ năng mềm (Final)")
    
    bd_records = {}
    for r in range(2, sh_bd.max_row + 1):
        name_val = clean_str(sh_bd.cell(row=r, column=c_bd_name+1).value)
        cname = clean_str(sh_bd.cell(row=r, column=c_bd_class+1).value)
        branch = clean_str(sh_bd.cell(row=r, column=c_bd_branch+1).value)
        if not name_val: continue
        
        k = f"{clean_name(name_val)}_{cname}"
        bd_records[k] = {
            "name": name_val, "class": cname, "branch": branch,
            "sp": parse_float(sh_bd.cell(row=r, column=c_bd_sp+1).value),
            "vd": parse_float(sh_bd.cell(row=r, column=c_bd_vd+1).value),
            "th": parse_float(sh_bd.cell(row=r, column=c_bd_th+1).value),
            "tn": parse_float(sh_bd.cell(row=r, column=c_bd_tn+1).value),
            "cntt": parse_float(sh_bd.cell(row=r, column=c_bd_cntt+1).value),
            "qtkd": parse_float(sh_bd.cell(row=r, column=c_bd_qtkd+1).value),
            "reading": parse_float(sh_bd.cell(row=r, column=c_bd_read+1).value),
            "listening": parse_float(sh_bd.cell(row=r, column=c_bd_listen+1).value),
            "ta": parse_float(sh_bd.cell(row=r, column=c_bd_ta+1).value),
            "knm": parse_float(sh_bd.cell(row=r, column=c_bd_knm+1).value)
        }

    # 2. CNTT Sheet
    sh_cntt = wb["Danh sách ĐGNL CNTT"]
    headers_c = [cell.value for cell in sh_cntt[1]]
    c_c_name = headers_c.index("Họ và tên học viên")
    c_c_class = headers_c.index("Mã lớp hiện tại")
    c_c_branch = headers_c.index("Cơ sở đào tạo")
    c_c_ca = headers_c.index("Ca thi")
    c_c_phong = headers_c.index("Phòng thi")
    c_c_sp = headers_c.index("Sản phẩm (Đ1)")
    c_c_vd = headers_c.index("Vấn đáp (Đ1)")
    c_c_th = headers_c.index("Thực hành (Đ1)")
    c_c_tn = headers_c.index("Trắc nghiệm (Đ1)")
    c_c_final = headers_c.index("Điểm final ĐGNL (Lần 1)")
    c_c_res = headers_c.index("Kết quả final ĐGNL (Lần 1)")
    c_c_gc = headers_c.index("Ghi chú")
    c_c_bs_dm = headers_c.index("Điểm danh thi BS") if "Điểm danh thi BS" in headers_c else -1

    ks24_students = []
    ks25_students = []

    for r in range(2, sh_cntt.max_row + 1):
        name_val = clean_str(sh_cntt.cell(row=r, column=c_c_name+1).value)
        cname = clean_str(sh_cntt.cell(row=r, column=c_c_class+1).value)
        branch = clean_str(sh_cntt.cell(row=r, column=c_c_branch+1).value)
        if not name_val or not cname: continue
        if "QTKD" in cname: continue  # Skip QTKD in CNTT sheet

        ca = clean_str(sh_cntt.cell(row=r, column=c_c_ca+1).value)
        phong = clean_str(sh_cntt.cell(row=r, column=c_c_phong+1).value)
        sp = parse_float(sh_cntt.cell(row=r, column=c_c_sp+1).value)
        vd = parse_float(sh_cntt.cell(row=r, column=c_c_vd+1).value)
        th = parse_float(sh_cntt.cell(row=r, column=c_c_th+1).value)
        tn = parse_float(sh_cntt.cell(row=r, column=c_c_tn+1).value)
        gc = clean_str(sh_cntt.cell(row=r, column=c_c_gc+1).value)
        bs_val = parse_float(sh_cntt.cell(row=r, column=c_c_bs_dm+1).value) if c_c_bs_dm != -1 else 0.0

        k = f"{clean_name(name_val)}_{cname}"
        matched = bd_records.get(k, {})
        ta = matched.get("ta", 0.0)
        knm = matched.get("knm", 0.0)
        read = matched.get("reading", 0.0)
        listen = matched.get("listening", 0.0)

        if sp == 0.0 and matched.get("sp", 0.0) > 0.0: sp = matched["sp"]
        if vd == 0.0 and matched.get("vd", 0.0) > 0.0: vd = matched["vd"]
        if th == 0.0 and matched.get("th", 0.0) > 0.0: th = matched["th"]
        if tn == 0.0 and matched.get("tn", 0.0) > 0.0: tn = matched["tn"]

        if "KS24" in cname:
            if "HN" in cname:
                calc_final = round(sp * 0.3 + vd * 0.2 + (th * 0.2 + tn * 0.8) * 0.5, 1)
            else:
                calc_final = round(vd * 0.4 + (th * 0.2 + tn * 0.8) * 0.6, 1)
                
            final_10 = round(calc_final / 10.0, 1)
            is_absent = (sp == 0 and vd == 0 and th == 0 and tn == 0) and bs_val != 1.0

            if is_absent:
                tier = 0
                tier_label = "Mức 0: Chưa tham gia khảo thí / Vắng thi"
            elif final_10 >= 8.0:
                tier = 3
                tier_label = "Mức 3: Năng lực Xuất sắc / Làm chủ Tốt"
            elif final_10 >= 6.0:
                tier = 2
                tier_label = "Mức 2: Đạt Chuẩn Đầu ra Doanh nghiệp"
            elif final_10 >= 4.0:
                tier = 1
                tier_label = "Mức 1: Đạt Yêu cầu Cơ bản / Cần Bổ trợ"
            else:
                tier = 0
                tier_label = "Mức 0: Chưa đạt Chuẩn Kiến thức Cốt lõi"

            tech_score = max(th, sp)
            if is_absent:
                persona = "Vắng thi / Cần xác minh lý do khảo thí"
                action_plan = "Tổ chức khảo thí bổ sung và xác nhận tinh thần học tập."
                persona_cls = "badge-muted"
            elif tech_score >= 65.0 and vd < 50.0:
                persona = "Vững Thực hành Kỹ thuật - Hạn chế Diễn đạt Vấn đáp"
                action_plan = "Bắt buộc tham gia Phòng Phỏng vấn Chuyên môn Giả định (Simulated Technical Interview) rèn luyện phương pháp STAR."
                persona_cls = "badge-danger"
            elif tech_score < 50.0 and (vd >= 50.0 or knm >= 75.0):
                persona = "Thế mạnh Giao tiếp / Kỹ năng Mềm - Hạn chế Lập trình Sâu"
                action_plan = "Tư vấn phân luồng định hướng: IT Business Analyst (BA), Software QA/Tester, Project Coordinator."
                persona_cls = "badge-warning"
            elif tech_score >= 65.0 and vd >= 50.0:
                persona = "Đạt Chuẩn Năng lực Toàn diện (Kỹ thuật & Vấn đáp)"
                action_plan = "Bổ trợ tiếng Anh chuyên ngành và kiến trúc hệ thống nâng cao để đáp ứng doanh nghiệp quốc tế."
                persona_cls = "badge-success"
            elif tech_score < 50.0 and vd < 50.0 and knm < 70.0:
                persona = "Chưa đạt Chuẩn Kiến thức Cốt lõi (Cần Phụ đạo)"
                action_plan = "Bắt buộc tham gia Khóa Học Bổ trợ Tăng cường Java Core & Spring Boot 3 tuần trước khi nhận Đồ án Tốt nghiệp."
                persona_cls = "badge-danger"
            else:
                persona = "Đạt Mức Trung bình Cơ bản (Cần Củng cố)"
                action_plan = "Tăng cường luyện tập các chuyên đề Giao dịch đồng thời và Bảo mật phân quyền API."
                persona_cls = "badge-info"

            ks24_students.append({
                "name": name_val, "class": cname, "branch": branch, "ca": ca, "phong": phong,
                "sp": sp, "vd": vd, "th": th, "tn": tn, "final": calc_final, "final_10": final_10,
                "knm": knm, "ta": ta, "reading": read, "listening": listen,
                "is_absent": is_absent, "is_pass": final_10 >= 5.0,
                "tier": tier, "tier_label": tier_label,
                "persona": persona, "action_plan": action_plan, "persona_cls": persona_cls, "gc": gc
            })

        elif "KS25" in cname:
            calc_final = round(th * 0.7 + tn * 0.3, 1)
            final_10 = round(calc_final / 10.0, 1)
            is_absent = (th == 0 and tn == 0) and bs_val != 1.0

            if is_absent:
                tier = 0
                tier_label = "Mức 0: Chưa tham gia khảo thí / Vắng thi"
            elif final_10 >= 8.0:
                tier = 3
                tier_label = "Mức 3: Năng lực Xuất sắc / Làm chủ Tốt"
            elif final_10 >= 6.0:
                tier = 2
                tier_label = "Mức 2: Đạt Chuẩn Đầu ra Khóa học"
            elif final_10 >= 4.0:
                tier = 1
                tier_label = "Mức 1: Đạt Yêu cầu Cơ bản / Cần Bổ trợ"
            else:
                tier = 0
                tier_label = "Mức 0: Chưa đạt Chuẩn Kiến thức Cốt lõi"

            if is_absent:
                persona = "Vắng thi / Cần xác minh lý do khảo thí"
                action_plan = "Tổ chức khảo thí bổ sung và xác nhận tinh thần học tập."
                persona_cls = "badge-muted"
            elif th >= 50.0:
                persona = "Nắm vững Năng lực Thực hành Lập trình (Solid Coder)"
                action_plan = "Tiếp tục học thẳng lộ trình chuyên sâu Kỳ III (Cấu trúc dữ liệu & Thuật toán, Machine Learning, RAG/LLM)."
                persona_cls = "badge-success"
            elif tn >= 65.0 and th < 50.0:
                persona = "Nắm vững Lý thuyết - Hạn chế Kỹ năng Thực hành Lập trình"
                action_plan = "Bắt buộc tham gia Khóa Học Bổ trợ Tăng cường FastAPI Live-Coding 2 tuần để hình thành phản xạ code độc lập."
                persona_cls = "badge-danger"
            elif knm >= 75.0 and th < 50.0:
                persona = "Thế mạnh Giao tiếp / Kỹ năng Mềm - Hạn chế Lập trình Sâu"
                action_plan = "Định hướng phân luồng môn Phân tích Nghiệp vụ (BA) và Kiểm thử Phần mềm (QA) từ đầu Kỳ III."
                persona_cls = "badge-warning"
            elif tn < 50.0 and th < 50.0:
                persona = "Chưa đạt Chuẩn Kiến thức Cốt lõi (Cần Phụ đạo)"
                action_plan = "Phụ đạo lại kiến thức lập trình Python Core căn bản trước khi vào chương trình học kỳ mới."
                persona_cls = "badge-danger"
            else:
                persona = "Đạt Mức Trung bình Cơ bản (Cần Củng cố)"
                action_plan = "Thực hành xây dựng API theo mẫu kiến trúc chuẩn (Boilerplate Project Skeleton)."
                persona_cls = "badge-info"

            ks25_students.append({
                "name": name_val, "class": cname, "branch": branch, "ca": ca, "phong": phong,
                "th": th, "tn": tn, "final": calc_final, "final_10": final_10,
                "knm": knm, "ta": ta, "reading": read, "listening": listen,
                "is_absent": is_absent, "is_pass": final_10 >= 5.0,
                "tier": tier, "tier_label": tier_label,
                "persona": persona, "action_plan": action_plan, "persona_cls": persona_cls, "gc": gc
            })

    # 3. QTKD Sheet
    sh_qtkd = wb["Danh sách ĐGNL QTKD"]
    headers_q = [cell.value for cell in sh_qtkd[1]]
    c_q_name = headers_q.index("Họ và tên học viên")
    c_q_class = headers_q.index("Mã lớp hiện tại")
    c_q_branch = headers_q.index("Cơ sở đào tạo")
    c_q_nhom = headers_q.index("Nhóm")
    c_q_ca = headers_q.index("Ca thi")
    c_q_phong = headers_q.index("Phòng thi")
    c_q_d1 = headers_q.index("Điểm thi (Đợt 1)")
    c_q_d2 = headers_q.index("Điểm thi (Đợt 2)")
    c_q_final = headers_q.index("Điểm final ĐGNL (Lần 1)")
    c_q_res = headers_q.index("Kết quả final ĐGNL (Lần 1)")
    c_q_gc = headers_q.index("Ghi chú")

    qtkd_students = []
    for r in range(2, sh_qtkd.max_row + 1):
        cname = clean_str(sh_qtkd.cell(row=r, column=c_q_class+1).value)
        if "QTKD" not in cname: continue
        name_val = clean_str(sh_qtkd.cell(row=r, column=c_q_name+1).value)
        if not name_val: continue

        branch = clean_str(sh_qtkd.cell(row=r, column=c_q_branch+1).value)
        nhom = clean_str(sh_qtkd.cell(row=r, column=c_q_nhom+1).value) or "Chưa phân nhóm"
        ca = clean_str(sh_qtkd.cell(row=r, column=c_q_ca+1).value)
        phong = clean_str(sh_qtkd.cell(row=r, column=c_q_phong+1).value)
        d1 = parse_float(sh_qtkd.cell(row=r, column=c_q_d1+1).value)
        d2 = parse_float(sh_qtkd.cell(row=r, column=c_q_d2+1).value)
        final = parse_float(sh_qtkd.cell(row=r, column=c_q_final+1).value)
        res = clean_str(sh_qtkd.cell(row=r, column=c_q_res+1).value)
        gc = clean_str(sh_qtkd.cell(row=r, column=c_q_gc+1).value)

        k = f"{clean_name(name_val)}_{cname}"
        matched = bd_records.get(k, {})
        ta = matched.get("ta", 0.0)
        knm = matched.get("knm", 0.0)
        read = matched.get("reading", 0.0)
        listen = matched.get("listening", 0.0)

        is_absent = (final == 0 and d1 == 0 and d2 == 0)
        final_10 = round(final / 10.0, 1)
        is_pass = res == "Đạt" or final >= 50.0

        if is_absent:
            tier = 0
            tier_label = "Mức 0: Chưa tham gia khảo thí / Vắng thi"
        elif final >= 75.0 and knm >= 85.0 and ta >= 450.0:
            tier = 3
            tier_label = "Mức 3: Năng lực Xuất sắc / Sẵn sàng Môi trường Quốc tế"
        elif final >= 65.0 and knm >= 75.0:
            tier = 2
            tier_label = "Mức 2: Đạt Chuẩn Đầu ra Doanh nghiệp"
        elif final >= 50.0:
            tier = 1
            tier_label = "Mức 1: Đạt Yêu cầu Cơ bản / Cần Bổ trợ"
        else:
            tier = 0
            tier_label = "Mức 0: Chưa đạt Chuẩn Kiến thức Cốt lõi"

        if is_absent:
            persona = "Vắng thi / Cần xác minh lý do khảo thí"
            action_plan = "Xác nhận lý do vắng và tổ chức bảo vệ dự án bổ sung."
            persona_cls = "badge-muted"
        elif final >= 70.0 and ta >= 450.0:
            persona = "Năng lực Toàn diện / Sẵn sàng Doanh nghiệp Quốc tế"
            action_plan = "Ưu tiên giới thiệu vào các chương trình Quản trị viên Tập sự (Management Trainee) tại doanh nghiệp đa quốc gia."
            persona_cls = "badge-success"
        elif final >= 70.0 and ta < 350.0:
            persona = "Vững Chuyên môn & Thuyết trình - Khoảng trống Ngoại ngữ"
            action_plan = "Bắt buộc tham gia Khóa Học Bổ trợ Tiếng Anh Thương mại (Business English Workshop) từ Kỳ III."
            persona_cls = "badge-warning"
        elif knm >= 85.0 and final >= 60.0:
            persona = "Thế mạnh Đàm phán & Giao tiếp Thương mại"
            action_plan = "Định hướng phát triển vị trí Chuyên viên Phát triển Kinh doanh (B2B Sales) & Quản lý Khách hàng (Account Executive)."
            persona_cls = "badge-info"
        elif final < 50.0:
            persona = "Chưa đạt Chuẩn Kiến thức Cốt lõi (Cần Phụ đạo)"
            action_plan = "Phụ đạo lại phương pháp lập kế hoạch kinh doanh và phân tích thị trường."
            persona_cls = "badge-danger"
        else:
            persona = "Đạt Mức Trung bình Cơ bản"
            action_plan = "Nâng cao kỹ năng lập kế hoạch Marketing số và Quản trị vận hành."
            persona_cls = "badge-info"

        qtkd_students.append({
            "name": name_val, "class": cname, "branch": branch, "nhom": nhom, "ca": ca, "phong": phong,
            "d1": d1, "d2": d2, "final": final, "final_10": final_10,
            "knm": knm, "ta": ta, "reading": read, "listening": listen,
            "is_absent": is_absent, "is_pass": is_pass,
            "tier": tier, "tier_label": tier_label,
            "persona": persona, "action_plan": action_plan, "persona_cls": persona_cls, "gc": gc
        })

    return {
        "ks24": ks24_students,
        "ks25": ks25_students,
        "qtkd": qtkd_students
    }

if __name__ == "__main__":
    data = load_data()
    print("Data loaded successfully:")
    print("KS24 count:", len(data["ks24"]))
    print("KS25 count:", len(data["ks25"]))
    print("QTKD count:", len(data["qtkd"]))

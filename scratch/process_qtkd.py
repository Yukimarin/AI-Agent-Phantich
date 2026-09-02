import openpyxl
import os
import sys
import re
import json

sys.stdout.reconfigure(encoding="utf-8")

def clean_str(val):
    if val is None: return ""
    return str(val).strip()

def clean_name(name):
    if name is None: return ""
    name = str(name).strip()
    name = re.sub(r"\s+\d+$", "", name)
    return name.lower()

def main():
    excel_path = "inputs/Danh sách thi ĐGNL.xlsx" if os.path.exists("inputs/Danh sách thi ĐGNL.xlsx") else r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx"
    
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    
    # 1. Load Bảng điểm (Đợt 1) for all scores
    sh_bd = wb["Bảng điểm (Đợt 1)"]
    headers_bd = [cell.value for cell in sh_bd[1]]
    
    c_bd_name = headers_bd.index("Họ và tên học viên")
    c_bd_class = headers_bd.index("Mã lớp hiện tại")
    c_bd_email = headers_bd.index("Email học viên") if "Email học viên" in headers_bd else -1
    c_bd_src = headers_bd.index("SourceID")
    c_bd_qtkd = headers_bd.index("Đ1_Điểm QTKD (Final)")
    c_bd_ta = headers_bd.index("Đ1_Tiếng Anh (Final)")
    c_bd_knm = headers_bd.index("Đ1_Kỹ năng mềm (Final)")
    c_bd_read = headers_bd.index("Đ1_Reading")
    c_bd_listen = headers_bd.index("Đ1_Listening")
    
    bd_data = {}
    for r in range(2, sh_bd.max_row + 1):
        name_val = clean_str(sh_bd.cell(row=r, column=c_bd_name+1).value)
        cname = clean_str(sh_bd.cell(row=r, column=c_bd_class+1).value)
        if not name_val: continue
        
        qtkd_val = sh_bd.cell(row=r, column=c_bd_qtkd+1).value
        ta_val = sh_bd.cell(row=r, column=c_bd_ta+1).value
        knm_val = sh_bd.cell(row=r, column=c_bd_knm+1).value
        read_val = sh_bd.cell(row=r, column=c_bd_read+1).value
        listen_val = sh_bd.cell(row=r, column=c_bd_listen+1).value
        
        k = f"{clean_name(name_val)}_{cname}"
        bd_data[k] = {
            "qtkd_score": float(qtkd_val) if qtkd_val is not None and str(qtkd_val).strip() != "" else 0.0,
            "ta_score": float(ta_val) if ta_val is not None and str(ta_val).strip() != "" else 0.0,
            "knm_score": float(knm_val) if knm_val is not None and str(knm_val).strip() != "" else 0.0,
            "reading": float(read_val) if read_val is not None and str(read_val).strip() != "" else 0.0,
            "listening": float(listen_val) if listen_val is not None and str(listen_val).strip() != "" else 0.0
        }
        
    # 2. Load Danh sách ĐGNL QTKD
    sh_qtkd = wb["Danh sách ĐGNL QTKD"]
    headers_q = [cell.value for cell in sh_qtkd[1]]
    
    c_q_name = headers_q.index("Họ và tên học viên")
    c_q_class = headers_q.index("Mã lớp hiện tại")
    c_q_email = headers_q.index("Email học viên")
    c_q_nhom = headers_q.index("Nhóm")
    c_q_ca = headers_q.index("Ca thi")
    c_q_phong = headers_q.index("Phòng thi")
    c_q_d1 = headers_q.index("Điểm thi (Đợt 1)")
    c_q_d2 = headers_q.index("Điểm thi (Đợt 2)")
    c_q_final = headers_q.index("Điểm final ĐGNL (Lần 1)")
    c_q_res = headers_q.index("Kết quả final ĐGNL (Lần 1)")
    c_q_gc = headers_q.index("Ghi chú")
    c_q_bb = headers_q.index("Biên bản")
    
    students = []
    for r in range(2, sh_qtkd.max_row + 1):
        cname = clean_str(sh_qtkd.cell(row=r, column=c_q_class+1).value)
        if "QTKD" not in cname:
            continue
        name = clean_str(sh_qtkd.cell(row=r, column=c_q_name+1).value)
        if not name:
            continue
            
        email = clean_str(sh_qtkd.cell(row=r, column=c_q_email+1).value)
        nhom = clean_str(sh_qtkd.cell(row=r, column=c_q_nhom+1).value) or "Chưa phân nhóm"
        ca = clean_str(sh_qtkd.cell(row=r, column=c_q_ca+1).value)
        phong = clean_str(sh_qtkd.cell(row=r, column=c_q_phong+1).value)
        d1 = sh_qtkd.cell(row=r, column=c_q_d1+1).value
        d2 = sh_qtkd.cell(row=r, column=c_q_d2+1).value
        final = sh_qtkd.cell(row=r, column=c_q_final+1).value
        res = clean_str(sh_qtkd.cell(row=r, column=c_q_res+1).value)
        gc = clean_str(sh_qtkd.cell(row=r, column=c_q_gc+1).value)
        bb = clean_str(sh_qtkd.cell(row=r, column=c_q_bb+1).value)
        
        final_val = float(final) if final is not None and str(final).strip() != "" else 0.0
        d1_val = float(d1) if d1 is not None and str(d1).strip() != "" else 0.0
        d2_val = float(d2) if d2 is not None and str(d2).strip() != "" else 0.0
        
        # Merge scores from bd_data
        k = f"{clean_name(name)}_{cname}"
        matched = bd_data.get(k, {})
        ta_score = matched.get("ta_score", 0.0)
        knm_score = matched.get("knm_score", 0.0)
        reading = matched.get("reading", 0.0)
        listening = matched.get("listening", 0.0)
        
        is_pass = res == "Đạt" or final_val >= 50.0
        is_absent = final_val == 0.0 and d1_val == 0.0 and d2_val == 0.0
        
        # Readiness Tier & Career Orientation
        # Tier 3: Global Business & Management (QTKD >= 75, KNM >= 85, TA >= 500)
        # Tier 2: Corporate Ready (QTKD >= 65, KNM >= 75)
        # Tier 1: Foundation Pass (QTKD >= 50)
        # Tier 0: Below Standard
        if is_absent:
            tier = 0
            tier_label = "Mức 0: Vắng thi / Chưa có dữ liệu"
        elif final_val >= 75.0 and knm_score >= 85.0 and ta_score >= 450.0:
            tier = 3
            tier_label = "Mức 3: Làm chủ & Sẵn sàng Quốc tế (Global Ready)"
        elif final_val >= 65.0 and knm_score >= 75.0:
            tier = 2
            tier_label = "Mức 2: Đạt chuẩn Doanh nghiệp (Corporate Ready)"
        elif final_val >= 50.0:
            tier = 1
            tier_label = "Mức 1: Đạt cơ bản (Basic Pass)"
        else:
            tier = 0
            tier_label = "Mức 0: Chưa đạt chuẩn (Below Standard)"
            
        # Career recommendation
        if tier == 0:
            career = "Bổ trợ & Đào tạo lại"
            career_note = "Cần củng cố kiến thức quản trị căn bản và kỹ năng lập kế hoạch."
        elif knm_score >= 90.0 and final_val >= 70.0:
            career = "Sales & Account Management"
            career_note = "Kỹ năng giao tiếp và đàm phán xuất sắc, phù hợp kinh doanh dự án B2B."
        elif ta_score >= 450.0 and final_val >= 70.0:
            career = "Business Analyst (BA) / Quốc tế"
            career_note = "Ngoại ngữ tốt, tư duy quy trình và phân tích kinh doanh mạch lạc."
        elif knm_score >= 80.0:
            career = "Digital Marketing & Truyền thông"
            career_note = "Tư duy sáng tạo, khả năng làm việc nhóm và bảo vệ kế hoạch tốt."
        else:
            career = "Vận hành & Quản trị Kinh doanh"
            career_note = "Nền tảng nghiệp vụ đạt yêu cầu, cần nâng cao ngoại ngữ giao tiếp."
            
        students.append({
            "name": name,
            "class": cname,
            "email": email,
            "nhom": nhom,
            "ca": ca,
            "phong": phong,
            "d1": d1_val,
            "d2": d2_val,
            "final": final_val,
            "final_10": round(final_val / 10.0, 1),
            "res": res if res else ("Đạt" if is_pass else "Không đạt"),
            "is_pass": is_pass,
            "is_absent": is_absent,
            "ta_score": ta_score,
            "knm_score": knm_score,
            "reading": reading,
            "listening": listening,
            "tier": tier,
            "tier_label": tier_label,
            "career": career,
            "career_note": career_note,
            "gc": gc,
            "bb": bb
        })
        
    print(f"Total QTKD students processed: {len(students)}")
    with open("scratch/qtkd_data.json", "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)
        
    print("Saved scratch/qtkd_data.json successfully!")

if __name__ == "__main__":
    main()

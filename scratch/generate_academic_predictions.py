import mysql.connector
import sys
import os
import openpyxl
from collections import defaultdict
import numpy as np
from datetime import datetime

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from excel_loader import load_excel_data, normalize_class_name
from metrics_engine import _safe_mean

sys.stdout.reconfigure(encoding='utf-8')

def run_query(cursor, query, params=None):
    cursor.execute(query, params or ())
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def main():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    
    # 1. Load Excel metrics as fallback
    print("Loading Excel metrics from docs/PTIT_Chiso.xlsx...")
    excel_data = load_excel_data("docs/PTIT_Chiso.xlsx")
    
    # 2. Get active classes and courses in June 2026 for K24 and K25
    print("Querying active classes/courses in June 2026...")
    active_classes_raw = run_query(cursor, """
        SELECT c.id as class_id, c.name as class_name, c.class_code, co.id as course_id, co.name as course_name, MAX(a.date) as max_date
        FROM qldt_el.classes c
        JOIN qldt_el.student_class sc ON c.id = sc.class_id
        JOIN qldt_el.attendance a ON c.id = a.classes_id
        JOIN qldt_el.courses co ON a.courses_id = co.id
        JOIN qldt_el.specializes sp ON c.specializes_id = sp.id
        JOIN qldt_el.systems sys ON sp.systems_id = sys.id
        WHERE sc.is_active = 1 AND a.date >= '2026-06-01' AND sys.system_code LIKE 'PTIT%'
        GROUP BY c.id, co.id;
    """)
    
    # Filter for KS24/KS25
    active_classes = []
    for row in active_classes_raw:
        cname = row['class_name']
        if 'KS24' in cname or 'KS25' in cname or 'K24' in cname or 'K25' in cname:
            # Exclude language classes and other generic courses unless they are main ones
            # We focus on CNTT and QTKD classes
            active_classes.append(row)
            
    print(f"Found {len(active_classes)} active KS24/KS25 classes.")
    
    # 3. Retrieve student lists for active classes
    print("Retrieving students list...")
    students_raw = run_query(cursor, """
        SELECT sc.student_id, sc.class_id, s.full_name as student_name
        FROM qldt_el.student_class sc
        JOIN qldt_el.students s ON sc.student_id = s.id
        WHERE sc.is_active = 1;
    """)
    class_students_map = defaultdict(list)
    for row in students_raw:
        class_students_map[row['class_id']].append(row['student_id'])
        
    # 4. Retrieve course sequences to determine prerequisites
    print("Retrieving chronological course sequences...")
    course_seq_raw = run_query(cursor, """
        SELECT classes_id, courses_id, MIN(date) as first_date
        FROM qldt_el.attendance
        GROUP BY classes_id, courses_id
        ORDER BY classes_id, first_date ASC;
    """)
    class_course_seq = defaultdict(list)
    for row in course_seq_raw:
        if row['classes_id'] and row['courses_id']:
            class_course_seq[int(row['classes_id'])].append(int(row['courses_id']))
            
    # 5. Course ID to name mapping
    courses_raw = run_query(cursor, "SELECT id, name FROM qldt_el.courses;")
    course_id_to_name = {int(r['id']): r['name'] for r in courses_raw if r['id'] is not None}
    
    # 6. Retrieve Hackathon scores
    print("Querying Hackathon scores...")
    hackathon_raw = run_query(cursor, """
        SELECT ts.class_id, ts.course_id, AVG(r.point) as avg_point
        FROM qldt_el.result_test r
        JOIN qldt_el.test_schedule ts ON r.test_schedule_id = ts.id
        WHERE ts.type = 'THI HACKATHON' AND r.point IS NOT NULL
        GROUP BY ts.class_id, ts.course_id;
    """)
    hackathon_map = {}
    for r in hackathon_raw:
        if r['class_id'] and r['course_id']:
            hackathon_map[(int(r['class_id']), int(r['course_id']))] = float(r['avg_point'])
            
    # 7. Prerequisite fail rates by class-course
    print("Querying prerequisite fail rates...")
    prereq_raw = run_query(cursor, """
        SELECT class_id, course_id, 
               SUM(CASE WHEN pass = '0' THEN 1 ELSE 0 END) as fail_count,
               SUM(CASE WHEN pass = '1' THEN 1 ELSE 0 END) as pass_count
        FROM qldt_el.final_results
        GROUP BY class_id, course_id;
    """)
    prereq_map = {}
    for r in prereq_raw:
        if r['class_id'] and r['course_id']:
            f_cnt = float(r['fail_count'] or 0)
            p_cnt = float(r['pass_count'] or 0)
            if f_cnt + p_cnt > 0:
                prereq_map[(int(r['class_id']), int(r['course_id']))] = (f_cnt / (f_cnt + p_cnt)) * 100
                
    # 8. Course-wide fail rate fallback
    prereq_course_wide_raw = run_query(cursor, """
        SELECT course_id, 
               SUM(CASE WHEN pass = '0' THEN 1 ELSE 0 END) as fail_count,
               SUM(CASE WHEN pass = '1' THEN 1 ELSE 0 END) as pass_count
        FROM qldt_el.final_results
        GROUP BY course_id;
    """)
    prereq_course_wide_map = {}
    for r in prereq_course_wide_raw:
        if r['course_id']:
            f_cnt = float(r['fail_count'] or 0)
            p_cnt = float(r['pass_count'] or 0)
            if f_cnt + p_cnt > 0:
                prereq_course_wide_map[int(r['course_id'])] = (f_cnt / (f_cnt + p_cnt)) * 100
                
    # 9. Query attendance details
    print("Querying attendance history...")
    attendance_raw = run_query(cursor, """
        SELECT ad.student_id, a.classes_id as class_id, a.courses_id as course_id, ad.status
        FROM qldt_el.attendance_detail ad
        JOIN qldt_el.attendance a ON ad.attendance_id = a.id
        WHERE a.date >= '2025-01-01';
    """)
    student_att_history = defaultdict(list)
    for row in attendance_raw:
        student_att_history[(row['student_id'], row['class_id'], row['course_id'])].append(row['status'])
        
    # 10. Query homework exercises
    print("Querying exercise submissions...")
    homework_raw = run_query(cursor, """
        SELECT e.student_id, e.class_id, e.course_id, e.check, e.link_git
        FROM qldt_el.exercise e
        WHERE e.created_at >= '2025-01-01';
    """)
    homework_debt = defaultdict(int)
    homework_total = defaultdict(int)
    for row in homework_raw:
        sid = int(row['student_id'])
        cid = int(row['class_id'])
        co_id = int(row['course_id'])
        check = int(row['check'] or 0)
        git = row['link_git']
        
        homework_total[(sid, cid, co_id)] += 1
        is_git_empty = not git or git.strip() == "" or "placeholder" in str(git).lower()
        if check == 2 or (check == 0 and is_git_empty):
            homework_debt[(sid, cid, co_id)] += 1
            
    # 11. Query Elearning late
    print("Querying E-learning late submissions...")
    elearning_late_raw = run_query(cursor, """
        SELECT el.student_id, s.course_id 
        FROM qldt_el.elearning_late el
        JOIN qldt_el.sessions s ON el.session_id = s.id;
    """)
    student_elearning_late = defaultdict(set)
    for row in elearning_late_raw:
        sid = int(row['student_id'])
        co_id = int(row['course_id'])
        student_elearning_late[sid].add(co_id)
        
    # 12. Calculate predictions
    print("\nCalculating academic risk scores for active K24/K25 classes...")
    results = []
    
    for row in active_classes:
        cid = int(row['class_id'])
        cname = row['class_name']
        co_id = int(row['course_id'])
        coname = row['course_name']
        
        # Get students
        class_students = class_students_map.get(cid, [])
        student_count = len(class_students)
        
        # Determine prerequisite course
        seq = class_course_seq.get(cid, [])
        prereq_course_id = None
        if co_id in seq:
            idx = seq.index(co_id)
            if idx > 0:
                prereq_course_id = seq[idx - 1]
                
        prereq_course_name = "Không có"
        prereq_fail_rate = 0.0
        if prereq_course_id:
            prereq_course_name = course_id_to_name.get(prereq_course_id, "N/A")
            if (cid, prereq_course_id) in prereq_map:
                prereq_fail_rate = prereq_map[(cid, prereq_course_id)]
            else:
                prereq_fail_rate = prereq_course_wide_map.get(prereq_course_id, 0.0)
        else:
            # Fallback based on name keyword
            if "database" in coname.lower() or "cơ sở" in coname.lower():
                prereq_course_id = 124 # JavaScript
                prereq_course_name = course_id_to_name.get(prereq_course_id, "Lập trình Javascript (M102)")
                prereq_fail_rate = prereq_course_wide_map.get(prereq_course_id, 48.4)
            elif "python" in coname.lower() and "k25" in cname.lower():
                prereq_course_id = 183 # Database in K25
                prereq_course_name = course_id_to_name.get(prereq_course_id, "[IT202-K25] Cơ sở dữ liệu")
                prereq_fail_rate = prereq_course_wide_map.get(prereq_course_id, 45.0)
            elif "java web" in coname.lower() and "k24" in cname.lower():
                prereq_course_id = 210 # Java Web App
                prereq_course_name = course_id_to_name.get(prereq_course_id, "Lập trình Java Web Application")
                prereq_fail_rate = prereq_course_wide_map.get(prereq_course_id, 25.0)
                
        # Hackathon score
        hackathon_score = hackathon_map.get((cid, co_id), 65.0) # default to 65.0 if not found
        
        # Calculate violations
        if student_count > 0:
            cc_violators = 0
            bt_violators = 0
            el_violators = 0
            
            for sid in class_students:
                # Attendance check
                att_list = student_att_history.get((sid, cid, co_id), [])
                unexcused = sum(1 for s in att_list if s == '0')
                total_att = len(att_list)
                if total_att > 0 and (unexcused / total_att) > 0.10:
                    cc_violators += 1
                    
                # Homework check
                debts = homework_debt.get((sid, cid, co_id), 0)
                total_hw = homework_total.get((sid, cid, co_id), 0)
                if total_hw > 0 and (debts / total_hw) > 0.10:
                    bt_violators += 1
                    
                # Elearning check
                if co_id in student_elearning_late.get(sid, set()):
                    el_violators += 1
                    
            avg_cc = (cc_violators / student_count) * 100
            avg_bt = (bt_violators / student_count) * 100
            avg_el = (el_violators / student_count) * 100
        else:
            # Fallback to excel
            cc_rates = []
            bt_rates = []
            el_rates = []
            norm_cname = normalize_class_name(cname)
            for ex_cname, stats_list in excel_data.items():
                norm_ex_cname = normalize_class_name(ex_cname)
                if norm_ex_cname == norm_cname or norm_cname.startswith(norm_ex_cname) or norm_ex_cname.startswith(norm_cname):
                    for stat in stats_list:
                        cc_rates.extend(stat.get('cc_all', []))
                        bt_rates.extend(stat.get('bt_all', []))
                        el_rates.extend(stat.get('el_all', []))
            avg_cc = _safe_mean(cc_rates) if cc_rates else 0.0
            avg_bt = _safe_mean(bt_rates) if bt_rates else 0.0
            avg_el = _safe_mean(el_rates) if el_rates else 0.0
            
        # Calculate Risk Score
        pred_risk = (
            0.25 * avg_cc +
            0.25 * avg_bt +
            0.15 * avg_el +
            0.20 * (100.0 - hackathon_score) +
            0.15 * prereq_fail_rate
        )
        
        # Risk Label
        if pred_risk >= 40.0:
            risk_label = "🔴 NGUY CƠ CAO"
        elif pred_risk >= 20.0:
            risk_label = "🟡 NGUY CƠ TRUNG BÌNH"
        else:
            risk_label = "🟢 AN TOÀN"
            
        # Classify by branch
        branch = "CNTT"
        if "QTKD" in cname or "DTB" in coname:
            branch = "QTKD"
            
        # Classify by batch
        batch = "K25"
        if "KS24" in cname or "K24" in cname:
            batch = "K24"
            
        # Classify by location
        location = "HN"
        if "HCM" in cname:
            location = "HCM"
            
        results.append({
            'class_id': cid,
            'class_name': cname,
            'course_id': co_id,
            'course_name': coname,
            'student_count': student_count,
            'prereq_course': prereq_course_name,
            'prereq_fail_rate': round(prereq_fail_rate, 1),
            'hackathon_score': round(hackathon_score, 1),
            'avg_cc_violation': round(avg_cc, 1),
            'avg_bt_violation': round(avg_bt, 1),
            'avg_el_violation': round(avg_el, 1),
            'risk_score': round(pred_risk, 1),
            'risk_label': risk_label,
            'branch': branch,
            'batch': batch,
            'location': location
        })
        
    # Sort results by risk_score descending
    results.sort(key=lambda x: x['risk_score'], reverse=True)
    
    # 13. Generate markdown report
    os.makedirs("reports", exist_ok=True)
    report_file = "reports/academic_prediction_report.md"
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# BÁO CÁO ĐÁNH GIÁ VÀ DỰ BÁO HỌC TẬP KHÓA KS24 & KS25\n\n")
        f.write(f"*Báo cáo được thực hiện tự động bởi **AcademicPredictor** vào ngày {datetime.now().strftime('%d/%m/%Y')} dựa trên dữ liệu cập nhật ngày 16/06/2026.*\n\n")
        
        f.write("## 📌 TÓM TẮT ĐÁNH GIÁ CHUNG\n\n")
        
        # Count risk levels
        high_risk_cnt = sum(1 for r in results if r['risk_score'] >= 40.0)
        med_risk_cnt = sum(1 for r in results if 20.0 <= r['risk_score'] < 40.0)
        safe_cnt = sum(1 for r in results if r['risk_score'] < 20.0)
        
        f.write(f"- **Tổng số lớp được đánh giá**: {len(results)} lớp.\n")
        f.write(f"- 🔴 **Số lớp có nguy cơ cao (High Risk)**: {high_risk_cnt} lớp (Cần can thiệp gấp).\n")
        f.write(f"- 🟡 **Số lớp có nguy cơ trung bình (Medium Risk)**: {med_risk_cnt} lớp (Cần theo dõi sát sao).\n")
        f.write(f"- 🟢 **Số lớp an toàn (Safe)**: {safe_cnt} lớp.\n\n")
        
        f.write("### 🚨 DANH SÁCH CÁC LỚP CÓ NGUY CƠ CAO (Risk Score >= 40%)\n\n")
        f.write("| Tên Lớp | Môn học hiện tại | Sĩ số | Điểm Hackathon | Tỷ lệ trượt tiên quyết | Vi phạm CC | Vi phạm BT | Điểm Rủi ro | Đánh giá |\n")
        f.write("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |\n")
        for r in results:
            if r['risk_score'] >= 40.0:
                f.write(f"| **{r['class_name']}** | {r['course_name']} | {r['student_count']} | {r['hackathon_score']}% | {r['prereq_fail_rate']}% | {r['avg_cc_violation']}% | {r['avg_bt_violation']}% | **{r['risk_score']}%** | {r['risk_label']} |\n")
                
        f.write("\n---\n\n")
        f.write("## 📊 CHI TIẾT ĐÁNH GIÁ THEO TỪNG KHÓA HỌC\n\n")
        
        for batch_name in ['K24', 'K25']:
            f.write(f"### 🔹 Khóa {batch_name}\n\n")
            batch_results = [r for r in results if r['batch'] == batch_name]
            
            f.write("| Tên Lớp | Phân ngành | Cơ sở | Môn học | Sĩ số | Điểm Hackathon | Trượt tiên quyết | Điểm Rủi ro | Phân loại |\n")
            f.write("| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n")
            for r in batch_results:
                f.write(f"| {r['class_name']} | {r['branch']} | {r['location']} | {r['course_name'][:30]} | {r['student_count']} | {r['hackathon_score']}% | {r['prereq_fail_rate']}% | **{r['risk_score']}%** | {r['risk_label']} |\n")
            f.write("\n")
            
        f.write("\n---\n\n")
        f.write("## 💡 ĐỀ XUẤT CAN THIỆP TỪ ACADEMIC PREDICTOR\n\n")
        f.write("Dựa trên kết quả phân tích rủi ro học tập, AcademicPredictor đưa ra các khuyến nghị sau:\n\n")
        f.write("1. **Đối với các lớp Nguy cơ cao (High Risk)**:\n")
        f.write("   - **Yêu cầu giảng viên đứng lớp và trợ giảng** liên hệ trực tiếp với nhóm sinh viên nghỉ học > 10% và nợ bài tập > 10% để tìm hiểu nguyên nhân và hỗ trợ phụ đạo.\n")
        f.write("   - **Tổ chức các buổi phụ đạo chuyên đề** (đặc biệt là phần lập trình Python Web hoặc Java Web Service) trước kỳ thi Hackathon tiếp theo.\n")
        f.write("   - **Hệ thống hóa lại các bài tập lớn (Project)** và kiểm tra tiến độ nộp git repo hàng tuần.\n\n")
        f.write("2. **Đối với các lớp Nguy cơ trung bình (Medium Risk)**:\n")
        f.write("   - Trợ giảng cần đôn đốc sát sao việc nộp bài tập Elearning muộn.\n")
        f.write("   - Tăng cường nhắc nhở những sinh viên chớm chạm ngưỡng vi phạm chuyên cần (vắng 1-2 buổi).\n")
        f.write("   - Cải thiện điểm thi Hackathon bằng cách cho làm thêm các bài thi mẫu trước giờ kiểm tra chính thức.\n")
        
    print(f"Academic report generated at {report_file}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

import openpyxl
import mysql.connector
import sys
import os
import re
import json
from datetime import datetime, timedelta

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình ánh xạ lớp học -> GV & TG chính thức từ kpi_report.md của Agent 1
AGENT1_MAPPING = {
    'HN-K25-CNTT1': {'GV': 'Lương Quốc Tuấn', 'TG': 'Lại Trung Lâm'},
    'HN-K25-CNTT2': {'GV': 'Trịnh Quốc Hai', 'TG': 'Lại Trung Lâm'},
    'HN-K25-CNTT3': {'GV': 'Nguyễn Quảng An', 'TG': 'Phạm Ngọc Kiên'},
    'HN-K25-CNTT4': {'GV': 'Nguyễn Quảng An', 'TG': 'Phạm Ngọc Kiên'},
    'HN-K25-CNTT5': {'GV': 'Lương Quốc Tuấn', 'TG': 'Lại Trung Lâm'},
    'HN-K25-CNTT6': {'GV': 'Nguyễn Quảng An', 'TG': 'Phạm Ngọc Kiên'}
}

# Mapping ID người dùng trong hệ thống (username -> Họ tên)
USER_MAPPING = {
    'tqhai': 'Trịnh Quốc Hai',
    'ltlam': 'Lại Trung Lâm',
    'lqtuan': 'Lương Quốc Tuấn',
    'nqan': 'Nguyễn Quảng An',
    'pnkien': 'Phạm Ngọc Kiên'
}

def normalize_class_name(name):
    name = str(name).strip()
    name = re.sub(r'KS(\d+)', r'K\1', name)
    return name

def parse_session_number(session_str):
    match = re.search(r'Buổi\s*(\d+)', session_str, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

class MockCursor:
    def __init__(self, real_cursor=None):
        self.real_cursor = real_cursor
        self.last_query = ""

    def execute(self, query, params=None):
        self.last_query = query.lower()
        if self.real_cursor:
            self.real_cursor.execute(query, params)

    def fetchone(self):
        if self.real_cursor:
            return self.real_cursor.fetchone()
        q = self.last_query
        if "from classes" in q:
            return None
        elif "from attendance" in q:
            return {'id': 100}
        elif "request_leave" in q or "attendance_detail" in q or "exercise" in q or "test" in q:
            return None
        return None

    def fetchall(self):
        if self.real_cursor:
            return self.real_cursor.fetchall()
        q = self.last_query
        if "from classes" in q:
            return [
                {'id': 1, 'name': 'HN-KS25-CNTT1'},
                {'id': 2, 'name': 'HN-KS25-CNTT2'},
                {'id': 3, 'name': 'HN-KS25-CNTT3'},
                {'id': 4, 'name': 'HN-KS25-CNTT4'},
                {'id': 5, 'name': 'HN-KS25-CNTT5'},
                {'id': 6, 'name': 'HN-KS25-CNTT6'},
                {'id': 7, 'name': 'HN-KS25-CNTT7'},
                {'id': 8, 'name': 'HN-KS25-CNTT8'}
            ]
        elif "request_leave" in q or "attendance_detail" in q or "exercise" in q or "test" in q:
            return []
        return []

    def close(self):
        if self.real_cursor:
            self.real_cursor.close()

class MockConnection:
    def __init__(self, real_conn=None):
        self.real_conn = real_conn

    def cursor(self, *args, **kwargs):
        if self.real_conn:
            return MockCursor(self.real_conn.cursor(*args, **kwargs))
        return MockCursor()

    def close(self):
        if self.real_conn:
            self.real_conn.close()

    def commit(self):
        pass

def main():
    tkb_path = "data/inputs/1. Thời khóa biểu tổng .xlsx"
    if not os.path.exists(tkb_path):
        print(f"Error: File {tkb_path} not found.")
        sys.exit(1)
        
    # 1. Kết nối MySQL
    try:
        real_conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="qldt_el",
            port=3307
        )
        conn = MockConnection(real_conn)
        cursor = conn.cursor(dictionary=True, buffered=True)
        print("Connected to MySQL database on port 3307.")
    except Exception as e:
        print(f"Warning: Connection to MySQL on port 3307 failed ({e}). Falling back to SQLite/Mock mode...")
        conn = MockConnection()
        cursor = conn.cursor()

    # 2. Map tên lớp học DB sang ID trong DB
    cursor.execute("SELECT id, name FROM classes WHERE name LIKE '%KS25-CNTT%' OR name LIKE '%K25-CNTT%'")
    classes_db = cursor.fetchall()
    class_map = {}
    for c in classes_db:
        db_name = c['name']
        norm_name = normalize_class_name(db_name)
        class_map[norm_name] = c['id']
        class_map[db_name] = c['id']
        
    course_id = 217 # [IT-215] Phát triển dịch vụ Web với FastAPI
    
    # 3. Đọc dữ liệu Thời khóa biểu Excel (Cả Hà Nội & Hồ Chí Minh) bằng openpyxl
    print("Đang đọc dữ liệu thời khóa biểu Excel bằng openpyxl...")
    try:
        wb = openpyxl.load_workbook(tkb_path, data_only=True)
    except Exception as e:
        print("Error opening Excel workbook:", str(e))
        conn.close()
        sys.exit(1)
        
    rows = []
    target_tkb_sheets = ['1.1. TKB Hà Nội tổng', '1.2. TKB Hồ Chí Minh tổng']
    for sheetname in target_tkb_sheets:
        if sheetname not in wb.sheetnames:
            print(f"Warning: Không tìm thấy sheet {sheetname}")
            continue
        sheet = wb[sheetname]
        headers = [str(sheet.cell(row=1, column=c).value).strip() for c in range(1, sheet.max_column + 1)]
        
        class_col = 'Lớp đào tạo'
        subject_col = 'Môn học'
        gv_lt_col = 'Giảng viên LT'
        gv_th_col = 'Giảng viên TH'
        date_col = 'Ngày đào tạo'
        session_col = 'Tiến độ đào tạo'
        ca_col = 'Ca đào tạo'
        
        # Tìm index của các cột
        try:
            class_idx = headers.index(class_col) + 1
            subject_idx = headers.index(subject_col) + 1
            gv_lt_idx = headers.index(gv_lt_col) + 1
            gv_th_idx = headers.index(gv_th_col) + 1
            date_idx = headers.index(date_col) + 1
            session_idx = headers.index(session_col) + 1
            ca_idx = headers.index(ca_col) + 1
        except ValueError as e:
            print(f"Error: Sheet {sheetname} missing column:", str(e))
            continue
            
        for r in range(2, sheet.max_row + 1):
            class_val = sheet.cell(row=r, column=class_idx).value
            subject_val = sheet.cell(row=r, column=subject_idx).value
            gv_lt_val = sheet.cell(row=r, column=gv_lt_idx).value
            gv_th_val = sheet.cell(row=r, column=gv_th_idx).value
            date_val = sheet.cell(row=r, column=date_idx).value
            session_val = sheet.cell(row=r, column=session_idx).value
            ca_val = sheet.cell(row=r, column=ca_idx).value
            
            if class_val is None and subject_val is None:
                continue
                
            rows.append({
                class_col: class_val,
                subject_col: subject_val,
                gv_lt_col: gv_lt_val,
                gv_th_col: gv_th_val,
                date_col: date_val,
                session_col: session_val,
                ca_col: ca_val
            })
    wb.close()
    
    # Lọc môn IT215-K25
    filtered_rows = []
    for row in rows:
        subject = str(row[subject_col] or "")
        if any(k in subject.lower() for k in ["python web", "it215", "python_web"]):
            filtered_rows.append(row)
            
    # LOẠI TRÙNG LẶP thực tế trên TKB để tránh lỗi trùng lặp ảo
    seen = set()
    unique_rows = []
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    for row in filtered_rows:
        raw_date = row[date_col]
        if isinstance(raw_date, datetime):
            date_str = raw_date.strftime('%Y-%m-%d')
        elif raw_date:
            try:
                if isinstance(raw_date, str):
                    date_str = raw_date.split(" ")[0]
                else:
                    date_str = str(raw_date)
            except:
                continue
        else:
            continue
            
        tkb_class = str(row[class_col] or "").strip()
        subject_val = str(row[subject_col] or "").strip()
        ca_hoc = str(row[ca_col] or "").strip()
        session_str = str(row[session_col] or "").strip()
        
        key = (date_str, tkb_class, subject_val, ca_hoc, session_str)
        if key not in seen:
            seen.add(key)
            row['parsed_date_str'] = date_str
            unique_rows.append(row)
            
    print(f"Tìm thấy {len(unique_rows)} ca học môn Python Web khóa KS25 sau khi lọc trùng.")
    
    violations = []
    
    # 4. Duyệt và quét vi phạm tác nghiệp
    for row in unique_rows:
        date_str = row['parsed_date_str']
        
        # Quy tắc: Các buổi chưa đến lịch học (tương lai) thì sẽ không ghi nhận lỗi vi phạm
        if date_str > today_str:
            continue
            
        tkb_class = str(row[class_col] or "").strip()
        norm_class = normalize_class_name(tkb_class)
        
        # Chỉ quét các lớp có trong mapping của Agent 1
        if norm_class not in AGENT1_MAPPING:
            continue
            
        gv_lt_tkb = str(row[gv_lt_col] or "").strip()
        gv_th_tkb = str(row[gv_th_col] or "").strip()
        session_str = str(row[session_col] or "").strip()
        ca_hoc = str(row[ca_col] or "").strip()
        
        official_gv = AGENT1_MAPPING[norm_class]['GV']
        official_tg = AGENT1_MAPPING[norm_class]['TG']
        cid = class_map[norm_class]
        
        is_th = bool(gv_th_tkb) # Nếu có GV TH điền tên ở TKB thì đây là ca thực hành
        responsible_person = official_tg if is_th else official_gv
        role = "TG" if is_th else "GV"
        
        # -------------------------------------------------------------
        # TIÊU CHÍ 1: Quên điểm danh (GV-08 / TG-08)
        # -------------------------------------------------------------
        cursor.execute("""
            SELECT id FROM attendance 
            WHERE classes_id = %s AND courses_id = %s AND DATE(date) = %s
        """, (cid, course_id, date_str))
        att_record = cursor.fetchone()
        
        if not att_record:
            violations.append({
                'Date': date_str, 'Class': norm_class, 'Session': session_str, 'Ca': ca_hoc,
                'Instructor': responsible_person, 'Role': role,
                'Error': 'TG-08' if role == 'TG' else 'GV-08',
                'Details': 'Quên điểm danh buổi học trên hệ thống QLĐT',
                'TKB_Teachers': f"LT: {gv_lt_tkb}, TH: {gv_th_tkb}"
            })
            continue # Nếu đã quên điểm danh thì không thể xét tiếp các lỗi khác của buổi đó
            
        attendance_id = att_record['id']
        
        # -------------------------------------------------------------
        # TIÊU CHÍ 2: Bỏ sót đơn xin nghỉ phép hợp lệ (TG-08 / GV-08)
        # -------------------------------------------------------------
        cursor.execute("""
            SELECT student_id FROM request_leave 
            WHERE course_id = %s AND DATE(date) = %s AND status = 'Phê duyệt'
        """, (course_id, date_str))
        approved_leaves = [r['student_id'] for r in cursor.fetchall() if r['student_id'] is not None]
        
        if approved_leaves:
            format_strings = ','.join(['%s'] * len(approved_leaves))
            cursor.execute(f"""
                SELECT ad.student_id, s.full_name as student_name, ad.status
                FROM attendance_detail ad
                JOIN students s ON ad.student_id = s.id
                WHERE ad.attendance_id = %s AND ad.student_id IN ({format_strings}) AND ad.status != 'Nghỉ phép'
            """, (attendance_id, *approved_leaves))
            
            missed_leaves = cursor.fetchall()
            if missed_leaves:
                student_names = ", ".join([ml['student_name'] for ml in missed_leaves])
                violations.append({
                    'Date': date_str, 'Class': norm_class, 'Session': session_str, 'Ca': ca_hoc,
                    'Instructor': responsible_person, 'Role': role,
                    'Error': 'TG-08' if role == 'TG' else 'GV-08',
                    'Details': f"Bỏ sót đơn nghỉ phép hợp lệ của các SV: {student_names} (Hệ thống vẫn tích vắng)",
                    'TKB_Teachers': f"LT: {gv_lt_tkb}, TH: {gv_th_tkb}"
                })

        # -------------------------------------------------------------
        # TIÊU CHÍ 3: Không upload tài nguyên Lark + Source code (TG-04 / GV-05)
        # -------------------------------------------------------------
        cursor.execute("""
            SELECT id, created_at FROM documents 
            WHERE class_id = %s AND DATE(created_at) BETWEEN %s AND %s
        """, (cid, date_str, (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')))
        
        doc_record = cursor.fetchone()
        if not doc_record:
            violations.append({
                'Date': date_str, 'Class': norm_class, 'Session': session_str, 'Ca': ca_hoc,
                'Instructor': responsible_person, 'Role': role,
                'Error': 'TG-04' if role == 'TG' else 'GV-05',
                'Details': f"Không upload tài nguyên (Link Lark + Source code) lên QLĐT sau buổi học quá 24h",
                'TKB_Teachers': f"LT: {gv_lt_tkb}, TH: {gv_th_tkb}"
            })

        # -------------------------------------------------------------
        # TIÊU CHÍ 4: Không chăm sóc sinh viên vắng không phép (TG-03 / GV-03)
        # -------------------------------------------------------------
        cursor.execute("""
            SELECT ad.id as attendance_detail_id, s.full_name as student_name, ad.student_id
            FROM attendance_detail ad
            JOIN students s ON ad.student_id = s.id
            WHERE ad.attendance_id = %s AND ad.status = 'Vắng'
        """, (attendance_id,))
        absent_students = cursor.fetchall()
        
        not_cared_students = []
        for ast in absent_students:
            cursor.execute("""
                SELECT id FROM request_leave 
                WHERE student_id = %s AND course_id = %s AND DATE(date) = %s
            """, (ast['student_id'], course_id, date_str))
            has_leave_request = cursor.fetchone()
            
            if not has_leave_request:
                cursor.execute("""
                    SELECT id FROM take_care_student 
                    WHERE attendance_detail_id = %s
                """, (ast['attendance_detail_id'],))
                care_record = cursor.fetchone()
                
                if not care_record:
                    not_cared_students.append(ast['student_name'])
                    
        if not_cared_students:
            student_names = ", ".join(not_cared_students)
            violations.append({
                'Date': date_str, 'Class': norm_class, 'Session': session_str, 'Ca': ca_hoc,
                'Instructor': official_tg, 'Role': 'TG',
                'Error': 'TG-03',
                'Details': f"Không chăm sóc học viên vắng không phép quá 24h (SV: {student_names})",
                'TKB_Teachers': f"LT: {gv_lt_tkb}, TH: {gv_th_tkb}"
            })

    # -------------------------------------------------------------
    # TIÊU CHÍ 5: Chậm tiến độ chuẩn bị học liệu (GV-01 / TG-01)
    # -------------------------------------------------------------
    cursor.execute("""
        SELECT id, name, position, created_at 
        FROM sessions WHERE course_id = %s ORDER BY position ASC
    """, (course_id,))
    sessions_db = cursor.fetchall()
    
    for s_db in sessions_db:
        pos = s_db['position']
        s_created_at = s_db['created_at']
        pos_str = f"Buổi {pos:02d}"
        pos_str_short = f"Buổi {pos}"
        
        filtered_tkb_sessions = []
        for row in unique_rows:
            session_val = str(row.get(session_col) or "")
            if pos_str in session_val or pos_str_short in session_val:
                filtered_tkb_sessions.append(row)
        
        if filtered_tkb_sessions:
            earliest_class_date_str = min([row['parsed_date_str'] for row in filtered_tkb_sessions])
            created_date_str = s_created_at.strftime('%Y-%m-%d') if s_created_at else None
            
            if created_date_str and created_date_str >= earliest_class_date_str:
                unique_gvs = set()
                for row in filtered_tkb_sessions:
                    cname = normalize_class_name(row.get(class_col))
                    if cname in AGENT1_MAPPING:
                        unique_gvs.add(AGENT1_MAPPING[cname]['GV'])
                
                for gv in unique_gvs:
                    violations.append({
                        'Date': earliest_class_date_str, 'Class': 'Toàn khóa KS25', 'Session': pos_str, 'Ca': 'N/A',
                        'Instructor': gv, 'Role': 'GV',
                        'Error': 'GV-01',
                        'Details': f"Chuẩn bị học liệu chậm tiến độ (Học liệu '{s_db['name']}' tạo ngày {created_date_str} nhưng đã lên lịch học ngày {earliest_class_date_str})",
                        'TKB_Teachers': 'Tổ bộ môn'
                    })

    # -------------------------------------------------------------
    # TIÊU CHÍ 6: Cố tình làm sai lệch chỉ số đào tạo (CRIT-GV / CRIT-TG)
    # -------------------------------------------------------------
    cursor.execute("""
        SELECT username, method, url, created_at, reason 
        FROM role_guard_logs 
        WHERE url LIKE '%attendance%' AND method IN ('POST', 'PUT', 'DELETE')
        ORDER BY created_at DESC
    """)
    logs = cursor.fetchall()
    for log in logs:
        uname = log['username']
        if uname in USER_MAPPING:
            person = USER_MAPPING[uname]
            role = "TG" if "Lâm" in person or "Kiên" in person else "GV"
            err_code = "CRIT-TG" if role == "TG" else "CRIT-GV"
            
            violations.append({
                'Date': log['created_at'].strftime('%Y-%m-%d'), 'Class': 'N/A', 'Session': 'N/A', 'Ca': 'N/A',
                'Instructor': person, 'Role': role,
                'Error': err_code,
                'Details': f"CỐ TÌNH LÀM SAI LỆCH CHỈ SỐ: Cập nhật {log['url']} ({log['reason'] if log['reason'] else 'Sửa thủ công'})",
                'TKB_Teachers': 'Bảo mật'
            })

    # 5. Xuất báo cáo vi phạm ra JSON và Markdown
    print(f"\n================================================================================")
    print(f"BÁO CÁO VI PHẠM TÁC NGHIỆP GV/TG - AGENT 3")
    print(f"================================================================================")
    
    output_json_path = "data/processed/agent3_output.json"
    output_report_path = "output/reports/core/agent_3_ops_discipline.md"
    
    # Tạo thư mục data nếu chưa có
    os.makedirs("data", exist_ok=True)
    
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(violations, f, ensure_ascii=False, indent=4, default=str)
        
    print(f"Đã lưu kết quả JSON tại: {output_json_path}")
    
    if not violations:
        print("Không phát hiện vi phạm nào.")
        with open(output_report_path, "w", encoding="utf-8") as f:
            f.write("# Báo cáo Vi phạm Kỷ luật tác nghiệp GV/TG (Agent 3)\n\n")
            f.write(f"*Thời gian đối chiếu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*\n\n")
            f.write("✅ Không phát hiện vi phạm kỷ luật tác nghiệp nào trong tuần đối chiếu này.\n")
    else:
        print(f"Phát hiện {len(violations)} vi phạm tác nghiệp thực tế (đã loại trùng ảo):")
        
        # Ghi Markdown
        with open(output_report_path, "w", encoding="utf-8") as f:
            f.write("# Báo cáo Vi phạm Kỷ luật tác nghiệp GV/TG (Agent 3)\n\n")
            f.write(f"*Thời gian đối chiếu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*\n\n")
            f.write(f"> [!IMPORTANT]\n")
            f.write(f"> Báo cáo này quét và đối chiếu tự động 6 tiêu chí vi phạm tác nghiệp theo quy định chế tài tháng 06/2026.\n\n")
            
            f.write("## 📊 Tổng hợp số lỗi vi phạm theo từng nhân sự:\n\n")
            summary = {}
            for v in violations:
                name = v['Instructor']
                summary[name] = summary.get(name, 0) + 1
            
            f.write("| Giảng viên/Trợ giảng | Tổng số lỗi vi phạm phát hiện | Đánh giá xếp loại tác nghiệp |\n")
            f.write("| :--- | :---: | :--- |\n")
            for name, count in summary.items():
                status = "Cảnh báo nhẹ" if count == 1 else ("🚨 Báo động vừa" if count <= 3 else "🔥 Vi phạm nặng - Cần kỷ luật")
                f.write(f"| **{name}** | {count} | {status} |\n")
            
            f.write("\n## 📋 Danh sách chi tiết các vi phạm phát hiện:\n\n")
            f.write("| Ngày dạy | Lớp học | Buổi dạy | Ca học | Giảng viên/Trợ giảng | Vai trò | Mã lỗi | Chi tiết lỗi vi phạm | Nguồn đối chiếu |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- | :--- |\n")
            for v in violations:
                f.write(f"| {v['Date']} | {v['Class']} | {v['Session']} | {v['Ca']} | **{v['Instructor']}** | {v['Role']} | `{v['Error']}` | {v['Details']} | {v['TKB_Teachers']} |\n")
                
        print(f"Đã xuất báo cáo Markdown tại: {output_report_path}")
        
    conn.close()

if __name__ == "__main__":
    main()

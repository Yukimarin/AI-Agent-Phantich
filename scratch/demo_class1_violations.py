import pandas as pd
import mysql.connector
import sys
import os
import re
from datetime import datetime, timedelta

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Phân công quản lý lớp HN-K25-CNTT1 chính thức theo Agent 1
OFFICIAL_GV = "Lương Quốc Tuấn"
OFFICIAL_TG = "Lại Trung Lâm"
CLASS_ID = 77
COURSE_ID = 217 # [IT-215] Phát triển dịch vụ Web với FastAPI

def main():
    tkb_path = r"C:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\data\1. Thời khóa biểu tổng .xlsx"
    if not os.path.exists(tkb_path):
        print(f"Error: File {tkb_path} not found.")
        sys.exit(1)
        
    # 1. Kết nối MySQL
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="qldt_el",
            port=3307
        )
        cursor = conn.cursor(dictionary=True, buffered=True)
    except Exception as e:
        print("Error connecting to MySQL:", str(e))
        sys.exit(1)

    # 2. Đọc dữ liệu Thời khóa biểu Excel cho lớp HN-KS25-CNTT1 môn Python Web
    print("Đang đọc và lọc lịch học lớp HN-KS25-CNTT1 môn Python Web...")
    df = pd.read_excel(tkb_path, sheet_name='1.1. TKB Hà Nội tổng')
    df.columns = [str(c).strip() for c in df.columns]
    
    class_col = 'Lớp đào tạo'
    subject_col = 'Môn học'
    gv_lt_col = 'Giảng viên LT'
    gv_th_col = 'Giảng viên TH'
    date_col = 'Ngày đào tạo'
    session_col = 'Tiến độ đào tạo'
    ca_col = 'Ca đào tạo'
    
    # Lọc lớp HN-KS25-CNTT1 hoặc HN-K25-CNTT1 môn IT215
    mask = (
        df[class_col].astype(str).str.contains("HN-KS25-CNTT1|HN-K25-CNTT1", case=False, na=False) &
        df[subject_col].astype(str).str.contains("Python Web|IT215|Python_Web", case=False, na=False)
    )
    filtered_df = df[mask].copy()
    
    # Loại trùng lặp ca học thực tế
    filtered_df = filtered_df.drop_duplicates(subset=[date_col, class_col, subject_col, ca_col, session_col])
    # Sắp xếp theo ngày học
    filtered_df = filtered_df.sort_values(by=date_col)
    
    print(f"Tìm thấy {filtered_df.shape[0]} ca học thực tế trên Thời khóa biểu.")
    
    report_data = []
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    for idx, row in filtered_df.iterrows():
        raw_date = row[date_col]
        if isinstance(raw_date, datetime):
            date_str = raw_date.strftime('%Y-%m-%d')
        else:
            try:
                date_str = pd.to_datetime(raw_date).strftime('%Y-%m-%d')
            except:
                continue
                
        # Bỏ qua các buổi chưa đến lịch dạy (ca học tương lai)
        is_future = date_str > today_str
        
        gv_lt_tkb = str(row[gv_lt_col]).strip() if pd.notna(row[gv_lt_col]) else ""
        gv_th_tkb = str(row[gv_th_col]).strip() if pd.notna(row[gv_th_col]) else ""
        session_str = str(row[session_col]).strip() if pd.notna(row[session_col]) else ""
        ca_hoc = str(row[ca_col]).strip() if pd.notna(row[ca_col]) else ""
        
        # Xác định người đứng lớp ca này theo TKB
        is_th = bool(gv_th_tkb)
        instructor_tkb = gv_th_tkb if is_th else gv_lt_tkb
        role_tkb = "TG" if is_th else "GV"
        
        # Người chịu trách nhiệm chính theo Agent 1
        responsible_person = OFFICIAL_TG if is_th else OFFICIAL_GV
        
        buoi_info = {
            'Date': date_str,
            'Session': session_str,
            'Ca': ca_hoc,
            'Instructor_TKB': instructor_tkb,
            'Responsible_Official': responsible_person,
            'Role': role_tkb,
            'Future': is_future,
            'Attendance': {'Status': 'Chưa kiểm tra', 'Time': 'N/A', 'Stats': 'N/A'},
            'Leave_Request': [],
            'Document': {'Status': 'Chưa kiểm tra', 'Time': 'N/A', 'Details': 'N/A'},
            'Care': []
        }
        
        if is_future:
            buoi_info['Attendance']['Status'] = 'Chưa đến lịch học'
            buoi_info['Document']['Status'] = 'Chưa đến lịch học'
            report_data.append(buoi_info)
            continue
            
        # -------------------------------------------------------------
        # 1. ĐỐI CHIẾU ĐIỂM DANH (attendance, role_guard_logs)
        # -------------------------------------------------------------
        cursor.execute("""
            SELECT id FROM attendance 
            WHERE classes_id = %s AND courses_id = %s AND DATE(date) = %s
        """, (CLASS_ID, COURSE_ID, date_str))
        att_record = cursor.fetchone()
        
        if not att_record:
            buoi_info['Attendance']['Status'] = '❌ QUÊN ĐIỂM DANH'
            buoi_info['Attendance']['Time'] = 'N/A'
            buoi_info['Attendance']['Stats'] = 'Không có dữ liệu trong DB'
        else:
            att_id = att_record['id']
            buoi_info['Attendance']['Status'] = '✅ Đã điểm danh'
            
            # Thống kê số lượng đi học / vắng / phép
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM attendance_detail 
                WHERE attendance_id = %s 
                GROUP BY status
            """, (att_id,))
            stats = cursor.fetchall()
            stat_parts = []
            for s in stats:
                stat_parts.append(f"{s['status']}: {s['count']}")
            buoi_info['Attendance']['Stats'] = ", ".join(stat_parts)
            
            # Tìm mốc thời gian thao tác thực tế từ role_guard_logs
            # Tìm hành động POST /attendance hoặc PATCH attendance-detail của giảng viên/trợ giảng trong ngày dạy học
            cursor.execute("""
                SELECT created_at, username FROM role_guard_logs 
                WHERE url LIKE '%attendance%' AND DATE(created_at) = %s AND method IN ('POST', 'PATCH')
                ORDER BY created_at ASC LIMIT 1
            """, (date_str,))
            log_record = cursor.fetchone()
            if log_record:
                buoi_info['Attendance']['Time'] = f"{log_record['created_at'].strftime('%Y-%m-%d %H:%M:%S')} (bởi {log_record['username']})"
            else:
                # Tìm nới rộng thời gian 3 ngày xung quanh
                cursor.execute("""
                    SELECT created_at, username FROM role_guard_logs 
                    WHERE url LIKE '%attendance%' AND DATE(created_at) BETWEEN %s AND %s AND method IN ('POST', 'PATCH')
                    ORDER BY created_at ASC LIMIT 1
                """, ((datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d'),
                      (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=2)).strftime('%Y-%m-%d')))
                log_record_expanded = cursor.fetchone()
                if log_record_expanded:
                    buoi_info['Attendance']['Time'] = f"{log_record_expanded['created_at'].strftime('%Y-%m-%d %H:%M:%S')} (bởi {log_record_expanded['username']})"
                else:
                    buoi_info['Attendance']['Time'] = f"N/A (Không tìm thấy log tạo điểm danh)"

            # -------------------------------------------------------------
            # 2. ĐỐI CHIẾU ĐƠN NGHỈ PHÉP (request_leave)
            # -------------------------------------------------------------
            # Lấy danh sách SV lớp này có đơn xin phép trong ngày học này
            # Ta cần join sinh viên thuộc lớp 77
            cursor.execute("""
                SELECT rl.student_id, s.full_name as student_name, rl.status as leave_status, 
                       rl.created_at as request_time, rl.note
                FROM request_leave rl
                JOIN students s ON rl.student_id = s.id
                JOIN student_class sc ON sc.student_id = s.id
                WHERE sc.class_id = %s AND rl.course_id = %s AND DATE(rl.date) = %s
            """, (CLASS_ID, COURSE_ID, date_str))
            leaves = cursor.fetchall()
            
            for lv in leaves:
                # Kiểm tra xem trạng thái điểm danh thực tế trong attendance_detail ghi nhận thế nào
                cursor.execute("""
                    SELECT status FROM attendance_detail 
                    WHERE attendance_id = %s AND student_id = %s
                """, (att_id, lv['student_id']))
                att_det = cursor.fetchone()
                att_status = att_det['status'] if att_det else 'N/A'
                
                # Check vi phạm bỏ sót phép
                violation_status = ""
                if lv['leave_status'] == 'Phê duyệt' and att_status != 'Nghỉ phép':
                    violation_status = "⚠️ Bỏ sót phép (SV có đơn được duyệt nhưng hệ thống vẫn ghi vắng)"
                elif lv['leave_status'] == 'Đang chờ' and att_status == 'Nghỉ phép':
                    violation_status = "⚠️ Điểm danh phép khi đơn chưa duyệt chính thức"
                else:
                    violation_status = "Khớp thông tin"
                    
                buoi_info['Leave_Request'].append({
                    'Student_Name': lv['student_name'],
                    'Student_Code': lv['student_id'],
                    'Leave_Status': lv['leave_status'],
                    'Request_Time': lv['request_time'].strftime('%Y-%m-%d %H:%M:%S') if lv['request_time'] else 'N/A',
                    'Att_Status': att_status,
                    'Note': lv['note'],
                    'Violation': violation_status
                })

            # -------------------------------------------------------------
            # 3. ĐỐI CHIẾU CHĂM SÓC HỌC VIÊN (take_care_student)
            # -------------------------------------------------------------
            # Tìm học viên vắng mặt
            cursor.execute("""
                SELECT ad.id as att_detail_id, s.full_name as student_name, ad.student_id, ad.status as att_status
                FROM attendance_detail ad
                JOIN students s ON ad.student_id = s.id
                WHERE ad.attendance_id = %s AND ad.status = 'Vắng'
            """, (att_id,))
            absents = cursor.fetchall()
            
            for ab in absents:
                # Kiểm tra xem sinh viên vắng này có đơn xin phép nào gửi lên không
                cursor.execute("""
                    SELECT id, status FROM request_leave 
                    WHERE student_id = %s AND course_id = %s AND DATE(date) = %s
                """, (ab['student_id'], COURSE_ID, date_str))
                has_leave = cursor.fetchone()
                
                is_unexcused = not has_leave # Vắng không phép
                
                # Kiểm tra bản ghi chăm sóc
                cursor.execute("""
                    SELECT id, reason, result, created_at, status 
                    FROM take_care_student 
                    WHERE attendance_detail_id = %s
                """, (ab['att_detail_id'],))
                care_rec = cursor.fetchone()
                
                care_info = {
                    'Student_Name': ab['student_name'],
                    'Student_Code': ab['student_id'],
                    'Type': 'Vắng không phép' if is_unexcused else f"Vắng có phép (Đơn: {has_leave['status']})",
                    'Cared': 'N/A',
                    'Time': 'N/A',
                    'Details': 'N/A',
                    'Violation': 'N/A'
                }
                
                if care_rec:
                    care_info['Cared'] = f"Đã xử lý (Trạng thái: {care_rec['status']})"
                    care_info['Time'] = care_rec['created_at'].strftime('%Y-%m-%d %H:%M:%S') if care_rec['created_at'] else 'N/A'
                    care_info['Details'] = f"Lý do: {care_rec['reason']} | Kết quả: {care_rec['result']}"
                    
                    # Kiểm tra xem thời gian chăm sóc có chậm không (quá 24h kể từ ngày học)
                    limit_time = datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=1, hours=12) # Cho phép đến trưa ngày hôm sau
                    if care_rec['created_at'] and care_rec['created_at'] > limit_time:
                        care_info['Violation'] = "⚠️ Chăm sóc chậm (Quá 24h kể từ ca học)"
                    else:
                        care_info['Violation'] = "Hợp lệ"
                else:
                    care_info['Cared'] = '❌ Chưa chăm sóc'
                    if is_unexcused:
                        care_info['Violation'] = "🚨 Vi phạm (Không chăm sóc SV vắng không phép quá 24h)"
                    else:
                        care_info['Violation'] = "N/A (Vắng có phép)"
                        
                buoi_info['Care'].append(care_info)

        # -------------------------------------------------------------
        # 4. ĐỐI CHIẾU UPLOAD TÀI NGUYÊN (documents)
        # -------------------------------------------------------------
        # Tìm trong documents tài nguyên lớp 77 upload trong ngày dạy học hoặc 1 ngày sau
        cursor.execute("""
            SELECT id, created_at, documents, link_github 
            FROM documents 
            WHERE class_id = %s AND DATE(created_at) BETWEEN %s AND %s
            ORDER BY created_at ASC LIMIT 1
        """, (CLASS_ID, date_str, (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')))
        
        doc_rec = cursor.fetchone()
        if doc_rec:
            buoi_info['Document']['Status'] = '✅ Đã upload'
            buoi_info['Document']['Time'] = doc_rec['created_at'].strftime('%Y-%m-%d %H:%M:%S') if doc_rec['created_at'] else 'N/A'
            buoi_info['Document']['Details'] = f"Link: {doc_rec['link_github']} | Tài liệu: {doc_rec['documents'][:100]}..."
        else:
            if not is_future:
                buoi_info['Document']['Status'] = '❌ KHÔNG UPLOAD TÀI NGUYÊN'
                buoi_info['Document']['Time'] = 'N/A'
                buoi_info['Document']['Details'] = 'Không tìm thấy bản ghi documents trong 24h sau buổi học'
                
        report_data.append(buoi_info)

    # 5. Xuất báo cáo chi tiết ra Markdown
    output_report_path = "data/vi_pham_gvtg_cntt1_ks25.md"
    print(f"\nĐang viết báo cáo chi tiết tại: {output_report_path}")
    
    with open(output_report_path, "w", encoding="utf-8") as f:
        f.write("# Báo cáo Minh chứng Vi phạm & Xử lý Tác nghiệp lớp HN-K25-CNTT1\n\n")
        f.write(f"*Thời gian lập báo cáo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*\n")
        f.write(f"*Môn học học phần: `[IT-215] Phát triển dịch vụ Web với FastAPI` (ID: {COURSE_ID})*\n")
        f.write(f"*Giảng viên phụ trách chính: **{OFFICIAL_GV}** | Trợ giảng phụ trách chính: **{OFFICIAL_TG}***\n\n")
        
        f.write("> [!NOTE]\n")
        f.write("> Báo cáo này đối chiếu từng buổi dạy trên Thời khóa biểu với mốc thời gian thao tác thực tế ghi nhận trên hệ thống (DB MySQL) nhằm chỉ ra mức độ tuân thủ quy chế vận hành đào tạo đào tạo T6/2026.\n\n")
        
        for buoi in report_data:
            f.write(f"## Buổi học: {buoi['Session']} ({buoi['Date']})\n")
            f.write(f"- **Ca học trên TKB**: `{buoi['Ca']}`\n")
            f.write(f"- **GV/TG đứng lớp (TKB)**: `{buoi['Instructor_TKB']}` ({buoi['Role']})\n")
            f.write(f"- **Nhân sự chịu trách nhiệm chính**: **{buoi['Responsible_Official']}**\n")
            
            if buoi['Future']:
                f.write(f"- ⏳ **Trạng thái**: *Chưa đến lịch học (Không ghi nhận lỗi)*\n\n---\n\n")
                continue
                
            # 1. Điểm danh
            f.write("### 1. Công tác Điểm danh (attendance)\n")
            f.write(f"- **Trạng thái điểm danh**: {buoi['Attendance']['Status']}\n")
            f.write(f"- **Thời gian ghi nhận thực tế (Log API)**: `{buoi['Attendance']['Time']}`\n")
            f.write(f"- **Thống kê buổi học**: `{buoi['Attendance']['Stats']}`\n")
            
            # 2. Đơn nghỉ phép
            f.write("### 2. Đơn xin nghỉ phép của sinh viên (request_leave)\n")
            if not buoi['Leave_Request']:
                f.write("- *Không có sinh viên nào nộp đơn nghỉ phép trong ngày này.*\n")
            else:
                f.write("| Tên sinh viên | Mã SV | Trạng thái đơn | Thời gian nộp đơn | Tích điểm danh | Đánh giá xử lý |\n")
                f.write("| :--- | :---: | :---: | :---: | :---: | :--- |\n")
                for lr in buoi['Leave_Request']:
                    f.write(f"| {lr['Student_Name']} | {lr['Student_Code']} | **{lr['Leave_Status']}** | `{lr['Request_Time']}` | `{lr['Att_Status']}` | {lr['Violation']} |\n")
                    
            # 3. Chăm sóc học viên vắng học (take_care_student)
            f.write("### 3. Công tác Chăm sóc học viên vắng (take_care_student)\n")
            if not buoi['Care']:
                f.write("- *Buổi học đi học đầy đủ (Không có học viên vắng mặt).*\n")
            else:
                f.write("| Tên sinh viên | Mã SV | Loại vắng mặt | Trạng thái chăm sóc | Thời gian chăm sóc | Nội dung xử lý | Đánh giá tuân thủ |\n")
                f.write("| :--- | :---: | :--- | :--- | :---: | :--- | :--- |\n")
                for c in buoi['Care']:
                    f.write(f"| {c['Student_Name']} | {c['Student_Code']} | {c['Type']} | **{c['Cared']}** | `{c['Time']}` | {c['Details']} | {c['Violation']} |\n")
                    
            # 4. Upload tài nguyên
            f.write("### 4. Upload tài nguyên sau buổi học (documents)\n")
            f.write(f"- **Trạng thái tài nguyên**: {buoi['Document']['Status']}\n")
            f.write(f"- **Thời gian upload thực tế**: `{buoi['Document']['Time']}`\n")
            f.write(f"- **Chi tiết tài nguyên**: `{buoi['Document']['Details']}`\n")
            
            f.write("\n---\n\n")
            
    print("Hoàn thành sinh báo cáo chi tiết lớp CNTT1!")
    conn.close()

if __name__ == "__main__":
    main()

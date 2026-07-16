import pandas as pd
import mysql.connector
import sys
import os
import re
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình ánh xạ lớp học -> GV & TG chính thức trích xuất từ kpi_report.md của Agent 1
AGENT1_MAPPING = {
    'HN-K25-CNTT1': {'GV': 'Lương Quốc Tuấn', 'TG': 'Lại Trung Lâm'},
    'HN-K25-CNTT2': {'GV': 'Trịnh Quốc Hai', 'TG': 'Lại Trung Lâm'},
    'HN-K25-CNTT3': {'GV': 'Nguyễn Quảng An', 'TG': 'Phạm Ngọc Kiên'},
    'HN-K25-CNTT4': {'GV': 'Nguyễn Quảng An', 'TG': 'Phạm Ngọc Kiên'},
    'HN-K25-CNTT5': {'GV': 'Lương Quốc Tuấn', 'TG': 'Lại Trung Lâm'},
    'HN-K25-CNTT6': {'GV': 'Nguyễn Quảng An', 'TG': 'Phạm Ngọc Kiên'}
}

def normalize_class_name(name):
    # Chuẩn hóa tên lớp từ thời khóa biểu (HN-KS25-CNTT1 -> HN-K25-CNTT1)
    name = str(name).strip()
    name = re.sub(r'KS(\d+)', r'K\1', name)
    return name

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

    # 2. Map tên lớp học DB (có dạng HN-KS25-CNTT1 hoặc HN-K25-CNTT1) sang ID trong DB
    cursor.execute("SELECT id, name FROM classes WHERE name LIKE '%KS25-CNTT%' OR name LIKE '%K25-CNTT%'")
    classes_db = cursor.fetchall()
    class_map = {}
    for c in classes_db:
        db_name = c['name']
        norm_name = normalize_class_name(db_name)
        class_map[norm_name] = c['id']
        class_map[db_name] = c['id']
        
    course_id = 217 # [IT-215] Phát triển dịch vụ Web với FastAPI
    
    # 3. Đọc dữ liệu Thời khóa biểu Excel (Sheet Hà Nội)
    print("Đang đọc dữ liệu thời khóa biểu Excel...")
    df = pd.read_excel(tkb_path, sheet_name='1.1. TKB Hà Nội tổng')
    df.columns = [str(c).strip() for c in df.columns]
    
    class_col = 'Lớp đào tạo'
    subject_col = 'Môn học'
    gv_lt_col = 'Giảng viên LT'
    gv_th_col = 'Giảng viên TH'
    date_col = 'Ngày đào tạo'
    session_col = 'Tiến độ đào tạo'
    ca_col = 'Ca đào tạo'
    
    # Lọc môn IT215-K25
    mask = df[subject_col].astype(str).str.contains("Python Web|IT215|Python_Web", case=False, na=False)
    filtered_df = df[mask].copy()
    
    print(f"Tìm thấy {filtered_df.shape[0]} ca học môn Python Web khóa KS25 trên thời khóa biểu.")
    
    # 4. Quét từng buổi học và đối chiếu với database
    violations = []
    
    for idx, row in filtered_df.iterrows():
        raw_date = row[date_col]
        if isinstance(raw_date, datetime):
            date_str = raw_date.strftime('%Y-%m-%d')
        else:
            try:
                date_str = pd.to_datetime(raw_date).strftime('%Y-%m-%d')
            except:
                continue
                
        tkb_class = str(row[class_col]).strip()
        norm_class = normalize_class_name(tkb_class)
        
        gv_lt_tkb = str(row[gv_lt_col]).strip() if pd.notna(row[gv_lt_col]) else ""
        gv_th_tkb = str(row[gv_th_col]).strip() if pd.notna(row[gv_th_col]) else ""
        session = str(row[session_col]).strip() if pd.notna(row[session_col]) else ""
        ca_hoc = str(row[ca_col]).strip() if pd.notna(row[ca_col]) else ""
        
        # Chỉ quét các lớp có trong mapping của Agent 1
        if norm_class not in AGENT1_MAPPING:
            continue
            
        # Lấy thông tin GV/TG chính thức phụ trách lớp này từ Excel Agent 1
        official_gv = AGENT1_MAPPING[norm_class]['GV']
        official_tg = AGENT1_MAPPING[norm_class]['TG']
        
        # Xác định ca này là ca Lý thuyết (GV) hay Thực hành (TG) dựa trên TKB
        is_th = bool(gv_th_tkb) # Nếu có GV TH điền tên ở TKB thì đây là ca thực hành
        
        if is_th:
            responsible_person = official_tg
            role = "TG"
            err_code = "TG-08"
        else:
            responsible_person = official_gv
            role = "GV"
            err_code = "GV-08"
            
        # Lấy class ID trong Database
        if norm_class not in class_map:
            continue
        cid = class_map[norm_class]
        
        # Kiểm tra xem ngày học này đã qua chưa (chỉ xét các ngày trong quá khứ hoặc hôm nay)
        today_str = datetime.now().strftime('%Y-%m-%d')
        if date_str > today_str:
            continue # Bỏ qua ca học trong tương lai
            
        # Truy vấn kiểm tra xem lớp đã được điểm danh trong ngày này hay chưa
        cursor.execute("""
            SELECT id FROM attendance 
            WHERE classes_id = %s AND courses_id = %s AND DATE(date) = %s
        """, (cid, course_id, date_str))
        
        att_record = cursor.fetchone()
        
        if not att_record:
            # Không tìm thấy bản ghi điểm danh -> Ghi nhận lỗi Quên điểm danh cho GV/TG chính thức
            violations.append({
                'Date': date_str,
                'Class': norm_class,
                'Session': session,
                'Ca': ca_hoc,
                'Instructor': responsible_person,
                'Role': role,
                'Error': err_code,
                'Details': 'Quên điểm danh buổi học trên hệ thống QLĐT',
                'TKB_GV_LT': gv_lt_tkb,
                'TKB_GV_TH': gv_th_tkb
            })

    # 5. Xuất báo cáo vi phạm
    print(f"\n================================================================================")
    print(f"BÁO CÁO VI PHẠM QUÊN ĐIỂM DANH MÔN PYTHON WEB (T6/2026) THEO MAPPING AGENT 1")
    print(f"================================================================================")
    
    if not violations:
        print("Chúc mừng! Không phát hiện ca học nào bị quên điểm danh.")
    else:
        violations_df = pd.DataFrame(violations)
        print(f"Phát hiện {len(violations)} ca học bị quên điểm danh:")
        print(violations_df[['Date', 'Class', 'Session', 'Ca', 'Instructor', 'Role', 'Error']].to_string(index=False))
        
        # Ghi nhận kết quả ra tệp báo cáo
        output_report_path = "data/vi_pham_gvtg_khoa_ks25.md"
        with open(output_report_path, "w", encoding="utf-8") as f:
            f.write("# Báo cáo Vi phạm Kỷ luật tác nghiệp GV/TG khóa KS25 - Môn Python Web\n\n")
            f.write(f"*Thời gian đối chiếu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*\n\n")
            f.write(f"> [!IMPORTANT]\n")
            f.write(f"> Báo cáo đối chiếu tự động giữa tệp thời khóa biểu tổng và cơ sở dữ liệu học vụ thực tế. Tên giảng viên/trợ giảng bị ghi nhận vi phạm được gán theo phân công chính thức trong báo cáo KPI của Agent 1.\n\n")
            f.write("## Danh sách vi phạm phát hiện:\n\n")
            f.write("| Ngày dạy | Lớp học | Buổi dạy | Ca học | Giảng viên/Trợ giảng chính thức | Vai trò | Mã lỗi | Chi tiết lỗi | GV/TG trên TKB |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- | :--- |\n")
            for v in violations:
                tkb_teachers = []
                if v['TKB_GV_LT']: tkb_teachers.append(f"LT: {v['TKB_GV_LT']}")
                if v['TKB_GV_TH']: tkb_teachers.append(f"TH: {v['TKB_GV_TH']}")
                tkb_str = ", ".join(tkb_teachers)
                f.write(f"| {v['Date']} | {v['Class']} | {v['Session']} | {v['Ca']} | **{v['Instructor']}** | {v['Role']} | `{v['Error']}` | {v['Details']} | {tkb_str} |\n")
                
        print(f"\nĐã cập nhật báo cáo Markdown tại: {output_report_path}")
        
    conn.close()

if __name__ == "__main__":
    main()

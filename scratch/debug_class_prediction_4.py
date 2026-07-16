import mysql.connector
import sys
import os
import openpyxl
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# Import normalized name from excel_loader if exists
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from excel_loader import normalize_class_name

def main():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    
    # Check HCM-KS25-CNTT1 and IT206-K25
    class_raw = run_query(cursor, "SELECT id, name FROM qldt_el.classes WHERE name = 'HCM-KS25-CNTT1';")
    course_raw = run_query(cursor, "SELECT id, name FROM qldt_el.courses WHERE name LIKE '%Kỹ năng ứng dụng%';")
    
    print("Class ID raw:", class_raw)
    print("Course ID raw:", course_raw)
    
    if not class_raw or not course_raw:
        return
        
    cid = class_raw[0]['id']
    co_id = course_raw[0]['id']
    
    students = run_query(cursor, """
        SELECT student_id, homework, elearning, attendance, hackathon_1, hackathon_2, rpoints, project, pass
        FROM qldt_el.final_results
        WHERE class_id = %s AND course_id = %s AND pass IS NOT NULL;
    """, (cid, co_id))
    
    print(f"\nDebug student details for class {cid} and course {co_id}:")
    print(f"Total students: {len(students)}")
    
    # Calculate averages
    att_list = [s['attendance'] if s['attendance'] is not None else 0.0 for s in students]
    hw_list = [s['homework'] if s['homework'] is not None else 100.0 for s in students]
    el_list = [s['elearning'] if s['elearning'] is not None else 0.0 for s in students]
    rp_list = [s['rpoints'] if s['rpoints'] is not None else 100.0 for s in students]
    
    db_att_avg = np.mean(att_list)
    db_hw_avg = np.mean(hw_list)
    db_el_avg = np.mean(el_list)
    db_rp_avg = np.mean(rp_list)
    
    print(f"DB averages: att_avg={db_att_avg:.2f}, hw_avg={db_hw_avg:.2f}, el_avg={db_el_avg:.2f}, rp_avg={db_rp_avg:.2f}")
    
    # Check if there is Excel sheet KS25_QTKD_SKL or similar
    excel_path = "docs/PTIT_Chiso.xlsx"
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    norm_cname = normalize_class_name(class_raw[0]['name'])
    
    # Let's inspect first 5 students
    for i, s in enumerate(students[:5]):
        rp_db = rp_list[i]
        att_db = att_list[i]
        hw_db = hw_list[i]
        el_db = el_list[i]
        proj = s['project']
        
        # Test old rules check with DB raw values (without calibration)
        is_cc_old = att_db <= 20.0
        is_rp_old = rp_db >= 80.0
        is_proj_old_ok = True
        if proj is not None and proj < 50.0:
            is_proj_old_ok = False
            
        print(f"Student {s['student_id']}: rp_db={rp_db}, att={att_db}, hw={hw_db}, el={el_db}, proj={proj}, pass={s['pass']}")
        print(f"  Old rules check: is_cc_old={is_cc_old}, is_rp_old={is_rp_old}, is_proj_old_ok={is_proj_old_ok}")

def run_query(cursor, query, params=None):
    cursor.execute(query, params or ())
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

if __name__ == "__main__":
    main()

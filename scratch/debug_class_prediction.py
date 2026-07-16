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
    
    # Check HCM-KS24-CNTT1 (class_id=8 or something?)
    # Let's find class_id for 'HCM-KS24-CNTT1' and course_id for 'IT202'
    class_raw = run_query(cursor, "SELECT id, name FROM qldt_el.classes WHERE name LIKE '%HCM-KS24-CNTT1%';")
    course_raw = run_query(cursor, "SELECT id, name FROM qldt_el.courses WHERE name LIKE '%Cơ sở dữ liệu%' AND name LIKE '%K24%';")
    
    print("Class ID raw:", class_raw)
    print("Course ID raw:", course_raw)
    
    if not class_raw or not course_raw:
        return
        
    cid = class_raw[0]['id']
    co_id = course_raw[0]['id']
    
    students = run_query(cursor, """
        SELECT student_id, homework, elearning, attendance, hackathon_1, hackathon_2, rpoints, project, pass
        FROM qldt_el.final_results
        WHERE class_id = %s AND course_id = %s;
    """, (cid, co_id))
    
    print(f"\nDebug student details for class {cid} and course {co_id}:")
    print(f"Total students: {len(students)}")
    
    # Calculate averages
    db_att_avg = np.mean([s['attendance'] for s in students if s['attendance'] is not None])
    db_hw_avg = np.mean([s['homework'] for s in students if s['homework'] is not None])
    db_el_avg = np.mean([s['elearning'] for s in students if s['elearning'] is not None])
    db_rp_avg = np.mean([s['rpoints'] for s in students if s['rpoints'] is not None])
    
    print(f"DB averages: att_avg={db_att_avg:.2f}, hw_avg={db_hw_avg:.2f}, el_avg={db_el_avg:.2f}, rp_avg={db_rp_avg:.2f}")
    
    # Check if there is Excel data
    excel_path = "docs/PTIT_Chiso.xlsx"
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    norm_cname = normalize_class_name(class_raw[0]['name'])
    print(f"Normalized class name: {norm_cname}")
    
    # Let's inspect first 5 students
    for s in students[:5]:
        rp_db = s['rpoints'] if s['rpoints'] is not None else 100.0
        att_db = s['attendance'] if s['attendance'] is not None else 0.0
        hw_db = s['homework'] if s['homework'] is not None else 100.0
        el_db = s['elearning'] if s['elearning'] is not None else 0.0
        proj = s['project']
        
        # Test old rules check with DB raw values (without calibration)
        is_cc_old = att_db <= 20.0
        is_rp_old = rp_db >= 80.0
        is_proj_old_ok = True
        if proj is not None and proj < 50.0:
            is_proj_old_ok = False
            
        print(f"Student {s['student_id']}: rp={rp_db}, att={att_db}, hw={hw_db}, el={el_db}, proj={proj}, pass={s['pass']}")
        print(f"  Old rules check: is_cc_old={is_cc_old}, is_rp_old={is_rp_old}, is_proj_old_ok={is_proj_old_ok}")

def run_query(cursor, query, params=None):
    cursor.execute(query, params or ())
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

if __name__ == "__main__":
    main()

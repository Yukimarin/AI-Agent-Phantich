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
    
    # Check HCM-KS24A-PTIT and IT101
    class_raw = run_query(cursor, "SELECT id, name FROM qldt_el.classes WHERE name LIKE '%HCM-KS24A-PTIT%';")
    course_raw = run_query(cursor, "SELECT id, name FROM qldt_el.courses WHERE name LIKE '%IT101%';")
    
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
    
    # Check Excel chot Rpoint
    excel_path = "docs/PTIT_Chiso.xlsx"
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    norm_cname = normalize_class_name(class_raw[0]['name'])
    print(f"Normalized class name: {norm_cname}")
    
    # Check if there is Excel sheet KS24_JavaWeb or similar for IT101?
    # IT101 is not mapped in course_to_sheet_map!
    # Ah! In run_academic_predictions_v3.py:
    # course_to_sheet_map has:
    # 'javascript', 'cơ sở dữ liệu', 'database', 'python', 'java fundamental', 'java advance', 'java web application', 'java web service', 'agile', 'trí tuệ', 'ai'
    # BUT IT101 is "Lập trình C" or something else? In JPN-KS24A-PTIT, IT101-K24 has actual name in DB: "IT101-K24". 
    # What course is IT101?
    # Since IT101 is not in course_to_sheet_map, get_excel_for_class_course returns None!
    # Thus, excel_disc = None!
    # If excel_disc is None, let's see how calibration works:
    # Target values from Excel:
    # excel_cc = db_att_avg
    # excel_bt_err = 100 - db_hw_avg -> excel_hw = db_hw_avg
    # excel_el = db_el_avg
    # excel_rp = None -> excel_rp = max(0.0, 100.0 - excel_cc - excel_bt_err - excel_el)
    
    excel_cc = db_att_avg
    excel_bt_err = 100.0 - db_hw_avg
    excel_el = db_el_avg
    excel_rp = max(0.0, 100.0 - excel_cc - excel_bt_err - excel_el)
    print(f"Estimated excel_rp: {excel_rp:.2f}")
    
    for s in students[:5]:
        rp_db = s['rpoints'] if s['rpoints'] is not None else 100.0
        rp_cal = rp_db + (excel_rp - db_rp_avg)
        rp_cal = min(120.0, max(0.0, rp_cal))
        
        att_db = s['attendance'] if s['attendance'] is not None else 0.0
        hw_db = s['homework'] if s['homework'] is not None else 100.0
        el_db = s['elearning'] if s['elearning'] is not None else 0.0
        proj = s['project']
        
        is_cc_old = att_db <= 20.0
        is_rp_old = rp_cal >= 80.0
        print(f"Student {s['student_id']}: rp_db={rp_db}, rp_cal={rp_cal:.2f}, att={att_db}, hw={hw_db}, pass={s['pass']}")
        print(f"  Old rules check: is_cc_old={is_cc_old}, is_rp_old={is_rp_old}")

def run_query(cursor, query, params=None):
    cursor.execute(query, params or ())
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

if __name__ == "__main__":
    main()

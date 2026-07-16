import mysql.connector
import sys
import os
import openpyxl
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_three_recent_courses_report import get_excel_chot_data, normalize_class_name, calibrate_students

def main():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    
    excel_path = r"C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx"
    excel_data = get_excel_chot_data(excel_path)
    
    # Class HCM-KS25-CNTT1
    class_raw = [{'id': 81, 'name': 'HCM-KS25-CNTT1'}]
    course_raw = [{'id': 79, 'name': '[IT103B-K25] Xây dựng ứng dụng'}]
    
    cid = 81
    co_id = 79
    
    students_results = run_query(cursor, """
        SELECT student_id, homework, elearning, attendance, hackathon_1, hackathon_2, rpoints, project, pass
        FROM qldt_el.final_results
        WHERE class_id = %s AND course_id = %s;
    """, (cid, co_id))
    
    print(f"Total students in DB for class {cid} and course {co_id}: {len(students_results)}")
    
    norm_cname = normalize_class_name('HCM-KS25-CNTT1')
    excel_disc = excel_data.get(norm_cname, {}).get('KS25_Python')
    
    print("Excel disc details:", excel_disc)
    
    calibrated = calibrate_students(students_results, excel_disc)
    
    for i, s in enumerate(calibrated[:5]):
        print(f"Student {s['student_id']}: rp_cal={s['rpoints']:.1f}, att_cal={s['attendance']:.1f}, hw_cal={s['homework']:.1f}, el_cal={s['elearning']:.1f}, pass={s['pass']}")

def run_query(cursor, query, params=None):
    cursor.execute(query, params or ())
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

if __name__ == "__main__":
    main()

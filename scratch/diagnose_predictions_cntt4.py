import mysql.connector
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

def mean(lst):
    return sum(lst) / len(lst) if lst else 0.0

def main():
    conn = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor(dictionary=True)
    
    cid = 51 # HN-KS24-CNTT4
    co_id = 123 # IT202 - K24 - Cơ sở dữ liệu
    
    # 1. Query students results
    cursor.execute("""
        SELECT student_id, homework, elearning, attendance, hackathon_1, hackathon_2, rpoints, project, pass
        FROM qldt_el.final_results
        WHERE class_id = %s AND course_id = %s AND pass IS NOT NULL;
    """, (cid, co_id))
    students_results = cursor.fetchall()
    
    total_students = len(students_results)
    actual_pass_count = sum(1 for s in students_results if s['pass'] == 1)
    actual_pass_rate = (actual_pass_count / total_students) * 100 if total_students > 0 else 0
    print(f"DEBUG: total={total_students}, pass_count={actual_pass_count}, pass_rate={actual_pass_rate:.2f}%")
    
    # Let's inspect what final_results contains for these students
    print("\nStudent list in DB:")
    for s in students_results[:10]:
        print(f"  student_id: {s['student_id']} | pass: {s['pass']} | hack1: {s['hackathon_1']} | rpoints: {s['rpoints']} | hw: {s['homework']}")
        
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

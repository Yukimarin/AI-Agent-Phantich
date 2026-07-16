import mysql.connector
import sys
import openpyxl
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

def main():
    conn = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor(dictionary=True)
    
    # 1. Inspect class HN-KS24-CNTT4
    print("=== 1. DIAGNOSING HN-KS24-CNTT4 ===")
    cursor.execute("SELECT id, name FROM classes WHERE name LIKE '%HN-KS24-CNTT4%'")
    cntt4_classes = cursor.fetchall()
    print("CNTT4 classes in DB:", cntt4_classes)
    
    if cntt4_classes:
        cid = cntt4_classes[0]['id']
        cursor.execute("""
            SELECT f.course_id, c.name as course_name, 
                   COUNT(*) as total_students,
                   SUM(CASE WHEN f.pass = 1 THEN 1 ELSE 0 END) as pass_count,
                   AVG(f.attendance) as avg_att,
                   AVG(f.homework) as avg_hw,
                   AVG(f.hackathon_1) as avg_h1,
                   AVG(f.rpoints) as avg_rp
            FROM final_results f
            JOIN courses c ON f.course_id = c.id
            WHERE f.class_id = %s
            GROUP BY f.course_id, c.name
        """, (cid,))
        results = cursor.fetchall()
        print("\nResults for HN-KS24-CNTT4 per course:")
        for r in results:
            pass_rate = (r['pass_count']/r['total_students'])*100 if r['total_students'] > 0 else 0
            print(f"Course: {r['course_name']} (ID {r['course_id']}) | Total: {r['total_students']} | Pass count: {r['pass_count']} | Pass%: {pass_rate:.2f}%")
            print(f"  Avg CC: {r['avg_att']}% | Avg HW: {r['avg_hw']}% | Avg Hackathon 1: {r['avg_h1']}% | Avg Rpoint: {r['avg_rp']}%")
            
            # Query sample of 3 students to see if their grades are identical or varied
            cursor.execute("""
                SELECT student_id, attendance, homework, hackathon_1, rpoints, pass
                FROM final_results
                WHERE class_id = %s AND course_id = %s
                LIMIT 3
            """, (cid, r['course_id']))
            samples = cursor.fetchall()
            print("  Samples:", samples)
            
    # 2. Inspect KS25 HCM classes mapping
    print("\n=== 2. DIAGNOSING KS25 HCM CLASSES ===")
    cursor.execute("SELECT id, name FROM classes WHERE name LIKE '%HCM-KS25%'")
    hcm_classes = cursor.fetchall()
    print("HCM KS25 classes in DB:", hcm_classes)
    
    # 3. Inspect QTKD classes
    print("\n=== 3. DIAGNOSING QTKD CLASSES ===")
    cursor.execute("SELECT id, name FROM classes WHERE name LIKE '%QTKD%'")
    qtkd_classes = cursor.fetchall()
    print("QTKD classes in DB:", qtkd_classes)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

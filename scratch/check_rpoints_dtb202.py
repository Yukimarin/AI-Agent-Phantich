import mysql.connector
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    
    print("=== QUERYING RPOINTS FOR DTB202 ===")
    cursor.execute("""
        SELECT class_id, AVG(total_score), AVG(attendance_score), AVG(assignment_score), AVG(compliance_score)
        FROM auto_rpoints 
        WHERE course_id = 178 AND class_id IN (82, 83, 84) 
        GROUP BY class_id
    """)
    rows = cursor.fetchall()
    for r in rows:
        print(f"Class ID: {r[0]} | Avg Rpoint: {r[1]:.2f}% | Attendance: {r[2]:.2f}% | Assignment: {r[3]:.2f}% | Compliance: {r[4]:.2f}%")
        
    conn.close()
except Exception as e:
    print("Error:", str(e))

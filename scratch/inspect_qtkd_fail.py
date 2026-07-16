import sys
sys.stdout.reconfigure(encoding='utf-8')
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='qldt_el')
cur = conn.cursor(dictionary=True)
cur.execute("""
    SELECT f.student_id, f.homework, f.elearning, f.attendance, f.mutiple_choice_1, f.interview_point, f.pass, f.guarantee
    FROM final_results f
    WHERE f.class_id = 83 AND f.course_id = 188
    LIMIT 10
""")
rows = cur.fetchall()
for r in rows:
    print(r)
conn.close()

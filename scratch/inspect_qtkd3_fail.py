import sys
sys.stdout.reconfigure(encoding='utf-8')
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='qldt_el')
cur = conn.cursor(dictionary=True)

cur.execute("""
    SELECT f.student_id, s.full_name, f.pass, f.attendance, f.homework
    FROM final_results f
    JOIN students s ON f.student_id = s.id
    WHERE f.class_id = 82 AND f.course_id = 188
    LIMIT 10
""")
rows = cur.fetchall()
for r in rows:
    print(r)
conn.close()

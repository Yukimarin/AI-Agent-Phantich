import sys
sys.stdout.reconfigure(encoding='utf-8')
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='qldt_el')
cur = conn.cursor(dictionary=True)

ids = [1734, 1720, 1696, 1718]
for sid in ids:
    cur.execute("""
        SELECT student_id, homework, attendance, elearning
        FROM final_results
        WHERE student_id = %s AND course_id = 178
    """, (sid,))
    print(cur.fetchone())
conn.close()

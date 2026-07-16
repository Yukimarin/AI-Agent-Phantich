import sys
sys.stdout.reconfigure(encoding='utf-8')
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='qldt_el')
cur = conn.cursor(dictionary=True)
cur.execute("""
    SELECT DISTINCT f.course_id, c.name
    FROM final_results f
    JOIN courses c ON f.course_id = c.id
    WHERE f.class_id = 77;
""")
print("Courses for Class 77:")
for r in cur.fetchall():
    print(r)
conn.close()

import sys
sys.stdout.reconfigure(encoding='utf-8')
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='qldt_el')
cur = conn.cursor(dictionary=True)

students = [
    {"id": 1734, "name": "Bùi Hà Uyên"},
    {"id": 1720, "name": "Nguyễn Bảo Ngọc"},
    {"id": 1696, "name": "Nguyễn Minh Hiếu 7"},
    {"id": 1718, "name": "Lê Nam Phong"}
]

for s in students:
    print(f"=== {s['name']} (ID: {s['id']}) ===")
    cur.execute("""
        SELECT a.date, ad.status
        FROM attendance a
        JOIN attendance_detail ad ON ad.attendance_id = a.id
        WHERE a.classes_id = 82 AND a.courses_id = 178 AND ad.student_id = %s
    """, (s['id'],))
    rows = cur.fetchall()
    for r in rows:
        print(r)
conn.close()

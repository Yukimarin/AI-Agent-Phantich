import sys
sys.stdout.reconfigure(encoding='utf-8')
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='qldt_el')
cur = conn.cursor(dictionary=True)

ids = [1734, 1720]
for sid in ids:
    cur.execute("""
        SELECT *
        FROM final_results
        WHERE student_id = %s AND course_id = 188
    """, (sid,))
    row = cur.fetchone()
    print(f"=== Student {sid} ===")
    if row:
        for k, v in row.items():
            if v is not None and v != 0 and v != 0.0:
                print(f"  {k}: {v}")
conn.close()

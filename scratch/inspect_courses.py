import sys
sys.stdout.reconfigure(encoding='utf-8')
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='qldt_el')
cur = conn.cursor(dictionary=True)
cur.execute("SELECT id, name FROM courses WHERE name LIKE '%Python%' OR name LIKE '%Java%' OR name LIKE '%AI%' OR name LIKE '%JavaScript%' OR name LIKE '%Business%' OR name LIKE '%Doanh nghiệp%';")
print("Courses in DB:")
for r in cur.fetchall():
    print(r)
conn.close()

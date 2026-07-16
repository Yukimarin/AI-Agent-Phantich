import sys
sys.stdout.reconfigure(encoding='utf-8')
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='qldt_el')
cur = conn.cursor(dictionary=True)
cur.execute("SELECT `check`, COUNT(*) as cnt FROM exercise GROUP BY `check`")
rows = cur.fetchall()
for r in rows:
    print(r)
conn.close()

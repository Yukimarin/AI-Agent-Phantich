import sys
sys.stdout.reconfigure(encoding='utf-8')
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='qldt_el')
cur = conn.cursor(dictionary=True)

print("Columns in attendance:")
cur.execute("DESCRIBE attendance;")
for r in cur.fetchall():
    print(r)

print("\nColumns in exercise:")
cur.execute("DESCRIBE exercise;")
for r in cur.fetchall():
    print(r)
    
conn.close()

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
    
    print("=== INSPECTING 'courses' TABLE ===")
    cursor.execute("DESCRIBE courses")
    print("Columns:", [c[0] for c in cursor.fetchall()])
    
    cursor.execute("SELECT id, name, course_code FROM courses LIMIT 30")
    print("Rows in courses:")
    for r in cursor.fetchall():
        print("  ", r)
        
    conn.close()
except Exception as e:
    print("Error:", str(e))

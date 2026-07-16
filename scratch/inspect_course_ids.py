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
    
    # Tìm kiếm các môn học chứa DTB202 hoặc PRJ302
    cursor.execute("SELECT id, name, course_code FROM courses WHERE name LIKE '%DTB%' OR name LIKE '%PRJ%' OR course_code LIKE '%DTB%' OR course_code LIKE '%PRJ%'")
    print("Matching courses:")
    for r in cursor.fetchall():
        print("  ", r)
        
    conn.close()
except Exception as e:
    print("Error:", str(e))

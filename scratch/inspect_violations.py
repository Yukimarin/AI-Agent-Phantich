import mysql.connector
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="qldt_el"
)
cursor = conn.cursor()

output_file = 'scratch/inspect_tables.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=== SCHEMA OF ATTENDANCE_DETAIL ===\n")
    cursor.execute("DESCRIBE qldt_el.attendance_detail;")
    for row in cursor.fetchall():
        f.write(f"  {row[0]}: {row[1]}\n")
        
    f.write("\n=== DISTINCT STATUS IN ATTENDANCE_DETAIL ===\n")
    cursor.execute("SELECT DISTINCT status FROM qldt_el.attendance_detail LIMIT 10;")
    for row in cursor.fetchall():
        f.write(f"  Status: {row[0]}\n")
        
    f.write("\n=== SCHEMA OF LATE_SUBMISSIONS ===\n")
    cursor.execute("SHOW TABLES LIKE 'late_submissions';")
    if cursor.fetchall():
        cursor.execute("DESCRIBE qldt_el.late_submissions;")
        for row in cursor.fetchall():
            f.write(f"  {row[0]}: {row[1]}\n")
            
    f.write("\n=== SCHEMA OF ELEARNING_LATE ===\n")
    cursor.execute("SHOW TABLES LIKE 'elearning_late';")
    if cursor.fetchall():
        cursor.execute("DESCRIBE qldt_el.elearning_late;")
        for row in cursor.fetchall():
            f.write(f"  {row[0]}: {row[1]}\n")

    f.write("\n=== SCHEMA OF ATTENDANCE_WARNING ===\n")
    cursor.execute("SHOW TABLES LIKE 'attendance_warning';")
    if cursor.fetchall():
        cursor.execute("DESCRIBE qldt_el.attendance_warning;")
        for row in cursor.fetchall():
            f.write(f"  {row[0]}: {row[1]}\n")

    f.write("\n=== SCHEMA OF RPOINTS ===\n")
    cursor.execute("SHOW TABLES LIKE 'rpoints';")
    if cursor.fetchall():
        cursor.execute("DESCRIBE qldt_el.rpoints;")
        for row in cursor.fetchall():
            f.write(f"  {row[0]}: {row[1]}\n")

print("Violation inspection completed.")
cursor.close()
conn.close()

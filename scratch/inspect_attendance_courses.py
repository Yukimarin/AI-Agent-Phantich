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
    f.write("=== ALL COURSES IN DATABASE ===\n")
    cursor.execute("SELECT id, name FROM qldt_el.courses ORDER BY id;")
    for row in cursor.fetchall():
        f.write(f"Course ID: {row[0]}, Name: {row[1]}\n")
        
    f.write("\n=== ACTIVE COURSES IN ATTENDANCE FOR KS24, KS25, QTKD ===\n")
    ks24_cids = (48, 49, 156, 51, 63, 64, 69, 50, 52)
    ks25_cids = (77, 76, 75, 74, 73, 72, 71, 81, 80, 79, 78)
    qtkd_cids = (84, 83, 82)
    all_cids = ks24_cids + ks25_cids + qtkd_cids
    
    query = """
        SELECT DISTINCT a.classes_id, cl.name as class_name, a.courses_id, c.name as course_name
        FROM qldt_el.attendance a
        JOIN qldt_el.courses c ON a.courses_id = c.id
        JOIN qldt_el.classes cl ON a.classes_id = cl.id
        WHERE a.classes_id IN ({})
        ORDER BY a.classes_id, a.courses_id;
    """.format(",".join(map(str, all_cids)))
    
    cursor.execute(query)
    for row in cursor.fetchall():
        f.write(f"Class: {row[1]} (ID: {row[0]}) -> Course: {row[3]} (ID: {row[2]})\n")

print("Attendance courses query completed.")
cursor.close()
conn.close()

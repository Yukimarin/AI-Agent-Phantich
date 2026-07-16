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

# Targeted classes
ks24_cids = (48, 49, 156, 51, 63, 64, 69)
ks25_cids = (77, 76, 75, 74, 73, 72, 71, 81, 80, 79, 78)
qtkd_cids = (84, 83, 82)

output_file = 'scratch/inspect_tables.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=== ACTIVE COURSES IN FINAL_RESULTS WITH NULL PASS (CURRENT COURSES) ===\n")
    
    # Query current course for each class batch
    query = """
        SELECT DISTINCT f.class_id, cl.name as class_name, f.course_id, c.name as course_name, COUNT(*) as student_count
        FROM qldt_el.final_results f
        JOIN qldt_el.courses c ON f.course_id = c.id
        JOIN qldt_el.classes cl ON f.class_id = cl.id
        WHERE f.class_id IN ({}) AND f.pass IS NULL
        GROUP BY f.class_id, f.course_id
        ORDER BY f.class_id, f.course_id;
    """.format(",".join(map(str, ks24_cids + ks25_cids + qtkd_cids)))
    
    cursor.execute(query)
    for row in cursor.fetchall():
        f.write(f"Class: {row[1]} (ID: {row[0]}) -> Course: {row[3]} (ID: {row[2]}) | Students: {row[4]}\n")
        
    f.write("\n=== SAMPLE STUDENTS FOR TARGETED COURSES ===\n")
    # Let's check some student names and grades for a class
    cursor.execute("""
        SELECT f.class_id, cl.name as class_name, f.course_id, c.name as course_name, 
               s.id as student_id, s.full_name as student_name, s.student_code,
               f.attendance, f.homework, f.elearning, f.hackathon_1, f.hackathon_2, f.project, f.pass
        FROM qldt_el.final_results f
        JOIN qldt_el.students s ON f.student_id = s.id
        JOIN qldt_el.courses c ON f.course_id = c.id
        JOIN qldt_el.classes cl ON f.class_id = cl.id
        WHERE f.class_id IN ({}) AND f.pass IS NULL
        LIMIT 50;
    """.format(",".join(map(str, ks24_cids + ks25_cids + qtkd_cids))))
    
    for row in cursor.fetchall():
        f.write(f"Class: {row[1]}, Course: {row[3]}, Student: {row[5]} ({row[6]}) | Att: {row[7]} | HW: {row[8]} | EL: {row[9]} | H1: {row[10]} | H2: {row[11]} | Proj: {row[12]} | Pass: {row[13]}\n")

print("Current students query completed.")
cursor.close()
conn.close()

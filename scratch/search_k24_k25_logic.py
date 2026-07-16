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
    f.write("=== KS24 AI RECORDS IN FINAL_RESULTS ===\n")
    query = """
        SELECT f.class_id, cl.name as class_name, f.course_id, c.name as course_name, COUNT(*)
        FROM qldt_el.final_results f
        JOIN qldt_el.courses c ON f.course_id = c.id
        JOIN qldt_el.classes cl ON f.class_id = cl.id
        WHERE f.class_id IN (48, 49, 156, 51, 63, 64, 69) AND (c.name LIKE '%AI%' OR c.name LIKE '%Trí tuệ%')
        GROUP BY f.class_id, f.course_id;
    """
    cursor.execute(query)
    for row in cursor.fetchall():
        f.write(f"  Class: {row[1]} (ID: {row[0]}) -> Course: {row[3]} (ID: {row[2]}) | Count: {row[4]}\n")

    f.write("\n=== KS25 PYTHON RECORDS IN FINAL_RESULTS ===\n")
    query2 = """
        SELECT f.class_id, cl.name as class_name, f.course_id, c.name as course_name, COUNT(*)
        FROM qldt_el.final_results f
        JOIN qldt_el.courses c ON f.course_id = c.id
        JOIN qldt_el.classes cl ON f.class_id = cl.id
        WHERE f.class_id IN (77, 76, 75, 74, 73, 72, 71, 81, 80, 79, 78) AND (c.name LIKE '%Python%' OR c.name LIKE '%FastAPI%')
        GROUP BY f.class_id, f.course_id;
    """
    cursor.execute(query2)
    for row in cursor.fetchall():
        f.write(f"  Class: {row[1]} (ID: {row[0]}) -> Course: {row[3]} (ID: {row[2]}) | Count: {row[4]}\n")

    f.write("\n=== QTKD RECORDS IN FINAL_RESULTS ===\n")
    query3 = """
        SELECT f.class_id, cl.name as class_name, f.course_id, c.name as course_name, COUNT(*)
        FROM qldt_el.final_results f
        JOIN qldt_el.courses c ON f.course_id = c.id
        JOIN qldt_el.classes cl ON f.class_id = cl.id
        WHERE f.class_id IN (84, 83, 82) AND (c.name LIKE '%DTB202%' OR c.name LIKE '%PRJ302%' OR c.name LIKE '%Chuyển đổi số%' OR c.name LIKE '%Dự án%')
        GROUP BY f.class_id, f.course_id;
    """
    cursor.execute(query3)
    for row in cursor.fetchall():
        f.write(f"  Class: {row[1]} (ID: {row[0]}) -> Course: {row[3]} (ID: {row[2]}) | Count: {row[4]}\n")

print("Updated search completed.")
cursor.close()
conn.close()

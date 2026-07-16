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
    f.write("=== ACTIVE COURSES PER CLASS BATCH ===\n")
    
    # Class groups
    ks24_cids = (48, 49, 156, 51, 63, 64, 69, 50, 52)
    ks25_cids = (77, 76, 75, 74, 73, 72, 71, 81, 80, 79, 78)
    qtkd_cids = (84, 83, 82)
    
    all_cids = ks24_cids + ks25_cids + qtkd_cids
    
    query = """
        SELECT DISTINCT c.id, c.name, f.class_id, cl.name as class_name
        FROM qldt_el.final_results f
        JOIN qldt_el.courses c ON f.course_id = c.id
        JOIN qldt_el.classes cl ON f.class_id = cl.id
        WHERE f.class_id IN ({})
        ORDER BY f.class_id, c.id;
    """.format(",".join(map(str, all_cids)))
    
    cursor.execute(query)
    for row in cursor.fetchall():
        f.write(f"Class ID: {row[2]} ({row[3]}) -> Course ID: {row[0]}, Course Name: {row[1]}\n")

print("Detailed courses query completed.")
cursor.close()
conn.close()

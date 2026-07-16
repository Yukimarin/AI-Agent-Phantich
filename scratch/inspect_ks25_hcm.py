import mysql.connector
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    conn = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor(dictionary=True)
    
    print("=== KS25 HCM CLASSES & COURSES IN NEW DB ===")
    cursor.execute("""
        SELECT DISTINCT c.id as class_id, c.name as class_name, f.course_id, co.name as course_name, COUNT(*) as students_count
        FROM final_results f
        JOIN classes c ON f.class_id = c.id
        JOIN courses co ON f.course_id = co.id
        WHERE c.name LIKE '%HCM-KS25%'
        GROUP BY c.id, c.name, f.course_id, co.name
        ORDER BY c.name, co.name;
    """)
    rows = cursor.fetchall()
    for r in rows:
        print(f"Class: {r['class_name']} (ID {r['class_id']}) | Course: {r['course_name']} (ID {r['course_id']}) | Students: {r['students_count']}")
        
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

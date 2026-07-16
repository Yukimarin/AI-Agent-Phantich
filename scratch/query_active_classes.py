import mysql.connector
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor(dictionary=True)
    
    # Query active classes and their course
    cursor.execute("""
        SELECT c.id as class_id, c.name as class_name, c.class_code, co.id as course_id, co.name as course_name, MAX(a.date) as max_date
        FROM qldt_el.classes c
        JOIN qldt_el.student_class sc ON c.id = sc.class_id
        JOIN qldt_el.attendance a ON c.id = a.classes_id
        JOIN qldt_el.courses co ON a.courses_id = co.id
        JOIN qldt_el.specializes sp ON c.specializes_id = sp.id
        JOIN qldt_el.systems sys ON sp.systems_id = sys.id
        WHERE sc.is_active = 1 AND a.date >= '2025-01-01' AND sys.system_code LIKE 'PTIT%'
        GROUP BY c.id, co.id;
    """)
    active_classes = cursor.fetchall()
    print(f"Found {len(active_classes)} active class-course pairs:")
    for row in active_classes:
        print(f"  Class ID: {row['class_id']:<3} | Class: {row['class_name']:<25} | Course ID: {row['course_id']:<3} | Course: {row['course_name'][:30]:<30} | Last Attendance: {row['max_date']}")
        
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

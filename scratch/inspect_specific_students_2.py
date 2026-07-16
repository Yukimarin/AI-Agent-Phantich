import sys
sys.stdout.reconfigure(encoding='utf-8')
import mysql.connector

conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='qldt_el')
cur = conn.cursor(dictionary=True)

names = ["Bùi Hà Uyên", "Nguyễn Bảo Ngọc"]
for name in names:
    print(f"=== Student: {name} ===")
    cur.execute("SELECT id, full_name, student_code FROM students WHERE full_name LIKE %s", (f"%{name}%",))
    students = cur.fetchall()
    for s in students:
        sid = s['id']
        print(s)
        # Query final_results for this student
        cur.execute("""
            SELECT f.course_id, c.name as course_name, f.class_id, cl.name as class_name, 
                   f.homework, f.elearning, f.attendance, f.mutiple_choice_1, f.project, f.pass, f.rpoints
            FROM final_results f
            JOIN courses c ON f.course_id = c.id
            JOIN classes cl ON f.class_id = cl.id
            WHERE f.student_id = %s
        """, (sid,))
        results = cur.fetchall()
        for r in results:
            print(r)
conn.close()

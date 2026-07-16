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
    cursor.execute("""
        SELECT student_id, homework, elearning, attendance, hackathon_1, hackathon_2, rpoints, pass
        FROM qldt_el.final_results
        WHERE course_id = 183 AND class_id = 77
        LIMIT 10;
    """)
    rows = cursor.fetchall()
    print("Sample data from final_results for course 183 class 77:")
    for r in rows:
        print(r)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

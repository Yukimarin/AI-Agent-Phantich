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
    
    # Check grades for class HCM-KS24-CNTT1 (ID 63) in Java Service (ID 194)
    cursor.execute("""
        SELECT student_id, homework, elearning, attendance, hackathon_1, hackathon_2, do_project, project, pass
        FROM qldt_el.final_results
        WHERE class_id = 63 AND course_id = 194;
    """)
    rows = cursor.fetchall()
    print("Grades for HCM-KS24-CNTT1 in Java Service:")
    for r in rows[:15]:
        print(r)
        
    # Check why pass is 0 for everyone
    passes = sum(1 for r in rows if r['pass'] == 1)
    fails = sum(1 for r in rows if r['pass'] == 0)
    nulls = sum(1 for r in rows if r['pass'] is None)
    print(f"\nSummary: Total={len(rows)}, Pass={passes}, Fail={fails}, Null={nulls}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

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
    cursor = conn.cursor()
    cursor.execute("""
        SELECT class_id, 
               SUM(CASE WHEN pass = 1 THEN 1 ELSE 0 END) as pass_count,
               COUNT(*) as total
        FROM qldt_el.final_results
        WHERE course_id = 124
        GROUP BY class_id;
    """)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    print("Columns:", columns)
    for row in rows[:5]:
        print("Row:", row)
        zipped = dict(zip(columns, row))
        print("Zipped:", zipped)
        print("total val:", zipped['total'], type(zipped['total']))
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

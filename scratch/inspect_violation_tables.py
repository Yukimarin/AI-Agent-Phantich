import mysql.connector
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    tables = ['request_leave', 'documents', 'take_care_student', 'sessions', 'lessons', 'role_guard_logs']
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="qldt_el",
            port=3307
        )
        cursor = conn.cursor()
        
        for table in tables:
            print(f"\n========================================\nCấu trúc bảng: {table}\n========================================")
            try:
                cursor.execute(f"DESCRIBE {table}")
                cols = cursor.fetchall()
                for c in cols:
                    print(f"Column: {c[0]} | Type: {c[1]} | Null: {c[2]} | Key: {c[3]}")
            except Exception as e:
                print(f"Error describing table {table}: {e}")
                
        conn.close()
    except Exception as e:
        print("Error connecting to MySQL:", str(e))

if __name__ == "__main__":
    main()

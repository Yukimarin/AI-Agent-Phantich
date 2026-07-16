import mysql.connector
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="qldt_el",
            port=3307
        )
        cursor = conn.cursor(dictionary=True)
        
        # 1. Tìm thông tin môn học
        print("--- Tìm kiếm môn học (courses) ---")
        cursor.execute("SELECT id, name FROM courses WHERE name LIKE '%Python%' OR name LIKE '%Web%'")
        courses = cursor.fetchall()
        for c in courses:
            print(f"Course ID: {c['id']} | Name: {c['name']}")
            
        # 2. Tìm thông tin lớp học khóa KS25
        print("\n--- Tìm kiếm lớp học (classes) ---")
        cursor.execute("SELECT id, name FROM classes WHERE name LIKE '%KS25-CNTT%' OR name LIKE '%K25-CNTT%'")
        classes = cursor.fetchall()
        for cl in classes:
            print(f"Class ID: {cl['id']} | Name: {cl['name']}")
            
        conn.close()
    except Exception as e:
        print("Error connecting to MySQL:", str(e))

if __name__ == "__main__":
    main()

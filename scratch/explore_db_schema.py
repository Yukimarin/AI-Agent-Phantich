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
    
    # 1. Show tables
    cursor.execute("SHOW TABLES;")
    tables = [row[0] for row in cursor.fetchall()]
    print("Tables in database:", tables)
    
    # 2. Check some table structures
    target_tables = ['classes', 'courses', 'student_class', 'attendance', 'attendance_detail', 'final_results', 'result_test']
    for table in target_tables:
        if table in tables:
            cursor.execute(f"DESCRIBE {table};")
            columns = cursor.fetchall()
            print(f"\nStructure of '{table}':")
            for col in columns[:8]: # print first 8 columns
                print(f"  {col[0]}: {col[1]} (Null: {col[2]}, Key: {col[3]})")
            if len(columns) > 8:
                print(f"  ... and {len(columns)-8} more columns")
                
    # 3. Check some class names
    cursor.execute("SELECT name FROM classes LIMIT 15;")
    classes = [row[0] for row in cursor.fetchall()]
    print("\nSome class names:", classes)

    # 4. Check some course names
    cursor.execute("SELECT name FROM courses LIMIT 15;")
    courses = [row[0] for row in cursor.fetchall()]
    print("\nSome course names:", courses)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

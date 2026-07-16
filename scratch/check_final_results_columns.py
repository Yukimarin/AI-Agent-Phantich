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
    cursor.execute("DESCRIBE final_results;")
    columns = cursor.fetchall()
    print("Columns in final_results:")
    for col in columns:
        print(f"  {col[0]}: {col[1]}")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

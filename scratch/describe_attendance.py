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
        cursor = conn.cursor()
        
        cursor.execute("DESCRIBE attendance")
        print("Bảng attendance:")
        for c in cursor.fetchall():
            print(f"- {c[0]} ({c[1]})")
            
        cursor.execute("DESCRIBE attendance_detail")
        print("\nBảng attendance_detail:")
        for c in cursor.fetchall():
            print(f"- {c[0]} ({c[1]})")
            
        conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()

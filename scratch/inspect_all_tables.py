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
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        print("Danh sách các bảng trong CSDL qldt_el:")
        for t in tables:
            print(f"- {t}")
        conn.close()
    except Exception as e:
        print("Error connecting to MySQL:", str(e))

if __name__ == "__main__":
    main()

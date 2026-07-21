import mysql.connector
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'qldt_el',
    'port': 3307
}

def main():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM courses ORDER BY id ASC")
        rows = cursor.fetchall()
        print("=== ALL COURSES IN DB ===")
        for r in rows:
            print(f"ID: {r['id']} | Name: {r['name']}")
        conn.close()
    except Exception as e:
        print("Error connecting to MySQL:", str(e))

if __name__ == "__main__":
    main()

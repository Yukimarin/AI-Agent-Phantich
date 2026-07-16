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
        
        print("Các log liên quan đến điểm danh trong role_guard_logs (15 dòng đầu):")
        cursor.execute("""
            SELECT username, method, url, created_at, reason 
            FROM role_guard_logs 
            WHERE url LIKE '%attendance%' 
            ORDER BY created_at DESC 
            LIMIT 15
        """)
        rows = cursor.fetchall()
        for r in rows:
            print(f"User: {r['username']} | Method: {r['method']} | URL: {r['url']} | Created At: {r['created_at']} | Reason: {r['reason']}")
            
        conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()

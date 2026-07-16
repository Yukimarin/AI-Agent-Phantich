import mysql.connector
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    
    # Liệt kê các bảng
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    print("Tables in qldt_el:", tables)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = cursor.fetchone()[0]
        print(f"\nTable: {table} | Row count: {cnt}")
        
        # Xem cấu trúc cột
        cursor.execute(f"DESCRIBE {table}")
        cols = cursor.fetchall()
        print("  Columns:", [c[0] for c in cols])
        
        # Xem 3 dòng đầu
        cursor.execute(f"SELECT * FROM {table} LIMIT 3")
        rows = cursor.fetchall()
        print("  First 3 rows:")
        for r in rows:
            print("    ", [str(x) for x in r])
            
    conn.close()
except Exception as e:
    print("Error connecting to MySQL:", str(e))

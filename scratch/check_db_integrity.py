import sqlite3
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

db_path = 'data/qldt.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]
print("Tables found:", tables)

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    cnt = cursor.fetchone()[0]
    print(f"\nTable: {table} | Row count: {cnt}")
    
    cursor.execute(f"PRAGMA table_info({table})")
    cols = cursor.fetchall()
    print("  Columns:", [c[1] for c in cols])
    
    cursor.execute(f"SELECT * FROM {table} LIMIT 3")
    rows = cursor.fetchall()
    print("  First 3 rows:")
    for r in rows:
        # Convert row values to string and encode to utf-8 safely when printing
        r_str = [str(x) for x in r]
        print("    ", ", ".join(r_str))
        
    if table == 'student_grades':
        cursor.execute("SELECT student_id, class_id, COUNT(*) FROM student_grades GROUP BY student_id, class_id HAVING COUNT(*) > 1")
        dups = cursor.fetchall()
        print(f"  Duplicates in student_grades (student_id + class_id): {len(dups)}")
        
conn.close()

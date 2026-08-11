import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('data/inputs/qldt.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in SQLite qldt.db:", tables)
for t in tables:
    tname = t[0]
    cursor.execute(f"PRAGMA table_info({tname});")
    info = cursor.fetchall()
    print(f"\nTable {tname} schema:")
    for col in info:
        print("  ", col)
    cursor.execute(f"SELECT COUNT(*) FROM {tname};")
    cnt = cursor.fetchone()[0]
    print(f"  Total rows: {cnt}")
    if cnt > 0:
        cursor.execute(f"SELECT * FROM {tname} LIMIT 3;")
        print("  Sample rows:")
        for r in cursor.fetchall():
            print("    ", r)
conn.close()

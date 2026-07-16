import sqlite3
conn = sqlite3.connect('data/qldt.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in SQLite database:")
for t in cursor.fetchall():
    print(t[0])
conn.close()

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="qldt_el"
)
cursor = conn.cursor()

print("Searching courses in MySQL:")
# Find courses matching keywords
cursor.execute("SELECT id, name FROM qldt_el.courses WHERE name LIKE '%212%' OR name LIKE '%215%' OR name LIKE '%302%' OR name LIKE '%FastAPI%' OR name LIKE '%AI%' OR name LIKE '%Python%' OR name LIKE '%PRJ%';")
for row in cursor.fetchall():
    print(f"  ID: {row[0]}, Name: {row[1]}")

cursor.close()
conn.close()

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="qldt_el"
)
cursor = conn.cursor()

# Check all columns of final_results
cursor.execute("DESCRIBE qldt_el.final_results;")
cols = cursor.fetchall()
print("All columns of final_results:")
for col in cols:
    print(f"  {col[0]}: {col[1]} (Key: {col[3]})")

# List courses related to AI, Python, FastAPI, PRJ302
cursor.execute("SELECT id, name FROM qldt_el.courses WHERE name LIKE '%AI%' OR name LIKE '%Python%' OR name LIKE '%FastAPI%' OR name LIKE '%PRJ%' OR name LIKE '%DTB%' OR name LIKE '%Project%';")
print("\nMatching courses:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

cursor.close()
conn.close()

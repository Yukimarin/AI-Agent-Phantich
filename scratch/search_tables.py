import sqlite3
import mysql.connector

def search_sqlite():
    print("=== SQLITE TABLES ===")
    conn = sqlite3.connect("data/qldt.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print("Tables:", tables)
    conn.close()

def search_mysql():
    print("\n=== MYSQL TABLES ===")
    conn = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = [t[0] for t in cursor.fetchall()]
    print("Total tables:", len(tables))
    keywords = ["task", "project", "daily", "worklane", "log", "weekly", "report", "gvtg", "violation"]
    for t in tables:
        for kw in keywords:
            if kw in t.lower():
                print(f"Matched table: {t} (kw: {kw})")
    conn.close()

if __name__ == "__main__":
    search_sqlite()
    search_mysql()

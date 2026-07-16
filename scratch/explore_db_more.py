import sqlite3
import mysql.connector
import sys

def inspect_sqlite(f):
    f.write("=== SQLITE TABLES ===\n")
    try:
        conn = sqlite3.connect("data/qldt.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for t in tables:
            f.write(f"Table: {t[0]}\n")
            cursor.execute(f"PRAGMA table_info({t[0]});")
            cols = cursor.fetchall()
            for col in cols:
                f.write(f"  Col: {col[1]} ({col[2]})\n")
            
            try:
                # Print sample data
                cursor.execute(f"SELECT * FROM {t[0]} LIMIT 2;")
                rows = cursor.fetchall()
                f.write(f"  Sample rows: {rows}\n")
            except Exception as ex:
                f.write(f"  Error reading sample: {ex}\n")
        conn.close()
    except Exception as e:
        f.write(f"Error SQLite: {e}\n")

def inspect_mysql(f):
    f.write("\n=== MYSQL TABLES ===\n")
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="qldt_el"
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        for t in tables:
            f.write(f"Table: {t[0]}\n")
            cursor.execute(f"DESCRIBE {t[0]};")
            cols = cursor.fetchall()
            for col in cols:
                f.write(f"  Col: {col[0]} ({col[1]})\n")
            
            try:
                # Print sample data
                cursor.execute(f"SELECT * FROM {t[0]} LIMIT 2;")
                rows = cursor.fetchall()
                f.write(f"  Sample data: {rows}\n")
            except Exception as ex:
                f.write(f"  Error reading sample: {ex}\n")
        conn.close()
    except Exception as e:
        f.write(f"Error MySQL: {e}\n")

if __name__ == "__main__":
    with open("scratch/explore_db_results.txt", "w", encoding="utf-8") as f:
        inspect_sqlite(f)
        inspect_mysql(f)
    print("Inspection finished. Results written to scratch/explore_db_results.txt")

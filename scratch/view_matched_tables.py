import mysql.connector

def view_details():
    conn = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    
    tables_to_view = [
        "daily_class_report", 
        "project", 
        "project_detail", 
        "project_students", 
        "task", 
        "task_detail", 
        "completed_task"
    ]
    
    with open("scratch/matched_tables_detail.txt", "w", encoding="utf-8") as f:
        for t in tables_to_view:
            f.write(f"\n==================== TABLE: {t} ====================\n")
            try:
                cursor.execute(f"DESCRIBE {t};")
                cols = cursor.fetchall()
                f.write("Columns:\n")
                for col in cols:
                    f.write(f"  {col[0]} ({col[1]})\n")
                
                cursor.execute(f"SELECT COUNT(*) FROM {t};")
                cnt = cursor.fetchone()[0]
                f.write(f"Total Rows: {cnt}\n")
                
                cursor.execute(f"SELECT * FROM {t} LIMIT 5;")
                rows = cursor.fetchall()
                f.write("Sample Data:\n")
                for r in rows:
                    f.write(f"  {r}\n")
            except Exception as e:
                f.write(f"Error viewing table {t}: {e}\n")
                
    conn.close()
    print("Done. Details written to scratch/matched_tables_detail.txt")

if __name__ == "__main__":
    view_details()

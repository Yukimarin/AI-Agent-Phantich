import mysql.connector

def run_queries(f):
    conn = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    
    f.write("=== DỮ LIỆU BÁO CÁO NGÀY (DAILY CLASS REPORT) ===\n")
    cursor.execute("SELECT MIN(date), MAX(date), COUNT(*) FROM daily_class_report;")
    min_date, max_date, total_reports = cursor.fetchone()
    f.write(f"Khoảng ngày báo cáo: {min_date} đến {max_date}. Tổng số báo cáo ngày: {total_reports}\n")
    
    cursor.execute("""
        SELECT d.date, COUNT(DISTINCT d.class_id) as active_classes, 
               SUM(d.absent_count) as total_absents, 
               SUM(d.missing_homework_count) as total_missing_hw,
               SUM(d.elearning_late_count) as total_late_el,
               SUM(d.total_students) as total_students
        FROM daily_class_report d
        WHERE d.date BETWEEN '2026-07-06' AND '2026-07-12'
        GROUP BY d.date
        ORDER BY d.date;
    """)
    f.write("\nThống kê báo cáo ngày Tuần 28 (06/07 - 12/07/2026):\n")
    rows = cursor.fetchall()
    for r in rows:
        f.write(f"Ngày {r[0]}: {r[1]} lớp học, Vắng {r[2]} SV, Nợ BT {r[3]} SV, Chậm EL {r[4]} SV, Tổng {r[5]} SV\n")
        
    f.write("\n=== CẤU TRÚC BẢNG LỚP HỌC & MÔN HỌC ===\n")
    cursor.execute("SHOW TABLES;")
    tables = [t[0] for t in cursor.fetchall()]
    f.write("Các bảng trong MySQL liên quan tới Course/Class/Student/User:\n")
    for t in tables:
        if any(kw in t.lower() for kw in ["course", "class", "student", "user"]):
            f.write(f"  {t}\n")
            
    for t in ["courses", "classes", "students", "users", "student_class"]:
        if t in tables:
            cursor.execute(f"DESCRIBE {t};")
            f.write(f"\nTable {t}:\n")
            for col in cursor.fetchall():
                f.write(f"  {col[0]} ({col[1]})\n")
                
            cursor.execute(f"SELECT * FROM {t} LIMIT 3;")
            rows = cursor.fetchall()
            f.write("  Sample rows:\n")
            for r in rows:
                f.write(f"    {r}\n")

    conn.close()

if __name__ == "__main__":
    with open("scratch/query_project_stats_results.txt", "w", encoding="utf-8") as f:
        try:
            run_queries(f)
            f.write("\nQueries executed successfully.\n")
        except Exception as e:
            f.write(f"Lỗi: {e}\n")
    print("Done. Output written to scratch/query_project_stats_results.txt")

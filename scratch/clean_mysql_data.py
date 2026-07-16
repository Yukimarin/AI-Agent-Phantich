import mysql.connector
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    conn = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    print("=== STARTING MYSQL DATABASE CLEANING (qldt_el) ===")
    
    # 1. Giới hạn điểm số vượt trần 100.0 và dưới sàn 0.0
    # Trong final_results
    cursor.execute("UPDATE final_results SET rpoints = 100.0 WHERE rpoints > 100.0")
    fr_cap_cnt = cursor.rowcount
    cursor.execute("UPDATE final_results SET rpoints = 0.0 WHERE rpoints < 0.0")
    fr_floor_cnt = cursor.rowcount
    
    # Trong auto_rpoints
    cursor.execute("UPDATE auto_rpoints SET total_score = 100.0 WHERE total_score > 100.0")
    ar_cap_cnt = cursor.rowcount
    cursor.execute("UPDATE auto_rpoints SET total_score = 0.0 WHERE total_score < 0.0")
    ar_floor_cnt = cursor.rowcount
    
    print(f"Limiting scores:")
    print(f"  - final_results.rpoints limited (>100): {fr_cap_cnt} rows, (<0): {fr_floor_cnt} rows")
    print(f"  - auto_rpoints.total_score limited (>100): {ar_cap_cnt} rows, (<0): {ar_floor_cnt} rows")
    
    # 2. Xóa các bản ghi trùng lặp (Deduplication)
    # Bảng final_results
    cursor.execute("""
        DELETE t1 FROM final_results t1
        INNER JOIN final_results t2 
        ON t1.student_id = t2.student_id 
        AND t1.course_id = t2.course_id 
        AND t1.id < t2.id
    """)
    fr_dup_deleted = cursor.rowcount
    
    # Bảng auto_rpoints
    cursor.execute("""
        DELETE t1 FROM auto_rpoints t1
        INNER JOIN auto_rpoints t2 
        ON t1.student_id = t2.student_id 
        AND t1.course_id = t2.course_id 
        AND t1.id < t2.id
    """)
    ar_dup_deleted = cursor.rowcount
    
    print(f"Deleting duplicates:")
    print(f"  - final_results duplicates deleted: {fr_dup_deleted} rows")
    print(f"  - auto_rpoints duplicates deleted: {ar_dup_deleted} rows")
    
    conn.commit()
    conn.close()
    print("MySQL database cleaning completed successfully!")
    
except Exception as e:
    print("Error during MySQL database cleaning:", str(e))

import mysql.connector
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    
    print("=== INSPECTING QLDT_EL FOR DIRTY DATA ===")
    
    # 1. Kiểm tra điểm số bất thường trong final_results (ví dụ: gpa, rpoints)
    # Tìm xem bảng final_results có cột nào
    cursor.execute("DESCRIBE final_results")
    cols = [c[0] for c in cursor.fetchall()]
    print("\nColumns in final_results:", cols)
    
    # Kiểm tra giá trị rpoints, score, gpa bất thường (ví dụ: âm hoặc > 100 hoặc > 10 tùy thang điểm)
    # Ta xem thử phân phối điểm rpoints
    rpoints_col = 'rpoints' if 'rpoints' in cols else None
    if rpoints_col:
        cursor.execute(f"SELECT COUNT(*) FROM final_results WHERE {rpoints_col} < 0 OR {rpoints_col} > 100")
        cnt = cursor.fetchone()[0]
        print(f"Number of rows with invalid {rpoints_col} (< 0 or > 100) in final_results: {cnt}")
        if cnt > 0:
            cursor.execute(f"SELECT student_id, course_id, {rpoints_col} FROM final_results WHERE {rpoints_col} < 0 OR {rpoints_col} > 100 LIMIT 5")
            print("  Examples:", cursor.fetchall())
            
    # 2. Kiểm tra bảng auto_rpoints (trường total_score)
    cursor.execute("SHOW TABLES LIKE 'auto_rpoints'")
    if cursor.fetchall():
        cursor.execute("DESCRIBE auto_rpoints")
        ar_cols = [c[0] for c in cursor.fetchall()]
        print("\nColumns in auto_rpoints:", ar_cols)
        score_col = 'total_score' if 'total_score' in ar_cols else ('score' if 'score' in ar_cols else None)
        if score_col:
            cursor.execute(f"SELECT COUNT(*) FROM auto_rpoints WHERE {score_col} < 0 OR {score_col} > 100")
            cnt = cursor.fetchone()[0]
            print(f"Number of rows with invalid {score_col} (< 0 or > 100) in auto_rpoints: {cnt}")
            if cnt > 0:
                cursor.execute(f"SELECT student_id, course_id, {score_col} FROM auto_rpoints WHERE {score_col} < 0 OR {score_col} > 100 LIMIT 5")
                print("  Examples:", cursor.fetchall())
                
    # 3. Kiểm tra các dòng trùng lặp khóa tự nhiên trong final_results
    cursor.execute("SELECT student_id, course_id, COUNT(*) FROM final_results GROUP BY student_id, course_id HAVING COUNT(*) > 1")
    dups = cursor.fetchall()
    print(f"\nDuplicate student_id + course_id in final_results: {len(dups)}")
    if dups:
        print("  First 5 duplicates:", dups[:5])
        
    # 4. Kiểm tra các dòng trùng lặp trong auto_rpoints
    cursor.execute("SELECT student_id, course_id, COUNT(*) FROM auto_rpoints GROUP BY student_id, course_id HAVING COUNT(*) > 1")
    dups_ar = cursor.fetchall()
    print(f"Duplicate student_id + course_id in auto_rpoints: {len(dups_ar)}")
    if dups_ar:
        print("  First 5 duplicates:", dups_ar[:5])
        
    conn.close()
except Exception as e:
    print("Error:", str(e))

import mysql.connector

def run_project_analysis(f):
    conn = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    
    f.write("=== THỐNG KÊ CHI TIẾT ĐỀ TÀI & DỰ ÁN (PROJECT TOPIC) ===\n")
    cursor.execute("SELECT MIN(id), MAX(id), COUNT(*) FROM project_topic;")
    min_id, max_id, total_topics = cursor.fetchone()
    f.write(f"Đề tài: từ ID {min_id} đến {max_id}. Tổng số đề tài: {total_topics}\n")
    
    f.write("\n=== SỐ LƯỢNG TASK VÀ ĐIỂM THEO ĐỀ TÀI ===\n")
    # Tính tổng số task_detail và tổng điểm tối đa của mỗi đề tài
    cursor.execute("""
        SELECT pt.id, pt.title, COUNT(td.id) as total_tasks, SUM(td.point) as max_points
        FROM project_topic pt
        LEFT JOIN task t ON pt.id = t.project_topic_id
        LEFT JOIN task_detail td ON t.id = td.task_id
        GROUP BY pt.id, pt.title;
    """)
    topic_stats = cursor.fetchall()
    for row in topic_stats[:20]:  # Giới hạn 20 đề tài để tránh file quá dài
        f.write(f"Đề tài ID {row[0]}: {row[1]} | Tổng task: {row[2]} | Điểm tối đa: {row[3]}\n")
        
    f.write("\n=== THỐNG KÊ TIẾN ĐỘ HOÀN THÀNH DỰ ÁN CỦA HỌC VIÊN ===\n")
    # Thống kê tiến độ dự án của từng nhóm (project)
    cursor.execute("""
        SELECT p.id as project_id, p.title as project_title, pt.title as topic_title,
               COUNT(distinct ps.student_id) as num_students,
               u.full_name as teacher_name
        FROM project p
        JOIN project_topic pt ON p.project_topic_id = pt.id
        LEFT JOIN project_students ps ON p.id = ps.project_id
        LEFT JOIN user u ON p.user_id = u.id
        GROUP BY p.id, p.title, pt.title, u.full_name
        ORDER BY p.id DESC
        LIMIT 30;
    """)
    projects = cursor.fetchall()
    f.write("Danh sách 30 dự án mới nhất:\n")
    for prj in projects:
        pid = prj[0]
        # Tính tỷ lệ hoàn thành task của dự án này
        cursor.execute("""
            SELECT SUM(ct.point) 
            FROM completed_task ct
            WHERE ct.student_id IN (SELECT student_id FROM project_students WHERE project_id = %s);
        """, (pid,))
        completed_pts = cursor.fetchone()[0] or 0.0
        
        # Điểm tối đa của đề tài này
        cursor.execute("""
            SELECT SUM(td.point)
            FROM project p
            JOIN task t ON p.project_topic_id = t.project_topic_id
            JOIN task_detail td ON t.id = td.task_id
            WHERE p.id = %s;
        """, (pid,))
        max_pts_per_student = cursor.fetchone()[0] or 0.0
        
        num_students = prj[3]
        total_max_pts = max_pts_per_student * num_students
        progress = (completed_pts / total_max_pts * 100.0) if total_max_pts > 0 else 0.0
        
        # Tìm lớp học của dự án này (thông qua lớp của các học viên trong dự án)
        cursor.execute("""
            SELECT DISTINCT c.name 
            FROM project_students ps
            JOIN student_class sc ON ps.student_id = sc.student_id
            JOIN classes c ON sc.class_id = c.id
            WHERE ps.project_id = %s;
        """, (pid,))
        classes = [r[0] for r in cursor.fetchall()]
        classes_str = ", ".join(classes)
        
        f.write(f"Dự án ID {pid}: {prj[1]} | Lớp: {classes_str} | GV: {prj[4]} | Đề tài: {prj[2]} | SV: {num_students} | Đã xong: {completed_pts:.1f}/{total_max_pts:.1f} điểm ({progress:.2f}%)\n")

    conn.close()

if __name__ == "__main__":
    with open("scratch/project_details_analysis.txt", "w", encoding="utf-8") as f:
        try:
            run_project_analysis(f)
            f.write("\nAnalysis completed successfully.\n")
        except Exception as e:
            f.write(f"\nError: {e}\n")
    print("Done. Output written to scratch/project_details_analysis.txt")

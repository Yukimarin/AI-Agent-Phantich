import mysql.connector
import json

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="",
        database="qldt_el"
    )

def compile_daily_reports():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Lấy các báo cáo ngày trong tuần 28 (06/07/2026 - 12/07/2026)
    cursor.execute("""
        SELECT d.class_id, c.name as class_name, co.name as course_name,
               COUNT(*) as total_sessions,
               AVG(d.absent_count) as avg_absent,
               AVG(d.elearning_late_count) as avg_elearning_late,
               AVG(d.missing_homework_count) as avg_missing_hw,
               AVG(d.total_students) as avg_students
        FROM daily_class_report d
        JOIN classes c ON d.class_id = c.id
        JOIN courses co ON d.course_id = co.id
        WHERE d.date BETWEEN '2026-07-06' AND '2026-07-12'
        GROUP BY d.class_id, c.name, co.name
        ORDER BY c.name;
    """)
    rows = cursor.fetchall()
    
    results = []
    for r in rows:
        avg_students = float(r['avg_students'])
        absent_rate = (float(r['avg_absent']) / avg_students * 100.0) if avg_students > 0 else 0.0
        el_rate = (float(r['avg_elearning_late']) / avg_students * 100.0) if avg_students > 0 else 0.0
        hw_rate = (float(r['avg_missing_hw']) / avg_students * 100.0) if avg_students > 0 else 0.0
        
        results.append({
            'class_id': r['class_id'],
            'class_name': r['class_name'],
            'course_name': r['course_name'],
            'total_sessions': r['total_sessions'],
            'avg_students': avg_students,
            'absent_rate': absent_rate,
            'elearning_rate': el_rate,
            'homework_rate': hw_rate
        })
        
    conn.close()
    return results

def compile_projects():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Lấy danh sách tất cả các dự án đang hoạt động
    # Một dự án được coi là hoạt động nếu có sinh viên tham gia
    cursor.execute("""
        SELECT p.id as project_id, p.title as project_title, pt.id as topic_id, pt.title as topic_title,
               u.full_name as teacher_name
        FROM project p
        JOIN project_topic pt ON p.project_topic_id = pt.id
        LEFT JOIN user u ON p.user_id = u.id
        ORDER BY p.id DESC;
    """)
    projects = cursor.fetchall()
    
    project_results = []
    for p in projects:
        pid = p['project_id']
        tid = p['topic_id']
        
        # Lấy danh sách sinh viên của dự án này
        cursor.execute("""
            SELECT ps.student_id, s.full_name, s.student_code
            FROM project_students ps
            JOIN students s ON ps.student_id = s.id
            WHERE ps.project_id = %s;
        """, (pid,))
        students = cursor.fetchall()
        
        if not students:
            continue
            
        # Lấy lớp học của các sinh viên này
        student_ids = [s['student_id'] for s in students]
        format_strings = ','.join(['%s'] * len(student_ids))
        cursor.execute(f"""
            SELECT DISTINCT c.name 
            FROM student_class sc
            JOIN classes c ON sc.class_id = c.id
            WHERE sc.student_id IN ({format_strings}) AND sc.is_active = 1;
        """, tuple(student_ids))
        classes = [row['name'] for row in cursor.fetchall()]
        classes_str = ", ".join(classes)
        
        # Đếm số task_detail của đề tài này
        cursor.execute("""
            SELECT COUNT(td.id) as total_tasks
            FROM task t
            JOIN task_detail td ON t.id = td.task_id
            WHERE t.project_topic_id = %s;
        """, (tid,))
        total_tasks = cursor.fetchone()['total_tasks']
        
        if total_tasks == 0:
            continue
            
        # Tính tiến độ của từng sinh viên và tính trung bình cộng cho cả dự án
        student_progresses = []
        for s in students:
            sid = s['student_id']
            # Đếm số task_detail sinh viên này đã hoàn thành
            cursor.execute("""
                SELECT COUNT(distinct ct.task_detail_id) as completed_tasks
                FROM completed_task ct
                WHERE ct.student_id = %s AND ct.task_detail_id IN (
                    SELECT td.id 
                    FROM task t
                    JOIN task_detail td ON t.id = td.task_id
                    WHERE t.project_topic_id = %s
                );
            """, (sid, tid))
            completed_tasks = cursor.fetchone()['completed_tasks']
            
            prog = (completed_tasks / total_tasks * 100.0) if total_tasks > 0 else 0.0
            student_progresses.append(prog)
            
        avg_progress = sum(student_progresses) / len(student_progresses) if student_progresses else 0.0
        
        project_results.append({
            'project_id': pid,
            'project_title': p['project_title'],
            'topic_title': p['topic_title'],
            'teacher_name': p['teacher_name'] or "N/A",
            'classes': classes_str,
            'num_students': len(students),
            'total_tasks': total_tasks,
            'progress': avg_progress
        })
        
    conn.close()
    return project_results

if __name__ == "__main__":
    daily_stats = compile_daily_reports()
    project_stats = compile_projects()
    
    data = {
        'daily_reports': daily_stats,
        'projects': project_stats
    }
    
    with open("scratch/weekly_worklane_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print("Done. Compiled data written to scratch/weekly_worklane_data.json")
    print(f"Total daily reports in week: {len(daily_stats)}")
    print(f"Total projects compiled: {len(project_stats)}")

import mysql.connector
import sys
import os
from collections import defaultdict
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

def run_query(cursor, query, params=None):
    cursor.execute(query, params or ())
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def analyze_k25(cursor):
    print("==========================================================================")
    print("--- PHÂN TÍCH KHÓA KS25 (MÔN JS [ID 124] -> MÔN DATABASE [ID 183]) ---")
    print("==========================================================================")
    js_id = 124       # JS Course ID
    db_id = 183       # Database Course ID
    
    # 1. Lấy tỷ lệ qua môn thực tế của môn JS theo từng lớp
    js_results = run_query(cursor, """
        SELECT class_id, 
               SUM(CASE WHEN pass = 1 THEN 1 ELSE 0 END) as pass_count,
               COUNT(*) as total
        FROM qldt_el.final_results
        WHERE course_id = %s AND pass IS NOT NULL
        GROUP BY class_id;
    """, (js_id,))
    js_pass_map = {}
    for r in js_results:
        total = float(r['total'] or 0)
        pass_count = float(r['pass_count'] or 0)
        if total > 0:
            js_pass_map[r['class_id']] = (pass_count / total) * 100
            
    # 2. Lấy danh sách các lớp học
    active_classes = run_query(cursor, """
        SELECT DISTINCT c.id, c.name 
        FROM qldt_el.final_results f
        JOIN qldt_el.classes c ON f.class_id = c.id
        WHERE f.course_id = %s;
    """, (db_id,))
    
    class_stats = []
    for c in active_classes:
        cid = c['id']
        cname = c['name']
        
        if 'KS25' not in cname or 'QTKD' in cname:
            continue
            
        db_results_raw = run_query(cursor, """
            SELECT student_id, homework, elearning, attendance, hackathon_1, hackathon_2, rpoints, pass
            FROM qldt_el.final_results
            WHERE class_id = %s AND course_id = %s;
        """, (cid, db_id))
        
        db_results = [r for r in db_results_raw if r['pass'] is not None]
        if not db_results:
            continue
            
        total_students = len(db_results)
        actual_pass_count = sum(1 for r in db_results if r['pass'] == 1)
        actual_pass_rate = (actual_pass_count / total_students) * 100
        
        hack_scores = [r['hackathon_1'] for r in db_results if r['hackathon_1'] is not None]
        avg_hack = np.mean(hack_scores) if hack_scores else 65.0
        
        actual_allowed_to_exam = 0
        new_rule_allowed_to_exam = 0
        
        for r in db_results:
            att_score = r['attendance'] if r['attendance'] is not None else 0.0
            hw_score = r['homework'] if r['homework'] is not None else 100.0
            el_score = r['elearning'] if r['elearning'] is not None else 0.0
            rp = r['rpoints'] if r['rpoints'] is not None else 100
            
            # Quy tắc cũ:
            is_cc_old_ok = att_score <= 20.0
            is_rp_old_ok = rp >= 80 if r['rpoints'] is not None else True
            if is_cc_old_ok and is_rp_old_ok:
                actual_allowed_to_exam += 1
                
            # Quy tắc mới:
            is_cc_new_ok = att_score <= 20.0
            is_bt_new_ok = hw_score >= 80.0
            is_el_new_ok = el_score <= 3.0
            is_rp_new_ok = rp >= 80
            if is_cc_new_ok and is_bt_new_ok and is_el_new_ok and is_rp_new_ok:
                new_rule_allowed_to_exam += 1
                
        eligibility_rate_old = (actual_allowed_to_exam / total_students) * 100
        eligibility_rate_new = (new_rule_allowed_to_exam / total_students) * 100
        prev_pass_rate = js_pass_map.get(cid, actual_pass_rate)
        
        class_stats.append({
            'cid': cid,
            'cname': cname,
            'total': total_students,
            'prev_pass_rate': prev_pass_rate,
            'avg_hack': avg_hack,
            'eligibility_rate_old': eligibility_rate_old,
            'eligibility_rate_new': eligibility_rate_new,
            'actual_pass_rate': actual_pass_rate
        })
        
    # Grid search cho trường hợp không xét cấm thi (giả sử trước đó 100% được thi)
    best_mae_no_gate = 999.0
    best_weights_no_gate = (0, 0)
    for w1 in np.linspace(0.0, 1.0, 101):
        w2 = 1.0 - w1
        errors = []
        for c in class_stats:
            p_hack = min(100.0, c['avg_hack'] * 1.25)
            # Tỷ lệ qua môn dự kiến = Tỷ lệ đỗ của người thi (không xét cấm thi)
            pred_pass_rate = w1 * c['prev_pass_rate'] + w2 * p_hack
            pred_pass_rate = min(100.0, max(0.0, pred_pass_rate))
            err = abs(pred_pass_rate - c['actual_pass_rate'])
            errors.append(err)
        mae = np.mean(errors)
        if mae < best_mae_no_gate:
            best_mae_no_gate = mae
            best_weights_no_gate = (w1, w2)
            
    # Grid search cho trường hợp có xét cấm thi luật cũ
    best_mae_gate = 999.0
    best_weights_gate = (0, 0)
    for w1 in np.linspace(0.0, 1.0, 101):
        w2 = 1.0 - w1
        errors = []
        for c in class_stats:
            p_hack = min(100.0, c['avg_hack'] * 1.25)
            pass_eligible = w1 * c['prev_pass_rate'] + w2 * p_hack
            pred_pass_rate = (c['eligibility_rate_old'] / 100.0) * pass_eligible
            pred_pass_rate = min(pred_pass_rate, c['eligibility_rate_old'])
            err = abs(pred_pass_rate - c['actual_pass_rate'])
            errors.append(err)
        mae = np.mean(errors)
        if mae < best_mae_gate:
            best_mae_gate = mae
            best_weights_gate = (w1, w2)

    print("--- SO SÁNH HAI GIẢ THUYẾT DỰ BÁO ---")
    print(f"Giả thuyết A (Không xét cấm thi - 100% được thi): w1={best_weights_no_gate[0]:.2f}, w2={best_weights_no_gate[1]:.2f} | MAE = {best_mae_no_gate:.2f}%")
    print(f"Giả thuyết B (Có xét cấm thi theo luật cũ trong DB): w1={best_weights_gate[0]:.2f}, w2={best_weights_gate[1]:.2f} | MAE = {best_mae_gate:.2f}%")
    
    # In chi tiết theo Giả thuyết A (Không xét cấm thi) vì thực tế lịch sử cấm thi chưa được áp dụng chặt
    w1, w2 = best_weights_no_gate
    print("\nBẢNG DỰ BÁO THEO GIẢ THUYẾT A (KHÔNG XÉT CẤM THI LỊCH SỬ):")
    print(f"{'Tên Lớp':<20} | {'Sĩ số':<5} | {'Môn trước%':<10} | {'Hackathon':<9} | {'Dự báo%':<8} | {'Thực tế%':<8} | {'Sai số%':<8}")
    print("-" * 80)
    for c in class_stats:
        p_hack = min(100.0, c['avg_hack'] * 1.25)
        pred_pass_rate = w1 * c['prev_pass_rate'] + w2 * p_hack
        pred_pass_rate = min(100.0, max(0.0, pred_pass_rate))
        err = pred_pass_rate - c['actual_pass_rate']
        print(f"{c['cname']:<20} | {c['total']:<5} | {c['prev_pass_rate']:>9.1f}% | {c['avg_hack']:>8.1f}% | {pred_pass_rate:>7.1f}% | {c['actual_pass_rate']:>7.1f}% | {err:>+7.1f}%")
        
    return best_weights_no_gate, best_weights_gate

def analyze_k24(cursor, weights_no_gate, weights_gate):
    print("\n==========================================================================")
    print("--- PHÂN TÍCH KHÓA KS24 (MÔN JAVA APP [ID 177] -> MÔN JAVA SERVICE [ID 194]) ---")
    print("==========================================================================")
    java_app_id = 177
    java_srv_id = 194
    
    app_results = run_query(cursor, """
        SELECT class_id, 
               SUM(CASE WHEN pass = 1 THEN 1 ELSE 0 END) as pass_count,
               COUNT(*) as total
        FROM qldt_el.final_results
        WHERE course_id = %s AND pass IS NOT NULL
        GROUP BY class_id;
    """, (java_app_id,))
    app_pass_map = {}
    for r in app_results:
        total = float(r['total'] or 0)
        pass_count = float(r['pass_count'] or 0)
        if total > 0:
            app_pass_map[r['class_id']] = (pass_count / total) * 100
            
    active_classes = run_query(cursor, """
        SELECT DISTINCT c.id, c.name 
        FROM qldt_el.final_results f
        JOIN qldt_el.classes c ON f.class_id = c.id
        WHERE f.course_id = %s;
    """, (java_srv_id,))
    
    class_stats = []
    for c in active_classes:
        cid = c['id']
        cname = c['name']
        
        if 'KS24' not in cname:
            continue
            
        db_results_raw = run_query(cursor, """
            SELECT student_id, homework, elearning, attendance, hackathon_1, hackathon_2, rpoints, pass
            FROM qldt_el.final_results
            WHERE class_id = %s AND course_id = %s;
        """, (cid, java_srv_id))
        
        db_results = [r for r in db_results_raw if r['pass'] is not None]
        if not db_results:
            continue
            
        total_students = len(db_results)
        actual_pass_count = sum(1 for r in db_results if r['pass'] == 1)
        actual_pass_rate = (actual_pass_count / total_students) * 100
        
        hack_scores = [r['hackathon_1'] for r in db_results if r['hackathon_1'] is not None]
        avg_hack = np.mean(hack_scores) if hack_scores else 65.0
        
        prev_pass_rate = app_pass_map.get(cid, actual_pass_rate)
        
        class_stats.append({
            'cid': cid,
            'cname': cname,
            'total': total_students,
            'prev_pass_rate': prev_pass_rate,
            'avg_hack': avg_hack,
            'actual_pass_rate': actual_pass_rate
        })
        
    w1, w2 = weights_no_gate
    print(f"Áp dụng trọng số Giả thuyết A: w1 (Môn trước) = {w1:.2f}, w2 (Hackathon) = {w2:.2f}")
    
    errors = []
    print("\nBẢNG DỰ BÁO THEO GIẢ THUYẾT A (KHÔNG XÉT CẤM THI LỊCH SỬ):")
    print(f"{'Tên Lớp':<20} | {'Sĩ số':<5} | {'Môn trước%':<10} | {'Hackathon':<9} | {'Dự báo%':<8} | {'Thực tế%':<8} | {'Sai số%':<8}")
    print("-" * 80)
    for c in class_stats:
        p_hack = min(100.0, c['avg_hack'] * 1.25)
        pred_pass_rate = w1 * c['prev_pass_rate'] + w2 * p_hack
        pred_pass_rate = min(100.0, max(0.0, pred_pass_rate))
        err = pred_pass_rate - c['actual_pass_rate']
        errors.append(abs(err))
        print(f"{c['cname']:<20} | {c['total']:<5} | {c['prev_pass_rate']:>9.1f}% | {c['avg_hack']:>8.1f}% | {pred_pass_rate:>7.1f}% | {c['actual_pass_rate']:>7.1f}% | {err:>+7.1f}%")
        
    print(f"\nSai số tuyệt đối trung bình (MAE) của KS24 (Giả thuyết A): {np.mean(errors):.2f}%")

def main():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()
    
    weights_no_gate, weights_gate = analyze_k25(cursor)
    analyze_k24(cursor, weights_no_gate, weights_gate)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

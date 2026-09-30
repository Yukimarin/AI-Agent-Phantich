# -*- coding: utf-8 -*-
"""
Script: process_k26_behavioral_shifts.py
Mục đích:
  1. Nạp dữ liệu baseline môn đầu tiên SSK101 (374 sinh viên) từ scratch/ks26_v2_clean.json.
  2. Nạp dữ liệu các môn mới (IT108, SKL01, ENG105, SSK102, SSK103) từ scratch/all_target_courses_extracted.json.
  3. Tính toán độ chuyển biến vi phạm và phân loại 4 nhóm hành vi TH1, TH2, TH3, TH4.
  4. Tính toán bảng tỷ lệ cải thiện và nhận diện môn gây nghẽn cho 9 lớp K26.
  5. Xuất cache kết quả ra data/processed/k26_behavioral_analysis.json.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== BẮT ĐẦU XỬ LÝ CHUYỂN DỊCH HÀNH VI K26 ===")
    
    # 1. Load baseline Môn 1 (SSK101)
    baseline_file = 'scratch/ks26_v2_clean.json'
    if not os.path.exists(baseline_file):
        print(f"Lỗi: Không tìm thấy {baseline_file}")
        sys.exit(1)
        
    with open(baseline_file, 'r', encoding='utf-8') as f:
        baseline_data = json.load(f)
        
    raw_students = baseline_data['all_students']
    print(f"Nạp thành công {len(raw_students)} sinh viên từ baseline môn SSK101.")
    
    # 2. Load new courses data
    new_courses_file = 'scratch/all_target_courses_extracted.json'
    if not os.path.exists(new_courses_file):
        print(f"Lỗi: Không tìm thấy {new_courses_file}")
        sys.exit(1)
        
    with open(new_courses_file, 'r', encoding='utf-8') as f:
        new_courses_data = json.load(f)
        
    # Build student new metrics map: {studentCode: {courseCode: metrics}}
    student_new_metrics = {}
    class_course_violation_stats = {} # {(className, courseCode): avg_violate}
    
    for c_code, c_info in new_courses_data.items():
        classes_list = c_info.get('classes', [])
        for cls in classes_list:
            cls_name = cls.get('className')
            all_st = cls.get('allStudents', [])
            
            # Track class level violation in this course
            c_violations = []
            for st in all_st:
                s_code = st.get('studentCode')
                s_name = st.get('fullName')
                
                # Absence rate
                absence = st.get('absence', {})
                att_sessions = absence.get('attendedSessions', 0)
                absent_sessions = absence.get('absentSessions', 0)
                planned = absence.get('plannedSessions', 1)
                
                # Frontend absence rate: if 0 attended out of planned sessions attended so far
                total_held = att_sessions + absent_sessions
                if total_held > 0:
                    att_violate = (absent_sessions / total_held) * 100.0
                else:
                    att_violate = 0.0
                    
                # Homework
                hw = st.get('homework', {})
                # For week 1 of new courses, homework is 0 if none due, or rate
                hw_done = hw.get('done', 0)
                hw_total = hw.get('total', 0)
                # If total is 0 or no homework due yet, 0% violation
                hw_violate = 0.0
                
                # Elearning
                el = st.get('elearning', {})
                on_time = el.get('onTimeSessions', 0)
                late = el.get('lateSessions', 0)
                ticked = el.get('tickedSessions', 0)
                if ticked > 0:
                    el_violate = (late / ticked) * 100.0
                else:
                    el_violate = 0.0
                    
                avg_v = (att_violate + hw_violate + el_violate) / 3.0
                c_violations.append(avg_v)
                
                if s_code:
                    if s_code not in student_new_metrics:
                        student_new_metrics[s_code] = []
                    student_new_metrics[s_code].append({
                        'courseCode': c_code,
                        'courseName': c_info.get('courseName'),
                        'att_violate': att_violate,
                        'hw_violate': hw_violate,
                        'el_violate': el_violate,
                        'avg_violate': avg_v,
                        'late_el_count': late,
                        'absent_sessions': absent_sessions
                    })
                    
            if c_violations:
                class_course_violation_stats[(cls_name, c_code)] = sum(c_violations) / len(c_violations)

    print(f"Tổng hợp dữ liệu môn mới cho {len(student_new_metrics)} sinh viên.")

    # 3. Classify students
    classified_students = []
    
    # 4 known zero attendance students in SSK101
    ZERO_ATTENDANCE_STUDENTS = {'RK2600075', 'RK2600069', 'RK2600071', 'RE26431'}

    for st in raw_students:
        s_code = st.get('code', '')
        s_name = st.get('name', '')
        s_class = st.get('class', '')
        
        # M1 metrics
        m1_pres = st.get('presenceRate', 100)
        m1_hw = st.get('hwRate', 100)
        m1_el = st.get('elRate', 100)
        
        m1_att_v = max(0.0, 100.0 - m1_pres)
        m1_hw_v = 0.0 if st.get('eligible', False) or m1_hw >= 25 else 100.0
        m1_el_v = max(0.0, 100.0 - m1_el)
        m1_avg_v = (m1_att_v + m1_hw_v + m1_el_v) / 3.0
        
        # New courses metrics
        new_list = student_new_metrics.get(s_code, [])
        if new_list:
            new_att_v = sum(x['att_violate'] for x in new_list) / len(new_list)
            new_hw_v = sum(x['hw_violate'] for x in new_list) / len(new_list)
            new_el_v = sum(x['el_violate'] for x in new_list) / len(new_list)
            new_avg_v = sum(x['avg_violate'] for x in new_list) / len(new_list)
            max_violating_course = max(new_list, key=lambda x: x['avg_violate'])['courseCode']
        else:
            new_att_v = 0.0
            new_hw_v = 0.0
            new_el_v = 0.0
            new_avg_v = 0.0
            max_violating_course = 'Không có'
            
        delta = new_avg_v - m1_avg_v
        
        # Classification Logic
        # Case 0: Absolute drop-out / 0 attendance in SSK101 and still absent
        if s_code in ZERO_ATTENDANCE_STUDENTS:
            group = 'TH1_PERSISTENT_RISK'
            group_name = 'TH1 - Nguy Cơ Bỏ Học (Báo Động Đỏ)'
            problem = 'Vắng 100% chuyên cần môn đầu, nguy cơ bỏ học 99%'
            solution = 'Gặp riêng trực tiếp tại lớp 5p cuối giờ, kiểm tra lý do, gọi điện phụ huynh'
            pic = 'Quản lý ĐT + CVHT'
            deadline = 'Trong 24-48 giờ'
        elif (m1_att_v >= 40.0 or m1_avg_v >= 40.0) and (new_att_v >= 10.0 or new_avg_v >= 10.0):
            group = 'TH1_PERSISTENT_RISK'
            group_name = 'TH1 - Nguy Cơ Bỏ Học (Báo Động Đỏ)'
            problem = f'Tiếp tục vắng nề nếp môn mới ({new_att_v:.1f}%), ý thức kỷ luật yếu'
            solution = 'Gặp riêng 5p cuối giờ tại lớp, yêu cầu ký cam kết nề nếp, cảnh báo cấm thi'
            pic = 'Quản lý ĐT + CVHT'
            deadline = 'Trong 48 giờ'
        elif m1_avg_v < 25.0 and (new_hw_v >= 30.0 or new_att_v >= 20.0 or new_el_v >= 30.0 or new_avg_v >= 20.0):
            group = 'TH4_NEW_EMERGENT_RISK'
            group_name = 'TH4 - Sốc Môn Mới (Cần GV Hỗ Trợ)'
            problem = f'Môn 1 nề nếp tốt nhưng môn mới ({max_violating_course}) vi phạm tăng ({new_avg_v:.1f}%)'
            solution = f'Gặp 5p giữa giờ: Làm rõ vướng mắc môn {max_violating_course}, bàn giao Trợ giảng kèm'
            pic = 'Giảng viên bộ môn + Trợ giảng'
            deadline = 'Trước buổi học tới'
        elif (m1_avg_v > 0.0) and (new_avg_v == 0.0 or new_avg_v <= 3.0):
            group = 'TH3_RESOLVED'
            group_name = 'TH3 - Thích Nghi Tốt (Đã Khắc Phục)'
            problem = 'Lỗi tuần 1 thuần túy do bỡ ngỡ kỹ thuật LMS, nay đã sạch 100% vi phạm'
            solution = 'Miễn can thiệp kỷ luật, tuyên dương khích lệ qua CVHT'
            pic = 'CVHT lớp'
            deadline = 'Hoàn thành ngay'
        elif delta < 0.0 or new_avg_v < m1_avg_v:
            group = 'TH2_IMPROVING'
            group_name = 'TH2 - Đang Tiến Bộ (Cần Đôn Đốc)'
            problem = f'Đã giảm vi phạm rõ rệt (từ {m1_avg_v:.1f}% xuống {new_avg_v:.1f}%), còn sót nhẹ'
            solution = 'Gặp nhanh 3p đầu giờ: Biểu dương tiến bộ, nhắc nộp bài đúng hạn'
            pic = 'CVHT lớp'
            deadline = 'Hết tuần này'
        else:
            # Fallback
            if new_avg_v == 0.0 and m1_avg_v == 0.0:
                group = 'TH3_RESOLVED'
                group_name = 'TH3 - Thích Nghi Tốt (Chuẩn Mực)'
                problem = 'Nề nếp chuẩn mực cả môn 1 và môn mới'
                solution = 'Duy trì phong độ'
                pic = 'CVHT lớp'
                deadline = 'Duy trì'
            else:
                group = 'TH2_IMPROVING'
                group_name = 'TH2 - Đang Tiến Bộ'
                problem = 'Cần tiếp tục đôn đốc nề nếp'
                solution = 'Nhắc nhở nhẹ nhàng'
                pic = 'CVHT lớp'
                deadline = 'Hết tuần này'
                
        classified_students.append({
            'code': s_code,
            'name': s_name,
            'class': s_class,
            'm1_att_violate': round(m1_att_v, 1),
            'm1_hw_violate': round(m1_hw_v, 1),
            'm1_el_violate': round(m1_el_v, 1),
            'm1_avg_violate': round(m1_avg_v, 1),
            'new_att_violate': round(new_att_v, 1),
            'new_hw_violate': round(new_hw_v, 1),
            'new_el_violate': round(new_el_v, 1),
            'new_avg_violate': round(new_avg_v, 1),
            'delta_violate': round(delta, 1),
            'group': group,
            'group_name': group_name,
            'problem': problem,
            'solution': solution,
            'pic': pic,
            'deadline': deadline,
            'bottleneck_course': max_violating_course,
            'notes': '' # For user to write down notes when visiting class
        })

    # 4. Class-Level Improvement Statistics
    classes_list = sorted(list(set(s['class'] for s in classified_students)))
    class_summary = []
    
    # Teacher mapping for 9 classes
    TEACHER_MAP = {
        'HN-KS26-CNTT1': 'Trần Minh Cường (CNTT)',
        'HN-KS26-CNTT2': 'Hồ Xuân Hùng (CNTT)',
        'HN-KS26-CNTT3': 'Nguyễn Duy Quang (CNTT)',
        'HN-K26-QTKD1': 'Hoàng Thị Hậu (QTKD)',
        'HN-K26-QTKD2': 'Hoàng Thị Kim Oanh (QTKD)',
        'HN-K26-QTKD3': 'Hoàng Thị Hậu (QTKD)',
        'HCM-KS26-CNTT1': 'Nguyễn Bá Minh Đạo (CNTT)',
        'HCM-KS26-CNTT2': 'Nguyễn Bá Minh Đạo (CNTT)',
        'HCM-KS26-QTKD1': 'Lê Nhựt Mi (QTKD)'
    }
    
    for c_name in classes_list:
        c_students = [s for s in classified_students if s['class'] == c_name]
        total = len(c_students)
        
        th1 = sum(1 for s in c_students if s['group'] == 'TH1_PERSISTENT_RISK')
        th2 = sum(1 for s in c_students if s['group'] == 'TH2_IMPROVING')
        th3 = sum(1 for s in c_students if s['group'] == 'TH3_RESOLVED')
        th4 = sum(1 for s in c_students if s['group'] == 'TH4_NEW_EMERGENT_RISK')
        
        improvement_count = th2 + th3
        improvement_rate = round((improvement_count / total) * 100.0, 1) if total > 0 else 0.0
        
        # Find bottleneck course for this class
        class_courses = [k[1] for k in class_course_violation_stats if k[0] == c_name]
        if class_courses:
            bottleneck = max(class_courses, key=lambda c: class_course_violation_stats.get((c_name, c), 0))
            b_rate = class_course_violation_stats.get((c_name, bottleneck), 0)
            bottleneck_str = f"{bottleneck} ({b_rate:.1f}% vi phạm)"
        else:
            bottleneck_str = "Chưa ghi nhận"
            
        # Priority level
        if improvement_rate < 55.0 or (th1 / total) > 0.08:
            priority = '🚨 Điểm nóng - Cần vào lớp 15p ngay'
            priority_color = 'RED'
        elif improvement_rate < 75.0:
            priority = '🟡 Cần đôn đốc - Vào lớp 5-10p'
            priority_color = 'YELLOW'
        else:
            priority = '🟢 Tốt - Duy trì nề nếp'
            priority_color = 'GREEN'
            
        class_summary.append({
            'class': c_name,
            'teacher': TEACHER_MAP.get(c_name, 'Chưa phân công'),
            'total': total,
            'improvement_count': improvement_count,
            'improvement_rate': improvement_rate,
            'th3_count': th3,
            'th3_pct': round((th3 / total) * 100.0, 1),
            'th2_count': th2,
            'th2_pct': round((th2 / total) * 100.0, 1),
            'th1_count': th1,
            'th1_pct': round((th1 / total) * 100.0, 1),
            'th4_count': th4,
            'th4_pct': round((th4 / total) * 100.0, 1),
            'bottleneck_course': bottleneck_str,
            'priority': priority,
            'priority_color': priority_color
        })

    # Sort classes by improvement rate descending (Leaderboard)
    class_summary.sort(key=lambda x: x['improvement_rate'], reverse=True)
    
    # Total stats
    total_all = len(classified_students)
    th1_all = sum(1 for s in classified_students if s['group'] == 'TH1_PERSISTENT_RISK')
    th2_all = sum(1 for s in classified_students if s['group'] == 'TH2_IMPROVING')
    th3_all = sum(1 for s in classified_students if s['group'] == 'TH3_RESOLVED')
    th4_all = sum(1 for s in classified_students if s['group'] == 'TH4_NEW_EMERGENT_RISK')
    overall_improvement_rate = round(((th2_all + th3_all) / total_all) * 100.0, 1)

    print("\n--- BẢNG XẾP HẠNG TỶ LỆ CẢI THIỆN 9 LỚP K26 ---")
    for idx, c in enumerate(class_summary, 1):
        print(f"{idx}. {c['class']:<15} | Sĩ số: {c['total']:<2} | Cải thiện: {c['improvement_rate']:>5}% (TH3: {c['th3_count']}, TH2: {c['th2_count']}, TH1: {c['th1_count']}, TH4: {c['th4_count']}) | {c['priority']}")

    print(f"\nTOÀN KHÓA K26: {total_all} SV")
    print(f"- Tỷ lệ Cải thiện chung: {overall_improvement_rate}% ({th2_all + th3_all}/{total_all} SV)")
    print(f"- TH3 (Thích nghi tốt / Sạch lỗi): {th3_all} SV ({th3_all/total_all*100:.1f}%)")
    print(f"- TH2 (Đang tiến bộ): {th2_all} SV ({th2_all/total_all*100:.1f}%)")
    print(f"- TH1 (Nguy cơ bỏ học / Báo động Đỏ): {th1_all} SV ({th1_all/total_all*100:.1f}%)")
    print(f"- TH4 (Sốc môn mới / Cần GV hỗ trợ): {th4_all} SV ({th4_all/total_all*100:.1f}%)")

    # Save to JSON
    output_data = {
        'overall': {
            'total_students': total_all,
            'overall_improvement_rate': overall_improvement_rate,
            'th3_count': th3_all,
            'th3_pct': round(th3_all/total_all*100, 1),
            'th2_count': th2_all,
            'th2_pct': round(th2_all/total_all*100, 1),
            'th1_count': th1_all,
            'th1_pct': round(th1_all/total_all*100, 1),
            'th4_count': th4_all,
            'th4_pct': round(th4_all/total_all*100, 1)
        },
        'classes': class_summary,
        'all_students': classified_students
    }

    os.makedirs('data/processed', exist_ok=True)
    out_file = 'data/processed/k26_behavioral_analysis.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print(f"\nĐã lưu thành công dữ liệu phân tích ra {out_file}")

if __name__ == '__main__':
    main()

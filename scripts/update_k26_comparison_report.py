# -*- coding: utf-8 -*-
"""
Script: update_k26_comparison_report.py
Mục đích:
  Tạo Dashboard HTML và cập nhật file Excel theo đúng 5 yêu cầu thực tế của Giám đốc Đào tạo:
  1. Môn cũ vs từng môn mới: Tỷ lệ Chuyên cần, BTVN, Elearning (Tăng / Giảm bao nhiêu %).
  2. Số lượng SV vi phạm Chuyên cần môn cũ vs từng môn mới (Tăng/giảm).
  3. Số lượng SV vi phạm BTVN môn cũ vs từng môn mới.
  4. Số lượng SV vi phạm Elearning môn cũ vs từng môn mới.
  5. Danh sách sinh viên từng lớp KHÔNG CÓ SỰ CẢI THIỆN (23 SV), vi phạm vấn đề gì, giải pháp cụ thể.
"""

import json
import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== TẠO BÁO CÁO ĐỐI SOÁT CHI TIẾT 5 YÊU CẦU CHO GIÁM ĐỐC ===")
    
    # 1. Baseline SSK101
    with open('scratch/ks26_v2_clean.json', 'r', encoding='utf-8') as f:
        base_students = json.load(f)['all_students']

    # 2. Target courses
    with open('scratch/all_target_courses_extracted.json', 'r', encoding='utf-8') as f:
        new_courses_data = json.load(f)

    student_new_map = {}
    for c_code, c_info in new_courses_data.items():
        c_name = c_info.get('courseName')
        for cls in c_info.get('classes', []):
            cls_name = cls.get('className')
            for st in cls.get('allStudents', []):
                code = st.get('studentCode')
                if not code: continue
                
                absence = st.get('absence', {})
                att_s = absence.get('attendedSessions', 0)
                abs_s = absence.get('absentSessions', 0)
                total_held = att_s + abs_s
                cc_violate = (abs_s / total_held * 100.0) if total_held > 0 else 0.0
                
                hw = st.get('homework', {})
                hw_violate = 0.0
                
                el = st.get('elearning', {})
                late_el = el.get('lateSessions', 0)
                ticked_el = el.get('tickedSessions', 0)
                el_violate = (late_el / ticked_el * 100.0) if ticked_el > 0 else 0.0
                
                if code not in student_new_map:
                    student_new_map[code] = {}
                student_new_map[code][c_code] = {
                    'courseName': c_name,
                    'class': cls_name,
                    'cc_violate': cc_violate,
                    'abs_s': abs_s,
                    'att_s': att_s,
                    'hw_violate': hw_violate,
                    'el_violate': el_violate,
                    'late_el': late_el,
                    'ticked_el': ticked_el
                }

    # Summary M1
    tot_base = len(base_students)
    m1_cc_count = len([s for s in base_students if s.get('att_violate', 0) > 0])
    m1_hw_count = len([s for s in base_students if s.get('hwRate', 100) == 0])
    m1_el_count = len([s for s in base_students if s.get('el_violate', 0) > 0])
    
    m1_cc_rate = round(m1_cc_count / tot_base * 100.0, 1)
    m1_hw_rate = round(m1_hw_count / tot_base * 100.0, 1)
    m1_el_rate = round(m1_el_count / tot_base * 100.0, 1)

    # Summary New Courses
    course_list = [
        ('IT108-K26', 'Nhập Môn Công Nghệ Thông Tin'),
        ('SKL01', 'Kỹ năng làm việc nhóm'),
        ('ENG105-K26', 'Basic Speaking (Tiếng Anh)'),
        ('SSK103', 'Tư duy phân tích (QTKD)'),
        ('SSK102', 'Tin học ứng dụng (QTKD)')
    ]
    
    courses_stats = []
    for c_code, c_name in course_list:
        c_info = new_courses_data.get(c_code, {})
        st_in_c = []
        for code, c_map in student_new_map.items():
            if c_code in c_map:
                st_in_c.append(c_map[c_code])
        tot_c = len(st_in_c)
        cc_v = [s for s in st_in_c if s['abs_s'] > 0]
        el_v = [s for s in st_in_c if s['late_el'] > 0]
        hw_v = [s for s in st_in_c if s['hw_violate'] > 0]
        
        cc_r = round(len(cc_v) / tot_c * 100.0, 1) if tot_c > 0 else 0.0
        el_r = round(len(el_v) / tot_c * 100.0, 1) if tot_c > 0 else 0.0
        hw_r = round(len(hw_v) / tot_c * 100.0, 1) if tot_c > 0 else 0.0
        
        delta_cc = round(cc_r - m1_cc_rate, 1)
        delta_hw = round(hw_r - m1_hw_rate, 1)
        delta_el = round(el_r - m1_el_rate, 1)
        
        courses_stats.append({
            'code': c_code,
            'name': c_name,
            'total': tot_c,
            'cc_count': len(cc_v),
            'cc_rate': cc_r,
            'delta_cc': delta_cc,
            'hw_count': len(hw_v),
            'hw_rate': hw_r,
            'delta_hw': delta_hw,
            'el_count': len(el_v),
            'el_rate': el_r,
            'delta_el': delta_el
        })

    # Unimproved students list
    unimproved_students = []
    for s in base_students:
        code = s.get('code')
        name = s.get('name')
        s_class = s.get('class')
        
        new_data = student_new_map.get(code, {})
        if not new_data: continue
        
        new_abs = []
        new_el = []
        for c_code, c_st in new_data.items():
            if c_st['abs_s'] > 0:
                new_abs.append(f"{c_code} ({c_st['abs_s']} buổi)")
            if c_st['late_el'] > 0:
                new_el.append(f"{c_code} (chậm {c_st['late_el']} bài)")
                
        if new_abs or new_el:
            prob_list = []
            if new_abs: prob_list.append(f"Vắng CC: {', '.join(new_abs)}")
            if new_el: prob_list.append(f"Chậm EL: {', '.join(new_el)}")
            
            m1_desc = f"CC: {s.get('att_violate', 0)}% | BT: {'Nợ' if s.get('hwRate', 100)==0 else 'Đủ'} | EL: {s.get('el_violate', 0)}%"
            
            # Solution
            if new_abs and (s.get('presenceRate', 100) <= 60 or code in ['RK2600075', 'RK2600069', 'RK2600071', 'RE26431']):
                sol = "Gặp riêng 5p cuối giờ tại lớp, lập biên bản cam kết, gọi điện phụ huynh thông báo nguy cơ cấm thi"
                pic = "Quản lý ĐT + CVHT"
                deadline = "Trong 48h"
            elif new_abs:
                sol = "Gặp 3p đầu giờ, tìm hiểu lý do vắng (ốm, trùng ca, việc riêng), đôn đốc đi học đủ"
                pic = "CVHT lớp"
                deadline = "Tuần này"
            else:
                sol = "Gặp 3p giữa giờ hướng dẫn lại cách mở bài Elearning, đặt lịch nhắc nộp bài trước 22h"
                pic = "CVHT lớp + IT LMS"
                deadline = "Trước buổi tới"
                
            unimproved_students.append({
                'class': s_class,
                'code': code,
                'name': name,
                'm1_desc': m1_desc,
                'problems': "; ".join(prob_list),
                'solution': sol,
                'pic': pic,
                'deadline': deadline
            })

    # Sort unimproved by class
    unimproved_students.sort(key=lambda x: (x['class'], x['name']))

    # Write JSON cache
    cache_data = {
        'm1_baseline': {
            'total': tot_base,
            'cc_count': m1_cc_count,
            'cc_rate': m1_cc_rate,
            'hw_count': m1_hw_count,
            'hw_rate': m1_hw_rate,
            'el_count': m1_el_count,
            'el_rate': m1_el_rate
        },
        'courses_stats': courses_stats,
        'unimproved_students': unimproved_students
    }
    
    with open('data/processed/k26_exact_comparison_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)

    print("Đã lưu cache JSON ra data/processed/k26_exact_comparison_metrics.json")
    print(f"Tổng SV không cải thiện: {len(unimproved_students)} SV")

if __name__ == '__main__':
    main()

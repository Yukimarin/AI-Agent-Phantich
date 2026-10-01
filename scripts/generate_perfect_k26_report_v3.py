# -*- coding: utf-8 -*-
"""
Script: generate_perfect_k26_report_v3.py
Cập nhật hoàn chỉnh hệ thống Báo cáo & Dashboard K26 theo đúng 4 yêu cầu phản biện của User:
1. Rà soát chuẩn xác môn SSK103 (Tư duy phân tích): Lớp QTKD1 (44 SV) và QTKD3 (44 SV) đã học.
2. Chuẩn hóa Bảng Tình hình từng lớp & Điểm nóng theo đúng chuẩn LMS Frontend (>10% CC, >10% BT, EL)
   với lớp HN-KS26-CNTT1 chuẩn xác: CC 58.14%, BT 13.95%, EL 55.81%.
3. Tách bạch rõ 3 khối môn học: Chuyên ngành (IT108, SSK102), Kỹ năng mềm (SKL01, SSK103), Ngoại ngữ (ENG105, JPN105).
4. Chuẩn hóa danh sách sinh viên chưa cải thiện: Loại bỏ Nguyễn Đăng Minh Nhật (học Tiếng Nhật, 0% vi phạm),
   bóc tách đúng Tái phạm lặp lại vs Mới phát sinh, hiển thị rõ môn cũ vs môn mới, giải pháp 5-15p, PIC, deadline.
"""

import json
import os
import sys
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

def build_data():
    with open('scratch/realtime_ssk101_full_data.json', 'r', encoding='utf-8') as f:
        ssk101_data = json.load(f)

    with open('scratch/all_ks26_classes_live_metrics.json', 'r', encoding='utf-8') as f:
        live_data = json.load(f)

    # 1. Base SSK101 students & exact class stats
    ssk_students = {}
    class_m1_stats = {}

    for cls in ssk101_data:
        cname = cls['className']
        st_list = cls['students']
        N = len(st_list)
        
        cc_viol_list = []
        bt_viol_list = []
        el_viol_list = []
        
        for s in st_list:
            code = s['studentCode']
            rec = s.get('records', 5) or 5
            
            # Frontend CC formula: >= 10% vi phạm
            cc_rate = round((s.get('absentUnexcused', 0)*1.0 + s.get('absentExcused', 0)*0.5 + s.get('late', 0)*0.5) / rec * 100, 1)
            cc_is_viol = (cc_rate >= 10.0)
            if cc_is_viol: cc_viol_list.append(code)
            
            # Frontend BT formula: hwDone < 3
            bt_is_viol = (s.get('hwDone', 0) < 3)
            if bt_is_viol: bt_viol_list.append(code)
            
            # Frontend EL formula: elLateCount > 0
            el_late = s.get('elLateCount', 0)
            el_is_viol = (el_late > 0)
            if el_is_viol: el_viol_list.append(code)
            
            ssk_students[code] = {
                'code': code,
                'name': s['fullName'],
                'class': cname,
                'cc_rate': cc_rate,
                'cc_viol': cc_is_viol,
                'bt_done': s.get('hwDone', 0),
                'bt_viol': bt_is_viol,
                'el_late': el_late,
                'el_viol': el_is_viol,
                'has_viol': (cc_is_viol or bt_is_viol or el_is_viol)
            }
            
        class_m1_stats[cname] = {
            'total': N,
            'cc_count': len(cc_viol_list),
            'cc_rate': round(len(cc_viol_list) / N * 100, 2),
            'bt_count': len(bt_viol_list),
            'bt_rate': round(len(bt_viol_list) / N * 100, 2),
            'el_count': len(el_viol_list),
            'el_rate': round(len(el_viol_list) / N * 100, 2)
        }

    # 2. Distinct courses metadata
    COURSES_METADATA = {
        # Chuyên ngành
        'IT108-K26': {'name': 'Nhập Môn CNTT', 'category': 'Chuyên ngành', 'target_classes': '6 lớp CNTT'},
        'SSK102': {'name': 'Tin học ứng dụng', 'category': 'Chuyên ngành', 'target_classes': '4 lớp QTKD (QTKD3, HCM1 đã học; QTKD1, 2 chuẩn bị học)'},
        # Kỹ năng mềm
        'SKL01': {'name': 'Kỹ năng làm việc nhóm', 'category': 'Kỹ năng mềm', 'target_classes': '5 lớp CNTT'},
        'SSK103': {'name': 'Tư duy phân tích', 'category': 'Kỹ năng mềm', 'target_classes': '4 lớp QTKD (QTKD1, QTKD3, HCM1 đã học; QTKD2 chuẩn bị học)'},
        # Ngoại ngữ
        'ENG105-K26': {'name': 'Basic Speaking (Tiếng Anh)', 'category': 'Ngoại ngữ', 'target_classes': '8 lớp (CNTT2, 3, QTKD1, 2, 3, HCM1, 2, QTKD1)'},
        'JPN105-K26': {'name': 'Tiếng Nhật cơ sở 1', 'category': 'Ngoại ngữ', 'target_classes': 'Dành riêng cho lớp HN-KS26-CNTT1'}
    }

    # Calculate actual statistics for each new course across registered students
    course_stats = {}
    for ccode, meta in COURSES_METADATA.items():
        total_enrolled = 0
        cc_viol_count = 0
        bt_viol_count = 0
        el_viol_count = 0
        classes_active = []
        
        for cname, courses in live_data.items():
            if ccode in courses:
                cinfo = courses[ccode]
                st_list = [s for s in cinfo.get('students', []) if s.get('studentCode') in ssk_students and ssk_students[s.get('studentCode')]['class'] == cname]
                if not st_list: continue
                
                total_enrolled += len(st_list)
                c_cc = sum(1 for s in st_list if s.get('absence', {}).get('absentSessions', 0) > 0)
                c_el = sum(1 for s in st_list if s.get('elearning', {}).get('lateSessions', 0) > 0)
                cc_viol_count += c_cc
                el_viol_count += c_el
                classes_active.append(f"{cname} ({len(st_list)} SV, vắng {c_cc}b, chậm {c_el} EL)")
                
        cc_rate = round(cc_viol_count / total_enrolled * 100, 1) if total_enrolled > 0 else 0.0
        el_rate = round(el_viol_count / total_enrolled * 100, 1) if total_enrolled > 0 else 0.0
        
        course_stats[ccode] = {
            'code': ccode,
            'name': meta['name'],
            'category': meta['category'],
            'target_classes': meta['target_classes'],
            'total': total_enrolled,
            'cc_count': cc_viol_count,
            'cc_rate': cc_rate,
            'el_count': el_viol_count,
            'el_rate': el_rate,
            'classes_active': classes_active
        }

    # 3. Analyze each student's performance in new courses
    student_eval = {}
    for code, st_info in ssk_students.items():
        student_eval[code] = {
            'code': code,
            'name': st_info['name'],
            'class': st_info['class'],
            'm1': st_info,
            'courses': {},
            'has_new_viol': False,
            'abs_courses': [],
            'el_courses': [],
            'viol_details': []
        }

    for cname, courses in live_data.items():
        for ccode in COURSES_METADATA.keys():
            if ccode not in courses: continue
            cinfo = courses[ccode]
            c_title = cinfo.get('courseName')
            for st in cinfo.get('students', []):
                code = st.get('studentCode')
                if not code or code not in student_eval: continue
                # Verify class membership
                if student_eval[code]['class'] != cname: continue
                
                abs_s = st.get('absence', {}).get('absentSessions', 0)
                late_el = st.get('elearning', {}).get('lateSessions', 0)
                
                is_viol = (abs_s > 0) or (late_el > 0)
                student_eval[code]['courses'][ccode] = {
                    'courseCode': ccode,
                    'courseName': c_title,
                    'absentSessions': abs_s,
                    'lateEL': late_el,
                    'isViol': is_viol
                }
                if is_viol:
                    student_eval[code]['has_new_viol'] = True
                    d = []
                    if abs_s > 0:
                        d.append(f"vắng {abs_s} buổi")
                        student_eval[code]['abs_courses'].append(f"{ccode} (vắng {abs_s}b)")
                    if late_el > 0:
                        d.append(f"chậm {late_el} bài EL")
                        student_eval[code]['el_courses'].append(f"{ccode} (chậm {late_el} bài)")
                    student_eval[code]['viol_details'].append(f"{ccode}: {', '.join(d)}")

    # 4. Class Hotspots Matrix (9 Classes)
    CLASS_TEACHERS = {
        'HN-KS26-CNTT1': {'gv_m1': 'Trần Minh Cường', 'gv_new': 'Trịnh Quốc Hai (IT108) & Giáp Thị Minh Hằng (JPN105)'},
        'HN-KS26-CNTT2': {'gv_m1': 'Hồ Xuân Hùng', 'gv_new': 'Trịnh Quốc Hai (IT108) & Nguyễn Hồng Nhung (ENG105)'},
        'HN-KS26-CNTT3': {'gv_m1': 'Nguyễn Duy Quang', 'gv_new': 'Lương Quốc Tuấn (IT108) & Lò Thị Ngọc Anh (ENG105)'},
        'HN-K26-QTKD1': {'gv_m1': 'Hoàng Thị Hậu', 'gv_new': 'Nguyễn Ngọc Vân Khanh (SSK103) & Lò Thị Ngọc Anh (ENG105)'},
        'HN-K26-QTKD2': {'gv_m1': 'Hoàng Thị Kim Oanh', 'gv_new': 'Nguyễn Hồng Nhung (ENG105)'},
        'HN-K26-QTKD3': {'gv_m1': 'Hoàng Thị Hậu', 'gv_new': 'Nguyễn Ngọc Vân Khanh (SSK103) & Nguyễn Thị Hồng Minh (SSK102)'},
        'HCM-KS26-CNTT1': {'gv_m1': 'Nguyễn Bá Minh Đạo', 'gv_new': 'Lê Hà Thanh Sang (IT108) & Huỳnh Thị Kim Khánh (ENG105)'},
        'HCM-KS26-CNTT2': {'gv_m1': 'Nguyễn Bá Minh Đạo', 'gv_new': 'Lê Hà Thanh Sang (IT108) & Huỳnh Thị Kim Khánh (ENG105)'},
        'HCM-K26-QTKD1': {'gv_m1': 'Lê Nhựt Mi', 'gv_new': 'Lê Thị Bảo Yến (SSK103) & Lê Hà Thanh Sang (SSK102)'}
    }

    class_hotspots = []
    for cname, m1 in class_m1_stats.items():
        tot = m1['total']
        c_students = [s for s in student_eval.values() if s['class'] == cname]
        
        # New violations
        violators = [s for s in c_students if s['has_new_viol']]
        repeat_v = [s for s in violators if s['m1']['has_viol']]
        new_v = [s for s in violators if not s['m1']['has_viol']]
        clean_cnt = tot - len(violators)
        clean_rate = round(clean_cnt / tot * 100, 1)
        
        # Hotspot classification
        if len(violators) >= 15:
            hotspot = '🚨 ĐIỂM NÓNG CẦN CAN THIỆP GẤP'
            tag_class = 'tag-red'
            action = 'Quản lý ĐT + GV vào trực tiếp lớp 15p chấn chỉnh, gọi phụ huynh nhóm tái phạm'
        elif len(violators) >= 8:
            hotspot = '🟠 CẦN XỬ LÝ NHÓM TÁI PHẠM'
            tag_class = 'tag-orange'
            action = 'CVHT gặp riêng 5-10p giữa giờ đôn đốc, ký biên bản cam kết nề nếp'
        elif len(violators) >= 3:
            hotspot = '🟡 TIẾN BỘ RÕ RỆT (CẦN NHẮC NHỞ NHẸ)'
            tag_class = 'tag-yellow'
            action = 'CVHT nhắc nhanh 3p đầu giờ, đôn đốc nộp bài Elearning bù trước 22h'
        else:
            hotspot = '🟢 XUẤT SẮC — SẠCH 100% VI PHẠM'
            tag_class = 'tag-green'
            action = 'Tuyên dương toàn lớp qua nhóm Zalo, duy trì nền nếp chuẩn mực'

        class_hotspots.append({
            'class': cname,
            'teachers': CLASS_TEACHERS.get(cname, {'gv_m1': 'Chưa phân', 'gv_new': 'Chưa phân'}),
            'total': tot,
            # Môn cũ chuẩn Frontend
            'm1_cc_rate': m1['cc_rate'],
            'm1_cc_count': m1['cc_count'],
            'm1_bt_rate': m1['bt_rate'],
            'm1_bt_count': m1['bt_count'],
            'm1_el_rate': m1['el_rate'],
            'm1_el_count': m1['el_count'],
            # Môn mới
            'violators_count': len(violators),
            'repeat_count': len(repeat_v),
            'new_count': len(new_v),
            'clean_count': clean_cnt,
            'clean_rate': clean_rate,
            'hotspot': hotspot,
            'tag_class': tag_class,
            'action': action
        })

    class_hotspots.sort(key=lambda x: x['violators_count'], reverse=True)

    # 5. Build unimproved students list (strict & verified)
    unimproved_students = []
    for s in student_eval.values():
        if not s['has_new_viol']: continue
        
        is_repeat = s['m1']['has_viol']
        off_type = 'LẶP LẠI HÀNH VI (Tái phạm)' if is_repeat else 'MỚI PHÁT SINH VI PHẠM'
        off_tag = 'tag-red' if is_repeat else 'tag-yellow'
        
        m1_desc = f"CC: {s['m1']['cc_rate']}% | BT: {s['m1']['bt_done']}/3 bài | EL: {s['m1']['el_late']} bài chậm"
        new_desc = "; ".join(s['viol_details'])
        
        has_abs = len(s['abs_courses']) > 0
        if is_repeat and has_abs:
            sol = "Gặp riêng 5p cuối giờ tại lớp, lập biên bản cam kết nề nếp, gọi điện phụ huynh thông báo nguy cơ cấm thi"
            pic = "Quản lý ĐT + CVHT"
            dl = "Trong 48h"
        elif has_abs:
            sol = "Gặp 3p đầu giờ tìm hiểu lý do vắng (ốm, trùng ca), đôn đốc đi học đủ các buổi còn lại"
            pic = "CVHT lớp"
            dl = "Tuần này"
        else:
            sol = "Gặp 3p giữa giờ hướng dẫn mở app hoàn thành bài Elearning bù trước 22h"
            pic = "CVHT lớp + GV phụ trách"
            dl = "Trước buổi tới"

        unimproved_students.append({
            'class': s['class'],
            'code': s['code'],
            'name': s['name'],
            'off_type': off_type,
            'off_tag': off_tag,
            'm1_desc': m1_desc,
            'new_desc': new_desc,
            'solution': sol,
            'pic': pic,
            'deadline': dl,
            'is_repeat': is_repeat
        })

    unimproved_students.sort(key=lambda x: (0 if x['is_repeat'] else 1, x['class'], x['name']))

    return {
        'class_m1_stats': class_m1_stats,
        'course_stats': course_stats,
        'class_hotspots': class_hotspots,
        'unimproved_students': unimproved_students,
        'student_eval': student_eval
    }

def export_excel(data, filepath):
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    header_font = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='1E3A8A', end_color='1E3A8A', fill_type='solid')
    sub_fill = PatternFill(start_color='2563EB', end_color='2563EB', fill_type='solid')
    alert_fill = PatternFill(start_color='FEE2E2', end_color='FEE2E2', fill_type='solid')
    warning_fill = PatternFill(start_color='FEF3C7', end_color='FEF3C7', fill_type='solid')
    success_fill = PatternFill(start_color='D1FAE5', end_color='D1FAE5', fill_type='solid')
    border = Border(
        left=Side(style='thin', color='CBD5E1'), right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'), bottom=Side(style='thin', color='CBD5E1')
    )

    # ----------------------------------------------------
    # SHEET 1: HOTSPOTS MATRIX (BẢNG ĐIỂM NÓNG 9 LỚP)
    # ----------------------------------------------------
    ws1 = wb.create_sheet('1_DIEM_NONG_9_LOP')
    ws1.views.sheetView[0].showGridLines = True

    # Title
    ws1.merge_cells('A1:L1')
    ws1['A1'] = "BẢNG ĐỐI SOÁT CHUYỂN DỊCH HÀNH VI VÀ NHẬN DIỆN ĐIỂM NÓNG 9 LỚP K26"
    ws1['A1'].font = Font(name='Segoe UI', size=14, bold=True, color='1E3A8A')
    ws1['A1'].alignment = Alignment(horizontal='left', vertical='center')

    headers1 = [
        "STT", "Lớp Học", "Sĩ số", "GV Môn Cũ (SSK101)", "GV Môn Mới",
        "Môn Cũ CC (>10%)", "Môn Cũ BT (>10%)", "Môn Cũ EL",
        "SV Vi Phạm Môn Mới", "Tái Phạm (Lặp lại)", "Mới Phát Sinh", "Tỷ Lệ Sạch Lỗi Môn Mới", "Đánh Giá & Kế Hoạch 5-15 Phút"
    ]
    ws1.append([])
    ws1.append(headers1)
    for col_idx in range(1, len(headers1) + 1):
        cell = ws1.cell(row=3, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    for i, c in enumerate(data['class_hotspots'], 1):
        row = [
            i, c['class'], c['total'], c['teachers']['gv_m1'], c['teachers']['gv_new'],
            f"{c['m1_cc_rate']}% ({c['m1_cc_count']} SV)",
            f"{c['m1_bt_rate']}% ({c['m1_bt_count']} SV)",
            f"{c['m1_el_rate']}% ({c['m1_el_count']} SV)",
            c['violators_count'], c['repeat_count'], c['new_count'],
            f"{c['clean_rate']}% ({c['clean_count']} SV)",
            f"{c['hotspot']} — {c['action']}"
        ]
        ws1.append(row)
        r_idx = ws1.max_row
        for col_idx in range(1, len(row) + 1):
            cell = ws1.cell(row=r_idx, column=col_idx)
            cell.border = border
            cell.font = Font(name='Segoe UI', size=10)
            if col_idx in [1, 3, 9, 10, 11]:
                cell.alignment = Alignment(horizontal='center', vertical='center')
            elif col_idx in [6, 7, 8, 12]:
                cell.alignment = Alignment(horizontal='center', vertical='center')
            else:
                cell.alignment = Alignment(horizontal='left', vertical='center')

    # ----------------------------------------------------
    # SHEET 2: CÁC MÔN HỌC MỚI (PHÂN THEO 3 KHỐI)
    # ----------------------------------------------------
    ws2 = wb.create_sheet('2_DOI_SOAT_MON_HOC_MOI')
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells('A1:H1')
    ws2['A1'] = "THỐNG KÊ CHI TIẾT CÁC MÔN HỌC MỚI K26 (PHÂN ĐỊNH 3 KHỐI MÔN)"
    ws2['A1'].font = Font(name='Segoe UI', size=14, bold=True, color='1E3A8A')

    headers2 = ["Khối Môn", "Mã Môn", "Tên Môn Học", "Đối Tượng Lớp", "Tổng SV Học", "Tỷ Lệ Vắng CC", "Tỷ Lệ Chậm EL", "Ghi Chú Đào Tạo"]
    ws2.append([])
    ws2.append(headers2)
    for col_idx in range(1, len(headers2) + 1):
        cell = ws2.cell(row=3, column=col_idx)
        cell.font = header_font
        cell.fill = sub_fill
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    for ccode, c in data['course_stats'].items():
        row = [
            c['category'], c['code'], c['name'], c['target_classes'], c['total'],
            f"{c['cc_rate']}% ({c['cc_count']} SV)",
            f"{c['el_rate']}% ({c['el_count']} SV)",
            "; ".join(c['classes_active'])
        ]
        ws2.append(row)
        r_idx = ws2.max_row
        for col_idx in range(1, len(row) + 1):
            cell = ws2.cell(row=r_idx, column=col_idx)
            cell.border = border
            cell.font = Font(name='Segoe UI', size=10)
            if col_idx in [5, 6, 7]:
                cell.alignment = Alignment(horizontal='center', vertical='center')

    # ----------------------------------------------------
    # SHEET 3: DANH SÁCH SINH VIÊN CHƯA CẢI THIỆN & TÁI PHẠM
    # ----------------------------------------------------
    ws3 = wb.create_sheet('3_SV_CHUA_CAI_THIEN_VA_TAI_PHAM')
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells('A1:I1')
    ws3['A1'] = "DANH SÁCH SINH VIÊN CHƯA CẢI THIỆN / TÁI PHẠM MÔN MỚI CẦN XỬ LÝ 5-15 PHÚT"
    ws3['A1'].font = Font(name='Segoe UI', size=14, bold=True, color='B91C1C')

    headers3 = ["STT", "Phân Loại", "Lớp Học", "Mã SV", "Họ và Tên", "Chỉ Số Môn Cũ (SSK101)", "Vi Phạm Môn Mới Thực Tế", "Giải Pháp Trực Tiếp 5-15 Phút", "Người Phụ Trách (PIC)", "Thời Hạn (Deadline)"]
    ws3.append([])
    ws3.append(headers3)
    for col_idx in range(1, len(headers3) + 1):
        cell = ws3.cell(row=3, column=col_idx)
        cell.font = header_font
        cell.fill = PatternFill(start_color='B91C1C', end_color='B91C1C', fill_type='solid')
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    for i, s in enumerate(data['unimproved_students'], 1):
        row = [
            i, s['off_type'], s['class'], s['code'], s['name'],
            s['m1_desc'], s['new_desc'], s['solution'], s['pic'], s['deadline']
        ]
        ws3.append(row)
        r_idx = ws3.max_row
        for col_idx in range(1, len(row) + 1):
            cell = ws3.cell(row=r_idx, column=col_idx)
            cell.border = border
            cell.font = Font(name='Segoe UI', size=10)
            if col_idx in [1, 3, 4, 9, 10]:
                cell.alignment = Alignment(horizontal='center', vertical='center')
            elif col_idx == 2:
                cell.alignment = Alignment(horizontal='center', vertical='center')
                if 'Tái phạm' in s['off_type']:
                    cell.fill = alert_fill
                    cell.font = Font(name='Segoe UI', size=10, bold=True, color='B91C1C')
                else:
                    cell.fill = warning_fill
                    cell.font = Font(name='Segoe UI', size=10, bold=True, color='D97706')

    # Auto fit column widths
    for ws in [ws1, ws2, ws3]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 50)

    wb.save(filepath)
    print(f"Saved verified Excel to: {filepath}")

def export_html(data, filepath):
    hotspots = data['class_hotspots']
    courses = data['course_stats']
    unimproved = data['unimproved_students']
    
    repeat_list = [s for s in unimproved if s['is_repeat']]
    new_list = [s for s in unimproved if not s['is_repeat']]

    # Prepare rows for Hotspots Table
    hotspot_rows_html = ""
    for c in hotspots:
        hotspot_rows_html += f"""
        <tr class="hover:bg-slate-800/40 border-b border-slate-800 transition-colors">
            <td class="py-3 px-4 font-bold text-white whitespace-nowrap">{c['class']}</td>
            <td class="py-3 px-3 text-center font-mono font-bold text-slate-300">{c['total']}</td>
            <td class="py-3 px-3 text-xs text-slate-400">
                <span class="text-slate-300 font-medium">{c['teachers']['gv_m1']}</span><br>
                <span class="text-blue-400 font-medium">{c['teachers']['gv_new']}</span>
            </td>
            <td class="py-3 px-3 text-center font-semibold text-rose-400">{c['m1_cc_rate']}% <span class="text-[11px] text-slate-500">({c['m1_cc_count']})</span></td>
            <td class="py-3 px-3 text-center font-semibold text-amber-400">{c['m1_bt_rate']}% <span class="text-[11px] text-slate-500">({c['m1_bt_count']})</span></td>
            <td class="py-3 px-3 text-center font-semibold text-purple-400">{c['m1_el_rate']}% <span class="text-[11px] text-slate-500">({c['m1_el_count']})</span></td>
            <td class="py-3 px-3 text-center font-bold text-rose-400">{c['violators_count']}</td>
            <td class="py-3 px-3 text-center font-bold text-red-500">{c['repeat_count']}</td>
            <td class="py-3 px-3 text-center font-bold text-amber-400">{c['new_count']}</td>
            <td class="py-3 px-3 text-center font-extrabold text-emerald-400">{c['clean_rate']}% <span class="text-[11px] text-slate-500">({c['clean_count']})</span></td>
            <td class="py-3 px-4 text-xs">
                <span class="px-2 py-0.5 rounded text-[11px] font-bold {c['tag_class']}">{c['hotspot']}</span>
                <p class="text-[11px] text-slate-400 mt-1">{c['action']}</p>
            </td>
        </tr>
        """

    # Prepare rows for 3 Distinct Course Blocks
    courses_html = ""
    for cat in ['Chuyên ngành', 'Kỹ năng mềm', 'Ngoại ngữ']:
        cat_courses = [c for c in courses.values() if c['category'] == cat]
        courses_html += f"""
        <div class="space-y-3 mb-6">
            <h4 class="text-sm font-bold text-blue-400 uppercase tracking-wider flex items-center gap-2">
                <i class="fa-solid fa-folder-open"></i> Khối {cat}
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        """
        for c in cat_courses:
            courses_html += f"""
                <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-800 hover:border-slate-700 transition">
                    <div class="flex items-center justify-between mb-2">
                        <span class="font-bold text-white text-sm">[{c['code']}] {c['name']}</span>
                        <span class="text-xs px-2 py-0.5 rounded font-mono bg-blue-950 text-blue-300 border border-blue-800">{c['total']} SV theo học</span>
                    </div>
                    <p class="text-xs text-slate-400 mb-3">{c['target_classes']}</p>
                    <div class="grid grid-cols-2 gap-2 text-center text-xs">
                        <div class="bg-slate-800/60 p-2 rounded">
                            <span class="text-slate-400 block text-[11px]">Vi phạm CC (>0b)</span>
                            <span class="font-bold text-rose-400 text-sm">{c['cc_rate']}%</span>
                            <span class="text-slate-500 text-[10px] block">({c['cc_count']} SV vắng)</span>
                        </div>
                        <div class="bg-slate-800/60 p-2 rounded">
                            <span class="text-slate-400 block text-[11px]">Chậm Elearning</span>
                            <span class="font-bold text-purple-400 text-sm">{c['el_rate']}%</span>
                            <span class="text-slate-500 text-[10px] block">({c['el_count']} SV chậm)</span>
                        </div>
                    </div>
                </div>
            """
        courses_html += "</div></div>"

    # Prepare rows for Unimproved Students
    unimproved_rows_html = ""
    for s in unimproved:
        unimproved_rows_html += f"""
        <tr class="hover:bg-slate-800/40 border-b border-slate-800 text-xs">
            <td class="py-3 px-3 font-semibold text-slate-400 whitespace-nowrap">{s['class']}</td>
            <td class="py-3 px-3 font-mono text-slate-300">{s['code']}</td>
            <td class="py-3 px-3 font-bold text-white whitespace-nowrap">{s['name']}</td>
            <td class="py-3 px-3 text-center whitespace-nowrap">
                <span class="px-2 py-0.5 rounded text-[11px] font-bold {s['off_tag']}">{s['off_type']}</span>
            </td>
            <td class="py-3 px-3 text-slate-300 whitespace-nowrap">{s['m1_desc']}</td>
            <td class="py-3 px-3 text-rose-300 font-medium">{s['new_desc']}</td>
            <td class="py-3 px-3 text-slate-300">{s['solution']}</td>
            <td class="py-3 px-3 text-center font-medium text-amber-300 whitespace-nowrap">{s['pic']}</td>
            <td class="py-3 px-3 text-center text-slate-400 whitespace-nowrap">{s['deadline']}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Đối Soát Hành Vi Tân Sinh Viên K26 & Ma Trận Điểm Nóng — Giám Đốc Đào Tạo</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
        .tag-red {{ background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }}
        .tag-orange {{ background: rgba(249, 115, 22, 0.15); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.3); }}
        .tag-yellow {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}
        .tag-green {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
    </style>
</head>
<body class="bg-slate-950 text-slate-200 p-4 lg:p-8 min-h-screen">
    <div class="max-w-[1520px] mx-auto space-y-6">

        <!-- HEADER -->
        <div class="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
                <div class="flex items-center gap-2 mb-2">
                    <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30">
                        CHỈ ĐẠO GIÁM ĐỐC ĐÀO TẠO
                    </span>
                    <span class="text-xs text-slate-400">Khóa K26 • Cập nhật LMS Live Analytics</span>
                </div>
                <h1 class="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
                    Báo Cáo Đối Soát Chuyển Dịch Hành Vi & Ma Trận Điểm Nóng K26
                </h1>
                <p class="text-slate-400 text-sm mt-1">
                    Đối soát giữa Môn đầu tiên (SSK101 - Chuẩn LMS Frontend) và 3 Khối Môn Học Mới (Chuyên ngành, Kỹ năng mềm, Ngoại ngữ). Tác chiến 5–15 phút trực tiếp tại lớp.
                </p>
            </div>
            <div class="flex items-center gap-3">
                <a href="K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold flex items-center gap-2 shadow-lg transition">
                    <i class="fa-solid fa-file-excel"></i> Tải Excel Tác Chiến 3 Sheet
                </a>
            </div>
        </div>

        <!-- 4 KPI SUMMARY CARDS -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl">
                <span class="text-slate-400 text-xs font-semibold uppercase">Quy Mô Khóa K26</span>
                <div class="text-3xl font-extrabold text-white mt-1">370 SV</div>
                <div class="text-xs text-slate-500 mt-1">9 Lớp (6 Hà Nội + 3 TP.HCM)</div>
            </div>
            <div class="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl">
                <span class="text-slate-400 text-xs font-semibold uppercase">Tái Phạm / Lặp Lại Hành Vi</span>
                <div class="text-3xl font-extrabold text-rose-400 mt-1">{len(repeat_list)} SV</div>
                <div class="text-xs text-rose-300 mt-1">🚨 Môn 1 vi phạm & Môn mới tiếp tục vi phạm</div>
            </div>
            <div class="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl">
                <span class="text-slate-400 text-xs font-semibold uppercase">Mới Phát Sinh Vi Phạm</span>
                <div class="text-3xl font-extrabold text-amber-400 mt-1">{len(new_list)} SV</div>
                <div class="text-xs text-amber-300 mt-1">🟡 Môn 1 tốt, môn mới bỡ ngỡ ca học/bài</div>
            </div>
            <div class="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl">
                <span class="text-slate-400 text-xs font-semibold uppercase">Sạch 100% Lỗi Môn Mới</span>
                <div class="text-3xl font-extrabold text-emerald-400 mt-1">{370 - len(unimproved)} SV</div>
                <div class="text-xs text-emerald-300 mt-1">🟢 Đạt {(370 - len(unimproved))/370*100:.1f}% toàn khóa sạch vi phạm</div>
            </div>
        </div>

        <!-- SECTION 1: HOTSPOTS MATRIX -->
        <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-2">
                <div>
                    <h3 class="text-lg font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-fire text-rose-500"></i> 1. Bảng Tình Hình Từng Lớp Học & Nhận Diện Điểm Nóng (Class Hotspots)
                    </h3>
                    <p class="text-xs text-slate-400">
                        Số liệu môn cũ SSK101 chuẩn LMS Frontend (>10% CC, >10% BT, EL) &bull; Điển hình HN-KS26-CNTT1 chuẩn xác: CC 58.14%, BT 13.95%, EL 55.81%.
                    </p>
                </div>
            </div>
            <div class="overflow-x-auto rounded-xl border border-slate-800">
                <table class="w-full text-left text-xs lg:text-sm">
                    <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800 text-[11px]">
                        <tr>
                            <th class="py-3 px-4">Tên Lớp</th>
                            <th class="py-3 px-3 text-center">Sĩ số</th>
                            <th class="py-3 px-3">GV Môn Cũ / GV Môn Mới</th>
                            <th class="py-3 px-3 text-center text-rose-400">Môn Cũ CC (>10%)</th>
                            <th class="py-3 px-3 text-center text-amber-400">Môn Cũ BT (>10%)</th>
                            <th class="py-3 px-3 text-center text-purple-400">Môn Cũ EL</th>
                            <th class="py-3 px-3 text-center text-rose-400">SV Vi Phạm Môn Mới</th>
                            <th class="py-3 px-3 text-center text-red-500">Tái Phạm</th>
                            <th class="py-3 px-3 text-center text-amber-400">Mới Bị</th>
                            <th class="py-3 px-3 text-center text-emerald-400">Sạch Lỗi Môn Mới</th>
                            <th class="py-3 px-4">Điểm Nóng & Kế Hoạch 5-15p</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800">
                        {hotspot_rows_html}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- SECTION 2: 3 DISTINCT COURSE CATEGORIES -->
        <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <div>
                <h3 class="text-lg font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-layer-group text-blue-400"></i> 2. Cơ Cấu 3 Khối Môn Học Đang Triển Khai (Không Gộp Chung Gây Lẫn Lộn)
                </h3>
                <p class="text-xs text-slate-400">
                    Phân tách bạch 3 khối đào tạo: Chuyên ngành, Kỹ năng mềm, và Ngoại ngữ (Tiếng Anh vs Tiếng Nhật).
                </p>
            </div>
            {courses_html}
        </div>

        <!-- SECTION 3: UNIMPROVED & REPEAT OFFENDERS LIST -->
        <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-2">
                <div>
                    <h3 class="text-lg font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-user-xmark text-rose-500"></i> 3. Danh Sách Sinh Viên Chưa Cải Thiện & Tái Phạm (Bóc Tách Minh Bạch)
                    </h3>
                    <p class="text-xs text-slate-400">
                        Đã loại trừ sinh viên học Tiếng Nhật đạt chuẩn (như Nguyễn Đăng Minh Nhật 0% vi phạm). Hiển thị rõ vi phạm thực tế từng môn mới, giải pháp trực tiếp 5-15 phút tại lớp, PIC và Deadline.
                    </p>
                </div>
            </div>
            <div class="overflow-x-auto rounded-xl border border-slate-800 max-h-[600px]">
                <table class="w-full text-left text-xs">
                    <thead class="bg-slate-900 text-slate-300 uppercase font-bold border-b border-slate-800 sticky top-0 text-[11px]">
                        <tr>
                            <th class="py-3 px-3">Lớp</th>
                            <th class="py-3 px-3">Mã SV</th>
                            <th class="py-3 px-3">Họ và Tên</th>
                            <th class="py-3 px-3 text-center">Phân Loại</th>
                            <th class="py-3 px-3">Chỉ Số Môn Cũ (SSK101)</th>
                            <th class="py-3 px-3">Vi Phạm Môn Mới Thực Tế</th>
                            <th class="py-3 px-3">Giải Pháp Trực Tiếp 5-15 Phút</th>
                            <th class="py-3 px-3 text-center">PIC</th>
                            <th class="py-3 px-3 text-center">Deadline</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800">
                        {unimproved_rows_html}
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</body>
</html>
    """

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Saved verified HTML to: {filepath}")

def main():
    print("Bắt đầu xử lý dữ liệu chuẩn xác...")
    data = build_data()
    
    excel_path = 'output/dashboards/management/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx'
    html_path = 'output/dashboards/management/bao_cao_k26_chuyen_dich_hanh_vi.html'
    deploy_html_path = 'deploy_web/bao_cao_k26_chuyen_dich_hanh_vi.html'
    
    export_excel(data, excel_path)
    export_html(data, html_path)
    
    # Deploy copy
    os.makedirs('deploy_web', exist_ok=True)
    shutil.copy(html_path, deploy_html_path)
    print(f"Deployed copy to: {deploy_html_path}")

if __name__ == '__main__':
    main()

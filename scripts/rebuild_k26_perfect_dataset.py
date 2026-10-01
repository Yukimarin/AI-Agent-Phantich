# -*- coding: utf-8 -*-
"""
Rebuild complete, verified dataset for K26 Behavioral Shifts & Interventions
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/realtime_ssk101_full_data.json', 'r', encoding='utf-8') as f:
    ssk101_data = json.load(f)

with open('scratch/all_ks26_classes_live_metrics.json', 'r', encoding='utf-8') as f:
    live_data = json.load(f)

# 1. Base SSK101 students
ssk_students = {}
class_m1_stats = {}

for cls in ssk101_data:
    cname = cls['className']
    st_list = cls['students']
    N = len(st_list)
    
    # Exact Frontend formulas:
    cc_viol_list = []
    bt_viol_list = []
    el_viol_list = []
    
    for s in st_list:
        code = s['studentCode']
        rec = s.get('records', 5) or 5
        
        # CC: (absentUnexcused*1.0 + absentExcused*0.5 + late*0.5)/rec * 100
        cc_rate = round((s.get('absentUnexcused', 0)*1.0 + s.get('absentExcused', 0)*0.5 + s.get('late', 0)*0.5) / rec * 100, 1)
        cc_is_viol = (cc_rate >= 10.0)
        if cc_is_viol: cc_viol_list.append(code)
        
        # BT: hwDone < 3
        bt_is_viol = (s.get('hwDone', 0) < 3)
        if bt_is_viol: bt_viol_list.append(code)
        
        # EL: elLateCount > 0
        el_is_viol = (s.get('elLateCount', 0) > 0)
        if el_is_viol: el_viol_list.append(code)
        
        ssk_students[code] = {
            'code': code,
            'name': s['fullName'],
            'class': cname,
            'cc_rate': cc_rate,
            'cc_viol': cc_is_viol,
            'bt_done': s.get('hwDone', 0),
            'bt_viol': bt_is_viol,
            'el_late': s.get('elLateCount', 0),
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

print("=== MÔN CŨ SSK101 (CHUẨN FRONTEND) ===")
for cname, st in class_m1_stats.items():
    print(f"{cname:15} | Sĩ số: {st['total']:2} | CC: {st['cc_rate']:5.2f}% ({st['cc_count']}) | BT: {st['bt_rate']:5.2f}% ({st['bt_count']}) | EL: {st['el_rate']:5.2f}% ({st['el_count']})")

# 2. Map actual new courses for each class
# Distinct courses by category:
COURSES_METADATA = {
    'IT108-K26': {'name': 'Nhập Môn CNTT', 'category': 'Chuyên ngành', 'classes': ['HN-KS26-CNTT1', 'HN-KS26-CNTT2', 'HN-KS26-CNTT3', 'HN-KS26-CNTT4', 'HCM-KS26-CNTT1', 'HCM-KS26-CNTT2']},
    'SSK102': {'name': 'Tin học ứng dụng', 'category': 'Chuyên ngành', 'classes': ['HN-K26-QTKD1', 'HN-K26-QTKD2', 'HN-K26-QTKD3', 'HCM-K26-QTKD1']},
    'SKL01': {'name': 'Kỹ năng làm việc nhóm', 'category': 'Kỹ năng mềm', 'classes': ['HN-KS26-CNTT1', 'HN-KS26-CNTT2', 'HN-KS26-CNTT3', 'HCM-KS26-CNTT1', 'HCM-KS26-CNTT2']},
    'SSK103': {'name': 'Tư duy phân tích', 'category': 'Kỹ năng mềm', 'classes': ['HN-K26-QTKD1', 'HN-K26-QTKD2', 'HN-K26-QTKD3', 'HCM-K26-QTKD1']},
    'ENG105-K26': {'name': 'Basic Speaking (Tiếng Anh)', 'category': 'Ngoại ngữ', 'classes': ['HN-KS26-CNTT2', 'HN-KS26-CNTT3', 'HN-K26-QTKD1', 'HN-K26-QTKD2', 'HN-K26-QTKD3', 'HCM-KS26-CNTT1', 'HCM-KS26-CNTT2', 'HCM-K26-QTKD1']},
    'JPN105-K26': {'name': 'Tiếng Nhật cơ sở 1', 'category': 'Ngoại ngữ', 'classes': ['HN-KS26-CNTT1']}
}

# 3. Analyze each student's performance in new courses
student_new_metrics = {}
for code, st_info in ssk_students.items():
    student_new_metrics[code] = {
        'code': code,
        'name': st_info['name'],
        'class': st_info['class'],
        'm1': st_info,
        'courses': {},
        'has_new_viol': False,
        'viol_details': []
    }

for cname, courses in live_data.items():
    for ccode, cinfo in courses.items():
        if ccode not in COURSES_METADATA:
            continue
        c_name = cinfo.get('courseName')
        for st in cinfo.get('students', []):
            code = st.get('studentCode')
            if not code or code not in student_new_metrics:
                continue
            # Ensure student belongs to class
            if student_new_metrics[code]['class'] != cname:
                continue
            
            abs_s = st.get('absence', {}).get('absentSessions', 0)
            late_el = st.get('elearning', {}).get('lateSessions', 0)
            hw_done = st.get('homework', {}).get('done', 0)
            
            is_viol = (abs_s > 0) or (late_el > 0)
            student_new_metrics[code]['courses'][ccode] = {
                'courseCode': ccode,
                'courseName': c_name,
                'absentSessions': abs_s,
                'lateEL': late_el,
                'hwDone': hw_done,
                'isViol': is_viol
            }
            if is_viol:
                student_new_metrics[code]['has_new_viol'] = True
                d = []
                if abs_s > 0: d.append(f"vắng {abs_s}b")
                if late_el > 0: d.append(f"chậm {late_el} bài EL")
                student_new_metrics[code]['viol_details'].append(f"{ccode} ({', '.join(d)})")

# Check Nguyen Dang Minh Nhat
nhat = student_new_metrics.get('B26DTCN100')
if nhat:
    print(f"\nKiểm tra Nguyễn Đăng Minh Nhật:")
    print(f"  Môn 1: CC: {nhat['m1']['cc_rate']}% | BT: {nhat['m1']['bt_done']} bài | EL: {nhat['m1']['el_late']} bài chậm")
    print(f"  Môn mới: {list(nhat['courses'].keys())}")
    for ccode, cdet in nhat['courses'].items():
        print(f"    - {ccode}: Vắng {cdet['absentSessions']}b, Chậm EL {cdet['lateEL']}b, Vi phạm: {cdet['isViol']}")
    print(f"  has_new_viol: {nhat['has_new_viol']}")

# Summary of violators
violators = [s for s in student_new_metrics.values() if s['has_new_viol']]
repeat_violators = [s for s in violators if s['m1']['has_viol']]
new_violators = [s for s in violators if not s['m1']['has_viol']]

print(f"\nTổng số sinh viên có vi phạm môn mới: {len(violators)}")
print(f"  1. Nhóm TÁI PHẠM / LẶP LẠI (Môn 1 vi phạm -> Môn mới vi phạm): {len(repeat_violators)} SV")
print(f"  2. Nhóm MỚI PHÁT SINH (Môn 1 chuẩn -> Môn mới vi phạm): {len(new_violators)} SV")

# Class breakdown for violators
print("\nPhân bổ sinh viên vi phạm môn mới theo từng lớp:")
for cname in class_m1_stats.keys():
    c_viol = [s for s in violators if s['class'] == cname]
    c_rep = [s for s in repeat_violators if s['class'] == cname]
    c_new = [s for s in new_violators if s['class'] == cname]
    tot = class_m1_stats[cname]['total']
    clean_cnt = tot - len(c_viol)
    clean_rate = round(clean_cnt / tot * 100, 1)
    print(f"  {cname:15} | Tổng: {tot} | Vi phạm: {len(c_viol):2} (Tái phạm: {len(c_rep):2}, Mới: {len(c_new):2}) | Sạch 100%: {clean_cnt:2} ({clean_rate}%)")

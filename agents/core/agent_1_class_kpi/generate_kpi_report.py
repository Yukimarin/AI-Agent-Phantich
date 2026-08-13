# -*- coding: utf-8 -*-
import sys
import openpyxl
from datetime import datetime, date, timedelta
from collections import defaultdict
import numpy as np
import re
from openpyxl.utils import get_column_letter

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

class_sizes = {}
def extract_class_size(class_name):
    match = re.search(r'\((\d+)\)', str(class_name))
    if match:
        return int(match.group(1))
    return 30

excel_path = 'data/inputs/PTIT_Chiso.xlsx'
output_path = 'output/reports/core/agent_1_student_discipline.md'

wb = openpyxl.load_workbook(excel_path, data_only=True)

def parse_date(d_val):
    if not d_val:
        return None
    if isinstance(d_val, datetime):
        return d_val.date()
    if isinstance(d_val, date):
        return d_val
    d_str = str(d_val).strip()
    parts = d_str.split('/')
    if len(parts) == 2:
        try:
            return date(2026, int(parts[1]), int(parts[0]))
        except ValueError:
            return None
    elif len(parts) == 3:
        try:
            year = int(parts[2])
            if year < 100:
                year += 2000
            return date(year, int(parts[1]), int(parts[0]))
        except ValueError:
            return None
    return None

def normalize_class_name(name):
    if not name:
        return ""
    name_str = str(name).strip()
    if '(' in name_str:
        name_str = name_str.split('(')[0].strip()
    for suffix in ['_HK2', '_HL', '-HL', '\t', ' - cũ', '_GL']:
        if name_str.endswith(suffix):
            name_str = name_str[:-len(suffix)].strip()
    name_str = name_str.replace("KS25", "K25").replace("KS24", "K24").replace("KS23", "K23")
    return name_str

def build_class_timelines(workbook):
    timelines = defaultdict(lambda: defaultdict(list))
    active_sheets = []
    for s_name in workbook.sheetnames:
        if s_name.lower() == 'sheet1':
            continue
        if any(k in s_name for k in ['KS24', 'KS25', 'SKL']):
            active_sheets.append(s_name)
            
    for sheetname in active_sheets:
        sheet = workbook[sheetname]
        row3 = list(sheet.iter_rows(min_row=3, max_row=3, values_only=True))[0]
        
        dates_list = []
        current_date = None
        for c_idx in range(3, len(row3)):
            col_letter = get_column_letter(c_idx + 1)
            dim = sheet.column_dimensions.get(col_letter)
            if dim and dim.hidden:
                continue
            val3 = row3[c_idx]
            if val3:
                current_date = parse_date(val3)
            if current_date:
                dates_list.append((c_idx, current_date))
                
        for r in range(5, sheet.max_row + 1):
            cname = sheet.cell(row=r, column=2).value
            if cname:
                cname_str = str(cname).strip()
                current_class = normalize_class_name(cname_str)
                for c_idx, d in dates_list:
                    val = sheet.cell(row=r, column=c_idx + 1).value
                    if val is not None:
                        if d not in timelines[current_class][sheetname]:
                            timelines[current_class][sheetname].append(d)
                            
    sorted_timelines = {}
    for cls, sheets_dict in timelines.items():
        sorted_timelines[cls] = {}
        for s_name, date_list in sheets_dict.items():
            sorted_timelines[cls][s_name] = sorted(list(set(date_list)))
            
    return sorted_timelines

def test_build_class_timelines(workbook):
    timelines = build_class_timelines(workbook)
    assert isinstance(timelines, dict), "Timeline map must be a dictionary"
    assert len(timelines) > 0, "Timelines should not be empty"
    print("test_build_class_timelines: PASS")

test_build_class_timelines(wb)

def get_compare_date_range(class_name, sheet_curr, monday_curr, timelines):
    subject_dates = timelines.get(class_name, {}).get(sheet_curr, [])
    past_dates = [d for d in subject_dates if d < monday_curr]
    
    if past_dates:
        last_date = max(past_dates)
        monday_prev = last_date - timedelta(days=last_date.weekday())
        sunday_prev = monday_prev + timedelta(days=6)
        return monday_prev, sunday_prev, sheet_curr, False
        
    other_subjects = timelines.get(class_name, {})
    candidates = []
    for s_name, date_list in other_subjects.items():
        if s_name == sheet_curr:
            continue
        past_subj_dates = [d for d in date_list if d < monday_curr]
        if past_subj_dates:
            candidates.append((max(past_subj_dates), s_name))
            
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        last_date, sheet_prev = candidates[0]
        monday_prev = last_date - timedelta(days=last_date.weekday())
        sunday_prev = monday_prev + timedelta(days=6)
        return monday_prev, sunday_prev, sheet_prev, True
        
    return None, None, None, True

def test_get_compare_date_range():
    mock_timelines = {
        'TEST-CLASS': {
            'SubjectA': [date(2026, 7, 10), date(2026, 7, 15)],
            'SubjectB': [date(2026, 8, 11), date(2026, 8, 14)]
        }
    }
    m_p, s_p, s_prev, is_new = get_compare_date_range('TEST-CLASS', 'SubjectA', date(2026, 7, 16), mock_timelines)
    assert s_prev == 'SubjectA'
    assert not is_new
    assert m_p == date(2026, 7, 13)
    
    m_p, s_p, s_prev, is_new = get_compare_date_range('TEST-CLASS', 'SubjectB', date(2026, 8, 10), mock_timelines)
    assert s_prev == 'SubjectA'
    assert is_new
    assert m_p == date(2026, 7, 13)
    
    print("test_get_compare_date_range: PASS")

test_get_compare_date_range()

def get_max_excel_date(wb, sheets):
    all_dates = []
    for sheetname in sheets:
        if sheetname not in wb.sheetnames:
            continue
        sheet = wb[sheetname]
        row3 = list(sheet.iter_rows(min_row=3, max_row=3, values_only=True))[0]
        for val in row3:
            parsed = parse_date(val)
            if parsed:
                all_dates.append(parsed)
    return max(all_dates) if all_dates else date(2026, 7, 17)

active_sheets = []
for s_name in wb.sheetnames:
    if s_name.lower() == 'sheet1':
        continue
    if any(k in s_name for k in ['KS24', 'KS25', 'SKL']):
        active_sheets.append(s_name)
max_date = get_max_excel_date(wb, active_sheets)
monday_curr = max_date - timedelta(days=max_date.weekday())
sunday_curr = monday_curr + timedelta(days=6)

monday_prev = monday_curr - timedelta(days=7)
sunday_prev = monday_prev + timedelta(days=6)

start_prev = monday_prev
end_prev = sunday_prev
start_curr = monday_curr
end_curr = sunday_curr

print(f"Tự động phát hiện tuần báo cáo: {start_curr.strftime('%d/%m')} - {end_curr.strftime('%d/%m/%Y')}")
print(f"Tuần đối chiếu: {start_prev.strftime('%d/%m')} - {end_prev.strftime('%d/%m/%Y')}")

weekly_groups = {
    'KS25_CNTT_HN': {
        'classes': ['HN-K25-CNTT1', 'HN-K25-CNTT2', 'HN-K25-CNTT3', 'HN-K25-CNTT4', 'HN-K25-CNTT5', 'HN-K25-CNTT6'],
        'sheet_curr': 'KS25_Python_Web',
        'sheet_prev': 'KS25_Python_Web',
        'label': 'Khóa KS25 CNTT Hà Nội (Python Web)'
    },
    'KS25_CNTT_HCM': {
        'classes': ['HCM-K25-CNTT5', 'HCM-K25-CNTT6', 'HCM-K25-CNTT7', 'HCM-K25-CNTT8'],
        'sheet_curr': 'KS25_Python_Web',
        'sheet_prev': 'KS25_Python_Web',
        'label': 'Khóa KS25 CNTT TP. HCM (Python Web)'
    },
    'KS25_QTKD_HN': {
        'classes': ['HN-K25-QTKD1', 'HN-K25-QTKD2', 'HN-K25-QTKD3'],
        'sheet_curr': 'KS25_QTKD_BA201',
        'sheet_prev': 'KS25_QTKD_PRJ302',
        'label': 'Khóa KS25 QTKD Hà Nội (BA201 / PRJ302)'
    },
    'KS24_CNTT_HN': {
        'classes': ['HN-K24-CNTT1', 'HN-K24-CNTT2', 'HN-K24-CNTT3', 'HN-K24-CNTT4', 'HN-K24-CNTT5'],
        'sheet_curr': 'KS24_AI_Intergration',
        'sheet_prev': 'KS24_AI',
        'label': 'Khóa KS24 CNTT Hà Nội (AI Integration / AI)'
    },
    'KS24_CNTT_HCM': {
        'classes': ['HCM-K24-CNTT1', 'HCM-K24-CNTT2'],
        'sheet_curr': 'KS24_AI_Intergration',
        'sheet_prev': 'KS24_AI',
        'label': 'Khóa KS24 CNTT TP. HCM (AI Integration / AI)'
    }
}

def format_weekly_cell(curr_val, prev_val):
    diff = curr_val - prev_val
    if diff > 0.05:
        return f"{curr_val:.2f}% <span style='color:#ef4444; font-weight:600;'>(▲ +{diff:.2f}%)</span>"
    elif diff < -0.05:
        return f"{curr_val:.2f}% <span style='color:#10b981; font-weight:600;'>(▼ {diff:.2f}%)</span>"
    else:
        return f"{curr_val:.2f}% <span style='color:#64748b;'>(--)</span>"

def get_weekly_metrics(sheetname, classes_target, start_date, end_date):
    if sheetname not in wb.sheetnames:
        return {}
    sheet = wb[sheetname]
    row3 = list(sheet.iter_rows(min_row=3, max_row=3, values_only=True))[0]
    row4 = list(sheet.iter_rows(min_row=4, max_row=4, values_only=True))[0]
    
    dates_list = []
    current_date = None
    for c_idx in range(3, len(row3)):
        col_letter = get_column_letter(c_idx + 1)
        dim = sheet.column_dimensions.get(col_letter)
        if dim and dim.hidden:
            continue
        val3 = row3[c_idx]
        val4 = row4[c_idx]
        if val3:
            current_date = parse_date(val3)
        if current_date and start_date <= current_date <= end_date:
            dates_list.append((c_idx, current_date, val4))
            
    res = {}
    current_class = None
    for r in range(5, sheet.max_row + 1):
        cname = sheet.cell(row=r, column=2).value
        teacher_val = sheet.cell(row=r, column=3).value
        
        if cname:
            cname_str = str(cname).strip()
            current_class = normalize_class_name(cname_str)
            size = extract_class_size(cname_str)
            class_sizes[current_class] = size
            
            matched_class = None
            for tc in classes_target:
                if tc == current_class:
                    matched_class = tc
                    break
            if not matched_class:
                continue
                
            teacher_name = str(teacher_val).strip() if teacher_val else "N/A"
            
            tg_name = "N/A"
            if r + 1 <= sheet.max_row:
                next_c2 = sheet.cell(row=r+1, column=2).value
                next_c3 = sheet.cell(row=r+1, column=3).value
                if not next_c2 and next_c3:
                    tg_name = str(next_c3).strip()
                    
            day_vals = defaultdict(list)
            for c_idx, d, val4 in dates_list:
                val = sheet.cell(row=r, column=c_idx + 1).value
                if val is not None:
                    try:
                        day_vals[val4].append(float(val))
                    except ValueError:
                        pass
                        
            averages = {}
            for metric in ['Chuyên cần', 'Bài tập', 'Elearning']:
                vals = day_vals.get(metric, [])
                averages[metric] = sum(vals) / len(vals) if vals else 0.0
                
            res[matched_class] = {
                'teacher': teacher_name,
                'tg': tg_name,
                'metrics': averages
            }
    return res

timelines = build_class_timelines(wb)

weekly_stats = {}
for gkey, ginfo in weekly_groups.items():
    classes = ginfo['classes']
    curr_data = get_weekly_metrics(ginfo['sheet_curr'], classes, start_curr, end_curr)
    
    prev_data = {}
    for cls in classes:
        # Default empty comparison metrics
        prev_data[cls] = {
            'teacher': 'N/A',
            'tg': 'N/A',
            'metrics': {'Chuyên cần': 0.0, 'Bài tập': 0.0, 'Elearning': 0.0}
        }
        m_prev, s_prev_date, sheet_prev, is_new = get_compare_date_range(cls, ginfo['sheet_curr'], start_curr, timelines)
        if m_prev and s_prev_date and sheet_prev:
            cls_prev_metrics = get_weekly_metrics(sheet_prev, [cls], m_prev, s_prev_date)
            if cls in cls_prev_metrics:
                prev_data[cls] = cls_prev_metrics[cls]
                
    weekly_stats[gkey] = {
        'label': ginfo['label'],
        'classes': classes,
        'curr': curr_data,
        'prev': prev_data
    }

all_sheets = []
for s_name in wb.sheetnames:
    if s_name.lower() == 'sheet1':
        continue
    if any(k in s_name for k in ['KS24', 'KS25', 'SKL']):
        all_sheets.append(s_name)

class_course_data = defaultdict(dict)
teacher_stats = {}

for sheetname in all_sheets:
    if sheetname not in wb.sheetnames:
        continue
    sheet = wb[sheetname]
    row3 = list(sheet.iter_rows(min_row=3, max_row=3, values_only=True))[0]
    row4 = list(sheet.iter_rows(min_row=4, max_row=4, values_only=True))[0]
    
    dates_list = []
    current_date = None
    for c_idx in range(3, len(row3)):
        col_letter = get_column_letter(c_idx + 1)
        dim = sheet.column_dimensions.get(col_letter)
        if dim and dim.hidden:
            continue
        val3 = row3[c_idx]
        val4 = row4[c_idx]
        if val3:
            current_date = parse_date(val3)
        if current_date:
            dates_list.append((c_idx, current_date, val4))
            
    current_class = None
    gv_cc_vals, gv_bt_vals, gv_el_vals = [], [], []
    tg_cc_vals, tg_bt_vals, tg_el_vals = [], [], []
    current_gv_name = None
    current_tg_name = None
    
    for r in range(5, sheet.max_row + 1):
        cname = sheet.cell(row=r, column=2).value
        teacher_tg_val = sheet.cell(row=r, column=3).value
        teacher_tg_name = str(teacher_tg_val).strip() if teacher_tg_val else ""
        
        if cname:
            cname_str = str(cname).strip()
            current_class = normalize_class_name(cname_str)
            size = extract_class_size(cname_str)
            class_sizes[current_class] = size
            role = 'GV'
            current_gv_name = teacher_tg_name
            gv_cc_vals, gv_bt_vals, gv_el_vals = [], [], []
            
            for c_idx, d, val4 in dates_list:
                val = sheet.cell(row=r, column=c_idx + 1).value
                if val is not None:
                    try:
                        val_f = float(val)
                        if val4 == 'Chuyên cần': gv_cc_vals.append(val_f)
                        elif val4 == 'Bài tập': gv_bt_vals.append(val_f)
                        elif val4 == 'Elearning': gv_el_vals.append(val_f)
                    except ValueError:
                        pass
        else:
            role = 'TG'
            current_tg_name = teacher_tg_name
            tg_cc_vals = gv_cc_vals.copy()
            tg_bt_vals = gv_bt_vals.copy()
            tg_el_vals = gv_el_vals.copy()
            
        if not current_class or teacher_tg_name in ['', 'None', 'Chưa phân công', 'Giảng viên/Trợ giảng']:
            continue
            
        name = teacher_tg_name
        dept = 'QTKD' if 'QTKD' in sheetname or 'QTKD' in current_class else 'CNTT'
        
        cc_vals = gv_cc_vals.copy() if role == 'GV' else tg_cc_vals.copy()
        bt_vals = gv_bt_vals.copy() if role == 'GV' else tg_bt_vals.copy()
        el_vals = gv_el_vals.copy() if role == 'GV' else tg_el_vals.copy()
        
        cc_avg = np.mean(cc_vals) if cc_vals else 0.0
        bt_avg = np.mean(bt_vals) if bt_vals else 0.0
        el_avg = np.mean(el_vals) if el_vals else 0.0
        
        class_course_data[(current_class, role)][sheetname] = {
            'cc_avg': cc_avg,
            'bt_avg': bt_avg,
            'el_avg': el_avg,
            'teacher': name,
            'min_date': min(d for c, d, s in dates_list) if dates_list else date.min
        }
        
        if name not in teacher_stats:
            teacher_stats[name] = {
                'role': role,
                'department': dept,
                'cc': [],
                'bt': [],
                'el': [],
                'classes': set(),
                'sheets': set()
            }
        teacher_stats[name]['classes'].add(current_class)
        teacher_stats[name]['sheets'].add(sheetname)
        if cc_vals: teacher_stats[name]['cc'].extend(cc_vals)
        if bt_vals: teacher_stats[name]['bt'].extend(bt_vals)
        if el_vals: teacher_stats[name]['el'].extend(el_vals)

transitions = []
for (cname, role), courses in sorted(class_course_data.items()):
    if len(courses) < 2:
        continue
    sorted_courses = sorted(courses.items(), key=lambda x: x[1]['min_date'])
    for i in range(1, len(sorted_courses)):
        prev_sheet, prev_data = sorted_courses[i-1]
        curr_sheet, curr_data = sorted_courses[i]
        
        delta_cc = prev_data['cc_avg'] - curr_data['cc_avg']
        delta_bt = prev_data['bt_avg'] - curr_data['bt_avg']
        delta_el = prev_data['el_avg'] - curr_data['el_avg']
        
        transitions.append({
            'class': cname,
            'role': role,
            'prev_sheet': prev_sheet,
            'prev_teacher': prev_data['teacher'],
            'prev_cc': prev_data['cc_avg'],
            'prev_bt': prev_data['bt_avg'],
            'prev_el': prev_data['el_avg'],
            'curr_sheet': curr_sheet,
            'curr_teacher': curr_data['teacher'],
            'curr_cc': curr_data['cc_avg'],
            'curr_bt': curr_data['bt_avg'],
            'curr_el': curr_data['el_avg'],
            'delta_cc': delta_cc,
            'delta_bt': delta_bt,
            'delta_el': delta_el
        })

evaluated_staff = []
watchlist_staff = []

for name, stats in teacher_stats.items():
    cc_mean = np.mean(stats['cc']) if stats['cc'] else 0.0
    bt_mean = np.mean(stats['bt']) if stats['bt'] else 0.0
    el_mean = np.mean(stats['el']) if stats['el'] else 0.0
    
    t_imps = [item for item in transitions if item['curr_teacher'] == name and item['role'] == stats['role']]
    
    if t_imps:
        cmi_values = []
        for class_item in t_imps:
            cmi_cc = 0.5 * class_item['prev_cc'] - class_item['curr_cc'] + 15.0
            cmi_bt = 0.5 * class_item['prev_bt'] - class_item['curr_bt'] + 15.0
            cmi_el = 0.5 * class_item['prev_el'] - class_item['curr_el'] + 15.0
            cmi_values.append((cmi_cc + cmi_bt + cmi_el) / 3.0)
            
        mgmt_score = np.mean(cmi_values)
        
        if mgmt_score > 12.0:
            classification = "Rescuers (Giải cứu xuất sắc)"
        elif mgmt_score < 0.0 or cc_mean > 25.0 or bt_mean > 20.0 or el_mean > 20.0:
            classification = "Cần Hỗ Trợ (Needs Support)"
        else:
            classification = "Duy trì (Maintainers)"
            
        avg_delta_cc = np.mean([item['delta_cc'] for item in t_imps])
        avg_delta_bt = np.mean([item['delta_bt'] for item in t_imps])
        avg_delta_el = np.mean([item['delta_el'] for item in t_imps])
        
        evaluated_staff.append({
            'name': name,
            'role': stats['role'],
            'dept': stats['department'],
            'classes_count': len(stats['classes']),
            'classes_list': ", ".join(list(stats['classes'])),
            'sheets_list': ", ".join(list(stats['sheets'])),
            'cc': cc_mean,
            'bt': bt_mean,
            'el': el_mean,
            'delta_cc': avg_delta_cc,
            'delta_bt': avg_delta_bt,
            'delta_el': avg_delta_el,
            'cmi': mgmt_score,
            'class': classification
        })
    else:
        watchlist_staff.append({
            'name': name,
            'role': stats['role'],
            'dept': stats['department'],
            'classes_count': len(stats['classes']),
            'classes_list': ", ".join(list(stats['classes'])),
            'sheets_list': ", ".join(list(stats['sheets'])),
            'cc': cc_mean,
            'bt': bt_mean,
        })

import json
trends_data = {
    'KS24_HN': {'courses': [], 'cc': [], 'bt': [], 'el': []},
    'KS24_HCM': {'courses': [], 'cc': [], 'bt': [], 'el': []},
    'HN': {'courses': [], 'cc': [], 'bt': [], 'el': []},
    'HCM': {'courses': [], 'cc': [], 'bt': [], 'el': []},
    'QTKD': {'courses': [], 'cc': [], 'bt': [], 'el': []}
}
cohort_sheets = {
    'KS24_HN': ['KS24-JavaAdvance', 'KS24_JavaWeb', 'KS24_JWS', 'KS24_AI', 'KS24_AI_Intergration'],
    'KS24_HCM': ['KS24-JavaAdvance', 'KS24_JavaWeb', 'KS24_JWS', 'KS24_AI', 'KS24_AI_Intergration'],
    'HN': ['KS25_Javascript', 'KS25_Database', 'KS25_Python', 'KS25_Python_Web'],
    'HCM': ['KS25_Javascript', 'KS25_Database', 'KS25_Python', 'KS25_Python_Web'],
    'QTKD': ['KS25_QTKD_M103', 'KS25_QTKD_M104', 'KS25_QTKD_DTB201', 'KS25_QTKD_DTB202', 'KS25_QTKD_PRJ302', 'KS25_QTKD_BA201']
}
for cohort, sheets in cohort_sheets.items():
    for sheetname in sheets:
        if sheetname not in wb.sheetnames:
            continue
        cc_weighted_sum, bt_weighted_sum, el_weighted_sum = 0.0, 0.0, 0.0
        total_students_cohort = 0
        
        for (cname, role), courses in class_course_data.items():
            if role != 'GV' or sheetname not in courses:
                continue
            if cohort == 'KS24_HN' and not ('HN' in cname and 'CNTT' in cname and 'K24' in cname): continue
            if cohort == 'KS24_HCM' and not ('HCM' in cname and 'CNTT' in cname and 'K24' in cname): continue
            if cohort == 'HN' and not ('HN' in cname and 'CNTT' in cname and 'K25' in cname): continue
            if cohort == 'HCM' and not ('HCM' in cname and 'CNTT' in cname and 'K25' in cname): continue
            if cohort == 'QTKD' and not 'QTKD' in cname: continue
            
            size = class_sizes.get(cname, 30)
            total_students_cohort += size
            cc_weighted_sum += courses[sheetname]['cc_avg'] * size
            bt_weighted_sum += courses[sheetname]['bt_avg'] * size
            el_weighted_sum += courses[sheetname]['el_avg'] * size
            
        course_name = sheetname.replace('KS24-', '').replace('KS24_', '').replace('KS25_', '').split('_')[-1]
        trends_data[cohort]['courses'].append(course_name)
        
        cc_avg = cc_weighted_sum / total_students_cohort if total_students_cohort > 0 else 0.0
        bt_avg = bt_weighted_sum / total_students_cohort if total_students_cohort > 0 else 0.0
        el_avg = el_weighted_sum / total_students_cohort if total_students_cohort > 0 else 0.0
        
        trends_data[cohort]['cc'].append(round(float(cc_avg), 2))
        trends_data[cohort]['bt'].append(round(float(bt_avg), 2))
        trends_data[cohort]['el'].append(round(float(el_avg), 2))

trends_data['compare'] = {}
for gkey, dict_key in [
    ('KS24_CNTT_HN', 'KS24_HN'),
    ('KS24_CNTT_HCM', 'KS24_HCM'),
    ('KS25_CNTT_HN', 'HN'),
    ('KS25_CNTT_HCM', 'HCM'),
    ('KS25_QTKD_HN', 'QTKD')
]:
    stats = weekly_stats.get(gkey, {'curr': {}, 'prev': {}})
    
    total_size_curr = 0
    weighted_cc_curr = 0.0
    weighted_bt_curr = 0.0
    weighted_el_curr = 0.0
    for cls, x in stats['curr'].items():
        size = class_sizes.get(cls, 30)
        total_size_curr += size
        weighted_cc_curr += x['metrics']['Chuyên cần'] * size
        weighted_bt_curr += x['metrics']['Bài tập'] * size
        weighted_el_curr += x['metrics']['Elearning'] * size
        
    curr_cc = weighted_cc_curr / total_size_curr if total_size_curr > 0 else 0.0
    curr_bt = weighted_bt_curr / total_size_curr if total_size_curr > 0 else 0.0
    curr_el = weighted_el_curr / total_size_curr if total_size_curr > 0 else 0.0
    
    total_size_prev = 0
    weighted_cc_prev = 0.0
    weighted_bt_prev = 0.0
    weighted_el_prev = 0.0
    for cls, x in stats['prev'].items():
        size = class_sizes.get(cls, 30)
        total_size_prev += size
        weighted_cc_prev += x['metrics']['Chuyên cần'] * size
        weighted_bt_prev += x['metrics']['Bài tập'] * size
        weighted_el_prev += x['metrics']['Elearning'] * size
        
    prev_cc = weighted_cc_prev / total_size_prev if total_size_prev > 0 else 0.0
    prev_bt = weighted_bt_prev / total_size_prev if total_size_prev > 0 else 0.0
    prev_el = weighted_el_prev / total_size_prev if total_size_prev > 0 else 0.0
    
    trends_data['compare'][dict_key] = {
        'curr': [round(float(curr_cc), 2), round(float(curr_bt), 2), round(float(curr_el), 2)],
        'prev': [round(float(prev_cc), 2), round(float(prev_bt), 2), round(float(prev_el), 2)]
    }

with open('data/processed/historical_trends.json', 'w', encoding='utf-8') as f:
    json.dump(trends_data, f, ensure_ascii=False, indent=4)

markdown_content = f"""# BÁO CÁO THỐNG KÊ CHỈ SỐ ĐÀO TẠO TUẦN & NĂNG LỰC QUẢN TRỊ LỚP CỦA GV/TG

<div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 12px 20px; border-radius: 8px; display: inline-block; font-weight: 600; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);">
  <i class="fas fa-calendar-check" style="margin-right: 8px;"></i> Báo cáo Tuần: {start_curr.strftime('%d/%m/%Y')} - {end_curr.strftime('%d/%m/%Y')}
</div>
"""

markdown_content += "\n"

def generate_kpi_card(title, curr_val, prev_val):
    diff = curr_val - prev_val
    trend_class = "trend-bad" if diff > 0 else "trend-good"
    arrow = "▲" if diff > 0 else "▼" if diff < 0 else "-"
    diff_str = f"{diff:+.2f}%" if diff != 0 else "0.00%"
    return f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{curr_val:.2f}%</div>
        <div class="kpi-trend {trend_class}">{arrow} {diff_str} so với tuần trước</div>
    </div>
    """

def generate_cohort_section(cohort_id, weekly_stats_group):
    # Calculate weighted averages
    curr_vals = {}
    prev_vals = {}
    for m in ['Chuyên cần', 'Bài tập', 'Elearning']:
        total_size_curr = 0
        weighted_sum_curr = 0.0
        for cls, x in weekly_stats_group['curr'].items():
            size = class_sizes.get(cls, 30)
            total_size_curr += size
            weighted_sum_curr += x['metrics'][m] * size
        curr_vals[m] = weighted_sum_curr / total_size_curr if total_size_curr > 0 else 0.0
        
        total_size_prev = 0
        weighted_sum_prev = 0.0
        for cls, x in weekly_stats_group['prev'].items():
            size = class_sizes.get(cls, 30)
            total_size_prev += size
            weighted_sum_prev += x['metrics'][m] * size
        prev_vals[m] = weighted_sum_prev / total_size_prev if total_size_prev > 0 else 0.0
    
    cc_diff_overall = curr_vals['Chuyên cần'] - prev_vals['Chuyên cần']
    bt_diff_overall = curr_vals['Bài tập'] - prev_vals['Bài tập']
    el_diff_overall = curr_vals['Elearning'] - prev_vals['Elearning']
    
    issues = []
    if cc_diff_overall > 2.0: issues.append(f"Tỷ lệ vắng mặt chuyên cần tăng mạnh (+{cc_diff_overall:.2f}%) so với tuần trước.")
    if bt_diff_overall > 2.0: issues.append(f"Tỷ lệ nợ bài tập có dấu hiệu đáng báo động (+{bt_diff_overall:.2f}%).")
    if el_diff_overall > 2.0: issues.append(f"Học viên đang lơ là Elearning (+{el_diff_overall:.2f}%).")
    
    ai_insights = ""
    if issues:
        ai_insights = f"""
<div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; margin: 20px 0; backdrop-filter: blur(10px);">
    <h4 style="margin-top:0; color:#e2e8f0; display:flex; align-items:center; gap:8px;">
        <span style="font-size:1.2rem;">📌</span> Kế hoạch Hành động Khắc phục (Hệ thống đề xuất)
    </h4>
    <div style="display: flex; gap: 16px; margin-top: 16px; flex-wrap: wrap;">
        <div style="flex:1; min-width: 250px; background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 12px; border-radius: 4px;">
            <div style="color: #fca5a5; font-weight: 600; margin-bottom: 8px;">🚨 Vấn đề phát hiện</div>
            <ul style="margin:0; padding-left:20px; color:#e2e8f0; font-size:0.9rem;">
                {''.join(f'<li>{i}</li>' for i in issues)}
            </ul>
        </div>
        <div style="flex:1; min-width: 250px; background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 12px; border-radius: 4px;">
            <div style="color: #6ee7b7; font-weight: 600; margin-bottom: 8px;">💡 Hành động yêu cầu</div>
            <ul style="margin:0; padding-left:20px; color:#e2e8f0; font-size:0.9rem;">
                <li>Chỉ đạo Trợ giảng liên hệ ngay sinh viên vi phạm để đôn đốc.</li>
                <li>Giảng viên cần chấn chỉnh kỷ luật lớp đầu giờ học tiếp theo.</li>
            </ul>
        </div>
    </div>
</div>
"""
    else:
        ai_insights = f"""
<div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 16px; margin: 20px 0; display: flex; align-items: center; gap: 12px;">
    <span style="font-size: 1.5rem;">✅</span>
    <div>
        <strong style="color: #6ee7b7;">Đánh giá chung:</strong> Kỷ luật học tập của khóa {cohort_id} duy trì ổn định so với tuần trước. Không cần can thiệp khẩn cấp.
    </div>
</div>
"""
    
    html = f"""
---
### Khóa {cohort_id}

{ai_insights}

<div class="data-grid-container" markdown="1">

| Tên Lớp | Giảng viên | Trợ giảng | Chuyên cần | Bài tập | Elearning | Xu hướng |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
"""
    for cls in weekly_stats_group['classes']:
        curr_info = weekly_stats_group['curr'].get(cls, {'metrics': {'Chuyên cần': 0.0, 'Bài tập': 0.0, 'Elearning': 0.0}, 'teacher': 'N/A', 'tg': 'N/A'})
        prev_info = weekly_stats_group['prev'].get(cls, {'metrics': {'Chuyên cần': 0.0, 'Bài tập': 0.0, 'Elearning': 0.0}})
        c_m, p_m = curr_info['metrics'], prev_info['metrics']
        cc_cell = format_weekly_cell(c_m['Chuyên cần'], p_m['Chuyên cần'])
        bt_cell = format_weekly_cell(c_m['Bài tập'], p_m['Bài tập'])
        el_cell = format_weekly_cell(c_m['Elearning'], p_m['Elearning'])
        cc_diff = c_m['Chuyên cần'] - p_m['Chuyên cần']
        bt_diff = c_m['Bài tập'] - p_m['Bài tập']
        el_diff = c_m['Elearning'] - p_m['Elearning']
        
        status_html = "<span class='badge badge-danger'>🚨 Tăng</span>" if (cc_diff > 1.0 or bt_diff > 1.0 or el_diff > 1.0) else "<span class='badge badge-success'>✅ Ổn định</span>"
        html += f"| **{cls}** | {curr_info['teacher']} | {curr_info['tg']} | {cc_cell} | {bt_cell} | {el_cell} | {status_html} |\n"
    
    html += """
</div>
"""
    return html

markdown_content += generate_cohort_section('HN-KS24-CNTT', weekly_stats['KS24_CNTT_HN'])
markdown_content += generate_cohort_section('HCM-KS24-CNTT', weekly_stats['KS24_CNTT_HCM'])
markdown_content += generate_cohort_section('HN-KS25-CNTT', weekly_stats['KS25_CNTT_HN'])
markdown_content += generate_cohort_section('HCM-KS25-CNTT', weekly_stats['KS25_CNTT_HCM'])
markdown_content += generate_cohort_section('HN-KS25-QTKD', weekly_stats['KS25_QTKD_HN'])


markdown_content += r"""
## II. ĐÁNH GIÁ NĂNG LỰC QUẢN TRỊ LỚP TÍCH LŨY CỦA GIẢNG VIÊN VÀ TRỢ GIẢNG (CMI HISTORICAL RANKING)

<div class="quote-box" style="margin-bottom: 30px;" markdown="1">
<h3 style="margin-top: 0; color: #60a5fa;"><i class="fas fa-calculator"></i> 3 Bước Đánh Giá CMI</h3>
<ul style="margin-bottom: 0;">
<li style="margin-bottom: 8px;"><b>1. Trọng số:</b> Tính theo công thức <code>50% Tỷ lệ lỗi cũ - 100% Tỷ lệ lỗi mới + Điểm nền (15)</code>.</li>
<li style="margin-bottom: 8px;"><b>2. Ý nghĩa:</b> Điểm càng cao (>12) ➔ Khắc phục lỗi càng tốt (Giải cứu xuất sắc).</li>
<li><b>3. Phân loại:</b> Nếu điểm dưới 0 hoặc vi phạm hiện tại quá cao (CC > 25%, BT > 20%, EL > 20%) ➔ <b>Cần Hỗ Trợ</b>.</li>
</ul>
</div>

### 🏆 Bảng xếp hạng Top 5 Giảng viên xuất sắc (Giảng viên phụ trách)

| Hạng | Họ và Tên | Tổng số lớp đã dạy | Chỉ số CMI tích lũy | Phân loại |
| :---: | :--- | :---: | :---: | :--- |
"""

all_gv = [x for x in evaluated_staff if x['role'] == 'GV']
all_gv = sorted(all_gv, key=lambda x: x['cmi'], reverse=True)[:5]

rank = 1
for item in all_gv:
    markdown_content += f"| {rank} | **{item['name']}** | {item['classes_count']} lớp | **{item['cmi']:+.2f}%** | {item['class']} |\n"
    rank += 1

markdown_content += """
### 🏆 Bảng xếp hạng Top 5 Trợ giảng xuất sắc (Trợ giảng phụ trách)

| Hạng | Họ và Tên | Tổng số lớp đã dạy | Chỉ số CMI tích lũy | Phân loại |
| :---: | :--- | :---: | :---: | :--- |
"""

all_tg = [x for x in evaluated_staff if x['role'] == 'TG']
all_tg = sorted(all_tg, key=lambda x: x['cmi'], reverse=True)[:5]

rank = 1
for item in all_tg:
    markdown_content += f"| {rank} | **{item['name']}** | {item['classes_count']} lớp | **{item['cmi']:+.2f}%** | {item['class']} |\n"
    rank += 1

def generate_staff_card(item):
    badge_color = "#10b981" if "Giải cứu" in item['class'] else "#3b82f6" if "Duy trì" in item['class'] else "#ef4444"
    icon = "fa-star" if "Giải cứu" in item['class'] else "fa-check-circle" if "Duy trì" in item['class'] else "fa-exclamation-triangle"
    
    weakness = "N/A"
    solution = "N/A"
    if item['delta_cc'] < -2.0: 
        weakness = "Tỷ lệ vắng mặt tăng"
        solution = "Gắt gao điểm danh và liên hệ học viên"
    elif item['delta_bt'] < -2.0:
        weakness = "Học viên lười làm bài tập"
        solution = "Chữa bài tập kỹ hơn, giao task nhỏ gọn hơn"
    elif item['delta_el'] < -2.0:
        weakness = "Chậm tiến độ Elearning"
        solution = "Nhắc nhở học viên làm Elearning ngay trên lớp"
    elif "Giải cứu" in item['class']:
        weakness = "Không có (Kỷ luật cực tốt)"
        solution = "Duy trì phong độ và chia sẻ kinh nghiệm cho nhóm"
    else:
        weakness = "Kỷ luật ở mức trung bình ổn"
        solution = "Cải thiện động lực học của sinh viên yếu kém"

    card = f"""<div class="staff-card" style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 16px;">
<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 12px; margin-bottom: 12px;">
<div>
<h4 style="margin: 0; color: #f8fafc; font-size: 1.1rem;">{item['name']}</h4>
<div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Vai trò: {item['role']} - {item['classes_count']} Lớp ({item['classes_list']})</div>
</div>
<div style="background: {badge_color}20; color: {badge_color}; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">
<i class="fas {icon}"></i> {item['class']}
</div>
</div>
<div style="display: flex; gap: 12px; font-size: 0.85rem;">
<div style="flex: 1;">
<div style="color: #ef4444; font-weight: 600; margin-bottom: 4px;"><i class="fas fa-arrow-down"></i> Điểm Yếu</div>
<div style="color: #cbd5e1;">{weakness}</div>
</div>
<div style="flex: 1;">
<div style="color: #10b981; font-weight: 600; margin-bottom: 4px;"><i class="fas fa-lightbulb"></i> Đề Xuất</div>
<div style="color: #cbd5e1;">{solution}</div>
</div>
</div>
</div>
"""
    return card

evaluated_cntt = []
evaluated_qtkd = []
for item in evaluated_staff:
    classes_str = item['classes_list'].upper()
    if 'QTKD' in classes_str:
        evaluated_qtkd.append(item)
    else:
        evaluated_cntt.append(item)

markdown_content += """
---

## III. ĐÁNH GIÁ CHI TIẾT TỪNG NHÂN SỰ VÀ ĐỀ XUẤT CẢI THIỆN
"""

# Khối CNTT
markdown_content += "\n### 💻 Khối Công nghệ Thông tin (CNTT)\n"
html_cards_cntt = "<div class='staff-grid' style='display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; margin-top: 15px; margin-bottom: 30px;' markdown='1'>\n"
for item in sorted(evaluated_cntt, key=lambda x: x['cmi'], reverse=True):
    html_cards_cntt += generate_staff_card(item)
html_cards_cntt += "</div>\n"
markdown_content += html_cards_cntt

# Khối QTKD
markdown_content += "\n### 📊 Khối Quản trị Kinh doanh (QTKD)\n"
html_cards_qtkd = "<div class='staff-grid' style='display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; margin-top: 15px; margin-bottom: 30px;' markdown='1'>\n"
for item in sorted(evaluated_qtkd, key=lambda x: x['cmi'], reverse=True):
    html_cards_qtkd += generate_staff_card(item)
html_cards_qtkd += "</div>\n"
markdown_content += html_cards_qtkd


# Lưu báo cáo
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(markdown_content)

print(f"Agent 1: Báo cáo đã được ghi đè thành công tại {output_path}")
wb.close()

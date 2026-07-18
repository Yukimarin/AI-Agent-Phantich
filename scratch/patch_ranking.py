import re
import os

filepath = "scratch/generate_kpi_ranking.py"

with open(filepath, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Inject import json and violations data loading
load_violation_code = """# Load operational violations
violations_data = []
violation_path = "data/vi_pham_gvtg.json"
if os.path.exists(violation_path):
    try:
        with open(violation_path, "r", encoding="utf-8") as f:
            violations_data = json.load(f)
        print(f"Loaded {len(violations_data)} operational violations.")
    except Exception as e:
        print(f"Error loading violations json: {e}")"""

# We insert this after predictions_data loading (around line 169)
code = code.replace(
    "print(f\"File not found: {PRED_JSON_PATH}\")",
    "print(f\"File not found: {PRED_JSON_PATH}\")\n\n" + load_violation_code
)

# 2. Correct TA metrics reading logic (use val_t instead of val_ta to fix the blank cells bug)
old_ta_read = """            # For TA
            if is_ta_valid and isinstance(val_ta, (int, float)):
                val_float_ta = float(val_ta)
                if sub == 'Chuyên cần': cc_ta.append(val_float_ta)
                elif sub == 'Bài tập': bt_ta.append(val_float_ta)
                elif sub == 'Elearning': el_ta.append(val_float_ta)"""

new_ta_read = """            # For TA (take class metrics from teacher row r to prevent blank cell bias)
            if is_ta_valid and isinstance(val_t, (int, float)):
                val_float_t = float(val_t)
                if sub == 'Chuyên cần': cc_ta.append(val_float_t)
                elif sub == 'Bài tập': bt_ta.append(val_float_t)
                elif sub == 'Elearning': el_ta.append(val_float_t)"""

code = code.replace(old_ta_read, new_ta_read)

# 3. Replace WEIGHTS definition with WEIGHTS_V2 definition
old_weights = """# Define standard weights based on Rank category
WEIGHTS = {
    'TA': { # Rank 1-2
        'tuanchu': 0.10, 'kyluat': 0.05, 'hoclieu': 0.05,
        'siso': 0.10, 'dondoc': 0.10, 'phoihop': 0.05,
        'giaiquyet': 0.10, 'daura': 0.10, 'phattrien': 0.05,
        'truyendat_dugio': 0.05, 'truyendat_uprank': 0.15,
        'csat': 0.05, 'hoclieu_duyet': 0.05,
        'toiuu_ct': 0.0, 'hieusuat_duoi': 0.0, 'thuonghieu': 0.0, 'sangkien': 0.0
    },
    'GV': { # Rank 3-4
        'tuanchu': 0.05, 'kyluat': 0.05, 'hoclieu': 0.05,
        'siso': 0.10, 'dondoc': 0.10, 'phoihop': 0.05,
        'giaiquyet': 0.10, 'daura': 0.10, 'phattrien': 0.05,
        'truyendat_dugio': 0.10, 'truyendat_uprank': 0.15,
        'csat': 0.05, 'hoclieu_duyet': 0.05,
        'toiuu_ct': 0.0, 'hieusuat_duoi': 0.0, 'thuonghieu': 0.0, 'sangkien': 0.0
    },
    'PM': { # Rank 5-6 (Subject/Program Manager)
        'tuanchu': 0.05, 'kyluat': 0.02, 'hoclieu': 0.03,
        'siso': 0.05, 'dondoc': 0.05, 'phoihop': 0.05,
        'giaiquyet': 0.10, 'daura': 0.05, 'phattrien': 0.05,
        'truyendat_dugio': 0.02, 'truyendat_uprank': 0.05,
        'csat': 0.05, 'hoclieu_duyet': 0.03,
        'toiuu_ct': 0.10, 'hieusuat_duoi': 0.15, 'thuonghieu': 0.05, 'sangkien': 0.10
    },
    'Lead': { # Rank 7-8 (Lãnh đạo khối / GĐ Đào tạo)
        'tuanchu': 0.02, 'kyluat': 0.01, 'hoclieu': 0.02,
        'siso': 0.02, 'dondoc': 0.02, 'phoihop': 0.01,
        'giaiquyet': 0.05, 'daura': 0.03, 'phattrien': 0.02,
        'truyendat_dugio': 0.0, 'truyendat_uprank': 0.05,
        'csat': 0.03, 'hoclieu_duyet': 0.02,
        'toiuu_ct': 0.15, 'hieusuat_duoi': 0.20, 'thuonghieu': 0.10, 'sangkien': 0.25
    }
}"""

new_weights = """# Define standard weights based on Rank category (V2 Updated Standard)
WEIGHTS = {
    'TA': { # Rank 1-2
        'tuanchu': 0.10, 'kyluat': 0.10, 'hoclieu': 0.10, 'phoihop': 0.05,
        'siso': 0.15, 'el': 0.10, 'bt': 0.05,
        'giaiquyet': 0.05, 'pass_rate': 0.05, 'kha_gioi': 0.05,
        'cc_cn': 0.02, 'bang_cap': 0.03,
        'truyendat_dugio': 0.0, 'truyendat_uprank': 0.0,
        'csat': 0.05, 'hoclieu_duyet': 0.10,
        'toiuu_ct': 0.0, 'hieusuat_duoi': 0.0, 'thuonghieu': 0.0, 'sangkien': 0.0
    },
    'GV': { # Rank 3-4
        'tuanchu': 0.10, 'kyluat': 0.05, 'hoclieu': 0.05, 'phoihop': 0.05,
        'siso': 0.10, 'el': 0.05, 'bt': 0.05,
        'giaiquyet': 0.10, 'pass_rate': 0.05, 'kha_gioi': 0.05,
        'cc_cn': 0.02, 'bang_cap': 0.03,
        'truyendat_dugio': 0.10, 'truyendat_uprank': 0.10,
        'csat': 0.05, 'hoclieu_duyet': 0.05,
        'toiuu_ct': 0.0, 'hieusuat_duoi': 0.0, 'thuonghieu': 0.0, 'sangkien': 0.0
    },
    'QL': { # Rank 5-6 (Quản lý)
        'tuanchu': 0.05, 'kyluat': 0.02, 'hoclieu': 0.03, 'phoihop': 0.05,
        'siso': 0.05, 'el': 0.03, 'bt': 0.02,
        'giaiquyet': 0.10, 'pass_rate': 0.03, 'kha_gioi': 0.02,
        'cc_cn': 0.02, 'bang_cap': 0.03,
        'truyendat_dugio': 0.02, 'truyendat_uprank': 0.05,
        'csat': 0.05, 'hoclieu_duyet': 0.03,
        'toiuu_ct': 0.15, 'hieusuat_duoi': 0.10, 'thuonghieu': 0.10, 'sangkien': 0.05
    },
    'TH': { # Rank 5-6 (GV Thương hiệu)
        'tuanchu': 0.05, 'kyluat': 0.05, 'hoclieu': 0.03, 'phoihop': 0.02,
        'siso': 0.05, 'el': 0.03, 'bt': 0.02,
        'giaiquyet': 0.10, 'pass_rate': 0.05, 'kha_gioi': 0.05,
        'cc_cn': 0.02, 'bang_cap': 0.03,
        'truyendat_dugio': 0.10, 'truyendat_uprank': 0.10,
        'csat': 0.05, 'hoclieu_duyet': 0.05,
        'toiuu_ct': 0.20, 'hieusuat_duoi': 0.0, 'thuonghieu': 0.10, 'sangkien': 0.0
    },
    'Lead': { # Rank 7-8
        'tuanchu': 0.02, 'kyluat': 0.01, 'hoclieu': 0.02, 'phoihop': 0.01,
        'siso': 0.02, 'el': 0.01, 'bt': 0.01,
        'giaiquyet': 0.05, 'pass_rate': 0.02, 'kha_gioi': 0.01,
        'cc_cn': 0.01, 'bang_cap': 0.01,
        'truyendat_dugio': 0.0, 'truyendat_uprank': 0.05,
        'csat': 0.03, 'hoclieu_duyet': 0.02,
        'toiuu_ct': 0.10, 'hieusuat_duoi': 0.25, 'thuonghieu': 0.15, 'sangkien': 0.20
    }
}"""

code = code.replace(old_weights, new_weights)

# 4. Replace rank mapping to include 'TH' class
old_rank_map = """    # Determine rank category for weights
    if rank_val in (1, 2):
        w_cat = 'TA'
    elif rank_val in (3, 4):
        w_cat = 'GV'
    elif rank_val in (5, 6):
        w_cat = 'PM'
    else:
        w_cat = 'Lead'"""

new_rank_map = """    # Determine rank category for weights (V2 Updated)
    if rank_val in (1, 2):
        w_cat = 'TA'
    elif rank_val in (3, 4):
        w_cat = 'GV'
    elif rank_val in (5, 6):
        if "thương hiệu" in role.lower():
            w_cat = 'TH'
        else:
            w_cat = 'QL'
    else:
        w_cat = 'Lead'"""

code = code.replace(old_rank_map, new_rank_map)

# 5. Upgrade loop calculation logic from old criteria (siso, dondoc, daura) to new V2 criteria (siso, el, bt, pass_rate, etc.)
pattern = r"# Extract raw metrics from Excel.*?overall_score_B = weighted_score_all"
replacement_calc = """# Extract raw metrics from Excel (V2 Updated)
    excel_info = excel_instructor_metrics.get(display_name, {})
    classes_list = list(excel_info.get('classes', []))
    classes_str = ", ".join(classes_list) if classes_list else "Không phụ trách lớp Excel"
    
    cc_vals = excel_info.get('cc_vals', [])
    bt_vals = excel_info.get('bt_vals', [])
    el_vals = excel_info.get('el_vals', [])
    
    # Average student violations (from Excel)
    avg_cc_violation = sum(cc_vals) / len(cc_vals) if cc_vals else 0.0
    avg_bt_violation = sum(bt_vals) / len(bt_vals) if bt_vals else 0.0
    avg_el_violation = sum(el_vals) / len(el_vals) if el_vals else 0.0
    
    # Clean percentages (Invert BT violation percentage to completion percentage)
    student_cc_rate = 100.0 - avg_cc_violation
    student_bt_rate = 100.0 - avg_bt_violation
    student_el_rate = 100.0 - avg_el_violation
    
    # If no classes, set to default high values
    if not classes_list:
        student_cc_rate = 95.0
        student_bt_rate = 92.0
        student_el_rate = 90.0
        
    # Quality score (pass rate)
    pass_rates = []
    for cls in classes_list:
        norm_cls = normalize_class_name(cls)
        p_rate = predictions_data.get(norm_cls)
        if p_rate is not None:
            pass_rates.append(p_rate)
    
    student_pass_rate = sum(pass_rates) / len(pass_rates) if pass_rates else 90.0
    if not classes_list:
        student_pass_rate = 95.0
        
    # Count operational violations from JSON
    op_viols = 0
    for v in violations_data:
        v_name = clean_instructor_name(v.get('Họ và tên', ''))
        if v_name.strip().lower() == name_lower:
            op_viols += 1
            
    # Compliance logs violations from daily log data
    missing_days = log_info.get("missing_days", [])
    time_violations = log_info.get("time_violations", [])
    uncompleted_tasks = log_info.get("uncompleted_tasks", [])
    
    compliance_violations_count = len(missing_days) + len(time_violations)
    material_violations_count = len(uncompleted_tasks)
    
    # Apply Rubrics (Thang 10)
    # 1. Tuân thủ (Báo cáo ngày)
    if compliance_violations_count == 0:
        score_tuanchu = 10.0
    elif compliance_violations_count <= 2:
        score_tuanchu = 8.0
    elif compliance_violations_count <= 4:
        score_tuanchu = 5.0
    elif compliance_violations_count <= 6:
        score_tuanchu = 3.0
    else:
        score_tuanchu = 1.0
        
    # 2. Kỷ luật tác nghiệp (Op violations)
    if op_viols == 0:
        score_kyluat = 10.0
    elif op_viols <= 2:
        score_kyluat = 8.0
    elif op_viols <= 4:
        score_kyluat = 5.0
    elif op_viols <= 6:
        score_kyluat = 3.0
    else:
        score_kyluat = 1.0
        
    # 3. Tiến độ học liệu (uncompleted tasks)
    if material_violations_count == 0:
        score_hoclieu = 10.0
    elif material_violations_count <= 2:
        score_hoclieu = 8.0
    elif material_violations_count <= 4:
        score_hoclieu = 5.0
    elif material_violations_count <= 6:
        score_hoclieu = 3.0
    else:
        score_hoclieu = 1.0
        
    # 4. Quản lý sĩ số (chuyên cần trung bình)
    if student_cc_rate >= 90.0:
        score_siso = 10.0
    elif student_cc_rate >= 80.0:
        score_siso = 8.0
    elif student_cc_rate >= 70.0:
        score_siso = 5.0
    elif student_cc_rate >= 60.0:
        score_siso = 3.0
    else:
        score_siso = 1.0
        
    # 5. Đôn đốc E-learning
    if student_el_rate >= 90.0:
        score_el = 10.0
    elif student_el_rate >= 80.0:
        score_el = 8.0
    elif student_el_rate >= 70.0:
        score_el = 5.0
    elif student_el_rate >= 60.0:
        score_el = 3.0
    else:
        score_el = 1.0
        
    # 6. Đôn đốc BTVN
    if student_bt_rate >= 90.0:
        score_bt = 10.0
    elif student_bt_rate >= 80.0:
        score_bt = 8.0
    elif student_bt_rate >= 70.0:
        score_bt = 5.0
    elif student_bt_rate >= 60.0:
        score_bt = 3.0
    else:
        score_bt = 1.0
        
    # 7. Tỷ lệ pass (Đầu ra)
    if student_pass_rate >= 80.0:
        score_pass_rate = 10.0
    elif student_pass_rate >= 70.0:
        score_pass_rate = 8.0
    elif student_pass_rate >= 60.0:
        score_pass_rate = 5.0
    elif student_pass_rate >= 50.0:
        score_pass_rate = 3.0
    else:
        score_pass_rate = 1.0
        
    # Mặc định 5 điểm cho các tiêu chí khác chưa đo lường định lượng
    score_phoihop = 5.0
    score_giaiquyet = 5.0
    score_kha_gioi = 5.0
    score_cc_cn = 5.0
    score_bang_cap = 5.0
    score_truyendat_dugio = 5.0
    score_truyendat_uprank = 5.0
    score_csat = 5.0
    score_hoclieu_duyet = 5.0
    score_toiuu_ct = 5.0
    score_hieusuat_duoi = 5.0
    score_thuonghieu = 5.0
    score_sangkien = 5.0
    
    # 4. CALCULATE OVERALL PROCESS SCORES (V2 Weights matching)
    w_tuanchu = weights.get('tuanchu', 0.0)
    w_kyluat = weights.get('kyluat', 0.0)
    w_hoclieu = weights.get('hoclieu', 0.0)
    w_siso = weights.get('siso', 0.0)
    w_el = weights.get('el', 0.0)
    w_bt = weights.get('bt', 0.0)
    w_pass_rate = weights.get('pass_rate', 0.0)
    
    sum_w_real = w_tuanchu + w_kyluat + w_hoclieu + w_siso + w_el + w_bt + w_pass_rate
    
    weighted_score_real = (
        score_tuanchu * w_tuanchu +
        score_kyluat * w_kyluat +
        score_hoclieu * w_hoclieu +
        score_siso * w_siso +
        score_el * w_el +
        score_bt * w_bt +
        score_pass_rate * w_pass_rate
    )
    overall_score_A = weighted_score_real / sum_w_real if sum_w_real > 0 else 5.0
    
    # Option B: Complete weights with defaults (5.0) inserted
    weighted_score_all = (
        score_tuanchu * weights.get('tuanchu', 0.0) +
        score_kyluat * weights.get('kyluat', 0.0) +
        score_hoclieu * weights.get('hoclieu', 0.0) +
        score_phoihop * weights.get('phoihop', 0.0) +
        score_siso * weights.get('siso', 0.0) +
        score_el * weights.get('el', 0.0) +
        score_bt * weights.get('bt', 0.0) +
        score_giaiquyet * weights.get('giaiquyet', 0.0) +
        score_pass_rate * weights.get('pass_rate', 0.0) +
        score_kha_gioi * weights.get('kha_gioi', 0.0) +
        score_cc_cn * weights.get('cc_cn', 0.0) +
        score_bang_cap * weights.get('bang_cap', 0.0) +
        score_truyendat_dugio * weights.get('truyendat_dugio', 0.0) +
        score_truyendat_uprank * weights.get('truyendat_uprank', 0.0) +
        score_csat * weights.get('csat', 0.0) +
        score_hoclieu_duyet * weights.get('hoclieu_duyet', 0.0) +
        score_toiuu_ct * weights.get('toiuu_ct', 0.0) +
        score_hieusuat_duoi * weights.get('hieusuat_duoi', 0.0) +
        score_thuonghieu * weights.get('thuonghieu', 0.0) +
        score_sangkien * weights.get('sangkien', 0.0)
    )
    overall_score_B = weighted_score_all"""

code = re.sub(pattern, replacement_calc, code, flags=re.DOTALL)

# 6. Sửa lại rubric_scores mapping ở dòng 600-618 để tương ứng với V2 các tiêu chí
old_rubrics_map = """        'rubric_scores': {
            'tuanchu': score_tuanchu,
            'kyluat': score_kyluat,
            'hoclieu': score_hoclieu,
            'siso': score_siso,
            'dondoc': score_dondoc,
            'phoihop': score_phoihop,
            'giaiquyet': score_giaiquyet,
            'daura': score_daura,
            'phattrien': score_phattrien,
            'truyendat_dugio': score_truyendat_dugio,
            'truyendat_uprank': score_truyendat_uprank,
            'csat': score_csat,
            'hoclieu_duyet': score_hoclieu_duyet,
            'toiuu_ct': score_toiuu_ct,
            'hieusuat_duoi': score_hieusuat_duoi,
            'thuonghieu': score_thuonghieu,
            'sangkien': score_sangkien
        },"""

new_rubrics_map = """        'rubric_scores': {
            'tuanchu': score_tuanchu,
            'kyluat': score_kyluat,
            'hoclieu': score_hoclieu,
            'siso': score_siso,
            'dondoc': score_bt, # Map BTVN/dondoc for compatibility
            'phoihop': score_phoihop,
            'giaiquyet': score_giaiquyet,
            'daura': score_pass_rate, # Map pass_rate/daura for compatibility
            'phattrien': score_cc_cn, # Map cc_cn/phattrien for compatibility
            'truyendat_dugio': score_truyendat_dugio,
            'truyendat_uprank': score_truyendat_uprank,
            'csat': score_csat,
            'hoclieu_duyet': score_hoclieu_duyet,
            'toiuu_ct': score_toiuu_ct,
            'hieusuat_duoi': score_hieusuat_duoi,
            'thuonghieu': score_thuonghieu,
            'sangkien': score_sangkien
        },"""

code = code.replace(old_rubrics_map, new_rubrics_map)

# 7. Sửa lại raw_metrics dict ở dòng 593-599
old_raw_metrics = """        'raw_metrics': {
            'cc_rate': student_cc_rate,
            'bt_rate': student_bt_rate,
            'pass_rate': student_pass_rate,
            'compliance_violations': compliance_violations_count,
            'material_violations': material_violations_count
        },"""

new_raw_metrics = """        'raw_metrics': {
            'cc_rate': student_cc_rate,
            'bt_rate': student_bt_rate,
            'pass_rate': student_pass_rate,
            'compliance_violations': compliance_violations_count,
            'material_violations': material_violations_count,
            'el_rate': student_el_rate,
            'op_violations': op_viols
        },"""

code = code.replace(old_raw_metrics, new_raw_metrics)

# 8. Sửa lại logic sinh strengths, weaknesses ở dòng 565-569 để tránh tham chiếu biến cũ
code = code.replace("if score_dondoc >= 8.0:", "if score_bt >= 8.0:")
code = code.replace("strengths_list.append(f\"Đôn đốc sinh viên hoàn thành E-learning và BTVN tốt ({student_bt_rate:.1f}% học viên hoàn thành).\")",
                    "strengths_list.append(f\"Đôn đốc sinh viên hoàn thành BTVN tốt ({student_bt_rate:.1f}% học viên hoàn thành).\")")
code = code.replace("weaknesses_list.append(f\"Tỷ lệ nợ bài tập của sinh viên lớp phụ trách khá cao ({100.0-student_bt_rate:.1f}% nợ bài).\")",
                    "weaknesses_list.append(f\"Tỷ lệ nợ bài tập của sinh viên lớp phụ trách khá cao ({100.0-student_bt_rate:.1f}% nợ bài).\")")
code = code.replace("score_daura >= 8.0", "score_pass_rate >= 8.0")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(code)

print("Generate KPI Ranking patch completed successfully!")

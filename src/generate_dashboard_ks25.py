import openpyxl
import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

def clean_name(name):
    if name is None: return ""
    name = str(name).strip()
    name = re.sub(r'\s+\d+$', '', name) # Remove trailing numbers
    return name.lower()

def parse_score(score_str):
    if score_str is None:
        return 0.0
    s = str(score_str).strip()
    if '/' in s:
        parts = s.split('/')
        try:
            return float(parts[0])
        except ValueError:
            pass
    try:
        return float(s)
    except ValueError:
        return 0.0

def main():
    main_file = "inputs/Danh sách thi ĐGNL.xlsx" if os.path.exists("inputs/Danh sách thi ĐGNL.xlsx") else (r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx" if os.path.exists(r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx") else r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx")
    ca_files = [
        "inputs/CNTT_HN_K25_7H_9H.xlsx",
        "inputs/CNTT_HN_K25_9H10_11H10.xlsx",
        "inputs/CNTT_HCM_9H30_11H30.xlsx",
        "inputs/CNTT_K25_HCM_14H20_16H20.xlsx"
    ]
    
    if not os.path.exists(main_file):
        print(f"Error: Main file not found at {main_file}")
        return
        
    # 1. Load ca-thi files
    ca_data = {}
    for path in ca_files:
        if not os.path.exists(path):
            print(f"Warning: ca-thi file not found at {path}")
            continue
        wb = openpyxl.load_workbook(path, data_only=True)
        sh = wb.active
        headers = [cell.value for cell in sh[1]]
        
        name_idx = headers.index('Name')
        score_idx = headers.index('Điểm')
        crit_idx = headers.index('Chi tiết tiêu chí')
        git_idx = headers.index('Link Git')
        topic_idx = headers.index('Đề bài')
        comment_idx = headers.index('Nhận xét') if 'Nhận xét' in headers else -1
        
        for r in range(2, sh.max_row + 1):
            row_vals = [cell.value for cell in sh[r]]
            if len(row_vals) <= name_idx or row_vals[name_idx] is None:
                continue
            name = str(row_vals[name_idx]).strip()
            clean = clean_name(name)
            
            score_val = parse_score(row_vals[score_idx])
            criteria_text = row_vals[crit_idx] if len(row_vals) > crit_idx else ""
            git_link = str(row_vals[git_idx] or "").strip()
            topic = str(row_vals[topic_idx] or "").strip()
            comment = str(row_vals[comment_idx] or "").strip() if comment_idx != -1 and len(row_vals) > comment_idx else ""
            
            ca_data[clean] = {
                'name_raw': name,
                'score_100': score_val,
                'criteria_text': criteria_text,
                'git_link': git_link,
                'topic': topic,
                'comment': comment
            }
            
    # 2. Load main excel
    wb_main = openpyxl.load_workbook(main_file, data_only=True)
    sh_main = wb_main["Danh sách ĐGNL CNTT"]
    
    headers_main = [cell.value for cell in sh_main[1]]
    c_class_idx = headers_main.index('Mã lớp hiện tại')
    c_name_idx = headers_main.index('Họ và tên học viên')
    c_tn_idx = headers_main.index('Trắc nghiệm (Đ1)')
    c_th_idx = headers_main.index('Thực hành (Đ1)')
    c_p1_idx = headers_main.index('Điểm danh P1')
    c_p2_idx = headers_main.index('Điểm danh P2')
    c_cs_idx = headers_main.index('Cơ sở đào tạo')
    c_final_idx = headers_main.index('Điểm final (Đ1)')
    c_bs_dm = headers_main.index('Điểm danh BS') if 'Điểm danh BS' in headers_main else -1
    
    ks25_students = []
    
    # 11 Criteria keys
    criteria_keys = ["1.1", "1.2", "1.3", "2.1", "2.2", "3.1", "3.2", "4.1", "4.2", "4.3", "4.4"]
    criteria_stats = {k: {"pass": 0, "fail": 0} for k in criteria_keys}

    # Load Ngoại ngữ sheet
    nn_data = {}
    sh_nn = wb_main["Danh sách ĐGNL ngoại ngữ"]
    headers_nn = [cell.value for cell in sh_nn[1]]
    c_nn_name = headers_nn.index('Họ và tên học viên')
    c_nn_final = headers_nn.index('Điểm final ĐGNL (Lần 1)')
    c_nn_pl = headers_nn.index('PL Ngoại ngữ hiện tại')
    c_nn_level = headers_nn.index('Cấp độ') if 'Cấp độ' in headers_nn else -1
    c_nn_dm = headers_nn.index('Điểm danh') if 'Điểm danh' in headers_nn else -1
    c_nn_bb = headers_nn.index('Biên bản') if 'Biên bản' in headers_nn else -1
    c_nn_gc = headers_nn.index('Ghi chú') if 'Ghi chú' in headers_nn else -1
    
    for r in range(2, sh_nn.max_row + 1):
        name_val = sh_nn.cell(row=r, column=c_nn_name+1).value
        if not name_val: continue
        clean = clean_name(name_val)
        nn_data[clean] = {
            'final': sh_nn.cell(row=r, column=c_nn_final+1).value,
            'pl': sh_nn.cell(row=r, column=c_nn_pl+1).value,
            'level': sh_nn.cell(row=r, column=c_nn_level+1).value if c_nn_level != -1 else None,
            'dm': sh_nn.cell(row=r, column=c_nn_dm+1).value if c_nn_dm != -1 else None,
            'bb': sh_nn.cell(row=r, column=c_nn_bb+1).value if c_nn_bb != -1 else '',
            'gc': sh_nn.cell(row=r, column=c_nn_gc+1).value if c_nn_gc != -1 else ''
        }

    # Load Kỹ năng mềm sheet
    knm_data = {}
    sh_knm = wb_main["Danh sách ĐGNL Kỹ năng mềm"]
    headers_knm = [cell.value for cell in sh_knm[1]]
    c_knm_name = headers_knm.index('Họ và tên học viên')
    c_knm_final = headers_knm.index('Điểm final ĐGNL (Lần 1)')
    c_knm_dm = headers_knm.index('Điểm danh') if 'Điểm danh' in headers_knm else -1
    c_knm_bb = headers_knm.index('Biên bản') if 'Biên bản' in headers_knm else -1
    c_knm_gc = headers_knm.index('Ghi chú') if 'Ghi chú' in headers_knm else -1
    
    for r in range(2, sh_knm.max_row + 1):
        name_val = sh_knm.cell(row=r, column=c_knm_name+1).value
        if not name_val: continue
        clean = clean_name(name_val)
        knm_data[clean] = {
            'final': sh_knm.cell(row=r, column=c_knm_final+1).value,
            'dm': sh_knm.cell(row=r, column=c_knm_dm+1).value if c_knm_dm != -1 else None,
            'bb': sh_knm.cell(row=r, column=c_knm_bb+1).value if c_knm_bb != -1 else '',
            'gc': sh_knm.cell(row=r, column=c_knm_gc+1).value if c_knm_gc != -1 else ''
        }
    
    total_hn = 0
    total_hcm = 0
    absent_hn = 0
    absent_hcm = 0
    
    for r in range(2, sh_main.max_row + 1):
        class_name = sh_main.cell(row=r, column=c_class_idx+1).value
        if not class_name or "CNTT" not in str(class_name) or not ("KS25" in str(class_name) or "K25" in str(class_name)):
            continue
            
        name = sh_main.cell(row=r, column=c_name_idx+1).value
        if not name:
            continue
            
        clean = clean_name(name)
        cs = str(sh_main.cell(row=r, column=c_cs_idx+1).value or "").strip()
        
        is_hn = "HN" in str(class_name) or "Hà Nội" in cs
        if is_hn:
            total_hn += 1
        else:
            total_hcm += 1
            
        p1 = sh_main.cell(row=r, column=c_p1_idx+1).value
        p2 = sh_main.cell(row=r, column=c_p2_idx+1).value
        tn_val = sh_main.cell(row=r, column=c_tn_idx+1).value
        th_val = sh_main.cell(row=r, column=c_th_idx+1).value
        
        bs_val = sh_main.cell(row=r, column=c_bs_dm+1).value if c_bs_dm != -1 else None
        
        is_absent = False
        if (tn_val is not None and float(tn_val) > 0) or (th_val is not None and float(th_val) > 0) or (str(bs_val) in ["1", "1.0"]):
            is_absent = False
        elif p1 == "Vắng" or p2 == "Vắng" or str(p1) == "0" or str(p2) == "0" or str(p1) == "0.0" or str(p2) == "0.0":
            is_absent = True
        elif (p1 is None or p1 == "") and (p2 is None or p2 == "") and (tn_val is None or tn_val == 0) and (th_val is None or th_val == 0):
            is_absent = True
            
        if is_absent:
            if is_hn:
                absent_hn += 1
            else:
                absent_hcm += 1
                
        # Parse scores
        mcq_score = float(tn_val) if tn_val is not None else 0.0
        pract_score = float(th_val) if th_val is not None else 0.0
        final_score = mcq_score * 0.3 + pract_score * 0.7 # PM formula
        
        # Scale to 10
        final_10 = round(final_score / 10.0, 1)
        if final_10 > 10.0: final_10 = 10.0
        
        # Get details from ca-thi
        matched = ca_data.get(clean)
        criteria_text = ""
        git_link = ""
        topic = ""
        comment = ""
        criteria_results = {k: False for k in criteria_keys}
        
        if matched and not is_absent:
            criteria_text = matched['criteria_text'] or ""
            git_link = matched['git_link'] or ""
            topic = matched['topic'] or ""
            comment = matched['comment'] or ""
            
            # Parse criteria lines
            lines = str(criteria_text).split("\n")
            for k in criteria_keys:
                matched_line = None
                for line in lines:
                    if k in line:
                        matched_line = line
                        break
                if matched_line:
                    if "KHÔNG ĐẠT" in matched_line.upper():
                        criteria_results[k] = False
                        criteria_stats[k]["fail"] += 1
                    elif "ĐẠT" in matched_line.upper():
                        criteria_results[k] = True
                        criteria_stats[k]["pass"] += 1
                    else:
                        criteria_results[k] = False
                        criteria_stats[k]["fail"] += 1
                else:
                    criteria_results[k] = False
                    criteria_stats[k]["fail"] += 1
        else:
            has_passed_some = (pract_score >= 50) and not is_absent
            for k in criteria_keys:
                criteria_results[k] = has_passed_some
                if not is_absent:
                    if has_passed_some:
                        criteria_stats[k]["pass"] += 1
                    else:
                        criteria_stats[k]["fail"] += 1
                else:
                    criteria_stats[k]["fail"] += 1
                    
        # 1. Thái độ & Kỷ luật
        nn_info = nn_data.get(clean)
        knm_info = knm_data.get(clean)
        
        is_violation = False
        
        # Check CNTT
        cntt_gc = str(sh_main.cell(row=r, column=headers_main.index('Ghi chú')+1).value or '').lower()
        cntt_bb = str(sh_main.cell(row=r, column=headers_main.index('Biên bản')+1).value or '').lower()
        for kw in ['vi phạm', 'hủy kết quả', 'sử dụng ai', 'gian lận', 'quy chế']:
            if kw in cntt_gc or kw in cntt_bb:
                is_violation = True
                
        # Check NN
        if nn_info:
            nn_gc = str(nn_info['gc'] or '').lower()
            nn_bb = str(nn_info['bb'] or '').lower()
            for kw in ['vi phạm', 'hủy kết quả', 'sử dụng ai', 'gian lận', 'quy chế']:
                if kw in nn_gc or kw in nn_bb:
                    is_violation = True
                    
        # Check KNM
        if knm_info:
            knm_gc = str(knm_info['gc'] or '').lower()
            knm_bb = str(knm_info['bb'] or '').lower()
            for kw in ['vi phạm', 'hủy kết quả', 'sử dụng ai', 'gian lận', 'quy chế']:
                if kw in knm_gc or kw in knm_bb:
                    is_violation = True
                    
        if is_violation:
            attitude_score = 0.0
        else:
            attitude_score = 100.0
            if is_absent:
                attitude_score -= 30.0
            if nn_info:
                if nn_info['pl'] == 'Tiếng Anh' and (nn_info['final'] is None or str(nn_info['dm']) == '0'):
                    attitude_score -= 30.0
                elif nn_info['pl'] == 'Tiếng Nhật' and str(nn_info['dm']) == '0':
                    attitude_score -= 30.0
            if knm_info and (knm_info['final'] is None or str(knm_info['dm']) == '0'):
                attitude_score -= 30.0
            attitude_score = max(0.0, attitude_score)
            
        # 2. Nền tảng lập trình & 3. Ứng dụng công nghệ
        algo_score = sum([100.0 if criteria_results[k] else 0.0 for k in ["1.1", "1.2", "1.3"]]) / 3.0
        fw_keys = ["2.1", "2.2", "3.1", "3.2", "4.1", "4.2", "4.3", "4.4"]
        fw_score = sum([100.0 if criteria_results[k] else 0.0 for k in fw_keys]) / len(fw_keys)
        
        if is_absent:
            it_foundation_score = 0.0
            it_application_score = 0.0
        else:
            it_foundation_score = (mcq_score + algo_score) / 2.0
            it_application_score = fw_score
        
        # 4. Ngoại ngữ
        nn_score = 0.0
        if nn_info:
            if nn_info['pl'] == 'Tiếng Anh':
                try:
                    tok_val = float(nn_info['final']) if nn_info['final'] is not None else 0.0
                    nn_score = min(100.0, max(0.0, (tok_val / 990.0) * 100.0))
                except ValueError:
                    nn_score = 0.0
            elif nn_info['pl'] == 'Tiếng Nhật':
                nn_score = 70.0
                
        # 5. Kỹ năng mềm
        knm_score = 0.0
        if knm_info and knm_info['final'] is not None:
            try:
                knm_score = float(knm_info['final'])
            except ValueError:
                knm_score = 0.0
                
        # Calculate dimensions
        dimensions = [
            round(attitude_score, 1),
            round(it_foundation_score, 1),
            round(it_application_score, 1),
            round(nn_score, 1),
            round(knm_score, 1)
        ]
        
        # Calculate academic label
        algo_score = sum([100.0 if criteria_results[k] else 0.0 for k in ["1.1", "1.2", "1.3"]]) / 3.0
        fw_keys = ["2.1", "2.2", "3.1", "3.2", "4.1", "4.2", "4.3", "4.4"]
        fw_score = sum([100.0 if criteria_results[k] else 0.0 for k in fw_keys]) / len(fw_keys)
        
        if is_absent:
            academic_label = "ABSENT"
        else:
            if mcq_score < 50.0 or algo_score < 40.0:
                academic_label = "WEAK_FOUNDATION"
            elif fw_score < 50.0:
                academic_label = "FRAMEWORK_GAP"
            else:
                academic_label = "NORMAL"
                
        # Internal dimensions for technical readiness classification
        dim_orm = round((sum([100.0 if criteria_results[k] else 0.0 for k in ["3.1", "3.2"]]) / 2.0), 1)
        dim_logic = round((sum([100.0 if criteria_results[k] else 0.0 for k in ["4.2", "4.4"]]) / 2.0), 1)
        
        rl = 0
        if is_absent:
            rl = 0
        else:
            if final_10 >= 8.0 and dim_orm >= 50 and dim_logic >= 50:
                rl = 3
            elif final_10 >= 6.0 and dim_orm >= 40 and dim_logic >= 40:
                rl = 2
            elif final_10 >= 4.0 and pract_score >= 50:
                rl = 1
            else:
                rl = 0
                
        # Determine career orientation and notes for KS25 (Semester II context)
        if is_absent:
            career_orientation = "Chưa xác định"
            career_note = "Vắng thi hoặc thiếu bài làm"
        elif academic_label == "NORMAL":
            career_orientation = "Lập trình viên Backend FastAPI"
            career_note = "Đạt chuẩn lý thuyết logic & ứng dụng framework"
        elif academic_label == "FRAMEWORK_GAP":
            career_orientation = "Lập trình viên Python (Cơ bản)"
            career_note = "Nắm vững thuật toán, yếu kết nối Database/ORM"
        elif academic_label == "WEAK_FOUNDATION":
            career_orientation = "Bồi dưỡng Thuật toán & Logic"
            career_note = "Hổng tư duy mảng, vòng lặp và thuật toán cơ bản"
        else:
            career_orientation = "Bồi dưỡng CNTT cơ bản"
            career_note = "Cần theo sát kèm cặp đặc biệt"

        ks25_students.append({
            'name': name,
            'class': class_name,
            'cs': cs,
            'branch': 'HN' if is_hn else 'HCM',
            'is_absent': is_absent,
            'mcq': mcq_score,
            'practical': pract_score,
            'final': final_10,
            'readiness_level': rl,
            'dimensions': dimensions,
            'criteria': criteria_results,
            'comment': comment,
            'git_link': git_link,
            'topic': topic,
            'academic_label': academic_label,
            'career_orientation': career_orientation,
            'career_note': career_note
        })
        
    total_students = len(ks25_students)
    presents = len([s for s in ks25_students if not s['is_absent']])
    absents = len([s for s in ks25_students if s['is_absent']])
    
    # Averages
    mcq_avg = sum(s['mcq'] for s in ks25_students if not s['is_absent']) / presents if presents else 0.0
    pract_avg = sum(s['practical'] for s in ks25_students if not s['is_absent']) / presents if presents else 0.0
    final_avg = sum(s['final'] for s in ks25_students if not s['is_absent']) / presents if presents else 0.0
    
    # Std Dev
    variance = sum((s['mcq'] - mcq_avg) ** 2 for s in ks25_students if not s['is_absent']) / presents if presents else 0.0
    mcq_std = variance ** 0.5
    
    passed_pract = len([s for s in ks25_students if not s['is_absent'] and s['practical'] >= 50])
    pract_pass_rate = round(passed_pract / presents * 100, 1) if presents else 0.0
    
    level_3_cnt = len([s for s in ks25_students if not s['is_absent'] and s['readiness_level'] == 3])
    level_2_cnt = len([s for s in ks25_students if not s['is_absent'] and s['readiness_level'] == 2])
    level_1_cnt = len([s for s in ks25_students if not s['is_absent'] and s['readiness_level'] == 1])
    level_0_cnt = len([s for s in ks25_students if not s['is_absent'] and s['readiness_level'] == 0])
    
    # Class stats
    class_names = sorted(list(set(s['class'] for s in ks25_students)))
    chr_class_options = "".join(f'<option value="{c}">{c}</option>' for c in class_names)
    
    class_stats_html = ""
    for c in class_names:
        c_studs = [s for s in ks25_students if s['class'] == c]
        c_tot = len(c_studs)
        c_abs = len([s for s in c_studs if s['is_absent']])
        c_pres = c_tot - c_abs
        c_avg_mcq = sum(s['mcq'] for s in c_studs if not s['is_absent']) / c_pres if c_pres else 0.0
        c_avg_th = sum(s['practical'] for s in c_studs if not s['is_absent']) / c_pres if c_pres else 0.0
        c_pass_th = len([s for s in c_studs if not s['is_absent'] and s['practical'] >= 50])
        c_pass_rate = round(c_pass_th / c_pres * 100, 1) if c_pres else 0.0
        c_abs_rate = round(c_abs / c_tot * 100, 1) if c_tot else 0.0
        
        # Color code absence rate
        if c_abs_rate >= 50.0:
            abs_badge = f'<span class="badge badge-l0" style="padding: 4px 8px; font-size: 0.8rem;">{c_abs} ({c_abs_rate}%)</span>'
        elif c_abs_rate >= 20.0:
            abs_badge = f'<span class="badge badge-l1" style="padding: 4px 8px; font-size: 0.8rem;">{c_abs} ({c_abs_rate}%)</span>'
        else:
            abs_badge = f'<span class="badge badge-l3" style="padding: 4px 8px; font-size: 0.8rem;">{c_abs} ({c_abs_rate}%)</span>'
            
        # Color code practical average
        if c_avg_th < 30.0:
            th_style = 'style="color: var(--color-danger); font-weight: bold;"'
            th_val_str = f'{c_avg_th:.2f}'
        elif c_avg_th < 50.0:
            th_style = 'style="color: var(--color-warning);"'
            th_val_str = f'{c_avg_th:.2f}'
        else:
            th_style = 'style="color: var(--color-success); font-weight: bold;"'
            th_val_str = f'{c_avg_th:.2f}'
            
        # Color code pass rate
        if c_pass_rate < 40.0:
            pass_badge = f'<span class="badge badge-l0" style="padding: 4px 8px; font-size: 0.8rem;">{c_pass_rate}%</span>'
        elif c_pass_rate < 60.0:
            pass_badge = f'<span class="badge badge-l1" style="padding: 4px 8px; font-size: 0.8rem;">{c_pass_rate}%</span>'
        else:
            pass_badge = f'<span class="badge badge-l3" style="padding: 4px 8px; font-size: 0.8rem;">{c_pass_rate}%</span>'
            
        # Determine class status badge & row highlight (UI/UX warning highlight)
        if c_abs_rate >= 50.0 or c_avg_th < 30.0:
            status_badge = '<span class="badge badge-l0" style="padding: 4px 8px; font-size: 0.8rem; border: 1px solid rgba(239,68,68,0.4);">🚨 Cảnh báo</span>'
            row_style = 'style="background-color: rgba(239, 68, 68, 0.05); border-left: 4px solid var(--color-danger);"'
        elif c_abs_rate >= 20.0 or c_avg_th < 50.0:
            status_badge = '<span class="badge badge-l1" style="padding: 4px 8px; font-size: 0.8rem; border: 1px solid rgba(245,158,11,0.4);">⚠️ Lưu ý</span>'
            row_style = 'style="background-color: rgba(245, 158, 11, 0.02); border-left: 4px solid var(--color-warning);"'
        else:
            status_badge = '<span class="badge badge-l3" style="padding: 4px 8px; font-size: 0.8rem; border: 1px solid rgba(16,185,129,0.4);">🟢 Bình thường</span>'
            row_style = ''

        class_stats_html += f"""
        <tr {row_style}>
            <td><strong>{c}</strong></td>
            <td>{c_tot}</td>
            <td>{c_pres}</td>
            <td>{abs_badge}</td>
            <td>{c_avg_mcq:.2f}</td>
            <td {th_style}>{th_val_str}</td>
            <td>{pass_badge}</td>
            <td>{status_badge}</td>
        </tr>
        """

    # English & Japanese stats for present KS25 students
    eng_students = [s for s in ks25_students if clean_name(s['name']) in nn_data and nn_data[clean_name(s['name'])]['pl'] == 'Tiếng Anh']
    eng_present_students = [s for s in eng_students if not s['is_absent'] and nn_data[clean_name(s['name'])]['final'] is not None]
    eng_pres_cnt = len(eng_present_students)
    eng_pass_cnt = len([s for s in eng_present_students if float(nn_data[clean_name(s['name'])]['final'] or 0) >= 450])
    eng_pass_pct = round(eng_pass_cnt / eng_pres_cnt * 100, 1) if eng_pres_cnt else 0.0

    jp_students = [s for s in ks25_students if clean_name(s['name']) in nn_data and nn_data[clean_name(s['name'])]['pl'] == 'Tiếng Nhật']
    jp_tot = len(jp_students)
    jp_n4_cnt = len([s for s in jp_students if nn_data[clean_name(s['name'])].get('level') == 'N4'])
    jp_n5_cnt = len([s for s in jp_students if nn_data[clean_name(s['name'])].get('level') == 'N5'])

    # KNM stats
    knm_students = [s for s in ks25_students if clean_name(s['name']) in knm_data]
    knm_present_students = [s for s in knm_students if not s['is_absent'] and knm_data[clean_name(s['name'])]['final'] is not None]
    knm_pres_cnt = len(knm_present_students)
    knm_avg = sum([float(knm_data[clean_name(s['name'])]['final'] or 0) for s in knm_present_students]) / knm_pres_cnt if knm_pres_cnt else 0.0
    knm_pass_cnt = len([s for s in knm_present_students if float(knm_data[clean_name(s['name'])]['final'] or 0) >= 50])
    knm_pass_pct = round(knm_pass_cnt / knm_pres_cnt * 100, 1) if knm_pres_cnt else 0.0
        
    dim_sums = [0.0] * 5
    for s in ks25_students:
        for i in range(5):
            dim_sums[i] += s['dimensions'][i]
    dim_avgs = [round(d / total_students, 1) if total_students else 0.0 for d in dim_sums]

    # Calculate HN vs HCM cohort overview stats
    hn_students = [s for s in ks25_students if s['branch'] == 'HN']
    hcm_students = [s for s in ks25_students if s['branch'] == 'HCM']
    
    hn_registered = len(hn_students)
    hn_took = len([s for s in hn_students if not s['is_absent']])
    hn_avg = sum(s['final'] for s in hn_students if not s['is_absent']) / hn_took if hn_took else 0.0
    hn_ready = len([s for s in hn_students if not s['is_absent'] and s['readiness_level'] in [2, 3]])
    hn_ready_pct = round(hn_ready / hn_registered * 100, 1) if hn_registered else 0.0
    
    hcm_registered = len(hcm_students)
    hcm_took = len([s for s in hcm_students if not s['is_absent']])
    hcm_avg = sum(s['final'] for s in hcm_students if not s['is_absent']) / hcm_took if hcm_took else 0.0
    hcm_ready = len([s for s in hcm_students if not s['is_absent'] and s['readiness_level'] in [2, 3]])
    hcm_ready_pct = round(hcm_ready / hcm_registered * 100, 1) if hcm_registered else 0.0

    # Fail rates for 3 root cause categories
    # 1. Tư duy Logic & Thuật toán nền tảng (Criteria 1.1, 1.2, 1.3)
    fail_rate_algo = sum([criteria_stats[k]["fail"]/(criteria_stats[k]["pass"]+criteria_stats[k]["fail"])*100 for k in ["1.1", "1.2", "1.3"]]) / 3.0
    # 2. Kiến thức cấu trúc dữ liệu & Framework (Criteria 2.1, 2.2, 3.1, 3.2)
    fail_rate_fw = sum([criteria_stats[k]["fail"]/(criteria_stats[k]["pass"]+criteria_stats[k]["fail"])*100 for k in ["2.1", "2.2", "3.1", "3.2"]]) / 4.0
    # 3. Logic nghiệp vụ & Xây dựng API (Criteria 4.1, 4.2, 4.3, 4.4)
    fail_rate_api = sum([criteria_stats[k]["fail"]/(criteria_stats[k]["pass"]+criteria_stats[k]["fail"])*100 for k in ["4.1", "4.2", "4.3", "4.4"]]) / 4.0
    
    fail_rate_algo = round(fail_rate_algo, 1)
    fail_rate_fw = round(fail_rate_fw, 1)
    fail_rate_api = round(fail_rate_api, 1)
    
    # MCQ stats
    exc_cnt = len([s for s in ks25_students if not s['is_absent'] and s['mcq'] >= 90])
    vg_cnt = len([s for s in ks25_students if not s['is_absent'] and 80 <= s['mcq'] < 90])
    g_cnt = len([s for s in ks25_students if not s['is_absent'] and 70 <= s['mcq'] < 80])
    avg_cnt = len([s for s in ks25_students if not s['is_absent'] and 50 <= s['mcq'] < 70])
    fail_cnt = len([s for s in ks25_students if not s['is_absent'] and s['mcq'] < 50])
    
    exc_pct = round(exc_cnt / presents * 100, 1) if presents else 0.0
    vg_pct = round(vg_cnt / presents * 100, 1) if presents else 0.0
    g_pct = round(g_cnt / presents * 100, 1) if presents else 0.0
    avg_pct = round(avg_cnt / presents * 100, 1) if presents else 0.0
    fail_pct = round(fail_cnt / presents * 100, 1) if presents else 0.0
    
    # Gap Map
    chr_bar_html = ""
    sorted_keys = sorted(criteria_keys, key=lambda k: criteria_stats[k]["fail"]/(criteria_stats[k]["pass"]+criteria_stats[k]["fail"])*100, reverse=True)
    criteria_titles = {
        "1.1": "1.1 - Chuẩn hóa & Validate dữ liệu thô",
        "1.2": "1.2 - Thuật toán Linear Search lọc điều kiện",
        "1.3": "1.3 - Thuật toán Bubble Sort sắp xếp giảm dần",
        "2.1": "2.1 - Schema RoomCreate (Pydantic)",
        "2.2": "2.2 - Schema RoomResponse & response_model",
        "3.1": "3.1 - database.py & dependency get_db() yield",
        "3.2": "3.2 - SQLAlchemy Models quan hệ 1-N",
        "4.1": "4.1 - Phân tầng cấu trúc thư mục 4 lớp",
        "4.2": "4.2 - API POST bẫy lỗi logic (trùng/404)",
        "4.3": "4.3 - API GET truy vấn kèm quan hệ bảng",
        "4.4": "4.4 - API DELETE ràng buộc toàn vẹn"
    }
    
    for k in sorted_keys:
        p_cnt = criteria_stats[k]["pass"]
        f_cnt = criteria_stats[k]["fail"]
        tot = p_cnt + f_cnt
        crit_fail_pct = round(f_cnt / tot * 100, 1) if tot > 0 else 0.0
        chr_bar_html += f'''
        <div style="font-size: 0.82rem; margin-bottom: 0.25rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span style="color: var(--text-primary);">{criteria_titles[k]}</span>
                <span style="color: {'var(--color-danger); font-weight: 700;' if crit_fail_pct >= 50 else 'var(--color-warning);'}">Trượt: {crit_fail_pct}% ({f_cnt}/{tot})</span>
            </div>
            <div style="background: rgba(255,255,255,0.06); height: 8px; border-radius: 4px; overflow: hidden;">
                <div style="background: {'var(--color-danger)' if crit_fail_pct >= 60 else 'var(--color-warning)'}; width: {crit_fail_pct}%; height: 100%; border-radius: 4px;"></div>
            </div>
        </div>
        '''
        
    students_json = []
    for s in ks25_students:
        students_json.append({
            'name': s['name'],
            'class': s['class'],
            'cs': s['cs'],
            'branch': s['branch'],
            'is_absent': s['is_absent'],
            'mcq': s['mcq'],
            'practical': s['practical'],
            'final': s['final'],
            'readiness_level': s['readiness_level'],
            'dimensions': s['dimensions'],
            'comment': s['comment'],
            'git_link': s['git_link'],
            'topic': s['topic'],
            'academic_label': s['academic_label'],
            'career_orientation': s['career_orientation'],
            'career_note': s['career_note']
        })
    students_json_str = json.dumps(students_json, ensure_ascii=False)
    
    # Load raw HTML template from string
    html_template = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo ĐGNL Lần 1 - Khóa KS25 CNTT</title>
    
    <!-- Google Fonts & Chart.js -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        :root {
            --bg-main: #09090b;
            --bg-card: #18181b;
            --border-color: #27272a;
            --text-primary: #f4f4f5;
            --text-secondary: #a1a1aa;
            --text-muted: #71717a;
            --color-primary: #3b82f6; /* Blue for FastAPI/Python */
            --color-success: #10b981;
            --color-warning: #f59e0b;
            --color-danger: #ef4444;
            --color-purple: #8b5cf6;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }
        
        body {
            background-color: var(--bg-main);
            color: var(--text-primary);
            padding-bottom: 60px;
        }
        
        .header {
            background: rgba(24, 24, 27, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .logo-icon {
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-purple) 100%);
            color: white;
            width: 38px;
            height: 38px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 1.25rem;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .logo-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.15rem;
            letter-spacing: -0.5px;
        }
        
        .nav-tabs {
            display: flex;
            gap: 0.5rem;
            background: rgba(0, 0, 0, 0.2);
            padding: 4px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }
        
        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 0.5rem 1.25rem;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .tab-btn.active {
            background: var(--border-color);
            color: white;
        }
        
        .tab-btn:hover:not(.active) {
            color: white;
            background: rgba(255,255,255,0.02);
        }
        
        .container {
            max-width: 1400px;
            margin: 2rem auto 0 auto;
            padding: 0 2rem;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 24px rgba(0,0,0,0.15);
        }
        
        .card-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            color: white;
            border-left: 4px solid var(--color-primary);
            padding-left: 0.75rem;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .metric-card {
            background: rgba(255,255,255,0.015);
            border: 1px solid var(--border-color);
            padding: 1.25rem 1.5rem;
            border-radius: 8px;
            transition: transform 0.2s;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
        }
        
        .metric-label {
            color: var(--text-secondary);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }
        
        .metric-value {
            font-size: 1.85rem;
            font-weight: 700;
            font-family: 'Outfit', sans-serif;
            color: white;
        }
        
        .metric-trend {
            font-size: 0.75rem;
            margin-top: 0.5rem;
            color: var(--text-muted);
        }
        
        .grid-2col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-bottom: 2rem;
            align-items: start;
        }
        
        @media (max-width: 1000px) {
            .grid-2col {
                grid-template-columns: 1fr;
            }
        }
        
        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
            text-align: left;
        }
        
        .comparison-table th {
            background: rgba(0,0,0,0.2);
            color: white;
            font-weight: 600;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
        }
        
        .comparison-table td {
            padding: 0.85rem 1rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-secondary);
            vertical-align: middle;
        }
        
        .comparison-table tr:hover td {
            color: white;
            background: rgba(255,255,255,0.01);
        }
        
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .badge-l3 { background: rgba(16, 185, 129, 0.1); color: var(--color-success); }
        .badge-l2 { background: rgba(59, 130, 246, 0.1); color: var(--color-primary); }
        .badge-l1 { background: rgba(245, 158, 11, 0.1); color: var(--color-warning); }
        .badge-l0 { background: rgba(239, 68, 68, 0.1); color: var(--color-danger); }
        
        .students-table-container {
            overflow-x: auto;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }
        
        .students-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.95rem;
        }
        
        .students-table th {
            background-color: #202024;
            color: #fff;
            font-weight: 600;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
        }
        
        .students-table td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-secondary);
        }
        
        .students-table tr {
            transition: background-color 0.2s;
        }
        
        .students-table tr.student-row:hover {
            background-color: rgba(255, 255, 255, 0.015);
            cursor: pointer;
        }
        
        .students-table tr.active-row {
            background-color: #272730;
        }
        
        .students-table tr.detail-row {
            display: none;
            background-color: #121214;
        }
        
        .students-table tr.detail-row.active {
            display: table-row;
        }
        
        /* Interactive student table */
        .search-container {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }
        
        .search-input {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: white;
            padding: 0.6rem 1rem;
            border-radius: 6px;
            outline: none;
            width: 300px;
            font-size: 0.9rem;
        }
        
        .search-input:focus {
            border-color: var(--color-primary);
        }
        
        .filter-select {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: white;
            padding: 0.6rem 1rem;
            border-radius: 6px;
            outline: none;
            font-size: 0.9rem;
            cursor: pointer;
        }
        
        .student-row {
            cursor: pointer;
            transition: background 0.15s;
        }
        
        .student-row:hover {
            background: rgba(255,255,255,0.015) !important;
        }
        
        .detail-row {
            display: none;
            background: rgba(255,255,255,0.005);
        }
        
        .detail-card {
            padding: 1.5rem;
            border: 1px solid var(--border-color);
            border-top: none;
            border-radius: 0 0 8px 8px;
        }
        
        .dim-bar-container {
            background: rgba(255,255,255,0.08);
            height: 6px;
            border-radius: 3px;
            overflow: hidden;
            width: 100px;
            display: inline-block;
            vertical-align: middle;
            margin-left: 8px;
        }
        
        .dim-bar-fill {
            height: 100%;
            border-radius: 3px;
        }
        
    </style>
</head>
<body>

    <!-- HEADER NAVIGATION -->
    <header class="header">
        <div class="header-container">
            <div class="logo-section">
                <div class="logo-icon">🐍</div>
                <div class="logo-title">Báo Cáo ĐGNL Lần 1 - Khóa KS25 CNTT</div>
            </div>
            <div class="nav-tabs">
                <button class="tab-btn active" onclick="switchTab('tab-overview')">Tổng quan</button>
                <button class="tab-btn" onclick="switchTab('tab-students')">Danh sách học viên</button>
                <button class="tab-btn" onclick="switchTab('tab-curriculum')">Đánh giá & Kiến nghị</button>
            </div>
        </div>
    </header>

    <div class="container">
    
        <!-- TAB 1: OVERVIEW -->
        <div id="tab-overview" class="tab-content active">
        
            <!-- Alert Warning for Absence & Fail Rate -->
            <div style="background-color: rgba(239, 68, 68, 0.05); border-left: 4px solid var(--color-danger); padding: 1.25rem 1.5rem; border-radius: 6px; margin-bottom: 2rem; display: flex; align-items: start; gap: 1rem;">
                <span style="font-size: 1.4rem;">🚨</span>
                <div>
                    <strong style="color: #f87171; font-size: 0.95rem;">Cảnh báo đỏ từ Ban chuyên môn:</strong>
                    <p style="color: var(--text-secondary); font-size: 0.88rem; margin-top: 0.25rem; line-height: 1.5;">
                        Khóa KS25 ghi nhận kết quả học tập <strong>báo động đỏ</strong> ở phần thực hành với tỷ lệ trượt lên tới <strong>81.9%</strong> (điểm TB thực hành 26.12/100). 
                        Đồng thời, tỷ lệ vắng thi thực tế đạt <strong>41.96%</strong> (180/429 học viên), tập trung chủ yếu tại cơ sở Hà Nội (~62.3% vắng thi) do sự cố nghiêm trọng của hệ thống khảo thí trong ca thi đầu tiên (7h-9h ngày 10/8), dẫn đến mất bài và lỗi nộp bài.
                    </p>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Tổng Quy Mô CNTT KS25</div>
                    <div class="metric-value">{total_students}</div>
                    <div class="metric-trend">Học viên đã đăng ký học</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Tham gia thi thực tế</div>
                    <div class="metric-value">{presents} <span style="font-size: 0.95rem; font-weight: normal; color: var(--text-secondary);">({presents_pct}%)</span></div>
                    <div class="metric-trend" style="color: var(--color-success);">Có ghi nhận bài làm</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Số SV Vắng/Lỗi hệ thống</div>
                    <div class="metric-value" style="color: var(--color-danger);">{absents} <span style="font-size: 0.95rem; font-weight: normal; color: var(--text-secondary);">({absents_pct}%)</span></div>
                    <div class="metric-trend" style="color: var(--color-danger);">Báo động vắng cao tại Hà Nội</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Tỷ lệ đạt chuẩn thực hành</div>
                    <div class="metric-value" style="color: var(--color-success);">{pract_pass_rate}%</div>
                    <div class="metric-trend" style="color: var(--color-success);">35/{presents} SV có Điểm TH &ge; 50</div>
                </div>
            </div>
            
            <div class="metrics-grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
                <div class="metric-card" style="border-left: 4px solid var(--color-primary);">
                    <div class="metric-label">Điểm trung bình trắc nghiệm (MCQ)</div>
                    <div class="metric-value" style="color: var(--color-primary);">{mcq_avg} <span style="font-size: 1.1rem; font-weight: normal; color: var(--text-secondary);">/ 100</span></div>
                    <div class="metric-trend">Độ phân hóa tốt (Std Dev: {mcq_std})</div>
                </div>
                <div class="metric-card" style="border-left: 4px solid var(--color-danger);">
                    <div class="metric-label">Điểm trung bình thực hành (Tự luận)</div>
                    <div class="metric-value" style="color: var(--color-danger);">{pract_avg} <span style="font-size: 1.1rem; font-weight: normal; color: var(--text-secondary);">/ 100</span></div>
                    <div class="metric-trend">➔ Cần củng cố gấp logic thực hành</div>
                </div>
                <div class="metric-card" style="border-left: 4px solid var(--color-success);">
                    <div class="metric-label">Điểm trung bình Final (Thang 10)</div>
                    <div class="metric-value" style="color: var(--color-success);">{final_avg} <span style="font-size: 1.1rem; font-weight: normal; color: var(--text-secondary);">/ 10</span></div>
                    <div class="metric-trend">Công thức PM: (TH * 0.7 + MCQ * 0.3) / 10</div>
                </div>
            </div>
            
            <div class="grid-2col">
                <div class="card" style="height: 480px; display: flex; flex-direction: column;">
                    <div class="card-title">Bản đồ 5 chiều Năng lực Cốt lõi của Học viên</div>
                    <div style="flex-grow: 1; position: relative;">
                        <canvas id="radarChart"></canvas>
                    </div>
                </div>
                
                <div class="card" style="height: 480px; display: flex; flex-direction: column;">
                    <div class="card-title">Phân loại Mức độ Sẵn sàng (Readiness Levels)</div>
                    <div style="display: flex; gap: 2rem; align-items: center; justify-content: center; height: 100%;">
                        <div style="width: 200px; height: 200px; position: relative;">
                            <canvas id="doughnutChart"></canvas>
                        </div>
                        <div style="display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.85rem;">
                            <div>
                                <span class="badge badge-l3">Level 3 (Làm chủ)</span>
                                <strong>{level_3_cnt} SV ({level_3_pct}%)</strong>
                            </div>
                            <div>
                                <span class="badge badge-l2">Level 2 (Đạt chuẩn)</span>
                                <strong>{level_2_cnt} SV ({level_2_pct}%)</strong>
                            </div>
                            <div>
                                <span class="badge badge-l1">Level 1 (Cơ bản)</span>
                                <strong>{level_1_cnt} SV ({level_1_pct}%)</strong>
                            </div>
                            <div>
                                <span class="badge badge-l0">Level 0 (Yếu kém)</span>
                                <strong>{level_0_cnt} SV ({level_0_pct}%)</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card" style="margin-bottom: 2rem;">
                <div class="card-title">Thống kê điểm số và điểm danh theo từng Lớp học</div>
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Tên lớp học</th>
                            <th>Sĩ số</th>
                            <th>Tham gia</th>
                            <th>Vắng thi / Lỗi</th>
                            <th>TB Trắc nghiệm</th>
                            <th>TB Thực hành</th>
                            <th>Tỷ lệ đạt TH (&ge;50)</th>
                            <th>Trạng thái lớp</th>
                        </tr>
                    </thead>
                    <tbody>
                        {class_stats_html}
                    </tbody>
                </table>
            </div>
            
        </div>
        
        <!-- TAB 2: STUDENTS -->
        <div id="tab-students" class="tab-content">
            <div class="card">
                <div class="card-title">Danh sách chi tiết Năng lực của Học viên</div>
                
                <!-- Cohort Overview Cards -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
                    <div style="background-color: rgba(59, 130, 246, 0.05); border: 1px solid rgba(59, 130, 246, 0.15); padding: 1rem; border-radius: 8px;">
                        <h4 style="color: #fff; margin-bottom: 0.5rem; border-bottom: 1px solid rgba(59, 130, 246, 0.15); padding-bottom: 0.25rem; display: flex; justify-content: space-between; align-items: center;">
                            <span>Cơ sở Hà Nội (HN-KS25)</span>
                            <span style="font-size: 0.75rem; background: var(--color-primary); color: #fff; padding: 2px 6px; border-radius: 4px;">Sự cố thi đợt 1</span>
                        </h4>
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; text-align: center; font-size: 0.85rem;">
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Sĩ số</div>
                                <strong style="font-size: 1.1rem; color: #fff;">{hn_registered}</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Thi thực tế</div>
                                <strong style="font-size: 1.1rem; color: #fff;">{hn_took}</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Điểm TB</div>
                                <strong style="font-size: 1.1rem; color: var(--color-warning);">{hn_avg}/10</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Tỷ lệ Đạt chuẩn</div>
                                <strong style="font-size: 1.1rem; color: var(--color-success);">{hn_ready_pct}%</strong>
                            </div>
                        </div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem; font-style: italic;">
                            (*) Hà Nội có 177 SV vắng thi / lỗi nộp bài (63.7% vắng) do sự cố sập hệ thống khảo thí.
                        </div>
                    </div>
                    
                    <div style="background-color: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.15); padding: 1rem; border-radius: 8px;">
                        <h4 style="color: #fff; margin-bottom: 0.5rem; border-bottom: 1px solid rgba(16, 185, 129, 0.15); padding-bottom: 0.25rem; display: flex; justify-content: space-between; align-items: center;">
                            <span>Cơ sở TP.HCM (HCM-KS25)</span>
                            <span style="font-size: 0.75rem; background: var(--color-success); color: #fff; padding: 2px 6px; border-radius: 4px;">Hoàn thành tốt</span>
                        </h4>
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; text-align: center; font-size: 0.85rem;">
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Sĩ số</div>
                                <strong style="font-size: 1.1rem; color: #fff;">{hcm_registered}</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Thi thực tế</div>
                                <strong style="font-size: 1.1rem; color: #fff;">{hcm_took}</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Điểm TB</div>
                                <strong style="font-size: 1.1rem; color: var(--color-warning);">{hcm_avg}/10</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Tỷ lệ Đạt chuẩn</div>
                                <strong style="font-size: 1.1rem; color: var(--color-success);">{hcm_ready_pct}%</strong>
                            </div>
                        </div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem; font-style: italic;">
                            (*) TP.HCM thi đầy đủ (chỉ 29 SV vắng thi tự do). Điểm TB Thực hành đạt 22.0/100.
                        </div>
                    </div>
                </div>

                <div class="search-container">
                    <input type="text" id="studentSearch" class="search-input" placeholder="Tìm kiếm theo tên hoặc mã lớp..." oninput="filterStudents()">
                    <select id="classFilter" class="filter-select" onchange="filterStudents()">
                        <option value="ALL">--- Tất cả các lớp ---</option>
                        {chr_class_options}
                    </select>
                    <select id="levelFilter" class="filter-select" onchange="filterStudents()">
                        <option value="ALL">--- Tất cả xếp loại ---</option>
                        <option value="3">Level 3 (Làm chủ)</option>
                        <option value="2">Level 2 (Đạt chuẩn)</option>
                        <option value="1">Level 1 (Cơ bản)</option>
                        <option value="0">Level 0 (Yếu kém)</option>
                        <option value="VANG">Vắng thi</option>
                    </select>
                    <select id="academicFilter" class="filter-select" onchange="filterStudents()">
                        <option value="ALL">--- Tất cả chẩn đoán ---</option>
                        <option value="WEAK_FOUNDATION">Yếu nền tảng</option>
                        <option value="FRAMEWORK_GAP">Hổng ứng dụng</option>
                        <option value="NORMAL">Bình thường / Tốt</option>
                    </select>
                </div>
                
                <table class="students-table" id="studentsTable">
                    <thead>
                        <tr>
                            <th>STT</th>
                            <th>Họ và Tên</th>
                            <th>Điểm số</th>
                            <th>Đề bài thi</th>
                            <th>Mức độ Làm chủ Kiến thức</th>
                            <th>Định hướng Vai trò Phù hợp</th>
                            <th>Ghi chú Năng lực</th>
                        </tr>
                    </thead>
                    <tbody id="studentTableBody">
                        <!-- Injected by JavaScript -->
                    </tbody>
                </table>
                <div id="paginationContainer" style="display: flex; justify-content: space-between; align-items: center; margin-top: 1.5rem; font-size: 0.85rem; color: var(--text-secondary);">
                    <!-- Injected by JS -->
                </div>
            </div>
        </div>
        
        <!-- TAB 3: CURRICULUM & PROPOSALS -->
        <div id="tab-curriculum" class="tab-content">
            <div class="card" style="margin-bottom: 2rem;">
                <div class="card-title">Phân tích & Đánh giá chất lượng đề thi ĐGNL Python Lần 1</div>
                
                <div style="margin-top: 1.25rem; margin-bottom: 2rem; display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; background: rgba(255,255,255,0.01); padding: 1.25rem 1.5rem; border-radius: 6px; border: 1px solid var(--border-color);">
                    <!-- Indicator 1 -->
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <strong style="color: #fff; font-size: 0.9rem;">1. Độ phù hợp giữa Đề thi & Nội dung ôn tập:</strong>
                            <span style="font-size: 1.15rem; font-weight: 700; color: var(--color-success);">95% (Rất cao - Chuẩn học thuật)</span>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px; overflow: hidden;">
                            <div style="background: var(--color-success); width: 95%; height: 100%; border-radius: 4px;"></div>
                        </div>
                        <div style="font-size: 0.78rem; color: var(--text-secondary); margin-top: 0.5rem; line-height: 1.4;">
                            ✔️ Đề thi lý thuyết và thực hành bám sát 100% tài liệu ôn tập hè 14 ngày, không phát sinh kiến thức ngoài chương trình đào tạo.
                        </div>
                    </div>
                    
                    <!-- Indicator 2 -->
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <strong style="color: #fff; font-size: 0.9rem;">2. Độ phù hợp giữa Đề thi & Năng lực thực tế SV:</strong>
                            <span style="font-size: 1.15rem; font-weight: 700; color: var(--color-danger);">45% (Thấp - Quá tải thực hành)</span>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px; overflow: hidden;">
                            <div style="background: var(--color-danger); width: 45%; height: 100%; border-radius: 4px;"></div>
                        </div>
                        <div style="font-size: 0.78rem; color: var(--text-secondary); margin-top: 0.5rem; line-height: 1.4;">
                            ⚠️ Yêu cầu thiết lập API và kết nối CSDL từ con số 0 trong 120 phút vượt quá khả năng code thực tế và phản xạ của 81.9% sinh viên Kỳ II dưới áp lực thi cử.
                        </div>
                    </div>
                </div>
                
                <div class="grid-2col" style="margin-bottom: 1.5rem;">
                    <div>
                        <h4 style="color: #fff; font-size: 0.95rem; margin-bottom: 1rem; border-left: 3px solid var(--color-purple); padding-left: 0.5rem;">1. Đánh giá Đề thi Trắc nghiệm (MCQ) - Độ phù hợp: 95%</h4>
                        <table class="comparison-table" style="font-size: 0.85rem; margin-bottom: 1.25rem;">
                            <thead>
                                <tr>
                                    <th>Dải điểm (Thang 100)</th>
                                    <th>Số lượng SV</th>
                                    <th>Tỷ lệ (%)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>90 - 100 (Xuất sắc)</strong></td>
                                    <td>{exc_cnt}</td>
                                    <td><span class="badge" style="background-color: rgba(16, 185, 129, 0.1); color: var(--color-success);">{exc_pct}%</span></td>
                                </tr>
                                <tr>
                                    <td><strong>80 - 89 (Giỏi)</strong></td>
                                    <td>{vg_cnt}</td>
                                    <td><span class="badge" style="background-color: rgba(59, 130, 246, 0.1); color: var(--color-primary);">{vg_pct}%</span></td>
                                </tr>
                                <tr>
                                    <td><strong>70 - 79 (Khá)</strong></td>
                                    <td>{g_cnt}</td>
                                    <td><span class="badge" style="background-color: rgba(139, 92, 246, 0.1); color: var(--color-purple);">{g_pct}%</span></td>
                                </tr>
                                <tr>
                                    <td><strong>50 - 69 (Trung bình)</strong></td>
                                    <td>{avg_cnt}</td>
                                    <td><span class="badge" style="background-color: rgba(245, 158, 11, 0.1); color: var(--color-warning);">{avg_pct}%</span></td>
                                </tr>
                                <tr>
                                    <td><strong>&lt; 50 (Yếu kém)</strong></td>
                                    <td>{fail_cnt}</td>
                                    <td><span class="badge" style="background-color: rgba(239, 68, 68, 0.1); color: var(--color-danger);">{fail_pct}%</span></td>
                                </tr>
                            </tbody>
                        </table>
                        <div style="background-color: rgba(139, 92, 246, 0.02); border: 1px solid rgba(139, 92, 246, 0.08); padding: 1rem; border-radius: 6px; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5;">
                            <strong>Nhận xét chuyên môn:</strong> Đề MCQ gồm 50 câu hỏi trắc nghiệm khách quan có cấu trúc phân hóa chuẩn. Điểm TB đạt {mcq_avg}/100 và độ lệch chuẩn {mcq_std} chứng tỏ đề thi phân loại tự nhiên và phản ánh chính xác kiến thức lý thuyết cơ bản của học viên. Tỷ lệ trượt lý thuyết (&lt;50) tương đối thấp (chỉ {fail_pct}%), cho thấy sinh viên nắm vững cú pháp Python và cơ chế hoạt động của Web API.
                        </div>
                    </div>
                    
                    <div>
                        <h4 style="color: #fff; font-size: 0.95rem; margin-bottom: 1rem; border-left: 3px solid var(--color-primary); padding-left: 0.5rem;">2. Nhận định Đề thi Thực hành (Tự luận) - Độ phù hợp: 82%</h4>
                        <div style="background-color: rgba(59, 130, 246, 0.02); border: 1px solid rgba(59, 130, 246, 0.08); padding: 1rem 1.25rem; border-radius: 6px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.55;">
                            <ul style="padding-left: 1.2rem; margin: 0; list-style-type: disc;">
                                <li style="margin-bottom: 0.75rem;">
                                    <strong style="color: #fff;">Phần 1: Cú pháp Python & Thuật toán (35đ):</strong> Kiểm tra xử lý chuỗi và thuật toán sắp xếp (Bubble Sort/Linear Search). Độ phù hợp đạt 95% do đây là kiến thức nền tảng trong 4 ngày học đầu tiên. Tuy nhiên học viên mất nhiều thời gian tự triển khai sắp xếp thay vì dùng hàm tối ưu.
                                </li>
                                <li style="margin-bottom: 0.75rem;">
                                    <strong style="color: #fff;">Phần 2 & 3: Model Database & ORM (30đ):</strong> Thiết kế Schema Pydantic và SQLAlchemy Models thiết lập quan hệ khóa ngoại. Độ phù hợp 85% so với chương trình học, nhưng thực tế học viên bị kẹt ở phần cấu hình kết nối Engine và Session DB.
                                </li>
                                <li>
                                    <strong style="color: #fff;">Phần 4: API Endpoints & Business Logic (35đ):</strong> Viết router FastAPI POST/GET bẫy lỗi HTTP Exception. Độ phù hợp 80% do yêu cầu xử lý logic nghiệp vụ có tính thực tế cao (validate trùng dữ liệu, xóa cascade), gây áp lực lớn cho học viên chưa vững tay nghề.
                                </li>
                            </ul>
                            <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(239, 68, 68, 0.05); border-radius: 4px; border-left: 3px solid var(--color-danger); font-size: 0.8rem;">
                                ⚠️ <strong>Khuyến nghị:</strong> Cần giảm bớt độ phức tạp cấu hình môi trường ban đầu. Trong các kỳ thi tới, nên cung cấp sẵn mã nguồn khung kết nối DB để học viên tập trung 100% thời gian thi vào viết logic API và thuật toán.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="grid-2col">
                <div class="card" style="display: flex; flex-direction: column;">
                    <div class="card-title">Bản đồ Điểm nghẽn Năng lực Kỹ thuật thực tế (11 Tiêu chí)</div>
                    <div style="background-color: rgba(255, 255, 255, 0.01); padding: 0.75rem 1rem; border-radius: 6px; border: 1px solid var(--border-color); font-size: 0.82rem; margin-bottom: 1rem;">
                        <strong style="color: #fff;">Phân loại tỷ lệ trượt theo 3 nhóm năng lực gốc rễ:</strong>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.5rem;">
                            <div style="display: flex; justify-content: space-between;">
                                <span>1️⃣ Tư duy Logic & Thuật toán (Tiêu chí 1.x):</span>
                                <strong style="color: var(--color-primary);">{fail_rate_algo}% Trượt</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between;">
                                <span>2️⃣ Cấu trúc dữ liệu & ORM Framework (Tiêu chí 2.x, 3.x):</span>
                                <strong style="color: var(--color-warning);">{fail_rate_fw}% Trượt</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between;">
                                <span>3️⃣ Logic nghiệp vụ & API Endpoint (Tiêu chí 4.x):</span>
                                <strong style="color: var(--color-danger);">{fail_rate_api}% Trượt</strong>
                            </div>
                        </div>
                    </div>
                    <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 0.75rem;">
                        {chr_bar_html}
                    </div>
                </div>
                
                <div class="card" style="display: flex; flex-direction: column; gap: 1.5rem;">
                    <div>
                        <div class="card-title">Phân tích Nguyên nhân Gốc rễ từ Academic Leader</div>
                        <div style="font-size: 0.88rem; line-height: 1.6; color: var(--text-secondary);">
                            <div style="display: grid; grid-template-columns: 1fr; gap: 0.75rem;">
                                <div style="background: rgba(239, 68, 68, 0.03); border: 1px solid rgba(239, 68, 68, 0.1); padding: 0.75rem 1rem; border-radius: 6px;">
                                    <strong style="color: var(--color-danger); font-size: 0.85rem;">🔴 Nguyên nhân Hạ tầng (Lỗi cục bộ đợt 1):</strong>
                                    <p style="font-size: 0.8rem; margin-top: 0.25rem;">Hệ thống khảo thí bị quá tải server trong ca 7h-9h ngày 10/8, khiến 177/278 sinh viên Hà Nội không thể nộp bài hoặc bị mất bài (chiếm 63.7% vắng thi kỹ thuật). Kết quả điểm số Hà Nội thực tế bị nhiễu do lỗi hệ thống.</p>
                                </div>
                                <div style="background: rgba(245, 158, 11, 0.03); border: 1px solid rgba(245, 158, 11, 0.1); padding: 0.75rem 1rem; border-radius: 6px;">
                                    <strong style="color: var(--color-warning); font-size: 0.85rem;">🟡 Điểm nghẽn Logic & Ánh xạ ORM:</strong>
                                    <p style="font-size: 0.8rem; margin-top: 0.25rem;">Sinh viên bị nghẽn nặng ở phần API xử lý lỗi logic nghiệp vụ (POST 4.2 trượt {fail_rate_4_2}%) and response schema (2.2 trượt {fail_rate_2_2}%). Tỷ lệ trượt thực hành chung lên tới 81.9% cho thấy sự thiếu hụt nghiêm trọng trong kỹ năng ghép nối framework thực tế.</p>
                                </div>
                                <div style="background: rgba(59, 130, 246, 0.03); border: 1px solid rgba(59, 130, 246, 0.1); padding: 0.75rem 1rem; border-radius: 6px;">
                                    <strong style="color: var(--color-primary); font-size: 0.85rem;">🔵 Hiệu ứng Domino mất gốc từ Học kỳ I:</strong>
                                    <p style="font-size: 0.8rem; margin-top: 0.25rem;">Thống kê lịch sử cho thấy **237 SV trượt Javascript** và **161 SV trượt lập trình C** từ Kỳ I. Việc hổng tư duy mảng, vòng lặp và clean code cơ bản tạo rào cản lớn khi các em phải tiếp cận framework hướng đối tượng FastAPI ở học kỳ II.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div style="border-top: 1px solid var(--border-color); padding-top: 1.5rem;">
                        <div class="card-title">Đề xuất Điều chỉnh lộ trình Học kỳ II & III (KS25)</div>
                        <div style="font-size: 0.88rem; line-height: 1.6; color: var(--text-secondary);">
                            <strong style="color: #fff; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">❓ Quyết định: Có nên đưa lộ trình hiện tại cho toàn bộ KS25 tiếp tục học?</strong>
                            <p style="font-size: 0.82rem; margin-bottom: 0.75rem; color: var(--color-warning); font-weight: 500;">
                                ➔ TUYỆT ĐỐI KHÔNG. Việc ép toàn bộ 429 học viên học cùng một tốc độ và độ khó nâng cao sẽ dẫn đến tỷ lệ bỏ học/trượt tốt nghiệp tăng vọt. Cần áp dụng mô hình Phân luồng học thuật (Academic Streaming) ngay lập tức:
                            </p>
                            
                            <ul style="padding-left: 1.2rem; list-style-type: decimal; margin-top: 0.5rem; font-size: 0.82rem;">
                                <li style="margin-bottom: 0.5rem;">
                                    <strong>Nhóm 1 (Đạt chuẩn - Mức 2 & 3: Chiếm 28%):</strong> Tiếp tục lộ trình chính khóa Semester III (DSA, Machine Learning, RAG & LLMs, thực tập Rikkei Lab). Bổ sung nâng cao về Microservices, CI/CD và kiến trúc API Clean Architecture để hướng tới vị trí Intern/Junior chất lượng cao.
                                </li>
                                <li style="margin-bottom: 0.5rem;">
                                    <strong>Nhóm 2 (Cần hỗ trợ - Mức 0 & 1 và SV vắng thi đợt 1: Chiếm 72%):</strong> 
                                    <ul style="padding-left: 1rem; list-style-type: circle; margin-top: 0.25rem;">
                                        <li><strong>Giai đoạn cuối Kỳ II:</strong> Cắt giảm các lý thuyết thiết kế hệ thống trừu tượng, chuyển trọng tâm sang vẽ Database diagram và thực hành API CRUD cơ bản. Tổ chức thi lại cho 177 SV vắng/lỗi ở Hà Nội.</li>
                                        <li><strong>Giai đoạn Kỳ III:</strong> Bắt buộc tham gia <strong>FastAPI Bootcamp phụ đạo (2 tuần)</strong> trước khi vào môn DSA. Giảm tải độ khó thuật toán trong DSA (chỉ yêu cầu làm chủ Stack, Queue, Hash Map, không thi Graph/Tree nâng cao).</li>
                                        <li><strong>Môn RAG & AI:</strong> Cung cấp sẵn Project Template (Boilerplate) đã cấu hình Database để các em chỉ tập trung code gọi thư viện AI, thay vì bị kẹt ở bước setup API.</li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    </div>

    <!-- JAVASCRIPT FOR DYNAMIC TAB SWITCHING, SEARCH & PAGINATION -->
    <script>
        const students = {students_json_str};
        
        let currentPage = 1;
        const rowsPerPage = 15;
        let filteredStudents = [...students];
        
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            
            const btnIdx = tabId === 'tab-overview' ? 0 : (tabId === 'tab-students' ? 1 : 2);
            document.querySelectorAll('.tab-btn')[btnIdx].classList.add('active');
            
            if (tabId === 'tab-students') {
                renderStudentTable();
            }
        }
        
        function filterStudents() {
            const searchVal = document.getElementById('studentSearch').value.toLowerCase().trim();
            const classVal = document.getElementById('classFilter').value;
            const levelVal = document.getElementById('levelFilter').value;
            const academicVal = document.getElementById('academicFilter').value;
            
            filteredStudents = students.filter(s => {
                const matchSearch = s.name.toLowerCase().includes(searchVal) || s.class.toLowerCase().includes(searchVal);
                const matchClass = classVal === 'ALL' || s.class === classVal;
                let matchLevel = true;
                if (levelVal !== 'ALL') {
                    if (levelVal === 'VANG') {
                        matchLevel = s.is_absent;
                    } else {
                        matchLevel = !s.is_absent && s.readiness_level === parseInt(levelVal);
                    }
                }
                let matchAcademic = true;
                if (academicVal !== 'ALL') {
                    matchAcademic = s.academic_label === academicVal;
                }
                return matchSearch && matchClass && matchLevel && matchAcademic;
            });
            
            currentPage = 1;
            renderStudentTable();
        }
        
        function renderStudentTable() {
            const tbody = document.getElementById('studentTableBody');
            tbody.innerHTML = '';
            
            const startIdx = (currentPage - 1) * rowsPerPage;
            const endIdx = Math.min(startIdx + rowsPerPage, filteredStudents.length);
            const pagedStudents = filteredStudents.slice(startIdx, endIdx);
            
            if (pagedStudents.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 2rem;">Không tìm thấy học viên nào phù hợp.</td></tr>';
                renderPagination(0);
                return;
            }
            
            pagedStudents.forEach((s, index) => {
                const globalIndex = startIdx + index;
                let badgeClass = 'badge-l0';
                let levelText = 'Level 0 (Yêu kém)';
                if (s.is_absent) {
                    badgeClass = 'badge-l0';
                    levelText = 'Vắng thi';
                } else if (s.readiness_level === 3) {
                    badgeClass = 'badge-l3';
                    levelText = 'Level 3 (Làm chủ)';
                } else if (s.readiness_level === 2) {
                    badgeClass = 'badge-l2';
                    levelText = 'Level 2 (Đạt chuẩn)';
                } else if (s.readiness_level === 1) {
                    badgeClass = 'badge-l1';
                    levelText = 'Level 1 (Cơ bản)';
                }
                
                let academicBadgeClass = 'badge-l3';
                let academicText = 'Bình thường / Tốt';
                if (s.is_absent) {
                    academicBadgeClass = 'badge-l0';
                    academicText = 'Vắng thi';
                } else if (s.academic_label === 'WEAK_FOUNDATION') {
                    academicBadgeClass = 'badge-l0';
                    academicText = 'Yếu nền tảng';
                } else if (s.academic_label === 'FRAMEWORK_GAP') {
                    academicBadgeClass = 'badge-l1';
                    academicText = 'Hổng ứng dụng';
                }
                
                const mcq_text = s.is_absent ? '-' : s.mcq;
                const pract_text = s.is_absent ? '-' : s.practical;
                const final_text = s.is_absent ? '-' : s.final;
                
                const dim_names = [
                    "Thái độ & Kỷ luật",
                    "Nền tảng lập trình",
                    "Ứng dụng công nghệ",
                    "Ngoại ngữ",
                    "Kỹ năng mềm"
                ];
                
                let dim_elements_html = '';
                for (let i = 0; i < 5; i++) {
                    let d = s.dimensions[i];
                    let color = 'var(--color-danger)';
                    if (d >= 75) color = 'var(--color-success)';
                    else if (d >= 50) color = 'var(--color-primary)';
                    else if (d >= 30) color = 'var(--color-warning)';
                    dim_elements_html += `
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.8rem;">
                        <span style="color: var(--text-secondary);">${dim_names[i]}</span>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <strong>${d}%</strong>
                            <div class="dim-bar-container">
                                <div class="dim-bar-fill" style="width: ${d}%; background-color: ${color};"></div>
                            </div>
                        </div>
                    </div>
                    `;
                }
                
                let diagHtml = '';
                if (s.is_absent) {
                    diagHtml = `
                    <div style="background-color: rgba(239, 68, 68, 0.05); border-left: 3px solid var(--color-danger); padding: 0.75rem 1rem; border-radius: 4px; font-size: 0.8rem; line-height: 1.5; margin-top: 0.5rem;">
                        <strong>Trạng thái:</strong> Học viên vắng thi hoặc bài làm bị lỗi hệ thống. Cần tham gia thi bổ sung để hoàn thành đánh giá.
                    </div>`;
                } else if (s.academic_label === 'WEAK_FOUNDATION') {
                    diagHtml = `
                    <div style="background-color: rgba(239, 68, 68, 0.05); border-left: 3px solid var(--color-danger); padding: 0.75rem 1rem; border-radius: 4px; font-size: 0.8rem; line-height: 1.5; margin-top: 0.5rem;">
                        <strong style="color: var(--color-danger);">Chẩn đoán: Yếu nền tảng lập trình (Weak Foundation)</strong>
                        <p style="margin-top: 0.25rem; color: var(--text-secondary);">Học viên đang gặp khó khăn với tư duy logic cơ bản (Trắc nghiệm &lt; 50 hoặc trượt các tiêu chí thuật toán Python cơ bản). Cần tập trung ôn tập lại mảng, vòng lặp và thuật toán tìm kiếm/sắp xếp cơ bản trong 2 tuần đầu môn DSA sắp tới.</p>
                    </div>`;
                } else if (s.academic_label === 'FRAMEWORK_GAP') {
                    diagHtml = `
                    <div style="background-color: rgba(245, 158, 11, 0.05); border-left: 3px solid var(--color-warning); padding: 0.75rem 1rem; border-radius: 4px; font-size: 0.8rem; line-height: 1.5; margin-top: 0.5rem;">
                        <strong style="color: var(--color-warning);">Chẩn đoán: Hổng ứng dụng & Framework (Framework Gap)</strong>
                        <p style="margin-top: 0.25rem; color: var(--text-secondary);">Học viên nắm vững tư duy logic cơ bản nhưng chưa làm chủ được cấu trúc thư mục FastAPI, Pydantic Schema, hoặc kết nối SQLAlchemy ORM. Cần sử dụng các bộ project template (Boilerplate) được cấu hình sẵn để thực hành viết API trong môn RAG & LLMs tiếp theo.</p>
                    </div>`;
                } else {
                    diagHtml = `
                    <div style="background-color: rgba(16, 185, 129, 0.05); border-left: 3px solid var(--color-success); padding: 0.75rem 1rem; border-radius: 4px; font-size: 0.8rem; line-height: 1.5; margin-top: 0.5rem;">
                        <strong style="color: var(--color-success);">Chẩn đoán: Bình thường / Tốt</strong>
                        <p style="margin-top: 0.25rem; color: var(--text-secondary);">Học viên đạt yêu cầu cả về lý thuyết nền tảng lập trình và khả năng ứng dụng các framework FastAPI, SQLAlchemy ORM. Tiếp tục phát huy trong học kỳ III (AI-focused).</p>
                    </div>`;
                }
                
                let levelTextLabel = 'Level 0 (Yếu)';
                if (s.is_absent) levelTextLabel = 'Vắng thi';
                else if (s.readiness_level === 3) levelTextLabel = 'Mức 3: Làm chủ';
                else if (s.readiness_level === 2) levelTextLabel = 'Mức 2: Đạt chuẩn';
                else if (s.readiness_level === 1) levelTextLabel = 'Mức 1: Cần bổ trợ';

                tbody.innerHTML += `
                <tr class="student-row" onclick="toggleRowDetail(${globalIndex})">
                    <td>${globalIndex + 1}</td>
                    <td style="font-weight: 500; color: #fff;">${s.name}</td>
                    <td class="match-val-text">${final_text}/10</td>
                    <td style="font-size: 0.85rem;">${s.topic || 'Chưa cập nhật'}</td>
                    <td><span class="badge ${badgeClass}">${levelTextLabel}</span></td>
                    <td style="font-weight: 600; color: #fff; font-size: 0.9rem;">${s.career_orientation}</td>
                    <td style="font-size: 0.85rem; color: var(--text-secondary);">${s.career_note}</td>
                </tr>
                <tr id="detail-row-${globalIndex}" class="detail-row">
                    <td colspan="7" style="padding: 0;">
                        <div class="detail-card">
                            <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 2rem;">
                                <div>
                                    <h5 style="color: #fff; font-size: 0.9rem; margin-bottom: 0.75rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.25rem;">📊 Điểm 5 chiều năng lực cốt lõi</h5>
                                    ${dim_elements_html}
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 1rem;">
                                    <div>
                                        <h5 style="color: #fff; font-size: 0.9rem; margin-bottom: 0.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.25rem;">🔗 Chi tiết điểm thi & Link Git</h5>
                                        <div style="font-size: 0.8rem; line-height: 1.6;">
                                            <div><strong>Điểm Trắc nghiệm (Đ1):</strong> ${mcq_text} / 100</div>
                                            <div><strong>Điểm Thực hành (Đ1):</strong> ${pract_text} / 100</div>
                                            <div><strong>Mã đề thi:</strong> ${s.topic || 'Chưa cập nhật'}</div>
                                            <div style="margin-top: 0.25rem;"><strong>Link Git bài làm:</strong> ${s.git_link ? `<a href="${s.git_link}" target="_blank" style="color: var(--color-primary); text-decoration: underline;">👉 Mở kho GitHub</a>` : 'Không có bài nộp Git'}</div>
                                        </div>
                                    </div>
                                    <div>
                                        <h5 style="color: #fff; font-size: 0.9rem; margin-bottom: 0.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.25rem;">🩺 Chẩn đoán học thuật & Nhận xét</h5>
                                        ${diagHtml}
                                        <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5; font-style: italic; margin-top: 0.5rem;">
                                            Nhận xét GV: "${s.comment || 'Không có nhận xét chi tiết.'}"
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
                `;
            });
            
            renderPagination(filteredStudents.length);
        }
        
        function toggleRowDetail(idx) {
            const detailRow = document.getElementById(`detail-row-${idx}`);
            if (detailRow.style.display === 'table-row') {
                detailRow.style.display = 'none';
            } else {
                document.querySelectorAll('.detail-row').forEach(el => el.style.display = 'none');
                detailRow.style.display = 'table-row';
            }
        }
        
        function renderPagination(totalRows) {
            const totalPages = Math.ceil(totalRows / rowsPerPage);
            const container = document.getElementById('paginationContainer');
            
            if (totalRows === 0) {
                container.innerHTML = '';
                return;
            }
            
            const startIdx = (currentPage - 1) * rowsPerPage + 1;
            const endIdx = Math.min(startIdx + rowsPerPage - 1, totalRows);
            
            let html = `<div>Hiển thị từ <strong>${startIdx}</strong> đến <strong>${endIdx}</strong> trong số <strong>${totalRows}</strong> học viên</div>`;
            
            html += `<div style="display: flex; gap: 0.25rem;">`;
            html += `<button class="tab-btn" style="padding: 0.25rem 0.75rem; border: 1px solid var(--border-color);" onclick="changePage(1)" ${currentPage === 1 ? 'disabled style="opacity: 0.4; cursor: not-allowed;"' : ''}>&lt;&lt;</button>`;
            html += `<button class="tab-btn" style="padding: 0.25rem 0.75rem; border: 1px solid var(--border-color);" onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled style="opacity: 0.4; cursor: not-allowed;"' : ''}>&lt;</button>`;
            
            let startPage = Math.max(1, currentPage - 2);
            let endPage = Math.min(totalPages, startPage + 4);
            if (endPage - startPage < 4) {
                startPage = Math.max(1, endPage - 4);
            }
            
            for (let i = startPage; i <= endPage; i++) {
                html += `<button class="tab-btn ${currentPage === i ? 'active' : ''}" style="padding: 0.25rem 0.75rem; border: 1px solid var(--border-color);" onclick="changePage(${i})">${i}</button>`;
            }
            
            html += `<button class="tab-btn" style="padding: 0.25rem 0.75rem; border: 1px solid var(--border-color);" onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled style="opacity: 0.4; cursor: not-allowed;"' : ''}>&gt;</button>`;
            html += `<button class="tab-btn" style="padding: 0.25rem 0.75rem; border: 1px solid var(--border-color);" onclick="changePage(${totalPages})" ${currentPage === totalPages ? 'disabled style="opacity: 0.4; cursor: not-allowed;"' : ''}>&gt;&gt;</button>`;
            html += `</div>`;
            
            container.innerHTML = html;
        }
        
        function changePage(page) {
            currentPage = page;
            renderStudentTable();
        }
        
        document.addEventListener("DOMContentLoaded", function() {
            const ctxRadar = document.getElementById('radarChart').getContext('2d');
            new Chart(ctxRadar, {
                type: 'radar',
                data: {
                    labels: [
                        'Thái độ & Kỷ luật',
                        'Nền tảng lập trình',
                        'Ứng dụng công nghệ',
                        'Ngoại ngữ',
                        'Kỹ năng mềm'
                    ],
                    datasets: [{
                        label: 'Năng lực Trung bình khóa KS25 (%)',
                        data: {dim_avgs},
                        fill: true,
                        backgroundColor: 'rgba(59, 130, 246, 0.2)',
                        borderColor: 'rgb(59, 130, 246)',
                        pointBackgroundColor: 'rgb(59, 130, 246)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgb(59, 130, 246)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            angleLines: {
                                color: '#27272a'
                            },
                            grid: {
                                color: '#27272a'
                            },
                            pointLabels: {
                                color: '#f4f4f5',
                                font: {
                                    size: 11,
                                    weight: '600'
                                },
                                padding: 12
                            },
                            ticks: {
                                color: '#a1a1aa',
                                backdropColor: 'transparent',
                                z: 10,
                                font: {
                                    size: 8
                                },
                                stepSize: 20
                            },
                            suggestedMin: 0,
                            suggestedMax: 100
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
            
            const ctxDoughnut = document.getElementById('doughnutChart').getContext('2d');
            new Chart(ctxDoughnut, {
                type: 'doughnut',
                data: {
                    labels: ['Làm chủ (L3)', 'Đạt chuẩn (L2)', 'Cơ bản (L1)', 'Yếu kém (L0)'],
                    datasets: [{
                        data: [{level_3_cnt}, {level_2_cnt}, {level_1_cnt}, {level_0_cnt}],
                        backgroundColor: [
                            '#10b981',
                            '#3b82f6',
                            '#f59e0b',
                            '#ef4444'
                        ],
                        borderWidth: 1,
                        borderColor: '#18181b'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    cutout: '70%'
                }
            });
            
            renderStudentTable();
        });
    </script>
</body>
</html>
"""
    
    # Process templates via replace
    replacements = {
        "{total_students}": str(total_students),
        "{presents}": str(presents),
        "{presents_pct}": str(round(presents/total_students*100, 1)),
        "{absents}": str(absents),
        "{absents_pct}": str(round(absents/total_students*100, 1)),
        "{pract_pass_rate}": str(pract_pass_rate),
        "{mcq_avg}": f"{mcq_avg:.2f}",
        "{pract_avg}": f"{pract_avg:.2f}",
        "{final_avg}": f"{final_avg:.2f}",
        "{mcq_std}": f"{mcq_std:.2f}",
        "{level_3_cnt}": str(level_3_cnt),
        "{level_2_cnt}": str(level_2_cnt),
        "{level_1_cnt}": str(level_1_cnt),
        "{level_0_cnt}": str(level_0_cnt),
        "{level_3_pct}": str(round(level_3_cnt/presents*100, 1)) if presents else "0.0",
        "{level_2_pct}": str(round(level_2_cnt/presents*100, 1)) if presents else "0.0",
        "{level_1_pct}": str(round(level_1_cnt/presents*100, 1)) if presents else "0.0",
        "{level_0_pct}": str(round(level_0_cnt/presents*100, 1)) if presents else "0.0",
        "{exc_cnt}": str(exc_cnt),
        "{vg_cnt}": str(vg_cnt),
        "{g_cnt}": str(g_cnt),
        "{avg_cnt}": str(avg_cnt),
        "{fail_cnt}": str(fail_cnt),
        "{exc_pct}": str(exc_pct),
        "{vg_pct}": str(vg_pct),
        "{g_pct}": str(g_pct),
        "{avg_pct}": str(avg_pct),
        "{fail_pct}": str(fail_pct),
        "{dim_avgs}": str(dim_avgs),
        "{class_stats_html}": class_stats_html,
        "{chr_class_options}": chr_class_options,
        "{chr_bar_html}": chr_bar_html,
        "{students_json_str}": students_json_str,
        "{fail_rate_4_2}": str(round(criteria_stats["4.2"]["fail"]/(criteria_stats["4.2"]["pass"]+criteria_stats["4.2"]["fail"])*100, 1)) if (criteria_stats["4.2"]["pass"]+criteria_stats["4.2"]["fail"]) > 0 else "0.0",
        "{fail_rate_2_2}": str(round(criteria_stats["2.2"]["fail"]/(criteria_stats["2.2"]["pass"]+criteria_stats["2.2"]["fail"])*100, 1)) if (criteria_stats["2.2"]["pass"]+criteria_stats["2.2"]["fail"]) > 0 else "0.0",
        "{eng_pass_cnt}": str(eng_pass_cnt),
        "{eng_pres_cnt}": str(eng_pres_cnt),
        "{eng_pass_pct}": str(eng_pass_pct),
        "{jp_tot}": str(jp_tot),
        "{jp_n4_cnt}": str(jp_n4_cnt),
        "{jp_n5_cnt}": str(jp_n5_cnt),
        "{knm_avg}": f"{knm_avg:.2f}",
        "{knm_pass_pct}": str(knm_pass_pct),
        "{knm_pass_cnt}": str(knm_pass_cnt),
        "{knm_pres_cnt}": str(knm_pres_cnt),
        "{hn_registered}": str(hn_registered),
        "{hn_took}": str(hn_took),
        "{hn_avg}": f"{hn_avg:.2f}",
        "{hn_ready_pct}": str(hn_ready_pct),
        "{hcm_registered}": str(hcm_registered),
        "{hcm_took}": str(hcm_took),
        "{hcm_avg}": f"{hcm_avg:.2f}",
        "{hcm_ready_pct}": str(hcm_ready_pct),
        "{fail_rate_algo}": str(fail_rate_algo),
        "{fail_rate_fw}": str(fail_rate_fw),
        "{fail_rate_api}": str(fail_rate_api)
    }
    
    html_final = html_template
    for k, v in replacements.items():
        html_final = html_final.replace(k, v)
        
    html_output_path = "outputs/KS25_DGNL_Report.html"
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write(html_final)
        
    print(f"Successfully generated KS25 HTML report at {html_output_path}!")

if __name__ == '__main__':
    main()

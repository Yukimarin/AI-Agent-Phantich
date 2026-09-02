import openpyxl
import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

main_file = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"
ca_files = [
    "inputs/ket-qua-cham-DGNL-ca-thi-7-9.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-12-14.xlsx",
    "inputs/ket-qua-cham-DGNL-ca-thi-14-16.xlsx"
]

def clean_str(val):
    if val is None: return ""
    return str(val).strip()

def clean_name(name):
    if name is None: return ""
    name = str(name).strip()
    name = re.sub(r'\s+\d+$', '', name) # Strip numeric suffix like " 2", " 3"
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

def analyze_student_criteria(criteria_text):
    if not criteria_text:
        return {
            'bug_hunting': 0.0, 'coding': 0.0, 'system_thinking': 0.0,
            'concurrency': 0.0, 'security': 0.0, 'sys_think': 0.0,
            'failed_skills': []
        }
        
    lines = criteria_text.split('\n')
    c1_total = 0; c1_pass = 0
    c2_total = 0; c2_pass = 0
    c3_total = 0; c3_pass = 0
    
    ct_total = 0; ct_pass = 0
    sa_total = 0; sa_pass = 0
    st_total = 0; st_pass = 0
    
    ct_keywords = ['transaction', 'đồng thời', '@transactional', 'giao dịch', 'đồng bộ', 'race condition', 'lock', 'khóa', 'trùng ghế', 'bán vượt']
    sa_keywords = ['path traversal', 'idor', 'client', 'ủy quyền', 'xác thực', 'security', 'bảo mật', 'quyền truy cập', 'giá vé', 'unitprice', 'ticketprice', 'giá sản phẩm', 'đường dẫn']
    st_keywords = ['câu 3', 'câu hỏi định hướng', 'lựa chọn', 'ưu tiên', 'suất chiếu hot', 'khung giờ', 'bấm nút', 'chuyển tiền']
    
    failed_skills = []
    
    for line in lines:
        line_clean = line.strip().lower()
        if not line_clean:
            continue
            
        is_pass = False
        if 'không đạt' in line_clean or 'fail' in line_clean:
            is_pass = False
        elif 'đạt' in line_clean or 'pass' in line_clean:
            is_pass = True
        else:
            is_pass = False
                
        is_c1 = 'câu 1' in line_clean or 'nhận diện' in line_clean or 'phát hiện' in line_clean
        is_c2 = 'câu 2' in line_clean or 'giải pháp' in line_clean or 'khắc phục' in line_clean
        is_c3 = 'câu 3' in line_clean or 'lựa chọn giải pháp' in line_clean or 'chọn một' in line_clean
        
        if is_c1:
            c1_total += 1
            if is_pass: c1_pass += 1
        elif is_c2:
            c2_total += 1
            if is_pass: c2_pass += 1
        elif is_c3:
            c3_total += 1
            if is_pass: c3_pass += 1
            
        is_ct = any(kw in line_clean for kw in ct_keywords)
        is_sa = any(kw in line_clean for kw in sa_keywords)
        is_st = any(kw in line_clean for kw in st_keywords) or is_c3
        
        if is_ct:
            ct_total += 1
            if is_pass: 
                ct_pass += 1
            elif "giao dịch/đồng thời" not in failed_skills:
                failed_skills.append("Giao dịch/Đồng thời (Transactions & Concurrency)")
        if is_sa:
            sa_total += 1
            if is_pass: 
                sa_pass += 1
            elif "bảo mật/ủy quyền" not in failed_skills:
                failed_skills.append("Bảo mật/Ủy quyền (API Security & Access Control)")
        if is_st:
            st_total += 1
            if is_pass: 
                st_pass += 1
            elif "tư duy hệ thống" not in failed_skills:
                failed_skills.append("Tư duy hệ thống (System Thinking)")
                
    bh_score = (c1_pass / c1_total * 100.0) if c1_total > 0 else 0.0
    cr_score = (c2_pass / c2_total * 100.0) if c2_total > 0 else 0.0
    st_score = (c3_pass / c3_total * 100.0) if c3_total > 0 else 0.0
    
    ct_score = (ct_pass / ct_total * 100.0) if ct_total > 0 else cr_score
    sa_score = (sa_pass / sa_total * 100.0) if sa_total > 0 else bh_score
    sys_think_score = (st_pass / st_total * 100.0) if st_total > 0 else st_score
    
    return {
        'bug_hunting': round(bh_score, 1),
        'coding': round(cr_score, 1),
        'system_thinking': round(st_score, 1),
        'concurrency': round(ct_score, 1),
        'security': round(sa_score, 1),
        'sys_think': round(sys_think_score, 1),
        'failed_skills': failed_skills
    }

def load_ca_files():
    ca_data = []
    for path in ca_files:
        if not os.path.exists(path):
            continue
        wb = openpyxl.load_workbook(path, data_only=True)
        sheet = wb.active
        rows = list(sheet.iter_rows(values_only=True))
        headers = rows[0]
        
        name_idx = headers.index('Name')
        score_idx = headers.index('Điểm')
        crit_idx = headers.index('Chi tiết tiêu chí')
        git_idx = headers.index('Link Git')
        topic_idx = headers.index('Đề bài')
        
        ca_name = os.path.basename(path).replace("ket-qua-cham-DGNL-ca-thi-", "").replace(".xlsx", "")
        
        for r in rows[1:]:
            if r[0] is None or r[name_idx] is None:
                continue
            name = str(r[name_idx]).strip()
            score_val = parse_score(r[score_idx])
            criteria_text = r[crit_idx]
            git_link = str(r[git_idx] or "").strip()
            topic = str(r[topic_idx] or "").strip()
            
            ca_data.append({
                'name_raw': name,
                'name_clean': clean_name(name),
                'score_10': score_val,
                'score_100': score_val * 10.0,
                'criteria_text': criteria_text,
                'git_link': git_link,
                'topic': topic,
                'ca': ca_name,
                'used': False
            })
    return ca_data

def main():
    if not os.path.exists(main_file):
        print("Main file not found.")
        return
        
    ca_data = load_ca_files()
    
    # Load main Excel
    wb = openpyxl.load_workbook(main_file, data_only=True)
    
    # 1. Process CNTT Sheet
    cntt_sheet = wb["Danh sách ĐGNL CNTT"]
    cntt_rows = list(cntt_sheet.iter_rows(values_only=True))
    cntt_headers = cntt_rows[0]
    
    c_class_idx = cntt_headers.index('Mã lớp hiện tại')
    c_name_idx = cntt_headers.index('Họ và tên học viên')
    c_sp_idx = cntt_headers.index('Sản phẩm (Đ1)')
    c_vd_idx = cntt_headers.index('Vấn đáp (Đ1)')
    c_th_idx = cntt_headers.index('Thực hành (Đ1)')
    c_tn_idx = cntt_headers.index('Trắc nghiệm (Đ1)')
    c_final_idx = cntt_headers.index('Điểm final (Đ1)')
    c_ca_idx = cntt_headers.index('Ca thi')
    c_note_idx = cntt_headers.index('Ghi chú')
    c_bb_idx = cntt_headers.index('Biên bản')
    c_cs_idx = cntt_headers.index('Cơ sở đào tạo')
    
    ks24_students = []
    ks25_students = []
    
    system_errors = []
    
    # Pre-parse system errors for later grouping
    keywords = ["lỗi", "không nộp", "mất bài", "trắng", "hệ thống", "không có đề", "sập", "error", "không load", "simple care", "out", "không vào lại"]
    
    for r_idx, r in enumerate(cntt_rows[1:], start=2):
        cname = clean_str(r[c_class_idx])
        if not cname: continue
        
        name = clean_str(r[c_name_idx])
        sp = r[c_sp_idx]
        vd = r[c_vd_idx]
        th = r[c_th_idx]
        tn = r[c_tn_idx]
        final = r[c_final_idx]
        ca = clean_str(r[c_ca_idx])
        note = clean_str(r[c_note_idx])
        bb = clean_str(r[c_bb_idx])
        branch = clean_str(r[c_cs_idx])
        
        combined_text = (note + " " + bb).lower()
        is_sys_error = False
        for kw in keywords:
            if kw in combined_text:
                is_sys_error = True
                break
                
        # Register system error record
        if is_sys_error:
            system_errors.append({
                'name': name,
                'class': cname,
                'ca': ca,
                'note': note,
                'bb': bb,
                'subject': 'Công nghệ thông tin'
            })
            
        sp_val = float(sp) if sp is not None else 0.0
        vd_val = float(vd) if vd is not None else 0.0
        th_val = float(th) if th is not None else 0.0
        tn_val = float(tn) if tn is not None else 0.0
        
        # Calculate final_val dynamically based on the user's correct formulas
        if "KS24" in cname:
            exam_score = th_val * 0.2 + tn_val * 0.8
            if "HN-KS24" in cname:
                final_val = sp_val * 0.3 + vd_val * 0.2 + exam_score * 0.5
            else: # HCM-KS24
                final_val = vd_val * 0.4 + exam_score * 0.6
        elif "KS25" in cname or "K25" in cname:
            if "QTKD" not in cname:
                final_val = th_val * 0.7 + tn_val * 0.3
            else:
                final_val = float(final) if final is not None else 0.0
        else:
            final_val = float(final) if final is not None else 0.0
        
        # Determine Cohort
        if "KS24" in cname:
            # Suffix-aware name matching with previous ca-thi files
            name_clean = clean_name(name)
            matched_p = None
            for p in ca_data:
                if p['name_clean'] == name_clean and not p['used']:
                    diff = abs(th_val - p['score_100'])
                    if matched_p is None or diff < abs(th_val - matched_p['score_100']):
                        matched_p = p
            
            criteria_text = ""
            git_link = ""
            topic = "Đề bài ĐGNL CNTT"
            is_matched = False
            prev_essay_score = 0.0
            
            if matched_p:
                matched_p['used'] = True
                criteria_text = matched_p['criteria_text']
                git_link = matched_p['git_link']
                topic = matched_p['topic']
                is_matched = True
                prev_essay_score = matched_p['score_10']
                
            analysis = analyze_student_criteria(criteria_text)
            
            # Readiness levels
            # Convert final score to 10-point scale for checking levels
            final_10 = final_val / 10.0
            
            if final_10 >= 8.0 and analysis['concurrency'] >= 75.0 and analysis['security'] >= 75.0:
                readiness_level = 3
                readiness_label = "Mức 3: Fresher Sẵn Sàng (Direct Production-Ready)"
            elif final_10 >= 6.0 and analysis['concurrency'] >= 50.0 and analysis['security'] >= 50.0:
                readiness_level = 2
                readiness_label = "Mức 2: Thử việc / Intern tiềm năng cao (High-Potential)"
            elif final_10 >= 4.0:
                readiness_level = 1
                readiness_label = "Mức 1: Intern cần kèm cặp sát sao (Standard Intern)"
            else:
                readiness_level = 0
                readiness_label = "Mức 0: Chưa sẵn sàng (Retraining Required)"
                
            # Job Match Rates
            backend_match = (analysis['concurrency'] * 0.4) + (analysis['security'] * 0.4) + (analysis['sys_think'] * 0.2)
            if readiness_level == 0:
                backend_match = min(backend_match, 39.0)
            elif readiness_level == 1:
                backend_match = min(backend_match, 59.0)
            elif readiness_level == 2:
                backend_match = min(backend_match, 79.0)
                
            qa_match = (analysis['bug_hunting'] * 0.7) + (analysis['sys_think'] * 0.3)
            if final_10 < 4.0:
                qa_match = min(qa_match, 39.0)
            elif final_10 < 5.5:
                qa_match = min(qa_match, 59.0)
                
            ai_match = (final_10 * 10.0 * 0.5) + (analysis['sys_think'] * 0.5)
            if readiness_level < 2:
                ai_match = min(ai_match, 59.0)
                
            has_git = len(git_link) > 10 and "github.com" in git_link.lower()
            react_score = 100.0 if has_git else 0.0
            fullstack_match = (backend_match * 0.6) + (react_score * 0.4)
            
            # Check for grading mismatches
            is_mismatch = False
            mismatch_reason = ""
            if is_matched:
                diff = abs(th_val - prev_essay_score * 10.0)
                if diff > 1.0:
                    is_mismatch = True
                    if "ai trong quá trình" in combined_text:
                        mismatch_reason = "Bị huỷ điểm do gian lận (sử dụng AI)"
                    elif "t phước" in combined_text:
                        mismatch_reason = "Được cập nhật điểm tự luận (vấn đáp lại/chấm lại)"
                    else:
                        mismatch_reason = "Sai lệch số liệu (chưa rõ nguyên nhân)"
            elif not is_matched and th_val > 0:
                # Student has a practical grade in main sheet but not in grading files
                # Wait, this happens if they took makeup exams or were graded later
                is_mismatch = True
                mismatch_reason = "Có điểm trên Excel chính nhưng không có trong file ca thi cũ (có thể thi bổ sung muộn)"
                
            student_rec = {
                'name': name,
                'class': cname,
                'branch': branch,
                'sp': sp_val,
                'vd': vd_val,
                'th': th_val,
                'tn': tn_val,
                'final': final_val,
                'final_10': round(final_10, 2),
                'ca': ca,
                'note': note,
                'bb': bb,
                'is_matched': is_matched,
                'prev_essay_score': prev_essay_score,
                'is_mismatch': is_mismatch,
                'mismatch_reason': mismatch_reason,
                'bug_hunting': analysis['bug_hunting'],
                'coding': analysis['coding'],
                'system_thinking': analysis['system_thinking'],
                'concurrency': analysis['concurrency'],
                'security': analysis['security'],
                'sys_think': analysis['sys_think'],
                'failed_skills': analysis['failed_skills'],
                'readiness_level': readiness_level,
                'readiness_label': readiness_label,
                'job_matches': {
                    'backend_dev': round(backend_match, 1),
                    'api_qa': round(qa_match, 1),
                    'ai_integration': round(ai_match, 1),
                    'fullstack_dev': round(fullstack_match, 1)
                }
            }
            ks24_students.append(student_rec)
            
        elif "KS25" in cname or "K25" in cname:
            student_rec = {
                'name': name,
                'class': cname,
                'branch': branch,
                'th': th_val,
                'tn': tn_val,
                'final': final_val,
                'final_10': round(final_val / 10.0, 2),
                'ca': ca,
                'note': note,
                'bb': bb
            }
            ks25_students.append(student_rec)
            
    # Process other sheets for system errors
    for sname in ["Danh sách ĐGNL ngoại ngữ", "Danh sách ĐGNL Kỹ năng mềm"]:
        sheet = wb[sname]
        rows = list(sheet.iter_rows(values_only=True))
        headers = rows[0]
        
        name_idx = None; class_idx = None; note_idx = None; bb_idx = None; ca_idx = None
        for idx, h in enumerate(headers):
            h_clean = clean_str(h).lower()
            if 'họ và tên' in h_clean or 'họ tên' in h_clean or h_clean == 'tên sv' or h_clean == 'tên':
                if name_idx is None: name_idx = idx
            if 'mã lớp' in h_clean or h_clean == 'lớp':
                if class_idx is None: class_idx = idx
            if 'ghi chú' in h_clean or 'note' in h_clean:
                if note_idx is None: note_idx = idx
            if 'biên bản' in h_clean or 'kết quả bb' in h_clean:
                if bb_idx is None: bb_idx = idx
            if 'ca thi' in h_clean:
                if ca_idx is None: ca_idx = idx
                
        if name_idx is None: name_idx = 1
        if class_idx is None: class_idx = 7
        if note_idx is None:
            for idx, h in enumerate(headers):
                if 'chú' in clean_str(h).lower(): note_idx = idx
        if bb_idx is None:
            for idx, h in enumerate(headers):
                if 'bản' in clean_str(h).lower(): bb_idx = idx
                
        subj_name = "Ngoại ngữ" if "ngoại ngữ" in sname.lower() else "Kỹ năng mềm"
        
        for r in rows[1:]:
            name = clean_str(r[name_idx])
            cname = clean_str(r[class_idx])
            note = clean_str(r[note_idx]) if note_idx is not None else ""
            bb = clean_str(r[bb_idx]) if bb_idx is not None else ""
            ca = clean_str(r[ca_idx]) if ca_idx is not None else ""
            
            combined_text = (note + " " + bb).lower()
            is_sys_error = False
            for kw in keywords:
                if kw in combined_text:
                    is_sys_error = True
                    break
            if is_sys_error:
                system_errors.append({
                    'name': name,
                    'class': cname,
                    'ca': ca,
                    'note': note,
                    'bb': bb,
                    'subject': subj_name
                })
                
    # Process supplement registrations
    supp_sheet = wb["Thi bổ sung Đợt 1"]
    supp_rows = list(supp_sheet.iter_rows(values_only=True))
    supp_headers = supp_rows[0]
    s_name_idx = supp_headers.index('Họ tên')
    s_class_idx = supp_headers.index('Mã lớp')
    s_mon_idx = supp_headers.index('Môn thi')
    s_cs_idx = supp_headers.index('Cơ sở thi')
    
    supplement_registrations = []
    for r in supp_rows[1:]:
        name = clean_str(r[s_name_idx])
        cname = clean_str(r[s_class_idx])
        mon = clean_str(r[s_mon_idx])
        cs = clean_str(r[s_cs_idx])
        if name:
            supplement_registrations.append({
                'name': name,
                'class': cname,
                'subject': mon,
                'location': cs
            })
            
    # Calculate statistics for KS24 HN vs HCM
    hn_ks24 = [s for s in ks24_students if "HN" in s['branch']]
    hcm_ks24 = [s for s in ks24_students if "HCM" in s['branch']]
    
    def get_stats_dict(students_list):
        total = len(students_list)
        if total == 0: return {}
        
        valid = [s for s in students_list if s['final'] > 0]
        avg_score = sum(s['final'] for s in students_list) / total
        avg_score_valid = sum(s['final'] for s in valid) / len(valid) if valid else 0.0
        
        avg_prac = sum(s['th'] for s in students_list) / total
        avg_mcq = sum(s['tn'] for s in students_list) / total
        avg_oral = sum(s['vd'] for s in students_list) / total
        avg_prod = sum(s['sp'] for s in students_list) / total
        
        levels = {0: 0, 1: 0, 2: 0, 3: 0}
        for s in students_list:
            levels[s['readiness_level']] += 1
            
        placement_rate = (levels[2] + levels[3]) / total * 100.0
        
        # Averages of skill dimensions (only for matching students with skill text)
        matched_students = [s for s in students_list if s['is_matched']]
        m_total = len(matched_students)
        avg_skills = {
            'bug_hunting': sum(s['bug_hunting'] for s in matched_students) / m_total if m_total else 0.0,
            'coding': sum(s['coding'] for s in matched_students) / m_total if m_total else 0.0,
            'system_thinking': sum(s['system_thinking'] for s in matched_students) / m_total if m_total else 0.0,
            'concurrency': sum(s['concurrency'] for s in matched_students) / m_total if m_total else 0.0,
            'security': sum(s['security'] for s in matched_students) / m_total if m_total else 0.0,
            'sys_think': sum(s['sys_think'] for s in matched_students) / m_total if m_total else 0.0,
        }
        
        return {
            'total_registered': total,
            'total_took_exam': len(valid),
            'avg_score': round(avg_score, 2),
            'avg_score_valid': round(avg_score_valid, 2),
            'avg_prac': round(avg_prac, 2),
            'avg_mcq': round(avg_mcq, 2),
            'avg_oral': round(avg_oral, 2),
            'avg_prod': round(avg_prod, 2),
            'placement_rate': round(placement_rate, 2),
            'levels': levels,
            'avg_skills': {k: round(v, 2) for k, v in avg_skills.items()}
        }
        
    hn_stats = get_stats_dict(hn_ks24)
    hcm_stats = get_stats_dict(hcm_ks24)
    all_ks24_stats = get_stats_dict(ks24_students)
    
    output_data = {
        'ks24_stats': {
            'all': all_ks24_stats,
            'hn': hn_stats,
            'hcm': hcm_stats
        },
        'ks24_students': ks24_students,
        'ks25_students_count': len(ks25_students),
        'system_errors': system_errors,
        'supplement_registrations': supplement_registrations
    }
    
    # Save to JSON
    os.makedirs("scratch", exist_ok=True)
    with open("scratch/optimized_dgnl_data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print("\nAnalysis Data saved to scratch/optimized_dgnl_data.json successfully!")
    print(f"Total KS24 students processed: {len(ks24_students)}")
    print(f"  HN: {len(hn_ks24)} | HCM: {len(hcm_ks24)}")
    print(f"  HN Avg Score: {hn_stats['avg_score']} | HCM Avg Score: {hcm_stats['avg_score']}")
    print(f"  HN Placement Rate: {hn_stats['placement_rate']}% | HCM Placement Rate: {hcm_stats['placement_rate']}%")
    print(f"Total System Errors scanned: {len(system_errors)}")
    print(f"Total Supplement Registrations: {len(supplement_registrations)}")

if __name__ == "__main__":
    main()

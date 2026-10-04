import openpyxl
import json
import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

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
    
    # Criteria stats
    c1_total = 0
    c1_pass = 0
    c2_total = 0
    c2_pass = 0
    c3_total = 0
    c3_pass = 0
    
    # Skill stats
    ct_total = 0
    ct_pass = 0
    sa_total = 0
    sa_pass = 0
    st_total = 0
    st_pass = 0
    
    # Keywords
    ct_keywords = ['transaction', 'đồng thời', '@transactional', 'giao dịch', 'đồng bộ', 'race condition', 'lock', 'khóa', 'trùng ghế', 'bán vượt']
    sa_keywords = ['path traversal', 'idor', 'client', 'ủy quyền', 'xác thực', 'security', 'bảo mật', 'quyền truy cập', 'giá vé', 'unitprice', 'ticketprice', 'giá sản phẩm', 'đường dẫn']
    st_keywords = ['câu 3', 'câu hỏi định hướng', 'lựa chọn', 'ưu tiên', 'suất chiếu hot', 'khung giờ', 'bấm nút', 'chuyển tiền']
    
    failed_skills = []
    
    for line in lines:
        line_clean = line.strip().lower()
        if not line_clean:
            continue
            
        # Determine status
        is_pass = False
        if '— đạt' in line_clean or '– đạt' in line_clean or ': đạt' in line_clean or '— pass' in line_clean or 'đạt:' in line_clean:
            is_pass = True
        elif '— không đạt' in line_clean or '– không đạt' in line_clean or ': không đạt' in line_clean or '— fail' in line_clean:
            is_pass = False
        else:
            if 'đạt' in line and 'không đạt' not in line:
                is_pass = True
                
        # Determine Question Category
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
            
        # Determine Skill Category
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
                
    # Calculate percentages
    bh_score = (c1_pass / c1_total * 100.0) if c1_total > 0 else 0.0
    cr_score = (c2_pass / c2_total * 100.0) if c2_total > 0 else 0.0
    st_score = (c3_pass / c3_total * 100.0) if c3_total > 0 else 0.0
    
    # Fallback to general question scores if no specific skill keywords found
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

def main():
    files = [
        "inputs/ket-qua-cham-DGNL-ca-thi-7-9.xlsx",
        "inputs/ket-qua-cham-DGNL-ca-thi-12-14.xlsx",
        "inputs/ket-qua-cham-DGNL-ca-thi-14-16.xlsx"
    ]
    
    students_data = []
    
    for path in files:
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue
            
        wb = openpyxl.load_workbook(path, data_only=True)
        sheet = wb.active
        rows = list(sheet.iter_rows(values_only=True))
        headers = rows[0]
        
        name_idx = headers.index('Name')
        score_idx = headers.index('Điểm')
        topic_idx = headers.index('Đề bài')
        crit_idx = headers.index('Chi tiết tiêu chí')
        git_idx = headers.index('Link Git')
        
        ca_thi = os.path.basename(path).replace("ket-qua-cham-DGNL-ca-", "").replace(".xlsx", "")
        
        for r in rows[1:]:
            if r[0] is None or r[name_idx] is None:
                continue
                
            name = str(r[name_idx]).strip()
            raw_score = r[score_idx]
            score_val = parse_score(raw_score)
            topic = str(r[topic_idx] or "Câu hỏi tự luận").strip()
            criteria_text = r[crit_idx]
            git_link = str(r[git_idx] or "").strip()
            
            # Analyze criteria
            analysis = analyze_student_criteria(criteria_text)
            
            # Readiness Levels (Mức 0 to Mức 3)
            # Level 3: Score >= 8.0, and Concurrency >= 75%, and Security >= 75%
            # Level 2: Score >= 6.0, and Concurrency >= 50%, and Security >= 50%
            # Level 1: Score >= 4.0
            # Level 0: Score < 4.0
            
            if score_val >= 8.0 and analysis['concurrency'] >= 75.0 and analysis['security'] >= 75.0:
                readiness_level = 3
                readiness_label = "Mức 3: Fresher Sẵn Sàng (Direct Production-Ready)"
            elif score_val >= 6.0 and analysis['concurrency'] >= 50.0 and analysis['security'] >= 50.0:
                readiness_level = 2
                readiness_label = "Mức 2: Thử việc / Intern tiềm năng cao (High-Potential)"
            elif score_val >= 4.0:
                readiness_level = 1
                readiness_label = "Mức 1: Intern cần kèm cặp sát sao (Standard Intern)"
            else:
                readiness_level = 0
                readiness_label = "Mức 0: Chưa sẵn sàng (Retraining Required)"
                
            # Job Match Rates
            # 1. Java Backend Developer
            backend_match = (analysis['concurrency'] * 0.4) + (analysis['security'] * 0.4) + (analysis['sys_think'] * 0.2)
            # Limit maximum match based on readiness level
            if readiness_level == 0:
                backend_match = min(backend_match, 39.0)
            elif readiness_level == 1:
                backend_match = min(backend_match, 59.0)
            elif readiness_level == 2:
                backend_match = min(backend_match, 79.0)
                
            # 2. API QA / Tester
            # Tester relies heavily on Bug Hunting (BH)
            qa_match = (analysis['bug_hunting'] * 0.7) + (analysis['sys_think'] * 0.3)
            if score_val < 4.0:
                qa_match = min(qa_match, 39.0)
            elif score_val < 5.5:
                qa_match = min(qa_match, 59.0)
                
            # 3. AI Integration Engineer
            # Relies on Overall score and System thinking
            ai_match = (score_val * 10.0 * 0.5) + (analysis['sys_think'] * 0.5)
            if readiness_level < 2:
                ai_match = min(ai_match, 59.0)
                
            # 4. Enterprise Fullstack Dev (Java + React)
            # If Git link is present, assume React capability = 100%, else 0%
            has_git = len(git_link) > 10 and "github.com" in git_link.lower()
            react_score = 100.0 if has_git else 0.0
            fullstack_match = (backend_match * 0.6) + (react_score * 0.4)
            
            student_record = {
                'name': name,
                'score': score_val,
                'topic': topic,
                'ca_thi': ca_thi,
                'git_link': git_link,
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
            students_data.append(student_record)
            
    # Calculate aggregate stats
    total_students = len(students_data)
    avg_score = sum(s['score'] for s in students_data) / total_students
    
    level_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    for s in students_data:
        level_counts[s['readiness_level']] += 1
        
    avg_skills = {
        'bug_hunting': sum(s['bug_hunting'] for s in students_data) / total_students,
        'coding': sum(s['coding'] for s in students_data) / total_students,
        'system_thinking': sum(s['system_thinking'] for s in students_data) / total_students,
        'concurrency': sum(s['concurrency'] for s in students_data) / total_students,
        'security': sum(s['security'] for s in students_data) / total_students,
        'sys_think': sum(s['sys_think'] for s in students_data) / total_students
    }
    
    avg_job_matches = {
        'backend_dev': sum(s['job_matches']['backend_dev'] for s in students_data) / total_students,
        'api_qa': sum(s['job_matches']['api_qa'] for s in students_data) / total_students,
        'ai_integration': sum(s['job_matches']['ai_integration'] for s in students_data) / total_students,
        'fullstack_dev': sum(s['job_matches']['fullstack_dev'] for s in students_data) / total_students
    }
    
    # Placement rate (Ready for enterprise placement = Level 2 or 3)
    ready_count = level_counts[2] + level_counts[3]
    placement_rate = ready_count / total_students * 100.0
    
    stats = {
        'summary': {
            'total_students': total_students,
            'avg_score': round(avg_score, 2),
            'placement_rate': round(placement_rate, 2),
            'level_counts': {
                'level_0': level_counts[0],
                'level_1': level_counts[1],
                'level_2': level_counts[2],
                'level_3': level_counts[3]
            },
            'avg_skills': {k: round(v, 2) for k, v in avg_skills.items()},
            'avg_job_matches': {k: round(v, 2) for k, v in avg_job_matches.items()}
        },
        'students': students_data
    }
    
    # Save to scratch
    os.makedirs("scratch", exist_ok=True)
    with open("scratch/ks24_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
        
    print(f"Data processing complete!")
    print(f"Parsed {total_students} students.")
    print(f"Average score: {avg_score:.2f}")
    print(f"Readiness Levels distribution:")
    print(f"  Level 3 (Fresher Sẵn Sàng): {level_counts[3]} students ({level_counts[3]/total_students*100:.2f}%)")
    print(f"  Level 2 (Thử việc/Intern tốt): {level_counts[2]} students ({level_counts[2]/total_students*100:.2f}%)")
    print(f"  Level 1 (Intern cần kèm cặp): {level_counts[1]} students ({level_counts[1]/total_students*100:.2f}%)")
    print(f"  Level 0 (Chưa đạt): {level_counts[0]} students ({level_counts[0]/total_students*100:.2f}%)")
    print(f"Ready for placement rate (Level 2 + 3): {placement_rate:.2f}%")

if __name__ == "__main__":
    main()

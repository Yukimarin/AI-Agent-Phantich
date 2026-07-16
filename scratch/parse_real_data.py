import os
import re
import json

def parse_kpi_report():
    kpi_list = []
    filepath = "data/report_kpi_gv_tg.md"
    if not os.path.exists(filepath):
        return kpi_list
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    lines = content.split("\n")
    table_started = False
    
    for line in lines:
        if "| Họ và tên |" in line:
            table_started = True
            continue
        if table_started:
            if not line.strip() or not line.startswith("|"):
                if kpi_list:
                    table_started = False
                continue
            if "---" in line:
                continue
            
            # Thay thế các link Obsidian có dạng [[link|text]] thành text trước để tránh split sai
            line_clean = re.sub(r"\[\[[^\]]*?\|(.*?)\]\]", r"\1", line)
            parts = [p.strip() for p in line_clean.split("|")[1:-1]]
            if len(parts) >= 7:
                name = parts[0].replace("**", "")
                role = parts[1]
                classes = parts[2]
                score_discipline = float(parts[3])
                score_academic = float(parts[4])
                score_logs = float(parts[5])
                score_total = float(parts[6].replace("**", ""))
                
                kpi_list.append({
                    "name": name,
                    "role": role,
                    "classes": classes,
                    "score_discipline": score_discipline,
                    "score_academic": score_academic,
                    "score_logs": score_logs,
                    "score_total": score_total
                })
    return kpi_list

def parse_student_violations():
    # Parse các bảng lớp học trong output/1_kpi_report.html
    filepath = "output/1_kpi_report.html"
    classes_data = []
    if not os.path.exists(filepath):
        return classes_data
        
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Tìm các bảng HTML
    tables = re.findall(r"<table.*?>(.*?)</table>", html, re.DOTALL)
    # 4 bảng đầu là danh sách lớp học
    for table_idx in range(min(4, len(tables))):
        table_content = tables[table_idx]
        rows = re.findall(r"<tr.*?>(.*?)</tr>", table_content, re.DOTALL)
        for row in rows[1:]: # Bỏ qua header
            cols = re.findall(r"<td.*?>(.*?)</td>", row, re.DOTALL)
            if len(cols) >= 6:
                # Clean html tags
                class_name = re.sub(r"<.*?>", "", cols[0]).strip()
                gv = re.sub(r"<.*?>", "", cols[1]).strip()
                tg = re.sub(r"<.*?>", "", cols[2]).strip()
                cc = re.sub(r"<.*?>", "", cols[3]).strip()
                bt = re.sub(r"<.*?>", "", cols[4]).strip()
                el = re.sub(r"<.*?>", "", cols[5]).strip()
                # Điểm kỷ luật lớp học (cột 7 nếu có, hoặc tính toán)
                score = re.sub(r"<.*?>", "", cols[6]).strip() if len(cols) > 6 else "90"
                
                classes_data.append({
                    "class": class_name,
                    "gv": gv,
                    "tg": tg,
                    "cc": cc,
                    "bt": bt,
                    "el": el,
                    "score": score
                })
    return classes_data

def parse_student_risks():
    filepath = "output/2_student_risk_dashboard.html"
    risks = []
    if not os.path.exists(filepath):
        return risks
        
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Tìm bảng học viên nguy cơ
    rows = re.findall(r"<tr.*?>(.*?)</tr>", html, re.DOTALL)
    for row in rows:
        cols = re.findall(r"<td.*?>(.*?)</td>", row, re.DOTALL)
        if len(cols) >= 6:
            name = re.sub(r"<.*?>", "", cols[1]).strip()
            class_name = re.sub(r"<.*?>", "", cols[2]).strip()
            risk_level = re.sub(r"<.*?>", "", cols[3]).strip()
            reason = re.sub(r"<.*?>", "", cols[4]).strip()
            action = re.sub(r"<.*?>", "", cols[5]).strip()
            
            # Tránh lấy header
            if name == "Họ và Tên" or not name:
                continue
                
            risks.append({
                "name": name,
                "class": class_name,
                "risk_level": risk_level,
                "reason": reason,
                "action": action
            })
    return risks

def parse_gvtg_violations():
    filepath = "output/3_gvtg_violations_report.html"
    violations = []
    if not os.path.exists(filepath):
        return violations
        
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
        
    rows = re.findall(r"<tr.*?>(.*?)</tr>", html, re.DOTALL)
    for row in rows:
        cols = re.findall(r"<td.*?>(.*?)</td>", row, re.DOTALL)
        if len(cols) >= 5:
            date = re.sub(r"<.*?>", "", cols[0]).strip()
            name = re.sub(r"<.*?>", "", cols[1]).strip()
            role = re.sub(r"<.*?>", "", cols[2]).strip()
            violation_type = re.sub(r"<.*?>", "", cols[3]).strip()
            penalty = re.sub(r"<.*?>", "", cols[4]).strip()
            
            if name == "Họ và Tên" or not name:
                continue
                
            violations.append({
                "date": date,
                "name": name,
                "role": role,
                "type": violation_type,
                "penalty": penalty
            })
    return violations

def main():
    kpis = parse_kpi_report()
    student_viols = parse_student_violations()
    risks = parse_student_risks()
    gvtg_viols = parse_gvtg_violations()
    
    print(f"Parsed {len(kpis)} GV/TG KPI metrics.")
    print(f"Parsed {len(student_viols)} student classroom violation metrics.")
    print(f"Parsed {len(risks)} high risk students.")
    print(f"Parsed {len(gvtg_viols)} GV/TG compliance violations.")

if __name__ == "__main__":
    main()

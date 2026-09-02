import sys
import pandas as pd
import json
import re

sys.stdout.reconfigure(encoding="utf-8")

excel_path = "inputs/Danh sách thi ĐGNL.xlsx"
df_bd = pd.read_excel(excel_path, sheet_name="Bảng điểm (Đợt 1)")

def clean_str(val):
    if val is None: return ""
    return str(val).strip()

def clean_name(name):
    if name is None: return ""
    name = str(name).strip()
    name = re.sub(r"\s+\d+$", "", name)
    return name.lower()

# KS24 Classification
ks24 = df_bd[df_bd["Mã lớp hiện tại"].astype(str).str.contains("KS24-CNTT", na=False)].copy()
for c in ["Đ1_Sản phẩm_CNTT", "Đ1_Vấn đáp_CNTT", "Đ1_Thực hành_CNTT", "Đ1_Trắc nghiệm_CNTT", "Đ1_Điểm CNTT (Final)", "Đ1_Tiếng Anh (Final)", "Đ1_Kỹ năng mềm (Final)"]:
    ks24[c] = pd.to_numeric(ks24[c], errors="coerce")

ks24_records = []
for _, r in ks24.iterrows():
    name = clean_str(r["Họ và tên học viên"])
    cname = clean_str(r["Mã lớp hiện tại"])
    sp = r["Đ1_Sản phẩm_CNTT"] if pd.notna(r["Đ1_Sản phẩm_CNTT"]) else None
    vd = r["Đ1_Vấn đáp_CNTT"] if pd.notna(r["Đ1_Vấn đáp_CNTT"]) else None
    th = r["Đ1_Thực hành_CNTT"] if pd.notna(r["Đ1_Thực hành_CNTT"]) else None
    tn = r["Đ1_Trắc nghiệm_CNTT"] if pd.notna(r["Đ1_Trắc nghiệm_CNTT"]) else None
    knm = r["Đ1_Kỹ năng mềm (Final)"] if pd.notna(r["Đ1_Kỹ năng mềm (Final)"]) else None
    ta = r["Đ1_Tiếng Anh (Final)"] if pd.notna(r["Đ1_Tiếng Anh (Final)"]) else None
    
    # tech score = max(th, sp)
    valid_tech = [v for v in [th, sp] if v is not None]
    tech_score = max(valid_tech) if valid_tech else 0
    oral_score = vd if vd is not None else 0
    soft_score = knm if knm is not None else 0
    
    is_absent = (th is None or th == 0) and (vd is None or vd == 0) and (sp is None or sp == 0) and (tn is None or tn == 0)
    
    if is_absent:
        persona = "Vắng thi / Chưa có dữ liệu"
        action = "Xác minh lý do vắng và tổ chức thi bổ sung"
        badge_cls = "badge-muted"
    elif tech_score >= 65 and oral_score < 50:
        persona = "Silent Coder (Code giỏi, Vấn đáp yếu)"
        action = "Bắt buộc tham gia Mock Interview Lab 1-1"
        badge_cls = "badge-danger"
    elif tech_score < 50 and (oral_score >= 50 or soft_score >= 75):
        persona = "Career Shifter (Giao tiếp tốt, Code yếu - Hướng BA/QA)"
        action = "Tư vấn chuyển luồng IT Business Analyst / Software Tester"
        badge_cls = "badge-warning"
    elif tech_score >= 65 and oral_score >= 50:
        persona = "All-Rounder (Toàn diện Đạt chuẩn Doanh nghiệp)"
        action = "Đưa vào luồng phỏng vấn doanh nghiệp đối tác & Dự án Onsite"
        badge_cls = "badge-success"
    elif tech_score < 50 and oral_score < 50 and soft_score < 70:
        persona = "At-Risk (Yếu cả Kỹ thuật lẫn Giao tiếp)"
        action = "Phụ đạo Java Core & Spring Boot Bootcamp bắt buộc"
        badge_cls = "badge-danger"
    else:
        persona = "Trung gian (Đạt mức cơ bản 50-64đ)"
        action = "Củng cố thêm kỹ năng giao dịch đồng thời & bảo mật API"
        badge_cls = "badge-info"
        
    ks24_records.append({
        "name": name, "class": cname, "sp": sp, "vd": vd, "th": th, "tn": tn,
        "knm": knm, "ta": ta, "persona": persona, "action": action, "badge_cls": badge_cls
    })

print(f"KS24 records classified: {len(ks24_records)}")
df_ks24_diag = pd.DataFrame(ks24_records)
print(df_ks24_diag["persona"].value_counts())

# Save diagnostic data
with open("scratch/ks24_diagnosis.json", "w", encoding="utf-8") as f:
    json.dump(ks24_records, f, ensure_ascii=False, indent=2)

# KS25 Classification
ks25 = df_bd[df_bd["Mã lớp hiện tại"].astype(str).str.contains("KS25-CNTT", na=False)].copy()
for c in ["Đ1_Thực hành_CNTT", "Đ1_Trắc nghiệm_CNTT", "Đ1_Điểm CNTT (Final)", "Đ1_Tiếng Anh (Final)", "Đ1_Kỹ năng mềm (Final)"]:
    ks25[c] = pd.to_numeric(ks25[c], errors="coerce")

ks25_records = []
for _, r in ks25.iterrows():
    name = clean_str(r["Họ và tên học viên"])
    cname = clean_str(r["Mã lớp hiện tại"])
    th = r["Đ1_Thực hành_CNTT"] if pd.notna(r["Đ1_Thực hành_CNTT"]) else None
    tn = r["Đ1_Trắc nghiệm_CNTT"] if pd.notna(r["Đ1_Trắc nghiệm_CNTT"]) else None
    knm = r["Đ1_Kỹ năng mềm (Final)"] if pd.notna(r["Đ1_Kỹ năng mềm (Final)"]) else None
    ta = r["Đ1_Tiếng Anh (Final)"] if pd.notna(r["Đ1_Tiếng Anh (Final)"]) else None
    
    th_score = th if th is not None else 0
    tn_score = tn if tn is not None else 0
    soft_score = knm if knm is not None else 0
    
    is_absent = (th is None or th == 0) and (tn is None or tn == 0)
    
    if is_absent:
        persona = "Vắng thi / Chưa có dữ liệu"
        action = "Xếp vào nhóm cần phụ đạo và xác minh lý do vắng"
        badge_cls = "badge-muted"
    elif th_score >= 50:
        persona = "Solid Coder (Vững Thực hành Code)"
        action = "Tiếp tục lộ trình nâng cao (DSA, Machine Learning, RAG/LLM)"
        badge_cls = "badge-success"
    elif tn_score >= 65 and th_score < 50:
        persona = "Ảo tưởng Lý thuyết (Trắc nghiệm giỏi, Thực hành liệt)"
        action = "Bắt buộc tham gia FastAPI Live-Coding Bootcamp 2 tuần"
        badge_cls = "badge-danger"
    elif soft_score >= 75 and th_score < 50:
        persona = "Tiềm năng BA/QA (Giao tiếp tốt, Hổng code)"
        action = "Định hướng phân luồng môn BA/QA từ đầu Kỳ III"
        badge_cls = "badge-warning"
    elif tn_score < 50 and th_score < 50:
        persona = "Mất căn bản (Yếu cả Lý thuyết lẫn Code)"
        action = "Phụ đạo lại kiến thức lập trình Python Core căn bản"
        badge_cls = "badge-danger"
    else:
        persona = "Cơ bản (Cần tăng cường thực hành)"
        action = "Luyện tập code API theo boilerplate skeleton"
        badge_cls = "badge-info"
        
    ks25_records.append({
        "name": name, "class": cname, "th": th, "tn": tn, "knm": knm, "ta": ta,
        "persona": persona, "action": action, "badge_cls": badge_cls
    })

print(f"\nKS25 records classified: {len(ks25_records)}")
df_ks25_diag = pd.DataFrame(ks25_records)
print(df_ks25_diag["persona"].value_counts())

with open("scratch/ks25_diagnosis.json", "w", encoding="utf-8") as f:
    json.dump(ks25_records, f, ensure_ascii=False, indent=2)


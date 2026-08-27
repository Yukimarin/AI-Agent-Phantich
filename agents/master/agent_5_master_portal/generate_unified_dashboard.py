import os
import sys
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def format_title_name(name):
    if not name:
        return "—"
    words = name.strip().split()
    return " ".join([w.capitalize() for w in words])

def build_executive_dataset():
    cache_path = "data/processed/classes_metrics_cache.json"
    a1_path = "data/processed/agent1_output.json"
    a2_path = "data/processed/agent2_output.json"
    a3_path = "data/processed/agent3_output.json"
    a4_path = "data/processed/daily_log_analysis.json"
    
    cache_data = json.load(open(cache_path, "r", encoding="utf-8")) if os.path.exists(cache_path) else {}
    a1_data = json.load(open(a1_path, "r", encoding="utf-8")) if os.path.exists(a1_path) else {}
    a2_data = json.load(open(a2_path, "r", encoding="utf-8")) if os.path.exists(a2_path) else {}
    a3_data = json.load(open(a3_path, "r", encoding="utf-8")) if os.path.exists(a3_path) else []
    a4_data = json.load(open(a4_path, "r", encoding="utf-8")) if os.path.exists(a4_path) else {}
    
    classes_dict = cache_data.get("classes", {})
    instructors_a1 = a1_data.get("instructors", {})
    care_list = a2_data.get("care_list", [])
    dashboard_a2 = a2_data.get("dashboard_data", {})
    weekly_stats_a4 = a4_data.get("weekly_stats", {})

    staff_violations_map = {}
    for v in a3_data:
        inst = v.get("Instructor")
        if inst:
            name_key = inst.strip().lower()
            if name_key not in staff_violations_map:
                staff_violations_map[name_key] = []
            staff_violations_map[name_key].append(v)

    active_classes_config = [
        {"name": "HN-K24-CNTT1", "group_title": "Khối KS24 CNTT (Kỳ IV — AI Integration)", "batch": "KS24", "dept": "Khối CNTT", "campus": "HN", "subject": "KS24_AI_Intergration", "gv": "Nguyễn Công Hưởng", "tg": "Phạm Tuấn Bình"},
        {"name": "HN-K24-CNTT2", "group_title": "Khối KS24 CNTT (Kỳ IV — AI Integration)", "batch": "KS24", "dept": "Khối CNTT", "campus": "HN", "subject": "KS24_AI_Intergration", "gv": "Bùi Thanh Hải", "tg": "Đinh Thành Nam"},
        {"name": "HN-K24-CNTT3", "group_title": "Khối KS24 CNTT (Kỳ IV — AI Integration)", "batch": "KS24", "dept": "Khối CNTT", "campus": "HN", "subject": "KS24_AI_Intergration", "gv": "Bùi Thanh Hải", "tg": "Phạm Tuấn Bình"},
        {"name": "HN-K24-CNTT4", "group_title": "Khối KS24 CNTT (Kỳ IV — AI Integration)", "batch": "KS24", "dept": "Khối CNTT", "campus": "HN", "subject": "KS24_AI_Intergration", "gv": "Bùi Thanh Hải", "tg": "Đinh Thành Nam"},
        {"name": "HCM-K24-CNTT1", "group_title": "Khối KS24 CNTT (Kỳ IV — AI Integration)", "batch": "KS24", "dept": "Khối CNTT", "campus": "HCM", "subject": "KS24_AI_Intergration", "gv": "Nguyễn Bá Minh Đạo", "tg": "Phan Ngọc Tài"},
        
        {"name": "HN-K25-CNTT1", "group_title": "Khối KS25 CNTT — Cơ sở Hà Nội (Kỳ II — Python Web)", "batch": "KS25", "dept": "Khối CNTT", "campus": "HN", "subject": "KS25_Python_Web", "gv": "Lương Quốc Tuấn", "tg": "Lại Trung Lâm"},
        {"name": "HN-K25-CNTT2", "group_title": "Khối KS25 CNTT — Cơ sở Hà Nội (Kỳ II — Python Web)", "batch": "KS25", "dept": "Khối CNTT", "campus": "HN", "subject": "KS25_Python_Web", "gv": "Lâm Tùng Dương", "tg": "Lại Trung Lâm"},
        {"name": "HN-K25-CNTT3", "group_title": "Khối KS25 CNTT — Cơ sở Hà Nội (Kỳ II — Python Web)", "batch": "KS25", "dept": "Khối CNTT", "campus": "HN", "subject": "KS25_Python_Web", "gv": "Nguyễn Quảng An", "tg": "Phạm Ngọc Kiên"},
        {"name": "HN-K25-CNTT4", "group_title": "Khối KS25 CNTT — Cơ sở Hà Nội (Kỳ II — Python Web)", "batch": "KS25", "dept": "Khối CNTT", "campus": "HN", "subject": "KS25_Python_Web", "gv": "Nguyễn Quảng An", "tg": "Phạm Ngọc Kiên"},
        {"name": "HN-K25-CNTT5", "group_title": "Khối KS25 CNTT — Cơ sở Hà Nội (Kỳ II — Python Web)", "batch": "KS25", "dept": "Khối CNTT", "campus": "HN", "subject": "KS25_Python_Web", "gv": "Lương Quốc Tuấn", "tg": "Lại Trung Lâm"},
        {"name": "HN-K25-CNTT6", "group_title": "Khối KS25 CNTT — Cơ sở Hà Nội (Kỳ II — Python Web)", "batch": "KS25", "dept": "Khối CNTT", "campus": "HN", "subject": "KS25_Python_Web", "gv": "Nguyễn Quảng An", "tg": "Phạm Ngọc Kiên"},
        {"name": "HN-K25-CNTT8", "group_title": "Khối KS25 CNTT — Cơ sở Hà Nội (Kỳ II — Python Web)", "batch": "KS25", "dept": "Khối CNTT", "campus": "HN", "subject": "KS25_Python_Web", "gv": "Trịnh Quốc Hai", "tg": "Đặng Minh Luân"},
        
        {"name": "HCM-K25-CNTT5", "group_title": "Khối KS25 CNTT — Cơ sở TP. HCM (Kỳ II — Python Web)", "batch": "KS25", "dept": "Khối CNTT", "campus": "HCM", "subject": "KS25_Python_Web", "gv": "Lê Hà Thanh Sang", "tg": "Lưu Hoàng Xuân Nguyên"},
        {"name": "HCM-K25-CNTT6", "group_title": "Khối KS25 CNTT — Cơ sở TP. HCM (Kỳ II — Python Web)", "batch": "KS25", "dept": "Khối CNTT", "campus": "HCM", "subject": "KS25_Python_Web", "gv": "Trần Quốc Tuấn", "tg": "Lưu Hoàng Xuân Nguyên"},
        {"name": "HCM-K25-CNTT7", "group_title": "Khối KS25 CNTT — Cơ sở TP. HCM (Kỳ II — Python Web)", "batch": "KS25", "dept": "Khối CNTT", "campus": "HCM", "subject": "KS25_Python_Web", "gv": "Trần Quốc Tuấn", "tg": "Lưu Hoàng Xuân Nguyên"},
        {"name": "HCM-K25-CNTT8", "group_title": "Khối KS25 CNTT — Cơ sở TP. HCM (Kỳ II — Python Web)", "batch": "KS25", "dept": "Khối CNTT", "campus": "HCM", "subject": "KS25_Python_Web", "gv": "Lê Hà Thanh Sang", "tg": "Phan Ngọc Tài"},
        
        {"name": "HN-K25-QTKD1", "group_title": "Khối KS25 QTKD (Kỳ II — Business Analysis)", "batch": "KS25", "dept": "Khối QTKD", "campus": "HN", "subject": "KS25_QTKD_BA201", "gv": "Nguyễn Thị Hồng Minh", "tg": "Đặng Quỳnh Trang"},
        {"name": "HN-K25-QTKD2", "group_title": "Khối KS25 QTKD (Kỳ II — Business Analysis)", "batch": "KS25", "dept": "Khối QTKD", "campus": "HN", "subject": "KS25_QTKD_BA201", "gv": "Nguyễn Ngọc Vân Khanh", "tg": "Lê Thành Ngọc"},
        {"name": "HN-K25-QTKD3", "group_title": "Khối KS25 QTKD (Kỳ II — Business Analysis)", "batch": "KS25", "dept": "Khối QTKD", "campus": "HN", "subject": "KS25_QTKD_BA201", "gv": "Nguyễn Ngọc Vân Khanh", "tg": "Hoàng Thị Hậu"}
    ]

    classes_list = []
    for cfg in active_classes_config:
        cname = cfg["name"]
        subj = cfg["subject"]
        gv_name = format_title_name(cfg["gv"])
        tg_name = format_title_name(cfg["tg"])
        
        c_raw = classes_dict.get(cname, {})
        sheets = c_raw.get("sheets", {})
        subj_data = sheets.get(subj, {})
        metrics = subj_data.get("metrics", {})
        
        latest_date = "2026-08-26"
        best_m = {}
        if metrics:
            latest_date = list(metrics.keys())[-1]
            best_m = metrics[latest_date]

        cc = best_m.get("cc", 0.0)
        bt = best_m.get("bt", 0.0)
        el = best_m.get("el", 0.0)
        v_class = round((cc + bt + el) / 3.0, 1)

        pred_pass = 75.0
        class_size = c_raw.get("size", 35)
        for batch_key in ['KS24', 'KS25', 'QTKD']:
            if batch_key in dashboard_a2 and 'curr' in dashboard_a2[batch_key]:
                for c in dashboard_a2[batch_key]['curr']:
                    c_cand = c.get('class_name', '')
                    if cname.replace('K', 'KS') in c_cand or c_cand.replace('KS', 'K') in cname:
                        pred_pass = c.get('pred_new', c.get('pred_old', 75.0))
                        class_size = c.get('size', class_size)
                        break

        c_care_list = []
        for s in care_list:
            s_class = s.get('class_name', '')
            if cname.replace('K', 'KS') in s_class or cname in s_class:
                c_care_list.append(s)

        paradox_count = len([s for s in c_care_list if s.get('is_excellent') and s.get('is_failed_new')])
        red_sv_count = len([s for s in c_care_list if s.get('risk_level') == 'RED'])
        banned_sv_count = len([s for s in c_care_list if s.get('is_failed_new')])

        if pred_pass < 60.0 or v_class > 20.0 or red_sv_count >= 10:
            health = "RED"
            status_text = "🔴 Báo động Đỏ"
            action_takeaway = f"TG {tg_name} tổ chức phụ đạo gấp; GV {gv_name} tăng cường kiểm tra code thực chiến"
        elif pred_pass < 80.0 or v_class > 10.0 or len(c_care_list) >= 5:
            health = "YELLOW"
            status_text = "🟡 Cần theo dõi"
            action_takeaway = f"Theo dõi sát {len(c_care_list)} sinh viên Care List, đôn đốc nộp bài tập"
        else:
            health = "GREEN"
            status_text = "🟢 Ổn định"
            action_takeaway = "Duy trì chất lượng giảng dạy và kiểm soát nề nếp chuyên cần"

        care_items = []
        for s in c_care_list[:25]:
            midterm_val = s.get("midterm_score") or s.get("hack") or 0.0
            att_val = s.get("att") or 0.0
            hw_val = s.get("hw") if s.get("hw") is not None else 100.0

            care_items.append({
                "student_id": s.get("student_id", ""),
                "full_name": format_title_name(s.get("full_name", "")),
                "risk_level": s.get("risk_level", "YELLOW"),
                "gpa": round(float(midterm_val), 1),
                "att": round(float(att_val), 1),
                "hw": round(float(hw_val), 1),
                "is_excellent": s.get("is_excellent", False),
                "is_failed_new": s.get("is_failed_new", False)
            })

        classes_list.append({
            "class_name": cname,
            "group_title": cfg["group_title"],
            "subject": subj,
            "batch": cfg["batch"],
            "campus": cfg["campus"],
            "dept": cfg["dept"],
            "size": class_size,
            "latest_date": latest_date,
            "cc": round(cc, 1),
            "bt": round(bt, 1),
            "el": round(el, 1),
            "v_class": v_class,
            "discipline_score": round(100.0 - v_class, 1),
            "pred_pass": round(pred_pass, 1),
            "gv": gv_name,
            "tg": tg_name,
            "care_count": len(c_care_list),
            "paradox_count": paradox_count,
            "red_sv_count": red_sv_count,
            "banned_sv_count": banned_sv_count,
            "health": health,
            "status_text": status_text,
            "action_takeaway": action_takeaway,
            "care_list": care_items
        })

    teaching_staff_names = set()
    for c in classes_list:
        if c["gv"] and c["gv"] != "—": teaching_staff_names.add(c["gv"].lower().strip())
        if c["tg"] and c["tg"] != "—": teaching_staff_names.add(c["tg"].lower().strip())

    staff_meta = {}
    rank_file_path = "data/inputs/staff_roles_ranks.md"
    if os.path.exists(rank_file_path):
        with open(rank_file_path, "r", encoding="utf-8") as f:
            current_dept = "Khối CNTT"
            for line in f:
                if line.startswith("## Khối"):
                    current_dept = line.replace("##", "").strip()
                elif "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 2:
                        raw_name = parts[0].replace("-", "").strip()
                        role = parts[1]
                        rank_val = parts[2].replace("Rank:", "").strip() if len(parts) > 2 else "N/A"
                        staff_meta[raw_name.lower()] = {
                            "name": format_title_name(raw_name),
                            "role": role,
                            "rank": rank_val,
                            "dept": current_dept
                        }

    teaching_staff_list = []
    support_staff_list = []
    hcm_staff = ["đặng minh luân", "lê hà thanh sang", "lưu hoàng xuân nguyên", "lưu xuân hoàng nguyên", "phan ngọc tài", "trần quốc tuấn", "lê nhựt mi", "lê thị bảo yến", "nguyễn ngọc vân khanh"]

    for name_raw, stats in weekly_stats_a4.items():
        name_clean = name_raw.lower().strip()
        meta = staff_meta.get(name_clean, {})
        display_name = format_title_name(meta.get("name", name_raw))
        dept = meta.get("dept", "Khối CNTT")
        role = meta.get("role", stats.get("role", "Giảng viên"))
        rank = meta.get("rank", stats.get("rank", "R3"))
        campus = "HCM" if any(h in name_clean for h in hcm_staff) else "HN"

        rep_days = stats.get("reported_days", 0)
        missing_days = stats.get("missing_days", [])
        declared_hours = stats.get("declared_hours", 0.0)
        warning_flags = stats.get("warning_flags", [])
        is_unverified = any("UNVERIFIED" in str(f) for f in warning_flags)

        if rep_days == 0:
            score_log = 0.0
        else:
            base_log = (rep_days / 3.0) * 80.0 + (min(24.0, declared_hours) / 24.0) * 20.0
            if is_unverified:
                base_log -= 25.0
            score_log = max(0.0, min(100.0, round(base_log, 1)))

        viols = staff_violations_map.get(name_clean, [])
        score_ops = max(30.0, round(100.0 - len(viols) * 6.0, 1))

        is_active_teaching = any(t in name_clean or name_clean in t for t in teaching_staff_names)

        if is_active_teaching:
            a1_inst = instructors_a1.get(name_raw, {}) or instructors_a1.get(display_name, {})
            score_sv = a1_inst.get("student_discipline_score", 85.0)

            related_classes = [c for c in classes_list if name_clean in c['gv'].lower() or name_clean in c['tg'].lower()]
            if related_classes:
                score_acad = round(sum(c['pred_pass'] for c in related_classes) / len(related_classes), 1)
            else:
                score_acad = 75.0

            kpi_total = round((score_sv * 0.20 + score_ops * 0.20) + (score_acad * 0.30 + score_log * 0.30), 1)

            if rep_days == 0 or score_log < 50.0:
                perf_group = "🚨 Cần Tái Đào Tạo"
                group_badge = "bg-rose-500/20 text-rose-300 border-rose-500/40"
            elif kpi_total >= 85.0 and score_ops >= 85.0:
                perf_group = "⭐ Xuất Sắc"
                group_badge = "bg-emerald-500/20 text-emerald-300 border-emerald-500/40"
            elif score_ops < 75.0:
                perf_group = "⚠️ Kỷ Luật Tác Nghiệp"
                group_badge = "bg-amber-500/20 text-amber-300 border-amber-500/40"
            else:
                perf_group = "✓ Đạt Chuẩn"
                group_badge = "bg-indigo-500/20 text-indigo-300 border-indigo-500/40"

            teaching_staff_list.append({
                "name": display_name,
                "role": role,
                "rank": rank,
                "dept": dept,
                "campus": campus,
                "rep_days": rep_days,
                "missing_days": missing_days,
                "kpi_total": kpi_total,
                "score_sv": score_sv,
                "score_ops": score_ops,
                "score_acad": score_acad,
                "score_log": score_log,
                "violation_count": len(viols),
                "is_unverified": is_unverified,
                "perf_group": perf_group,
                "group_badge": group_badge,
                "classes_assigned": [c['class_name'] for c in related_classes]
            })
        else:
            pmo_kpi = round(score_log * 0.60 + score_ops * 0.40, 1)

            if rep_days == 0:
                perf_group = "🚨 Chưa Nộp Báo Cáo"
                group_badge = "bg-rose-500/20 text-rose-300 border-rose-500/40"
            elif pmo_kpi >= 85.0:
                perf_group = "⭐ Hoàn Thành Tốt"
                group_badge = "bg-emerald-500/20 text-emerald-300 border-emerald-500/40"
            else:
                perf_group = "⚠️ Chậm Tiến Độ"
                group_badge = "bg-amber-500/20 text-amber-300 border-amber-500/40"

            support_staff_list.append({
                "name": display_name,
                "role": role,
                "rank": rank,
                "dept": dept,
                "campus": campus,
                "rep_days": rep_days,
                "missing_days": missing_days,
                "pmo_kpi": pmo_kpi,
                "score_ops": score_ops,
                "score_log": score_log,
                "declared_hours": declared_hours,
                "violation_count": len(viols),
                "is_unverified": is_unverified,
                "perf_group": perf_group,
                "group_badge": group_badge
            })

    teaching_staff_list.sort(key=lambda s: -s['kpi_total'])
    support_staff_list.sort(key=lambda s: -s['pmo_kpi'])

    total_students = 1236
    r1_urgent = [s for s in care_list if s.get('risk_level') == 'RED']
    r2_banned = [s for s in care_list if s.get('is_failed_new') and not s.get('is_excellent')]
    r3_paradox = [s for s in care_list if s.get('is_excellent') and s.get('is_failed_new')]
    r4_safe = max(0, total_students - len(care_list))

    risk_breakdown = {
        "total_students": total_students,
        "care_list_total": len(care_list),
        "r1_count": len(r1_urgent),
        "r1_pct": round(len(r1_urgent) / total_students * 100.0, 1),
        "r2_count": len(r2_banned),
        "r2_pct": round(len(r2_banned) / total_students * 100.0, 1),
        "r3_count": len(r3_paradox),
        "r3_pct": round(len(r3_paradox) / total_students * 100.0, 1),
        "r4_count": r4_safe,
        "r4_pct": round(r4_safe / total_students * 100.0, 1)
    }

    avg_pass_rate = round(sum(c['pred_pass'] for c in classes_list) / len(classes_list), 1) if classes_list else 78.4
    avg_violation = round(sum(c['v_class'] for c in classes_list) / len(classes_list), 1) if classes_list else 12.8
    avg_ops_score = round(sum(s['score_ops'] for s in teaching_staff_list) / len(teaching_staff_list), 1) if teaching_staff_list else 89.5
    avg_log_rate = round(sum(s['score_log'] for s in teaching_staff_list + support_staff_list) / len(teaching_staff_list + support_staff_list), 1)

    missing_leaders = [s['name'] for s in support_staff_list + teaching_staff_list if s['rep_days'] == 0 and any(l in s['name'].lower() for l in ['cường', 'hùng', 'đạo', 'huấn'])]

    return {
        "macro_kpis": {
            "avg_pass_rate": avg_pass_rate,
            "avg_violation": avg_violation,
            "avg_ops_score": avg_ops_score,
            "avg_log_rate": avg_log_rate,
            "total_classes": len(classes_list),
            "teaching_staff_count": len(teaching_staff_list),
            "support_staff_count": len(support_staff_list),
            "missing_leaders_count": len(missing_leaders)
        },
        "risk_breakdown": risk_breakdown,
        "classes": classes_list,
        "teaching_staff": teaching_staff_list,
        "support_staff": support_staff_list,
        "missing_leaders": missing_leaders
    }

def main():
    output_path = "output/dashboards/core/agent_5_master_portal.html"
    print("Agent 5: Biên dịch Executive Dashboard Điều Hành Giám Sát Chất Lượng Đào Tạo (Full Width Staff Table & Native iFrames)...")

    dataset = build_executive_dataset()
    macro = dataset["macro_kpis"]
    risk = dataset["risk_breakdown"]
    dataset_json = json.dumps(dataset, ensure_ascii=False)

    master_html = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Điều Hành Giám Sát Chất Lượng Đào Tạo — Rikkei Education &amp; PTIT</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{ sans: ['"Plus Jakarta Sans"', 'sans-serif'] }},
                    colors: {{
                        brand: {{ 50: '#eef2ff', 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca', 900: '#312e81' }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{
            background-color: #090d16;
            color: #f8fafc;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 14px;
            line-height: 1.55;
            overflow-x: hidden;
        }}
        .glass-panel {{
            background: rgba(15, 23, 42, 0.92);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}
        .glass-card {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.78) 0%, rgba(15, 23, 42, 0.94) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.45);
        }}
        .nav-btn.active {{
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.45);
            border-color: rgba(99, 102, 241, 0.5);
        }}
        .filter-chip.active {{
            background: #4f46e5;
            color: #ffffff;
            border-color: #6366f1;
        }}
        .staff-pill-btn.active {{
            background: #4f46e5;
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
        }}
        #master-slide-drawer {{
            transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        #master-slide-drawer.open {{
            transform: translateX(0);
        }}
        ::-webkit-scrollbar {{ width: 7px; height: 7px; }}
        ::-webkit-scrollbar-track {{ background: rgba(15, 23, 42, 0.6); }}
        ::-webkit-scrollbar-thumb {{ background: rgba(99, 102, 241, 0.45); border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: rgba(99, 102, 241, 0.85); }}
    </style>
</head>
<body class="min-h-screen flex flex-col selection:bg-indigo-500 selection:text-white">

    <!-- HEADER TỐI CAO BAN LÃNH ĐẠO -->
    <header class="sticky top-0 z-40 glass-panel border-b border-slate-800/80 px-6 py-4 shadow-xl">
        <div class="max-w-[1600px] mx-auto flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-400 flex items-center justify-center text-white text-xl shadow-lg shadow-indigo-500/30">
                    <i class="fas fa-university"></i>
                </div>
                <div>
                    <div class="flex items-center gap-2.5">
                        <h1 class="text-lg font-extrabold text-white tracking-tight">BÁO CÁO ĐIỀU HÀNH GIÁM SÁT CHẤT LƯỢNG ĐÀO TẠO</h1>
                        <span class="px-3 py-0.5 rounded-full text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Rikkei Education</span>
                    </div>
                    <p class="text-sm text-slate-300 mt-0.5">Phạm vi: <strong class="text-slate-100">{macro['total_classes']} Lớp Học Kỳ II</strong> • <strong class="text-slate-100">{macro['teaching_staff_count'] + macro['support_staff_count']} Cán bộ Giảng viên/Trợ giảng</strong> • <strong class="text-slate-100">{risk['total_students']} Học viên PTIT</strong></p>
                </div>
            </div>

            <!-- Bộ Lọc Nhanh C-Level -->
            <div class="flex flex-wrap items-center gap-3">
                <div class="flex items-center bg-slate-950/80 p-1.5 rounded-xl border border-slate-800 text-sm">
                    <span class="px-3 py-1 text-slate-400 font-semibold"><i class="fas fa-building mr-1.5"></i>Cơ sở:</span>
                    <button onclick="setFilter('campus', 'ALL')" id="filter-campus-ALL" class="filter-chip active px-3.5 py-1.5 rounded-lg text-slate-300 hover:text-white transition font-medium">Tất cả</button>
                    <button onclick="setFilter('campus', 'HN')" id="filter-campus-HN" class="filter-chip px-3.5 py-1.5 rounded-lg text-slate-300 hover:text-white transition font-medium">Hà Nội</button>
                    <button onclick="setFilter('campus', 'HCM')" id="filter-campus-HCM" class="filter-chip px-3.5 py-1.5 rounded-lg text-slate-300 hover:text-white transition font-medium">TP. HCM</button>
                </div>

                <div class="flex items-center bg-slate-950/80 p-1.5 rounded-xl border border-slate-800 text-sm">
                    <span class="px-3 py-1 text-slate-400 font-semibold"><i class="fas fa-layer-group mr-1.5"></i>Khối:</span>
                    <button onclick="setFilter('dept', 'ALL')" id="filter-dept-ALL" class="filter-chip active px-3.5 py-1.5 rounded-lg text-slate-300 hover:text-white transition font-medium">Tất cả</button>
                    <button onclick="setFilter('dept', 'Khối CNTT')" id="filter-dept-CNTT" class="filter-chip px-3.5 py-1.5 rounded-lg text-slate-300 hover:text-white transition font-medium">Khối CNTT</button>
                    <button onclick="setFilter('dept', 'Khối QTKD')" id="filter-dept-QTKD" class="filter-chip px-3.5 py-1.5 rounded-lg text-slate-300 hover:text-white transition font-medium">Khối QTKD</button>
                </div>

                <button onclick="location.reload()" class="p-2.5 bg-slate-800/80 hover:bg-slate-700 text-slate-300 rounded-xl border border-slate-700 transition" title="Tải lại số liệu">
                    <i class="fas fa-sync-alt"></i>
                </button>
            </div>

        </div>

        <!-- THANH ĐIỀU HƯỚNG TAB CHÍNH -->
        <div class="max-w-[1600px] mx-auto mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between flex-wrap gap-2">
            <div class="flex items-center gap-2.5 overflow-x-auto pb-1">
                <button onclick="switchMasterTab('cockpit')" id="nav-cockpit" class="nav-btn active px-4 py-2.5 rounded-xl text-sm font-bold border border-slate-700 text-slate-200 transition flex items-center gap-2">
                    <i class="fas fa-tachometer-alt"></i> Bảng Điều Hành Tổng Thể
                </button>
                <button onclick="switchMasterTab('agent1')" id="nav-agent1" class="nav-btn px-4 py-2.5 rounded-xl text-sm font-bold border border-transparent hover:border-slate-700 text-slate-300 hover:text-white transition flex items-center gap-2">
                    <i class="fas fa-user-shield"></i> 1. Kỷ Luật Sinh Viên
                </button>
                <button onclick="switchMasterTab('agent2')" id="nav-agent2" class="nav-btn px-4 py-2.5 rounded-xl text-sm font-bold border border-transparent hover:border-slate-700 text-slate-300 hover:text-white transition flex items-center gap-2">
                    <i class="fas fa-graduation-cap"></i> 2. Dự Báo &amp; Care List
                </button>
                <button onclick="switchMasterTab('agent3')" id="nav-agent3" class="nav-btn px-4 py-2.5 rounded-xl text-sm font-bold border border-transparent hover:border-slate-700 text-slate-300 hover:text-white transition flex items-center gap-2">
                    <i class="fas fa-chalkboard-teacher"></i> 3. Kỷ Luật Giảng Dạy
                </button>
                <button onclick="switchMasterTab('agent4')" id="nav-agent4" class="nav-btn px-4 py-2.5 rounded-xl text-sm font-bold border border-transparent hover:border-slate-700 text-slate-300 hover:text-white transition flex items-center gap-2">
                    <i class="fas fa-clipboard-check"></i> 4. Tiến Độ &amp; Báo Cáo PMO
                </button>
            </div>
            
            <div class="text-xs text-slate-400 flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                Dữ liệu đồng bộ: <span class="text-slate-200 font-bold">{macro['total_classes']} Lớp Học Kỳ II</span> • <span class="text-slate-200 font-bold">{macro['teaching_staff_count'] + macro['support_staff_count']} Nhân sự</span>
            </div>
        </div>
    </header>

    <!-- TAB 0: BẢNG ĐIỀU HÀNH TỔNG THỂ (EXECUTIVE VIEW) -->
    <section id="tab-cockpit-view" class="max-w-[1600px] mx-auto px-6 py-6 space-y-6 w-full">

        <!-- TẦNG 1: 4 CHỈ SỐ HOẠT ĐỘNG TRỌNG YẾU (CORE TRAINING KPIS) -->
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
            
            <!-- KPI 1 -->
            <div class="glass-card p-5 rounded-2xl relative overflow-hidden flex flex-col justify-between border-t-4 border-t-indigo-500">
                <div>
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Dự Báo Hoàn Thành Môn Học</span>
                        <span class="p-2.5 rounded-xl bg-indigo-500/15 text-indigo-400 text-base"><i class="fas fa-graduation-cap"></i></span>
                    </div>
                    <div class="mt-3.5 flex items-baseline gap-3">
                        <div class="text-4xl font-black text-white" id="card-pass-rate">{macro['avg_pass_rate']}%</div>
                        <span class="text-xs font-bold text-indigo-300">Mục tiêu: ≥ 85%</span>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-800 text-xs text-slate-300 flex items-start gap-2">
                    <i class="fas fa-info-circle text-indigo-400 mt-0.5"></i>
                    <span>Tỷ lệ hoàn thành bình quân 19 lớp học kỳ II (đã trừ hệ số phạt môi trường).</span>
                </div>
            </div>

            <!-- KPI 2 -->
            <div class="glass-card p-5 rounded-2xl relative overflow-hidden flex flex-col justify-between border-t-4 border-t-emerald-500">
                <div>
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Chỉ Số Kỷ Luật Học Đường</span>
                        <span class="p-2.5 rounded-xl bg-emerald-500/15 text-emerald-400 text-base"><i class="fas fa-user-check"></i></span>
                    </div>
                    <div class="mt-3.5 flex items-baseline gap-3">
                        <div class="text-4xl font-black text-emerald-400" id="card-discipline-rate">{100.0 - macro['avg_violation']:.1f}%</div>
                        <span class="text-xs text-slate-400 font-medium">Vi phạm: {macro['avg_violation']}%</span>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-800 text-xs text-slate-300 flex items-start gap-2">
                    <i class="fas fa-info-circle text-emerald-400 mt-0.5"></i>
                    <span>Tổng hợp từ Chuyên cần (vắng), Nợ bài tập và Chậm hoàn thành Elearning.</span>
                </div>
            </div>

            <!-- KPI 3 -->
            <div class="glass-card p-5 rounded-2xl relative overflow-hidden flex flex-col justify-between border-t-4 border-t-amber-500">
                <div>
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Kỷ Luật Tác Nghiệp Đội Ngũ</span>
                        <span class="p-2.5 rounded-xl bg-amber-500/15 text-amber-400 text-base"><i class="fas fa-chalkboard-teacher"></i></span>
                    </div>
                    <div class="mt-3.5 flex items-baseline gap-3">
                        <div class="text-4xl font-black text-amber-400" id="card-ops-score">{macro['avg_ops_score']} <span class="text-sm font-normal text-slate-400">/ 100đ</span></div>
                        <span class="text-xs text-slate-400 font-medium">Khung chế tài T6/2026</span>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-800 text-xs text-slate-300 flex items-start gap-2">
                    <i class="fas fa-info-circle text-amber-400 mt-0.5"></i>
                    <span>Đánh giá mức độ tuân thủ quy chế lên lớp, chấm BTVN và cập nhật tài nguyên.</span>
                </div>
            </div>

            <!-- KPI 4 -->
            <div class="glass-card p-5 rounded-2xl relative overflow-hidden flex flex-col justify-between border-t-4 border-t-rose-500">
                <div>
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Kỷ Luật Báo Cáo Điều Hành</span>
                        <span class="p-2.5 rounded-xl bg-rose-500/15 text-rose-400 text-base"><i class="fas fa-tasks"></i></span>
                    </div>
                    <div class="mt-3.5 flex items-baseline gap-3">
                        <div class="text-4xl font-black text-white" id="card-log-rate">{macro['avg_log_rate']}%</div>
                        <span class="text-xs font-bold text-rose-400 px-2.5 py-1 rounded-full bg-rose-500/20">{macro['missing_leaders_count']} Cán bộ Quản lý Chưa Nộp</span>
                    </div>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-800 text-xs text-slate-300 flex items-start gap-2">
                    <i class="fas fa-info-circle text-rose-400 mt-0.5"></i>
                    <span>Tỷ lệ nộp nhật ký điều hành và hoàn thành nhiệm vụ theo chuẩn Worklane.</span>
                </div>
            </div>

        </div>

        <!-- TẦNG 2: BẢNG CHẨN ĐOÁN CĂN NGUYÊN & NĂNG LỰC THỰC CHIẾN 3 KHỐI ĐÀO TẠO -->
        <div class="glass-card p-6 rounded-2xl">
            <div class="flex items-center justify-between mb-5 pb-3 border-b border-slate-800">
                <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-base">
                        <i class="fas fa-microscope"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-slate-100">Báo Cáo Chẩn Đoán Căn Nguyên &amp; Năng Lực Thực Chiến (Theo 3 Khối Đào Tạo)</h3>
                        <p class="text-xs text-slate-400 mt-0.5">Đối soát từ kết quả thi ĐGNL, lịch sử học tập database và tiến độ các môn học Học kỳ II</p>
                    </div>
                </div>
                <span class="text-xs px-3 py-1.5 rounded-lg bg-indigo-600/30 text-indigo-200 font-mono">Curriculum Analytics</span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 text-sm">
                
                <!-- Khối 1: KS24 CNTT -->
                <div class="p-5 rounded-xl bg-slate-950/60 border border-slate-800 flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between pb-2.5 border-b border-slate-800">
                            <span class="font-extrabold text-slate-100 text-base">1. Khối KS24 CNTT (Kỳ IV)</span>
                            <span class="px-2.5 py-1 rounded text-xs font-bold bg-indigo-500/20 text-indigo-300">AI Integration</span>
                        </div>
                        <div class="mt-3.5 space-y-2.5 text-slate-300">
                            <p><strong>• Hiện trạng:</strong> 4/5 lớp vận hành ổn định (vi phạm &lt; 10%). Riêng lớp <strong class="text-rose-400">HN-K24-CNTT3</strong> vi phạm 30.9%, nợ bài 26.8%, dự báo đỗ chỉ 36.0%.</p>
                            <p><strong>• Căn nguyên:</strong> Môn AI Integration có hàm lượng thực hành API/LLM lớn. Lớp CNTT3 sĩ số đông (42 bạn) nhưng Trợ giảng chưa kèm phụ đạo sát sao.</p>
                        </div>
                    </div>
                    <div class="pt-3 border-t border-slate-800/80 text-xs text-indigo-300 font-semibold">
                        ⚡ <strong>Chỉ đạo:</strong> TG mở 2 ca phụ đạo trong tuần; GV chốt sản phẩm Mini-Project.
                    </div>
                </div>

                <!-- Khối 2: KS25 CNTT -->
                <div class="p-5 rounded-xl bg-slate-950/60 border border-slate-800 flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between pb-2.5 border-b border-slate-800">
                            <span class="font-extrabold text-slate-100 text-base">2. Khối KS25 CNTT (Kỳ II)</span>
                            <span class="px-2.5 py-1 rounded text-xs font-bold bg-amber-500/20 text-amber-300">Python Web &amp; FastAPI</span>
                        </div>
                        <div class="mt-3.5 space-y-2.5 text-slate-300">
                            <p><strong>• Hiện trạng:</strong> Đang ở giai đoạn then chốt. Bài học từ kỳ thi ĐGNL vừa qua trượt thực hành <strong class="text-rose-400">85.9%</strong> cho thấy lỗ hổng lớn về kỹ năng tự viết code độc lập.</p>
                            <p><strong>• Căn nguyên:</strong> Mất gốc tích lũy từ JS/DB kỳ trước. Nếu TG buông lỏng việc chấm BTVN các session đầu, học viên sẽ bỏ cuộc khi vào phần Database ORM.</p>
                        </div>
                    </div>
                    <div class="pt-3 border-t border-slate-800/80 text-xs text-amber-300 font-semibold">
                        ⚡ <strong>Chỉ đạo:</strong> TG nghiệm thu bài tập 100% từng buổi; GV tăng 50% thời lượng Live-Code.
                    </div>
                </div>

                <!-- Khối 3: KS25 QTKD -->
                <div class="p-5 rounded-xl bg-slate-950/60 border border-slate-800 flex flex-col justify-between space-y-4">
                    <div>
                        <div class="flex items-center justify-between pb-2.5 border-b border-slate-800">
                            <span class="font-extrabold text-slate-100 text-base">3. Khối KS25 QTKD (Kỳ II)</span>
                            <span class="px-2.5 py-1 rounded text-xs font-bold bg-emerald-500/20 text-emerald-300">Business Analysis BA201</span>
                        </div>
                        <div class="mt-3.5 space-y-2.5 text-slate-300">
                            <p><strong>• Hiện trạng:</strong> Đạt chuẩn xuất sắc toàn diện. Cả 3 lớp tỷ lệ vi phạm dưới <strong class="text-emerald-400">8.0%</strong>, tỷ lệ dự báo qua môn đạt trên 85%.</p>
                            <p><strong>• Căn nguyên:</strong> Đội ngũ GV/TG QTKD (cô Hồng Minh, cô Vân Khanh) duy trì nề nếp điểm danh và kiểm tra bài tập Case Study nghiêm túc.</p>
                        </div>
                    </div>
                    <div class="pt-3 border-t border-slate-800/80 text-xs text-emerald-300 font-semibold">
                        ⚡ <strong>Chỉ đạo:</strong> Duy trì tiến độ; nhân rộng mô hình kiểm soát nề nếp sang các khối khác.
                    </div>
                </div>

            </div>
        </div>

        <!-- TẦNG 3: BẢNG PHÂN BỔ 4 NHÓM NGUY CƠ HỌC VIÊN TOÀN TRƯỜNG -->
        <div class="glass-card p-6 rounded-2xl">
            <div class="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-sm">
                        <i class="fas fa-users"></i>
                    </div>
                    <h3 class="text-sm font-bold text-slate-100 uppercase tracking-wider">Phân Bổ Học Viên Theo 4 Cấp Độ Năng Lực &amp; Nguy Cơ (Toàn trường: {risk['total_students']} SV)</h3>
                </div>
                <span class="text-xs text-slate-300">Tổng Danh sách Can thiệp (Care List): <strong class="text-rose-400 text-sm font-bold">{risk['care_list_total']} SV</strong> ({risk['r1_pct']}%)</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-rose-400">🔴 Nhóm 1: Cứu điểm khẩn cấp</span>
                        <span class="text-xs font-black text-rose-300">{risk['r1_pct']}%</span>
                    </div>
                    <div class="mt-2.5 text-2xl font-black text-white">{risk['r1_count']} <span class="text-xs font-normal text-slate-400">học viên</span></div>
                    <div class="text-xs text-slate-300 mt-1.5">GPA dưới 4.0 / Nguy cơ trượt môn cao</div>
                </div>

                <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-amber-400">🟡 Nhóm 2: Cảnh báo cấm thi</span>
                        <span class="text-xs font-black text-amber-300">{risk['r2_pct']}%</span>
                    </div>
                    <div class="mt-2.5 text-2xl font-black text-white">{risk['r2_count']} <span class="text-xs font-normal text-slate-400">học viên</span></div>
                    <div class="text-xs text-slate-300 mt-1.5">Vắng cận 20% hoặc Nợ bài tập >40%</div>
                </div>

                <div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-purple-400">⚡ Nhóm 3: Nghịch lý Kỷ luật</span>
                        <span class="text-xs font-black text-purple-300">{risk['r3_pct']}%</span>
                    </div>
                    <div class="mt-2.5 text-2xl font-black text-white">{risk['r3_count']} <span class="text-xs font-normal text-slate-400">học viên</span></div>
                    <div class="text-xs text-slate-300 mt-1.5">Điểm cao (≥8.0) nhưng đối mặt cấm thi</div>
                </div>

                <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-emerald-400">🟢 Nhóm 4: Vùng An toàn</span>
                        <span class="text-xs font-black text-emerald-300">{risk['r4_pct']}%</span>
                    </div>
                    <div class="mt-2.5 text-2xl font-black text-white">{risk['r4_count']} <span class="text-xs font-normal text-slate-400">học viên</span></div>
                    <div class="text-xs text-slate-300 mt-1.5">Dự báo đạt chuẩn qua môn theo quy chế</div>
                </div>
            </div>
        </div>

        <!-- TẦNG 4: DANH MỤC THẺ 19 LỚP HỌC KỲ II THEO TỪNG KHỐI (GROUPED CLASS CARDS GRID) -->
        <div class="glass-card p-6 rounded-2xl space-y-6">
            <div class="flex items-center justify-between pb-3.5 border-b border-slate-800">
                <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-base">
                        <i class="fas fa-th-large"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-slate-100">Bảng Giám Sát 19 Lớp Học Kỳ II Đang Vận Hành (Phân Theo Khối &amp; Cơ Sở)</h3>
                        <p class="text-xs text-slate-400 mt-0.5">Nhấp vào thẻ lớp học bất kỳ để mở ngăn kéo tra cứu danh sách học viên và chỉ số chuyên sâu</p>
                    </div>
                </div>
                <span class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-200 font-mono font-bold" id="class-grid-count">{macro['total_classes']} lớp học</span>
            </div>

            <!-- Container Thẻ Lớp Học Được Phân Nhóm Theo Khối -->
            <div id="grouped-class-cards-container" class="space-y-6">
                <!-- Rendered by JS -->
            </div>
        </div>

        <!-- TẦNG 5: ĐÁNH GIÁ ĐỘI NGŨ NHÂN SỰ TOÀN DIỆN (FULL-WIDTH, KHÔNG CUỘN TRỤC X/Y) -->
        <div class="glass-card p-6 rounded-2xl space-y-5">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
                <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-base">
                        <i class="fas fa-id-badge"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-slate-100">Bảng Đánh Giá KPI &amp; Xếp Loại Năng Lực Đội Ngũ Nhân Sự Đào Tạo</h3>
                        <p class="text-xs text-slate-400 mt-0.5">Hiển thị trọn vẹn toàn bộ cán bộ, không bị giới hạn cuộn (Scroll-free Executive View)</p>
                    </div>
                </div>

                <!-- Nút Chuyển Phân Tầng Nhân Sự -->
                <div class="flex items-center bg-slate-950 p-1.5 rounded-xl border border-slate-800 text-sm">
                    <button onclick="switchStaffSubView('teaching')" id="btn-staff-teaching" class="staff-pill-btn active px-4 py-2 rounded-lg font-bold transition flex items-center gap-2">
                        <i class="fas fa-chalkboard-teacher"></i> Đội Ngũ Đứng Lớp ({macro['teaching_staff_count']} Cán bộ)
                    </button>
                    <button onclick="switchStaffSubView('support')" id="btn-staff-support" class="staff-pill-btn px-4 py-2 rounded-lg text-slate-400 hover:text-white font-bold transition flex items-center gap-2">
                        <i class="fas fa-user-cog"></i> Khối Gián Tiếp / PMO ({macro['support_staff_count']} Cán bộ)
                    </button>
                </div>
            </div>

            <!-- VIEW 1: ĐỘI NGŨ TRỰC TIẾP ĐỨNG LỚP (FULL-WIDTH TABLE) -->
            <div id="view-teaching-staff" class="w-full">
                <table class="w-full text-left text-sm border-collapse">
                    <thead class="bg-slate-950/90 text-slate-400 uppercase text-xs font-bold border-b border-slate-800">
                        <tr>
                            <th class="py-3.5 px-4">Họ và Tên Cán Bộ</th>
                            <th class="py-3.5 px-3">Cơ Sở &amp; Rank</th>
                            <th class="py-3.5 px-3">Lớp Phụ Trách</th>
                            <th class="py-3.5 px-3">Vai Trò</th>
                            <th class="py-3.5 px-3 text-center">Tác Nghiệp (20%)</th>
                            <th class="py-3.5 px-3 text-center">Báo Cáo (30%)</th>
                            <th class="py-3.5 px-3 text-center">Học Tập SV (30%)</th>
                            <th class="py-3.5 px-3 text-center">Kỷ Luật SV (20%)</th>
                            <th class="py-3.5 px-4 text-center">KPI Tổng</th>
                            <th class="py-3.5 px-4 text-center">Xếp Loại</th>
                        </tr>
                    </thead>
                    <tbody id="teaching-staff-tbody" class="divide-y divide-slate-800/40">
                        <!-- Rendered by JS -->
                    </tbody>
                </table>
            </div>

            <!-- VIEW 2: KHỐI CHUYÊN MÔN GIÁN TIẾP / HỖ TRỢ / R&D (FULL-WIDTH TABLE) -->
            <div id="view-support-staff" class="w-full hidden">
                <table class="w-full text-left text-sm border-collapse">
                    <thead class="bg-slate-950/90 text-slate-400 uppercase text-xs font-bold border-b border-slate-800">
                        <tr>
                            <th class="py-3.5 px-4">Họ và Tên Cán Bộ</th>
                            <th class="py-3.5 px-3">Cơ Sở &amp; Rank</th>
                            <th class="py-3.5 px-3">Khối Chuyên Môn</th>
                            <th class="py-3.5 px-3">Chức Vụ</th>
                            <th class="py-3.5 px-3 text-center">Tác Nghiệp (40%)</th>
                            <th class="py-3.5 px-3 text-center">Báo Cáo PMO (60%)</th>
                            <th class="py-3.5 px-3 text-center">Tổng Giờ Khai</th>
                            <th class="py-3.5 px-4 text-center">Điểm PMO</th>
                            <th class="py-3.5 px-4 text-center">Trạng Thái</th>
                        </tr>
                    </thead>
                    <tbody id="support-staff-tbody" class="divide-y divide-slate-800/40">
                        <!-- Rendered by JS -->
                    </tbody>
                </table>
            </div>

            <div class="pt-3 border-t border-slate-800/60 text-xs text-slate-400 flex items-center justify-between">
                <span>💡 <em>Nhấp vào hàng nhân sự bất kỳ để mở ngăn kéo xem hồ sơ đánh giá chi tiết và nhật ký báo cáo.</em></span>
                <span class="text-slate-300 font-medium">Khung chuẩn đánh giá KPI &amp; Chế tài đào tạo 2026</span>
            </div>
        </div>

    </section>

    <!-- CONTAINER CÁC TAB CHI TIẾT CON (AGENT 1, 2, 3, 4) QUA FULL-SCREEN NATIVE VIEWPORT (SEAMLESS SCROLL-FREE) -->
    <div id="subagents-viewport" class="fixed inset-x-0 bottom-0 top-[76px] w-full h-[calc(100vh-76px)] z-30 bg-slate-950 hidden">
        <div id="tab-agent1-container" class="spa-tab-content hidden w-full h-full">
            <iframe src="agent_1_student_discipline.html" class="w-full h-full border-0 bg-slate-950 block" loading="lazy"></iframe>
        </div>

        <div id="tab-agent2-pred-container" class="spa-tab-content hidden w-full h-full">
            <iframe src="agent_2_academic_prediction.html" class="w-full h-full border-0 bg-slate-950 block" loading="lazy"></iframe>
        </div>

        <div id="tab-agent3-container" class="spa-tab-content hidden w-full h-full">
            <iframe src="agent_3_ops_discipline.html" class="w-full h-full border-0 bg-slate-950 block" loading="lazy"></iframe>
        </div>

        <div id="tab-agent4-container" class="spa-tab-content hidden w-full h-full">
            <iframe src="agent_4_daily_logs.html" class="w-full h-full border-0 bg-slate-950 block" loading="lazy"></iframe>
        </div>
    </div>

    <!-- SLIDE-OVER DRAWER RIÊNG CHO MASTER COCKPIT (FULL CHIỀU DÀI, CUỘN MƯỢT MÀ KHÔNG BỊ GIỚI HẠN) -->
    <div id="master-drawer-backdrop" onclick="closeMasterDrawer()" class="fixed inset-0 bg-black/75 backdrop-blur-md z-50 opacity-0 pointer-events-none transition-opacity duration-300"></div>
    <div id="master-slide-drawer" class="fixed top-0 right-0 bottom-0 w-full max-w-[580px] bg-slate-900 border-l border-slate-700/80 z-50 translate-x-full shadow-2xl p-6 flex flex-col justify-between h-screen">
        <div class="flex flex-col h-full overflow-hidden">
            <div class="flex items-center justify-between pb-4 border-b border-slate-800 flex-shrink-0">
                <div class="flex items-center gap-3">
                    <div id="master-drawer-icon" class="w-9 h-9 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-base">
                        <i class="fas fa-graduation-cap"></i>
                    </div>
                    <h3 id="master-drawer-title" class="text-lg font-extrabold text-white">Chi tiết lớp học</h3>
                </div>
                <button onclick="closeMasterDrawer()" class="text-slate-400 hover:text-white text-lg p-2 rounded-lg hover:bg-slate-800 transition">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <!-- Vùng cuộn tự nhiên toàn màn hình cho Drawer -->
            <div id="master-drawer-body" class="mt-5 space-y-4 text-sm overflow-y-auto flex-1 pr-1.5">
                <!-- Nội dung chi tiết được điền tự động bằng JavaScript -->
            </div>

            <div class="pt-4 mt-2 border-t border-slate-800 text-right flex-shrink-0">
                <button onclick="closeMasterDrawer()" class="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-bold transition">Đóng ngăn kéo</button>
            </div>
        </div>
    </div>

    <!-- SCRIPT ĐIỀU HÀNH EXECUTIVE DASHBOARD -->
    <script>
        const EXECUTIVE_DATA = {dataset_json};
        let currentCampus = 'ALL';
        let currentDept = 'ALL';

        function switchMasterTab(tabKey) {{
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById('nav-' + tabKey);
            if (activeBtn) activeBtn.classList.add('active');

            const cockpitView = document.getElementById('tab-cockpit-view');
            const subagentsViewport = document.getElementById('subagents-viewport');

            document.getElementById('tab-agent1-container').classList.add('hidden');
            document.getElementById('tab-agent2-pred-container').classList.add('hidden');
            document.getElementById('tab-agent3-container').classList.add('hidden');
            document.getElementById('tab-agent4-container').classList.add('hidden');

            if (tabKey === 'cockpit') {{
                cockpitView.classList.remove('hidden');
                subagentsViewport.classList.add('hidden');
                document.body.style.overflow = 'auto';
            }} else {{
                cockpitView.classList.add('hidden');
                subagentsViewport.classList.remove('hidden');
                document.body.style.overflow = 'hidden';

                if (tabKey === 'agent1') {{
                    document.getElementById('tab-agent1-container').classList.remove('hidden');
                }} else if (tabKey === 'agent2') {{
                    document.getElementById('tab-agent2-pred-container').classList.remove('hidden');
                }} else if (tabKey === 'agent3') {{
                    document.getElementById('tab-agent3-container').classList.remove('hidden');
                }} else if (tabKey === 'agent4') {{
                    document.getElementById('tab-agent4-container').classList.remove('hidden');
                }}
            }}
            window.dispatchEvent(new Event('resize'));
        }}

        function switchStaffSubView(viewType) {{
            if (viewType === 'teaching') {{
                document.getElementById('btn-staff-teaching').classList.add('active');
                document.getElementById('btn-staff-teaching').classList.remove('text-slate-400');
                document.getElementById('btn-staff-support').classList.remove('active');
                document.getElementById('btn-staff-support').classList.add('text-slate-400');
                document.getElementById('view-teaching-staff').classList.remove('hidden');
                document.getElementById('view-support-staff').classList.add('hidden');
            }} else {{
                document.getElementById('btn-staff-support').classList.add('active');
                document.getElementById('btn-staff-support').classList.remove('text-slate-400');
                document.getElementById('btn-staff-teaching').classList.remove('active');
                document.getElementById('btn-staff-teaching').classList.add('text-slate-400');
                document.getElementById('view-support-staff').classList.remove('hidden');
                document.getElementById('view-teaching-staff').classList.add('hidden');
            }}
        }}

        function setFilter(type, val) {{
            if (type === 'campus') {{
                currentCampus = val;
                document.querySelectorAll('[id^="filter-campus-"]').forEach(el => el.classList.remove('active'));
                document.getElementById('filter-campus-' + val).classList.add('active');
            }} else if (type === 'dept') {{
                currentDept = val;
                document.querySelectorAll('[id^="filter-dept-"]').forEach(el => el.classList.remove('active'));
                const key = val === 'ALL' ? 'ALL' : (val.includes('CNTT') ? 'CNTT' : 'QTKD');
                document.getElementById('filter-dept-' + key).classList.add('active');
            }}
            applyExecutiveFilters();
        }}

        function applyExecutiveFilters() {{
            const filteredClasses = EXECUTIVE_DATA.classes.filter(c => {{
                const matchCampus = (currentCampus === 'ALL' || c.campus === currentCampus);
                const matchDept = (currentDept === 'ALL' || c.dept === currentDept);
                return matchCampus && matchDept;
            }});

            const filteredTeachingStaff = EXECUTIVE_DATA.teaching_staff.filter(s => {{
                const matchCampus = (currentCampus === 'ALL' || s.campus === currentCampus);
                const matchDept = (currentDept === 'ALL' || s.dept.includes(currentDept.replace('Khối ', '')));
                return matchCampus && matchDept;
            }});

            const filteredSupportStaff = EXECUTIVE_DATA.support_staff.filter(s => {{
                const matchCampus = (currentCampus === 'ALL' || s.campus === currentCampus);
                const matchDept = (currentDept === 'ALL' || s.dept.includes(currentDept.replace('Khối ', '')));
                return matchCampus && matchDept;
            }});

            if (filteredClasses.length > 0) {{
                const avgPass = (filteredClasses.reduce((sum, c) => sum + c.pred_pass, 0) / filteredClasses.length).toFixed(1);
                const avgViol = (filteredClasses.reduce((sum, c) => sum + c.v_class, 0) / filteredClasses.length).toFixed(1);
                document.getElementById('card-pass-rate').innerText = avgPass + '%';
                document.getElementById('card-discipline-rate').innerText = (100.0 - avgViol).toFixed(1) + '%';
            }}

            renderGroupedClassCards(filteredClasses);
            renderStaffTables(filteredTeachingStaff, filteredSupportStaff);
        }}

        function renderGroupedClassCards(classList) {{
            const container = document.getElementById('grouped-class-cards-container');
            document.getElementById('class-grid-count').innerText = classList.length + ' lớp học';
            if (!container) return;

            const groupsMap = {{}};
            classList.forEach((c) => {{
                if (!groupsMap[c.group_title]) groupsMap[c.group_title] = [];
                groupsMap[c.group_title].push(c);
            }});

            let html = '';
            for (const [gTitle, gClasses] of Object.entries(groupsMap)) {{
                html += `
                <div class="space-y-3.5">
                    <div class="flex items-center gap-2.5 pb-2 border-b border-slate-800">
                        <span class="w-3 h-3 rounded-full bg-indigo-500"></span>
                        <h4 class="text-sm font-extrabold text-slate-100 tracking-wide uppercase">${{gTitle}}</h4>
                        <span class="text-xs text-slate-400 font-mono">(${{gClasses.length}} lớp)</span>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                `;

                gClasses.forEach((c) => {{
                    const borderCls = c.health === 'RED' ? 'border-rose-500/40 bg-gradient-to-br from-rose-500/10 via-slate-900/80 to-slate-900' : (c.health === 'YELLOW' ? 'border-amber-500/40 bg-gradient-to-br from-amber-500/10 via-slate-900/80 to-slate-900' : 'border-slate-800 bg-slate-950/70 hover:border-indigo-500/40');
                    const badgeCls = c.health === 'RED' ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' : (c.health === 'YELLOW' ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30');
                    const passCls = c.pred_pass < 60 ? 'text-rose-400 font-black' : (c.pred_pass < 80 ? 'text-amber-400 font-bold' : 'text-emerald-400 font-bold');

                    html += `
                        <div onclick="openMasterClassDrawerByName('${{c.class_name}}')" class="glass-card p-5 rounded-xl border ${{borderCls}} cursor-pointer transition-all hover:scale-[1.01] flex flex-col justify-between space-y-3.5">
                            <div>
                                <div class="flex items-center justify-between pb-2.5 border-b border-slate-800/80">
                                    <div class="flex items-center gap-2">
                                        <span class="font-black text-slate-100 text-base">${{c.class_name}}</span>
                                        <span class="text-xs text-slate-400 font-medium">(${{c.campus}})</span>
                                    </div>
                                    <span class="px-2.5 py-1 rounded text-xs font-bold border ${{badgeCls}}">${{c.status_text}}</span>
                                </div>

                                <div class="mt-3 grid grid-cols-2 gap-3 text-xs">
                                    <div>
                                        <span class="text-slate-400 font-medium">Môn học:</span>
                                        <div class="font-bold text-indigo-300 truncate text-sm mt-0.5">${{c.subject}}</div>
                                    </div>
                                    <div>
                                        <span class="text-slate-400 font-medium">Giảng dạy:</span>
                                        <div class="font-semibold text-slate-200 truncate mt-0.5">GV: ${{c.gv}}</div>
                                        <div class="text-slate-400 truncate mt-0.5">TG: ${{c.tg}}</div>
                                    </div>
                                </div>

                                <div class="mt-3 p-2.5 rounded-lg bg-slate-950/85 border border-slate-800/80 grid grid-cols-3 text-center text-xs">
                                    <div>
                                        <div class="text-slate-400 font-medium">Dự Báo Đỗ</div>
                                        <div class="text-sm mt-0.5 ${{passCls}}">${{c.pred_pass}}%</div>
                                    </div>
                                    <div>
                                        <div class="text-slate-400 font-medium">Vi Phạm</div>
                                        <div class="text-sm mt-0.5 font-bold ${{c.v_class > 15 ? 'text-rose-400' : 'text-slate-200'}}">${{c.v_class}}%</div>
                                    </div>
                                    <div>
                                        <div class="text-slate-400 font-medium">Care List</div>
                                        <div class="text-sm mt-0.5 font-bold text-amber-300">${{c.care_count}} SV</div>
                                    </div>
                                </div>
                            </div>

                            <div class="pt-2.5 border-t border-slate-800/60 flex items-center justify-between text-xs">
                                <span class="text-slate-300 truncate max-w-[280px]">⚡ ${{c.action_takeaway}}</span>
                                <span class="text-indigo-400 font-bold hover:underline">Chi tiết &rarr;</span>
                            </div>
                        </div>
                    `;
                }});

                html += `
                    </div>
                </div>
                `;
            }}

            container.innerHTML = html;
        }}

        function openMasterClassDrawerByName(className) {{
            const found = EXECUTIVE_DATA.classes.find(c => c.class_name === className);
            if (found) {{
                openMasterClassDrawer(found);
            }}
        }}

        function renderStaffTables(teachingList, supportList) {{
            const tBody = document.getElementById('teaching-staff-tbody');
            if (tBody) {{
                let html = '';
                teachingList.forEach((s) => {{
                    const reportCell = s.rep_days === 0 ? '<span class="text-rose-400 font-bold">0/3 ngày 🚨</span>' : `<span class="text-slate-200">${{s.rep_days}}/3 ngày</span>`;
                    const classesStr = s.classes_assigned && s.classes_assigned.length ? s.classes_assigned.join(', ') : '—';
                    html += `
                    <tr onclick="openMasterStaffDrawerByName('${{s.name}}', true)" class="hover:bg-slate-800/60 cursor-pointer transition text-sm">
                        <td class="py-3 px-4 font-semibold text-slate-100">
                            ${{s.name}}
                        </td>
                        <td class="py-3 px-3 text-slate-300">${{s.campus}} • Rank ${{s.rank}}</td>
                        <td class="py-3 px-3 text-indigo-300 font-mono text-xs">${{classesStr}}</td>
                        <td class="py-3 px-3 text-slate-300">${{s.role}}</td>
                        <td class="py-3 px-3 text-center font-bold text-slate-200">${{s.score_ops}}đ</td>
                        <td class="py-3 px-3 text-center font-medium">${{reportCell}}</td>
                        <td class="py-3 px-3 text-center text-slate-300">${{s.score_acad}}đ</td>
                        <td class="py-3 px-3 text-center text-slate-300">${{s.score_sv}}đ</td>
                        <td class="py-3 px-4 text-center font-black text-emerald-400 text-base">${{s.kpi_total}}đ</td>
                        <td class="py-3 px-4 text-center">
                            <span class="px-2.5 py-1 rounded text-xs font-bold border inline-block whitespace-nowrap ${{s.group_badge}}">${{s.perf_group}}</span>
                        </td>
                    </tr>
                    `;
                }});
                tBody.innerHTML = html;
            }}

            const sBody = document.getElementById('support-staff-tbody');
            if (sBody) {{
                let html = '';
                supportList.forEach((s) => {{
                    const reportCell = s.rep_days === 0 ? '<span class="text-rose-400 font-bold">0/3 ngày 🚨</span>' : `<span class="text-slate-200">${{s.rep_days}}/3 ngày</span>`;
                    html += `
                    <tr onclick="openMasterStaffDrawerByName('${{s.name}}', false)" class="hover:bg-slate-800/60 cursor-pointer transition text-sm">
                        <td class="py-3 px-4 font-semibold text-slate-100">
                            ${{s.name}}
                        </td>
                        <td class="py-3 px-3 text-slate-300">${{s.campus}} • Rank ${{s.rank}}</td>
                        <td class="py-3 px-3 text-indigo-300 font-medium">${{s.dept}}</td>
                        <td class="py-3 px-3 text-slate-300">${{s.role}}</td>
                        <td class="py-3 px-3 text-center font-bold text-slate-200">${{s.score_ops}}đ</td>
                        <td class="py-3 px-3 text-center font-medium">${{reportCell}}</td>
                        <td class="py-3 px-3 text-center text-slate-300">${{s.declared_hours}}h</td>
                        <td class="py-3 px-4 text-center font-black text-indigo-300 text-base">${{s.pmo_kpi}}đ</td>
                        <td class="py-3 px-4 text-center">
                            <span class="px-2.5 py-1 rounded text-xs font-bold border inline-block whitespace-nowrap ${{s.group_badge}}">${{s.perf_group}}</span>
                        </td>
                    </tr>
                    `;
                }});
                sBody.innerHTML = html;
            }}
        }}

        function openMasterStaffDrawerByName(staffName, isTeaching) {{
            const list = isTeaching ? EXECUTIVE_DATA.teaching_staff : EXECUTIVE_DATA.support_staff;
            const found = list.find(s => s.name === staffName);
            if (found) {{
                openMasterStaffDrawer(found, isTeaching);
            }}
        }}

        function openMasterClassDrawer(c) {{
            if (!c) return;
            document.getElementById('master-drawer-title').innerText = c.class_name;
            document.getElementById('master-drawer-icon').innerHTML = '<i class="fas fa-graduation-cap text-indigo-400"></i>';

            let careHtml = '';
            if (c.care_list && c.care_list.length > 0) {{
                careHtml = '<div class="mt-4"><div class="font-bold text-slate-100 text-sm mb-2.5 flex items-center justify-between"><span>👥 Danh sách Học viên Care List (' + c.care_count + ' SV):</span><span class="text-xs text-rose-400 font-semibold">' + c.banned_sv_count + ' SV bị cấm thi</span></div><div class="space-y-2">';
                c.care_list.forEach(s => {{
                    const badgeCls = s.risk_level === 'RED' ? 'bg-rose-500/20 text-rose-300 border-rose-500/40' : 'bg-amber-500/20 text-amber-300 border-amber-500/40';
                    const paradoxTag = (s.is_excellent && s.is_failed_new) ? '<span class="text-xs text-purple-300 font-bold ml-1.5">⚡ Nghịch lý</span>' : '';
                    const gpaVal = typeof s.gpa === 'number' ? s.gpa : 0.0;
                    const attVal = typeof s.att === 'number' ? s.att : 0.0;
                    const hwVal = typeof s.hw === 'number' ? (100 - s.hw).toFixed(1) : '0.0';

                    careHtml += `
                    <div class="p-3.5 rounded-lg bg-slate-950/85 border border-slate-800 flex items-center justify-between text-xs">
                        <div>
                            <div class="font-bold text-slate-100 text-sm">${{s.full_name}} <span class="text-xs text-slate-400 font-normal">(${{s.student_id}})</span>${{paradoxTag}}</div>
                            <div class="text-xs text-slate-300 mt-1">GPA: <strong class="text-slate-100">${{gpaVal}}</strong> • Vắng: <strong class="text-slate-100">${{attVal}}%</strong> • Nợ BT: <strong class="text-slate-100">${{hwVal}}%</strong></div>
                        </div>
                        <span class="text-xs px-2.5 py-1 rounded font-bold border whitespace-nowrap ${{badgeCls}}">${{s.risk_level}}</span>
                    </div>`;
                }});
                careHtml += '</div></div>';
            }} else {{
                careHtml = '<div class="mt-3 p-3.5 rounded-lg bg-emerald-500/10 text-emerald-400 text-center text-xs"><i class="fas fa-check-circle mr-1.5"></i>Không có học viên trong danh sách nguy cơ cao.</div>';
            }}

            document.getElementById('master-drawer-body').innerHTML = `
                <div class="p-4 rounded-xl bg-slate-950/85 border border-slate-800 space-y-2.5 text-xs">
                    <div class="flex justify-between">
                        <span class="text-slate-400 font-medium">Môn học & Cơ sở:</span>
                        <span class="font-bold text-slate-200">${{c.subject}} • ${{c.campus}} (${{c.dept}})</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400 font-medium">Đội ngũ giảng dạy:</span>
                        <span class="font-bold text-slate-200">GV: ${{c.gv}} | TG: ${{c.tg}}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400 font-medium">Dự báo Tỷ lệ Đỗ:</span>
                        <span class="font-black text-base ${{c.pred_pass < 60 ? 'text-rose-400' : 'text-indigo-400'}}">${{c.pred_pass}}%</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400 font-medium">Tỷ lệ Vi phạm Tổng hợp:</span>
                        <span class="font-bold text-rose-400">${{c.v_class}}% (CC: ${{c.cc}}% • BT: ${{c.bt}}% • EL: ${{c.el}}%)</span>
                    </div>
                </div>

                <div class="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-200 text-xs">
                    <div class="font-bold text-sm mb-1"><i class="fas fa-bullhorn mr-1.5"></i>Chỉ đạo điều hành:</div>
                    <div class="leading-relaxed">${{c.action_takeaway}}</div>
                </div>

                ${{careHtml}}
            `;

            document.getElementById('master-drawer-backdrop').classList.remove('opacity-0', 'pointer-events-none');
            document.getElementById('master-slide-drawer').classList.add('open');
        }}

        function openMasterStaffDrawer(s, isTeaching) {{
            if (!s) return;
            document.getElementById('master-drawer-title').innerText = s.name;
            document.getElementById('master-drawer-icon').innerHTML = '<i class="fas fa-user-tie text-emerald-400"></i>';

            let reportStatusHtml = s.rep_days === 0 
                ? '<div class="p-3 rounded-lg bg-rose-500/20 text-rose-300 font-bold text-xs"><i class="fas fa-exclamation-circle mr-1.5"></i>Chưa nộp bất kỳ báo cáo ngày nào (0/3 ngày)! Cần giải trình Ban Giám đốc.</div>'
                : `<div class="text-slate-200 text-xs">Đã nộp: <strong class="text-emerald-400 font-bold">${{s.rep_days}}/3 ngày</strong> (Điểm báo cáo: <strong>${{s.score_log}}đ</strong>)</div>`;

            let detailsHtml = '';
            if (isTeaching) {{
                detailsHtml = `
                <div class="grid grid-cols-2 gap-2.5 text-center text-xs">
                    <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
                        <div class="text-slate-400 font-medium">Kỷ Luật SV (20%)</div>
                        <div class="font-bold text-slate-100 text-sm mt-1">${{s.score_sv}}đ</div>
                    </div>
                    <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
                        <div class="text-slate-400 font-medium">Tác Nghiệp GV (20%)</div>
                        <div class="font-bold text-slate-100 text-sm mt-1">${{s.score_ops}}đ</div>
                    </div>
                    <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
                        <div class="text-slate-400 font-medium">Học Tập SV (30%)</div>
                        <div class="font-bold text-slate-100 text-sm mt-1">${{s.score_acad}}đ</div>
                    </div>
                    <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
                        <div class="text-slate-400 font-medium">Báo Cáo Ngày (30%)</div>
                        <div class="font-bold text-sm mt-1 ${{s.score_log === 0 ? 'text-rose-400' : 'text-slate-100'}}">${{s.score_log}}đ</div>
                    </div>
                </div>

                <div class="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 text-xs">
                    <div class="font-bold text-slate-200 mb-1">Lớp đang phụ trách:</div>
                    <div class="text-slate-300 font-medium">${{s.classes_assigned && s.classes_assigned.length ? s.classes_assigned.join(', ') : 'Đang phân công'}}</div>
                </div>
                `;
            }} else {{
                detailsHtml = `
                <div class="grid grid-cols-2 gap-2.5 text-center text-xs">
                    <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
                        <div class="text-slate-400 font-medium">Báo Cáo PMO (60%)</div>
                        <div class="font-bold text-sm mt-1 ${{s.score_log === 0 ? 'text-rose-400' : 'text-slate-100'}}">${{s.score_log}}đ</div>
                    </div>
                    <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
                        <div class="text-slate-400 font-medium">Kỷ Luật Tác Nghiệp (40%)</div>
                        <div class="font-bold text-slate-100 text-sm mt-1">${{s.score_ops}}đ</div>
                    </div>
                </div>
                `;
            }}

            document.getElementById('master-drawer-body').innerHTML = `
                <div class="p-4 rounded-xl bg-slate-950/85 border border-slate-800 space-y-2.5 text-xs">
                    <div class="flex justify-between">
                        <span class="text-slate-400 font-medium">Vai trò & Rank:</span>
                        <span class="font-bold text-slate-100">${{s.role}} • Rank ${{s.rank}} (${{s.campus}})</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400 font-medium">Khối chuyên môn:</span>
                        <span class="font-bold text-indigo-300">${{s.dept}}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400 font-medium">Điểm Đánh Giá Tổng Hợp:</span>
                        <span class="text-lg font-black text-emerald-400">${{isTeaching ? s.kpi_total : s.pmo_kpi}} đ</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400 font-medium">Xếp loại Năng lực:</span>
                        <span class="text-xs font-bold px-2.5 py-1 rounded border ${{s.group_badge}}">${{s.perf_group}}</span>
                    </div>
                </div>

                ${{detailsHtml}}

                <div class="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800">
                    <div class="font-bold text-slate-200 mb-1.5 text-xs">Tình trạng Nhật ký Báo cáo:</div>
                    ${{reportStatusHtml}}
                </div>
            `;

            document.getElementById('master-drawer-backdrop').classList.remove('opacity-0', 'pointer-events-none');
            document.getElementById('master-slide-drawer').classList.add('open');
        }}

        function closeMasterDrawer() {{
            document.getElementById('master-drawer-backdrop').classList.add('opacity-0', 'pointer-events-none');
            document.getElementById('master-slide-drawer').classList.remove('open');
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            applyExecutiveFilters();
        }});
    </script>

</body>
</html>
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(master_html)

    print(f"✓ Executive Dashboard đã được sinh thành công tại: {output_path}")

if __name__ == "__main__":
    main()

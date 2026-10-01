# -*- coding: utf-8 -*-
import json
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def compute_all():
    print("=== TÍNH TOÁN DỮ LIỆU SO SÁNH & MA TRẬN CÔNG SUẤT ĐA KỲ ===")

    # Nạp 3 kỳ kiểm toán
    with open('data/processed/worklane_audit_week_14_18.json', 'r', encoding='utf-8') as f:
        data_week = json.load(f)

    with open('data/processed/worklane_audit_sept_01_08.json', 'r', encoding='utf-8') as f:
        data_sept = json.load(f)

    with open('data/processed/worklane_audit_august.json', 'r', encoding='utf-8') as f:
        data_aug = json.load(f)

    group_keys = [
        "Khối CNTT Hà Nội",
        "Khối Quản trị Kinh doanh",
        "Khối Ngoại ngữ và KNM",
        "Khối QLCLĐT Hà Nội",
        "Khối CNTT HCM",
        "LMS AI"
    ]

    leader_names = {
        "Khối CNTT Hà Nội": "Hồ Xuân Hùng",
        "Khối Quản trị Kinh doanh": "Hoàng Thị Kim Oanh",
        "Khối Ngoại ngữ và KNM": "Giáp Thị Minh Hằng",
        "Khối QLCLĐT Hà Nội": "Nguyễn Thị Tươi",
        "Khối CNTT HCM": "Nguyễn Bá Minh Đạo",
        "LMS AI": "Trần Minh Cường"
    }

    short_labels = {
        "Khối CNTT Hà Nội": "CNTT Hà Nội",
        "Khối Quản trị Kinh doanh": "Khối QTKD",
        "Khối Ngoại ngữ và KNM": "Ngoại Ngữ & KNM",
        "Khối QLCLĐT Hà Nội": "QLCLĐT",
        "Khối CNTT HCM": "CNTT HCM",
        "LMS AI": "LMS AI"
    }

    # 1. Tính toán Capacity Matrix cho cả 3 kỳ
    capacity_results = {}
    periods_map = {
        "week_14_18": {
            "data": data_week,
            "days": 5,
            "period_name": "Tuần 14/09 - 18/09/2026 (5 ngày - Chuẩn 40h/tuần)"
        },
        "september": {
            "data": data_sept,
            "days": 12,
            "period_name": "Lũy kế Tháng 9 (01/09 - 18/09/2026 - 12 ngày)"
        },
        "august": {
            "data": data_aug,
            "days": 20,
            "period_name": "Tháng 08/2026 (20 ngày làm việc)"
        }
    }

    for p_key, p_cfg in periods_map.items():
        p_data = p_cfg["data"]
        days = p_cfg["days"]
        rows = []

        tot_ns = 0
        tot_declared = 0.0
        tot_std_master = 0.0
        tot_excess = 0.0
        tot_cap_40h = 0.0

        cntt_ns = 0
        cntt_declared = 0.0
        cntt_std_master = 0.0
        cntt_excess = 0.0
        cntt_cap_40h = 0.0

        for g in group_keys:
            staff = [s for s in p_data['staff_details'].values() if s['group'] == g or g in s['group']]
            ns = len(staff)
            tot_ns += ns

            dec = sum(s['total_declared_hours'] for s in staff)
            std = sum(s['total_standard_hours'] for s in staff)
            exc = sum(s['excess_hours'] for s in staff)

            tot_declared += dec
            tot_std_master += std
            tot_excess += exc

            if p_key == "week_14_18":
                cap_40h = sum(s.get('target_hours', 40.0) for s in staff)
            else:
                cap_40h = ns * 40.0

            tot_cap_40h += cap_40h
            cap_period = ns * days * 8.0
            pct_40h = (dec / cap_40h * 100) if cap_40h else 0
            pct_period = (dec / cap_period * 100) if cap_period else 0
            real_eff = (std / dec * 100) if dec else 0
            exc_pct = ((dec - std) / std * 100) if std else 0.0

            is_cntt = 'CNTT' in g
            if is_cntt:
                cntt_ns += ns
                cntt_declared += dec
                cntt_std_master += std
                cntt_excess += exc
                cntt_cap_40h += cap_40h

            rows.append({
                'group': g,
                'short_label': short_labels[g],
                'leader': leader_names[g],
                'staff_count': ns,
                'cap_40h': round(cap_40h, 1),
                'declared_hours': round(dec, 1),
                'pct_40h': round(pct_40h, 1),
                'cap_period': round(cap_period, 1),
                'pct_period': round(pct_period, 1),
                'standard_master': round(std, 1),
                'real_efficiency': round(real_eff, 1),
                'excess_hours': round(exc, 1),
                'excess_pct': round(exc_pct, 1),
                'is_cntt': is_cntt
            })

        cntt_cap_period = cntt_ns * days * 8.0
        cntt_summary = {
            'group': '🔥 TOÀN KHỐI CNTT (HN + HCM)',
            'short_label': 'Toàn Khối CNTT',
            'leader': 'Hồ Xuân Hùng & Nguyễn Bá Minh Đạo',
            'staff_count': cntt_ns,
            'cap_40h': round(cntt_cap_40h, 1),
            'declared_hours': round(cntt_declared, 1),
            'pct_40h': round((cntt_declared / cntt_cap_40h * 100), 1) if cntt_cap_40h else 0,
            'cap_period': round(cntt_cap_period, 1),
            'pct_period': round((cntt_declared / cntt_cap_period * 100), 1) if cntt_cap_period else 0,
            'standard_master': round(cntt_std_master, 1),
            'real_efficiency': round((cntt_std_master / cntt_declared * 100), 1) if cntt_declared else 0,
            'excess_hours': round(cntt_excess, 1),
            'excess_pct': round(((cntt_declared - cntt_std_master) / cntt_std_master * 100), 1) if cntt_std_master else 0,
            'is_highlight': True
        }

        tot_cap_period = tot_ns * days * 8.0
        total_summary = {
            'group': '⭐ TOÀN TRUNG TÂM ĐÀO TẠO',
            'short_label': 'Toàn Viện Đào Tạo',
            'leader': 'Thầy Nguyễn Duy Quang',
            'staff_count': tot_ns,
            'cap_40h': round(tot_cap_40h, 1),
            'declared_hours': round(tot_declared, 1),
            'pct_40h': round((tot_declared / tot_cap_40h * 100), 1) if tot_cap_40h else 0,
            'cap_period': round(tot_cap_period, 1),
            'pct_period': round((tot_declared / tot_cap_period * 100), 1) if tot_cap_period else 0,
            'standard_master': round(tot_std_master, 1),
            'real_efficiency': round((tot_std_master / tot_declared * 100), 1) if tot_declared else 0,
            'excess_hours': round(tot_excess, 1),
            'excess_pct': round(((tot_declared - tot_std_master) / tot_std_master * 100), 1) if tot_std_master else 0,
            'is_highlight': True
        }

        capacity_results[p_key] = {
            'period_name': p_cfg["period_name"],
            'days': days,
            'rows': rows,
            'cntt_summary': cntt_summary,
            'total_summary': total_summary
        }

    # Giữ alias "sept_01_08" trỏ đến "week_14_18" hoặc "september" để tương thích ngược tuyệt đối
    capacity_results["sept_01_08"] = capacity_results["week_14_18"]

    matrix_file = r"data/processed/capacity_matrix_data.json"
    with open(matrix_file, "w", encoding="utf-8") as f:
        json.dump(capacity_results, f, indent=2, ensure_ascii=False)
    print(f"✓ Đã xuất capacity_matrix_data.json thành công vào: {matrix_file}")

    # 2. Tính toán Comparison T8 vs Tuần 14-18 & Tháng 9
    comparison_results = []
    for g in group_keys:
        staff_aug = [s for s in data_aug['staff_details'].values() if s['group'] == g or g in s['group']]
        staff_sept = [s for s in data_sept['staff_details'].values() if s['group'] == g or g in s['group']]
        staff_week = [s for s in data_week['staff_details'].values() if s['group'] == g or g in s['group']]

        count_aug = len(staff_aug)
        count_sept = len(staff_sept)
        count_week = len(staff_week)

        dec_aug = sum(s['total_declared_hours'] for s in staff_aug)
        std_aug = sum(s['total_standard_hours'] for s in staff_aug)
        exc_aug = sum(s['excess_hours'] for s in staff_aug)
        comp_aug = sum(s['compliance_rate'] for s in staff_aug) / count_aug if count_aug else 0
        pct_aug = round(((dec_aug - std_aug) / std_aug * 100), 1) if std_aug else 0.0
        rate_day_aug = round(exc_aug / (20 * count_aug), 2) if count_aug else 0.0

        # Tuần 14-18
        dec_week = sum(s['total_declared_hours'] for s in staff_week)
        std_week = sum(s['total_standard_hours'] for s in staff_week)
        exc_week = sum(s['excess_hours'] for s in staff_week)
        comp_week = sum(s['compliance_rate'] for s in staff_week) / count_week if count_week else 0
        pct_week = round(((dec_week - std_week) / std_week * 100), 1) if std_week else 0.0
        rate_day_week = round(exc_week / (5 * count_week), 2) if count_week else 0.0

        # Tháng 9 lũy kế
        dec_sept = sum(s['total_declared_hours'] for s in staff_sept)
        std_sept = sum(s['total_standard_hours'] for s in staff_sept)
        exc_sept = sum(s['excess_hours'] for s in staff_sept)
        comp_sept = sum(s['compliance_rate'] for s in staff_sept) / count_sept if count_sept else 0
        pct_sept = round(((dec_sept - std_sept) / std_sept * 100), 1) if std_sept else 0.0
        rate_day_sept = round(exc_sept / (12 * count_sept), 2) if count_sept else 0.0

        pct_change = round(pct_week - pct_aug, 1)
        rate_change = round(rate_day_week - rate_day_aug, 2)

        comparison_results.append({
            "group": g,
            "short_label": short_labels[g],
            "leader": leader_names[g],
            "staff_count": count_week,
            "august": {
                "days": 20,
                "declared_hours": round(dec_aug, 1),
                "standard_hours": round(std_aug, 1),
                "excess_hours": round(exc_aug, 1),
                "excess_pct": pct_aug,
                "excess_per_day_staff": rate_day_aug,
                "compliance_rate": round(comp_aug, 1)
            },
            "september": {
                "days": 5,
                "declared_hours": round(dec_week, 1),
                "standard_hours": round(std_week, 1),
                "excess_hours": round(exc_week, 1),
                "excess_pct": pct_week,
                "excess_per_day_staff": rate_day_week,
                "compliance_rate": round(comp_week, 1)
            },
            "delta": {
                "excess_pct_change": pct_change,
                "excess_per_day_change": rate_change,
                "status": "CẢI THIỆN" if pct_change < 0 else "TĂNG DÔI DƯ"
            }
        })

    output_comp = {
        "meta": {
            "title": "So Sánh Hiệu Suất & Giờ Công Worklane: Tháng 08/2026 vs Tuần 14/09 - 18/09/2026",
            "groups_count": len(comparison_results),
            "total_staff": 42
        },
        "comparison": comparison_results
    }

    comp_file = r"data/processed/worklane_comparison_t8_t9.json"
    with open(comp_file, "w", encoding="utf-8") as f:
        json.dump(output_comp, f, indent=2, ensure_ascii=False)
    print(f"✓ Đã xuất worklane_comparison_t8_t9.json thành công vào: {comp_file}")

if __name__ == "__main__":
    compute_all()

import json
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

with open("data/processed/worklane_audit_detailed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

staff = data["staff_details"]

leaders = [
    ("Hồ Xuân Hùng", "hồ xuân hùng", "Khối CNTT Hà Nội", 12),
    ("Hoàng Thị Kim Oanh", "hoàng thị kim oanh", "Khối Quản trị Kinh doanh", 8),
    ("Giáp Thị Minh Hằng", "giáp thị minh hằng", "Khối Ngoại ngữ và KNM", 3),
    ("Nguyễn Thị Tươi", "nguyễn thị tươi", "Khối QLCLĐT Hà Nội", 3),
    ("Nguyễn Bá Minh Đạo", "nguyễn bá minh đạo", "Khối CNTT HCM", 8),
    ("Trần Minh Cường", "trần minh cường", "LMS AI", 2)
]

print("=== KIỂM TOÁN TRÁCH NHIỆM LEADER & TÌNH TRẠNG QUÂN ===")
for l_display, l_key, group_name, expected_subs in leaders:
    l_info = staff.get(l_key, {})
    # Quân dưới quyền:
    subs = [s for k, s in staff.items() if s.get("campus_leader", "").startswith(l_display) and k != l_key]
    
    sub_excess_total = round(sum(s.get("excess_hours", 0) for s in subs), 1)
    sub_review_rank = [s["name"] for s in subs if s.get("recommendation_category") == "CẦN RÀ SOÁT RANK"]
    sub_deduct_hours = [s["name"] for s in subs if s.get("recommendation_category") == "CẢNH BÁO BÙ GIỜ"]
    sub_missing = [s["name"] for s in subs if s.get("recommendation_category") == "CHƯA NỘP BÁO CÁO"]
    
    rep_days = l_info.get("reported_days", 0)
    exp_days = l_info.get("expected_days", 20)
    comp_rate = l_info.get("compliance_rate", 0)
    l_excess = l_info.get("excess_hours", 0)
    
    print(f"\nLeader: {l_display} ({group_name} - Rank {l_info.get('rank', 5)})")
    print(f"  - Quản lý: {len(subs)} quân (Khối: {group_name})")
    print(f"  - Bản thân làm gương: Báo cáo {rep_days}/{exp_days} ngày ({comp_rate}%), Dôi dư: +{l_excess}h")
    print(f"  - Tình trạng quân: Tổng dôi dư: +{sub_excess_total}h")
    print(f"    + Cần rà soát hạ Rank ({len(sub_review_rank)}): {', '.join(sub_review_rank)}")
    print(f"    + Cảnh báo bù giờ ({len(sub_deduct_hours)}): {', '.join(sub_deduct_hours)}")
    print(f"    + Chưa nộp báo cáo ({len(sub_missing)}): {', '.join(sub_missing)}")

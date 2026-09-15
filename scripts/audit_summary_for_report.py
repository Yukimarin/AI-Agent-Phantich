import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/processed/worklane_audit_sept_01_08.json', encoding='utf-8') as f:
    d = json.load(f)

staff = d.get('staff_details', {})
for s in staff.values():
    dec = s.get('total_declared_hours', 0)
    std = s.get('total_standard_hours', 0)
    s['eff'] = round((std / dec * 100), 1) if dec > 0 else 0

sorted_eff = sorted([s for s in staff.values() if s.get('total_declared_hours', 0) > 10], key=lambda x: x['eff'], reverse=True)
print("=== TOP 5 HIỆU SUẤT CAO NHẤT (CHUẨN MASTER) ===")
for s in sorted_eff[:5]:
    print(f"- {s['name']} ({s['group']}): Khai báo {s['total_declared_hours']}h | Chuẩn {s['total_standard_hours']}h | Hiệu suất {s['eff']}%")

print("\n=== TOP 5 DÔI DƯ NHẤT / KHAI BÁO PHÁT SINH CAO ===")
sorted_excess = sorted(staff.values(), key=lambda x: x.get('excess_hours', 0), reverse=True)
for s in sorted_excess[:5]:
    print(f"- {s['name']} ({s['group']}): Khai báo {s['total_declared_hours']}h | Chuẩn {s['total_standard_hours']}h | Dôi dư +{s.get('excess_hours', 0)}h | Hiệu suất {s['eff']}% | Phân loại: {s.get('recommendation_category')}")


print("\n=== PHÂN BỔ NHÂN SỰ THEO KHỐI & HIỆU SUẤT KHỐI ===")
with open('data/processed/capacity_matrix_data.json', encoding='utf-8') as f:
    cap = json.load(f)['september']

for r in cap['rows']:
    print(f"* {r['group']}: {r['staff_count']} NS | Định mức 40h: {r['cap_40h']}h | Khai báo: {r['declared_hours']}h ({r['pct_40h']}%) | Chuẩn việc: {r['standard_master']}h | Hiệu suất thực: {r['real_efficiency']}% | Dôi dư: +{r['excess_hours']}h")

print(f"\n* TOÀN KHỐI CNTT: {cap['cntt_summary']['staff_count']} NS | Định mức 40h: {cap['cntt_summary']['cap_40h']}h | Khai báo: {cap['cntt_summary']['declared_hours']}h ({cap['cntt_summary']['pct_40h']}%) | Chuẩn việc: {cap['cntt_summary']['standard_master']}h | Hiệu suất: {cap['cntt_summary']['real_efficiency']}%")
print(f"* TOÀN TRUNG TÂM: {cap['total_summary']['staff_count']} NS | Định mức 40h: {cap['total_summary']['cap_40h']}h | Khai báo: {cap['total_summary']['declared_hours']}h ({cap['total_summary']['pct_40h']}%) | Chuẩn việc: {cap['total_summary']['standard_master']}h | Hiệu suất: {cap['total_summary']['real_efficiency']}%")

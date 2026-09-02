import sys
import os
import json
import openpyxl
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

# 1. Load KS24 stats from scratch/ks24_stats.json
with open("scratch/ks24_stats.json", "r", encoding="utf-8") as f:
    ks24_json = json.load(f)

ks24_summary = ks24_json["summary"]
ks24_students = ks24_json["students"]

ks24_reg = ks24_summary["total_students"]
ks24_active = [s for s in ks24_students if s["final"] > 0]
ks24_took = len(ks24_active)
ks24_absent = ks24_reg - ks24_took
ks24_avg = ks24_summary["avg_score"]
ks24_levels = ks24_summary["level_counts"]
ks24_ready = ks24_levels["level_2"] + ks24_levels["level_3"]
ks24_ready_pct = round(ks24_ready / ks24_reg * 100, 1)

ks24_hn = [s for s in ks24_students if "HN" in s["branch"]]
ks24_hcm = [s for s in ks24_students if "HCM" in s["branch"]]

ks24_hn_took = len([s for s in ks24_hn if s["final"] > 0])
ks24_hn_avg = round(sum(s["score"] for s in ks24_hn if s["final"] > 0) / ks24_hn_took, 2) if ks24_hn_took else 0
ks24_hn_ready = len([s for s in ks24_hn if s["readiness_level"] in [2, 3]])

ks24_hcm_took = len([s for s in ks24_hcm if s["final"] > 0])
ks24_hcm_avg = round(sum(s["score"] for s in ks24_hcm if s["final"] > 0) / ks24_hcm_took, 2) if ks24_hcm_took else 0
ks24_hcm_ready = len([s for s in ks24_hcm if s["readiness_level"] in [2, 3]])

print("=== KS24 METRICS ===")
print(f"Registered: {ks24_reg}, Took: {ks24_took}, Absent: {ks24_absent} ({round(ks24_absent/ks24_reg*100,1)}%)")
print(f"Avg Score: {ks24_avg}/10, Ready (L2+L3): {ks24_ready} ({ks24_ready_pct}%)")
print(f"Levels: L0={ks24_levels['level_0']}, L1={ks24_levels['level_1']}, L2={ks24_levels['level_2']}, L3={ks24_levels['level_3']}")
print(f"HN: Reg={len(ks24_hn)}, Took={ks24_hn_took}, Avg={ks24_hn_avg}, Ready={ks24_hn_ready}")
print(f"HCM: Reg={len(ks24_hcm)}, Took={ks24_hcm_took}, Avg={ks24_hcm_avg}, Ready={ks24_hcm_ready}")

# 2. Compute KS25 stats directly from inputs/Danh sách thi ĐGNL.xlsx
wb = openpyxl.load_workbook("inputs/Danh sách thi ĐGNL.xlsx", data_only=True)
sh = wb["Danh sách ĐGNL CNTT"]
headers = [c.value for c in sh[1]]
c_class = headers.index("Mã lớp hiện tại")
c_name = headers.index("Họ và tên học viên")
c_tn = headers.index("Trắc nghiệm (Đ1)")
c_th = headers.index("Thực hành (Đ1)")
c_p1 = headers.index("Điểm danh P1")
c_p2 = headers.index("Điểm danh P2")
c_final = headers.index("Điểm final (Đ1)")
c_cs = headers.index("Cơ sở đào tạo")
c_bs_dm = headers.index("Điểm danh BS") if "Điểm danh BS" in headers else -1

ks25_list = []
for r in range(2, sh.max_row+1):
    cname = sh.cell(row=r, column=c_class+1).value
    if not cname or "CNTT" not in str(cname) or not ("KS25" in str(cname) or "K25" in str(cname)):
        continue
    name = sh.cell(row=r, column=c_name+1).value
    if not name: continue
    
    cs = str(sh.cell(row=r, column=c_cs+1).value or "").strip()
    is_hn = "HN" in str(cname) or "Hà Nội" in cs
    
    p1 = sh.cell(row=r, column=c_p1+1).value
    p2 = sh.cell(row=r, column=c_p2+1).value
    tn = sh.cell(row=r, column=c_tn+1).value
    th = sh.cell(row=r, column=c_th+1).value
    bs = sh.cell(row=r, column=c_bs_dm+1).value if c_bs_dm != -1 else None
    
    is_absent = False
    if (tn is not None and float(tn) > 0) or (th is not None and float(th) > 0) or (str(bs) in ["1", "1.0"]):
        is_absent = False
    elif p1 == "Vắng" or p2 == "Vắng" or str(p1) in ["0", "0.0"] or str(p2) in ["0", "0.0"]:
        is_absent = True
    elif (p1 is None or p1 == "") and (p2 is None or p2 == "") and (tn is None or tn == 0) and (th is None or th == 0):
        is_absent = True
        
    tn_val = float(tn) if tn is not None else 0.0
    th_val = float(th) if th is not None else 0.0
    final_val = tn_val * 0.3 + th_val * 0.7
    final_10 = round(final_val / 10.0, 1)
    if final_10 > 10.0: final_10 = 10.0
    
    # Readiness Level for KS25:
    # L3: final_10 >= 8.0 & th >= 70
    # L2: final_10 >= 6.0 & th >= 50
    # L1: final_10 >= 4.0 & th >= 30
    # L0: else
    if is_absent:
        level = 0
    elif final_10 >= 8.0 and th_val >= 70:
        level = 3
    elif final_10 >= 6.0 and th_val >= 50:
        level = 2
    elif final_10 >= 4.0 and th_val >= 30:
        level = 1
    else:
        level = 0
        
    ks25_list.append({
        "name": name,
        "class": cname,
        "is_hn": is_hn,
        "is_absent": is_absent,
        "tn": tn_val,
        "th": th_val,
        "final": final_val,
        "final_10": final_10,
        "level": level
    })

ks25_reg = len(ks25_list)
ks25_took = len([s for s in ks25_list if not s["is_absent"]])
ks25_absent = ks25_reg - ks25_took
ks25_took_active = [s for s in ks25_list if not s["is_absent"]]
ks25_avg = round(sum(s["final_10"] for s in ks25_took_active) / ks25_took, 2) if ks25_took else 0
ks25_l0 = len([s for s in ks25_list if s["level"] == 0])
ks25_l1 = len([s for s in ks25_list if s["level"] == 1])
ks25_l2 = len([s for s in ks25_list if s["level"] == 2])
ks25_l3 = len([s for s in ks25_list if s["level"] == 3])
ks25_ready = ks25_l2 + ks25_l3
ks25_ready_pct = round(ks25_ready / ks25_reg * 100, 1)

ks25_hn = [s for s in ks25_list if s["is_hn"]]
ks25_hcm = [s for s in ks25_list if not s["is_hn"]]

ks25_hn_took = len([s for s in ks25_hn if not s["is_absent"]])
ks25_hn_avg = round(sum(s["final_10"] for s in ks25_hn if not s["is_absent"]) / ks25_hn_took, 2) if ks25_hn_took else 0
ks25_hn_ready = len([s for s in ks25_hn if s["level"] in [2, 3]])

ks25_hcm_took = len([s for s in ks25_hcm if not s["is_absent"]])
ks25_hcm_avg = round(sum(s["final_10"] for s in ks25_hcm if not s["is_absent"]) / ks25_hcm_took, 2) if ks25_hcm_took else 0
ks25_hcm_ready = len([s for s in ks25_hcm if s["level"] in [2, 3]])

print("\n=== KS25 METRICS ===")
print(f"Registered: {ks25_reg}, Took: {ks25_took}, Absent: {ks25_absent} ({round(ks25_absent/ks25_reg*100,1)}%)")
print(f"Avg Score: {ks25_avg}/10, Ready (L2+L3): {ks25_ready} ({ks25_ready_pct}%)")
print(f"Levels: L0={ks25_l0}, L1={ks25_l1}, L2={ks25_l2}, L3={ks25_l3}")
print(f"HN: Reg={len(ks25_hn)}, Took={ks25_hn_took}, Avg={ks25_hn_avg}, Ready={ks25_hn_ready}")
print(f"HCM: Reg={len(ks25_hcm)}, Took={ks25_hcm_took}, Avg={ks25_hcm_avg}, Ready={ks25_hcm_ready}")

# 3. Consolidated All CNTT Metrics
total_reg = ks24_reg + ks25_reg
total_took = ks24_took + ks25_took
total_absent = total_reg - total_took
total_absent_pct = round(total_absent / total_reg * 100, 1)

total_ready = ks24_ready + ks25_ready
total_ready_pct = round(total_ready / total_reg * 100, 1)

total_l0 = ks24_levels["level_0"] + ks25_l0
total_l0_pct = round(total_l0 / total_reg * 100, 1)

print("\n=== CONSOLIDATED ALL CNTT METRICS ===")
print(f"Total Registered: {total_reg}")
print(f"Total Took Exam: {total_took} ({round(total_took/total_reg*100,1)}%)")
print(f"Total Absent: {total_absent} ({total_absent_pct}%)")
print(f"Total Ready (L2+L3): {total_ready} ({total_ready_pct}%)")
print(f"Total Level 0: {total_l0} ({total_l0_pct}%)")
print(f"Total Level 1: {ks24_levels['level_1'] + ks25_l1}")
print(f"Total Level 2: {ks24_levels['level_2'] + ks25_l2}")
print(f"Total Level 3: {ks24_levels['level_3'] + ks25_l3}")

metrics = {
    "ks24": {
        "reg": ks24_reg, "took": ks24_took, "absent": ks24_absent, "absent_pct": round(ks24_absent/ks24_reg*100,1),
        "avg": ks24_avg, "ready": ks24_ready, "ready_pct": ks24_ready_pct,
        "l0": ks24_levels["level_0"], "l1": ks24_levels["level_1"], "l2": ks24_levels["level_2"], "l3": ks24_levels["level_3"],
        "hn": {"reg": len(ks24_hn), "took": ks24_hn_took, "avg": ks24_hn_avg, "ready": ks24_hn_ready, "ready_pct": round(ks24_hn_ready/len(ks24_hn)*100,1) if len(ks24_hn) else 0},
        "hcm": {"reg": len(ks24_hcm), "took": ks24_hcm_took, "avg": ks24_hcm_avg, "ready": ks24_hcm_ready, "ready_pct": round(ks24_hcm_ready/len(ks24_hcm)*100,1) if len(ks24_hcm) else 0}
    },
    "ks25": {
        "reg": ks25_reg, "took": ks25_took, "absent": ks25_absent, "absent_pct": round(ks25_absent/ks25_reg*100,1),
        "avg": ks25_avg, "ready": ks25_ready, "ready_pct": ks25_ready_pct,
        "l0": ks25_l0, "l1": ks25_l1, "l2": ks25_l2, "l3": ks25_l3,
        "hn": {"reg": len(ks25_hn), "took": ks25_hn_took, "avg": ks25_hn_avg, "ready": ks25_hn_ready, "ready_pct": round(ks25_hn_ready/len(ks25_hn)*100,1) if len(ks25_hn) else 0},
        "hcm": {"reg": len(ks25_hcm), "took": ks25_hcm_took, "avg": ks25_hcm_avg, "ready": ks25_hcm_ready, "ready_pct": round(ks25_hcm_ready/len(ks25_hcm)*100,1) if len(ks25_hcm) else 0}
    },
    "total": {
        "reg": total_reg, "took": total_took, "took_pct": round(total_took/total_reg*100,1),
        "absent": total_absent, "absent_pct": total_absent_pct,
        "ready": total_ready, "ready_pct": total_ready_pct,
        "l0": total_l0, "l0_pct": total_l0_pct,
        "l1": ks24_levels["level_1"] + ks25_l1,
        "l2": ks24_levels["level_2"] + ks25_l2,
        "l3": ks24_levels["level_3"] + ks25_l3
    }
}

with open("scratch/consolidated_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, ensure_ascii=False, indent=2)

print("Saved consolidated metrics in scratch/consolidated_metrics.json")

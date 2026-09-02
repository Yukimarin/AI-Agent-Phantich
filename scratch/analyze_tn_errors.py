import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

f1 = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"
f2 = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx"

df1 = pd.read_excel(f1, sheet_name="Danh sách ĐGNL CNTT")
df2 = pd.read_excel(f2, sheet_name="Danh sách ĐGNL CNTT")

print("=== PHÂN TÍCH ĐIỂM TRẮC NGHIỆM TRÊN SHEET CNTT ===")
# Count non-null, 0, >0 Trắc nghiệm in old vs new
tn1 = df1["Trắc nghiệm (Đ1)"].dropna()
tn2 = df2["Trắc nghiệm (Đ1)"].dropna()
print(f"File cũ: Có {len(tn1)} bạn có điểm trắc nghiệm (trong đó { (tn1 == 0).sum() } bạn 0 điểm, { (tn1 > 0).sum() } bạn >0 điểm)")
print(f"File mới: Có {len(tn2)} bạn có điểm trắc nghiệm (trong đó { (tn2 == 0).sum() } bạn 0 điểm, { (tn2 > 0).sum() } bạn >0 điểm)")

# Merge to see specific changes
m = pd.merge(df1[["SourceID", "Họ và tên học viên", "Mã lớp hiện tại", "Ca thi", "Trắc nghiệm (Đ1)", "Thực hành (Đ1)", "Điểm final (Đ1)", "Ghi chú", "Biên bản"]],
             df2[["SourceID", "Họ và tên học viên", "Mã lớp hiện tại", "Ca thi", "Trắc nghiệm (Đ1)", "Thực hành (Đ1)", "Điểm final (Đ1)", "Ngày thi", "Điểm danh BS", "HĐ thi BS L1", "Ghi chú L1"]],
             on="SourceID", suffixes=("_cũ", "_mới"))

# Students whose TN changed from NaN or 0 to >0
tn_updated = m[(m["Trắc nghiệm (Đ1)_cũ"].isna() | (m["Trắc nghiệm (Đ1)_cũ"] == 0)) & (m["Trắc nghiệm (Đ1)_mới"] > 0)]
print(f"\nSố lượng SV được thêm/cập nhật điểm trắc nghiệm từ (trống hoặc 0) thành (>0): {len(tn_updated)}")

# Check by Class / Cohort
print("\nPhân bố các bạn được cập nhật điểm trắc nghiệm theo Lớp:")
print(tn_updated["Mã lớp hiện tại_mới"].value_counts())

# Check ca thi cũ của các bạn này
print("\nPhân bố theo Ca thi cũ:")
print(tn_updated["Ca thi_cũ"].value_counts())

# Check how many took thi bổ sung
print(f"\nTrong số {len(tn_updated)} bạn có điểm trắc nghiệm mới:")
print(f"- Số bạn có Ngày thi chuyển sang 22/08/2026: {(tn_updated['Ngày thi'] == '22/08/2026').sum()}")
print(f"- Số bạn có Điểm danh thi bổ sung (Điểm danh BS = 1): {(tn_updated['Điểm danh BS'] == 1).sum()}")
print(f"- Số bạn có HĐ thi BS: {tn_updated['HĐ thi BS L1'].notna().sum()}")

# Print samples of students who had system errors in round 1
print("\n=== MẪU CÁC BẠN TỪNG BỊ LỖI HỆ THỐNG / BIÊN BẢN ĐỢT 1 VÀ TÌNH TRẠNG HIỆN TẠI ===")
error_keywords = ["lỗi", "không nộp", "mất bài", "trắng", "hệ thống", "không có đề", "sập", "error", "không load", "simple care", "out", "thi bổ sung", "hoãn thi"]
m["has_error_flag"] = m.apply(lambda r: any(kw in (str(r["Ghi chú"]) + " " + str(r["Biên bản"])).lower() for kw in error_keywords), axis=1)

error_students = m[m["has_error_flag"]]
print(f"Tổng số SV có ghi chú lỗi/biên bản ở Đợt 1: {len(error_students)}")

for _, r in error_students.head(15).iterrows():
    print(f"- {r['Họ và tên học viên_mới']} ({r['Mã lớp hiện tại_mới']}):")
    print(f"    Ghi chú cũ: '{r['Ghi chú']}' | BB cũ: '{r['Biên bản']}'")
    print(f"    TN cũ: {r['Trắc nghiệm (Đ1)_cũ']} ➔ TN mới: {r['Trắc nghiệm (Đ1)_mới']}")
    print(f"    TH cũ: {r['Thực hành (Đ1)_cũ']} ➔ TH mới: {r['Thực hành (Đ1)_mới']}")
    print(f"    Final cũ: {r['Điểm final (Đ1)_cũ']} ➔ Final mới: {r['Điểm final (Đ1)_mới']}")
    print(f"    Thi BS 22/08: Ngày={r['Ngày thi']} | Điểm danh BS={r['Điểm danh BS']} | HĐ BS={r['HĐ thi BS L1']}")
    print("-" * 50)


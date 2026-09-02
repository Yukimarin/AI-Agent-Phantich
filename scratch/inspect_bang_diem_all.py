import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

excel_path = "inputs/Danh sách thi ĐGNL.xlsx"
df_bd = pd.read_excel(excel_path, sheet_name="Bảng điểm (Đợt 1)")

print("=== BẢNG ĐIỂM (ĐỢT 1) COLUMNS ===")
print(list(df_bd.columns))
print(f"Shape: {df_bd.shape}")
print(df_bd[["Họ và tên học viên", "Mã lớp hiện tại", "Đ1_Sản phẩm_CNTT", "Đ1_Vấn đáp_CNTT", "Đ1_Thực hành_CNTT", "Đ1_Trắc nghiệm_CNTT", "Đ1_Điểm CNTT (Final)", "Đ1_Điểm QTKD (Final)", "Đ1_Reading", "Đ1_Listening", "Đ1_Tiếng Anh (Final)", "Đ1_Kỹ năng mềm (Final)"]].head(10))


import pandas as pd
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    tkb_path = r"C:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\data\1. Thời khóa biểu tổng .xlsx"
    if not os.path.exists(tkb_path):
        print(f"Error: File {tkb_path} not found.")
        sys.exit(1)
        
    print("Đang tìm kiếm các lớp Python Web khóa KS25 trong thời khóa biểu...")
    xls = pd.ExcelFile(tkb_path)
    
    # Quét cả hai sheet Hà Nội và Hồ Chí Minh
    for sheet_name in xls.sheet_names:
        if "Hà Nội" in sheet_name or "TKB Hà Nội" in sheet_name or "1.1" in sheet_name:
            df = pd.read_excel(tkb_path, sheet_name=sheet_name)
            # Lọc theo môn học hoặc mã môn học
            # Môn học: 'Python Web' hoặc mã môn chứa 'IT215' hoặc 'IT215' trong cột Môn học / Môn học
            # Lớp đào tạo: chứa 'KS25'
            
            # Chuẩn hóa cột
            df.columns = [str(c).strip() for c in df.columns]
            
            # Tìm các dòng thỏa mãn môn học Python Web / IT215 và Khóa KS25
            class_col = 'Lớp đào tạo' if 'Lớp đào tạo' in df.columns else 'Lớp'
            subject_col = 'Môn học' if 'Môn học' in df.columns else 'Môn'
            gv_lt_col = 'Giảng viên LT' if 'Giảng viên LT' in df.columns else 'Giảng viên'
            gv_th_col = 'Giảng viên TH' if 'Giảng viên TH' in df.columns else 'Trợ giảng'
            date_col = 'Ngày đào tạo' if 'Ngày đào tạo' in df.columns else 'Ngày'
            
            # Lọc
            mask = df[subject_col].astype(str).str.contains("Python Web|IT215|Python_Web", case=False, na=False)
            filtered_df = df[mask]
            
            if not filtered_df.empty:
                print(f"\n=== Kết quả tại sheet: {sheet_name} ===")
                print(f"Tìm thấy {filtered_df.shape[0]} ca học môn Python Web / IT215.")
                
                # In các tổ hợp Lớp - Giảng viên LT - Giảng viên TH
                unique_combinations = filtered_df[[class_col, gv_lt_col, gv_th_col]].drop_duplicates()
                print("Các tổ hợp Lớp - GV - TG phụ trách:")
                print(unique_combinations.to_string(index=False))
                
                # In thông tin 5 ca học gần nhất hoặc đầu tiên
                print("\nChi tiết 5 ca học đầu tiên:")
                cols_to_print = [date_col, class_col, subject_col, 'Ca đào tạo', gv_lt_col, gv_th_col, 'Tiến độ đào tạo']
                cols_to_print = [c for c in cols_to_print if c in filtered_df.columns]
                print(filtered_df[cols_to_print].head(5).fillna("").to_string(index=False))
            else:
                print(f"\nKhông tìm thấy dữ liệu Python Web ở sheet: {sheet_name}")

if __name__ == "__main__":
    main()

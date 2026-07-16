import pandas as pd
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    excel_path = r"C:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\data\1. Thời khóa biểu tổng .xlsx"
    if not os.path.exists(excel_path):
        print(f"Error: File {excel_path} not found.")
        sys.exit(1)
        
    print(f"Đang đọc tệp Excel: {os.path.basename(excel_path)}")
    try:
        xls = pd.ExcelFile(excel_path)
        print(f"Đọc tệp thành công! Các sheet tìm thấy: {xls.sheet_names}")
        
        for sheet in xls.sheet_names[:3]: # Kiểm tra tối đa 3 sheet đầu
            print(f"\n--- Sheet: {sheet} ---")
            df = pd.read_excel(excel_path, sheet_name=sheet)
            print(f"Kích thước: {df.shape[0]} dòng, {df.shape[1]} cột")
            print("Cột tiêu đề tìm thấy:")
            print(list(df.columns))
            print("5 dòng dữ liệu đầu tiên:")
            # Thay thế giá trị null để hiển thị gọn gàng
            print(df.head(5).fillna("").to_string(index=False))
    except Exception as e:
        print(f"Error khi đọc tệp Excel: {e}")

if __name__ == "__main__":
    main()

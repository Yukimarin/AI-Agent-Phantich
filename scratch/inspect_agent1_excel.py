import pandas as pd
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    excel_path = r"c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\data\PTIT_Chiso.xlsx"
    if not os.path.exists(excel_path):
        print(f"Error: File {excel_path} not found.")
        sys.exit(1)
        
    print(f"Đang đọc tệp Excel Agent 1: {os.path.basename(excel_path)}")
    xls = pd.ExcelFile(excel_path)
    print(f"Các sheet tìm thấy: {xls.sheet_names}")
    
    # Thường thông tin GV/TG nằm ở sheet "KPI" hoặc sheet "KS25"
    for sheet in xls.sheet_names:
        if "KS25" in sheet or "KPI" in sheet or "Giảng viên" in sheet or "Lớp" in sheet:
            print(f"\n--- Xem 5 dòng đầu Sheet: {sheet} ---")
            df = pd.read_excel(excel_path, sheet_name=sheet)
            df.columns = [str(c).strip() for c in df.columns]
            print("Cột tìm thấy:", list(df.columns))
            print(df.head(5).fillna("").to_string(index=False))

if __name__ == "__main__":
    main()

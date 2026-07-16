import pandas as pd
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    excel_path = r"c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\data\Khung_Phat_Khenthuong_ĐT_T62026 (2).xlsx"
    output_md_path = r"c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\data\Khung_Phat_Khenthuong_ĐT_T62026.md"
    
    if not os.path.exists(excel_path):
        print(f"Error: File {excel_path} not found.")
        sys.exit(1)
        
    print("Đang đọc tệp Excel...")
    xls = pd.ExcelFile(excel_path)
    print(f"Các sheet tìm thấy: {xls.sheet_names}")
    
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write("# KHUNG PHẠT VÀ KHEN THƯỞNG ĐÀO TẠO THÁNG 06/2026\n\n")
        f.write(f"*Được chuyển đổi tự động từ tệp: `{os.path.basename(excel_path)}`*\n\n")
        
        for sheet_name in xls.sheet_names:
            f.write(f"## Sheet: {sheet_name}\n\n")
            # Đọc không giới hạn kiểu dữ liệu để giữ nguyên format
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            # Chuyển đổi DataFrame sang Markdown table
            md_table = df.to_markdown(index=False)
            f.write(md_table)
            f.write("\n\n---\n\n")
            
    print(f"Hoàn thành chuyển đổi! Tệp Markdown đã được lưu tại: {output_md_path}")

if __name__ == "__main__":
    main()

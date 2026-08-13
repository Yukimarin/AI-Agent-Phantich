import os
import sys
import openpyxl
import shutil

sys.stdout.reconfigure(encoding='utf-8')

def sanitize_excel(file_path):
    print(f"DataSanitizer: Bắt đầu làm sạch dữ liệu tại {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file {file_path}")
        return False
        
    # Tạo bản backup trước khi xử lý
    backup_path = file_path.replace(".xlsx", "_raw.xlsx")
    if not os.path.exists(backup_path):
        shutil.copy2(file_path, backup_path)
        print(f"DataSanitizer: Đã backup file gốc sang {backup_path}")
    
    try:
        wb = openpyxl.load_workbook(file_path)
        
        # Lặp qua tất cả các sheet
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            
            # Chuẩn hóa headers và data
            for row in range(1, sheet.max_row + 1):
                for col in range(1, sheet.max_column + 1):
                    cell = sheet.cell(row=row, column=col)
                    
                    if isinstance(cell.value, str):
                        # Cắt khoảng trắng thừa ở chuỗi, đặc biệt là tên GV
                        cell.value = cell.value.strip()
                    elif cell.value is None:
                        # Với các ô dữ liệu vi phạm (từ cột 4 trở đi) nếu None thì gán bằng 0
                        # Tuy nhiên không gán vô tội vạ, chỉ gán ở các hàng có data
                        # Ở đây tạm thời để nguyên None nếu là header, nhưng nếu là row data thì cần suy xét
                        # Tốt nhất là các script phân tích sẽ tự handle None to 0, nhưng ta có thể hỗ trợ chuẩn hóa
                        pass
                        
        wb.save(file_path)
        wb.close()
        print(f"DataSanitizer: Làm sạch thành công file {file_path}")
        return True
    except Exception as e:
        print(f"DataSanitizer Lỗi: {str(e)}")
        return False

def sync_from_backup():
    import json
    backup_path = r"C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx"
    target_path = "data/inputs/PTIT_Chiso.xlsx"
    sync_meta_path = "data/processed/last_sync.json"
    
    if os.path.exists(backup_path):
        print(f"DataSanitizer: Tìm thấy file backup tại {backup_path}")
        backup_mtime = os.path.getmtime(backup_path)
        
        should_copy = False
        if not os.path.exists(target_path):
            should_copy = True
        else:
            last_sync_time = 0.0
            if os.path.exists(sync_meta_path):
                try:
                    with open(sync_meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                        last_sync_time = meta.get("backup_mtime", 0.0)
                except Exception:
                    pass
            
            # Nếu mtime khác với lần đồng bộ trước, chứng tỏ file backup đã được người dùng chỉnh sửa
            if abs(backup_mtime - last_sync_time) > 0.01:
                should_copy = True
                
        if should_copy:
            try:
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                shutil.copy2(backup_path, target_path)
                print(f"✓ DataSanitizer: Đã tự động đồng bộ file Excel mới từ Backup vào dự án.")
                
                # Lưu mtime đã đồng bộ
                os.makedirs(os.path.dirname(sync_meta_path), exist_ok=True)
                with open(sync_meta_path, "w", encoding="utf-8") as f:
                    json.dump({"backup_mtime": backup_mtime}, f)
            except Exception as e:
                print(f"Warning: Không thể copy file từ Backup: {e}")
        else:
            print("DataSanitizer: File Excel trong dự án đã đồng bộ và là mới nhất.")
    else:
        print(f"DataSanitizer: Không tìm thấy file backup tại {backup_path}. Sử dụng file hiện tại trong dự án.")

def main():
    print("=========================================")
    print("KHỞI CHẠY DATA SANITIZER (HARNESS LAYER)")
    print("=========================================")
    
    # 0. Làm sạch trực tiếp file nguồn ngoài Desktop Backup trước (nếu có)
    backup_path = r"C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx"
    if os.path.exists(backup_path):
        print(f"DataSanitizer: Tiến hành làm sạch file nguồn ngoài Desktop: {backup_path}")
        sanitize_excel(backup_path)
        
    # 1. Đồng bộ hóa dữ liệu từ thư mục Backup ngoài dự án
    sync_from_backup()
    
    target_file = "data/inputs/PTIT_Chiso.xlsx"
    success = sanitize_excel(target_file)
    
    if success:
        print("DataSanitizer: Đã sẵn sàng môi trường dữ liệu sạch!")
        sys.exit(0)
    else:
        print("DataSanitizer: Gặp sự cố làm sạch dữ liệu. Các Agent phía sau có thể gặp lỗi rác dữ liệu.")
        sys.exit(1)

if __name__ == "__main__":
    main()

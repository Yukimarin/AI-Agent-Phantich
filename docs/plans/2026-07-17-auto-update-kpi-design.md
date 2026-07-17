# Thiết kế Hệ thống Tự động hóa Cập nhật Dữ liệu và KPI Đào tạo

**Ngày tạo**: 2026-07-17  
**Trạng thái**: Đã phê duyệt  

## 1. Mục tiêu
Tự động hóa hoàn toàn việc phát hiện tệp Excel chỉ số đào tạo thay đổi ở thư mục Backup, cập nhật dữ liệu, khởi chạy MySQL 9.7 (cổng 3307), thực thi pipeline tính toán KPI của 5 Agent, cập nhật xếp loại năng lực mới nhất, upload Catbox và đẩy báo cáo lên GitHub.

## 2. Các thành phần hệ thống

### 2.1 Script PowerShell chính (`scratch/auto_update_kpi.ps1`)
Một script PowerShell thực hiện các bước sau:
1. **Kiểm tra file Excel**: So sánh thời gian sửa đổi (`LastWriteTime`) giữa file backup `C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx` và file dự án `data/PTIT_Chiso.xlsx`.
2. **Sao lưu & Sao chép**: Sao lưu file cũ thành `data/PTIT_Chiso_backup.xlsx`, sao chép file mới đè lên `data/PTIT_Chiso.xlsx`.
3. **Quản lý MySQL 3307**: Kiểm tra cổng 3307, nếu chưa mở thì khởi chạy `mysqld.exe` ngầm chỉ định `datadir` và tắt X Plugin (`--mysqlx=OFF`).
4. **Thực thi Pipeline**: Chạy `run_pipeline.py` và `generate_kpi_ranking.py` thông qua `uv run` với các dependencies tương ứng.
5. **Upload & Đồng bộ Git**: Thực hiện upload dashboard và `git push` để cập nhật báo cáo online.
6. **Ghi nhật ký**: Ghi lại lịch sử thực thi và lỗi (nếu có) vào `data/auto_update.log`.

### 2.2 Đăng ký Windows Task Scheduler
- Tên Task: `PTIT_KPI_Auto_Update`
- Lịch trình: Chạy mỗi 1 giờ hoặc chạy mỗi ngày lúc 7:00 AM và khi người dùng log in vào Windows.
- Lệnh chạy: Kích hoạt PowerShell không hiển thị cửa sổ để chạy script `scratch/auto_update_kpi.ps1`.

## 3. Xử lý ngoại lệ và an toàn dữ liệu
- Nếu file backup bị hỏng hoặc lỗi copy, script sẽ dừng và ghi lỗi vào file log.
- Nếu MySQL 3307 bị crash khi khởi động, script sẽ thử lại hoặc dừng chạy để tránh làm hỏng database.
- Sử dụng các file backup tạm thời (`_backup.xlsx`) để phục hồi nếu quá trình ghi đè bị lỗi.

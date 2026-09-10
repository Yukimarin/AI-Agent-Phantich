@echo off
chcp 65001 > nul
title Kiểm Tra Trạng Thái Dịch Vụ Đồng Bộ Tự Động (PMO AI Agent)
color 0B

echo ===============================================================================
echo     TRẠNG THÁI DỊCH VỤ TỰ ĐỘNG CẬP NHẬT CHỈ SỐ ĐÀO TẠO (AUTO-WATCHER)
echo ===============================================================================
echo.

uv run python -c "import os, subprocess; pid_file = 'data/processed/watcher.pid'; (print('✓ Tiến trình đang chạy với PID: ' + open(pid_file).read().strip()) if os.path.exists(pid_file) and open(pid_file).read().strip() in subprocess.check_output('tasklist /FO CSV /NH', shell=True).decode('utf-8', errors='ignore') else print('⚠️ Dịch vụ chưa chạy hoặc đã dừng.'))"

echo.
echo -------------------------------------------------------------------------------
echo NHẬT KÝ HOẠT ĐỘNG GẦN NHẤT (logs/auto_watcher.log):
echo -------------------------------------------------------------------------------
powershell -Command "if (Test-Path 'logs/auto_watcher.log') { Get-Content 'logs/auto_watcher.log' -Tail 15 } else { Write-Output 'Chưa có file log.' }"
echo -------------------------------------------------------------------------------
echo.
echo Dịch vụ đã được cấu hình tự khởi động cùng Windows tại Startup folder.
echo Mỗi khi lưu file Excel (Ctrl + S), hệ thống sẽ tự cập nhật toàn bộ báo cáo!
echo.
pause

@echo off
chcp 65001 > nul
title Kích Hoạt Dịch Vụ Tự Động Đồng Bộ Chỉ Số Đào Tạo (PMO AI Agent)
color 0A

echo ===============================================================================
echo      HỆ THỐNG TỰ ĐỘNG CẬP NHẬT BÁO CÁO ĐÀO TẠO (AI PMO AGENT)
echo ===============================================================================
echo.
echo  File theo dõi: C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx
echo.
echo  CƠ CHẾ: Khi bạn chỉnh sửa và bấm Ctrl + S trong Excel,
echo  hệ thống sẽ TỰ ĐỘNG đồng bộ và biên dịch lại toàn bộ Dashboard & Báo cáo.
echo.
echo ===============================================================================
echo.

cd /d "%~dp0"
uv run python scripts/install_auto_watcher.py

echo.
echo Hoàn tất kích hoạt dịch vụ chạy ngầm! Bạn có thể đóng cửa sổ này.
timeout /t 5 > nul

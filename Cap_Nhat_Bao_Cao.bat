@echo off
chcp 65001 > nul
title CẬP NHẬT TỰ ĐỘNG BÁO CÁO ĐÀO TẠO & KIỂM TOÁN (PMO AI AGENT)
color 0B

echo ===============================================================================
echo        HỆ THỐNG CẬP NHẬT TỰ ĐỘNG BÁO CÁO & DASHBOARD ĐÀO TẠO (AI PMO)
echo ===============================================================================
echo.
echo  Đang chạy đường ống hợp nhất (PMO Data Hub + Gates + Dashboards + Chuẩn hóa tên file)...
echo.

cd /d "%~dp0"
uv run python -m pmo pipeline --fast

echo.
echo ===============================================================================
echo  HOÀN TẤT CẬP NHẬT! MỞ BÁO CÁO SỬ DỤNG THƯỜNG XUYÊN TẠI:
echo   [Thư mục chính]: output\01_Bao_Cao_Su_Dung_Thuong_Xuyen\HTML_Dashboards\
echo    - 00_Cong_Tong_Hop_Toan_Vien.html
echo    - 01_Bao_Cao_Giao_Ban_Dao_Tao_Tuan.html
echo    - 02_Kiem_Toan_Hieu_Suat_Nhan_Su_Worklane.html
echo    - 03_Bang_Dieu_Khien_Giam_Doc_Dao_Tao.html
echo    - 04_Theo_Doi_Ne_Nep_Hoc_Tap_Sinh_Vien.html
echo    - 05_Du_Bao_Ket_Qua_Hoc_Tap_Va_Nguy_Co.html
echo    - 06_Kiem_Toan_Ky_Luat_Tac_Nghiep_GV_TG.html
echo    - 07_Phan_Tich_Nhat_Ky_Bao_Cao_Ngay.html
echo    - 08_Chuyen_Sau_Hoc_Vu_Theo_Khoa\
echo ===============================================================================
echo.
pause

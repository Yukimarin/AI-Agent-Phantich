@echo off
chcp 65001 > nul
title CẬP NHẬT TỰ ĐỘNG BÁO CÁO ĐÀO TẠO & KIỂM TOÁN (PMO AI AGENT)
color 0B

echo ===============================================================================
echo        HỆ THỐNG CẬP NHẬT TỰ ĐỘNG BÁO CÁO & DASHBOARD ĐÀO TẠO (AI PMO)
echo ===============================================================================
echo.
echo  1. DataSanitizer: Làm sạch dữ liệu từ PTIT_Chiso.xlsx và đồng bộ cache
echo  2. Chạy song song: Kỷ luật sinh viên & Dự báo học vụ (Agent 1 + Agent 2)
echo  3. Chạy song song: Nhật ký công việc & Kỷ luật GV/TG (Agent 4 + Agent 3)
echo  4. Biên dịch Master Executive Portal & Báo cáo KPI Markdown (Agent 5)
echo  5. Biên dịch Management Dashboards: Director Cockpit & Worklane Staff Audit
echo  6. Biên dịch Academic Issues: Báo cáo chuyên sâu theo môn KS24, KS25, KS26
echo  7. Đồng bộ tự động toàn bộ sang deploy_web/
echo.
echo ===============================================================================
echo.

cd /d "%~dp0"
uv run python run_pipeline.py

echo.
echo ===============================================================================
echo  HOÀN TẤT CẬP NHẬT BÁO CÁO! BẠN CÓ THỂ MỞ:
echo   - Master Portal:       output\dashboards\core\agent_5_master_portal.html
echo   - Báo cáo Tuần GĐĐT:   output\dashboards\management\weekly_director_report.html
echo   - Director Cockpit:    output\dashboards\management\director_cockpit.html
echo   - Worklane Staff Audit:output\dashboards\management\worklane_staff_audit.html
echo   - Cổng Học Vụ Toàn Viện:output\dashboards\academic\index.html
echo   - KS24 Microservices:  output\dashboards\academic\ks24\it214_microservices_cntt.html
echo   - KS25 CNTT FastAPI:   output\dashboards\academic\ks25\it105_fastapi_cntt.html
echo   - KS25 QTKD MAN107:    output\dashboards\academic\ks25\man107_qtkd.html
echo   - KS26 CNTT SSK101:    output\dashboards\academic\ks26\ssk101_cntt.html
echo   - KS26 QTKD SSK101:    output\dashboards\academic\ks26\ssk101_qtkd.html
echo ===============================================================================
echo.
pause

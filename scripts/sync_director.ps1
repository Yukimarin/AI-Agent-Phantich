# PowerShell Script: Tự động đồng bộ báo cáo Giám đốc Đào tạo
# Hướng dẫn chạy: Mở PowerShell và gõ: .\scripts\sync_director.ps1 -IntervalSeconds 300

param (
    [int]$IntervalSeconds = 300 # Mặc định 5 phút (300 giây)
)

$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host " KHỞI CHẠY TÁC VỤ ĐỒNG BỘ BÁO CÁO GIÁM ĐỐC ĐÀO TẠO TỰ ĐỘNG" -ForegroundColor Cyan
Write-Host " Chu kỳ chạy: Mỗi $IntervalSeconds giây" -ForegroundColor Cyan
Write-Host " Nhấn Ctrl+C để dừng." -ForegroundColor Red
Write-Host "==========================================================================" -ForegroundColor Cyan

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$workspaceRoot = Resolve-Path "$scriptPath\.."

while ($true) {
    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "`n[$now] Bắt đầu chu kỳ đồng bộ dữ liệu mới..." -ForegroundColor Yellow
    
    # 1. Đồng bộ Worklane & chạy phân tích logs
    Write-Host "-> Bước 1: Đồng bộ Worklane PM & Phân tích nhật ký..." -ForegroundColor Gray
    $procRun = Start-Process -FilePath "uv" -ArgumentList "run python agents/core/agent_4_daily_logs/run.py" -WorkingDirectory $workspaceRoot -NoNewWindow -PassThru -Wait
    
    if ($procRun.ExitCode -eq 0) {
        Write-Host "✓ Đồng bộ dữ liệu & phân tích tuần/tháng hoàn tất." -ForegroundColor Green
    } else {
        Write-Warning "⚠ Có lỗi xảy ra trong quá trình chạy run.py (ExitCode: $($procRun.ExitCode))."
    }

    # 2. Sinh báo cáo cho Giám đốc Đào tạo
    Write-Host "-> Bước 2: Sinh báo cáo Giám đốc Đào tạo (generate_report_director.py)..." -ForegroundColor Gray
    $procReport = Start-Process -FilePath "uv" -ArgumentList "run python agents/advanced/management_audit/generate_report_director.py" -WorkingDirectory $workspaceRoot -NoNewWindow -PassThru -Wait
    
    if ($procReport.ExitCode -eq 0) {
        Write-Host "✓ Đã cập nhật thành công: output/dashboards/advanced/director_cockpit.html" -ForegroundColor Green
    } else {
        Write-Warning "⚠ Có lỗi xảy ra khi chạy generate_report_director.py (ExitCode: $($procReport.ExitCode))."
    }

    Write-Host "Đang chờ $IntervalSeconds giây cho chu kỳ tiếp theo..." -ForegroundColor DarkGray
    Start-Sleep -Seconds $IntervalSeconds
}

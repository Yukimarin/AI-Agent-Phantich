# schedule_task.ps1
# Lấy đường dẫn thư mục hiện tại làm thư mục làm việc
$WorkDir = "c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT"

# Action: Chạy uv run pipeline
$Action = New-ScheduledTaskAction -Execute "uv" -Argument "run --with mysql-connector-python --with openpyxl --with numpy --with pandas --with markdown scratch/run_pipeline.py" -WorkingDirectory $WorkDir

# Trigger: Lặp lại hàng ngày vào lúc 7:00 AM
$Trigger = New-ScheduledTaskTrigger -Daily -At 7:00AM

# Đăng ký Scheduled Task
Register-ScheduledTask -TaskName "PTIT_Daily_KPI_Fetch" -Action $Action -Trigger $Trigger -Description "Fetch Worklane data and update Training KPI dashboards daily at 7:00 AM" -Force

Write-Host "Đã đăng ký Scheduled Task 'PTIT_Daily_KPI_Fetch' thành công lúc 7h sáng hàng ngày!"

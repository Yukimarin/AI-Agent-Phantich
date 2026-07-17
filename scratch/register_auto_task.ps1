# Script to register the automated KPI update task in Windows Task Scheduler

$TaskName = "PTIT_KPI_Auto_Update"
$ScriptPath = "c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\scratch\auto_update_kpi.ps1"
$WorkingDirectory = "c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT"

Write-Output "Registering Windows Scheduled Task: $TaskName..."

# 1. Define Task Action
# Running powershell ngầm with Hidden window
$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`"" `
    -WorkingDirectory $WorkingDirectory

# 2. Define Triggers
# Trigger 1: Daily trigger starting at 7:00 AM, repeating every 1 hour
$DailyTrigger = New-ScheduledTaskTrigger -Daily -At "7:00AM"
$DailyTrigger.RepetitionInterval = (New-TimeSpan -Hours 1)
$DailyTrigger.RepetitionDuration = (New-TimeSpan -Days 999)

# Trigger 2: Run when any user logs on
$LogonTrigger = New-ScheduledTaskTrigger -AtLogOn

$Triggers = @($DailyTrigger, $LogonTrigger)

# 3. Define Settings
# Allow task to run on demand, stop if it runs longer than 2 hours, wake to run off, run even on battery
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

# 4. Register the Task
# Register under the current logged-in user context
try {
    # If task already exists, unregister it first to avoid conflicts
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Write-Output "Task '$TaskName' already exists. Re-registering..."
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }
    
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Triggers `
        -Settings $Settings `
        -Description "Tự động kiểm tra file Excel Backup, chạy pipeline đánh giá KPI GV/TG và đẩy báo cáo lên GitHub hàng giờ."
        
    Write-Output "SUCCESS: Windows Scheduled Task '$TaskName' registered successfully!"
    Write-Output "The task will run:"
    Write-Output "  - Every day starting at 7:00 AM, repeating every 1 hour."
    Write-Output "  - Every time you log in to Windows."
    Write-Output "  - You can also run it manually from Task Scheduler (taskschd.msc) or by clicking Run."
} catch {
    Write-Error "ERROR: Failed to register Scheduled Task: $_"
    Write-Output "Please ensure you run this script as Administrator if registration fails."
}

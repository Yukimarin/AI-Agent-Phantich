# PowerShell script for automated update of training indicators and KPI evaluation
# Target: C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx -> data/PTIT_Chiso.xlsx

$ProjectDir = "c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT"
$BackupFile = "C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx"
$DestFile = "$ProjectDir\data\PTIT_Chiso.xlsx"
$DestBackup = "$ProjectDir\data\PTIT_Chiso_backup.xlsx"
$LogFile = "$ProjectDir\data\auto_update.log"

# Function to log messages with timestamp
function Write-Log {
    param([string]$Message)
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$TimeStamp] $Message"
    Write-Output $LogMessage
    Add-Content -Path $LogFile -Value $LogMessage
}

# Ensure we are in the project directory
Set-Location -Path $ProjectDir

Write-Log "------------------------------------------------------------"
Write-Log "AUTO UPDATE KPI PROCESS STARTED"
Write-Log "------------------------------------------------------------"

# Check if backup file exists
if (-not (Test-Path $BackupFile)) {
    Write-Log "ERROR: Backup file not found at: $BackupFile. Exiting."
    exit 1
}

# Check if update is needed (compare modified dates)
$UpdateNeeded = $false
if (-not (Test-Path $DestFile)) {
    Write-Log "Project Excel file not found. Initial setup copy needed."
    $UpdateNeeded = $true
} else {
    $BackupTime = (Get-Item $BackupFile).LastWriteTime
    $DestTime = (Get-Item $DestFile).LastWriteTime
    
    # Check if backup is newer than destination
    if ($BackupTime -gt $DestTime) {
        Write-Log "Newer file detected in backup folder. (Backup: $BackupTime, Current: $DestTime)"
        $UpdateNeeded = $true
    } else {
        Write-Log "No newer data found in backup. (Backup: $BackupTime, Current: $DestTime). Stopping process."
        $UpdateNeeded = $false
    }
}

if (-not $UpdateNeeded) {
    Write-Log "Process finished without updates."
    exit 0
}

# Step 1: Backup current file
Write-Log "Step 1/6: Backing up current file to $DestBackup..."
try {
    if (Test-Path $DestFile) {
        Copy-Item -Path $DestFile -Destination $DestBackup -Force
        Write-Log "Backup successful."
    }
} catch {
    Write-Log "WARNING: Could not backup current file: $_"
}

# Step 2: Copy new file from Backup
Write-Log "Step 2/6: Copying new Excel file from Backup..."
try {
    Copy-Item -Path $BackupFile -Destination $DestFile -Force
    Write-Log "Copy successful. New file updated."
} catch {
    Write-Log "ERROR: Failed to copy new file from Backup: $_"
    exit 1
}

# Step 3: Check and start MySQL 3307 if not running
Write-Log "Step 3/6: Checking MySQL Server on port 3307..."
$PortCheck = Get-NetTCPConnection -LocalPort 3307 -ErrorAction SilentlyContinue
if ($PortCheck) {
    Write-Log "MySQL Server is already running on port 3307."
} else {
    Write-Log "MySQL Server on port 3307 is stopped. Attempting to start..."
    try {
        Start-Process "C:\Program Files\MySQL\MySQL Server 9.7\bin\mysqld.exe" `
            -ArgumentList "--port=3307 --datadir=c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\data\mysql_data_97 --mysqlx=OFF --shared-memory" `
            -WindowStyle Hidden
        
        # Wait for MySQL to initialize and start listening
        Start-Sleep -Seconds 5
        
        $PortCheck2 = Get-NetTCPConnection -LocalPort 3307 -ErrorAction SilentlyContinue
        if ($PortCheck2) {
            Write-Log "MySQL Server started successfully on port 3307."
        } else {
            Write-Log "ERROR: Failed to start MySQL Server on port 3307 (port still closed)."
            exit 1
        }
    } catch {
        Write-Log "ERROR: Failed to launch MySQL Server process: $_"
        exit 1
    }
}

# Step 4: Run integration pipeline
Write-Log "Step 4/6: Executing integration pipeline (run_pipeline.py)..."
try {
    $pipelineResult = uv run scratch/run_pipeline.py 2>&1
    Write-Log "Pipeline executed."
    # Append pipeline stdout to log
    Add-Content -Path $LogFile -Value $pipelineResult
} catch {
    Write-Log "ERROR: Pipeline execution failed: $_"
    exit 1
}

# Step 5: Run KPI ranking (generate_kpi_ranking.py)
Write-Log "Step 5/6: Executing KPI ranking and energy classification (generate_kpi_ranking.py)..."
try {
    $rankingResult = uv run --with openpyxl --with pandas --with markdown --with numpy --with mysql-connector-python scratch/generate_kpi_ranking.py 2>&1
    Write-Log "KPI Ranking executed successfully."
    # Append ranking stdout to log
    Add-Content -Path $LogFile -Value $rankingResult
} catch {
    Write-Log "ERROR: KPI Ranking execution failed: $_"
    exit 1
}

# Step 6: Commit and Push to GitHub
Write-Log "Step 6/6: Staging and pushing changes to GitHub..."
try {
    # Check if git status has changes
    $gitStatus = git status --porcelain
    if ($gitStatus) {
        git add .
        $CommitDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "auto: update KPI and reports on $CommitDate"
        git push origin main
        Write-Log "Git commit and push completed successfully."
    } else {
        Write-Log "No changes in reports. Skip pushing to GitHub."
    }
} catch {
    Write-Log "WARNING: Git sync failed: $_"
}

Write-Log "------------------------------------------------------------"
Write-Log "AUTO UPDATE KPI PROCESS COMPLETED SUCCESSFULLY"
Write-Log "------------------------------------------------------------"

$vaultPath = "C:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT"
$obsidianDir = Join-Path $vaultPath ".obsidian"
$pluginsDir = Join-Path $obsidianDir "plugins"

# Kích hoạt TLS 1.2 cho PowerShell để tránh lỗi tải mạng
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Tạo các thư mục cấu hình
New-Item -ItemType Directory -Force -Path $pluginsDir

# 1. Đăng ký plugin trong danh sách community-plugins.json để tự động kích hoạt
$communityPluginsJson = Join-Path $obsidianDir "community-plugins.json"
'["dataview", "obsidian-admonition"]' | Out-File -FilePath $communityPluginsJson -Encoding utf8

# 2. Tải plugin Dataview
$dataviewDir = Join-Path $pluginsDir "dataview"
New-Item -ItemType Directory -Force -Path $dataviewDir
Write-Host "Downloading Dataview plugin..."
Invoke-WebRequest -Uri "https://github.com/blacksmithgu/obsidian-dataview/releases/latest/download/main.js" -OutFile (Join-Path $dataviewDir "main.js")
Invoke-WebRequest -Uri "https://github.com/blacksmithgu/obsidian-dataview/releases/latest/download/manifest.json" -OutFile (Join-Path $dataviewDir "manifest.json")
Invoke-WebRequest -Uri "https://github.com/blacksmithgu/obsidian-dataview/releases/latest/download/styles.css" -OutFile (Join-Path $dataviewDir "styles.css")

# 3. Tải plugin Admonition
$admonitionDir = Join-Path $pluginsDir "obsidian-admonition"
New-Item -ItemType Directory -Force -Path $admonitionDir
Write-Host "Downloading Admonition plugin..."
Invoke-WebRequest -Uri "https://github.com/valentine195/obsidian-admonition/releases/latest/download/main.js" -OutFile (Join-Path $admonitionDir "main.js")
Invoke-WebRequest -Uri "https://github.com/valentine195/obsidian-admonition/releases/latest/download/manifest.json" -OutFile (Join-Path $admonitionDir "manifest.json")
try {
    Invoke-WebRequest -Uri "https://github.com/valentine195/obsidian-admonition/releases/latest/download/styles.css" -OutFile (Join-Path $admonitionDir "styles.css") -ErrorAction Stop
} catch {
    Write-Host "styles.css not found for Admonition (this is expected if it has no styles)"
}

Write-Host "Obsidian Plugins installed successfully!"

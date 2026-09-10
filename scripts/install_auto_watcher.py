import os
import sys
import subprocess
import shutil

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VBS_PATH = os.path.join(PROJECT_ROOT, "scripts", "run_watcher_silent.vbs")
STARTUP_DIR = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
SHORTCUT_PATH = os.path.join(STARTUP_DIR, "AutoSync_PTIT_Chiso.lnk")

def create_startup_shortcut():
    print("=" * 70)
    print("CÀI ĐẶT DỊCH VỤ TỰ ĐỘNG ĐỒNG BỘ CHỈ SỐ ĐÀO TẠO VÀO WINDOWS STARTUP")
    print("=" * 70)
    
    ps_script = f"""
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{SHORTCUT_PATH}')
$Shortcut.TargetPath = 'wscript.exe'
$Shortcut.Arguments = '"{VBS_PATH}"'
$Shortcut.WorkingDirectory = '{PROJECT_ROOT}'
$Shortcut.Description = 'Tu dong dong bo chi so dao tao tu Excel Backup vao PMO AI Agent'
$Shortcut.Save()
"""
    try:
        proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True)
        if os.path.exists(SHORTCUT_PATH):
            print(f"✓ Đã tạo thành công lối tắt tự khởi động cùng Windows tại:")
            print(f"  {SHORTCUT_PATH}")
        else:
            print(f"⚠️ Chưa tạo được shortcut qua PowerShell, thử copy file script trực tiếp...")
            target_vbs = os.path.join(STARTUP_DIR, "AutoSync_PTIT_Chiso.vbs")
            shutil.copy2(VBS_PATH, target_vbs)
            print(f"✓ Đã copy trực tiếp VBS vào Startup: {target_vbs}")
    except Exception as e:
        print(f"Lỗi khi cài đặt shortcut: {e}")

def start_daemon_now():
    print("\nKhởi động tiến trình chạy ngầm ngay bây giờ...")
    try:
        subprocess.Popen(["wscript.exe", VBS_PATH], cwd=PROJECT_ROOT)
        print("✓ Đã kích hoạt tiến trình theo dõi chạy ngầm (Silent Daemon) thành công!")
        print("  Từ nay, mỗi khi bạn mở file Excel và bấm Ctrl + S, báo cáo sẽ tự động làm mới ngầm!")
    except Exception as e:
        print(f"Lỗi khi khởi động daemon: {e}")

if __name__ == "__main__":
    create_startup_shortcut()
    start_daemon_now()

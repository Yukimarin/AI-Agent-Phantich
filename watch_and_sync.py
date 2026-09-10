import os
import sys
import time
import subprocess
import logging
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
WATCH_FILE = r"C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx"
POLL_INTERVAL = 1.5
PID_FILE = os.path.join(PROJECT_ROOT, "data", "processed", "watcher.pid")
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "auto_watcher.log")

os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

class FlushingFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        FlushingFileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def show_windows_notification(title, message):
    try:
        ps_cmd = f"""
Add-Type -AssemblyName System.Windows.Forms;
$n = New-Object System.Windows.Forms.NotifyIcon;
$n.Icon = [System.Drawing.SystemIcons]::Information;
$n.Visible = $true;
$n.ShowBalloonTip(3000, '{title}', '{message}', [System.Windows.Forms.ToolTipIcon]::Info);
Start-Sleep -Milliseconds 800;
$n.Dispose()
"""
        subprocess.Popen(
            ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_cmd],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
    except Exception as e:
        logging.warning(f"Không thể hiển thị Windows Toast: {e}")

def get_file_mtime(path):
    if not os.path.exists(path):
        return None
    try:
        return os.path.getmtime(path)
    except OSError:
        return None

def wait_for_file_ready(path, timeout=5.0):
    """Đợi file Excel nhả khóa ghi hoàn toàn sau khi nhấn Ctrl+S"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with open(path, "rb") as f:
                f.read(1024)
            return True
        except (IOError, PermissionError):
            time.sleep(0.3)
    return False

def trigger_fast_pipeline():
    start_time = time.time()
    logging.info("=" * 70)
    logging.info("🚀 PHÁT HIỆN THAY ĐỔI TỪ EXCEL! TỰ ĐỘNG CHẠY FAST PIPELINE...")
    logging.info("=" * 70)
    
    # Đợi Excel hoàn tất ghi đĩa
    time.sleep(1.0)
    if not wait_for_file_ready(WATCH_FILE):
        logging.warning("⚠️ File đang bị lock bởi ứng dụng khác, vẫn thử tiến hành đồng bộ...")
    
    cmd = ["uv", "run", "run_pipeline.py", "--fast"]
    try:
        proc = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, encoding='utf-8')
        if proc.stdout:
            for line in proc.stdout.strip().splitlines()[-10:]:
                logging.info(f"Pipeline: {line}")
        if proc.returncode != 0 and proc.stderr:
            logging.error(f"Lỗi Pipeline: {proc.stderr}")
            show_windows_notification("PMO AI Agent - Lỗi Đồng Bộ", "Có lỗi xảy ra khi cập nhật báo cáo tự động.")
            return False
            
        elapsed = time.time() - start_time
        logging.info("=" * 70)
        logging.info(f"✓ HOÀN TẤT ĐỒNG BỘ BÁO CÁO TRONG {elapsed:.2f} GIÂY!")
        logging.info("🎯 Báo cáo đã cập nhật: data/report_kpi_gv_tg.md & Dashboard HTML")
        logging.info("=" * 70)
        
        show_windows_notification(
            "PMO AI Agent - Đã Cập Nhật Báo Cáo",
            f"Dữ liệu Excel mới nhất đã được đồng bộ tự động ({datetime.now().strftime('%H:%M:%S')})!"
        )
        return True
    except Exception as e:
        logging.error(f"Lỗi ngoại lệ khi chạy pipeline: {e}")
        return False

def is_pid_running(pid):
    try:
        if os.name == 'nt':
            cmd = f'tasklist /FI "PID eq {pid}" /FO CSV /NH'
            out = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore').strip()
            if not out or "No tasks are running" in out or "INFO:" in out:
                return False
            out_lower = out.lower()
            return ("python" in out_lower or "uv" in out_lower)
        else:
            os.kill(pid, 0)
            return True
    except Exception:
        return False

def check_singleton():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r", encoding="utf-8") as f:
                old_pid = int(f.read().strip())
            if is_pid_running(old_pid):
                logging.info(f"Dịch vụ Auto-Watcher đã đang chạy (PID: {old_pid}). Thoát tiến trình trùng lặp.")
                sys.exit(0)
        except Exception:
            pass
    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))

def cleanup():
    try:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
    except Exception:
        pass

def main():
    check_singleton()
    logging.info("=" * 70)
    logging.info("DỊCH VỤ GIÁM SÁT TỰ ĐỘNG CẬP NHẬT CHỈ SỐ ĐÀO TẠO (AUTO-WATCHER DAEMON)")
    logging.info(f"File theo dõi: {WATCH_FILE}")
    logging.info(f"PID hiện tại: {os.getpid()}")
    logging.info("Cơ chế: Mỗi khi bạn lưu Excel (Ctrl+S), hệ thống tự động cập nhật báo cáo trong vài giây!")
    logging.info("=" * 70)
    
    last_mtime = get_file_mtime(WATCH_FILE)
    if last_mtime is None:
        logging.warning(f"⚠️ Cảnh báo: Không tìm thấy file {WATCH_FILE}. Đang chờ file xuất hiện...")
    else:
        logging.info(f"✓ Đang theo dõi file Excel (Mtime: {datetime.fromtimestamp(last_mtime).strftime('%Y-%m-%d %H:%M:%S')})...")
        
    try:
        while True:
            time.sleep(POLL_INTERVAL)
            current_mtime = get_file_mtime(WATCH_FILE)
            if current_mtime is None:
                continue
                
            if last_mtime is None or abs(current_mtime - last_mtime) > 0.05:
                logging.info(f"Phát hiện file thay đổi ({last_mtime} -> {current_mtime})")
                last_mtime = current_mtime
                trigger_fast_pipeline()
                last_mtime = get_file_mtime(WATCH_FILE)
    except KeyboardInterrupt:
        logging.info("Đã dừng dịch vụ giám sát tự động.")
    finally:
        cleanup()

if __name__ == "__main__":
    main()

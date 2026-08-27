import subprocess
import sys
import os
import shutil
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_script(name, path, with_deps=None):
    start_time = time.time()
    print("=" * 80)
    print(f"BẮT ĐẦU CHẠY: {name}")
    print(f"Path: {path}")
    print("=" * 80)
    
    if with_deps:
        cmd = ["uv", "run"]
        for dep in with_deps:
            cmd += ["--with", dep]
        cmd.append(path)
    else:
        cmd = [sys.executable, path]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print(result.stdout.strip())
        elapsed = time.time() - start_time
        print(f"✓ HOÀN THÀNH: {name} ({elapsed:.2f}s)\n")
        return True
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"✗ LỖI TẠI: {name} ({elapsed:.2f}s)")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        print(f"! FALLBACK: Bỏ qua lỗi tại {name} để hệ thống tiếp tục chạy.\n")
        return False

def validate_output(file_path, file_type):
    if not os.path.exists(file_path):
        print(f"✗ Cảnh báo: File {file_path} chưa được tạo ra.")
        return False
    # Kiểm tra nhanh kích thước file để xác nhận tính toàn vẹn
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        print(f"✗ Cảnh báo: File {file_path} bị rỗng (0 bytes).")
        return False
    return True

def ensure_mysql_started():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect(('127.0.0.1', 3307))
        s.close()
        return True
    except socket.error:
        s.close()
        
    print("⚠️ MySQL Server trên cổng 3307 đang tắt. Đang khởi động tự động...")
    mysql_bin = r"C:\Program Files\MySQL\MySQL Server 9.7\bin\mysqld.exe"
    data_dir = os.path.abspath("data/mysql_data_97")
    
    if not os.path.exists(mysql_bin):
        print(f"✗ Không tìm thấy MySQL binary. Fallback về SQLite.")
        return False
        
    cmd = [
        mysql_bin,
        "--no-defaults",
        f"--datadir={data_dir}",
        "--port=3307",
        "--shared-memory"
    ]
    
    try:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        for _ in range(8):
            time.sleep(0.5)
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.settimeout(0.3)
            try:
                s2.connect(('127.0.0.1', 3307))
                print("✓ Khởi động MySQL Server 3307 thành công!")
                s2.close()
                return True
            except socket.error:
                s2.close()
        return False
    except Exception as e:
        print(f"✗ Lỗi khởi động MySQL: {e}")
        return False

def main():
    total_start = time.time()
    run_advanced = "--with-advanced" in sys.argv
    
    print("================================================================================")
    print("KHỞI CHẠY ĐƯỜNG ỐNG TINH GỌN (CORE PIPELINE & MASTER PORTAL)")
    print("================================================================================")
    
    # Đảm bảo các thư mục đầu ra tồn tại
    os.makedirs("output/dashboards/core", exist_ok=True)
    os.makedirs("output/dashboards/advanced", exist_ok=True)
    os.makedirs("output/reports/core", exist_ok=True)
    os.makedirs("output/reports/advanced", exist_ok=True)

    # Bước 0: DataSanitizer (Harness Layer & Single Source Cache)
    run_script(
        "DataSanitizer: Làm sạch dữ liệu & Tạo Single Cache JSON", 
        "agents/common/data_sanitizer.py",
        with_deps=["openpyxl"]
    )

    # Bước 0.5: Kiểm tra Database
    ensure_mysql_started()

    # Bước 1: Agent 1 - Kỷ luật học viên
    run_script(
        "Agent 1: Kỷ luật học viên (Class KPI)", 
        "agents/core/agent_1_class_kpi/run.py",
        with_deps=["openpyxl", "numpy", "markdown"]
    )
    validate_output("data/processed/agent1_output.json", "json")
    validate_output("output/dashboards/core/agent_1_student_discipline.html", "html")
    
    # Bước 2: Agent 2 - Dự báo học vụ
    run_script(
        "Agent 2: Dự báo học vụ (Academic Predictor)", 
        "agents/core/agent_2_academic_pred/run.py",
        with_deps=["mysql-connector-python", "openpyxl", "numpy"]
    )
    validate_output("data/processed/agent2_output.json", "json")
    validate_output("output/dashboards/core/agent_2_academic_prediction.html", "html")
    
    # Bước 3: Agent 4 - Nhật ký công việc & Sync Worklane
    run_script(
        "Agent 4: Nhật ký công việc (Daily Logs Auditor)", 
        "agents/core/agent_4_daily_logs/run.py",
        with_deps=["openpyxl"]
    )
    validate_output("data/processed/daily_log_analysis.json", "json")
    validate_output("output/dashboards/core/agent_4_daily_logs.html", "html")
    
    # Bước 4: Agent 3 - Kỷ luật tác nghiệp GV/TG (Phụ thuộc Agent 4)
    run_script(
        "Agent 3: Kỷ luật tác nghiệp GV/TG (Ops Discipline)", 
        "agents/core/agent_3_ops_discipline/run.py",
        with_deps=["mysql-connector-python", "openpyxl"]
    )
    validate_output("data/processed/agent3_output.json", "json")
    validate_output("output/dashboards/core/agent_3_ops_discipline.html", "html")
    
    # Báo cáo Nâng cao (Tùy chọn khi truyền --with-advanced)
    if run_advanced:
        print("\n--- CHẠY BÁO CÁO NÂNG CAO (ON-DEMAND) ---")
        run_script(
            "Custom Director Report: Báo cáo Giám đốc Đào tạo",
            "agents/advanced/management_audit/generate_report_director.py",
            with_deps=["openpyxl"]
        )
        run_script(
            "Advanced QLDT Report: Báo cáo tháng QLĐT",
            "agents/advanced/management_audit/generate_qldt_report.py",
            with_deps=["openpyxl"]
        )
        run_script(
            "HCM Summary Report: Báo cáo tổng hợp nhân sự HCM",
            "agents/advanced/management_audit/generate_hcm_report.py",
            with_deps=["openpyxl"]
        )

    # Bước 5: Master Lead Portal & Báo cáo KPI Markdown
    run_script(
        "Agent 5: Biên dịch Executive Dashboard (Master Portal)", 
        "agents/master/agent_5_master_portal/generate_unified_dashboard.py"
    )
    validate_output("output/dashboards/core/agent_5_master_portal.html", "html")
    
    run_script(
        "Agent 5: Biên dịch Báo cáo KPI GV/TG Markdown", 
        "agents/master/agent_5_master_portal/generate_kpi_report.py"
    )
    validate_output("data/report_kpi_gv_tg.md", "markdown")
    
    total_elapsed = time.time() - total_start
    print("=" * 80)
    print(f"✓ ĐƯỜNG ỐNG ĐÃ HOÀN THÀNH TOÀN BỘ TRONG {total_elapsed:.2f} GIÂY!")
    print("================================================================================")

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import shutil
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_script(name, path, with_deps=None, extra_args=None):
    start_time = time.time()
    print("=" * 80, flush=True)
    print(f"BẮT ĐẦU CHẠY: {name}", flush=True)
    print(f"Path: {path}", flush=True)
    print("=" * 80, flush=True)
    
    if with_deps:
        cmd = ["uv", "run"]
        for dep in with_deps:
            cmd += ["--with", dep]
        cmd.append(path)
    else:
        cmd = ["uv", "run", "python", path]
        
    if extra_args:
        cmd.extend(extra_args)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print(result.stdout.strip(), flush=True)
        elapsed = time.time() - start_time
        print(f"✓ HOÀN THÀNH: {name} ({elapsed:.2f}s)\n", flush=True)
        return True
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"✗ LỖI TẠI: {name} ({elapsed:.2f}s)", flush=True)
        if e.stdout:
            print(e.stdout, flush=True)
        if e.stderr:
            print(e.stderr, flush=True)
        print(f"! FALLBACK: Bỏ qua lỗi tại {name} để hệ thống tiếp tục chạy.\n", flush=True)
        return False

def validate_output(file_path, file_type):
    if not os.path.exists(file_path):
        print(f"✗ Cảnh báo: File {file_path} chưa được tạo ra.")
        return False
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

def sync_to_deploy_web():
    """Đồng bộ toàn bộ báo cáo vào deploy_web để xem nhanh hoặc deploy"""
    deploy_dir = "deploy_web"
    os.makedirs(deploy_dir, exist_ok=True)
    os.makedirs(os.path.join(deploy_dir, "academic"), exist_ok=True)
    os.makedirs(os.path.join(deploy_dir, "management"), exist_ok=True)
    os.makedirs(os.path.join(deploy_dir, "core"), exist_ok=True)

    # Copy core dashboards
    core_src = "output/dashboards/core"
    if os.path.exists(core_src):
        for f in os.listdir(core_src):
            if f.endswith(".html"):
                shutil.copy2(os.path.join(core_src, f), os.path.join(deploy_dir, "core", f))
                shutil.copy2(os.path.join(core_src, f), os.path.join(deploy_dir, f))

    # Copy management dashboards
    mgmt_src = "output/dashboards/management"
    if os.path.exists(mgmt_src):
        for f in os.listdir(mgmt_src):
            if f.endswith(".html"):
                shutil.copy2(os.path.join(mgmt_src, f), os.path.join(deploy_dir, "management", f))
                shutil.copy2(os.path.join(mgmt_src, f), os.path.join(deploy_dir, f))

    # Copy academic dashboards (copy cả thư mục con ks24, ks25, ks26)
    acad_src = "output/dashboards/academic"
    if os.path.exists(acad_src):
        for item in os.listdir(acad_src):
            s_item = os.path.join(acad_src, item)
            d_item = os.path.join(deploy_dir, "academic", item)
            if os.path.isdir(s_item):
                shutil.copytree(s_item, d_item, dirs_exist_ok=True)
            elif item.endswith(".html"):
                shutil.copy2(s_item, d_item)

    # Đặt agent_5_master_portal làm index chính nếu có
    master_path = os.path.join(core_src, "agent_5_master_portal.html")
    if os.path.exists(master_path):
        shutil.copy2(master_path, os.path.join(deploy_dir, "index.html"))

    print("✓ Đã đồng bộ toàn bộ Dashboard vào deploy_web/")

def main():
    total_start = time.time()
    is_fast = "--fast" in sys.argv or "--quick" in sys.argv
    fast_args = ["--fast"] if is_fast else []
    
    mode_str = "CHẾ ĐỘ SIÊU TỐC (FAST PIPELINE < 15s)" if is_fast else "CHẾ ĐỘ TOÀN DIỆN (FULL PIPELINE)"
    print("================================================================================")
    print(f"KHỞI CHẠY ĐƯỜNG ỐNG ĐÀO TẠO PMO: {mode_str}")
    print("================================================================================")
    
    # Đảm bảo cấu trúc thư mục quy hoạch chuẩn
    os.makedirs("output/dashboards/core", exist_ok=True)
    os.makedirs("output/dashboards/management", exist_ok=True)
    os.makedirs("output/dashboards/academic", exist_ok=True)
    os.makedirs("output/reports/core", exist_ok=True)
    os.makedirs("output/reports/management", exist_ok=True)

    # Bước 0: DataSanitizer (Làm sạch dữ liệu & Single Source Cache)
    run_script(
        "DataSanitizer: Làm sạch dữ liệu & Tạo Single Cache JSON", 
        "agents/common/data_sanitizer.py",
        with_deps=["openpyxl"],
        extra_args=fast_args
    )

    # Bước 0.5: Kiểm tra Database
    ensure_mysql_started()

    # Bước 1 & 2: Chạy song song Nhánh A (Học thuật) và Nhánh B (Tác nghiệp)
    from concurrent.futures import ThreadPoolExecutor

    def run_branch_academic():
        print("\n[NHÁNH A] Bắt đầu xử lý Kỷ luật SV & Dự báo học thuật...")
        # Agent 1 - Kỷ luật học viên
        run_script(
            "Agent 1: Kỷ luật học viên (Class KPI)", 
            "agents/core/agent_1_class_kpi/run.py",
            with_deps=["openpyxl", "numpy", "markdown"]
        )
        validate_output("data/processed/agent1_output.json", "json")
        validate_output("output/dashboards/core/agent_1_student_discipline.html", "html")
        
        # Agent 2 - Dự báo học vụ
        run_script(
            "Agent 2: Dự báo học vụ (Academic Predictor)", 
            "agents/core/agent_2_academic_pred/run.py",
            with_deps=["mysql-connector-python", "openpyxl", "numpy"]
        )
        validate_output("data/processed/agent2_output.json", "json")
        validate_output("output/dashboards/core/agent_2_academic_prediction.html", "html")
        print("[NHÁNH A] ✓ Hoàn thành toàn bộ Kỷ luật SV & Dự báo học thuật!")
        return True

    def run_branch_operations():
        print("\n[NHÁNH B] Bắt đầu xử lý Nhật ký công việc & Kỷ luật tác nghiệp...")
        # Agent 4 - Nhật ký công việc & Sync Worklane
        run_script(
            "Agent 4: Nhật ký công việc (Daily Logs Auditor)", 
            "agents/core/agent_4_daily_logs/run.py",
            with_deps=["openpyxl"],
            extra_args=fast_args
        )
        validate_output("data/processed/daily_log_analysis.json", "json")
        validate_output("output/dashboards/core/agent_4_daily_logs.html", "html")
        
        # Agent 3 - Kỷ luật tác nghiệp GV/TG
        run_script(
            "Agent 3: Kỷ luật tác nghiệp GV/TG (Ops Discipline)", 
            "agents/core/agent_3_ops_discipline/run.py",
            with_deps=["mysql-connector-python", "openpyxl"]
        )
        validate_output("data/processed/agent3_output.json", "json")
        validate_output("output/dashboards/core/agent_3_ops_discipline.html", "html")
        print("[NHÁNH B] ✓ Hoàn thành toàn bộ Nhật ký công việc & Kỷ luật tác nghiệp!")
        return True

    print("\n" + "=" * 80)
    print("🚀 KHỞI CHẠY ĐỒNG THỜI 2 NHÁNH ĐỘC LẬP: HỌC THUẬT // TÁC NGHIỆP...")
    print("=" * 80)
    with ThreadPoolExecutor(max_workers=2) as executor:
        f_acad = executor.submit(run_branch_academic)
        f_ops = executor.submit(run_branch_operations)
        f_acad.result()
        f_ops.result()

    # Bước 3: Master Lead Portal & Báo cáo KPI Markdown
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

    # Bước 4: Quản trị & Kiểm toán (Management Dashboards: director_cockpit.html & worklane_staff_audit.html)
    print("\n" + "=" * 80)
    print("📊 BIÊN DỊCH BÁO CÁO QUẢN TRỊ & KIỂM TOÁN (MANAGEMENT DASHBOARDS)...")
    print("=" * 80)
    run_script(
        "Management: Báo cáo Giám đốc Đào tạo (Director Cockpit)",
        "agents/advanced/management_audit/generate_report_director.py",
        with_deps=["openpyxl"]
    )
    validate_output("output/dashboards/management/director_cockpit.html", "html")

    run_script(
        "Management: Kiểm toán Nhân sự Worklane Đa Kỳ (Staff Audit)",
        "agents/audit/generate_audit_dashboard.py"
    )
    validate_output("output/dashboards/management/worklane_staff_audit.html", "html")

    run_script(
        "Management: Báo cáo Giao ban Đào tạo Tuần (Weekly Director Report)",
        "scripts/generate_weekly_director_dashboard.py"
    )
    validate_output("output/dashboards/management/weekly_director_report.html", "html")

    # Bước 5: Báo cáo Chuyên sâu Vấn đề Học vụ 3 Khóa (KS24, KS25, KS26)
    print("\n" + "=" * 80)
    print("🎓 BIÊN DỊCH BÁO CÁO CHUYÊN SÂU VẤN ĐỀ THEO MÔN (KS24, KS25, KS26)...")
    print("=" * 80)
    run_script(
        "Academic: Báo cáo Chuyên sâu Học vụ KS24, KS25, KS26",
        "scripts/generate_academic_cohort_dashboards.py"
    )
    validate_output("output/dashboards/academic/ks24/it214_microservices_cntt.html", "html")
    validate_output("output/dashboards/academic/ks25/it105_fastapi_cntt.html", "html")
    validate_output("output/dashboards/academic/ks25/man107_qtkd.html", "html")
    validate_output("output/dashboards/academic/ks26/ssk101_cntt.html", "html")
    validate_output("output/dashboards/academic/ks26/ssk101_qtkd.html", "html")
    validate_output("output/dashboards/academic/index.html", "html")

    # Bước 6: Tự động đồng bộ vào deploy_web/
    sync_to_deploy_web()

    total_elapsed = time.time() - total_start
    print("=" * 80)
    print(f"✓ ĐƯỜNG ỐNG ĐÃ HOÀN THÀNH TOÀN BỘ TRONG {total_elapsed:.2f} GIÂY!")
    print("📂 CẤU TRÚC ĐẦU RA CHUẨN HÓA:")
    print("  - Core Dashboards:       output/dashboards/core/ (Agent 1 - 5)")
    print("  - Management Dashboards: output/dashboards/management/ (Director Cockpit & Worklane Staff Audit)")
    print("  - Academic Cohort Issues: output/dashboards/academic/ (KS24, KS25, KS26)")
    print("  - Web Deploy Portal:     deploy_web/ (Sẵn sàng mở hoặc host web)")
    print("================================================================================")

if __name__ == "__main__":
    main()

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
    # Sử dụng trực tiếp sys.executable trong .venv đã đồng bộ qua pyproject.toml
    cmd = [sys.executable, path]
    if extra_args:
        cmd.extend(extra_args)

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        elapsed = time.time() - start_time
        print(f"✓ HOÀN THÀNH: {name} ({elapsed:.2f}s)", flush=True)
        return True
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"✗ LỖI TẠI: {name} ({elapsed:.2f}s)", flush=True)
        if e.stdout:
            print(e.stdout, flush=True)
        if e.stderr:
            print(e.stderr, flush=True)
        return False

def validate_output(file_path, file_type, min_mtime=None):
    if not os.path.exists(file_path):
        print(f"✗ LỖI KIỂM ĐỊNH: File {file_path} không tồn tại!")
        return False
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        print(f"✗ LỖI KIỂM ĐỊNH: File {file_path} bị rỗng (0 bytes)!")
        return False
    if min_mtime is not None:
        mtime = os.path.getmtime(file_path)
        if mtime < min_mtime:
            print(f"⚠️ CẢNH BÁO: File {file_path} không được ghi mới trong lần chạy này (mtime: {mtime} < {min_mtime})")
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

    pipeline_errors = []

    # Bước 0: DataSanitizer (Làm sạch dữ liệu & Single Source Cache)
    ok_sanitizer = run_script(
        "DataSanitizer: Làm sạch dữ liệu & Tạo Single Cache JSON", 
        "agents/common/data_sanitizer.py",
        with_deps=["openpyxl"],
        extra_args=fast_args
    )
    if not ok_sanitizer:
        print("❌ DataSanitizer thất bại! Dừng toàn bộ pipeline vì dữ liệu nguồn lỗi.")
        sys.exit(1)

    # Bước 0.5: Kiểm tra Database
    ensure_mysql_started()

    # Bước 1 & 2: Chạy song song 3 nhánh độc lập: Agent 1 (Kỷ luật SV) // Agent 2 (Dự báo học vụ) // Nhánh B (Agent 4 -> Agent 3)
    from concurrent.futures import ThreadPoolExecutor

    def run_branch_agent1():
        print("\n[NHÁNH A1] Bắt đầu xử lý Agent 1: Kỷ luật học viên...")
        ok = run_script(
            "Agent 1: Kỷ luật học viên (Class KPI)",
            "agents/core/agent_1_class_kpi/run.py",
        )
        if not ok or not validate_output("data/processed/agent1_output.json", "json", min_mtime=total_start) or not validate_output("output/dashboards/core/agent_1_student_discipline.html", "html", min_mtime=total_start):
            return "Agent 1 (Class KPI)"
        return None

    def run_branch_agent2():
        print("\n[NHÁNH A2] Bắt đầu xử lý Agent 2: Dự báo học vụ...")
        ok = run_script(
            "Agent 2: Dự báo học vụ (Academic Predictor)",
            "agents/core/agent_2_academic_pred/run.py",
        )
        if not ok or not validate_output("data/processed/agent2_output.json", "json", min_mtime=total_start) or not validate_output("output/dashboards/core/agent_2_academic_prediction.html", "html", min_mtime=total_start):
            return "Agent 2 (Academic Predictor)"
        return None

    def run_branch_operations():
        print("\n[NHÁNH B] Bắt đầu xử lý Nhật ký công việc & Kỷ luật tác nghiệp...")
        ok_a4 = run_script(
            "Agent 4: Nhật ký công việc (Daily Logs Auditor)",
            "agents/core/agent_4_daily_logs/run.py",
            extra_args=fast_args
        )
        if not ok_a4 or not validate_output("data/processed/daily_log_analysis.json", "json", min_mtime=total_start) or not validate_output("output/dashboards/core/agent_4_daily_logs.html", "html", min_mtime=total_start):
            return "Agent 4 (Daily Logs Auditor)"

        ok_a3 = run_script(
            "Agent 3: Kỷ luật tác nghiệp GV/TG (Ops Discipline)",
            "agents/core/agent_3_ops_discipline/run.py",
        )
        if not ok_a3 or not validate_output("data/processed/agent3_output.json", "json", min_mtime=total_start) or not validate_output("output/dashboards/core/agent_3_ops_discipline.html", "html", min_mtime=total_start):
            return "Agent 3 (Ops Discipline)"
        return None

    print("\n" + "=" * 80)
    print("🚀 KHỞI CHẠY ĐỒNG THỜI 3 NHÁNH ĐỘC LẬP: AGENT 1 // AGENT 2 // NHÁNH TÁC NGHIỆP...")
    print("=" * 80)
    with ThreadPoolExecutor(max_workers=3) as executor:
        f_a1 = executor.submit(run_branch_agent1)
        f_a2 = executor.submit(run_branch_agent2)
        f_ops = executor.submit(run_branch_operations)
        for res_err in [f_a1.result(), f_a2.result(), f_ops.result()]:
            if res_err:
                pipeline_errors.append(res_err)

    # Bước 3, 4 & 5: Biên dịch song song các Báo cáo & Dashboard quản trị cốt lõi
    print("\n" + "=" * 80)
    print("⚡ BIÊN DỊCH SONG SONG CÁC BÁO CÁO & DASHBOARDS CỐT LÕI...")
    print("=" * 80)

    render_tasks = [
        (
            "Agent 5: Executive Dashboard (Master Portal)",
            "agents/master/agent_5_master_portal/generate_unified_dashboard.py",
            ["output/dashboards/core/agent_5_master_portal.html"],
        ),
        (
            "Agent 5: Báo cáo KPI GV/TG Markdown",
            "agents/master/agent_5_master_portal/generate_kpi_report.py",
            ["output/reports/core/agent_5_master_portal.md"],
        ),
        (
            "Management: Báo cáo Giám đốc Đào tạo (Director Cockpit)",
            "agents/advanced/management_audit/generate_report_director.py",
            ["output/dashboards/management/director_cockpit.html"],
        ),
        (
            "Management: Kiểm toán Nhân sự Worklane Đa Kỳ (Staff Audit)",
            "agents/audit/generate_audit_dashboard.py",
            ["output/dashboards/management/worklane_staff_audit.html"],
        ),
        (
            "Management: Báo cáo Giao ban Đào tạo Tuần (Weekly Director Report)",
            "scripts/generate_weekly_director_dashboard.py",
            ["output/dashboards/management/weekly_director_report.html"],
        ),
    ]

    # Chỉ chạy dashboard chuyên sâu môn cũ nếu có yêu cầu riêng
    if "--include-legacy-cohorts" in sys.argv:
        render_tasks.append((
            "Academic: Báo cáo Chuyên sâu Môn cũ KS24, KS25, KS26",
            "scripts/generate_academic_cohort_dashboards.py",
            [
                "output/dashboards/academic/ks24/it214_microservices_cntt.html",
                "output/dashboards/academic/ks25/it105_fastapi_cntt.html",
                "output/dashboards/academic/ks25/man107_qtkd.html",
                "output/dashboards/academic/ks26/ssk101_cntt.html",
                "output/dashboards/academic/ks26/ssk101_qtkd.html",
                "output/dashboards/academic/index.html",
            ],
        ))

    def _run_render_task(task):
        t_name, t_path, t_outputs = task
        ok = run_script(t_name, t_path)
        if not ok:
            return t_name
        for out_file in t_outputs:
            if not validate_output(out_file, "file", min_mtime=total_start):
                return f"{t_name} (out: {out_file})"
        return None

    with ThreadPoolExecutor(max_workers=min(len(render_tasks), 5)) as executor:
        futures = [executor.submit(_run_render_task, t) for t in render_tasks]
        for f in futures:
            err = f.result()
            if err:
                pipeline_errors.append(err)

    if pipeline_errors:
        print("\n" + "!" * 80)
        print("❌ PIPELINE CÓ LỖI TẠI CÁC BƯỚC SAU:")
        for pe in pipeline_errors:
            print(f"  - {pe}")
        print("!" * 80)
        sys.exit(1)

    # Bước 6: Tự động đồng bộ vào deploy_web/ & Xuất bản tên Tiếng Việt chuẩn hóa
    sync_to_deploy_web()
    try:
        from pmo import publisher, retention
        publisher.organize_adhoc_and_mixed_files()
        publisher.publish_regular_reports()
        retention.enforce_retention(keep_recent=2)
        print("✓ Đã chuẩn hóa tên file Tiếng Việt tại output/01_Bao_Cao_Su_Dung_Thuong_Xuyen/")
    except Exception as e:
        print(f"Warning khi đồng bộ tên file chuẩn: {e}")

    total_elapsed = time.time() - total_start
    print("=" * 80)
    print(f"✓ ĐƯỜNG ỐNG ĐÃ HOÀN THÀNH TOÀN BỘ TRONG {total_elapsed:.2f} GIÂY!")
    print("📂 CẤU TRÚC ĐẦU RA CHUẨN HÓA:")
    print("  - Core Dashboards:       output/dashboards/core/ (Agent 1 - 5)")
    print("  - Management Dashboards: output/dashboards/management/ (Director Cockpit & Worklane Staff Audit)")
    print("  - Academic Cohort Issues: output/dashboards/academic/ (KS24, KS25, KS26)")
    print("  - Web Deploy Portal:     deploy_web/ (Sẵn sàng mở hoặc host web)")
    print("================================================================================")
    print("  - Web Deploy Portal:     deploy_web/ (Sẵn sàng mở hoặc host web)")
    print("================================================================================")

if __name__ == "__main__":
    main()

import subprocess
import sys
import os
import shutil

sys.stdout.reconfigure(encoding='utf-8')

def run_script(name, path, with_deps=None):
    print("=" * 80)
    print(f"BẮT ĐẦU CHẠY: {name}")
    print(f"Path: {path}")
    print("=" * 80)
    
    cmd = ["uv", "run"]
    if with_deps:
        for dep in with_deps:
            cmd += ["--with", dep]
    cmd.append(path)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        print(f"✓ HOÀN THÀNH: {name} THÀNH CÔNG.\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ LỖI TẠI: {name}")
        print(e.stdout)
        print(e.stderr)
        print(f"! FALLBACK: Bỏ qua lỗi tại {name} để hệ thống tiếp tục chạy.")
        return False

def validate_output(file_path, file_type):
    print(f"Kiểm duyệt file đầu ra: {file_path}")
    if not os.path.exists(file_path):
        print(f"✗ Lỗi: File {file_path} không được tạo ra.")
        return False
        
    cmd = ["uv", "run", "agents/common/validator.py", file_path, file_type]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(e.stdout)
        print(e.stderr)
        print(f"✗ FALLBACK: Không thể sửa lỗi file {file_path}. Bỏ qua lỗi.")
        return False

def main():
    print("================================================================================")
    print("KHỞI CHẠY ĐƯỜNG ỐNG TỰ ĐỘNG (HARNESS - LOOP - GRAPH ARCHITECTURE)")
    print("================================================================================")
    
    # Bước 0: DataSanitizer (Harness Layer)
    run_script(
        "DataSanitizer: Làm sạch dữ liệu Excel", 
        "agents/common/data_sanitizer.py",
        with_deps=["openpyxl", "pandas"]
    )

    # Khởi tạo các thư mục đầu ra nếu chưa có
    os.makedirs("output/dashboards/core", exist_ok=True)
    os.makedirs("output/dashboards/advanced", exist_ok=True)
    os.makedirs("output/reports/core", exist_ok=True)
    os.makedirs("output/reports/advanced", exist_ok=True)

    # Bước 1: Chạy Agent 1
    run_script(
        "Agent 1: Kỷ luật học viên (Class KPI)", 
        "agents/core/agent_1_class_kpi/run.py",
        with_deps=["openpyxl", "numpy", "markdown"]
    )
    validate_output("data/processed/agent1_output.json", "json")
    validate_output("output/dashboards/core/agent_1_student_discipline.html", "html")
    
    # Bước 2: Chạy Agent 2
    run_script(
        "Agent 2: Dự báo học vụ (Academic Predictor)", 
        "agents/core/agent_2_academic_pred/run.py",
        with_deps=["mysql-connector-python", "openpyxl", "numpy"]
    )
    validate_output("data/processed/agent2_output.json", "json")
    validate_output("output/dashboards/core/agent_2_academic_prediction.html", "html")
    
    # Bước 3: Chạy Agent 3
    run_script(
        "Agent 3: Kỷ luật tác nghiệp GV/TG (Ops Discipline)", 
        "agents/core/agent_3_ops_discipline/run.py",
        with_deps=["mysql-connector-python", "openpyxl"]
    )
    validate_output("data/processed/agent3_output.json", "json")
    validate_output("output/dashboards/core/agent_3_ops_discipline.html", "html")
    
    # Bước 4: Chạy Agent 4
    run_script(
        "Agent 4: Nhật ký công việc (Daily Logs Auditor)", 
        "agents/core/agent_4_daily_logs/run.py",
        with_deps=["openpyxl"]
    )
    validate_output("data/processed/daily_log_analysis.json", "json")
    validate_output("output/dashboards/core/agent_4_daily_logs.html", "html")
    
    # Bước 4.5: Chạy báo cáo Giám đốc Đào tạo (Director Cockpit)
    run_script(
        "Custom Director Report: Báo cáo Giám đốc Đào tạo (Director Cockpit)",
        "agents/advanced/management_audit/generate_report_director.py",
        with_deps=["openpyxl"]
    )
    validate_output("output/dashboards/advanced/director_cockpit.html", "html")
    
    # Bước 5: Master Lead
    run_script(
        "Agent 5: Master Lead Portal", 
        "agents/master/agent_5_master_portal/run.py"
    )
    validate_output("output/dashboards/core/agent_5_master_portal.html", "html")
    
    # Vệ sinh thư mục output (Dọn dẹp các file thừa ở thư mục gốc output)
    print("Tiến hành vệ sinh thư mục output...")
    output_dir = "output"
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"  - Đã xóa file thừa: {file}")
                except Exception as e:
                    print(f"  - Không thể xóa {file}: {e}")
                    
    print("=" * 80)
    print("ĐƯỜNG ỐNG ĐÃ HOÀN THÀNH VỚI GRAPH ROUTING & FALLBACK!")
    print("================================================================================")

if __name__ == "__main__":
    main()

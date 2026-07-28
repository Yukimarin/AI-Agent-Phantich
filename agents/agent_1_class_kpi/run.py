import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("Agent 1: Khởi chạy quy trình phân tích kỷ luật học viên (run.py)...")
    
    # 1. Chạy calculate_kpi_json.py
    print("Agent 1: Chạy tính toán điểm KPI JSON...")
    res = subprocess.run([sys.executable, "agents/agent_1_class_kpi/calculate_kpi_json.py"], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("Error: Chạy calculate_kpi_json.py thất bại!")
        print(res.stderr)
        sys.exit(1)
        
    # 2. Chạy generate_kpi_report.py
    print("Agent 1: Chạy sinh báo cáo Markdown tuần...")
    res = subprocess.run([sys.executable, "agents/agent_1_class_kpi/generate_kpi_report.py"], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("Error: Chạy generate_kpi_report.py thất bại!")
        print(res.stderr)
        sys.exit(1)
        
    # 3. Chạy generate_report.py
    print("Agent 1: Chạy sinh trang báo cáo HTML...")
    res = subprocess.run([sys.executable, "agents/agent_1_class_kpi/generate_report.py"], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("Error: Chạy generate_report.py thất bại!")
        print(res.stderr)
        sys.exit(1)
        
    print("Agent 1: Quy trình đã hoàn tất thành công!")

if __name__ == "__main__":
    main()

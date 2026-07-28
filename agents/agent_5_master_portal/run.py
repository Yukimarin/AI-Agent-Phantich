import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("Agent 5: Bắt đầu chạy quy trình Master Portal (run.py)...")
    
    # 1. Chạy generate_kpi_report.py
    print("Agent 5: Chạy báo cáo tổng hợp KPI...")
    res = subprocess.run([sys.executable, "agents/agent_5_master_portal/generate_kpi_report.py"], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("Error: Chạy generate_kpi_report.py thất bại!")
        print(res.stderr)
        sys.exit(1)
        
    # 2. Chạy generate_unified_dashboard.py
    print("Agent 5: Sinh trang Web Dashboard tích hợp...")
    res = subprocess.run([sys.executable, "agents/agent_5_master_portal/generate_unified_dashboard.py"], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("Error: Chạy generate_unified_dashboard.py thất bại!")
        print(res.stderr)
        sys.exit(1)
        
    print("Agent 5: Master Portal đã hoàn tất xử lý thành công!")

if __name__ == "__main__":
    main()

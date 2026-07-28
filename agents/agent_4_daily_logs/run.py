import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("Agent 4: Khởi chạy quy trình nhật ký công việc (run.py)...")
    
    # 1. Chạy sync_worklane_projects.py để đồng bộ dự án từ Worklane
    print("Agent 4: Đồng bộ hóa dự án & tasks từ Worklane PM thời gian thực...")
    res = subprocess.run([sys.executable, "agents/agent_4_daily_logs/sync_worklane_projects.py"], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("Error: Chạy sync_worklane_projects.py thất bại!")
        print(res.stderr)
        sys.exit(1)

    # 1.5. Chạy analyze_daily_logs.py
    print("Agent 4: Phân tích báo cáo ngày & tiến độ...")
    res = subprocess.run([sys.executable, "agents/agent_4_daily_logs/analyze_daily_logs.py"], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("Error: Chạy analyze_daily_logs.py thất bại!")
        print(res.stderr)
        sys.exit(1)
        
    # 2. Chạy generate_report.py
    print("Agent 4: Sinh trang báo cáo HTML (PMO Dashboard V4)...")
    res = subprocess.run([sys.executable, "agents/agent_4_daily_logs/generate_report_v4.py"], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("Error: Chạy generate_report.py thất bại!")
        print(res.stderr)
        sys.exit(1)
        
    print("Agent 4: Quy trình đã hoàn tất thành công!")

if __name__ == "__main__":
    main()

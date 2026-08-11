import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("Agent 3: Khởi chạy quy trình kỷ luật tác nghiệp GV/TG (run.py)...")
    
    # 1. Chạy analyze_gvtg_violations.py
    print("Agent 3: Phân tích lỗi vi phạm tác nghiệp...")
    res = subprocess.run([sys.executable, "agents/core/agent_3_ops_discipline/analyze_gvtg_violations.py"], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("Error: Chạy analyze_gvtg_violations.py thất bại!")
        print(res.stderr)
        sys.exit(1)
        
    # 2. Chạy generate_report.py
    print("Agent 3: Sinh trang báo cáo HTML...")
    res = subprocess.run([sys.executable, "agents/core/agent_3_ops_discipline/generate_report.py"], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("Error: Chạy generate_report.py thất bại!")
        print(res.stderr)
        sys.exit(1)
        
    print("Agent 3: Quy trình đã hoàn tất thành công!")

if __name__ == "__main__":
    main()

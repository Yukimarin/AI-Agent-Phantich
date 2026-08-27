import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Ensure the module path is accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import analyze_gvtg_violations
import generate_report

def main():
    print("Agent 3: Khởi chạy quy trình kỷ luật tác nghiệp GV/TG (run.py)...")
    
    print("Agent 3: Phân tích lỗi vi phạm tác nghiệp...")
    analyze_gvtg_violations.main()
    
    print("Agent 3: Sinh trang báo cáo HTML...")
    generate_report.main()
    
    print("Agent 3: Quy trình đã hoàn tất thành công!")

if __name__ == "__main__":
    main()

import subprocess
import sys
import os
import shutil

sys.stdout.reconfigure(encoding='utf-8')

def run_step(name, args):
    print("=" * 80)
    print(f"BẮT ĐẦU BƯỚC: {name}")
    print("=" * 80)
    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        print(f"HOÀN THÀNH: {name} THÀNH CÔNG.\n")
    except subprocess.CalledProcessError as e:
        print(f"LỖI TẠI BƯỚC: {name}")
        print(e.stderr)
        sys.exit(1)

def main():
    print("Khởi chạy đường ống tích hợp báo cáo học vụ PTITxRikkei...\n")
    
    # Copy/Rename Agent 1 output if exists
    if os.path.exists("output/kpi_report.html"):
        try:
            shutil.copy("output/kpi_report.html", "output/1_kpi_report.html")
            print("Đã tạo bản sao báo cáo Agent 1: output/1_kpi_report.html")
        except Exception as e:
            print(f"Không thể sao chép kpi_report.html: {e}")
            
    # dependencies yêu cầu
    deps = [
        "--with", "mysql-connector-python",
        "--with", "openpyxl",
        "--with", "numpy",
        "--with", "pandas",
        "--with", "markdown"
    ]

    # Bước 1: Chạy mô hình dự báo nguy cơ trượt học tập của học viên
    run_step("1. Dự báo nguy cơ trượt học tập (analyze_student_risk_real)", 
             ["uv", "run"] + deps + ["scratch/analyze_student_risk_real.py"])

    # Bước 1.2: Xuất bản dashboard học lực Agent 2 (export_prediction_dashboard_html)
    run_step("1.2. Xuất bản dashboard học lực Agent 2 (export_prediction_dashboard_html)", 
             ["uv", "run"] + deps + ["scratch/export_prediction_dashboard_html.py"])

    # Bước 2: Phân tích vi phạm kỷ luật tác nghiệp GV/TG (analyze_gvtg_violations)
    run_step("2. Phân tích vi phạm kỷ luật tác nghiệp GV/TG (analyze_gvtg_violations)", 
             ["uv", "run"] + deps + ["scratch/analyze_gvtg_violations.py"])

    # Bước 2.2: Xuất bản báo cáo tác nghiệp Agent 3 (generate_agent3_report)
    run_step("2.2. Xuất bản báo cáo tác nghiệp Agent 3 (generate_agent3_report)", 
             ["uv", "run"] + deps + ["scratch/generate_agent3_report.py"])

    # Bước 2.5: Phân tích chất lượng báo cáo ngày GV/TG qua MCP (analyze_daily_logs_mcp)
    run_step("2.5. Phân tích chất lượng báo cáo ngày GV/TG qua MCP (analyze_daily_logs_mcp)", 
             ["uv", "run"] + deps + ["scratch/analyze_daily_logs_mcp.py"])

    # Bước 2.7: Xuất bản báo cáo nhật ký công việc Agent 4 (generate_agent4_report)
    run_step("2.7. Xuất bản báo cáo nhật ký công việc Agent 4 (generate_agent4_report)", 
             ["uv", "run"] + deps + ["scratch/generate_agent4_report.py"])

    # Bước 3: Chạy tính toán điểm KPI GV/TG và sinh báo cáo tổng hợp
    run_step("3. Tính toán KPI GV/TG & Báo cáo Obsidian Wiki-link (generate_kpi_report)", 
             ["uv", "run"] + deps + ["scratch/generate_kpi_report.py"])

    # Bước 4: Chạy bộ kiểm thử Harness đánh giá sai số thuật toán
    run_step("4. Kiểm thử hiệu năng thuật toán (evaluation_harness)", 
             ["uv", "run"] + deps + ["scratch/evaluation_harness.py"])

    # Bước 5: Sinh Web Dashboard tích hợp 2 Tab (Đánh giá GV/TG & Dự báo Học lực)
    run_step("5. Sinh Web Dashboard tích hợp 2 Tab (generate_unified_dashboard)", 
             ["uv", "run"] + deps + ["scratch/generate_unified_dashboard.py"])
             
    # Sao chép tệp dashboard tích hợp ra gốc dự án để đồng nhất đường dẫn mở
    if os.path.exists("output/5_master_evaluation_dashboard.html"):
        try:
            with open("output/5_master_evaluation_dashboard.html", "r", encoding="utf-8") as f:
                content = f.read()
            
            with open("unified_dashboard.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("Đã đồng bộ báo cáo tổng hợp Agent 5 ra gốc dự án: unified_dashboard.html (SPA Native).")
        except Exception as e:
            print(f"Không thể sao chép ra gốc: {e}")

    # Vệ sinh thư mục output (Dọn dẹp các file thừa theo yêu cầu)
    print("\nTiến hành vệ sinh thư mục output...")
    output_dir = "output"
    whitelist = [
        "1_kpi_report.html", 
        "2_class_predictions_dashboard.html", 
        "3_gvtg_violations_report.html", 
        "4_daily_logs_report.html", 
        "5_master_evaluation_dashboard.html"
    ]
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            if os.path.isfile(file_path) and file not in whitelist:
                try:
                    os.remove(file_path)
                    print(f"  - Đã xóa file thừa: {file}")
                except Exception as e:
                    print(f"  - Không thể xóa {file}: {e}")

    print("=" * 80)
    print("ĐƯỜNG ỐNG ĐÃ HOÀN THÀNH TOÀN BỘ!")
    print("Các báo cáo đã được cập nhật sẵn sàng trong Obsidian Vault:")
    print("  - [x] Báo cáo Nguy cơ Học viên: data/student_risk_report.md")
    print("  - [x] Báo cáo KPI GV/TG: data/report_kpi_gv_tg.md")
    print("  - [x] Báo cáo Hiệu năng Mô hình: data/evaluation_metrics.md")
    print("  - [x] Web Dashboard tích hợp: output/5_master_evaluation_dashboard.html")
    print("=" * 80)

if __name__ == "__main__":
    main()

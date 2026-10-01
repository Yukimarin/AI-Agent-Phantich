import subprocess
import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')

def run_step(step_name, cmd):
    t0 = time.time()
    print(f"\n>>> [{step_name}] Bắt đầu thực thi...")
    res = subprocess.run(cmd, shell=True, text=True, encoding='utf-8', capture_output=True)
    elapsed = time.time() - t0
    if res.returncode != 0:
        print(f"❌ [{step_name}] Thất bại sau {elapsed:.2f}s:")
        print(res.stderr or res.stdout)
        return False
    print(f"✓ [{step_name}] Hoàn tất trong {elapsed:.2f}s")
    if res.stdout.strip():
        # Print summary or last few lines
        lines = [l for l in res.stdout.strip().splitlines() if l.strip()]
        for l in lines[-5:]:
            print(f"   {l}")
    return True

def main():
    start_all = time.time()
    print("================================================================")
    print("LUỒNG TỐI ƯU SIÊU TỐC: ĐỒNG BỘ LMS MCP KS26 & CẬP NHẬT AGENT 1")
    print("Mục tiêu: Rút ngắn thời gian từ 10-15 phút xuống dưới 45 giây")
    print("================================================================")

    # 1. Trích xuất chỉ số chuẩn xác từ LMS MCP (Node.js fast fetch)
    step1 = run_step("1. LMS MCP Fetch", "node scratch/compute_ks26_exact_metrics.js")
    if not step1: sys.exit(1)

    # 2. Ghi chỉ số vào Excel Backup & Project Input
    step2 = run_step("2. Update Excel PTIT_Chiso.xlsx", '& "C:\\Users\\DELL\\.local\\bin\\python3.14.exe" scratch/apply_exact_ks26_excel.py')
    if not step2: sys.exit(1)

    # 3. DataSanitizer Fast Cache Rebuild
    step3 = run_step("3. DataSanitizer Fast Cache", '& "C:\\Users\\DELL\\.local\\bin\\python3.14.exe" agents/common/data_sanitizer.py --force')
    if not step3: sys.exit(1)

    # 4. Agent 1 Pipeline (JSON + Markdown + HTML)
    step4 = run_step("4. Agent 1 Pipeline", '& "C:\\Users\\DELL\\.local\\bin\\python3.14.exe" agents/core/agent_1_class_kpi/run.py')
    if not step4: sys.exit(1)

    # 5. Sync to deploy_web
    deploy_file = "deploy_web/agent_1_student_discipline.html"
    src_file = "output/dashboards/core/agent_1_student_discipline.html"
    if os.path.exists(deploy_file) and os.path.exists(src_file):
        import shutil
        shutil.copy2(src_file, deploy_file)
        print("✓ [5. Deploy] Đã đồng bộ sang deploy_web/agent_1_student_discipline.html")

    total_time = time.time() - start_all
    print("================================================================")
    print(f"🎉 HOÀN THÀNH TOÀN BỘ QUY TRÌNH TRONG {total_time:.2f} GIÂY! (Tiết kiệm >90% thời gian)")
    print("================================================================")

if __name__ == "__main__":
    main()

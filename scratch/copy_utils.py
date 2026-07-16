import shutil
import os

src_dir = r"C:\Users\DELL\Desktop\Education-DB-Analytic\scratch"
dst_dir = r"c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\scratch"

files_to_copy = ['excel_loader.py', 'metrics_engine.py']

for f in files_to_copy:
    src_file = os.path.join(src_dir, f)
    dst_file = os.path.join(dst_dir, f)
    if os.path.exists(src_file):
        shutil.copy2(src_file, dst_file)
        print(f"Copied {src_file} to {dst_file}")
    else:
        print(f"Source file {src_file} does not exist!")

import os
import shutil

src_dir = r"C:\Users\DELL\Desktop\Education-DB-Analytic\.agent\skills"
dst_dir = r"c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\.agents\skills"

if not os.path.exists(src_dir):
    print(f"Source directory {src_dir} does not exist!")
else:
    if os.path.exists(dst_dir):
        print(f"Destination directory {dst_dir} already exists. Removing it first...")
        shutil.rmtree(dst_dir)
    
    shutil.copytree(src_dir, dst_dir)
    print(f"Successfully copied skills from {src_dir} to {dst_dir}")
    
    # List the copied skills
    copied_skills = os.listdir(dst_dir)
    print(f"Copied skills: {copied_skills}")

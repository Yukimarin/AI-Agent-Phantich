import os

file_path = r"C:\Users\DELL\Desktop\Education-DB-Analytic\qldt_el-06-16-26.sql"
if os.path.exists(file_path):
    print("File exists, size:", os.path.getsize(file_path))
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for i in range(50):
            line = f.readline()
            if not line:
                break
            print(f"{i+1}: {line.strip()}")
else:
    print("File does not exist")

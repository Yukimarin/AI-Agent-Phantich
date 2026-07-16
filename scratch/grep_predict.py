import os

src_dir = r"C:\Users\DELL\Desktop\Education-DB-Analytic\scratch"
query = "predict"

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".py") or file.endswith(".md"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f):
                        if query in line.lower():
                            print(f"{file}:{i+1}: {line.strip()[:100]}")
            except Exception as e:
                pass

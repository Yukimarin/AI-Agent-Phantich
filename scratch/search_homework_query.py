import os

keywords = ['attendance_detail', 'late_submissions', 'elearning_late', 'rpoints']
scratch_dir = 'scratch'

for root, dirs, files in os.walk(scratch_dir):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                for kw in keywords:
                    if kw in content:
                        print(f"File: {path} contains keyword: {kw}")
            except Exception as e:
                pass

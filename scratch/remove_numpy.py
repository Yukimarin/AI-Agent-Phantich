import re

def main():
    filepath = "scratch/run_academic_predictions_v3.py"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace import
    content = content.replace("import numpy as np", """def mean(lst):
    return sum(lst) / len(lst) if lst else 0.0""")
    
    # Replace np.mean calls
    content = re.sub(r'np\.mean\(([^)]+)\)', r'mean(\1)', content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Successfully removed numpy dependency from run_academic_predictions_v3.py")

if __name__ == "__main__":
    main()

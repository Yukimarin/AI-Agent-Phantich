import re
import subprocess
import os

filepath = "output/5_unified_dashboard.html"
if not os.path.exists(filepath):
    print("File not found")
    exit(1)

with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Extract the script blocks
scripts = re.findall(r"<script>(.*?)</script>", html, re.DOTALL)
print(f"Found {len(scripts)} script blocks.")

# Save them to a JS file for linting
js_content = ""
for idx, script in enumerate(scripts):
    # Skip Tailwind script if loaded as <script src=...> but we are only matching block scripts anyway
    js_content += f"\n// --- Script Block {idx} ---\n" + script

js_filepath = "scratch/temp_extracted.js"
with open(js_filepath, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Saved extracted JS to {js_filepath}")

# Run node --check
try:
    res = subprocess.run(["node", "--check", js_filepath], capture_output=True, text=True, check=True)
    print("Node JS Check Result: SUCCESS (No syntax errors found!)")
except subprocess.CalledProcessError as e:
    print("Node JS Check Result: FAILED (Syntax errors found!)")
    print(e.stderr)

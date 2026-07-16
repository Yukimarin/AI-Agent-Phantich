import re

with open("output/5_unified_dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find placeholders that look like {name} where name is lowercase and contains underscores
placeholders = re.findall(r'\{[a-z0-9_]+\}', content)
print("Found placeholders:")
print(placeholders)

# Check if there is any javascript syntax error like undefined variables
# or unresolved tags
print("\nChecking for common error patterns...")
for line_no, line in enumerate(content.split('\n')):
    if 'undefined' in line or 'NaN' in line or 'null' in line:
        if line_no < 50 or line_no > 1650:
            print(f"Line {line_no+1}: {line.strip()}")

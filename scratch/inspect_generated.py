import os

filepath = "output/5_unified_dashboard.html"
if not os.path.exists(filepath):
    print("File not found")
else:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    print("File length:", len(content))
    
    # Check for placeholder strings that might not have been replaced
    placeholders = ["{tab3_body}", "{tab3_js}", "{raw_json_str}"]
    for p in placeholders:
        if p in content:
            print(f"WARNING: Placeholder {p} still exists in the generated HTML!")
        else:
            print(f"OK: Placeholder {p} was replaced.")
            
    # Print tab-daily-logs-container block
    idx = content.find("tab-daily-logs-container")
    if idx != -1:
        print("\n--- tab-daily-logs-container block ---")
        tab3_section = content[idx:idx+2000]
        # Write to a file to inspect
        with open("scratch/tab3_content.txt", "w", encoding="utf-8") as f:
            f.write(tab3_section)
        print("Tab 3 content written to scratch/tab3_content.txt")
    else:
        print("\nCould not find tab-daily-logs-container")
        
    # Print tab3_js block
    idx_js = content.find("tab3StaffScores")
    if idx_js != -1:
        print("\n--- tab3StaffScores js block ---")
        js_section = content[idx_js-100:idx_js+4000]
        with open("scratch/tab3_js.txt", "w", encoding="utf-8") as f:
            f.write(js_section)
        print("Tab 3 JS content written to scratch/tab3_js.txt")
    else:
        print("\nCould not find tab3StaffScores")

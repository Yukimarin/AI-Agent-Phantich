import json
import os

workspace_path = "c:\\Users\\DELL\\Desktop\\AI-Agent\\AI_PhantichchisoDT\\.obsidian\\workspace.json"

if not os.path.exists(workspace_path):
    print("No workspace.json found.")
    exit(0)

try:
    with open(workspace_path, "r", encoding="utf-8") as f:
        data = f.read()

    # Replace old map names in history and active tabs
    data_cleaned = data.replace("docs/knowledge_map.md", "docs/Bản đồ Tri thức MOC.md")
    data_cleaned = data_cleaned.replace("knowledge_map.md", "Bản đồ Tri thức MOC.md")
    
    # We will parse as JSON to remove any tab containing Untitled
    workspace_json = json.loads(data_cleaned)
    
    def clean_leaves(leaves):
        cleaned = []
        for leaf in leaves:
            state = leaf.get("state", {})
            file_path = state.get("state", {}).get("file", "")
            if "Untitled" in file_path or "knowledge_map" in file_path:
                print(f"Removing ghost leaf from workspace tabs: {file_path}")
                continue # Skip/remove this tab
            
            # Recurse if there are children/tabs inside
            if "children" in leaf:
                clean_leaves(leaf["children"])
            cleaned.append(leaf)
        return cleaned

    # Clean main split tabs
    if "main" in workspace_json and "children" in workspace_json["main"]:
        # Traverse splits
        def traverse_and_clean(node):
            if "children" in node:
                for child in node["children"]:
                    traverse_and_clean(child)
            if "leaves" in node:
                node["leaves"] = clean_leaves(node["leaves"])
                
        traverse_and_clean(workspace_json["main"])
        
    # Clean file history (recent files list)
    if "recentFiles" in workspace_json:
        rf_cleaned = []
        for f in workspace_json["recentFiles"]:
            if "Untitled" in f or "knowledge_map" in f:
                continue
            rf_cleaned.append(f)
        workspace_json["recentFiles"] = rf_cleaned
        
    with open(workspace_path, "w", encoding="utf-8") as f:
        json.dump(workspace_json, f, ensure_ascii=False, indent=2)
        
    print("Obsidian workspace.json cleaned successfully!")

except Exception as e:
    print(f"Error cleaning workspace.json: {e}")

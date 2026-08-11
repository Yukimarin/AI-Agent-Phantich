import urllib.request
import urllib.error
import json
import ssl
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def call_mcp_tool(tool_name, arguments={}):
    url = "https://pm.rikkei.edu.vn/api/mcp"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    headers = {
        "Authorization": "Bearer wl_jtpd1dOgxnUm5n2d7V6dxBT_AZHNrnCK",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        url, 
        data=json.dumps(payload).encode("utf-8"), 
        headers=headers, 
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            resp_str = response.read().decode("utf-8")
            for line in resp_str.split("\n"):
                if line.startswith("data:"):
                    json_str = line[5:].strip()
                    data = json.loads(json_str)
                    
                    if "error" in data:
                        print(f"DEBUG: MCP Server returned error for {tool_name}: {data['error']}")
                        return None
                        
                    content = data.get("result", {}).get("content", [])
                    for item in content:
                        text = item.get("text", "")
                        try:
                            return json.loads(text)
                        except Exception as parse_err:
                            return text
    except Exception as e:
        print(f"Error calling {tool_name} with args {arguments}: {e}")
    return None

def sync_projects():
    print("Fetching projects from Worklane for department 'DT'...")
    projects_result = call_mcp_tool("list_projects", {"department": "DT"})
    if not projects_result:
        print("Failed to fetch projects from Worklane API.")
        return

    projects_list = []
    if isinstance(projects_result, list):
        projects_list = projects_result
    elif isinstance(projects_result, dict):
        if "projects" in projects_result:
            projects_list = projects_result["projects"]
        else:
            for val in projects_result.values():
                if isinstance(val, list):
                    projects_list = val
                    break

    if not projects_list:
        print("Failed to fetch projects or projects list is empty.")
        return

    print(f"Found {len(projects_list)} projects. Fetching issues for each project...")
    project_issues_data = {}

    for idx, proj in enumerate(projects_list):
        key = proj.get("key")
        name = proj.get("name")
        status = proj.get("status")
        health = proj.get("health", "ON_TRACK")
        pic = proj.get("pic")

        print(f"[{idx+1}/{len(projects_list)}] Fetching issues for project {key} ({name})...")
        
        issues_result = call_mcp_tool("list_issues", {"project": key})
        issues_list = []
        if isinstance(issues_result, list):
            issues_list = issues_result
        elif isinstance(issues_result, dict) and "issues" in issues_result:
            issues_list = issues_result["issues"]
            
        print(f" -> Found {len(issues_list)} issues.")

        project_issues_data[key] = {
            "project_info": {
                "key": key,
                "slug": proj.get("slug"),
                "name": name,
                "status": status,
                "health": health,
                "pic": {"name": pic.get("name")} if pic else None
            },
            "issues": {
                "project": f"{key} — {name}",
                "count": len(issues_list),
                "issues": []
            }
        }

        for issue in issues_list:
            project_issues_data[key]["issues"]["issues"].append({
                "code": issue.get("code"),
                "title": issue.get("title"),
                "state": issue.get("state"),
                "priority": issue.get("priority", "NONE"),
                "assignee": issue.get("assignee"),
                "dueDate": issue.get("dueDate")
            })

    output_path = "data/processed/project_issues_worklane.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(project_issues_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully synced all projects and issues to {output_path}")

if __name__ == "__main__":
    sync_projects()

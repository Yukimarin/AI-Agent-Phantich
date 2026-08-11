import urllib.request
import urllib.error
import json
import ssl
import sys

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
                    return data
    except Exception as e:
        print(f"Error calling {tool_name}:", e)
    return None

dates = ["2026-07-27", "2026-07-28", "2026-07-29", "2026-07-30", "2026-07-31", "2026-08-01"]
reports_list = []

for d in dates:
    res = call_mcp_tool("list_daily_reports", {"date": d, "department": "DT"})
    if res and "result" in res:
        try:
            inner_str = res["result"]["content"][0].get("text", "")
            inner_json = json.loads(inner_str)
            reports = inner_json.get("reports", [])
            for r in reports:
                user = r.get("user")
                # Look for difficulties, issues, note, problem, etc.
                diff = r.get("difficulties") or r.get("difficulty") or r.get("issue") or r.get("issues") or r.get("note") or r.get("khó khăn")
                
                # Check for "khó khăn" or "difficulties" explicitly
                if diff and str(diff).strip():
                    reports_list.append({"date": d, "user": user, "difficulty": diff})
                else:
                    # Look through all keys and if any value contains "khó khăn", extract it
                    for k, v in r.items():
                        if v and isinstance(v, str) and ("khó khăn" in k.lower() or "vấn đề" in k.lower() or "issue" in k.lower() or "difficult" in k.lower()):
                            reports_list.append({"date": d, "user": user, "difficulty": f"{k}: {v}"})
        except Exception as e:
            pass

print(json.dumps(reports_list, ensure_ascii=False, indent=2))

print("\n--- SAMPLE RAW REPORT ---")
res = call_mcp_tool("list_daily_reports", {"date": "2026-07-27", "department": "DT"})
if res and "result" in res:
    try:
        inner_str = res["result"]["content"][0].get("text", "")
        inner_json = json.loads(inner_str)
        reports = inner_json.get("reports", [])
        if reports:
            print(json.dumps(reports[0], indent=2, ensure_ascii=False))
    except Exception as e:
        pass

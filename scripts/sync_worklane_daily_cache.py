import urllib.request
import urllib.error
import json
import ssl
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')


def _worklane_token():
    """Đọc WORKLANE_TOKEN từ biến môi trường hoặc file .env ở thư mục gốc (không ghi cứng bí mật)."""
    token = os.environ.get("WORKLANE_TOKEN", "").strip()
    if not token and os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8-sig") as f:
            for line in f:
                k, _, v = line.strip().partition("=")
                if k.strip() == "WORKLANE_TOKEN":
                    token = v.strip().strip('"').strip("'")
    if not token:
        raise SystemExit("Thiếu WORKLANE_TOKEN trong .env (dòng: WORKLANE_TOKEN=<token>).")
    return token


def call_worklane(tool_name, arguments={}):
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
        "Authorization": f"Bearer {_worklane_token()}",
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
        with urllib.request.urlopen(req, context=ctx, timeout=60) as response:
            resp_str = response.read().decode("utf-8")
            for line in resp_str.split("\n"):
                if line.startswith("data:"):
                    json_str = line[5:].strip()
                    data = json.loads(json_str)
                    content = data.get("result", {}).get("content", [])
                    for item in content:
                        text = item.get("text", "")
                        try:
                            return json.loads(text)
                        except:
                            return text
    except Exception as e:
        print(f"Error calling {tool_name} with {arguments}: {e}")
    return None

def main():
    cache_path = "data/processed/daily_reports_raw_cache.json"
    raw_cache = {}
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            raw_cache = json.load(f)

    # Dùng: uv run python scripts/sync_worklane_daily_cache.py 2026-09-28 2026-09-29 ...
    target_dates = sys.argv[1:]
    if not target_dates:
        raise SystemExit("Cần truyền danh sách ngày YYYY-MM-DD.")
    updated = False
    failed = []

    for d in target_dates:
        print(f"Fetching Worklane daily reports for {d}...")
        res = call_worklane("list_daily_reports", {"date": d, "department": "DT"})
        if res and isinstance(res, dict):
            reports = res.get("reports", [])
            print(f"  -> {d}: {len(reports)} reports received.")
            raw_cache[d] = reports
            updated = True
        else:
            failed.append(d)
            print(f"  -> {d}: no reports or empty response.")
    if failed:
        print(f"⚠️ CẢNH BÁO: không lấy được dữ liệu các ngày {failed} — số liệu tuần sẽ thiếu, kiểm tra lại trước khi dùng.")

    if updated:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(raw_cache, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved updated daily reports cache to {cache_path} (Total dates: {len(raw_cache)})")

if __name__ == "__main__":
    main()

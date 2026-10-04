"""LMS MCP connector (JSON-RPC 2.0 over HTTP POST). Chỉ Data Agent được dùng."""
from __future__ import annotations

import json
import time
import urllib.request
from typing import Any

from pmo.config import LMS_API_URL, lms_token


class LmsError(RuntimeError):
    pass


def call_tool(name: str, arguments: dict | None = None, timeout: int = 60, retries: int = 2) -> Any:
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000),
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments or {}},
    }).encode("utf-8")
    req = urllib.request.Request(
        LMS_API_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {lms_token()}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "pmo-data-hub/0.1 (+node-compatible)",
        },
    )
    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            break
        except Exception as e:  # mạng chập chờn: thử lại có giãn cách
            last_err = e
            code = getattr(e, "code", None)
            if isinstance(code, int) and 400 <= code < 500 and code != 429:
                raise LmsError(f"{name}: HTTP {code} (kiểm tra LMS_TOKEN / quyền truy cập)") from e
            time.sleep((5.0 if code == 429 else 1.5) * (attempt + 1))  # 429: LMS giới hạn tần suất
    else:
        raise LmsError(f"{name} thất bại sau {retries + 1} lần: {last_err}")

    if "error" in payload:
        raise LmsError(f"{name}: {payload['error']}")
    content = (payload.get("result") or {}).get("content") or []
    if not content:
        raise LmsError(f"{name}: phản hồi rỗng")
    text = content[0].get("text", "")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise LmsError(f"{name}: phản hồi không phải JSON: {text[:200]}")

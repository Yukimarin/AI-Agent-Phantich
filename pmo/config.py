"""Cấu hình tập trung: đường dẫn, endpoint, token (đọc từ môi trường, KHÔNG hardcode)."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAREHOUSE_DIR = ROOT / "data" / "warehouse"
OUTPUT_DIR = ROOT / "output"
CONFIG_DIR = ROOT / "config"
GOLDEN_DIR = ROOT / "tests" / "golden"

LMS_API_URL = "https://lmsapi.rikkeiedu.com/v1/mcp/analytics"

# Môn đang theo dõi (Orientation, SSK101, SKL01, SSK102, SSK103 đã kết thúc) — đồng bộ với scripts/fetch_ks26_live.js
TRACKED_COURSES = ["IT108-K26", "MAN101", "ENG105-K26", "JPN105-K26", "IT206-K26", "SSK101", "SEL101"]

# Dữ liệu cũ hơn số giờ này bị Gate 1 coi là quá hạn
MAX_DATA_AGE_HOURS = 24 * 7
# Raw LMS trong một kỳ phải cùng một lần lấy: chênh lệch giờ ghi tối đa giữa các file
MAX_RAW_SPREAD_HOURS = 2


def _load_dotenv() -> None:
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def lms_token() -> str:
    _load_dotenv()
    token = os.environ.get("LMS_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "Thiếu LMS_TOKEN. Tạo file .env ở thư mục gốc với dòng: LMS_TOKEN=<token> "
            "(không có tiền tố 'Bearer')."
        )
    return token.removeprefix("Bearer ").strip()

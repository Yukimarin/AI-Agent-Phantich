"""GATE 1 — Dữ liệu. Chạy sau Data Agent, trước khi tính chỉ số."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

from pmo.config import MAX_DATA_AGE_HOURS, MAX_RAW_SPREAD_HOURS
from pmo.data_agent import raw_name
from pmo.gates.base import FAIL, PASS, WARN, Check
from pmo.registry import is_valid_course_class_id
from pmo.warehouse import Snapshot

G = "G1 Dữ liệu"


def run(snapshot: Snapshot, now: datetime | None = None) -> list[Check]:
    now = now or datetime.now(timezone.utc)
    checks: list[Check] = []
    registry = snapshot.read_json("registry.json", [])
    fetch = snapshot.manifest().get("stages", {}).get("fetch", {})
    tracked = [r for r in registry if r["tracked"]]

    checks.append(Check(G, "Registry có dữ liệu", PASS if tracked else FAIL,
                        f"{len(tracked)} lớp-môn đang theo dõi" if tracked else "Registry rỗng"))

    bad_ids = [f"{r['className']}/{r['courseCode']}: '{r['courseClassId']}'"
               for r in tracked if not is_valid_course_class_id(r["courseClassId"])]
    checks.append(Check(G, "courseClassId hợp lệ", FAIL if bad_ids else PASS,
                        f"{len(bad_ids)} mã không hợp lệ" if bad_ids else "Tất cả hợp lệ", bad_ids))

    errs = [f"{e['courseClassId']}: {e['error']}" for e in fetch.get("errors", [])]
    checks.append(Check(G, "Lấy dữ liệu không lỗi", FAIL if errs else PASS,
                        f"{len(errs)} lỗi khi gọi LMS" if errs else "Không lỗi", errs))

    changed = fetch.get("registryChanges", [])
    if changed:
        checks.append(Check(G, "Mã lớp tự cập nhật từ LMS", WARN,
                            f"{len(changed)} courseClassId trong seed đã cũ, đã dùng mã hiện hành", changed))

    valid = [r for r in tracked if is_valid_course_class_id(r["courseClassId"])]
    missing = [f"{r['className']}/{r['courseCode']}" for r in valid if not snapshot.exists(raw_name(r["courseClassId"]))]
    checks.append(Check(G, "Đủ dữ liệu gốc cho mọi lớp-môn", FAIL if missing else PASS,
                        f"Thiếu {len(missing)}" if missing else f"Đủ {len(valid)}", missing))

    # Độ mới
    data_at = fetch.get("dataAt")
    if not data_at:
        checks.append(Check(G, "Độ mới dữ liệu", FAIL, "Không rõ thời điểm lấy dữ liệu"))
    else:
        age_h = (now - datetime.fromisoformat(data_at)).total_seconds() / 3600
        checks.append(Check(G, "Độ mới dữ liệu", FAIL if age_h > MAX_DATA_AGE_HOURS else PASS,
                            f"Lấy lúc {data_at} ({age_h:.1f} giờ trước)"))

    # Bài học 09/10: raw cache cũ trộn với raw mới (refresh lỗi giữa chừng rồi chạy lại không --refresh)
    mtimes = {}
    for r in valid:
        p = snapshot.path(raw_name(r["courseClassId"]))
        if p.exists():
            mtimes[f"{r['className']}/{r['courseCode']}"] = p.stat().st_mtime
    if mtimes:
        newest = max(mtimes.values())
        lagging = [f"{k} (cũ hơn {(newest - t) / 3600:.1f} giờ)" for k, t in mtimes.items()
                   if (newest - t) / 3600 > MAX_RAW_SPREAD_HOURS]
        checks.append(Check(G, "Dữ liệu gốc cùng một lần lấy", FAIL if lagging else PASS,
                            f"{len(lagging)} lớp-môn dùng raw cũ — xóa file raw tương ứng hoặc chạy --refresh"
                            if lagging else f"Chênh lệch ≤ {MAX_RAW_SPREAD_HOURS} giờ", lagging))

    # Bài học #3: sĩ số 0 trong khi cùng môn ở lớp khác đang có SV ⇒ nghi courseClassId cũ
    sizes: dict[str, int] = {}
    for r in valid:
        raw = snapshot.read_json(raw_name(r["courseClassId"]))
        if raw is not None:
            sizes[r["courseClassId"]] = len(raw.get("students") or [])
    running = defaultdict(int)
    for r in valid:
        if sizes.get(r["courseClassId"], 0) > 0:
            running[r["courseCode"]] += 1
    stale, not_started = [], []
    for r in valid:
        if r["courseClassId"] in sizes and sizes[r["courseClassId"]] == 0:
            label = f"{r['className']}/{r['courseCode']} ({r['courseClassId']})"
            (stale if running[r["courseCode"]] > 0 else not_started).append(label)
    checks.append(Check(G, "Sĩ số 0 bất thường (nghi mã lớp cũ)", FAIL if stale else PASS,
                        f"{len(stale)} lớp-môn sĩ số 0 trong khi lớp khác cùng môn đang học" if stale else "Không có",
                        stale))
    if not_started:
        checks.append(Check(G, "Môn chưa bắt đầu", WARN,
                            f"{len(not_started)} lớp-môn sĩ số 0 (môn chưa chạy ở lớp nào)", not_started))

    # Biến động sĩ số so với kỳ trước
    prev = snapshot.previous()
    if prev:
        jumps = []
        for cid, n in sizes.items():
            p = prev.read_json(raw_name(cid))
            if p is not None:
                pn = len(p.get("students") or [])
                if pn and abs(n - pn) / pn > 0.2:
                    jumps.append(f"{cid}: {pn} → {n}")
        checks.append(Check(G, f"Biến động sĩ số so với {prev.period}", WARN if jumps else PASS,
                            f"{len(jumps)} lớp-môn thay đổi > 20%" if jumps else "Ổn định", jumps))
    return checks

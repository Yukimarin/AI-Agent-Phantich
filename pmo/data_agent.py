"""DATA AGENT — agent duy nhất lấy dữ liệu từ nguồn. Lấy 1 lần mỗi kỳ, có cache.

Đầu ra trong kho kỳ:
  registry.json            bảng phân công
  raw/lms/<courseClassId>.json   phản hồi gốc của LMS (để truy vết)
  manifest.json (stage "fetch")
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from pmo.connectors import lms
from pmo.registry import build_registry, is_valid_course_class_id, load_seed
from pmo.warehouse import Snapshot

Fetcher = Callable[[str], dict]
Lister = Callable[[str], list]


def _default_fetcher(course_class_id: str) -> dict:
    return lms.call_tool("lms_course_class_statistics", {"courseClassId": course_class_id})


def _default_lister(class_id: str) -> list:
    res = lms.call_tool("lms_list_course_classes", {"classId": class_id})
    return res.get("items", []) if isinstance(res, dict) else res


def sync_registry(snapshot: Snapshot, seed: dict, lister: Lister, refresh: bool,
                  offline: bool = False) -> tuple[dict, list, list]:
    """Lấy danh sách môn hiện hành của từng lớp từ LMS. Trả về (seed_live, changes, errors).

    Bài học #3: mã courseClassId trong file cấu hình bị cũ → luôn lấy mã hiện hành từ LMS.
    Offline: dùng bản đã cache trong kho; nếu chưa có thì dùng seed.
    """
    live = {"classes": []}
    changes, errors = [], []
    for cls in seed.get("classes", []):
        name = f"raw/lms/registry_{cls['classId']}.json"
        items = None if (refresh and not offline) else snapshot.read_json(name)
        if items is None and offline:
            items = cls.get("assignedCourses", [])
        elif items is None:
            try:
                items = lister(cls["classId"])
                snapshot.write_json(name, items)
            except Exception as e:
                errors.append({"courseClassId": f"registry:{cls.get('className')}", "error": str(e)})
                items = cls.get("assignedCourses", [])
        old = {c.get("courseCode"): c.get("courseClassId") for c in cls.get("assignedCourses", [])}
        for c in items:
            prev = old.get(c.get("courseCode"))
            if prev and prev != c.get("courseClassId"):
                changes.append(f"{cls.get('className')}/{c.get('courseCode')}: {prev} → {c.get('courseClassId')}")
        live["classes"].append({**cls, "assignedCourses": items})
    return live, changes, errors


def raw_name(course_class_id: str) -> str:
    return f"raw/lms/{course_class_id}.json"


def fetch(snapshot: Snapshot, refresh: bool = False, offline: bool = False,
          fetcher: Fetcher | None = None, seed: dict | None = None, workers: int = 5,
          lister: Lister | None = None) -> dict:
    fetcher = fetcher or _default_fetcher
    seed = seed if seed is not None else load_seed()
    changes: list = []
    reg_errors: list = []
    if lister is None and fetcher is _default_fetcher:
        lister = _default_lister
    if lister is not None:
        seed, changes, reg_errors = sync_registry(snapshot, seed, lister, refresh, offline)
    registry = build_registry(seed)
    snapshot.write_json("registry.json", registry)

    targets = sorted({r["courseClassId"] for r in registry
                      if r["tracked"] and is_valid_course_class_id(r["courseClassId"])})
    todo = [cid for cid in targets if refresh or not snapshot.exists(raw_name(cid))]
    errors: list[dict] = []

    if offline:
        todo = []
    else:
        def work(cid: str):
            try:
                snapshot.write_json(raw_name(cid), fetcher(cid))
                return None
            except Exception as e:
                return {"courseClassId": cid, "error": str(e)}

        with ThreadPoolExecutor(max_workers=workers) as pool:
            errors = [e for e in pool.map(work, todo) if e]
    errors = reg_errors + errors

    info = {
        "source": "LMS MCP lms_course_class_statistics",
        "registryRows": len(registry),
        "targets": len(targets),
        "fetched": len(todo) - len(errors),
        "cached": len(targets) - len(todo),
        "offline": offline,
        "errors": errors,
        "registryChanges": changes,
    }
    # Chỉ đánh dấu thời điểm lấy dữ liệu khi thực sự có gọi nguồn
    prev = snapshot.manifest().get("stages", {}).get("fetch", {})
    if not todo and prev.get("dataAt"):
        info["dataAt"] = prev["dataAt"]
    elif todo:
        from pmo.warehouse import utcnow_iso
        info["dataAt"] = utcnow_iso()
    snapshot.update_manifest("fetch", info)
    return info

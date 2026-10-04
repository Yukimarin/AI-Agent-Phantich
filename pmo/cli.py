"""ORCHESTRATOR — một lệnh duy nhất.

  uv run python -m pmo run              kỳ hiện tại, dùng cache nếu đã lấy
  uv run python -m pmo run --refresh    lấy lại dữ liệu từ nguồn
  uv run python -m pmo run --offline    không gọi nguồn, chỉ dùng kho
  uv run python -m pmo verify           chỉ chạy gates trên kho kỳ hiện tại

Gate nào FAIL ⇒ dừng, không xuất kết quả module, ghi run_report.md nêu rõ lỗi. Exit code 1.
"""
from __future__ import annotations

import argparse
import json
import sys
import time

from pmo import data_agent
from pmo.config import OUTPUT_DIR
from pmo.gates import g1_data, g2_metrics
from pmo.gates.base import Check, passed, render_markdown
from pmo.metrics.build import build_student_metrics
from pmo.modules import REGISTRY
from pmo.warehouse import Snapshot, current_period, utcnow_iso


def _write_report(period: str, checks: list[Check], status: str, notes: list[str], outputs: list[str],
                  elapsed: float) -> str:
    out_dir = OUTPUT_DIR / period
    out_dir.mkdir(parents=True, exist_ok=True)
    md = [
        f"# Run report — kỳ {period}",
        "",
        f"- Thời điểm: {utcnow_iso()}",
        f"- Trạng thái: **{status}**",
        f"- Thời gian chạy: {elapsed:.1f}s",
        "",
        "## Cổng kiểm định",
        "",
        render_markdown(checks),
        "",
    ]
    if notes:
        md += ["## Ghi chú", ""] + [f"- {n}" for n in notes] + [""]
    if outputs:
        md += ["## Đầu ra", ""] + [f"- `{o}`" for o in outputs] + [""]
    path = out_dir / "run_report.md"
    path.write_text("\n".join(md), encoding="utf-8")
    (out_dir / "gates.json").write_text(
        json.dumps([c.to_dict() for c in checks], ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def _stop(period: str, checks: list[Check], notes: list[str], t0: float) -> int:
    path = _write_report(period, checks, "❌ DỪNG — có gate thất bại, KHÔNG xuất báo cáo", notes, [], time.time() - t0)
    print(f"\n❌ Gate thất bại. Xem {path}")
    return 1


def cmd_run(args: argparse.Namespace) -> int:
    t0 = time.time()
    period = args.period or current_period()
    snap = Snapshot(period)
    notes: list[str] = []
    print(f"▶ Kỳ {period} · kho {snap.dir}")

    info = data_agent.fetch(snap, refresh=args.refresh, offline=args.offline)
    print(f"  Data Agent: {info['fetched']} lấy mới, {info['cached']} dùng cache, {len(info['errors'])} lỗi")
    checks = g1_data.run(snap)
    if not passed(checks):
        return _stop(period, checks, notes, t0)

    rows = build_student_metrics(snap)
    print(f"  Metric Engine: {len(rows)} lớp-môn")
    checks += g2_metrics.run(snap, run_tests=not args.skip_tests)
    if not passed(checks):
        return _stop(period, checks, notes, t0)

    outputs = []
    selected = args.only.split(",") if args.only else list(REGISTRY)
    for key in selected:
        mod = REGISTRY[key]
        res = mod.run(snap)
        mdir = OUTPUT_DIR / period / mod.NAME
        mdir.mkdir(parents=True, exist_ok=True)
        for fname, obj in (("result.json", res["result"]), ("summary.json", res["summary"])):
            (mdir / fname).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
            outputs.append(str((mdir / fname).relative_to(OUTPUT_DIR.parent)))
        print(f"  Module {key}: OK")

    status = "✅ ĐẠT — mọi gate bắt buộc đã qua"
    if any(c.status == "warn" for c in checks):
        status += " (có cảnh báo, xem bảng)"
    path = _write_report(period, checks, status, notes, outputs, time.time() - t0)
    print(f"\n✅ Hoàn thành. Xem {path}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    t0 = time.time()
    period = args.period or current_period()
    snap = Snapshot(period)
    checks = g1_data.run(snap)
    if snap.exists("student_metrics.json"):
        checks += g2_metrics.run(snap, run_tests=not args.skip_tests)
    ok = passed(checks)
    path = _write_report(period, checks, "✅ ĐẠT" if ok else "❌ KHÔNG ĐẠT", [], [], time.time() - t0)
    print(("✅" if ok else "❌") + f" Xem {path}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="pmo", description="PMO Data Hub")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="Lấy dữ liệu → tính → kiểm định → xuất")
    r.add_argument("--period", help="Kỳ dạng YYYY-Www (mặc định: tuần hiện tại)")
    r.add_argument("--refresh", action="store_true", help="Lấy lại dữ liệu từ nguồn dù đã có cache")
    r.add_argument("--offline", action="store_true", help="Không gọi nguồn")
    r.add_argument("--only", help="Chỉ chạy các module, ví dụ: m1")
    r.add_argument("--skip-tests", action="store_true", help="Bỏ qua bộ test trong G2 (không khuyến nghị)")
    r.set_defaults(func=cmd_run)
    v = sub.add_parser("verify", help="Chỉ chạy các cổng kiểm định")
    v.add_argument("--period")
    v.add_argument("--skip-tests", action="store_true")
    v.set_defaults(func=cmd_verify)
    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

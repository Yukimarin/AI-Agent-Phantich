"""Modules phân tích: mỗi mục tiêu một module, chỉ đọc kho.

Giao diện chung: run(snapshot) -> {"result": dict, "summary": dict}
Thêm báo cáo mới = thêm module vào REGISTRY.
"""
from pmo.modules import m1_class_health, m4_class_diagnosis

REGISTRY = {
    "m1": m1_class_health,
    # "m2": m2_pass_forecast,   # đợt sau
    # "m3": m3_staff_performance,  # đợt sau (cần Worklane connector)
    "m4": m4_class_diagnosis,
}

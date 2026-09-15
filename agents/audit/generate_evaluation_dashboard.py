import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(root_dir, "agents/audit"))

print("=== NÂNG CẤP DASHBOARD ĐÁNH GIÁ NHÂN SỰ: SỬA UI/UX & ÁP DỤNG QUY TẮC MỚI ===")

# 1. Load the comprehensive master data
master_data_path = os.path.join(root_dir, 'data/processed/staff_evaluation_master.json')
with open(master_data_path, 'r', encoding='utf-8') as f:
    master_data = json.load(f)

# 2. Update 4 TAs data strictly according to user rules:
# Rule 1: Task quá hạn CHỈ tính nếu nhân sự trễ hạn (Cần làm / Đang làm). Nếu "Chờ duyệt" (PIC chưa duyệt) thì KHÔNG ghi nhận trễ hạn!
# Rule 2: Bổ sung 2 vi phạm cho Mai Xuân Chinh (22/08 tự ý đổi lịch coi thi, 09/09 vi phạm quy định ra BTVN 2 môn AI KS24).
tas_analysis = {
    "lại trung lâm": {
        "key": "lại trung lâm",
        "name": "Lại Trung Lâm",
        "role": "Trợ giảng",
        "rank": 2,
        "campus": "Cơ sở Hà Nội - Ngọc Trục",
        "group": "Khối CNTT Hà Nội",
        "leader": "Hồ Xuân Hùng",
        "rank_order": 1,
        "rank_title": "Hạng 1 - Xuất Sắc (Gương mẫu)",
        "badge_color": "emerald",
        "grade": "A+",
        "total_score": 99.6,
        "scores": {
            "log_score": 35.0,
            "task_score": 24.6,
            "issue_score": 25.0,
            "ops_score": 15.0
        },
        "overview": "Nhân sự có tính kỷ luật và tuân thủ cao nhất trong 4 trợ giảng. Đạt tỷ lệ nộp báo cáo ngày 100%, không để xảy ra bất kỳ ticket quá hạn nào trên Worklane (0%) và 0 lỗi tác nghiệp lên lớp. Tác phong mẫu mực, gương mẫu cho toàn khối.",
        "log_stats": {
            "reported": 18,
            "expected": 18,
            "rate": 100.0,
            "missing_days": [],
            "weekend": ["2026-08-22"],
            "total_hours": 158.2,
            "avg_hours": 8.79,
            "tasks_total": 59,
            "tasks_done": 58,
            "tasks_uncompleted": 1,
            "task_rate": 98.3,
            "uncompleted_desc": "2026-08-18: Chấm bài lớp CNTT1 2 5 (1.5h - 0%)"
        },
        "time_breakdown": [
            {"cat": "Hỗ trợ sinh viên & công việc chung", "hours": 80.8, "pct": 51.0, "color": "#64748b"},
            {"cat": "Kiểm tra / Chấm bài tập về nhà (BTVN)", "hours": 22.8, "pct": 14.4, "color": "#10b981"},
            {"cat": "Phát triển Tool / Dự án nội bộ", "hours": 13.5, "pct": 8.5, "color": "#6366f1"},
            {"cat": "Chăm sóc & Quản lý Học viên", "hours": 13.0, "pct": 8.2, "color": "#06b6d4"},
            {"cat": "Nghiên cứu môn / Chuẩn bị học liệu", "hours": 12.5, "pct": 7.9, "color": "#f59e0b"},
            {"cat": "Họp chuyên môn & Giao ban", "hours": 9.5, "pct": 6.0, "color": "#8b5cf6"},
            {"cat": "Trợ giảng lên lớp trực tiếp", "hours": 6.2, "pct": 3.9, "color": "#3b82f6"}
        ],
        "worklane_issues": {
            "total": 132,
            "done": 127,
            "done_rate": 96.2,
            "open": 2,
            "overdue": 0,
            "overdue_rate": 0.0,
            "projects": ["KS25GIAN", "KS26MON", "SANXUAT"],
            "overdue_list": [],
            "pending_approval_list": []
        },
        "violations": {
            "total_count": 0,
            "items": []
        },
        "recommendation": "Tiếp tục phát huy vai trò nòng cốt về nề nếp kỷ luật. Cần rà soát chuẩn hóa các đầu việc 'Hỗ trợ chung' (đang chiếm 51% quỹ thời gian) sang các mã định mức cụ thể theo barem KPI Master Khối CNTT."
    },
    "phạm ngọc kiên": {
        "key": "phạm ngọc kiên",
        "name": "Phạm Ngọc Kiên",
        "role": "Trợ giảng",
        "rank": 2,
        "campus": "Cơ sở Hà Nội - Ngọc Trục",
        "group": "Khối CNTT Hà Nội",
        "leader": "Hồ Xuân Hùng",
        "rank_order": 3,
        "rank_title": "Hạng 3 - Khá (Cần cải thiện nề nếp)",
        "badge_color": "blue",
        "grade": "B",
        "total_score": 82.6,
        "scores": {
            "log_score": 31.1,
            "task_score": 23.5,
            "issue_score": 23.0,
            "ops_score": 5.0
        },
        "overview": "Đóng góp tích cực trong việc lên lớp thực hành và chấm bài cho các lớp KS25/KS26 (chiếm 42% thời gian). Về tiến độ ticket, chỉ có 01 ticket quá hạn thực sự ('giảng dạy thực hành'), còn 01 ticket đang ở trạng thái 'Chờ duyệt' (PIC chưa nghiệm thu, không tính lỗi cho nhân sự). Điểm cần khắc phục là 02 ngày liên tiếp quên nộp báo cáo ngày.",
        "log_stats": {
            "reported": 16,
            "expected": 18,
            "rate": 88.9,
            "missing_days": ["2026-08-27", "2026-08-28"],
            "weekend": ["2026-08-22"],
            "total_hours": 145.0,
            "avg_hours": 9.06,
            "tasks_total": 51,
            "tasks_done": 48,
            "tasks_uncompleted": 3,
            "task_rate": 94.1,
            "uncompleted_desc": "17/08: Dạy tiết TH CNTT3+6 (5.0h); 17/08: Chấm BTVN CNTT3+4+6 (3.0h); 22/08: Soát bài nhập môn (4.5h)"
        },
        "time_breakdown": [
            {"cat": "Hỗ trợ sinh viên & công việc chung", "hours": 72.0, "pct": 49.7, "color": "#64748b"},
            {"cat": "Kiểm tra / Chấm bài tập về nhà (BTVN)", "hours": 45.0, "pct": 31.0, "color": "#10b981"},
            {"cat": "Trợ giảng lên lớp trực tiếp", "hours": 16.0, "pct": 11.0, "color": "#3b82f6"},
            {"cat": "Chăm sóc & Quản lý Học viên", "hours": 9.0, "pct": 6.2, "color": "#06b6d4"},
            {"cat": "Họp chuyên môn & Giao ban", "hours": 3.0, "pct": 2.1, "color": "#8b5cf6"}
        ],
        "worklane_issues": {
            "total": 63,
            "done": 57,
            "done_rate": 90.5,
            "open": 3,
            "overdue": 1,
            "overdue_rate": 1.6,
            "projects": ["KS25GIAN", "KS26MON", "SANXUAT"],
            "overdue_list": [
                {"code": "KS25GIAN-23", "title": "giảng dạy thực hành", "due": "2026-07-14", "state": "Cần làm", "project": "KS25GIAN"}
            ],
            "pending_approval_list": [
                {"code": "KS26MON-287", "title": "S23: Đề thi cuối môn", "due": "2026-08-07", "state": "Chờ duyệt (PIC chưa duyệt - Không tính lỗi nhân sự)", "project": "KS26MON"}
            ]
        },
        "violations": {
            "total_count": 3,
            "items": [
                {"type": "Quên Nộp Báo Cáo Ngày", "date": "2026-08-27", "desc": "Mã lỗi WL-DAILY-LOG-MISSING — Không nộp báo cáo ngày 27/08/2026 trên Worklane PM"},
                {"type": "Quên Nộp Báo Cáo Ngày", "date": "2026-08-28", "desc": "Mã lỗi WL-DAILY-LOG-MISSING — Không nộp báo cáo ngày 28/08/2026 trên Worklane PM"},
                {"type": "Trễ hạn Ticket Worklane", "date": "2026-07-14", "desc": "Ticket KS25GIAN-23 quá hạn (Cần làm) — giảng dạy thực hành"}
            ]
        },
        "recommendation": "Cài đặt nhắc nhở tự động cuối ngày để chấm dứt tình trạng quên nộp báo cáo ngày. Khẩn trương xử lý dứt điểm ticket KS25GIAN-23 và nhắc PIC nghiệm thu ticket KS26MON-287."
    },
    "đinh thành nam": {
        "key": "đinh thành nam",
        "name": "Đinh Thành Nam",
        "role": "Trợ giảng",
        "rank": 2,
        "campus": "Cơ sở Hà Nội - HPC",
        "group": "Khối CNTT Hà Nội",
        "leader": "Hồ Xuân Hùng",
        "rank_order": 4,
        "rank_title": "Hạng 4 - Cần Lưu Ý (Kỷ luật log yếu nhất & Lệch JD)",
        "badge_color": "amber",
        "grade": "B",
        "total_score": 78.2,
        "scores": {
            "log_score": 27.2,
            "task_score": 25.0,
            "issue_score": 23.0,
            "ops_score": 3.0
        },
        "overview": "Kỷ luật nộp báo cáo ngày thấp nhất trong nhóm (77.8%), liên tục tái diễn tình trạng quên nộp báo cáo (4 ngày: 18/08, 20/08, 10/09, 14/09). Về ticket, chỉ có 01 ticket quá hạn thực sự (PTITSAN2-19), còn 01 ticket (PTITSAN-22) đang ở trạng thái 'Chờ duyệt' (PIC chưa nghiệm thu, không tính lỗi cho nhân sự). Cơ cấu công việc đang bị lệch lớn sang làm Dev Tool (chiếm 41.5%) thay vì tập trung vào các nghiệp vụ trợ giảng lớp học.",
        "log_stats": {
            "reported": 14,
            "expected": 18,
            "rate": 77.8,
            "missing_days": ["2026-08-18", "2026-08-20", "2026-09-10", "2026-09-14"],
            "weekend": ["2026-08-22"],
            "total_hours": 114.5,
            "avg_hours": 8.18,
            "tasks_total": 43,
            "tasks_done": 43,
            "tasks_uncompleted": 0,
            "task_rate": 100.0,
            "uncompleted_desc": "Không có task dở dang."
        },
        "time_breakdown": [
            {"cat": "Phát triển Tool / Dự án nội bộ (App PH, web)", "hours": 47.5, "pct": 41.5, "color": "#6366f1"},
            {"cat": "Hỗ trợ sinh viên & công việc chung", "hours": 28.0, "pct": 24.5, "color": "#64748b"},
            {"cat": "Nghiên cứu môn / Chuẩn bị học liệu", "hours": 17.0, "pct": 14.8, "color": "#f59e0b"},
            {"cat": "Chăm sóc & Quản lý Học viên", "hours": 11.0, "pct": 9.6, "color": "#06b6d4"},
            {"cat": "Kiểm tra / Chấm bài tập về nhà (BTVN)", "hours": 8.5, "pct": 7.4, "color": "#10b981"},
            {"cat": "Họp chuyên môn & Giao ban", "hours": 2.5, "pct": 2.2, "color": "#8b5cf6"}
        ],
        "worklane_issues": {
            "total": 97,
            "done": 95,
            "done_rate": 97.9,
            "open": 2,
            "overdue": 1,
            "overdue_rate": 1.0,
            "projects": ["PTITSAN", "PTITSAN2", "PTITTRIE", "K24CSAN2", "KS24", "KS24INTE"],
            "overdue_list": [
                {"code": "PTITSAN2-19", "title": "[S09] Đề thi thực hành 2-10 — Session 09", "due": "2026-09-12", "state": "Cần làm", "project": "PTITSAN2"}
            ],
            "pending_approval_list": [
                {"code": "PTITSAN-22", "title": "[S09] Đề thi thực hành 3-6 — Session 09", "due": "2026-09-05", "state": "Chờ duyệt (PIC chưa duyệt - Không tính lỗi nhân sự)", "project": "PTITSAN"}
            ]
        },
        "violations": {
            "total_count": 5,
            "items": [
                {"type": "Quên Nộp Báo Cáo Ngày", "date": "2026-08-18", "desc": "Mã lỗi WL-DAILY-LOG-MISSING — Không nộp báo cáo ngày 18/08/2026 trên Worklane PM"},
                {"type": "Quên Nộp Báo Cáo Ngày", "date": "2026-08-20", "desc": "Mã lỗi WL-DAILY-LOG-MISSING — Không nộp báo cáo ngày 20/08/2026 trên Worklane PM"},
                {"type": "Quên Nộp Báo Cáo Ngày", "date": "2026-09-10", "desc": "Không nộp báo cáo ngày làm việc 10/09/2026"},
                {"type": "Quên Nộp Báo Cáo Ngày", "date": "2026-09-14", "desc": "Không nộp báo cáo ngày làm việc 14/09/2026 (tiếp tục tái phạm)"},
                {"type": "Trễ hạn Ticket Worklane", "date": "2026-09-12", "desc": "Ticket PTITSAN2-19 quá hạn (Cần làm) — [S09] Đề thi thực hành 2-10"}
            ]
        },
        "recommendation": "Đề nghị Leader Hồ Xuân Hùng lập biên bản nhắc nhở về tính gương mẫu và kỷ luật nộp log ngày đối với Thầy Đinh Thành Nam. Cần cân đối lại JD: Hiện Thầy Nam đang dành hơn 41% thời lượng để viết code App/Tool, trong khi thời lượng chấm bài và hỗ trợ học viên chỉ chiếm 17%, chưa đúng trọng tâm Trợ giảng Rank 2."
    },
    "mai xuân chinh": {
        "key": "mai xuân chinh",
        "name": "Mai Xuân Chinh",
        "role": "Trợ giảng",
        "rank": 2,
        "campus": "Cơ sở Hà Nội - HPC",
        "group": "Khối CNTT Hà Nội",
        "leader": "Hồ Xuân Hùng",
        "rank_order": 2,
        "rank_title": "Hạng 2 - Khá (Nề nếp log tốt, cần chấn chỉnh vi phạm quy chế)",
        "badge_color": "blue",
        "grade": "B",
        "total_score": 85.0,
        "scores": {
            "log_score": 35.0,
            "task_score": 25.0,
            "issue_score": 25.0,
            "ops_score": 0.0
        },
        "overview": "Đạt tỷ lệ nộp báo cáo ngày 100% (18/18 ngày) và 100% task tự khai báo hoàn thành. Trong kỳ đánh giá (16/08 - 15/09), Thầy Chinh không phát sinh ticket quá hạn (10 ticket học liệu cũ có hạn 12/08 trước kỳ đánh giá đã được bóc tách loại bỏ, 6 ticket dự án TRIEKHAI đang Chờ duyệt được miễn trừ theo quy chế). Tuy nhiên, nhân sự mắc 4 vi phạm quy chế đào tạo & khảo thí rất nghiêm trọng (2 lần chậm chấm BTVN, 1 vi phạm tự ý đổi lịch coi thi 22/08, 1 vi phạm quy định ra BTVN 2 môn AI ngày 09/09), bị trừ toàn bộ 15 điểm kỷ luật tác nghiệp.",
        "log_stats": {
            "reported": 18,
            "expected": 18,
            "rate": 100.0,
            "missing_days": [],
            "weekend": ["2026-08-22"],
            "total_hours": 146.5,
            "avg_hours": 8.14,
            "tasks_total": 53,
            "tasks_done": 53,
            "tasks_uncompleted": 0,
            "task_rate": 100.0,
            "uncompleted_desc": "Không có task dở dang."
        },
        "time_breakdown": [
            {"cat": "Nghiên cứu môn / Chuẩn bị học liệu", "hours": 44.0, "pct": 30.0, "color": "#f59e0b"},
            {"cat": "Kiểm tra / Chấm bài tập về nhà (BTVN)", "hours": 35.0, "pct": 23.9, "color": "#10b981"},
            {"cat": "Phát triển Tool / Dự án nội bộ (App PH)", "hours": 28.0, "pct": 19.1, "color": "#6366f1"},
            {"cat": "Hỗ trợ sinh viên & công việc chung", "hours": 23.0, "pct": 15.7, "color": "#64748b"},
            {"cat": "Chăm sóc & Quản lý Học viên", "hours": 12.5, "pct": 8.5, "color": "#06b6d4"},
            {"cat": "Họp chuyên môn & Giao ban", "hours": 4.0, "pct": 2.7, "color": "#8b5cf6"}
        ],
        "worklane_issues": {
            "total": 159,
            "done": 138,
            "done_rate": 86.8,
            "open": 21,
            "overdue": 0,
            "overdue_rate": 0.0,
            "projects": ["PTITSAN", "TRIEKHAI", "KS24INTE", "PTITTRIE"],
            "overdue_list": [],
            "pending_approval_list": [
                {"code": "TRIEKHAI-2", "title": "[Buổi 1] Hỗ trợ triển khai DA K24 — CNTT4", "due": "2026-07-06", "state": "Chờ duyệt (PIC chưa duyệt - Không tính lỗi nhân sự)", "project": "TRIEKHAI"},
                {"code": "TRIEKHAI-5", "title": "[Buổi 1] Hỗ trợ triển khai DA K24 — CNTT2", "due": "2026-07-08", "state": "Chờ duyệt (PIC chưa duyệt - Không tính lỗi nhân sự)", "project": "TRIEKHAI"},
                {"code": "TRIEKHAI-7", "title": "[Buổi 1] Hỗ trợ triển khai DA K24 — CNTT3", "due": "2026-07-09", "state": "Chờ duyệt (PIC chưa duyệt - Không tính lỗi nhân sự)", "project": "TRIEKHAI"},
                {"code": "TRIEKHAI-18", "title": "Hỗ trợ SV làm dự án — CNTT4", "due": "2026-07-10", "state": "Chờ duyệt (PIC chưa duyệt - Không tính lỗi nhân sự)", "project": "TRIEKHAI"},
                {"code": "TRIEKHAI-22", "title": "Hỗ trợ SV làm dự án — CNTT2", "due": "2026-07-10", "state": "Chờ duyệt (PIC chưa duyệt - Không tính lỗi nhân sự)", "project": "TRIEKHAI"},
                {"code": "TRIEKHAI-24", "title": "Hỗ trợ SV làm dự án — CNTT3", "due": "2026-07-10", "state": "Chờ duyệt (PIC chưa duyệt - Không tính lỗi nhân sự)", "project": "TRIEKHAI"}
            ]
        },
        "violations": {
            "total_count": 4,
            "items": [
                {"type": "Vi Phạm Khảo Thí", "date": "2026-08-22", "desc": "Cán bộ coi thi (CBCT) tự ý đổi lịch coi thi, vi phạm nghiêm trọng quy chế khảo thí của Trung tâm"},
                {"type": "Vi Phạm Quy Định Đào Tạo", "date": "2026-09-09", "desc": "Vi phạm quy định ra BTVN trong 2 môn AI với các lớp KS24 (giao bài sai quy chuẩn đào tạo)"},
                {"type": "Lỗi Tác Nghiệp Đào Tạo", "date": "2026-08-20", "desc": "Lớp HN-K24-CNTT3: Lỗi QLDT-EX-LATE — Chậm trễ chấm BTVN cho sinh viên (Lần 1)"},
                {"type": "Lỗi Tác Nghiệp Đào Tạo", "date": "2026-08-21", "desc": "Lớp HN-K24-CNTT3: Lỗi QLDT-EX-LATE — Chậm trễ chấm BTVN cho sinh viên (Lần 2 liên tiếp)"}
            ]
        },
        "recommendation": "Yêu cầu Giám đốc Đào tạo và Leader Hồ Xuân Hùng lập biên bản nhắc nhở đối với 4 vi phạm quy chế đào tạo & khảo thí của Thầy Chinh. Về tiến độ ticket, nhân sự không có ticket quá hạn trong kỳ đánh giá 16/08 - 15/09 (10 ticket học liệu cũ có hạn 12/08 đã được loại bỏ; 6 ticket TRIEKHAI đang chờ duyệt)."
    }
}

master_data['tas_analysis'] = tas_analysis

# Update 30days period in master data
for k, ta in tas_analysis.items():
    if k in master_data['meta']['periods']['period_30days']['staff_data']:
        s = master_data['meta']['periods']['period_30days']['staff_data'][k]
        s['reported_days'] = ta['log_stats']['reported']
        s['expected_days'] = ta['log_stats']['expected']
        s['missing_days'] = ta['log_stats']['missing_days']
        s['log_rate'] = ta['log_stats']['rate']
        s['total_declared_hours'] = ta['log_stats']['total_hours']
        s['avg_hours_per_day'] = ta['log_stats']['avg_hours']
        s['total_tasks'] = ta['log_stats']['tasks_total']
        s['completed_tasks'] = ta['log_stats']['tasks_done']
        s['task_completion_rate'] = ta['log_stats']['task_rate']
        s['total_issues'] = ta['worklane_issues']['total']
        s['done_issues'] = ta['worklane_issues']['done']
        s['open_issues'] = ta['worklane_issues']['open']
        s['overdue_issues_count'] = ta['worklane_issues']['overdue']
        s['overdue_issues'] = ta['worklane_issues']['overdue_list']
        s['ops_violations_count'] = ta['violations']['total_count']
        s['scores'] = ta['scores']
        s['total_score'] = ta['total_score']
        s['grade'] = ta['grade']
        s['grade_label'] = ta['rank_title']
        s['badge_color'] = ta['badge_color']

# Re-save master JSON
with open(master_data_path, 'w', encoding='utf-8') as f:
    json.dump(master_data, f, ensure_ascii=False, indent=2)

# Generate HTML file
dest_1 = os.path.join(root_dir, 'output/dashboards/audit/danh_gia_nhan_su_truc_quan.html')
dest_2 = os.path.join(root_dir, 'danh_gia_nhan_su.html')
os.makedirs(os.path.dirname(dest_1), exist_ok=True)

json_str = json.dumps(master_data, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Đánh Giá Hiệu Suất & Vi Phạm Nhân Sự Đào Tạo - Worklane PMO</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        slate: {
                            850: '#151e2e',
                            900: '#0f172a',
                            950: '#080c14'
                        },
                        indigo: {
                            600: '#4f46e5',
                            700: '#4338ca'
                        }
                    }
                }
            }
        }
    </script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #080c14;
            color: #e2e8f0;
        }
        .font-mono {
            font-family: 'JetBrains Mono', monospace;
        }
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #0f172a;
        }
        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #475569;
        }
        .drawer-slide {
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .card-glow:hover {
            border-color: #6366f1;
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.2);
            transform: translateY(-2px);
        }
        @media print {
            .no-print {
                display: none !important;
            }
            body {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            .print-clean {
                border: 1px solid #ccc !important;
                color: #000 !important;
                background: #fff !important;
            }
        }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen antialiased flex flex-col">

    <!-- TOP NAVIGATION -->
    <header class="bg-slate-900/95 backdrop-blur border-b border-slate-800 sticky top-0 z-30 px-6 py-3.5 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center space-x-3.5">
            <div class="w-11 h-11 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-rose-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25">
                <i class="fa-solid fa-shield-halved text-xl"></i>
            </div>
            <div>
                <div class="flex items-center space-x-2.5">
                    <h1 class="text-base font-bold text-white tracking-tight uppercase">Báo Cáo Đánh Giá Hiệu Suất & Vi Phạm Nhân Sự</h1>
                    <span class="px-2 py-0.5 text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full flex items-center gap-1">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Kiểm Toán Worklane PMO
                    </span>
                </div>
                <p class="text-xs text-slate-400">Kính gửi: <span class="text-indigo-300 font-semibold">Thầy Nguyễn Duy Quang</span> (GĐ Đào tạo) & <span class="text-indigo-300 font-semibold">Thầy Hồ Xuân Hùng</span> (Leader CNTT Hà Nội)</p>
            </div>
        </div>

        <div class="flex items-center space-x-3 text-xs">
            <!-- PERIOD SELECTOR -->
            <div class="flex items-center space-x-1.5 bg-slate-950 p-1 rounded-xl border border-indigo-500/40 shadow-inner">
                <span class="text-slate-400 pl-2 pr-1 font-semibold flex items-center gap-1">
                    <i class="fa-regular fa-calendar-check text-indigo-400"></i> Đợt Đánh Giá:
                </span>
                <select id="periodSelect" onchange="switchPeriod(this.value)" class="bg-slate-900 text-indigo-200 font-bold px-3 py-1.5 rounded-lg border border-indigo-500/40 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer">
                    <option value="period_30days">⚡ 30 Ngày Gần Nhất (16/08 - 15/09/2026)</option>
                    <option value="period_sept">📅 Kỳ 01/09 - 11/09/2026 (7 Ngày Công)</option>
                    <option value="period_aug">🏛️ Tháng 08/2026 (20 Ngày Công)</option>
                </select>
            </div>

            <!-- PRINT ACTION -->
            <button onclick="window.print()" class="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-medium transition flex items-center gap-1.5 shadow-sm">
                <i class="fa-solid fa-print text-slate-400"></i> In Báo Cáo
            </button>
        </div>
    </header>

    <!-- MAIN BODY -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">

        <!-- PERIOD CONTEXT BANNER -->
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-900/40 rounded-2xl p-5 flex flex-wrap items-center justify-between gap-4 shadow-xl">
            <div class="space-y-1.5">
                <div class="flex items-center gap-2">
                    <span id="periodBadge" class="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                        ĐANG XEM: 30 NGÀY GẦN NHẤT (16/08 - 15/09/2026)
                    </span>
                    <span id="periodWorkdaysBadge" class="text-xs text-slate-400 font-medium">18 ngày làm việc tiêu chuẩn (Trừ T7/CN và nghỉ lễ 31/08 - 02/09)</span>
                </div>
                <h2 id="periodTitle" class="text-lg font-bold text-white tracking-tight">Kiểm Toán Chuyên Sâu: 4 Thầy Trợ Giảng Khối CNTT Hà Nội & Toàn Viện</h2>
                <p id="periodDesc" class="text-xs text-slate-400 max-w-3xl leading-relaxed">
                    Báo cáo phân tích dữ liệu nhật ký công việc (Daily Reports), khối lượng và tiến độ ticket dự án (Worklane Issues), cùng dữ liệu vi phạm tác nghiệp đào tạo thực tế để cung cấp bức tranh minh bạch, công bằng cho Lãnh đạo Đào tạo.
                </p>
            </div>
            
            <div class="flex items-center gap-4 bg-slate-950/70 p-3 rounded-xl border border-slate-800">
                <div class="text-right">
                    <div class="text-2xl font-black text-indigo-400">4 <span class="text-xs text-slate-400 font-normal">/ 41 NS</span></div>
                    <div class="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Trợ Giảng Tiêu Điểm</div>
                </div>
                <div class="h-8 w-px bg-slate-800"></div>
                <div class="text-right">
                    <div class="text-2xl font-black text-emerald-400">91.7%</div>
                    <div class="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Tuân Thủ Nộp Log</div>
                </div>
                <div class="h-8 w-px bg-slate-800"></div>
                <div class="text-right">
                    <div class="text-2xl font-black text-rose-400">2</div>
                    <div class="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Ticket Quá Hạn (Cần làm)</div>
                </div>
            </div>
        </div>

        <!-- SECTION 1: BẢNG SO SÁNH TỔNG HỢP 4 THẦY TRỢ GIẢNG (THE CORE MATRIX) -->
        <div class="bg-slate-900/95 border border-indigo-500/30 rounded-2xl overflow-hidden shadow-xl space-y-4 p-5">
            <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-3">
                <div class="flex items-center space-x-2.5">
                    <div class="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold">
                        <i class="fa-solid fa-table-list text-sm"></i>
                    </div>
                    <div>
                        <h3 class="text-sm font-bold text-white uppercase tracking-wide">I. Bảng So Sánh Tổng Hợp Hiệu Suất & Vi Phạm (16/08 - 15/09/2026)</h3>
                        <p class="text-xs text-slate-400">Quy tắc chuẩn: Ticket chỉ tính quá hạn nếu nhân sự trễ hạn (Cần làm/Đang làm). Trạng thái 'Chờ duyệt' (PIC chưa duyệt) KHÔNG tính lỗi nhân sự.</p>
                    </div>
                </div>
                <span class="text-xs font-semibold px-2.5 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700">
                    Leader Phụ trách: Hồ Xuân Hùng
                </span>
            </div>

            <div class="overflow-x-auto w-full">
                <table class="w-full text-left text-xs text-slate-300 border-collapse">
                    <thead class="bg-slate-950/80 text-slate-400 uppercase font-bold text-[11px] tracking-wider border-b border-slate-800">
                        <tr>
                            <th class="py-3 px-2 text-center w-10">Hạng</th>
                            <th class="py-3 px-3">Họ và Tên</th>
                            <th class="py-3 px-2">Cơ sở & Rank</th>
                            <th class="py-3 px-2 text-center">Nộp Log Ngày</th>
                            <th class="py-3 px-2 text-center">Tổng giờ</th>
                            <th class="py-3 px-2 text-center">% Task Xong</th>
                            <th class="py-3 px-2 text-center">Issues</th>
                            <th class="py-3 px-2 text-center">Quá hạn</th>
                            <th class="py-3 px-2 text-center">Vi phạm</th>
                            <th class="py-3 px-2 text-center">Điểm KPI</th>
                            <th class="py-3 px-3 min-w-[260px]">Đánh giá Nề nếp & Hiệu suất</th>
                            <th class="py-3 px-2 text-center">Thao tác</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800/60" id="matrixTableBody">
                        <!-- Rendered by Javascript -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- SECTION 2: CHARTS ANALYTICS (FIXED UI/UX - PADDING & NO OVERFLOW) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- CHART 1: TIME BREAKDOWN -->
            <div class="lg:col-span-2 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-chart-column text-indigo-400"></i> Cơ Cấu Phân Bổ Thời Gian Thực Tế 4 Thầy TrỢ Giảng (Giờ)
                    </h3>
                    <span class="text-xs text-slate-400">30 ngày gần nhất (16/08 - 15/09/2026)</span>
                </div>
                <div class="h-80 w-full pb-2">
                    <canvas id="timeBreakdownChart"></canvas>
                </div>
            </div>

            <!-- CHART 2: OVERDUE ISSUES & VIOLATIONS -->
            <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-3 flex flex-col justify-between">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-triangle-exclamation text-rose-400"></i> Cảnh Báo Quá Hạn & Vi Phạm
                    </h3>
                    <span class="text-xs text-slate-400">Chỉ tính lỗi nhân sự</span>
                </div>
                <div class="h-72 relative flex items-center justify-center pb-2">
                    <canvas id="violationsBarChart"></canvas>
                </div>
                <div class="text-[11px] text-slate-400 border-t border-slate-800 pt-2 flex flex-col gap-0.5">
                    <span>* <strong>Ticket quá hạn:</strong> Chỉ đếm task 'Cần làm' / 'Đang làm' trễ deadline.</span>
                    <span>* <strong>Vi phạm quy chế:</strong> Gồm vi phạm khảo thí, quy chế BTVN & chậm chấm.</span>
                </div>
            </div>
        </div>

        <!-- SECTION 3: DEEP-DIVE PROFILES 4 TEACHING ASSISTANTS -->
        <div class="space-y-4">
            <div class="flex items-center justify-between">
                <h3 class="text-sm font-bold text-white uppercase tracking-wide flex items-center gap-2">
                    <i class="fa-solid fa-id-card-clip text-indigo-400"></i> II. Hồ Sơ Đánh Giá Chi Tiết Từng Thầy Trợ Giảng (Deep-Dive)
                </h3>
                <span class="text-xs text-slate-400">Chọn thầy để xem chi tiết đầy đủ 4 mặt công tác</span>
            </div>

            <!-- TABS FOR 4 TAs -->
            <div class="flex flex-wrap gap-2 border-b border-slate-800 pb-2" id="taTabsHeader">
                <button onclick="selectTATab('lại trung lâm')" id="tab-btn-lam" class="px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-indigo-600 text-white shadow-md">
                    <i class="fa-solid fa-award text-emerald-300"></i> 1. Lại Trung Lâm (A+ • 99.6đ)
                </button>
                <button onclick="selectTATab('mai xuân chinh')" id="tab-btn-chinh" class="px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-slate-800 text-slate-300 hover:bg-slate-700">
                    <i class="fa-solid fa-circle-check text-blue-400"></i> 2. Mai Xuân Chinh (B • 85.0đ)
                </button>
                <button onclick="selectTATab('phạm ngọc kiên')" id="tab-btn-kien" class="px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-slate-800 text-slate-300 hover:bg-slate-700">
                    <i class="fa-solid fa-circle-check text-blue-400"></i> 3. Phạm Ngọc Kiên (B • 82.6đ)
                </button>
                <button onclick="selectTATab('đinh thành nam')" id="tab-btn-nam" class="px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-slate-800 text-slate-300 hover:bg-slate-700">
                    <i class="fa-solid fa-calendar-xmark text-amber-400"></i> 4. Đinh Thành Nam (B • 78.2đ)
                </button>
            </div>

            <!-- SELECTED TA DETAILED CONTAINER -->
            <div class="bg-slate-900/95 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6" id="taDetailCard">
                <!-- Dynamically rendered by Javascript -->
            </div>
        </div>

        <!-- SECTION 4: KẾT LUẬN & ĐỀ XUẤT CỦA HỘI ĐỒNG KIỂM TOÁN PMO -->
        <div class="bg-gradient-to-br from-slate-900 via-slate-900 to-indigo-950/30 border border-indigo-900/40 rounded-2xl p-6 shadow-xl space-y-4">
            <h3 class="text-sm font-bold text-white uppercase tracking-wide flex items-center gap-2 text-indigo-300">
                <i class="fa-solid fa-clipboard-list"></i> III. Kết Luận & Đề Xuất Từ Hội Đồng Kiểm Toán PMO
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs leading-relaxed">
                <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800 space-y-2">
                    <h4 class="font-bold text-emerald-400 flex items-center gap-1.5">
                        <i class="fa-solid fa-calendar-check"></i> 1. Về Kỷ luật Báo cáo ngày
                    </h4>
                    <p class="text-slate-300">
                        • <strong>Biểu dương:</strong> Thầy <span class="text-emerald-300 font-semibold">Lại Trung Lâm</span> và Thầy <span class="text-emerald-300 font-semibold">Mai Xuân Chinh</span> giữ vững tỷ lệ nộp báo cáo <strong>100% đầy đủ</strong>, nộp cả Thứ Bảy.<br>
                        • <strong>Cảnh báo:</strong> Thầy <span class="text-rose-400 font-semibold">Đinh Thành Nam</span> (77.8% - quên 4 ngày, vừa tiếp tục quên ngày 14/09) và Thầy <span class="text-amber-400 font-semibold">Phạm Ngọc Kiên</span> (88.9% - quên 2 ngày). Yêu cầu Leader lập biên bản chấn chỉnh nề nếp.
                    </p>
                </div>

                <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800 space-y-2">
                    <h4 class="font-bold text-rose-400 flex items-center gap-1.5">
                        <i class="fa-solid fa-list-check"></i> 2. Quản trị Tiến độ Ticket Dự án
                    </h4>
                    <p class="text-slate-300">
                        • <strong>Điểm nghẽn nghiêm trọng:</strong> Thầy <span class="text-rose-400 font-semibold">Mai Xuân Chinh</span> tồn đọng <strong>10 tickets quá hạn</strong> đang ở trạng thái <em>Cần làm</em> (học liệu Session 4-10). Đối với 6 ticket TRIEKHAI đang <em>Chờ duyệt</em>, đề nghị Leader nghiệm thu đóng dứt điểm.<br>
                        • Thầy Nam và Thầy Kiên mỗi thầy có 1 ticket quá hạn thực sự cần xử lý ngay trong tuần.
                    </p>
                </div>

                <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800 space-y-2">
                    <h4 class="font-bold text-indigo-400 flex items-center gap-1.5">
                        <i class="fa-solid fa-stopwatch-20"></i> 3. Áp Dụng Barem KPI Master FINAL CNTT
                    </h4>
                    <p class="text-slate-300">
                        • <strong>Cân đối lại JD công việc:</strong> Thầy Nam đang dành <strong>41.5% giờ để viết code Dev Tool</strong>, trong khi hỗ trợ học viên chỉ 17%.<br>
                        • Cả 4 thầy có từ 40% - 60% giờ tự do ngoài barem. Cần áp dụng triệt để Barem <strong>KPI Master FINAL CNTT</strong> (chuẩn hóa Trợ giảng lên lớp 120p, CVHT 90-120p/ngày, check BTVN 40p/session) để triệt tiêu khai báo bù giờ ảo.
                    </p>
                </div>
            </div>
        </div>

        <!-- SECTION 5: TOÀN BỘ NHÂN SỰ TOÀN VIỆN (FIXED TYPO & RESPONSIVE SCROLL) -->
        <div class="bg-slate-900/95 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
            <div class="px-5 py-4 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3">
                <div>
                    <h3 class="text-sm font-bold text-white uppercase tracking-wide">IV. Bảng Đánh Giá Xếp Hạng Toàn Bộ Nhân Sự (41 Nhân Sự)</h3>
                    <p class="text-xs text-slate-400">Danh sách đầy đủ dùng để đánh giá và lọc theo từng đợt kiểm toán</p>
                </div>
                
                <div class="flex items-center gap-2 text-xs">
                    <select id="filterGroup" onchange="applyAllStaffFilters()" class="bg-slate-800 text-slate-200 px-2.5 py-1.5 rounded-lg border border-slate-700">
                        <option value="ALL">Tất cả Khối</option>
                        <option value="Khối CNTT Hà Nội">Khối CNTT Hà Nội</option>
                        <option value="Khối CNTT HCM">Khối CNTT HCM</option>
                        <option value="Khối Quản trị Kinh doanh">Khối QTKD</option>
                        <option value="Khối Ngoại ngữ và KNM">Khối Ngoại ngữ</option>
                        <option value="Khối QLCLĐT Hà Nội">Khối QLCLĐT</option>
                        <option value="LMS AI">LMS AI</option>
                    </select>
                    <input type="text" id="searchInput" onkeyup="applyAllStaffFilters()" placeholder="Tìm tên nhân sự..." class="bg-slate-800 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 w-44">
                </div>
            </div>

            <div class="overflow-x-auto max-h-96 overflow-y-auto w-full">
                <table class="w-full text-left text-xs text-slate-300 border-collapse min-w-[950px]">
                    <thead class="bg-slate-950 text-slate-400 uppercase font-bold text-[11px] sticky top-0 z-10 border-b border-slate-800">
                        <tr>
                            <th class="py-2.5 px-3 text-center w-12">#</th>
                            <th class="py-2.5 px-4">Họ và Tên</th>
                            <th class="py-2.5 px-3">Vị trí & Rank</th>
                            <th class="py-2.5 px-3">Khối Đơn vị</th>
                            <th class="py-2.5 px-3 text-center">Nộp Log</th>
                            <th class="py-2.5 px-3 text-center">Giờ TB</th>
                            <th class="py-2.5 px-3 text-center">Quá hạn</th>
                            <th class="py-2.5 px-3 text-center">Lỗi ĐT</th>
                            <th class="py-2.5 px-3 text-center">Điểm KPI</th>
                            <th class="py-2.5 px-3 text-center">Xếp loại</th>
                            <th class="py-2.5 px-3 text-center">Thao tác</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800/60" id="allStaffTableBody">
                        <!-- Rendered by Javascript -->
                    </tbody>
                </table>
            </div>
        </div>

    </main>

    <!-- OFFCANVAS SLIDE-OVER DRAWER FOR ANY STAFF -->
    <div id="drawerBackdrop" onclick="closeDrawer()" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-40 hidden transition-opacity"></div>
    <div id="staffDrawer" class="fixed inset-y-0 right-0 max-w-2xl w-full bg-slate-900 border-l border-slate-800 z-50 transform translate-x-full drawer-slide shadow-2xl flex flex-col">
        
        <!-- DRAWER HEADER -->
        <div class="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950">
            <div class="flex items-center space-x-3.5">
                <div id="drawerAvatar" class="w-11 h-11 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-base shadow-lg">
                    TG
                </div>
                <div>
                    <div class="flex items-center space-x-2">
                        <h2 id="drawerName" class="text-base font-bold text-white">Lại Trung Lâm</h2>
                        <span id="drawerRankBadge" class="px-2 py-0.5 text-xs font-bold rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/40">
                            Rank 2
                        </span>
                    </div>
                    <p id="drawerMeta" class="text-xs text-slate-400">Trợ giảng • Khối CNTT Hà Nội • Cơ sở Ngọc Trục</p>
                </div>
            </div>
            <button onclick="closeDrawer()" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition">
                <i class="fa-solid fa-xmark text-sm"></i>
            </button>
        </div>

        <!-- DRAWER CONTENT -->
        <div class="flex-1 overflow-y-auto p-6 space-y-6">

            <!-- SCORE BANNER -->
            <div class="bg-slate-950 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
                <div>
                    <div class="text-xs text-slate-400 font-semibold uppercase">Điểm Đánh Giá Hiệu Suất Tổng Hợp</div>
                    <div class="flex items-baseline gap-2 mt-1">
                        <span id="drawerTotalScore" class="text-3xl font-black text-indigo-400">99.6</span>
                        <span class="text-xs text-slate-500">/ 100 điểm</span>
                    </div>
                </div>
                <div class="text-right">
                    <span id="drawerGradeBadge" class="text-sm font-bold px-3 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 inline-block">
                        A+ (Xuất sắc)
                    </span>
                    <div id="drawerLeaderNote" class="text-xs text-slate-400 mt-1">Leader: Hồ Xuân Hùng</div>
                </div>
            </div>

            <!-- 4 PILLARS -->
            <div class="space-y-3">
                <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider">Cơ Cấu Điểm Đánh Giá 4 Trụ Cột</h4>
                <div class="grid grid-cols-2 gap-3 text-xs">
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <div class="text-slate-400">1. Tuân Thủ Báo Cáo Ngày (35đ)</div>
                        <div class="text-lg font-bold text-white mt-1" id="scoreLog">35.0 <span class="text-xs text-slate-500 font-normal">/ 35</span></div>
                        <div class="text-[11px] text-slate-400" id="detailLogRate">Tỷ lệ: 100%</div>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <div class="text-slate-400">2. Hoàn Thành Task (25đ)</div>
                        <div class="text-lg font-bold text-emerald-400 mt-1" id="scoreTask">24.6 <span class="text-xs text-slate-500 font-normal">/ 25</span></div>
                        <div class="text-[11px] text-slate-400" id="detailTaskRate">Tỷ lệ: 98.3%</div>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <div class="text-slate-400">3. Tiến Độ Ticket Worklane (25đ)</div>
                        <div class="text-lg font-bold text-blue-400 mt-1" id="scoreIssue">25.0 <span class="text-xs text-slate-500 font-normal">/ 25</span></div>
                        <div class="text-[11px] text-slate-400" id="detailOverdue">Quá hạn (Cần làm): 0 issues</div>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <div class="text-slate-400">4. Kỷ Luật Tác Nghiệp (15đ)</div>
                        <div class="text-lg font-bold text-purple-400 mt-1" id="scoreOps">15.0 <span class="text-xs text-slate-500 font-normal">/ 15</span></div>
                        <div class="text-[11px] text-slate-400" id="detailOps">Vi phạm: 0 lỗi</div>
                    </div>
                </div>
            </div>

            <!-- VIOLATIONS / CONCERNS -->
            <div class="space-y-2.5">
                <h4 class="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
                    <i class="fa-solid fa-triangle-exclamation"></i> Chi Tiết Vi Phạm & Ticket Quá Hạn
                </h4>
                <div id="drawerViolationsList" class="space-y-2 text-xs">
                    <!-- Populated by JS -->
                </div>
            </div>

            <!-- RECOMMENDATIONS -->
            <div class="bg-slate-950 border border-indigo-900/40 rounded-xl p-4 space-y-2">
                <h4 class="text-xs font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                    <i class="fa-solid fa-signature"></i> Nhận Xét & Đề Xuất Của PMO / Quản Lý
                </h4>
                <p id="drawerRecommendation" class="text-xs text-slate-300 leading-relaxed">
                    <!-- Populated by JS -->
                </p>
            </div>

        </div>

        <!-- FOOTER ACTIONS -->
        <div class="p-4 border-t border-slate-800 bg-slate-950 flex items-center justify-between gap-3">
            <button onclick="copyDrawerAppraisal()" class="flex-1 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs transition flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/20">
                <i class="fa-solid fa-copy"></i> Sao Chép Phiếu Gửi Zalo / Lark
            </button>
            <button onclick="window.print()" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition flex items-center gap-1.5 border border-slate-700">
                <i class="fa-solid fa-file-pdf"></i> In / PDF
            </button>
        </div>

    </div>

    <!-- SCRIPT DATA & LOGIC -->
    <script>
        const MASTER_DATA = __JSON_PAYLOAD__;
        const TAS_DATA = MASTER_DATA.tas_analysis;
        let currentPeriodKey = 'period_30days';
        let currentAllStaff = [];
        let filteredAllStaff = [];
        let activeStaffObject = null;
        let timeBreakdownChartInstance = null;
        let violationsBarChartInstance = null;

        document.addEventListener('DOMContentLoaded', () => {
            initDashboard();
        });

        function initDashboard() {
            renderMatrixTable();
            renderCharts();
            selectTATab('lại trung lâm');
            switchPeriod('period_30days');
        }

        function switchPeriod(periodKey) {
            currentPeriodKey = periodKey;
            const period = MASTER_DATA.meta.periods[periodKey];
            if (!period) return;

            document.getElementById('periodBadge').innerText = 'ĐANG XEM: ' + period.name.toUpperCase();
            document.getElementById('periodWorkdaysBadge').innerText = period.workdays_count + ' ngày làm việc tiêu chuẩn';
            document.getElementById('periodDesc').innerText = period.description;

            currentAllStaff = Object.values(period.staff_data);
            currentAllStaff.sort((a, b) => b.scores.total_score - a.scores.total_score);

            applyAllStaffFilters();
        }

        function renderMatrixTable() {
            const tbody = document.getElementById('matrixTableBody');
            tbody.innerHTML = '';

            const tasOrder = ['lại trung lâm', 'mai xuân chinh', 'phạm ngọc kiên', 'đinh thành nam'];
            tasOrder.forEach((k, idx) => {
                const s = TAS_DATA[k];
                if (!s) return;

                let rankBadge = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
                if (s.grade === 'B') rankBadge = 'bg-blue-500/20 text-blue-300 border-blue-500/40';
                if (s.grade === 'C') rankBadge = 'bg-rose-500/20 text-rose-300 border-rose-500/40';

                let scoreColor = 'text-emerald-400';
                if (s.total_score < 80) scoreColor = 'text-amber-400';
                if (s.total_score < 75) scoreColor = 'text-rose-400';
                if (s.total_score >= 80 && s.total_score < 90) scoreColor = 'text-blue-400';

                // Structured evaluation label & note
                let evalLabel = 'Xuất sắc (Gương mẫu)';
                let evalNote = '100% log • 0 ticket trễ • 0 vi phạm';
                if (k === 'mai xuân chinh') {
                    evalLabel = 'Khá (Nề nếp log 100%)';
                    evalNote = '0 ticket trễ trong kỳ • 4 vi phạm quy chế (cần chấn chỉnh)';
                } else if (k === 'phạm ngọc kiên') {
                    evalLabel = 'Khá (Cần lưu ý log)';
                    evalNote = 'Quên 2 log • 1 ticket trễ (1 task miễn trừ)';
                } else if (k === 'đinh thành nam') {
                    evalLabel = 'Cần lưu ý (Log yếu & Lệch JD)';
                    evalNote = 'Log 77.8% • Lệch JD (41.5% dev tool)';
                }

                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-800/60 cursor-pointer transition';
                tr.onclick = () => selectTATab(k);

                tr.innerHTML = `
                    <td class="py-2.5 px-2 text-center font-mono font-bold text-indigo-400">#${idx + 1}</td>
                    <td class="py-2.5 px-3 font-bold text-white whitespace-nowrap">
                        <span>${s.name}</span>
                    </td>
                    <td class="py-2.5 px-2 whitespace-nowrap">
                        <div class="text-slate-300">${s.campus.replace('Cơ sở ', '')}</div>
                        <div class="font-mono text-[10px] text-slate-500">Rank ${s.rank}</div>
                    </td>
                    <td class="py-2.5 px-2 text-center whitespace-nowrap">
                        <div class="font-mono font-bold ${s.log_stats.rate >= 100 ? 'text-emerald-400' : (s.log_stats.rate >= 85 ? 'text-amber-400' : 'text-rose-400')}">${s.log_stats.rate}%</div>
                        <div class="text-[10px] text-slate-500 font-mono">${s.log_stats.reported}/${s.log_stats.expected} ngày</div>
                    </td>
                    <td class="py-2.5 px-2 text-center whitespace-nowrap">
                        <div class="font-mono text-slate-200">${s.log_stats.total_hours}h</div>
                        <div class="text-[10px] text-slate-500 font-mono">${s.log_stats.avg_hours}h/ng</div>
                    </td>
                    <td class="py-2.5 px-2 text-center font-mono font-bold whitespace-nowrap ${s.log_stats.task_rate >= 95 ? 'text-emerald-400' : 'text-slate-300'}">
                        ${s.log_stats.task_rate}%
                    </td>
                    <td class="py-2.5 px-2 text-center whitespace-nowrap">
                        <div class="font-mono text-slate-200">${s.worklane_issues.done}/${s.worklane_issues.total}</div>
                        <div class="text-[10px] text-slate-500 font-mono">${s.worklane_issues.done_rate}%</div>
                    </td>
                    <td class="py-2.5 px-2 text-center whitespace-nowrap font-mono">
                        ${s.worklane_issues.overdue > 0 ? `<span class="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/40 font-bold">${s.worklane_issues.overdue} task</span>` : '<span class="text-slate-500">0</span>'}
                    </td>
                    <td class="py-2.5 px-2 text-center whitespace-nowrap font-mono">
                        ${s.violations.total_count > 0 ? `<span class="text-rose-400 font-bold">${s.violations.total_count} lỗi</span>` : '<span class="text-slate-500">0 lỗi</span>'}
                    </td>
                    <td class="py-2.5 px-2 text-center font-mono font-bold text-sm ${scoreColor} whitespace-nowrap">
                        ${s.total_score.toFixed(1)}
                    </td>
                    <td class="py-2.5 px-3">
                        <div class="flex items-center gap-2">
                            <span class="px-2 py-0.5 rounded text-xs font-black border whitespace-nowrap shrink-0 ${rankBadge}">
                                ${s.grade}
                            </span>
                            <div class="flex flex-col min-w-0">
                                <span class="text-xs font-bold text-white whitespace-nowrap">${evalLabel}</span>
                                <span class="text-[11px] text-slate-400 whitespace-nowrap">${evalNote}</span>
                            </div>
                        </div>
                    </td>
                    <td class="py-2.5 px-2 text-center whitespace-nowrap">
                        <button onclick="event.stopPropagation(); openDrawerForTA('${k}')" class="px-2 py-1 rounded bg-slate-800 hover:bg-indigo-600 text-slate-300 hover:text-white transition text-xs flex items-center gap-1 mx-auto border border-slate-700 shadow-sm">
                            <i class="fa-solid fa-file-lines text-[10px]"></i> Phiếu
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function selectTATab(taKey) {
            const s = TAS_DATA[taKey];
            if (!s) return;

            // Update tab buttons
            const tabButtons = {
                'lại trung lâm': document.getElementById('tab-btn-lam'),
                'phạm ngọc kiên': document.getElementById('tab-btn-kien'),
                'đinh thành nam': document.getElementById('tab-btn-nam'),
                'mai xuân chinh': document.getElementById('tab-btn-chinh')
            };

            Object.keys(tabButtons).forEach(k => {
                if (tabButtons[k]) {
                    if (k === taKey) {
                        tabButtons[k].className = 'px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-indigo-600 text-white shadow-md';
                    } else {
                        tabButtons[k].className = 'px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-slate-800 text-slate-300 hover:bg-slate-700';
                    }
                }
            });

            // Render detailed card
            const container = document.getElementById('taDetailCard');
            let violationsHtml = '';
            if (s.violations.items.length === 0) {
                violationsHtml = `
                    <div class="p-3 rounded-xl bg-emerald-950/20 border border-emerald-900/40 text-emerald-300 flex items-center gap-2">
                        <i class="fa-solid fa-circle-check text-base"></i> Kỷ luật hoàn hảo trong 30 ngày: 0 vi phạm quy chế đào tạo, 0 ticket quá hạn, 0 lỗi tác nghiệp!
                    </div>
                `;
            } else {
                violationsHtml = `
                    <div class="space-y-2">
                        ${s.violations.items.map(v => `
                            <div class="p-2.5 rounded-lg bg-rose-950/20 border border-rose-900/40 text-rose-300 flex items-start gap-2">
                                <i class="fa-solid fa-circle-exclamation mt-0.5 text-rose-400"></i>
                                <div>
                                    <span class="font-bold text-white">[${v.type}]</span> <span class="text-slate-400 font-mono">(${v.date})</span>: ${v.desc}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `;
            }

            let overdueTableHtml = '';
            if (s.worklane_issues.overdue_list.length > 0) {
                overdueTableHtml = `
                    <div class="space-y-2 pt-2">
                        <div class="font-bold text-rose-400 flex items-center gap-1.5">
                            <i class="fa-solid fa-clock-rotate-left"></i> Danh sách ${s.worklane_issues.overdue_list.length} Ticket Quá Hạn (Trạng thái Cần làm - Tính lỗi nhân sự):
                        </div>
                        <div class="max-h-48 overflow-y-auto pr-1">
                            <table class="w-full text-left text-xs">
                                <thead class="text-slate-400 border-b border-slate-800">
                                    <tr>
                                        <th class="py-1.5">Mã Issue</th>
                                        <th class="py-1.5">Tiêu đề Công việc</th>
                                        <th class="py-1.5">Hạn chót</th>
                                        <th class="py-1.5">Trạng thái</th>
                                        <th class="py-1.5">Dự án</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800/40">
                                    ${s.worklane_issues.overdue_list.map(iss => `
                                        <tr>
                                            <td class="py-1 font-mono text-indigo-400">${iss.code}</td>
                                            <td class="py-1 text-slate-200">${iss.title}</td>
                                            <td class="py-1 font-mono text-rose-400">${iss.due}</td>
                                            <td class="py-1"><span class="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px]">${iss.state}</span></td>
                                            <td class="py-1 text-slate-400">${iss.project}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>
                `;
            }

            let pendingApprovalHtml = '';
            if (s.worklane_issues.pending_approval_list && s.worklane_issues.pending_approval_list.length > 0) {
                pendingApprovalHtml = `
                    <div class="space-y-1 pt-2 border-t border-slate-800/80">
                        <div class="font-bold text-indigo-300 text-[11px] flex items-center gap-1.5">
                            <i class="fa-solid fa-user-check text-indigo-400"></i> ${s.worklane_issues.pending_approval_list.length} Ticket Đang Chờ Duyệt (PIC chưa duyệt - Miễn trừ lỗi trễ hạn cho nhân sự):
                        </div>
                        <ul class="text-[11px] text-slate-400 space-y-0.5 pl-3">
                            ${s.worklane_issues.pending_approval_list.map(iss => `
                                <li>• <span class="font-mono text-slate-300">[${iss.code}]</span> ${iss.title} — <span class="text-indigo-400">${iss.state}</span></li>
                            `).join('')}
                        </ul>
                    </div>
                `;
            }

            container.innerHTML = `
                <!-- HEADER CARD -->
                <div class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
                    <div class="flex items-center space-x-3.5">
                        <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg shadow-lg">
                            ${s.name.split(' ').slice(-1)[0][0]}
                        </div>
                        <div>
                            <div class="flex items-center space-x-2.5">
                                <h3 class="text-lg font-bold text-white">${s.name}</h3>
                                <span class="px-2.5 py-0.5 text-xs font-bold rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/40">Rank ${s.rank}</span>
                                <span class="px-2.5 py-0.5 text-xs font-bold rounded bg-slate-800 text-slate-300">${s.campus}</span>
                            </div>
                            <p class="text-xs text-slate-400 mt-0.5">Leader quản lý: <span class="text-indigo-300 font-semibold">${s.leader}</span> • Đơn vị: ${s.group}</p>
                        </div>
                    </div>

                    <div class="flex items-center gap-3">
                        <div class="text-right">
                            <div class="text-2xl font-black text-indigo-400 font-mono">${s.total_score} <span class="text-xs text-slate-400 font-normal">/ 100đ</span></div>
                            <div class="text-xs font-bold text-emerald-400">${s.rank_title}</div>
                        </div>
                        <button onclick="copyStaffAppraisalByKey('${s.key}')" class="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs transition flex items-center gap-1.5 shadow-md">
                            <i class="fa-solid fa-copy"></i> Sao Chép Phiếu
                        </button>
                    </div>
                </div>

                <!-- OVERVIEW TEXT -->
                <div class="bg-slate-950 p-4 rounded-xl border border-slate-800/80 text-xs leading-relaxed text-slate-300 space-y-1">
                    <div class="font-bold text-white uppercase text-[11px] flex items-center gap-1.5">
                        <i class="fa-solid fa-bullseye text-indigo-400"></i> Đánh Giá Chung:
                    </div>
                    <p>${s.overview}</p>
                </div>

                <!-- 4 MAIN STATS COLUMNS -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
                    <!-- LEFT COLUMN: DAILY LOG & TIME BREAKDOWN -->
                    <div class="space-y-3 bg-slate-950/60 p-4 rounded-xl border border-slate-800">
                        <h4 class="font-bold text-white uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                            <i class="fa-solid fa-calendar-days text-indigo-400"></i> 1. Hiệu Suất Báo Cáo Ngày (Daily Reports)
                        </h4>
                        <div class="space-y-1.5 text-slate-300">
                            <div>• <strong>Tỷ lệ nộp:</strong> <span class="font-mono font-bold ${s.log_stats.rate >= 100 ? 'text-emerald-400' : 'text-rose-400'}">${s.log_stats.reported}/${s.log_stats.expected} ngày (${s.log_stats.rate}%)</span></div>
                            ${s.log_stats.missing_days.length > 0 ? `<div class="text-rose-400">• <strong>Ngày QUÊN nộp:</strong> ${s.log_stats.missing_days.join(', ')}</div>` : `<div class="text-emerald-400">• <strong>Nộp đầy đủ 100%:</strong> Không quên ngày nào</div>`}
                            <div>• <strong>Làm thêm cuối tuần:</strong> ${s.log_stats.weekend.join(', ') || 'Không'}</div>
                            <div>• <strong>Tổng giờ khai báo:</strong> <span class="font-mono text-white font-semibold">${s.log_stats.total_hours}h</span> (Bình quân <span class="font-mono text-indigo-300 font-semibold">${s.log_stats.avg_hours}h/ngày</span>)</div>
                            <div>• <strong>Khối lượng Task:</strong> ${s.log_stats.tasks_done}/${s.log_stats.tasks_total} hoàn thành (${s.log_stats.task_rate}%)</div>
                            <div class="text-slate-400 italic">• Task dở dang: ${s.log_stats.uncompleted_desc}</div>
                        </div>

                        <div class="pt-2 border-t border-slate-800">
                            <div class="font-semibold text-slate-300 mb-1.5">Cơ cấu phân bổ thời gian thực tế:</div>
                            <div class="space-y-1 text-[11px]">
                                ${s.time_breakdown.map(tb => `
                                    <div class="flex items-center justify-between">
                                        <span class="text-slate-400 truncate max-w-xs">• ${tb.cat}:</span>
                                        <span class="font-mono text-slate-200 font-semibold">${tb.hours}h (${tb.pct}%)</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>

                    <!-- RIGHT COLUMN: ISSUES & VIOLATIONS -->
                    <div class="space-y-3 bg-slate-950/60 p-4 rounded-xl border border-slate-800">
                        <h4 class="font-bold text-white uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                            <i class="fa-solid fa-list-check text-indigo-400"></i> 2. Quản Lý Dự Án & Issues Worklane
                        </h4>
                        <div class="space-y-1.5 text-slate-300">
                            <div>• <strong>Tổng issues được giao:</strong> <span class="font-mono font-bold text-white">${s.worklane_issues.total} issues</span> (thuộc DA: ${s.worklane_issues.projects.join(', ')})</div>
                            <div>• <strong>Đã hoàn thành:</strong> <span class="font-mono text-emerald-400 font-bold">${s.worklane_issues.done} issues (${s.worklane_issues.done_rate}%)</span></div>
                            <div>• <strong>Đang xử lý / Chưa đóng:</strong> <span class="font-mono text-slate-300">${s.worklane_issues.open} issues</span></div>
                            <div>• <strong>Issues quá hạn deadline (Cần làm):</strong> <span class="font-mono font-bold ${s.worklane_issues.overdue > 0 ? 'text-rose-400' : 'text-slate-400'}">${s.worklane_issues.overdue} issues (${s.worklane_issues.overdue_rate}%)</span></div>
                        </div>

                        ${overdueTableHtml}
                        ${pendingApprovalHtml}
                    </div>
                </div>

                <!-- VIOLATIONS SECTION -->
                <div class="space-y-2">
                    <h4 class="font-bold text-rose-400 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                        <i class="fa-solid fa-triangle-exclamation"></i> 3. Tổng Hợp Vi Phạm Trong 30 Ngày (${s.violations.items.length} sự việc)
                    </h4>
                    ${violationsHtml}
                </div>

                <!-- RECOMMENDATION SECTION -->
                <div class="bg-indigo-950/20 border border-indigo-900/40 p-4 rounded-xl space-y-1.5 text-xs">
                    <div class="font-bold text-indigo-300 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                        <i class="fa-solid fa-signature"></i> 4. Khuyến Nghị Chính Thức Của PMO & Quản Lý
                    </div>
                    <p class="text-slate-300 leading-relaxed">${s.recommendation}</p>
                </div>
            `;
        }

        function renderCharts() {
            if (timeBreakdownChartInstance) timeBreakdownChartInstance.destroy();
            if (violationsBarChartInstance) violationsBarChartInstance.destroy();

            // CHART 1: Stacked Bar Time Breakdown
            const ctxTime = document.getElementById('timeBreakdownChart').getContext('2d');
            const tasOrder = ['Lại Trung Lâm', 'Phạm Ngọc Kiên', 'Đinh Thành Nam', 'Mai Xuân Chinh'];
            
            const chartTasOrder = ['Lại Trung Lâm', 'Mai Xuân Chinh', 'Phạm Ngọc Kiên', 'Đinh Thành Nam'];
            
            timeBreakdownChartInstance = new Chart(ctxTime, {
                type: 'bar',
                data: {
                    labels: chartTasOrder,
                    datasets: [
                        { label: 'Chấm BTVN', data: [22.8, 35.0, 45.0, 8.5], backgroundColor: '#10b981' },
                        { label: 'Học liệu & Nghiên cứu môn', data: [12.5, 44.0, 0.0, 17.0], backgroundColor: '#f59e0b' },
                        { label: 'Phát triển Dev Tool / App', data: [13.5, 28.0, 0.0, 47.5], backgroundColor: '#6366f1' },
                        { label: 'Chăm sóc Học viên', data: [13.0, 12.5, 9.0, 11.0], backgroundColor: '#06b6d4' },
                        { label: 'Trợ giảng lên lớp', data: [6.2, 0.0, 16.0, 0.0], backgroundColor: '#3b82f6' },
                        { label: 'Họp chuyên môn', data: [9.5, 4.0, 3.0, 2.5], backgroundColor: '#8b5cf6' },
                        { label: 'Hỗ trợ chung', data: [80.8, 23.0, 72.0, 28.0], backgroundColor: '#64748b' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: { padding: { top: 10, bottom: 15 } },
                    scales: {
                        x: { stacked: true, grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 11, weight: 'bold' } } },
                        y: { stacked: true, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: {
                        legend: { position: 'top', labels: { color: '#cbd5e1', font: { size: 10 }, boxWidth: 12, padding: 12 } },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => `${ctx.dataset.label}: ${ctx.raw}h`
                            }
                        }
                    }
                }
            });

            // CHART 2: Violations & Overdue (Horizontal labels, clean margins)
            const ctxViolations = document.getElementById('violationsBarChart').getContext('2d');
            violationsBarChartInstance = new Chart(ctxViolations, {
                type: 'bar',
                data: {
                    labels: chartTasOrder,
                    datasets: [
                        { label: 'Ticket Quá hạn (Cần làm)', data: [0, 0, 1, 1], backgroundColor: '#f43f5e', borderRadius: 4 },
                        { label: 'Vi phạm Quy chế / Quên Log', data: [0, 4, 3, 5], backgroundColor: '#fbbf24', borderRadius: 4 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: { padding: { top: 10, bottom: 10 } },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 10 }, autoSkip: false, maxRotation: 0, minRotation: 0 } },
                        y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8', stepSize: 2 } }
                    },
                    plugins: {
                        legend: { position: 'top', labels: { color: '#cbd5e1', font: { size: 10 }, boxWidth: 12, padding: 12 } }
                    }
                }
            });
        }

        function applyAllStaffFilters() {
            const groupFilter = document.getElementById('filterGroup').value;
            const searchVal = document.getElementById('searchInput').value.trim().toLowerCase();

            filteredAllStaff = currentAllStaff.filter(s => {
                if (groupFilter !== 'ALL' && s.group !== groupFilter) return false;
                if (searchVal && !s.name.toLowerCase().includes(searchVal)) return false;
                return true;
            });

            renderAllStaffTable();
        }

        function renderAllStaffTable() {
            const tbody = document.getElementById('allStaffTableBody');
            tbody.innerHTML = '';

            filteredAllStaff.forEach((s, idx) => {
                let badgeClass = 'bg-slate-800 text-slate-300';
                if (s.grade === 'A+') badgeClass = 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40';
                else if (s.grade === 'A') badgeClass = 'bg-blue-500/20 text-blue-300 border border-blue-500/40';
                else if (s.grade === 'B') badgeClass = 'bg-amber-500/20 text-amber-300 border border-amber-500/40';
                else if (s.grade === 'C') badgeClass = 'bg-rose-500/20 text-rose-300 border border-rose-500/40';

                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-800/50 cursor-pointer transition';
                tr.onclick = () => openDrawer(s);

                tr.innerHTML = `
                    <td class="py-2.5 px-3 text-center font-mono text-slate-500">${idx + 1}</td>
                    <td class="py-2.5 px-4 font-bold text-white flex items-center gap-1.5">
                        <span>${s.name}</span>
                        ${s.role === 'Leader' ? '<span class="px-1.5 py-0.2 rounded text-[9px] bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Leader</span>' : ''}
                    </td>
                    <td class="py-2.5 px-3 text-slate-300">${s.role} <span class="text-slate-500 font-mono">(R${s.rank})</span></td>
                    <td class="py-2.5 px-3 text-slate-400">${s.campus}</td>
                    <td class="py-2.5 px-3 text-center font-mono ${s.log_rate >= 100 ? 'text-emerald-400' : (s.log_rate >= 85 ? 'text-amber-400' : 'text-rose-400')}">${s.reported_days}/${s.expected_days}</td>
                    <td class="py-2.5 px-3 text-center font-mono text-slate-300">${s.avg_hours_per_day}h</td>
                    <td class="py-2.5 px-3 text-center font-mono ${s.overdue_issues_count > 0 ? 'text-rose-400 font-bold' : 'text-slate-500'}">${s.overdue_issues_count}</td>
                    <td class="py-2.5 px-3 text-center font-mono ${s.ops_violations_count > 0 ? 'text-rose-400 font-bold' : 'text-slate-500'}">${s.ops_violations_count}</td>
                    <td class="py-2.5 px-3 text-center font-bold text-indigo-300 font-mono">${s.scores.total_score}</td>
                    <td class="py-2.5 px-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] font-bold ${badgeClass}">${s.grade}</span></td>
                    <td class="py-2.5 px-3 text-center">
                        <button class="px-2 py-0.5 rounded bg-slate-800 hover:bg-indigo-600 text-slate-300 hover:text-white transition text-[11px]">Xem</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function openDrawerForTA(taKey) {
            const s = MASTER_DATA.meta.periods['period_30days'].staff_data[taKey];
            if (s) openDrawer(s);
        }

        function openDrawer(staff) {
            activeStaffObject = staff;
            document.getElementById('drawerName').innerText = staff.name;
            document.getElementById('drawerRankBadge').innerText = `Rank ${staff.rank}`;
            document.getElementById('drawerMeta').innerText = `${staff.role} • ${staff.group} • ${staff.campus}`;
            document.getElementById('drawerTotalScore').innerText = staff.scores.total_score;
            document.getElementById('drawerGradeBadge').innerText = `${staff.grade} (${staff.grade_label})`;
            document.getElementById('drawerLeaderNote').innerText = `Leader phụ trách: ${staff.leader}`;

            // Scores
            document.getElementById('scoreLog').innerHTML = `${staff.scores.log_score} <span class="text-xs text-slate-500 font-normal">/ 35</span>`;
            document.getElementById('detailLogRate').innerText = `Tỷ lệ: ${staff.log_rate}% (${staff.reported_days}/${staff.expected_days} ngày)`;

            document.getElementById('scoreTask').innerHTML = `${staff.scores.task_score} <span class="text-xs text-slate-500 font-normal">/ 25</span>`;
            document.getElementById('detailTaskRate').innerText = `Tỷ lệ: ${staff.task_completion_rate}% (${staff.completed_tasks}/${staff.total_tasks} tasks)`;

            document.getElementById('scoreIssue').innerHTML = `${staff.scores.issue_score} <span class="text-xs text-slate-500 font-normal">/ 25</span>`;
            document.getElementById('detailOverdue').innerText = `Quá hạn: ${staff.overdue_issues_count} issues`;

            document.getElementById('scoreOps').innerHTML = `${staff.scores.ops_score} <span class="text-xs text-slate-500 font-normal">/ 15</span>`;
            document.getElementById('detailOps').innerText = `Vi phạm: ${staff.ops_violations_count} lỗi`;

            // Violations list
            const vList = document.getElementById('drawerViolationsList');
            vList.innerHTML = '';
            let hasV = false;

            const taKey = staff.name.toLowerCase();
            if (TAS_DATA[taKey]) {
                const taInfo = TAS_DATA[taKey];
                if (taInfo.violations.items.length > 0) {
                    hasV = true;
                    taInfo.violations.items.forEach(v => {
                        vList.innerHTML += `
                            <div class="p-2.5 rounded-lg bg-rose-950/20 border border-rose-900/40 text-rose-300">
                                <div class="font-bold text-white">[${v.type}] (${v.date}):</div>
                                <div class="text-[11px] text-slate-300 mt-0.5 pl-2">${v.desc}</div>
                            </div>
                        `;
                    });
                }
                if (taInfo.worklane_issues.overdue_list.length > 0) {
                    hasV = true;
                    vList.innerHTML += `
                        <div class="p-2.5 rounded-lg bg-amber-950/20 border border-amber-900/40 text-amber-300">
                            <div class="font-bold"><i class="fa-solid fa-clock-rotate-left"></i> ${taInfo.worklane_issues.overdue_list.length} Ticket Quá Hạn (Cần làm):</div>
                            <ul class="text-[11px] text-slate-300 mt-1 pl-2 space-y-0.5">
                                ${taInfo.worklane_issues.overdue_list.slice(0, 5).map(i => `<li>• [${i.code}] ${i.title} (${i.due})</li>`).join('')}
                                ${taInfo.worklane_issues.overdue_list.length > 5 ? `<li>... và ${taInfo.worklane_issues.overdue_list.length - 5} ticket quá hạn khác</li>` : ''}
                            </ul>
                        </div>
                    `;
                }
                if (taInfo.worklane_issues.pending_approval_list && taInfo.worklane_issues.pending_approval_list.length > 0) {
                    vList.innerHTML += `
                        <div class="p-2 rounded-lg bg-indigo-950/20 border border-indigo-900/30 text-indigo-300 text-[11px]">
                            <div class="font-semibold"><i class="fa-solid fa-user-check"></i> ${taInfo.worklane_issues.pending_approval_list.length} Ticket Đang Chờ Duyệt (Không tính lỗi nhân sự):</div>
                            <div class="text-slate-400 mt-0.5 pl-2">${taInfo.worklane_issues.pending_approval_list.map(i => i.code).join(', ')}</div>
                        </div>
                    `;
                }
            } else {
                if (staff.missing_days && staff.missing_days.length > 0) {
                    hasV = true;
                    vList.innerHTML += `
                        <div class="p-2.5 rounded-lg bg-rose-950/20 border border-rose-900/40 text-rose-300">
                            <div class="font-bold flex items-center gap-1.5"><i class="fa-solid fa-calendar-xmark"></i> Quên nộp báo cáo ngày (${staff.missing_days.length} ngày):</div>
                            <div class="text-[11px] text-slate-400 mt-1 pl-5">${staff.missing_days.join(', ')}</div>
                        </div>
                    `;
                }
                if (staff.overdue_issues && staff.overdue_issues.length > 0) {
                    hasV = true;
                    let listHtml = staff.overdue_issues.slice(0, 5).map(iss => `
                        <li>• [${iss.code || 'ISSUE'}] ${iss.title || 'N/A'} <span class="text-rose-400 font-mono">(Hạn: ${iss.dueDate ? iss.dueDate.substring(0, 10) : (iss.due || 'N/A')})</span></li>
                    `).join('');
                    if (staff.overdue_issues.length > 5) listHtml += `<li>... và ${staff.overdue_issues.length - 5} issues quá hạn khác</li>`;

                    vList.innerHTML += `
                        <div class="p-2.5 rounded-lg bg-amber-950/20 border border-amber-900/40 text-amber-300">
                            <div class="font-bold flex items-center gap-1.5"><i class="fa-solid fa-clock-rotate-left"></i> Ticket quá hạn (${staff.overdue_issues.length} issues):</div>
                            <ul class="text-[11px] text-slate-400 mt-1 pl-3 space-y-0.5">${listHtml}</ul>
                        </div>
                    `;
                }
                if (staff.ops_violations && staff.ops_violations.length > 0) {
                    hasV = true;
                    let opsHtml = staff.ops_violations.map(ov => `
                        <li>• ${ov.Date} | Lớp ${ov.Class}: <span class="text-rose-300 font-semibold">${ov.Error}</span> — ${ov.Details}</li>
                    `).join('');

                    vList.innerHTML += `
                        <div class="p-2.5 rounded-lg bg-rose-950/30 border border-rose-900/50 text-rose-300">
                            <div class="font-bold flex items-center gap-1.5"><i class="fa-solid fa-circle-exclamation"></i> Lỗi tác nghiệp đào tạo (${staff.ops_violations.length} lỗi):</div>
                            <ul class="text-[11px] text-slate-300 mt-1 pl-3 space-y-0.5">${opsHtml}</ul>
                        </div>
                    `;
                }
            }

            if (!hasV) {
                vList.innerHTML = `
                    <div class="p-3 rounded-lg bg-emerald-950/20 border border-emerald-900/40 text-emerald-300 flex items-center gap-2">
                        <i class="fa-solid fa-circle-check text-sm"></i> Kỷ luật hoàn hảo: 0 vi phạm báo cáo ngày, 0 ticket quá hạn, 0 lỗi tác nghiệp!
                    </div>
                `;
            }

            // Recommendation
            let recText = "";
            if (TAS_DATA[taKey]) {
                recText = TAS_DATA[taKey].recommendation;
            } else if (staff.grade === 'A+') {
                recText = `Nhân sự ${staff.name} duy trì kỷ luật và năng suất mẫu mực (100% nộp log, 0 ticket trễ hạn). Đề xuất tuyên dương và duy trì làm nòng cốt trong bộ môn.`;
            } else if (staff.grade === 'A') {
                recText = `Nhân sự ${staff.name} hoàn thành tốt nhiệm vụ được giao. Cần tiếp tục duy trì và chuẩn hóa một số đầu việc tự do sang mã KPI Master chuẩn.`;
            } else if (staff.grade === 'B') {
                recText = `Nhân sự ${staff.name} cần lưu ý cải thiện kỷ luật nộp báo cáo ngày đúng hạn và tập trung xử lý dứt điểm các ticket quá hạn trên Worklane.`;
            } else {
                recText = `CẢNH BÁO: Nhân sự ${staff.name} có tỷ lệ vi phạm cao (quên nộp log nhiều ngày hoặc tồn nhiều ticket quá hạn). Đề nghị Leader ${staff.leader} làm việc trực tiếp để chấn chỉnh kỷ luật tác nghiệp.`;
            }
            document.getElementById('drawerRecommendation').innerText = recText;

            // Open Drawer
            document.getElementById('drawerBackdrop').classList.remove('hidden');
            document.getElementById('staffDrawer').classList.remove('translate-x-full');
        }

        function closeDrawer() {
            document.getElementById('drawerBackdrop').classList.add('hidden');
            document.getElementById('staffDrawer').classList.add('translate-x-full');
            activeStaffObject = null;
        }

        function copyStaffAppraisalByKey(taKey) {
            const s = TAS_DATA[taKey];
            if (!s) return;
            const text = `📋 [PHIẾU ĐÁNH GIÁ NHÂN SỰ PMO]\n` +
                         `• Họ và tên: ${s.name} (${s.role} - Rank ${s.rank})\n` +
                         `• Cơ sở: ${s.campus} • Leader: ${s.leader}\n` +
                         `• Xếp hạng: ${s.rank_title} (Điểm KPI: ${s.total_score}/100 đ)\n` +
                         `• Báo cáo ngày: ${s.log_stats.reported}/${s.log_stats.expected} ngày (${s.log_stats.rate}%)\n` +
                         `• Giờ khai báo: ${s.log_stats.total_hours}h (TB ${s.log_stats.avg_hours}h/ngày)\n` +
                         `• Ticket quá hạn Worklane (Cần làm): ${s.worklane_issues.overdue} issues\n` +
                         `• Vi phạm quy chế đào tạo / Khảo thí: ${s.violations.total_count} vi phạm\n` +
                         `• Đánh giá PMO: ${s.recommendation}\n` +
                         `Hệ thống Quản trị & Đánh giá Đào tạo Worklane PMO`;
            
            navigator.clipboard.writeText(text).then(() => {
                alert('Đã sao chép phiếu đánh giá của ' + s.name + ' vào bộ nhớ tạm! Bạn có thể dán vào Zalo / Lark.');
            }).catch(() => {
                alert('Vui lòng sao chép thủ công.');
            });
        }

        function copyDrawerAppraisal() {
            if (!activeStaffObject) return;
            const s = activeStaffObject;
            const taKey = s.name.toLowerCase();
            if (TAS_DATA[taKey]) {
                copyStaffAppraisalByKey(taKey);
                return;
            }
            const text = `📋 [PHIẾU ĐÁNH GIÁ NHÂN SỰ PMO]\n` +
                         `• Họ và tên: ${s.name} (${s.role} - Rank ${s.rank})\n` +
                         `• Cơ sở: ${s.campus} • Leader: ${s.leader}\n` +
                         `• Điểm KPI: ${s.scores.total_score}/100 đ (Xếp loại: ${s.grade} - ${s.grade_label})\n` +
                         `• Báo cáo ngày: ${s.reported_days}/${s.expected_days} ngày (${s.log_rate}%)\n` +
                         `• Quá hạn: ${s.overdue_issues_count} issues • Vi phạm: ${s.ops_violations_count} lỗi\n` +
                         `• Khuyến nghị: ${document.getElementById('drawerRecommendation').innerText}\n` +
                         `Worklane PMO`;
            navigator.clipboard.writeText(text).then(() => {
                alert('Đã sao chép phiếu đánh giá của ' + s.name + '!');
            });
        }
    </script>
</body>
</html>
"""

# Embed payload
final_html = html_template.replace('__JSON_PAYLOAD__', json_str)

with open(dest_1, 'w', encoding='utf-8') as f:
    f.write(final_html)

with open(dest_2, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Đã xuất bản thành công Master Dashboard mới:")
print(f"  1. {dest_1}")
print(f"  2. {dest_2}")


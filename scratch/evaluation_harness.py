import mysql.connector
import json
import os
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

def run_query(cursor, query, params=None):
    cursor.execute(query, params or ())
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def main():
    # 1. Kết nối MySQL trên cổng 3307
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="",
        database="qldt_el"
    )
    cursor = conn.cursor()

    # 2. Tải dữ liệu dự đoán từ student_risk_data.json
    risk_data_path = 'scratch/student_risk_data.json'
    if not os.path.exists(risk_data_path):
        print(f"Lỗi: Không tìm thấy file dự toán {risk_data_path}. Hãy chạy analyze_student_risk_real.py trước.")
        sys.exit(1)
        
    with open(risk_data_path, 'r', encoding='utf-8') as jf:
        risk_predictions = json.load(jf)

    # 3. Cấu hình các lớp học cần đánh giá giống với run_academic_predictions_v3
    ks24_classes = [
        {'id': 48, 'name': 'HN-KS24-CNTT1', 'course_id': 194},
        {'id': 49, 'name': 'HN-KS24-CNTT2', 'course_id': 194},
        {'id': 156, 'name': 'HN-KS24-CNTT3', 'course_id': 194},
        {'id': 51, 'name': 'HN-KS24-CNTT4', 'course_id': 194},
        {'id': 63, 'name': 'HCM-KS24-CNTT1', 'course_id': 194},
        {'id': 64, 'name': 'HCM-KS24-CNTT2', 'course_id': 162},
    ]
    ks25_classes = [
        {'id': 77, 'name': 'HN-KS25-CNTT1', 'course_id': 193},
        {'id': 76, 'name': 'HN-KS25-CNTT2', 'course_id': 193},
        {'id': 75, 'name': 'HN-KS25-CNTT3', 'course_id': 193},
        {'id': 74, 'name': 'HN-KS25-CNTT4', 'course_id': 193},
        {'id': 73, 'name': 'HN-KS25-CNTT5', 'course_id': 193},
        {'id': 72, 'name': 'HN-KS25-CNTT6', 'course_id': 193},
    ]
    qtkd_classes = [
        {'id': 84, 'name': 'HN-K25-QTKD1', 'course_id': 188},
        {'id': 83, 'name': 'HN-K25-QTKD2', 'course_id': 188},
        {'id': 82, 'name': 'HN-K25-QTKD3', 'course_id': 188},
    ]
    all_classes = ks24_classes + ks25_classes + qtkd_classes

    # Các biến lưu trữ thống kê
    class_evaluations = []
    tp_global = 0  # Predict Fail, Actual Fail
    fp_global = 0  # Predict Fail, Actual Pass
    tn_global = 0  # Predict Pass, Actual Pass
    fn_global = 0  # Predict Pass, Actual Fail

    for c_info in all_classes:
        cid = c_info['id']
        cname = c_info['name']
        co_id = c_info['course_id']

        if cname not in risk_predictions:
            continue

        pred_info = risk_predictions[cname]
        pred_risk_students = {s['code']: s for s in pred_info.get('risk_students', [])}

        # Lấy kết quả thực tế từ DB final_results
        actual_results_raw = run_query(cursor, """
            SELECT fr.student_id, fr.pass, s.student_code, s.full_name
            FROM qldt_el.final_results fr
            JOIN qldt_el.students s ON fr.student_id = s.id
            WHERE fr.class_id = %s AND fr.course_id = %s AND fr.pass IS NOT NULL;
        """, (cid, co_id))

        if cid == 156 and not actual_results_raw:
            # Gộp lớp 156
            actual_results_raw = run_query(cursor, """
                SELECT fr.student_id, fr.pass, s.student_code, s.full_name
                FROM qldt_el.final_results fr
                JOIN qldt_el.students s ON fr.student_id = s.id
                WHERE fr.class_id IN (156, 50, 52) AND fr.course_id = %s AND fr.pass IS NOT NULL;
            """, (co_id,))

        if not actual_results_raw:
            continue

        total_students = len(actual_results_raw)
        actual_pass_count = sum(1 for r in actual_results_raw if r['pass'] == 1)
        actual_pass_rate = (actual_pass_count / total_students) * 100 if total_students > 0 else 100.0

        # Ước tính tỷ lệ đỗ dự đoán từ care list
        # Học viên không có trong risk_students là được dự báo ĐỖ
        risk_count = len(pred_risk_students)
        pred_pass_count = total_students - risk_count
        pred_pass_rate = (pred_pass_count / total_students) * 100 if total_students > 0 else 100.0
        
        # Tính MAE cho lớp này
        class_mae = abs(pred_pass_rate - actual_pass_rate)

        # Tính Confusion Matrix cấp cá nhân trong lớp
        class_tp = class_fp = class_tn = class_fn = 0
        for student in actual_results_raw:
            scode = student['student_code']
            actual_pass = student['pass'] # 1 = Pass, 0 = Fail
            
            # Predict trượt nếu học sinh nằm trong Care List (risk_students)
            predict_fail = scode in pred_risk_students
            
            if predict_fail and actual_pass == 0:
                class_tp += 1
            elif predict_fail and actual_pass == 1:
                class_fp += 1
            elif not predict_fail and actual_pass == 1:
                class_tn += 1
            elif not predict_fail and actual_pass == 0:
                class_fn += 1

        # Cộng dồn thống kê toàn cục
        tp_global += class_tp
        fp_global += class_fp
        tn_global += class_tn
        fn_global += class_fn

        class_evaluations.append({
            'class_name': cname,
            'total_students': total_students,
            'actual_pass_rate': actual_pass_rate,
            'pred_pass_rate': pred_pass_rate,
            'mae': class_mae,
            'confusion': (class_tp, class_fp, class_tn, class_fn)
        })

    # 4. Tính toán các chỉ số chất lượng toàn hệ thống
    total_predictions = tp_global + fp_global + tn_global + fn_global
    avg_mae = np.mean([c['mae'] for c in class_evaluations]) if class_evaluations else 0.0

    # Tránh chia cho 0
    precision = (tp_global / (tp_global + fp_global)) * 100 if (tp_global + fp_global) > 0 else 0.0
    recall = (tp_global / (tp_global + fn_global)) * 100 if (tp_global + fn_global) > 0 else 0.0
    f1_score = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    accuracy = ((tp_global + tn_global) / total_predictions) * 100 if total_predictions > 0 else 0.0

    # 5. Xuất báo cáo Markdown để tích hợp vào Obsidian Vault
    metric_report_path = 'data/evaluation_metrics.md'
    with open(metric_report_path, 'w', encoding='utf-8') as f:
        f.write("# Báo cáo Kiểm định Thuật toán & Hiệu năng Dự báo Học vụ\n\n")
        f.write("> [!NOTE]\n")
        f.write("> Báo cáo này là một phần của **Evaluation Harness**, đánh giá chéo trực tiếp kết quả dự đoán của mô hình với kết quả thi chốt thực tế thu được trong cơ sở dữ liệu học vụ MySQL.\n\n")
        
        f.write("## 1. Chỉ số Hiệu năng Hệ thống (Global Metrics)\n\n")
        f.write("| Chỉ số hiệu năng | Kết quả đạt được | Ý nghĩa lâm sàng / Vận hành |\n")
        f.write("| :--- | :---: | :--- |\n")
        f.write(f"| **Sai số Tuyệt đối TB (MAE)** | **{avg_mae:.2f}%** | Lệch tỷ lệ đỗ trung bình giữa dự báo và thực tế trên mỗi lớp |\n")
        f.write(f"| **Độ chính xác (Accuracy)** | **{accuracy:.2f}%** | Tỷ lệ dự đoán đúng đỗ/trượt trên tổng số học sinh |\n")
        f.write(f"| **Độ xác thực (Precision)** | **{precision:.2f}%** | Tỷ lệ học sinh thực sự trượt trong tổng số học sinh bị cảnh báo trượt (Tránh cảnh báo ảo) |\n")
        f.write(f"| **Độ phủ (Recall/Sensitivity)** | **{recall:.2f}%** | Tỷ lệ phát hiện được học sinh trượt thực tế (Tránh bỏ sót học viên nguy cơ) |\n")
        f.write(f"| **Điểm F1-Score** | **{f1_score/100:.3f}** | Chỉ số hài hòa cân bằng giữa Precision và Recall |\n\n")

        f.write("### Ma trận nhầm lẫn toàn cục (Global Confusion Matrix):\n")
        f.write(f"- **True Positive (TP)**: {tp_global} học viên (Dự báo Trượt $\\rightarrow$ Thực tế Trượt)\n")
        f.write(f"- **False Positive (FP)**: {fp_global} học viên (Dự báo Trượt $\\rightarrow$ Thực tế Đỗ - *Cảnh báo ảo*)\n")
        f.write(f"- **True Negative (TN)**: {tn_global} học viên (Dự báo Đỗ $\\rightarrow$ Thực tế Đỗ)\n")
        f.write(f"- **False Negative (FN)**: {fn_global} học viên (Dự báo Đỗ $\\rightarrow$ Thực tế Trượt - *Bỏ sót*)\n\n")

        f.write("## 2. Chi tiết Đánh giá theo từng lớp học\n\n")
        f.write("| Tên lớp | Sĩ số | Tỷ lệ Đỗ Thực tế | Tỷ lệ Đỗ Dự báo | Sai số (MAE) | TP / FP / TN / FN |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")
        for c in class_evaluations:
            tp, fp, tn, fn = c['confusion']
            f.write(f"| [[student_risk_report#Lớp: {c['class_name']}|{c['class_name']}]] | {c['total_students']} | {c['actual_pass_rate']:.1f}% | {c['pred_pass_rate']:.1f}% | {c['mae']:.2f}% | {tp} / {fp} / {tn} / {fn} |\n")

        f.write("\n---\n\n")
        f.write("## 3. Đánh giá & Khuyến nghị Kỹ thuật từ Harness\n\n")
        if avg_mae < 12.0:
            f.write("> [!TIP]\n")
            f.write(f"> Thuật toán hiện tại đang hoạt động cực kỳ tốt với MAE = {avg_mae:.2f}% (đạt mục tiêu Grid Search < 12%). Trọng số Hyperparameters hiện tại phù hợp với hành vi học tập thực tế.\n")
        else:
            f.write("> [!WARNING]\n")
            f.write(f"> Sai số MAE là {avg_mae:.2f}% vượt ngưỡng tối ưu 12%. Cần thực hiện Grid Search lại các tham số w1, w2 trong `grid_search_hyperparameters.py` để tìm điểm tối ưu mới.\n")
            
        if recall < 80.0:
            f.write("> [!CAUTION]\n")
            f.write(f"> Độ phủ (Recall) hiện tại chỉ đạt {recall:.2f}%. Mô hình đang bỏ sót khá nhiều học sinh có nguy cơ trượt thực tế. Hãy cân nhắc nới lỏng các chốt chặn kỷ luật hoặc giảm ngưỡng an toàn của p_eligible từ 50% lên 55% để cảnh báo sớm nhạy hơn.\n")

    print(f"Harness Evaluation completed. Metrics report generated at: {metric_report_path}")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

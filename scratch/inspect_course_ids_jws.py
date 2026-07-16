import mysql.connector
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

conn = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="",
    database="qldt_el"
)
cursor = conn.cursor()

# We import the core functions from the predictions script
sys.path.append('scratch')
from run_cross_validation_predictions import get_excel_chot_data, predict_class_pass_rate

excel_data = get_excel_chot_data("docs/PTIT_Chiso.xlsx")

# Class ID for HN-KS24-CNTT1 is 48 (or let's find it dynamically)
cursor.execute("SELECT id FROM classes WHERE name = 'HN-KS24-CNTT1';")
class_id = cursor.fetchone()[0]

# Get sequence map
cursor.execute("SELECT DISTINCT class_id, course_id FROM final_results;")
class_course_seq = {}
for r in cursor.fetchall():
    cid_val = r[0]
    co_val = r[1]
    if cid_val not in class_course_seq:
        class_course_seq[cid_val] = []
    class_course_seq[cid_val].append(co_val)

# Run prediction
res = predict_class_pass_rate(cursor, class_id, 214, class_course_seq, excel_data, 'HN-KS24-CNTT1', '[IT-212] AI Application in Action', 'K24')
print("\nClass HN-KS24-CNTT1 AI Application prediction results:")
print(f"Size: {res['size']}, Class Average Old Rule: {res['avg_pred_old']:.2f}%, New Rule: {res['avg_pred_new']:.2f}%")
print("First 10 students detail:")
for s in res['students'][:10]:
    print(f"Name: {s['full_name']} | P_final: {s['p_final']:.2f}% | Risk: {s['risk_level']} | Reasons: {s['reasons']}")
    print(f"  CC vắng: {s['att']:.1f}% | HW: {s['hw']:.1f}% | EL: {s['el']:.1f} | RP: {s['rp']:.1f}")

conn.close()

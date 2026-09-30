import unittest

def classify_behavior(m1_cc_violate, m1_hw_violate, m1_el_violate, m2_cc_violate, m2_hw_violate, m2_el_violate):
    """
    Classify student into TH1, TH2, TH3, TH4 based on baseline vs new courses violations.
    """
    m1_violate_avg = (m1_cc_violate + m1_hw_violate + m1_el_violate) / 3.0
    m2_violate_avg = (m2_cc_violate + m2_hw_violate + m2_el_violate) / 3.0
    
    # TH1: Persistent High Risk - M1 CC >= 40% (or avg >= 50%) and M2 CC >= 20% or M2 avg >= 20%
    if (m1_cc_violate >= 40.0 or m1_violate_avg >= 50.0) and (m2_cc_violate >= 20.0 or m2_violate_avg >= 20.0):
        return 'TH1_PERSISTENT_RISK'
    
    # TH4: New Emergent Risk - M1 was good (< 20%), but M2 has high violation (>= 40% in hw or cc)
    if m1_violate_avg < 20.0 and (m2_hw_violate >= 40.0 or m2_cc_violate >= 40.0 or m2_violate_avg >= 30.0):
        return 'TH4_NEW_EMERGENT_RISK'
    
    # TH3: Turnaround / Resolved - M1 had violation (> 0%), but M2 is clean (0% or near 0%)
    if m1_violate_avg > 0 and m2_violate_avg == 0:
        return 'TH3_RESOLVED'
        
    # TH2: Improving - M1 had violation, M2 has reduced violation significantly
    if m2_violate_avg < m1_violate_avg:
        return 'TH2_IMPROVING'
        
    # Fallback clean student
    if m1_violate_avg == 0 and m2_violate_avg == 0:
        return 'TH3_RESOLVED'
        
    return 'TH2_IMPROVING'

def calculate_class_improvement_rate(students_in_class):
    if not students_in_class:
        return 0.0
    improved_count = sum(1 for s in students_in_class if s['group'] in ['TH2_IMPROVING', 'TH3_RESOLVED'])
    return round((improved_count / len(students_in_class)) * 100.0, 2)

class TestK26BehavioralShifts(unittest.TestCase):
    def test_th1_persistent_risk(self):
        # M1 high CC violation (50%), M2 still high (30%)
        res = classify_behavior(50, 0, 0, 30, 0, 0)
        self.assertEqual(res, 'TH1_PERSISTENT_RISK')

    def test_th4_new_emergent(self):
        # M1 clean (0%), M2 homework debt 80% (shocked by IT108)
        res = classify_behavior(0, 0, 0, 0, 80, 20)
        self.assertEqual(res, 'TH4_NEW_EMERGENT_RISK')

    def test_th3_resolved(self):
        # M1 had EL violation 40%, M2 clean 0%
        res = classify_behavior(0, 0, 40, 0, 0, 0)
        self.assertEqual(res, 'TH3_RESOLVED')

    def test_th2_improving(self):
        # M1 had 60% violation, M2 dropped to 10%
        res = classify_behavior(20, 60, 40, 0, 10, 5)
        self.assertEqual(res, 'TH2_IMPROVING')

    def test_class_improvement_rate(self):
        sample_students = [
            {'group': 'TH3_RESOLVED'},
            {'group': 'TH2_IMPROVING'},
            {'group': 'TH1_PERSISTENT_RISK'},
            {'group': 'TH4_NEW_EMERGENT_RISK'},
        ]
        # 2 out of 4 improved = 50%
        rate = calculate_class_improvement_rate(sample_students)
        self.assertEqual(rate, 50.0)

if __name__ == '__main__':
    unittest.main()

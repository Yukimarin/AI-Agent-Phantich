import json
import os

class CompetencyEngine:
    def __init__(self, config_path="harness/config/job_thresholds.json"):
        self.config_path = config_path
        self.thresholds = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found at: {self.config_path}")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f).get("thresholds", {})

    def calculate_job_readiness(self, student_scores, cohort, job_role):
        """
        Calculates the job readiness % of a student based on weights.
        student_scores: dict of {course_code: score}
        """
        cohort_rules = self.thresholds.get(cohort, {})
        job_rule = cohort_rules.get(job_role, {})
        
        if not job_rule:
            raise ValueError(f"Job role {job_role} not defined for cohort {cohort}")
            
        required_courses = job_rule.get("required_courses", [])
        weights = job_rule.get("weight", {})
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for course in required_courses:
            score = student_scores.get(course, 0.0)
            weight = weights.get(course, 1.0 / len(required_courses))
            weighted_sum += score * weight
            total_weight += weight
            
        if total_weight == 0:
            return 0.0
            
        # Returns raw percentage (0.0 to 100.0)
        return round(weighted_sum, 2)

if __name__ == "__main__":
    engine = CompetencyEngine()
    # Mock test
    mock_scores = {
        "IT203B-K24": 80.0,
        "IT210-K24": 75.0,
        "IT211-K24": 70.0,
        "IT202-K24": 85.0
    }
    readiness = engine.calculate_job_readiness(mock_scores, "KS24_CNTT", "Backend_Developer_Java")
    print(f"Mock Java Developer Readiness: {readiness}%")

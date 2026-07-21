import mysql.connector
import openpyxl
import sys
import os
import unicodedata
from collections import defaultdict

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# MySQL connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'qldt_el',
    'port': 3307
}

def main():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Query pass rates grouping by class and course
        query = """
            SELECT 
                c.id as class_id, 
                c.name as class_name, 
                co.id as course_id, 
                co.name as course_name, 
                COUNT(f.student_id) as total_students,
                SUM(CASE WHEN f.pass = 1 THEN 1 ELSE 0 END) as passed_students,
                (SUM(CASE WHEN f.pass = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(f.student_id)) as pass_rate
            FROM final_results f
            JOIN classes c ON f.class_id = c.id
            JOIN courses co ON f.course_id = co.id
            GROUP BY c.id, c.name, co.id, co.name
            ORDER BY c.name, co.name
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        print(f"Total class-course combinations in final_results: {len(rows)}")
        print("\nFirst 30 rows of pass rates:")
        for r in rows[:30]:
            print(f"Class: {r['class_name']} ({r['class_id']}) | Course: {r['course_name']} ({r['course_id']}) | Total Students: {r['total_students']} | Passed: {r['passed_students']} | Pass Rate: {r['pass_rate']:.2f}%")
            
        # Write all results to a temporary text file for search/lookup
        with open("scratch/db_pass_rates.txt", "w", encoding="utf-8") as f:
            for r in rows:
                f.write(f"ClassID: {r['class_id']} | ClassName: {r['class_name']} | CourseID: {r['course_id']} | CourseName: {r['course_name']} | Total: {r['total_students']} | Passed: {r['passed_students']} | PassRate: {r['pass_rate']:.2f}%\n")
                
        conn.close()
    except Exception as e:
        print("Error connecting to MySQL:", str(e))

if __name__ == "__main__":
    main()

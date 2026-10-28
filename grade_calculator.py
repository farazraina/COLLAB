# =====================================================================
# grade_calculator.py
# Calculates letter grades, remarks, CGPA, and aggregate statistics
# for single scores and multi-subject marks collections.
# =====================================================================

DEFAULT_SUBJECTS = [
    "Mathematics",
    "Python Programming",
    "Professional Skills",
    "Database Management",
    "DSD"
]


def calculate_grade(marks):
    """
    Takes marks or percentage (number from 0 to 100) and returns the letter grade.
    90 - 100 : A+ (Outstanding)
    80 - 89  : A  (Excellent)
    70 - 79  : B  (Very Good)
    60 - 69  : C  (Good)
    40 - 59  : D  (Pass)
    Below 40 : F  (Fail)
    """
    try:
        marks = float(marks)
    except (ValueError, TypeError):
        return "N/A"

    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"


def get_grade_remark(grade):
    """
    Returns a simple English explanation for each letter grade.
    """
    remarks = {
        "A+": "Outstanding",
        "A":  "Excellent",
        "B":  "Very Good",
        "C":  "Good",
        "D":  "Pass",
        "F":  "Needs Help (Failed)"
    }
    return remarks.get(grade, "No Grade")


def calculate_cgpa(percentage):
    """
    Converts a percentage (0 - 100) to a standard 10.0 scale CGPA.
    """
    try:
        pct = float(percentage)
        cgpa = max(0.0, min(10.0, pct / 10.0))
        return round(cgpa, 2)
    except (ValueError, TypeError):
        return 0.0


def calculate_student_stats(subjects_dict):
    """
    Given a dictionary of {subject_name: marks_obtained}, computes:
    - total_marks (sum of all subject marks)
    - max_marks (len(subjects) * 100)
    - percentage (total_marks / max_marks * 100)
    - grade (letter grade)
    - cgpa (10.0 scale)
    - remark (grade explanation)
    - passed_count (subjects with >= 40 marks)
    - failed_count (subjects with < 40 marks)
    - status ('PASSED' if all subjects >= 40 and pct >= 40, else 'NEEDS ATTENTION' or 'FAILED')
    """
    if not subjects_dict:
        return {
            "total_marks": 0.0,
            "max_marks": 0.0,
            "percentage": 0.0,
            "grade": "N/A",
            "cgpa": 0.0,
            "remark": "No Data",
            "passed_count": 0,
            "failed_count": 0,
            "status": "NO DATA"
        }

    total = 0.0
    passed_subjects = 0
    failed_subjects = 0

    for subj, val in subjects_dict.items():
        try:
            m = float(val)
        except (ValueError, TypeError):
            m = 0.0
        total += m
        if m >= 40.0:
            passed_subjects += 1
        else:
            failed_subjects += 1

    count = len(subjects_dict)
    max_marks = count * 100.0
    percentage = round((total / max_marks) * 100.0, 2) if max_marks > 0 else 0.0
    grade = calculate_grade(percentage)
    cgpa = calculate_cgpa(percentage)
    remark = get_grade_remark(grade)

    if failed_subjects == 0 and percentage >= 40.0:
        status = "PASSED"
    elif failed_subjects > 0 and percentage >= 40.0:
        status = "REMEDIAL REQUIRED"
    else:
        status = "FAILED"

    return {
        "total_marks": round(total, 2),
        "max_marks": max_marks,
        "percentage": percentage,
        "grade": grade,
        "cgpa": cgpa,
        "remark": remark,
        "passed_count": passed_subjects,
        "failed_count": failed_subjects,
        "status": status
    }

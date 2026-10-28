"""
grade_calculator.py - Grading System for Student Evaluation.
Maps numeric marks to academic letter grades with clear thresholds.
"""


def calculate_grade(marks):
    """
    Calculate letter grade based on marks (0 to 100).
    - 90 - 100 : A+ (Outstanding)
    - 80 - 89  : A  (Excellent)
    - 70 - 79  : B  (Very Good)
    - 60 - 69  : C  (Good)
    - 40 - 59  : D  (Pass)
    - Below 40 : F  (Fail / Academic Support Required)
    """
    try:
        numeric_marks = float(marks)
    except (ValueError, TypeError):
        return "N/A"

    if numeric_marks >= 90:
        return "A+"
    elif numeric_marks >= 80:
        return "A"
    elif numeric_marks >= 70:
        return "B"
    elif numeric_marks >= 60:
        return "C"
    elif numeric_marks >= 40:
        return "D"
    else:
        return "F"


def get_grade_remark(grade):
    """Return a descriptive remark corresponding to a letter grade."""
    remarks = {
        "A+": "Outstanding Performance",
        "A":  "Excellent Achievement",
        "B":  "Very Good",
        "C":  "Good / Satisfactory",
        "D":  "Passing Standard",
        "F":  "Needs Academic Support",
    }
    return remarks.get(grade, "No Grade Available")
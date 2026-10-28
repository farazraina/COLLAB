# =====================================================================
# grade_calculator.py
# This file calculates the letter grade based on a student's marks.
# =====================================================================

def calculate_grade(marks):
    """
    Takes marks (number from 0 to 100) and returns the letter grade.
    90 - 100 : A+ (Outstanding)
    80 - 89  : A  (Excellent)
    70 - 79  : B  (Very Good)
    60 - 69  : C  (Good)
    40 - 59  : D  (Pass)
    Below 40 : F  (Fail)
    """
    # Make sure marks is a float number
    try:
        marks = float(marks)
    except (ValueError, TypeError):
        return "N/A"

    # Check the marks range
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
    Returns a simple English explanation for each grade.
    """
    if grade == "A+":
        return "Outstanding"
    elif grade == "A":
        return "Excellent"
    elif grade == "B":
        return "Very Good"
    elif grade == "C":
        return "Good"
    elif grade == "D":
        return "Pass"
    elif grade == "F":
        return "Needs Help (Failed)"
    else:
        return "No Grade"
# =====================================================================
# analytics.py
# This file calculates class statistics (average, highest, pass/fail)
# and displays a simple dashboard.
# =====================================================================

from grade_calculator import calculate_grade


def calculate_analytics(students):
    """
    Calculates summary numbers from the list of students:
    - Total students
    - Class average marks
    - Highest and lowest marks
    - Number of passed and failed students
    - Count of each grade (A+, A, B, C, D, F)
    """
    # If there are no students, return empty defaults
    if not students:
        return {
            "total": 0,
            "average": 0.0,
            "highest": 0.0,
            "lowest": 0.0,
            "passed": 0,
            "failed": 0,
            "pass_percentage": 0.0,
            "grade_counts": {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0},
            "course_stats": {},
            "score_ranges": {"0-39 (Fail)": 0, "40-59 (Pass)": 0, "60-79 (Good)": 0, "80-100 (High)": 0}
        }

    # Step 1: Collect all marks into a simple list
    marks_list = []
    for s in students:
        marks_list.append(float(s["marks"]))

    total_students = len(students)
    total_marks = sum(marks_list)
    average_marks = round(total_marks / total_students, 2)
    highest_marks = max(marks_list)
    lowest_marks = min(marks_list)

    # Step 2: Count how many students passed (marks >= 40)
    passed_count = 0
    for marks in marks_list:
        if marks >= 40:
            passed_count = passed_count + 1

    failed_count = total_students - passed_count
    pass_percentage = round((passed_count / total_students) * 100, 2)

    # Step 3: Count how many students got each grade
    grade_counts = {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for s in students:
        grade = calculate_grade(s["marks"])
        if grade in grade_counts:
            grade_counts[grade] = grade_counts[grade] + 1

    # Step 4: Group students by course
    course_groups = {}
    for s in students:
        course = s.get("course", "General").strip().title()
        if course not in course_groups:
            course_groups[course] = []
        course_groups[course].append(float(s["marks"]))

    course_stats = {}
    for course_name, course_marks in course_groups.items():
        course_stats[course_name] = {
            "count": len(course_marks),
            "average": round(sum(course_marks) / len(course_marks), 2)
        }

    # Step 5: Count students in score ranges
    score_ranges = {
        "0-39 (Fail)": 0,
        "40-59 (Pass)": 0,
        "60-79 (Good)": 0,
        "80-100 (High)": 0
    }
    for m in marks_list:
        if m < 40:
            score_ranges["0-39 (Fail)"] += 1
        elif m < 60:
            score_ranges["40-59 (Pass)"] += 1
        elif m < 80:
            score_ranges["60-79 (Good)"] += 1
        else:
            score_ranges["80-100 (High)"] += 1

    return {
        "total": total_students,
        "average": average_marks,
        "highest": highest_marks,
        "lowest": lowest_marks,
        "passed": passed_count,
        "failed": failed_count,
        "pass_percentage": pass_percentage,
        "grade_counts": grade_counts,
        "course_stats": course_stats,
        "score_ranges": score_ranges
    }


def show_dashboard(students):
    """
    Prints a simple text dashboard in the terminal.
    """
    print("\n==========================================")
    print("      CLASS PERFORMANCE DASHBOARD")
    print("==========================================")

    if not students:
        print("No student records available.")
        return

    stats = calculate_analytics(students)

    print("Total Students   :", stats["total"])
    print("Class Average    :", stats["average"])
    print("Highest Marks    :", stats["highest"])
    print("Lowest Marks     :", stats["lowest"])
    print("Students Passed  :", stats["passed"])
    print("Students Failed  :", stats["failed"])
    print("Pass Percentage  :", stats["pass_percentage"], "%")

    print("\nGrade Counts:")
    for grade, count in stats["grade_counts"].items():
        print(f"  Grade {grade}: {count} student(s)")
    print("==========================================")
# =====================================================================
# analytics.py
# Computes comprehensive class performance analytics, grade distributions,
# course breakdowns, and multi-subject statistical benchmarks.
# =====================================================================

from grade_calculator import DEFAULT_SUBJECTS, calculate_grade


def calculate_analytics(students):
    """
    Calculates detailed summary metrics across all students:
    - Overall cohort statistics (Total, Class Average, Highest %, Lowest %, Pass/Fail)
    - Multi-subject breakdowns (Averages, Highs, Lows, Pass Rates per subject)
    - Grade distribution counts (A+, A, B, C, D, F)
    - Course / stream statistics
    - Score brackets distribution
    """
    default_subjs = {s: {"average": 0.0, "highest": 0.0, "lowest": 0.0, "passed": 0, "pass_rate": 0.0} for s in DEFAULT_SUBJECTS}

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
            "score_ranges": {"0-39 (Fail)": 0, "40-59 (Pass)": 0, "60-79 (Good)": 0, "80-100 (High)": 0},
            "subject_stats": default_subjs
        }

    total_students = len(students)

    # Collect percentages / marks
    percentages = []
    for s in students:
        pct = float(s.get("percentage", s.get("marks", 0.0)))
        percentages.append(pct)

    total_pct_sum = sum(percentages)
    average_percentage = round(total_pct_sum / total_students, 2)
    highest_percentage = round(max(percentages), 2)
    lowest_percentage = round(min(percentages), 2)

    # Pass / Fail counts based on overall percentage
    passed_count = sum(1 for p in percentages if p >= 40.0)
    failed_count = total_students - passed_count
    pass_percentage = round((passed_count / total_students) * 100.0, 2)

    # Grade distribution counts
    grade_counts = {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for p in percentages:
        g = calculate_grade(p)
        if g in grade_counts:
            grade_counts[g] += 1

    # Course grouping
    course_groups = {}
    for s in students:
        course = s.get("course", "General").strip().title()
        if course not in course_groups:
            course_groups[course] = []
        course_groups[course].append(float(s.get("percentage", s.get("marks", 0.0))))

    course_stats = {}
    for course_name, pcts in course_groups.items():
        course_stats[course_name] = {
            "count": len(pcts),
            "average": round(sum(pcts) / len(pcts), 2)
        }

    # Score brackets distribution
    score_ranges = {
        "0-39 (Fail)": 0,
        "40-59 (Pass)": 0,
        "60-79 (Good)": 0,
        "80-100 (High)": 0
    }
    for p in percentages:
        if p < 40.0:
            score_ranges["0-39 (Fail)"] += 1
        elif p < 60.0:
            score_ranges["40-59 (Pass)"] += 1
        elif p < 80.0:
            score_ranges["60-79 (Good)"] += 1
        else:
            score_ranges["80-100 (High)"] += 1

    # Subject-wise statistics
    subject_stats = {}
    for subj in DEFAULT_SUBJECTS:
        subj_marks = []
        for s in students:
            subjs = s.get("subjects", {})
            m = float(subjs.get(subj, s.get("marks", 0.0)))
            subj_marks.append(m)

        if subj_marks:
            s_avg = round(sum(subj_marks) / len(subj_marks), 2)
            s_high = round(max(subj_marks), 2)
            s_low = round(min(subj_marks), 2)
            s_pass = sum(1 for m in subj_marks if m >= 40.0)
            s_pass_rate = round((s_pass / len(subj_marks)) * 100.0, 2)
        else:
            s_avg = s_high = s_low = s_pass = s_pass_rate = 0.0

        subject_stats[subj] = {
            "average": s_avg,
            "highest": s_high,
            "lowest": s_low,
            "passed": s_pass,
            "pass_rate": s_pass_rate
        }

    return {
        "total": total_students,
        "average": average_percentage,
        "highest": highest_percentage,
        "lowest": lowest_percentage,
        "passed": passed_count,
        "failed": failed_count,
        "pass_percentage": pass_percentage,
        "grade_counts": grade_counts,
        "course_stats": course_stats,
        "score_ranges": score_ranges,
        "subject_stats": subject_stats
    }


def show_dashboard(students):
    """
    Prints a clean performance summary to the terminal.
    """
    print("\n==========================================")
    print("      CLASS PERFORMANCE DASHBOARD")
    print("==========================================")

    if not students:
        print("No student records available.")
        return

    stats = calculate_analytics(students)

    print("Total Students   :", stats["total"])
    print("Class Average    :", stats["average"], "%")
    print("Highest Score    :", stats["highest"], "%")
    print("Lowest Score     :", stats["lowest"], "%")
    print("Students Passed  :", stats["passed"])
    print("Students Failed  :", stats["failed"])
    print("Pass Percentage  :", stats["pass_percentage"], "%")

    print("\nSubject-Wise Averages:")
    for subj, data in stats["subject_stats"].items():
        print(f"  {subj:<22}: {data['average']:.2f}% (High: {data['highest']}, Low: {data['lowest']})")

    print("\nGrade Counts:")
    for grade, count in stats["grade_counts"].items():
        print(f"  Grade {grade}: {count} student(s)")
    print("==========================================")

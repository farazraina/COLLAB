"""
analytics.py - Performance Analytics Module for Student Management System.
Computes statistical indicators, grade distributions, and course summaries.
"""

from grade_calculator import calculate_grade


def calculate_analytics(students):
    """
    Compute comprehensive class performance analytics from student records.
    Returns a dictionary of metrics for consumption by CLI and GUI dashboards.
    """
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
        }

    marks_list = [float(s.get("marks", 0)) for s in students]
    total = len(students)
    avg_marks = sum(marks_list) / total
    high_marks = max(marks_list)
    low_marks = min(marks_list)

    passed_count = sum(1 for m in marks_list if m >= 40)
    failed_count = total - passed_count
    pass_pct = (passed_count / total) * 100

    # Grade distribution counts
    grade_counts = {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for s in students:
        g = calculate_grade(s.get("marks", 0))
        if g in grade_counts:
            grade_counts[g] += 1

    # Course statistics
    course_groups = {}
    for s in students:
        c = s.get("course", "General").strip().title() or "General"
        course_groups.setdefault(c, []).append(float(s.get("marks", 0)))

    course_stats = {}
    for c_name, c_marks in course_groups.items():
        course_stats[c_name] = {
            "count": len(c_marks),
            "average": round(sum(c_marks) / len(c_marks), 2),
            "highest": max(c_marks),
            "lowest": min(c_marks),
        }

    # Score range breakdown
    score_ranges = {
        "0-39 (Fail)": sum(1 for m in marks_list if m < 40),
        "40-59 (Pass)": sum(1 for m in marks_list if 40 <= m < 60),
        "60-79 (Good)": sum(1 for m in marks_list if 60 <= m < 80),
        "80-100 (High)": sum(1 for m in marks_list if m >= 80),
    }

    return {
        "total": total,
        "average": round(avg_marks, 2),
        "highest": round(high_marks, 2),
        "lowest": round(low_marks, 2),
        "passed": passed_count,
        "failed": failed_count,
        "pass_percentage": round(pass_pct, 2),
        "grade_counts": grade_counts,
        "course_stats": course_stats,
        "score_ranges": score_ranges,
    }


def show_dashboard(students):
    """Print an attractive text-based performance dashboard to the terminal."""
    print("\n" + "=" * 50)
    print("        CLASS PERFORMANCE DASHBOARD")
    print("=" * 50)

    if not students:
        print("  [Notice] No student records available to display.")
        print("=" * 50)
        return

    data = calculate_analytics(students)

    print(f"  • Total Enrolled Students : {data['total']}")
    print(f"  • Class Average Marks     : {data['average']:.2f}")
    print(f"  • Highest Score Achieved  : {data['highest']}")
    print(f"  • Lowest Score Recorded   : {data['lowest']}")
    print(f"  • Passing Students        : {data['passed']} ({data['pass_percentage']}%)")
    print(f"  • At-Risk / Failing       : {data['failed']}")
    print("-" * 50)
    print("  Grade Distribution:")
    for grade, count in data["grade_counts"].items():
        bar = "█" * count
        print(f"    {grade:>2} : {count:>2} student(s) {bar}")
    print("=" * 50)
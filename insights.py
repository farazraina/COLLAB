"""
insights.py - Actionable Academic Insights Module for Student Management System.
Identifies high achievers, students requiring support, and overall performance trends.
"""

from grade_calculator import calculate_grade


def get_insights(students):
    """
    Extract key qualitative and actionable academic insights from student records.
    Returns a dictionary of insights data.
    """
    if not students:
        return {
            "top_performer": None,
            "average": 0.0,
            "struggling_students": [],
            "top_performers_list": [],
        }

    # Top overall student
    top_student = max(students, key=lambda s: float(s.get("marks", 0)))

    # List of all students with grade A or A+
    top_performers = [
        s for s in students if float(s.get("marks", 0)) >= 80
    ]

    # Students scoring below passing mark (40)
    struggling = [
        s for s in students if float(s.get("marks", 0)) < 40
    ]

    avg_marks = sum(float(s.get("marks", 0)) for s in students) / len(students)

    return {
        "top_performer": top_student,
        "average": round(avg_marks, 2),
        "struggling_students": struggling,
        "top_performers_list": top_performers,
    }


def show_insights(students):
    """Print structured academic insights to the terminal console."""
    print("\n" + "=" * 50)
    print("        ACADEMIC PERFORMANCE INSIGHTS")
    print("=" * 50)

    if not students:
        print("  [Notice] No student records available to analyze.")
        print("=" * 50)
        return

    data = get_insights(students)
    top = data["top_performer"]
    struggling = data["struggling_students"]

    print("  🏆 TOP PERFORMER:")
    if top:
        grade = calculate_grade(top["marks"])
        print(f"     Name    : {top['name'].title()}")
        print(f"     Roll No : {top['roll_no']}")
        print(f"     Course  : {top['course']}")
        print(f"     Marks   : {top['marks']} ({grade})")

    print(f"\n  📊 CLASS AVERAGE: {data['average']:.2f} marks")

    print("\n  ⚠️ STUDENTS NEEDING ACADEMIC SUPPORT (< 40 marks):")
    if struggling:
        for s in struggling:
            print(f"     • Roll {s['roll_no']}: {s['name'].title()} - {s['marks']} marks (Course: {s['course']})")
    else:
        print("     ✓ Excellent! All students are currently meeting the passing standard.")

    print("=" * 50)
# =====================================================================
# insights.py
# This file finds the top student and students who need help.
# =====================================================================

from grade_calculator import calculate_grade


def get_insights(students):
    """
    Finds:
    1. The top performing student (highest marks).
    2. The class average.
    3. The list of students who scored below 40 (need support).
    """
    if not students:
        return {
            "top_performer": None,
            "average": 0.0,
            "struggling_students": []
        }

    # Step 1: Find the top student
    top_student = students[0]
    for s in students:
        if float(s["marks"]) > float(top_student["marks"]):
            top_student = s

    # Step 2: Calculate class average
    total_marks = 0
    for s in students:
        total_marks = total_marks + float(s["marks"])
    average = round(total_marks / len(students), 2)

    # Step 3: Find students who failed (marks less than 40)
    struggling = []
    for s in students:
        if float(s["marks"]) < 40:
            struggling.append(s)

    return {
        "top_performer": top_student,
        "average": average,
        "struggling_students": struggling
    }


def show_insights(students):
    """
    Prints the insights to the terminal console.
    """
    print("\n==========================================")
    print("      ACADEMIC PERFORMANCE INSIGHTS")
    print("==========================================")

    if not students:
        print("No student records available.")
        return

    data = get_insights(students)
    top = data["top_performer"]
    struggling = data["struggling_students"]

    # Show top student
    print("\nTop Performer:")
    if top:
        grade = calculate_grade(top["marks"])
        print("  Name :", top["name"])
        print("  Marks:", top["marks"], f"({grade})")
        print("  Roll :", top["roll_no"])

    print("\nClass Average:", data["average"])

    # Show students needing help
    print("\nStudents Needing Academic Support (< 40 marks):")
    if not struggling:
        print("  Great! All students are currently passing.")
    else:
        for s in struggling:
            print("  -", s["name"], f"({s['marks']} marks)")

    print("==========================================")
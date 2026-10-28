"""
student_actions.py - Search and Update Utilities for Student Records (CLI).
Allows searching student details and modifying marks with automatic re-grading.
"""

from storage import save_students
from grade_calculator import calculate_grade, get_grade_remark


def search_student(students):
    """Search for a student by roll number and display comprehensive information."""
    print("\n" + "-" * 35)
    print("        Search Student")
    print("-" * 35)

    roll_no = input("Enter Roll Number to search: ").strip()
    if not roll_no:
        print("[Error] Please enter a valid roll number.")
        return

    for s in students:
        if s.get("roll_no") == roll_no:
            marks = s.get("marks", 0)
            grade = calculate_grade(marks)
            remark = get_grade_remark(grade)

            print("\n[Found Student Record]")
            print(f"  • Roll Number : {s['roll_no']}")
            print(f"  • Full Name   : {s['name']}")
            print(f"  • Age         : {s.get('age', 'N/A')}")
            print(f"  • Course      : {s.get('course', 'N/A')}")
            print(f"  • Marks       : {marks}")
            print(f"  • Grade       : {grade} ({remark})")
            return

    print(f"[Notice] No student found with Roll Number '{roll_no}'.")


def update_marks(students):
    """Locate student by roll number and update their marks."""
    print("\n" + "-" * 35)
    print("        Update Student Marks")
    print("-" * 35)

    roll_no = input("Enter Roll Number to update: ").strip()
    if not roll_no:
        print("[Error] Please enter a valid roll number.")
        return

    for s in students:
        if s.get("roll_no") == roll_no:
            print(f"Current details: {s['name']} | Current Marks: {s['marks']} ({calculate_grade(s['marks'])})")
            try:
                new_marks = float(input("Enter New Marks (0 to 100): ").strip())
                if new_marks < 0 or new_marks > 100:
                    print("[Error] Marks must be between 0 and 100.")
                    return

                old_marks = s["marks"]
                s["marks"] = round(new_marks, 2)
                if save_students(students):
                    new_grade = calculate_grade(new_marks)
                    print(f"[Success] Marks updated from {old_marks} -> {new_marks} (New Grade: {new_grade})")
                return

            except ValueError:
                print("[Error] Marks must be a valid numeric value.")
                return

    print(f"[Notice] Student with Roll Number '{roll_no}' not found.")
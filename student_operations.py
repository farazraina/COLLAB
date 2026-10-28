"""
student_operations.py - Core CRUD Operations for Students (CLI).
Provides user prompts for adding and listing student records.
"""

from storage import save_students
from grade_calculator import calculate_grade


def add_student(students):
    """
    Prompt the user to add a new student with validation.
    Checks for unique roll numbers and validates numeric boundaries.
    """
    print("\n" + "-" * 35)
    print("        Register New Student")
    print("-" * 35)

    roll_no = input("Enter Roll Number       : ").strip()
    if not roll_no:
        print("[Error] Roll number cannot be empty.")
        return

    # Check for duplicate roll number
    if any(s.get("roll_no") == roll_no for s in students):
        print(f"[Error] Student with Roll Number '{roll_no}' already exists.")
        return

    name = input("Enter Full Name         : ").strip()
    if not name:
        print("[Error] Name cannot be empty.")
        return

    # Validate age
    try:
        age = int(input("Enter Age (e.g. 18-99)  : ").strip())
        if age <= 0 or age > 120:
            print("[Error] Please enter a realistic age (1-120).")
            return
    except ValueError:
        print("[Error] Age must be an integer.")
        return

    course = input("Enter Course / Stream   : ").strip()
    if not course:
        print("[Error] Course name cannot be empty.")
        return

    # Validate marks
    try:
        marks = float(input("Enter Marks (0 to 100)  : ").strip())
        if marks < 0 or marks > 100:
            print("[Error] Marks must be between 0 and 100.")
            return
    except ValueError:
        print("[Error] Marks must be a valid number.")
        return

    # Construct student record
    student = {
        "roll_no": roll_no,
        "name": name,
        "age": age,
        "course": course,
        "marks": round(marks, 2),
    }

    students.append(student)
    if save_students(students):
        print(f"\n[Success] Student '{name}' registered successfully with Grade {calculate_grade(marks)}!")


def display_students(students):
    """Display all registered students in a formatted tabular view."""
    print("\n" + "=" * 65)
    print("                    STUDENT DIRECTORY")
    print("=" * 65)

    if not students:
        print("  [Notice] No student records available.")
        print("=" * 65)
        return

    # Header
    print(f"{'Roll No':<10} {'Name':<22} {'Age':<6} {'Course':<15} {'Marks':<8} {'Grade'}")
    print("-" * 65)

    for s in students:
        marks = s.get("marks", 0)
        grade = calculate_grade(marks)
        print(f"{s.get('roll_no', 'N/A'):<10} {s.get('name', 'N/A'):<22} {s.get('age', 'N/A'):<6} "
              f"{s.get('course', 'N/A'):<15} {marks:<8.2f} {grade}")

    print("=" * 65)
    print(f"Total Records: {len(students)}")
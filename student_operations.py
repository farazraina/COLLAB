# =====================================================================
# student_operations.py
# This file handles adding a student and displaying all students.
# =====================================================================

from storage import save_students
from grade_calculator import calculate_grade


def add_student(students):
    """
    Asks the user for student details, validates them,
    and adds the new student to the list.
    """
    print("\n--- Add New Student ---")

    # 1. Roll Number
    roll_no = input("Enter roll number: ").strip()
    if not roll_no:
        print("Error: Roll number cannot be empty.")
        return

    # Check if roll number already exists
    for s in students:
        if s["roll_no"] == roll_no:
            print("Error: This roll number is already used.")
            return

    # 2. Student Name
    name = input("Enter student name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return

    # 3. Student Age
    try:
        age = int(input("Enter age: ").strip())
        if age <= 0 or age > 120:
            print("Error: Please enter a valid age between 1 and 120.")
            return
    except ValueError:
        print("Error: Age must be a number.")
        return

    # 4. Course
    course = input("Enter course name: ").strip()
    if not course:
        print("Error: Course cannot be empty.")
        return

    # 5. Marks
    try:
        marks = float(input("Enter marks (0-100): ").strip())
        if marks < 0 or marks > 100:
            print("Error: Marks must be between 0 and 100.")
            return
    except ValueError:
        print("Error: Marks must be a number.")
        return

    # Create the student dictionary
    new_student = {
        "roll_no": roll_no,
        "name": name,
        "age": age,
        "course": course,
        "marks": round(marks, 2)
    }

    # Add to list and save
    students.append(new_student)
    save_students(students)

    grade = calculate_grade(marks)
    print(f"Success: Student '{name}' was added with Grade {grade}!")


def display_students(students):
    """
    Prints a neat table of all students in the terminal.
    """
    print("\n------------------- STUDENT RECORDS -------------------")

    if not students:
        print("No student records found.")
        return

    print(f"{'Roll No':<10} {'Name':<20} {'Age':<6} {'Course':<15} {'Marks':<8} {'Grade'}")
    print("-" * 65)

    for s in students:
        grade = calculate_grade(s["marks"])
        print(f"{s['roll_no']:<10} {s['name']:<20} {s['age']:<6} {s['course']:<15} {s['marks']:<8} {grade}")

    print("-" * 65)
    print(f"Total students: {len(students)}")
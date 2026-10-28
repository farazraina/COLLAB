# =====================================================================
# student_actions.py
# This file handles searching for a student and updating student marks.
# =====================================================================

from storage import save_students
from grade_calculator import calculate_grade, get_grade_remark


def search_student(students):
    """
    Asks for a roll number and displays that student's details.
    """
    print("\n--- Search Student ---")
    roll_no = input("Enter roll number to search: ").strip()

    if not roll_no:
        print("Error: Please enter a roll number.")
        return

    # Loop through the list to find the matching roll number
    for s in students:
        if s["roll_no"] == roll_no:
            grade = calculate_grade(s["marks"])
            remark = get_grade_remark(grade)

            print("\nStudent Found:")
            print("  Roll Number :", s["roll_no"])
            print("  Name        :", s["name"])
            print("  Age         :", s["age"])
            print("  Course      :", s["course"])
            print("  Marks       :", s["marks"])
            print("  Grade       :", grade, f"({remark})")
            return

    # If loop finishes without returning, student wasn't found
    print("Notice: No student found with roll number", roll_no)


def update_marks(students):
    """
    Finds a student by roll number and updates their marks.
    """
    print("\n--- Update Student Marks ---")
    roll_no = input("Enter roll number to update: ").strip()

    if not roll_no:
        print("Error: Please enter a roll number.")
        return

    for s in students:
        if s["roll_no"] == roll_no:
            print(f"Current Marks for {s['name']}: {s['marks']}")

            try:
                new_marks = float(input("Enter new marks (0-100): ").strip())
                if new_marks < 0 or new_marks > 100:
                    print("Error: Marks must be between 0 and 100.")
                    return

                # Update marks and save
                s["marks"] = round(new_marks, 2)
                save_students(students)

                new_grade = calculate_grade(new_marks)
                print(f"Success: Marks updated to {new_marks} (New Grade: {new_grade})")
                return

            except ValueError:
                print("Error: Marks must be a number.")
                return

    print("Notice: No student found with roll number", roll_no)
"""
main.py - Main Console Application for Student Management System.
Provides a clean, interactive menu-driven interface in the terminal.
"""

from storage import load_students
from student_operations import add_student, display_students
from student_actions import search_student, update_marks
from analytics import show_dashboard
from insights import show_insights


def main():
    """Terminal application loop for the Student Management System."""
    students = load_students()

    while True:
        print("\n" + "=" * 45)
        print("     STUDENT MANAGEMENT SYSTEM (CLI)")
        print("=" * 45)
        print("  [1] Add New Student")
        print("  [2] View All Students")
        print("  [3] Search Student by Roll No")
        print("  [4] Update Student Marks")
        print("  [5] Class Performance Dashboard")
        print("  [6] Academic Performance Insights")
        print("  [7] Exit Program")
        print("=" * 45)

        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_marks(students)
        elif choice == "5":
            show_dashboard(students)
        elif choice == "6":
            show_insights(students)
        elif choice == "7":
            print("\nThank you for using the Student Management System. Goodbye!\n")
            break
        else:
            print("[Warning] Invalid selection. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
# =====================================================================
# main.py
# Main menu for the Student Management System (Terminal / Console).
# =====================================================================

from storage import load_students
from student_operations import add_student, display_students
from student_actions import search_student, update_marks
from analytics import show_dashboard
from insights import show_insights


def main():
    # Load existing students from the JSON file
    students = load_students()

    while True:
        print("\n==========================================")
        print("     STUDENT MANAGEMENT SYSTEM (CLI)")
        print("==========================================")
        print("1. Add New Student")
        print("2. Display All Students")
        print("3. Search Student by Roll Number")
        print("4. Update Student Marks")
        print("5. Class Performance Dashboard")
        print("6. Academic Performance Insights")
        print("7. Exit")
        print("==========================================")

        choice = input("Enter your choice (1-7): ").strip()

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
            print("\nGoodbye! Program closed successfully.\n")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
from storage import load_students
from student_operations import add_student, display_students
from student_actions import search_student, update_marks
from analytics import show_dashboard
from insights import show_insights
from grade_calculator import calculate_grade


students = load_students()

while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. Display Students")
    print("3. Search Student")
    print("4. Update Marks")
    print("5. Class Performance Dashboard")
    print("6. Academic Performance Insights")
    print("7. Exit")

    choice = input("Enter choice: ").strip()

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
        print("Program closed.")
        break

    else:
        print("Invalid choice. Please select 1-7.")
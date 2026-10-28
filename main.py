# =====================================================================
# main.py
# Main menu for the Student Academic Analysis System (Terminal / CLI).
# =====================================================================

from storage import load_students
from student_operations import add_student, display_students
from student_actions import search_student, update_marks
from analytics import show_dashboard
from insights import show_insights
from study_planner import generate_study_profile


def show_study_assistant_cli(students):
    """
    CLI view for the AI-driven study recommendations and adaptive weekly planner.
    """
    print("\n--- AI Personalized Study Assistant ---")
    roll_no = input("Enter student roll number: ").strip()
    if not roll_no:
        print("Error: Roll number is required.")
        return

    found = None
    for s in students:
        if str(s.get("roll_no", "")).strip() == roll_no:
            found = s
            break

    if not found:
        print(f"Notice: No student found with roll number '{roll_no}'.")
        return

    profile = generate_study_profile(found)
    print("\n" + "=" * 65)
    print(f"    AI STUDY PROFILE & ADAPTIVE PLAN: {found['name'].title()} (Roll {found['roll_no']})")
    print("=" * 65)
    print(f"  Recommended Weekly Study Load: {profile['total_weekly_hours']:.1f} hours/week")
    print(f"  Top Academic Strength        : {profile['top_strength']['subject']} ({profile['top_strength']['marks']:.1f}%)")
    print(f"  Priority Focus Area          : {profile['top_weakness']['subject']} ({profile['top_weakness']['marks']:.1f}%)")
    print("-" * 65)

    print("\nSUBJECT-WISE PRIORITY BREAKDOWN:")
    for item in profile["sorted_by_priority"]:
        print(f"\n  [{item['priority'].upper()}] {item['subject']}")
        print(f"    • Score      : {item['marks']:.1f}% (Grade {item['grade']})")
        print(f"    • Allocation : {item['weekly_hours']}")
        print(f"    • Strategy   : {item['strategy']}")
        print(f"    • Focus Area : {item['recommendation']}")

    print("\n" + "-" * 65)
    print("ADAPTIVE 7-DAY STUDY TIMETABLE (MON - SUN):")
    print("-" * 65)
    for day_plan in profile["weekly_schedule"]:
        print(f"  {day_plan['day']:<10} | {day_plan['session_time']:<22} | Focus: {day_plan['primary_subject']}")
        print(f"             Objective: {day_plan['task_objective']}")
    print("=" * 65)


def main():
    # Load existing students from the JSON file
    students = load_students()

    while True:
        print("\n==========================================")
        print("  STUDENT ACADEMIC ANALYSIS SYSTEM (CLI)")
        print("==========================================")
        print("1. Add New Student (5 Subjects)")
        print("2. Display All Students")
        print("3. Search Student by Roll Number")
        print("4. Update Student Subject Marks")
        print("5. Class Performance Dashboard")
        print("6. Academic Performance Insights")
        print("7. AI Study Assistant & Weekly Schedule")
        print("8. Exit")
        print("==========================================")

        choice = input("Enter your choice (1-8): ").strip()

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
            show_study_assistant_cli(students)
        elif choice == "8":
            print("\nGoodbye! Program closed successfully.\n")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()

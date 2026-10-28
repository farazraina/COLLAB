# =====================================================================
# student_actions.py
# Terminal operations for searching student profile cards and updating
# multi-subject scores.
# =====================================================================

from storage import save_students
from grade_calculator import DEFAULT_SUBJECTS, calculate_student_stats


def search_student(students):
    """
    Looks up a student by Roll Number and displays their detailed report card.
    """
    print("\n--- Search Student ---")
    roll_no = input("Enter roll number to search: ").strip()

    if not roll_no:
        print("Error: Please enter a roll number.")
        return

    found = None
    for s in students:
        if str(s["roll_no"]).strip() == roll_no:
            found = s
            break

    if not found:
        print(f"Notice: No student found with roll number '{roll_no}'.")
        return

    subjs = found.get("subjects", {})
    tot = found.get("total_marks", 0.0)
    pct = found.get("percentage", 0.0)
    grade = found.get("grade", "N/A")
    cgpa = found.get("cgpa", 0.0)
    remark = found.get("remark", "")
    status = found.get("status", "N/A")

    print("\n" + "=" * 48)
    print(f"       STUDENT REPORT CARD: {found['name'].title()}")
    print("=" * 48)
    print(f"  Roll Number  : {found['roll_no']}")
    print(f"  Name         : {found['name'].title()}")
    print(f"  Age          : {found['age']}")
    print(f"  Course       : {found['course']}")
    print("-" * 48)
    print("  Subject Scores (Out of 100):")
    for subj in DEFAULT_SUBJECTS:
        score = subjs.get(subj, 0.0)
        print(f"    • {subj:<24}: {score:>5.1f}")
    print("-" * 48)
    print(f"  Total Score  : {tot:.1f} / 500.0")
    print(f"  Percentage   : {pct:.2f}%")
    print(f"  Final Grade  : {grade} ({remark})")
    print(f"  CGPA (10.0)  : {cgpa:.2f}")
    print(f"  Status       : {status}")
    print("=" * 48)


def update_marks(students):
    """
    Finds a student by Roll Number and allows modifying marks for each subject.
    """
    print("\n--- Update Student Marks ---")
    roll_no = input("Enter roll number to update: ").strip()

    if not roll_no:
        print("Error: Please enter a roll number.")
        return

    found = None
    for s in students:
        if str(s["roll_no"]).strip() == roll_no:
            found = s
            break

    if not found:
        print(f"Notice: No student found with roll number '{roll_no}'.")
        return

    subjs = found.get("subjects", {})
    print(f"\nCurrent Marks for {found['name'].title()} (Roll {found['roll_no']}):")
    for subj in DEFAULT_SUBJECTS:
        print(f"  • {subj}: {subjs.get(subj, 0.0)}")

    print("\nEnter new marks for each subject (press Enter to keep current value):")
    updated_subjs = dict(subjs)

    for subj in DEFAULT_SUBJECTS:
        curr = subjs.get(subj, 0.0)
        val_str = input(f"  {subj} [Current: {curr}]: ").strip()
        if val_str:
            try:
                val = float(val_str)
                if 0.0 <= val <= 100.0:
                    updated_subjs[subj] = round(val, 2)
                else:
                    print(f"    Out of range (0-100). Keeping current value ({curr}).")
            except ValueError:
                print(f"    Invalid number. Keeping current value ({curr}).")

    # Recalculate stats
    stats = calculate_student_stats(updated_subjs)
    found["subjects"] = updated_subjs
    found["total_marks"] = stats["total_marks"]
    found["max_marks"] = stats["max_marks"]
    found["percentage"] = stats["percentage"]
    found["marks"] = stats["percentage"]
    found["grade"] = stats["grade"]
    found["cgpa"] = stats["cgpa"]
    found["remark"] = stats["remark"]
    found["status"] = stats["status"]

    save_students(students)

    print("\nSuccess: Student record updated!")
    print(f"New Percentage: {stats['percentage']}% | Grade: {stats['grade']} | CGPA: {stats['cgpa']}")

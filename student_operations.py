# =====================================================================
# student_operations.py
# Terminal operations for registering new students with multi-subject marks
# and displaying complete student records.
# =====================================================================

from storage import save_students
from grade_calculator import DEFAULT_SUBJECTS, calculate_student_stats


def add_student(students):
    """
    Prompts user for student profile details and marks for all 5 subjects,
    validates inputs, calculates aggregate metrics, and saves the record.
    """
    print("\n--- Add New Student ---")

    # 1. Roll Number
    roll_no = input("Enter roll number: ").strip()
    if not roll_no:
        print("Error: Roll number cannot be empty.")
        return

    # Check uniqueness
    for s in students:
        if str(s["roll_no"]).strip() == roll_no:
            print(f"Error: Roll number '{roll_no}' is already registered.")
            return

    # 2. Student Name
    name = input("Enter student name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return

    # 3. Student Age
    try:
        age = int(input("Enter age (1-120): ").strip())
        if age <= 0 or age > 120:
            print("Error: Please enter a valid age between 1 and 120.")
            return
    except ValueError:
        print("Error: Age must be a whole number.")
        return

    # 4. Course
    course = input("Enter course name: ").strip()
    if not course:
        print("Error: Course cannot be empty.")
        return

    # 5. Multi-Subject Marks (out of 100)
    print("\nEnter Marks for each Subject (0 - 100):")
    subjects = {}
    for subj in DEFAULT_SUBJECTS:
        while True:
            try:
                val = float(input(f"  • {subj}: ").strip())
                if 0.0 <= val <= 100.0:
                    subjects[subj] = round(val, 2)
                    break
                else:
                    print("    Invalid range! Marks must be between 0 and 100.")
            except ValueError:
                print("    Invalid input! Please enter a numerical score.")

    # Calculate aggregate metrics
    stats = calculate_student_stats(subjects)

    new_student = {
        "roll_no": roll_no,
        "name": name,
        "age": age,
        "course": course,
        "subjects": subjects,
        "total_marks": stats["total_marks"],
        "max_marks": stats["max_marks"],
        "percentage": stats["percentage"],
        "marks": stats["percentage"],
        "grade": stats["grade"],
        "cgpa": stats["cgpa"],
        "remark": stats["remark"],
        "status": stats["status"]
    }

    students.append(new_student)
    save_students(students)

    print(f"\nSuccess: Student '{name}' was added successfully!")
    print(f"Total: {stats['total_marks']}/{stats['max_marks']} | Percentage: {stats['percentage']}% | Grade: {stats['grade']} | CGPA: {stats['cgpa']}")


def display_students(students):
    """
    Displays a formatted table of all student records in the terminal.
    """
    print("\n------------------------- STUDENT RECORDS -------------------------")

    if not students:
        print("No student records found.")
        return

    header = f"{'Roll No':<8} {'Name':<18} {'Course':<10} {'Math':<6} {'Python':<7} {'Prof':<6} {'DBMS':<6} {'DSD':<6} {'Total':<7} {'%':<6} {'Grade':<6} {'CGPA'}"
    print(header)
    print("-" * 96)

    for s in students:
        subjs = s.get("subjects", {})
        m_math = subjs.get("Mathematics", 0.0)
        m_py   = subjs.get("Python Programming", 0.0)
        m_prof = subjs.get("Professional Skills", 0.0)
        m_db   = subjs.get("Database Management", 0.0)
        m_dsd  = subjs.get("DSD", 0.0)

        tot  = s.get("total_marks", 0.0)
        pct  = s.get("percentage", 0.0)
        grd  = s.get("grade", "N/A")
        cgpa = s.get("cgpa", 0.0)

        print(
            f"{s['roll_no']:<8} {s['name'][:17].title():<18} {s['course'][:9]:<10} "
            f"{m_math:<6.0f} {m_py:<7.0f} {m_prof:<6.0f} {m_db:<6.0f} {m_dsd:<6.0f} "
            f"{tot:<7.0f} {pct:<6.1f} {grd:<6} {cgpa:.2f}"
        )

    print("-" * 96)
    print(f"Total registered students: {len(students)}")

def show_dashboard(students):
    print("\n===== CLASS PERFORMANCE DASHBOARD =====")

    if not students:
        print("No student records available.")
        return

    marks_list = [student["marks"] for student in students]

    total_students = len(students)
    average = sum(marks_list) / total_students
    highest = max(marks_list)
    lowest = min(marks_list)

    passed = sum(1 for marks in marks_list if marks >= 40)
    failed = total_students - passed

    pass_percentage = (passed / total_students) * 100

    print("Total Students:", total_students)
    print("Class Average:", round(average, 2))
    print("Highest Marks:", highest)
    print("Lowest Marks:", lowest)
    print("Students Passed:", passed)
    print("Students Failed:", failed)
    print("Pass Percentage:", round(pass_percentage, 2), "%")
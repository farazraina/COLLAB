def show_insights(students):

    print("\n===== ACADEMIC PERFORMANCE INSIGHTS =====")

    if not students:
        print("No student records available.")
        return

    top_student = max(students, key=lambda student: student["marks"])

    print(
        "Top Performer:",
        top_student["name"],
        "-",
        top_student["marks"],
        "marks"
    )

    print("\nStudents needing academic support:")

    found = False

    for student in students:
        if student["marks"] < 40:
            print(student["name"], "-", student["marks"], "marks")
            found = True

    if not found:
        print("No students currently below the passing threshold.")

    average = sum(student["marks"] for student in students) / len(students)

    print("\nClass Average:", round(average, 2))
from storage import save_students


def search_student(students):
    print("\n--- Search Student ---")

    roll_no = input("Enter roll number to search: ").strip()

    for student in students:
        if student["roll_no"] == roll_no:
            print("\nStudent Found!")
            print("Name:", student["name"])
            print("Age:", student["age"])
            print("Course:", student["course"])
            print("Marks:", student["marks"])
            return

    print("Student not found.")


def update_student(students):
    print("\n--- Update Student ---")

    roll_no = input("Enter roll number to update: ").strip()

    for student in students:
        if student["roll_no"] == roll_no:
            print("Leave a field blank to keep its current value.")

            name = input("Enter new name: ").strip()
            age = input("Enter new age: ").strip()
            course = input("Enter new course: ").strip()
            marks = input("Enter new marks: ").strip()

            if name:
                student["name"] = name

            if age:
                try:
                    new_age = int(age)

                    if new_age <= 0:
                        print("Age must be positive.")
                        return

                    student["age"] = new_age

                except ValueError:
                    print("Invalid age.")
                    return

            if course:
                student["course"] = course

            if marks:
                try:
                    new_marks = float(marks)

                    if not 0 <= new_marks <= 100:
                        print("Marks must be between 0 and 100.")
                        return

                    student["marks"] = new_marks

                except ValueError:
                    print("Invalid marks.")
                    return

            save_students(students)

            print("Student updated successfully!")
            return

    print("Student not found.")


def delete_student(students):
    print("\n--- Delete Student ---")

    roll_no = input("Enter roll number to delete: ").strip()

    for student in students:
        if student["roll_no"] == roll_no:
            confirm = input(
                "Are you sure you want to delete this student? (y/n): "
            ).strip().lower()

            if confirm == "y":
                students.remove(student)
                save_students(students)
                print("Student deleted successfully!")
            else:
                print("Deletion cancelled.")

            return

    print("Student not found.")
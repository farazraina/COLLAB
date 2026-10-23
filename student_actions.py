from storage import save_students


def search_student(students):
    roll_no = input("Enter roll number: ").strip()

    for student in students:
        if student["roll_no"] == roll_no:
            print("\nStudent found!")
            print("Name:", student["name"])
            print("Course:", student["course"])
            print("Marks:", student["marks"])
            return

    print("Student not found.")


def update_marks(students):
    roll_no = input("Enter roll number: ").strip()

    for student in students:
        if student["roll_no"] == roll_no:

            try:
                marks = float(input("Enter new marks: "))

                if marks < 0 or marks > 100:
                    print("Marks must be between 0 and 100.")
                    return

                student["marks"] = marks
                save_students(students)

                print("Marks updated successfully!")
                return

            except ValueError:
                print("Please enter valid marks.")
                return

    print("Student not found.")
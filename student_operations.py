from storage import save_students


def add_student(students):
    print("\n--- Add Student ---")

    roll_no = input("Enter roll number: ").strip()

    if not roll_no:
        print("Roll number cannot be empty.")
        return

    for student in students:
        if student["roll_no"] == roll_no:
            print("This roll number already exists.")
            return

    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    try:
        age = int(input("Enter age: "))
        marks = float(input("Enter marks: "))

        if age <= 0:
            print("Age must be greater than zero.")
            return

        if marks < 0 or marks > 100:
            print("Marks must be between 0 and 100.")
            return

    except ValueError:
        print("Please enter valid numbers.")
        return

    course = input("Enter course: ").strip()

    if not course:
        print("Course cannot be empty.")
        return

    student = {
        "roll_no": roll_no,
        "name": name,
        "age": age,
        "course": course,
        "marks": marks
    }

    students.append(student)
    save_students(students)

    print("Student added successfully!")


def display_students(students):
    print("\n--- Student Records ---")

    if not students:
        print("No student records available.")
        return

    for student in students:
        print("----------------------")
        print("Roll Number:", student["roll_no"])
        print("Name:", student["name"])
        print("Age:", student["age"])
        print("Course:", student["course"])
        print("Marks:", student["marks"])
from storage import save_students


def add_student(students):
    print("\n--- Add Student ---")

    roll_no = input("Enter roll number: ").strip()

    # Check whether the roll number already exists
    for student in students:
        if student["roll_no"] == roll_no:
            print("Roll number already exists!")
            return

    name = input("Enter student name: ").strip()

    try:
        age = int(input("Enter age: "))
        marks = float(input("Enter marks: "))

        if age <= 0 or not 0 <= marks <= 100:
            print("Invalid age or marks.")
            return

    except ValueError:
        print("Please enter valid numbers for age and marks.")
        return

    course = input("Enter course: ").strip()

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
    print("\n--- All Students ---")

    if not students:
        print("No student records found.")
        return

    for student in students:
        print("-------------------------")
        print("Roll Number:", student["roll_no"])
        print("Name:", student["name"])
        print("Age:", student["age"])
        print("Course:", student["course"])
        print("Marks:", student["marks"])
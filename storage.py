import json
import os

FILE_NAME = "students.json"


def load_students():
    if not os.path.exists(FILE_NAME):
        save_students([])
        return []

    try:
        with open(FILE_NAME, "r") as file:
            students = json.load(file)

        if isinstance(students, list):
            return students

        print("Student file has an invalid format.")
        return []

    except json.JSONDecodeError:
        print("Student file is damaged or contains invalid JSON.")
        return []


def save_students(students):
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)
# =====================================================================
# storage.py
# This file saves student data to a JSON file and loads it back.
# JSON is a simple text format used to store lists and dictionaries.
# =====================================================================

import json
import os

FILE_NAME = "students.json"


def load_students():
    """
    Loads the list of students from 'students.json'.
    If the file does not exist, it creates a new empty file.
    Returns: a list of student dictionaries.
    """
    # Step 1: If the file doesn't exist yet, create it with an empty list []
    if not os.path.exists(FILE_NAME):
        save_students([])
        return []

    # Step 2: Read the JSON file
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            students = json.load(file)

        # Make sure the data is actually a list
        if isinstance(students, list):
            return students
        else:
            return []

    except json.JSONDecodeError:
        print("Warning: The students.json file is empty or corrupted. Starting fresh.")
        return []


def save_students(students):
    """
    Saves the list of students into 'students.json'.
    """
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            # indent=4 makes the JSON file neat and easy to read
            json.dump(students, file, indent=4)
        return True
    except Exception as error:
        print("Error saving student data:", error)
        return False
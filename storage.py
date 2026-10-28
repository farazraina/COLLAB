"""
storage.py - Data Persistence Module for Student Management System.
Handles loading and saving student records to 'students.json'.
"""

import json
import os

FILE_NAME = "students.json"


def load_students():
    """
    Load student records from the JSON file.
    If the file does not exist, an empty file is created.
    Returns a list of student dictionaries.
    """
    if not os.path.exists(FILE_NAME):
        save_students([])
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            # Validate essential fields for each record
            valid_students = []
            for item in data:
                if isinstance(item, dict) and "roll_no" in item and "name" in item:
                    valid_students.append(item)
            return valid_students

        print("[Warning] Student data file contains invalid structure. Resetting to empty list.")
        return []

    except (json.JSONDecodeError, OSError) as err:
        print(f"[Error] Failed to read '{FILE_NAME}': {err}")
        return []


def save_students(students):
    """
    Save the list of student dictionaries to 'students.json'.
    Ensures safe formatting and UTF-8 encoding.
    """
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
        return True
    except OSError as err:
        print(f"[Error] Failed to write to '{FILE_NAME}': {err}")
        return False
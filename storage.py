# =====================================================================
# storage.py
# Handles saving and loading student records to/from 'students.json'.
# Implements automatic schema normalization and legacy migration
# for multi-subject performance records.
# =====================================================================

import json
import os
from grade_calculator import DEFAULT_SUBJECTS, calculate_student_stats

FILE_NAME = "students.json"


def normalize_student(student):
    """
    Ensures that a student record contains all required fields, including
    the multi-subject dictionary, total marks, percentage, grade, CGPA,
    and legacy 'marks' field for backward compatibility.
    """
    if not isinstance(student, dict):
        return None

    roll_no = str(student.get("roll_no", "")).strip()
    name = str(student.get("name", "")).strip()
    course = str(student.get("course", "General")).strip()

    try:
        age = int(student.get("age", 20))
    except (ValueError, TypeError):
        age = 20

    # Retrieve or initialize subjects
    raw_subjects = student.get("subjects")
    subjects = {}

    if isinstance(raw_subjects, dict):
        for subj in DEFAULT_SUBJECTS:
            try:
                subjects[subj] = round(float(raw_subjects.get(subj, 0.0)), 2)
            except (ValueError, TypeError):
                subjects[subj] = 0.0
    else:
        # Legacy migration: fallback to single 'marks' if subjects not defined
        try:
            legacy_mark = float(student.get("marks", 60.0))
        except (ValueError, TypeError):
            legacy_mark = 60.0

        for subj in DEFAULT_SUBJECTS:
            subjects[subj] = round(legacy_mark, 2)

    # Compute aggregate stats
    stats = calculate_student_stats(subjects)

    normalized = {
        "roll_no": roll_no,
        "name": name,
        "age": age,
        "course": course,
        "subjects": subjects,
        "total_marks": stats["total_marks"],
        "max_marks": stats["max_marks"],
        "percentage": stats["percentage"],
        "marks": stats["percentage"],  # Kept for backward compatibility
        "grade": stats["grade"],
        "cgpa": stats["cgpa"],
        "remark": stats["remark"],
        "status": stats["status"]
    }
    return normalized


def load_students():
    """
    Loads student records from 'students.json'.
    Normalizes every record to ensure schema consistency.
    """
    if not os.path.exists(FILE_NAME):
        save_students([])
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        if not isinstance(raw_data, list):
            return []

        normalized_list = []
        for item in raw_data:
            rec = normalize_student(item)
            if rec:
                normalized_list.append(rec)

        return normalized_list

    except json.JSONDecodeError:
        print("Warning: The students.json file is empty or corrupted. Starting fresh.")
        return []
    except Exception as error:
        print("Error reading student data:", error)
        return []


def save_students(students):
    """
    Saves the list of normalized student records into 'students.json'.
    """
    try:
        normalized_list = []
        for s in students:
            rec = normalize_student(s)
            if rec:
                normalized_list.append(rec)

        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(normalized_list, file, indent=4)
        return True
    except Exception as error:
        print("Error saving student data:", error)
        return False

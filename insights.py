# =====================================================================
# insights.py
# Computes key academic insights:
# - Cohort Top Performer & Honor Roll
# - Subject-wise Top Scorers
# - Class Difficulty Benchmarks (Toughest vs Easiest Subjects)
# - Academic Support / Remedial intervention lists
# =====================================================================

from grade_calculator import DEFAULT_SUBJECTS, calculate_grade


def get_insights(students):
    """
    Analyzes student records to extract high-yield academic insights.
    """
    if not students:
        return {
            "top_performer": None,
            "average": 0.0,
            "struggling_students": [],
            "subject_toppers": {},
            "toughest_subject": None,
            "strongest_subject": None
        }

    # 1. Overall Top Performer
    top_student = max(students, key=lambda s: float(s.get("percentage", s.get("marks", 0.0))))

    # 2. Overall Class Average
    total_pct = sum(float(s.get("percentage", s.get("marks", 0.0))) for s in students)
    average = round(total_pct / len(students), 2)

    # 3. Students Needing Academic Support
    # Flagged if overall percentage < 40 or if failing any individual subject (< 40)
    struggling = []
    for s in students:
        pct = float(s.get("percentage", s.get("marks", 0.0)))
        subjs = s.get("subjects", {})
        failed_subjs = [name for name, score in subjs.items() if float(score) < 40.0]

        if pct < 40.0 or failed_subjs:
            struggling.append({
                "student": s,
                "percentage": pct,
                "failed_subjects": failed_subjs
            })

    # 4. Subject-wise Top Scorers
    subject_toppers = {}
    subject_averages = {}

    for subj in DEFAULT_SUBJECTS:
        best_student = None
        best_score = -1.0
        scores = []

        for s in students:
            subjs = s.get("subjects", {})
            score = float(subjs.get(subj, s.get("marks", 0.0)))
            scores.append(score)
            if score > best_score:
                best_score = score
                best_student = s

        subject_toppers[subj] = {
            "student_name": best_student["name"] if best_student else "N/A",
            "roll_no": best_student["roll_no"] if best_student else "N/A",
            "score": best_score
        }
        if scores:
            subject_averages[subj] = sum(scores) / len(scores)

    # 5. Toughest and Strongest Subjects in the class
    if subject_averages:
        toughest_name = min(subject_averages, key=subject_averages.get)
        strongest_name = max(subject_averages, key=subject_averages.get)
        toughest_subject = {"subject": toughest_name, "average": round(subject_averages[toughest_name], 2)}
        strongest_subject = {"subject": strongest_name, "average": round(subject_averages[strongest_name], 2)}
    else:
        toughest_subject = None
        strongest_subject = None

    return {
        "top_performer": top_student,
        "average": average,
        "struggling_students": struggling,
        "subject_toppers": subject_toppers,
        "toughest_subject": toughest_subject,
        "strongest_subject": strongest_subject
    }


def show_insights(students):
    """
    Prints academic insights in a structured format for the console.
    """
    print("\n==========================================")
    print("      ACADEMIC PERFORMANCE INSIGHTS")
    print("==========================================")

    if not students:
        print("No student records available.")
        return

    data = get_insights(students)
    top = data["top_performer"]
    struggling = data["struggling_students"]

    print("\nTop Performer:")
    if top:
        pct = float(top.get("percentage", top.get("marks", 0.0)))
        grade = calculate_grade(pct)
        print("  Name      :", top["name"].title())
        print("  Roll No   :", top["roll_no"])
        print("  Overall   :", f"{pct:.2f}% (Grade {grade}, CGPA: {top.get('cgpa', pct/10):.2f})")
        print("  Course    :", top.get("course", "N/A"))

    print("\nClass Mean Performance:", f"{data['average']:.2f}%")

    if data["strongest_subject"] and data["toughest_subject"]:
        print(f"  • Best Class Subject    : {data['strongest_subject']['subject']} ({data['strongest_subject']['average']}%)")
        print(f"  • Toughest Class Subject: {data['toughest_subject']['subject']} ({data['toughest_subject']['average']}%)")

    print("\nSubject Toppers:")
    for subj, info in data["subject_toppers"].items():
        print(f"  • {subj:<22}: {info['student_name'].title()} ({info['score']}/100)")

    print("\nStudents Needing Academic Support:")
    if not struggling:
        print("  ✓ Great! All students are in good standing across all subjects.")
    else:
        for item in struggling:
            s = item["student"]
            pct = item["percentage"]
            if item["failed_subjects"]:
                issues = f"Failed in: {', '.join(item['failed_subjects'])}"
            else:
                issues = "Aggregate < 40%"
            print(f"  • {s['name'].title()} (Roll {s['roll_no']}) — {pct:.1f}% [{issues}]")

    print("==========================================")

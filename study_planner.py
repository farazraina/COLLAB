# =====================================================================
# study_planner.py
# AI-Driven Study Recommendations & Adaptive Schedule Engine.
# Analyzes student marks across subjects to produce personalized
# priority rankings, remedial study strategies, and balanced weekly planners.
# =====================================================================

from grade_calculator import DEFAULT_SUBJECTS, calculate_grade


def analyze_subject_priority(subject, marks):
    """
    Categorizes a subject into High Priority, Medium Priority, or Maintenance
    based on the student's score, and provides tailored recommendations.
    """
    try:
        score = float(marks)
    except (ValueError, TypeError):
        score = 0.0

    if score < 60.0:
        return {
            "subject": subject,
            "marks": score,
            "grade": calculate_grade(score),
            "priority": "High Priority",
            "priority_level": 3,
            "badge_color": "#A21721",      # Crimson Ruby Alert
            "weekly_hours": "6 – 8 hrs/week",
            "hours_numeric": 7.0,
            "status_label": "Needs Urgent Improvement",
            "action_title": "Foundational Revision & Core Remediation",
            "recommendation": (
                "Break down core syllabus into micro-topics. Re-read standard textbook chapters, "
                "revisit tutorial recordings, and schedule doubt sessions with faculty."
            ),
            "strategy": "Daily 60–90 min structured sessions using active recall and chapter summaries.",
            "target_goal": "Aim to elevate score above 70% in upcoming unit tests."
        }
    elif score < 80.0:
        return {
            "subject": subject,
            "marks": score,
            "grade": calculate_grade(score),
            "priority": "Medium Priority",
            "priority_level": 2,
            "badge_color": "#B8621B",      # Warm Amber Focus
            "weekly_hours": "3 – 5 hrs/week",
            "hours_numeric": 4.0,
            "status_label": "Good Progress (Refinement Needed)",
            "action_title": "Targeted Problem-Solving & Mock Practice",
            "recommendation": (
                "Work through question banks and previous years' exam papers. Focus on tricky edge cases "
                "and time management during practice drills."
            ),
            "strategy": "Alternate-day 45–60 min timed quizzes and problem set reviews.",
            "target_goal": "Push performance from solid foundation to distinction (80%+)."
        }
    else:
        return {
            "subject": subject,
            "marks": score,
            "grade": calculate_grade(score),
            "priority": "Maintenance",
            "priority_level": 1,
            "badge_color": "#2A7B4C",      # Calm Emerald Green
            "weekly_hours": "1 – 2 hrs/week",
            "hours_numeric": 1.5,
            "status_label": "Mastery Achieved",
            "action_title": "Periodic Review & Advanced Applications",
            "recommendation": (
                "Maintain conceptual agility with quick weekly spaced repetition. Engage in peer tutoring, "
                "work on advanced projects, and explore competitive or honors topics."
            ),
            "strategy": "Weekly 45 min high-yield summary review and peer discussions.",
            "target_goal": "Sustain 90%+ mastery while mentoring peers."
        }


def generate_study_profile(student):
    """
    Generates a full personalized academic study profile for a student,
    including subject priorities, strengths, weaknesses, total recommended study hours,
    and an adaptive weekly timetable.
    """
    subjects = student.get("subjects", {})
    if not subjects:
        subjects = {subj: float(student.get("marks", 60.0)) for subj in DEFAULT_SUBJECTS}

    analyses = []
    for subj in DEFAULT_SUBJECTS:
        marks = subjects.get(subj, 0.0)
        analyses.append(analyze_subject_priority(subj, marks))

    # Sort by priority level (highest priority first), then by lowest marks
    sorted_analyses = sorted(analyses, key=lambda x: (-x["priority_level"], x["marks"]))

    # Identify Strengths and Weaknesses
    all_sorted_by_marks = sorted(analyses, key=lambda x: x["marks"], reverse=True)
    top_strength = all_sorted_by_marks[0]
    top_weakness = all_sorted_by_marks[-1]

    # Calculate total recommended weekly study hours
    total_weekly_hours = sum(item["hours_numeric"] for item in analyses)

    # Priority counts
    counts = {
        "High Priority": sum(1 for a in analyses if a["priority"] == "High Priority"),
        "Medium Priority": sum(1 for a in analyses if a["priority"] == "Medium Priority"),
        "Maintenance": sum(1 for a in analyses if a["priority"] == "Maintenance")
    }

    # Generate balanced weekly timetable
    timetable = generate_adaptive_weekly_schedule(analyses)

    return {
        "analyses": analyses,
        "sorted_by_priority": sorted_analyses,
        "top_strength": top_strength,
        "top_weakness": top_weakness,
        "total_weekly_hours": total_weekly_hours,
        "priority_counts": counts,
        "weekly_schedule": timetable
    }


def generate_adaptive_weekly_schedule(analyses):
    """
    Constructs an adaptive 7-day weekly study schedule (Monday - Sunday).
    Allocates high priority subjects more frequent and intensive time slots,
    medium priority subjects moderate practice, and maintenance subjects periodic drills.
    """
    # Group subjects by priority
    high_items = [a for a in analyses if a["priority"] == "High Priority"]
    med_items  = [a for a in analyses if a["priority"] == "Medium Priority"]
    maint_items = [a for a in analyses if a["priority"] == "Maintenance"]

    # Daily templates
    days = [
        {"day": "Monday",    "focus": "Core Fundamentals & Foundation", "session_time": "5:30 PM – 7:30 PM"},
        {"day": "Tuesday",   "focus": "Targeted Problem Sets & Code Drills", "session_time": "6:00 PM – 7:45 PM"},
        {"day": "Wednesday", "focus": "Remedial Topic Deep Dive", "session_time": "5:30 PM – 7:30 PM"},
        {"day": "Thursday",  "focus": "Mock Questions & Quizzes", "session_time": "6:00 PM – 7:45 PM"},
        {"day": "Friday",    "focus": "Concept Integration & Mini-Projects", "session_time": "5:00 PM – 6:45 PM"},
        {"day": "Saturday",  "focus": "Intensive Review & Doubt Resolution", "session_time": "10:00 AM – 12:30 PM"},
        {"day": "Sunday",    "focus": "Weekly Spaced Repetition & Rest", "session_time": "4:00 PM – 5:30 PM"}
    ]

    schedule = []

    # Map subjects onto the 7 days intelligently
    for i, d in enumerate(days):
        day_name = d["day"]
        day_theme = d["focus"]
        session_time = d["session_time"]

        primary_subject = None
        secondary_subject = None
        task_objective = ""

        if high_items:
            # Cycle through high items for primary slots on Mon, Wed, Fri, Sat
            high_idx = i % len(high_items)
            primary_subject = high_items[high_idx]["subject"]
            priority_tag = "High Priority"

            if med_items and i in (1, 3, 5):
                sec_idx = (i // 2) % len(med_items)
                secondary_subject = med_items[sec_idx]["subject"]
                task_objective = f"Deep dive into {primary_subject} difficult chapters; 30 min timed drill on {secondary_subject}."
            elif maint_items and i in (4, 6):
                m_idx = (i // 3) % len(maint_items)
                secondary_subject = maint_items[m_idx]["subject"]
                task_objective = f"Focus on {primary_subject} core concepts; quick refresh of {secondary_subject}."
            else:
                task_objective = f"Intensive formula revision, textbook exercises, and doubt resolution in {primary_subject}."

        elif med_items:
            # If no high priority, cycle medium items
            med_idx = i % len(med_items)
            primary_subject = med_items[med_idx]["subject"]
            priority_tag = "Medium Priority"

            if maint_items:
                m_idx = i % len(maint_items)
                secondary_subject = maint_items[m_idx]["subject"]
                task_objective = f"Problem set drills for {primary_subject} and review notes for {secondary_subject}."
            else:
                task_objective = f"Timed mock test and error log analysis in {primary_subject}."
        else:
            # All maintenance
            m_idx = i % len(maint_items)
            primary_subject = maint_items[m_idx]["subject"]
            priority_tag = "Maintenance"
            task_objective = f"Advanced problem exploration, competitive challenges, and peer mentoring in {primary_subject}."

        schedule.append({
            "day": day_name,
            "session_time": session_time,
            "primary_subject": primary_subject,
            "secondary_subject": secondary_subject,
            "priority_tag": priority_tag,
            "theme": day_theme,
            "task_objective": task_objective
        })

    return schedule


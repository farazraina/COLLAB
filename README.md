# 🎓 Student Academic Analysis System • Unified Academic Suite

A modern, full-featured Python desktop application and CLI designed for comprehensive student performance evaluation, multi-subject marks management, comparative class analytics, and AI-driven adaptive study planning.

Built with **Python**, **Tkinter**, and **Matplotlib**, styled in a signature **Porcelain Pearl White (`#FCF8F9`) & Cardinal Crimson Ruby (`#A21721`)** colorway with complete **Obsidian Dark Mode** support.

---

## 📑 Table of Contents
1. [Overview](#-overview)
2. [Key Architecture & Features](#-key-architecture--features)
   - [1. Role-Based Login & Authentication](#1-role-based-login--authentication)
   - [2. Multi-Subject Marks Management](#2-multi-subject-marks-management)
   - [3. Personalized Student Analytics Portal](#3-personalized-student-analytics-portal)
   - [4. AI-Driven Study Assistant & Adaptive Timetable](#4-ai-driven-study-assistant--adaptive-timetable)
   - [5. Admin Batch Analytics & Visual Charts](#5-admin-batch-analytics--visual-charts)
   - [6. Signature Dual Theme System](#6-signature-dual-theme-system)
3. [Project Directory & File Structure](#-project-directory--file-structure)
4. [Grading Scheme & Priority Rules](#-grading-scheme--priority-rules)
5. [Prerequisites & Installation](#-prerequisites--installation)
6. [How to Run the Application](#-how-to-run-the-application)
   - [Running the GUI Desktop App](#running-the-gui-desktop-app)
   - [Running the Terminal / CLI Menu](#running-the-terminal--cli-menu)
7. [Default Demo Credentials](#-default-demo-credentials)
8. [Data Model & Persistence](#-data-model--persistence)

---

## 🌟 Overview

The **Student Academic Analysis System** bridges the gap between administrative grading workflows and student-centered academic growth. Rather than storing a single generic marks number, it models 5 core subjects:
- 📐 **Mathematics**
- 🐍 **Python Programming**
- 💼 **Professional Skills**
- 🗄️ **Database Management**
- ⚡ **DSD (Digital System Design)**

The system provides two distinct user experiences:
1. **Administrative Staff & Instructors:** Manage class cohorts, enter and modify marks with live calculation previews, filter records, and inspect multi-dimensional Matplotlib charts.
2. **Students:** View an individualized report card, benchmark their scores against class averages, review automatic strengths/weaknesses insights, and follow an AI-generated weekly study plan.

---

## 🚀 Key Architecture & Features

### 1. Role-Based Login & Authentication
- **Startup Entry Point:** Clean login view with role switching between **Administrator Portal** and **Student Portal**.
- **Admin Authentication:** Protected by username and password (`admin` / `admin123`). Grants unrestricted access to batch analytics, student records management, score updates, and cohort insights.
- **Student Authentication:** Passwordless, friction-free login using **Roll Number** and **Full Name** (e.g., Roll: `101`, Name: `anayat zahoor`).
- **Session Isolation:** Once authenticated, students are locked strictly into their personal portal and cannot access other students' records or administrative modifications.
- **Safe Logout:** Both roles feature a one-click **Sign Out** button that clears active session state and redirects to the login screen.

### 2. Multi-Subject Marks Management
- Supports scores out of 100 for all 5 subjects.
- **Live Form Previews:** In both "Add Student" and "Update Marks", typing scores dynamically updates:
  $$\text{Aggregate} = \sum \text{Subject Marks} \quad (\text{out of } 500)$$
  $$\text{Percentage} = \frac{\text{Aggregate}}{500} \times 100$$
  $$\text{CGPA} = \frac{\text{Percentage}}{10.0}$$
- **Robust Field Validation:** Ensures unique roll numbers, reasonable age values (1–120), and strictly bounded scores (0–100).
- **Backward Compatibility:** Legacy records containing only a single `"marks"` field are automatically migrated and normalized on load without data loss.

### 3. Personalized Student Analytics Portal
- **Profile Hero Card:** Displays student name, roll number, course/stream, age, academic standing badge, and class rank (e.g., `#2 of 10`).
- **Subject-Wise Progress Cards:** Visual progress meters for each subject showing marks obtained vs. 100, individual letter grade, and passing status.
- **Comparative Class Benchmarking:** Displays the class average for every subject and calculates the delta ($+\Delta\%$ above average or $-\Delta\%$ below average).
- **Grouped Matplotlib Chart:** Side-by-side bar chart visualizing **My Score** vs. **Class Average** with numerical labels and benchmark lines.
- **Strengths & Weaknesses Breakdown:** Automatically identifies the student's highest-scoring subject (**Top Academic Strength**) and lowest-scoring subject (**Priority Focus Area**).

### 4. AI-Driven Study Assistant & Adaptive Timetable
A specialized academic engine that evaluates each subject's performance and generates an intelligent study schedule:
- **Low Marks ($< 60\%$):** Flags subject as **🚨 High Priority**
  - Study Allocation: **6 – 8 hours/week**
  - Focus: Foundational revision, topic breakdown, textbook review, and faculty doubt resolution.
- **Moderate Marks ($60\% – 79\%$):** Flags subject as **⚠️ Medium Priority**
  - Study Allocation: **3 – 5 hours/week**
  - Focus: Targeted problem-solving, timed practice quizzes, and error log analysis.
- **High Marks ($\ge 80\%$):** Flags subject as **✨ Maintenance**
  - Study Allocation: **1 – 2 hours/week**
  - Focus: Periodic spaced repetition, peer tutoring, and advanced mini-projects.
- **Adaptive Weekly Timetable Grid:** Generates an intelligent 7-day schedule (Monday to Sunday) mapping high-priority subjects to dedicated study blocks, rotating medium/maintenance subjects, and setting daily session themes.

### 5. Admin Batch Analytics & Visual Charts
- **6 Key Performance Indicators (KPIs):** Total Students, Class Average %, Highest Score %, Lowest Score %, Pass Rate %, and Failed Count.
- **6 Chart Modes:**
  1. **Dual View:** Subject class averages + Grade distribution donut side-by-side.
  2. **Subject Averages:** Bar chart of mean class scores across all 5 subjects.
  3. **Overall Percentages:** Student-by-student bar chart with pass/fail color coding and rotated labels.
  4. **Grade Distribution:** Donut chart with crimson gradient slices and external legend.
  5. **Course Comparison:** Horizontal bar chart comparing stream averages (e.g., AI & DS vs. CSE).
  6. **Score Brackets:** Histogram grouping students into brackets (0-39, 40-59, 60-79, 80-100).
- **Interactive Student Table:** Filterable by roll number, name, or course. Features a modal **View Report Card** dialogue and safe deletion.
- **Academic Insights Page:** Cohort Top Performer (Rank #1), Subject Toppers for each subject, Toughest vs. Strongest subject, and an At-Risk remedial alert list.

### 6. Signature Dual Theme System
- **Light Theme (Default):** Porcelain Pearl White canvas (`#FCF8F9`), Soft rose sidebar (`#F3E9EB`), Crisp white cards (`#FFFFFF`), and Signature Cardinal Crimson (`#A21721`).
- **Dark Theme:** Obsidian Dark canvas (`#150C0E`), Deep sidebar (`#0E0709`), Dark crimson cards (`#201215`), Crisp white text (`#FCF8F9`), and Cardinal Crimson (`#A21721`).
- Switchable anytime via the **☀️/🌙 Theme Toggle** on the login screen and sidebars.

---

## 📁 Project Directory & File Structure

```text
COLLAB/
├── analytics.py           # Class cohort statistics, score distributions, subject benchmarks
├── grade_calculator.py    # Grade thresholds, remarks, CGPA conversion, aggregate calculations
├── gui.py                 # Tkinter & Matplotlib desktop application (Login, Admin, Student)
├── insights.py            # Cohort honors, subject toppers, toughest subjects, remedial lists
├── main.py                # Terminal / CLI application menu with interactive options
├── storage.py             # JSON persistence, data normalization, and legacy schema migration
├── student_actions.py     # CLI actions: search report cards, update multi-subject marks
├── student_operations.py  # CLI operations: add new student, display formatted table
├── students.json          # Persistent database of normalized student records
├── study_planner.py       # AI recommendation engine & adaptive weekly timetable generator
└── README.md              # Project documentation and user manual
```

---

## 📊 Grading Scheme & Priority Rules

### Letter Grade Mapping
| Score Range (%) | Grade | Performance Remark | Grade Point (CGPA) |
|:---------------:|:-----:|:------------------:|:------------------:|
| **90 – 100**    | **A+**| Outstanding        | 9.0 – 10.0         |
| **80 – 89**     | **A** | Excellent          | 8.0 – 8.9          |
| **70 – 79**     | **B** | Very Good          | 7.0 – 7.9          |
| **60 – 69**     | **C** | Good               | 6.0 – 6.9          |
| **40 – 59**     | **D** | Pass               | 4.0 – 5.9          |
| **Below 40**    | **F** | Needs Help (Fail)  | Below 4.0          |

### AI Study Priority Heuristics
| Marks Range | Priority Level | Color Tag | Weekly Hours | Recommended Action Plan |
|:-----------:|:--------------:|:---------:|:------------:|:------------------------|
| **< 60%**   | **High**       | 🔴 Crimson| 6 – 8 hrs    | Foundational revision, micro-topic breakdown, textbook re-reading, faculty doubt clearing |
| **60 – 79%**| **Medium**     | 🟠 Amber  | 3 – 5 hrs    | Targeted problem sets, previous year papers, timed mock tests, formula drills |
| **≥ 80%**   | **Maintenance**| 🟢 Emerald| 1 – 2 hrs    | Spaced repetition, peer tutoring, advanced challenges, honors mini-projects |

---

## 💻 Prerequisites & Installation

### 1. Requirements
- Python 3.8 or higher installed on your system.
- Standard libraries: `tkinter`, `json`, `os`.
- Visualization library: `matplotlib` and `numpy`.

### 2. Install Required Dependencies
If `matplotlib` is not yet installed in your Python environment, run:
```bash
pip install matplotlib numpy
```

---

## 🖥️ How to Run the Application

### Running the GUI Desktop App
Launch the graphical interface from your terminal:
```bash
python gui.py
```
1. You will be greeted by the **Authentication Screen**.
2. Select **Administrator Portal** or **Student Portal**.
3. Sign in to explore the respective portal.

### Running the Terminal / CLI Menu
For headless environments or quick terminal-based operations, execute:
```bash
python main.py
```
Interactive menu options:
1. `Add New Student (5 Subjects)`
2. `Display All Students`
3. `Search Student by Roll Number`
4. `Update Student Subject Marks`
5. `Class Performance Dashboard`
6. `Academic Performance Insights`
7. `AI Study Assistant & Weekly Schedule`
8. `Exit`

---

## 🔑 Default Demo Credentials

| Role | Username / Identifier | Password / Validation | Access Scope |
|:---|:---|:---|:---|
| **Administrator** | `admin` | `admin123` | Full administrative control, all records, charts, and editing tools |
| **Student (Sample 1)** | Roll: `101` | Name: `anayat zahoor` | Personalized student analytics, class benchmark, AI planner |
| **Student (Sample 2)** | Roll: `102` | Name: `faraz tahir` | Personalized student analytics, class benchmark, AI planner |
| **Student (Sample 3)** | Roll: `103` | Name: `suhaib` | Cohort top performer profile (98% aggregate) |
| **Student (Sample 4)** | Roll: `109` | Name: `tufail` | Remedial profile with High Priority subject action plans |

*(Any student added by the Administrator will immediately be able to log in using their registered Roll Number and Full Name.)*

---

## 🗄️ Data Model & Persistence

Student records are saved in JSON format inside `students.json`. The normalized schema for each student entry is structured as follows:

```json
{
    "roll_no": "101",
    "name": "anayat zahoor",
    "age": 21,
    "course": "AI & DS",
    "subjects": {
        "Mathematics": 68.0,
        "Python Programming": 74.0,
        "Professional Skills": 70.0,
        "Database Management": 66.0,
        "DSD": 67.0
    },
    "total_marks": 345.0,
    "max_marks": 500.0,
    "percentage": 69.0,
    "marks": 69.0,
    "grade": "C",
    "cgpa": 6.9,
    "remark": "Good",
    "status": "PASSED"
}
```

Whenever data is loaded or saved via `storage.py`, `normalize_student()` verifies and recomputes all aggregate statistics, guaranteeing complete data integrity.


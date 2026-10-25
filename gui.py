import tkinter as tk
from tkinter import ttk, messagebox

from storage import load_students, save_students
from analytics import show_dashboard
from insights import show_insights
from grade_calculator import calculate_grade

# ── colour palette ─────────────────────────────────────────────────────────────
BG        = "#111827"
SURFACE   = "#1F2937"
CARD      = "#273449"
ACCENT    = "#818CF8"
ACCENT2   = "#A5B4FC"
TEXT      = "#E5E7EB"
MUTED     = "#9CA3AF"
SUCCESS   = "#4ADE80"
DANGER    = "#F87171"
BORDER    = "#374151"
ENTRY_BG  = "#182233"

FONT_H1   = ("Segoe UI", 20, "bold")
FONT_H2   = ("Segoe UI", 13, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 10)


# ── helpers ────────────────────────────────────────────────────────────────────
def styled_entry(parent, **kw):
    e = tk.Entry(parent, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                 relief="flat", font=FONT_BODY, bd=0, highlightthickness=1,
                 highlightbackground=BORDER, highlightcolor=ACCENT, **kw)
    return e


def styled_button(parent, text, command, color=ACCENT, width=18):
    btn = tk.Button(parent, text=text, command=command,
                    bg=color, fg="#ffffff", activebackground=ACCENT2,
                    activeforeground="#ffffff", relief="flat", cursor="hand2",
                    font=("Segoe UI", 10, "bold"), padx=12, pady=7,
                    bd=0, width=width)
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT2))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def form_row(parent, label, row):
    tk.Label(parent, text=label, bg=SURFACE, fg=MUTED,
             font=FONT_BODY, anchor="w").grid(row=row, column=0,
             sticky="w", padx=(0, 12), pady=6)
    e = styled_entry(parent, width=28)
    e.grid(row=row, column=1, sticky="ew", pady=6)
    return e


# ── main application ───────────────────────────────────────────────────────────
class StudentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("980x640")
        self.minsize(820, 560)
        self.configure(bg=BG)
        self.resizable(True, True)

        self.students = load_students()

        self._build_layout()

    # ── layout skeleton ────────────────────────────────────────────────────────
    def _build_layout(self):
        # ── sidebar ──────────────────────────────────────────────────────────
        sidebar = tk.Frame(self, bg=SURFACE, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Student\nManager", bg=SURFACE, fg=TEXT,
                 font=("Segoe UI", 13, "bold"), justify="center").pack(pady=(28, 4))
        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=16, pady=18)

        nav_items = [
            ("  Add Student",      self.show_add),
            ("  View Students",    self.show_view),
            ("  Search Student",   self.show_search),
            ("  Update Marks",     self.show_update),
            ("  Dashboard",        self.show_dashboard),
            ("  Insights",         self.show_insights),
        ]
        self.nav_buttons = []
        for label, cmd in nav_items:
            btn = tk.Button(sidebar, text=label, command=cmd,
                            bg=SURFACE, fg=TEXT, activebackground=CARD,
                            activeforeground=ACCENT, relief="flat",
                            anchor="w", padx=20, pady=10,
                            font=FONT_BODY, cursor="hand2", bd=0)
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=CARD, fg=ACCENT))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=SURFACE, fg=TEXT))
            self.nav_buttons.append(btn)

        # ── main content area ─────────────────────────────────────────────────
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True, padx=24, pady=24)

        self.show_view()          # default page

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _page_header(self, title, subtitle=""):
        tk.Label(self.content, text=title, bg=BG, fg=TEXT,
                 font=FONT_H1, anchor="w").pack(anchor="w")
        if subtitle:
            tk.Label(self.content, text=subtitle, bg=BG, fg=MUTED,
                     font=FONT_BODY, anchor="w").pack(anchor="w", pady=(2, 0))
        tk.Frame(self.content, bg=ACCENT, height=2).pack(fill="x", pady=(8, 18))

    # ── ADD STUDENT ────────────────────────────────────────────────────────────
    def show_add(self):
        self._clear_content()
        self._page_header("Add Student", "Register a new student record")

        card = tk.Frame(self.content, bg=SURFACE, padx=28, pady=28)
        card.pack(anchor="nw")
        card.columnconfigure(1, weight=1)

        self.e_roll    = form_row(card, "Roll Number", 0)
        self.e_name    = form_row(card, "Full Name",   1)
        self.e_age     = form_row(card, "Age",         2)
        self.e_course  = form_row(card, "Course",      3)
        self.e_marks   = form_row(card, "Marks (0-100)", 4)

        styled_button(card, "Add Student", self._do_add).grid(
            row=5, column=0, columnspan=2, sticky="w", pady=(16, 0))

    def _do_add(self):
        roll_no = self.e_roll.get().strip()
        name    = self.e_name.get().strip()
        course  = self.e_course.get().strip()

        if not roll_no or not name or not course:
            messagebox.showerror("Missing Fields", "Roll number, name and course are required.")
            return

        for s in self.students:
            if s["roll_no"] == roll_no:
                messagebox.showerror("Duplicate", "This roll number already exists.")
                return

        try:
            age   = int(self.e_age.get())
            marks = float(self.e_marks.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Age and marks must be numbers.")
            return

        if age <= 0:
            messagebox.showerror("Invalid Age", "Age must be greater than zero.")
            return
        if marks < 0 or marks > 100:
            messagebox.showerror("Invalid Marks", "Marks must be between 0 and 100.")
            return

        student = {"roll_no": roll_no, "name": name,
                   "age": age, "course": course, "marks": marks}
        self.students.append(student)
        save_students(self.students)

        messagebox.showinfo("Success", "Student added successfully!")
        for e in (self.e_roll, self.e_name, self.e_age, self.e_course, self.e_marks):
            e.delete(0, "end")

    # ── VIEW STUDENTS ──────────────────────────────────────────────────────────
    def show_view(self):
        self._clear_content()
        self._page_header("Student Records", f"{len(self.students)} student(s) registered")

        cols = ("Roll No", "Name", "Age", "Course", "Marks", "Grade")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                         background=CARD, foreground=TEXT,
                         fieldbackground=CARD, rowheight=32,
                         font=FONT_BODY, borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                         background=SURFACE, foreground=ACCENT2,
                         font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "#fff")])

        frame = tk.Frame(self.content, bg=BG)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=cols, show="headings",
                             style="Custom.Treeview")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=130)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

        for s in self.students:
            grade = calculate_grade(s["marks"])
            tree.insert("", "end", values=(
                s["roll_no"], s["name"], s["age"],
                s["course"], s["marks"], grade))

        if not self.students:
            tk.Label(self.content, text="No student records found.",
                     bg=BG, fg=MUTED, font=FONT_BODY).pack(pady=20)

    # ── SEARCH STUDENT ─────────────────────────────────────────────────────────
    def show_search(self):
        self._clear_content()
        self._page_header("Search Student", "Look up a student by roll number")

        row = tk.Frame(self.content, bg=BG)
        row.pack(anchor="w", pady=(0, 16))

        self.e_search = styled_entry(row, width=28)
        self.e_search.pack(side="left", padx=(0, 10))
        self.e_search.bind("<Return>", lambda e: self._do_search())
        styled_button(row, "Search", self._do_search, width=12).pack(side="left")

        self.search_result = tk.Frame(self.content, bg=BG)
        self.search_result.pack(anchor="w", fill="x")

    def _do_search(self):
        for w in self.search_result.winfo_children():
            w.destroy()

        roll_no = self.e_search.get().strip()
        found = next((s for s in self.students if s["roll_no"] == roll_no), None)

        if not found:
            tk.Label(self.search_result, text="Student not found.",
                     bg=BG, fg=DANGER, font=FONT_BODY).pack(anchor="w")
            return

        card = tk.Frame(self.search_result, bg=SURFACE, padx=24, pady=20)
        card.pack(anchor="w")

        grade = calculate_grade(found["marks"])
        fields = [
            ("Roll Number", found["roll_no"]),
            ("Name",        found["name"]),
            ("Age",         found["age"]),
            ("Course",      found["course"]),
            ("Marks",       found["marks"]),
            ("Grade",       grade),
        ]
        for i, (label, value) in enumerate(fields):
            tk.Label(card, text=label + ":", bg=SURFACE, fg=MUTED,
                     font=FONT_BODY, width=14, anchor="w").grid(
                row=i, column=0, sticky="w", pady=4)
            color = SUCCESS if label == "Grade" and grade != "F" else (DANGER if grade == "F" else TEXT)
            tk.Label(card, text=str(value), bg=SURFACE, fg=color,
                     font=("Segoe UI", 10, "bold"), anchor="w").grid(
                row=i, column=1, sticky="w", pady=4, padx=(8, 0))

    # ── UPDATE MARKS ───────────────────────────────────────────────────────────
    def show_update(self):
        self._clear_content()
        self._page_header("Update Marks", "Modify a student's marks by roll number")

        card = tk.Frame(self.content, bg=SURFACE, padx=28, pady=28)
        card.pack(anchor="nw")
        card.columnconfigure(1, weight=1)

        self.e_upd_roll  = form_row(card, "Roll Number", 0)
        self.e_upd_marks = form_row(card, "New Marks (0-100)", 1)

        styled_button(card, "Update Marks", self._do_update).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(16, 0))

    def _do_update(self):
        roll_no = self.e_upd_roll.get().strip()
        found = next((s for s in self.students if s["roll_no"] == roll_no), None)

        if not found:
            messagebox.showerror("Not Found", "Student not found.")
            return

        try:
            marks = float(self.e_upd_marks.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid marks.")
            return

        if marks < 0 or marks > 100:
            messagebox.showerror("Invalid Marks", "Marks must be between 0 and 100.")
            return

        found["marks"] = marks
        save_students(self.students)
        messagebox.showinfo("Success", "Marks updated successfully!")
        self.e_upd_roll.delete(0, "end")
        self.e_upd_marks.delete(0, "end")

    # ── DASHBOARD ──────────────────────────────────────────────────────────────
    def show_dashboard(self):
        self._clear_content()
        self._page_header("Class Performance Dashboard", "Overview of class statistics")

        if not self.students:
            tk.Label(self.content, text="No student records available.",
                     bg=BG, fg=MUTED, font=FONT_BODY).pack()
            return

        marks_list  = [s["marks"] for s in self.students]
        total       = len(self.students)
        average     = sum(marks_list) / total
        highest     = max(marks_list)
        lowest      = min(marks_list)
        passed      = sum(1 for m in marks_list if m >= 40)
        failed      = total - passed
        pass_pct    = (passed / total) * 100

        stats = [
            ("Total Students",   total,                  TEXT),
            ("Class Average",    f"{average:.2f}",       ACCENT2),
            ("Highest Marks",    highest,                SUCCESS),
            ("Lowest Marks",     lowest,                 DANGER),
            ("Students Passed",  passed,                 SUCCESS),
            ("Students Failed",  failed,                 DANGER),
            ("Pass Percentage",  f"{pass_pct:.2f} %",   ACCENT2),
        ]

        grid = tk.Frame(self.content, bg=BG)
        grid.pack(anchor="nw")

        for i, (label, value, color) in enumerate(stats):
            col = i % 3
            row = i // 3

            card = tk.Frame(grid, bg=SURFACE, padx=24, pady=18,
                            highlightthickness=1, highlightbackground=BORDER)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            tk.Label(card, text=str(value), bg=SURFACE, fg=color,
                     font=("Segoe UI", 26, "bold")).pack()
            tk.Label(card, text=label, bg=SURFACE, fg=MUTED,
                     font=FONT_BODY).pack()

    # ── INSIGHTS ───────────────────────────────────────────────────────────────
    def show_insights(self):
        self._clear_content()
        self._page_header("Academic Performance Insights", "Top performers and students needing support")

        if not self.students:
            tk.Label(self.content, text="No student records available.",
                     bg=BG, fg=MUTED, font=FONT_BODY).pack()
            return

        top = max(self.students, key=lambda s: s["marks"])
        average = sum(s["marks"] for s in self.students) / len(self.students)
        struggling = [s for s in self.students if s["marks"] < 40]

        # top performer card
        tc = tk.Frame(self.content, bg=SURFACE, padx=24, pady=18,
                      highlightthickness=1, highlightbackground=ACCENT)
        tc.pack(anchor="nw", fill="x", pady=(0, 16))

        tk.Label(tc, text="Top Performer", bg=SURFACE, fg=ACCENT2,
                 font=FONT_H2).pack(anchor="w")
        tk.Label(tc, text=f"{top['name']}  -  {top['marks']} marks  ({calculate_grade(top['marks'])})",
                 bg=SURFACE, fg=SUCCESS, font=("Segoe UI", 12)).pack(anchor="w", pady=(4, 0))

        # class average
        av_card = tk.Frame(self.content, bg=SURFACE, padx=24, pady=14,
                           highlightthickness=1, highlightbackground=BORDER)
        av_card.pack(anchor="nw", fill="x", pady=(0, 16))
        tk.Label(av_card, text=f"Class Average:  {average:.2f}",
                 bg=SURFACE, fg=ACCENT2, font=FONT_H2).pack(anchor="w")

        # struggling students
        sc = tk.Frame(self.content, bg=SURFACE, padx=24, pady=18,
                      highlightthickness=1, highlightbackground=DANGER if struggling else BORDER)
        sc.pack(anchor="nw", fill="x")

        tk.Label(sc, text="Students Needing Academic Support",
                 bg=SURFACE, fg=DANGER if struggling else MUTED,
                 font=FONT_H2).pack(anchor="w")

        if not struggling:
            tk.Label(sc, text="No students currently below the passing threshold.",
                     bg=SURFACE, fg=SUCCESS, font=FONT_BODY).pack(anchor="w", pady=(6, 0))
        else:
            for s in struggling:
                tk.Label(sc, text=f"  -  {s['name']}  -  {s['marks']} marks",
                         bg=SURFACE, fg=DANGER, font=FONT_BODY).pack(anchor="w", pady=2)


if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()

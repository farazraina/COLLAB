# =====================================================================
# gui.py
# Graphical User Interface (GUI) for Student Academic Analysis System.
# Built with Tkinter and Matplotlib.
#
# Features:
#   1. Role-Based Login & Authentication (Admin & Student)
#   2. Session Management & Safe Logout
#   3. Multi-Subject Marks Management (Math, Python, Prof Skills, DBMS, DSD)
#   4. Admin Analytics Dashboard & Visual Charts
#   5. Personalized Student Performance Dashboard & Class Comparison
#   6. AI-Driven Study Assistant & Adaptive Weekly Timetable
#   7. Dual Theme Support: Light (#FCF8F9 & #A21721) and Obsidian Dark
# =====================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from storage import load_students, save_students
from analytics import calculate_analytics
from insights import get_insights
from grade_calculator import (
    DEFAULT_SUBJECTS,
    calculate_grade,
    get_grade_remark,
    calculate_cgpa,
    calculate_student_stats
)
from study_planner import generate_study_profile


# =====================================================================
# 1. COLOR THEMES & CREDENTIALS
# =====================================================================

DEFAULT_ADMIN_USER = "admin"
DEFAULT_ADMIN_PASS = "admin123"

LIGHT_THEME = {
    "name": "light",
    "bg":              "#FCF8F9",   # Porcelain Pearl White canvas
    "sidebar":         "#F3E9EB",   # Soft rose-tinted gray sidebar
    "card":            "#FFFFFF",   # Crisp white card surface
    "card_hover":      "#FAF2F3",   # Card hover
    "input_bg":        "#FFFFFF",   # Entry box background
    "border":          "#E8D9DC",   # Subtle border
    "text":            "#1C0F11",   # Deep dark charcoal text
    "text_muted":      "#6E5659",   # Soft taupe-rose muted text
    "accent":          "#A21721",   # Signature Cardinal Crimson
    "accent_hover":    "#BF2430",   # Brighter crimson hover
    "btn_primary_bg":  "#A21721",   # Crimson primary button
    "btn_primary_fg":  "#FCF8F9",   # White text on crimson button
    "btn_primary_hov": "#831019",   # Dark crimson hover
    "btn_sec_bg":      "#F2E6E8",   # Neutral soft secondary button
    "btn_sec_fg":      "#A21721",   # Crimson text on secondary button
    "btn_sec_hov":     "#E6D4D7",   # Secondary button hover
    "chart_bg":        "#FFFFFF",   # Matplotlib figure background
    "chart_plot":      "#FCF8F9",   # Matplotlib axes plot area
    "chart_bar":       "#A21721",   # Student / Main bar color
    "chart_bar_alt":   "#8E7679",   # Class Avg / Comparison bar color
    "chart_border":    "#E8D9DC",   # Spines & gridlines
    "badge_high":      "#A21721",   # High priority crimson
    "badge_med":       "#B8621B",   # Medium priority amber
    "badge_maint":     "#2A7B4C",   # Maintenance green
}

DARK_THEME = {
    "name": "dark",
    "bg":              "#150C0E",   # Deep obsidian dark canvas
    "sidebar":         "#0E0709",   # Deeper dark sidebar
    "card":            "#201215",   # Dark crimson-tinted card surface
    "card_hover":      "#2C1A1E",   # Card hover
    "input_bg":        "#13090B",   # Entry box background
    "border":          "#381E23",   # Subtle dark border
    "text":            "#FCF8F9",   # Crisp porcelain white text
    "text_muted":      "#BBA4A7",   # Soft silver-rose muted text
    "accent":          "#A21721",   # Signature Cardinal Crimson
    "accent_hover":    "#BF2430",   # Brighter crimson hover
    "btn_primary_bg":  "#A21721",   # Crimson primary button
    "btn_primary_fg":  "#FCF8F9",   # White text on crimson button
    "btn_primary_hov": "#BF2430",   # Hover state
    "btn_sec_bg":      "#2C1A1E",   # Neutral dark button
    "btn_sec_fg":      "#FCF8F9",   # White text
    "btn_sec_hov":     "#3B2329",   # Hover state
    "chart_bg":        "#201215",   # Matplotlib figure background
    "chart_plot":      "#150C0E",   # Matplotlib axes plot area
    "chart_bar":       "#A21721",   # Student / Main bar color
    "chart_bar_alt":   "#7A6266",   # Class Avg / Comparison bar color
    "chart_border":    "#381E23",   # Spines & gridlines
    "badge_high":      "#E84C58",   # High priority bright crimson
    "badge_med":       "#F09543",   # Medium priority warm amber
    "badge_maint":     "#48B675",   # Maintenance bright emerald
}

# Typography
FONT_TITLE = ("Segoe UI", 17, "bold")
FONT_H1    = ("Segoe UI", 12, "bold")
FONT_BODY  = ("Segoe UI", 10)
FONT_BOLD  = ("Segoe UI", 10, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_MINI  = ("Segoe UI", 8)


# =====================================================================
# 2. SCROLLABLE FRAME HELPER
# =====================================================================
class ScrollableFrame(tk.Frame):
    """
    A smooth, auto-resizing scrollable frame using Tkinter Canvas
    with mousewheel support for all nested children.
    """
    def __init__(self, parent, bg_color):
        super().__init__(parent, bg=bg_color)
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content = tk.Frame(self.canvas, bg=bg_color)

        self.content.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.window_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self._bind_mousewheel(self)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)

    def _bind_mousewheel(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel)
        for child in widget.winfo_children():
            self._bind_mousewheel(child)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# =====================================================================
# 3. MAIN APPLICATION CLASS
# =====================================================================
class StudentApp(tk.Tk):
    """
    Unified Application Controller for Student Academic Analysis System.
    Handles authentication, role routing, theme toggling, and data sync.
    """

    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Student Academic Analysis System • Unified Portal")
        self.geometry("1240x800")
        self.minsize(1040, 680)

        # Theme initialization
        self.theme = LIGHT_THEME
        self.configure(bg=self.theme["bg"])

        # Active Session state
        # {"role": None | "admin" | "student", "user": None | student_dict}
        self.session = {"role": None, "user": None}

        # Data & Navigation State
        self.students = load_students()
        self.current_page = "dashboard"
        self.current_graph = "dual"
        self.chart_canvas = None

        # Build table styling and launch Login View
        self._setup_table_style()
        self.show_login()

    # -----------------------------------------------------------------
    # THEME AND STYLING
    # -----------------------------------------------------------------
    def _setup_table_style(self):
        """Sets up ttk.Treeview style for student table."""
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Custom.Treeview",
            background=self.theme["card"],
            foreground=self.theme["text"],
            fieldbackground=self.theme["card"],
            rowheight=30,
            font=FONT_BODY,
            borderwidth=0
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=self.theme["sidebar"],
            foreground=self.theme["accent"],
            font=FONT_BOLD,
            relief="flat",
            padding=(6, 8)
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", self.theme["btn_primary_bg"])],
            foreground=[("selected", self.theme["btn_primary_fg"])]
        )

    def toggle_theme(self):
        """Switches between Light (#FCF8F9) and Dark (#150C0E) theme."""
        if self.theme["name"] == "light":
            self.theme = DARK_THEME
        else:
            self.theme = LIGHT_THEME

        self.configure(bg=self.theme["bg"])
        self._setup_table_style()

        # Re-render active view
        if self.session["role"] is None:
            self.show_login()
        elif self.session["role"] == "admin":
            for widget in self.winfo_children():
                widget.destroy()
            self._build_admin_layout()
        elif self.session["role"] == "student":
            for widget in self.winfo_children():
                widget.destroy()
            self._build_student_layout()

    # -----------------------------------------------------------------
    # WIDGET CREATION HELPERS
    # -----------------------------------------------------------------
    def make_primary_button(self, parent, text, command):
        """Creates signature button in Cardinal Crimson #A21721."""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.theme["btn_primary_bg"],
            fg=self.theme["btn_primary_fg"],
            activebackground=self.theme["btn_primary_hov"],
            activeforeground=self.theme["btn_primary_fg"],
            font=FONT_BOLD,
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=7,
            bd=0
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=self.theme["btn_primary_hov"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.theme["btn_primary_bg"]))
        return btn

    def make_secondary_button(self, parent, text, command):
        """Creates subtle secondary button."""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.theme["btn_sec_bg"],
            fg=self.theme["btn_sec_fg"],
            activebackground=self.theme["btn_sec_hov"],
            activeforeground=self.theme["btn_sec_fg"],
            font=FONT_BODY,
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=6,
            bd=0
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=self.theme["btn_sec_hov"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.theme["btn_sec_bg"]))
        return btn

    def make_input_entry(self, parent, width=28, show=None):
        """Creates clean entry box with border focus highlight."""
        border_frame = tk.Frame(parent, bg=self.theme["border"], padx=1, pady=1)
        entry = tk.Entry(
            border_frame,
            bg=self.theme["input_bg"],
            fg=self.theme["text"],
            insertbackground=self.theme["accent"],
            font=FONT_BODY,
            relief="flat",
            bd=0,
            width=width,
            show=show
        )
        entry.pack(fill="both", expand=True, padx=8, pady=6)
        entry.bind("<FocusIn>",  lambda e: border_frame.config(bg=self.theme["accent"]))
        entry.bind("<FocusOut>", lambda e: border_frame.config(bg=self.theme["border"]))
        return border_frame, entry

    def make_form_row(self, parent, label_text, row_num, width=30):
        """Adds label and entry input to a form grid."""
        tk.Label(
            parent,
            text=label_text,
            bg=self.theme["card"],
            fg=self.theme["text_muted"],
            font=FONT_BODY,
            anchor="w"
        ).grid(row=row_num, column=0, sticky="w", padx=(0, 16), pady=6)

        frame, entry = self.make_input_entry(parent, width=width)
        frame.grid(row=row_num, column=1, sticky="ew", pady=6)
        return entry

    def _clear_window(self):
        """Cleans all widgets from main window."""
        if self.chart_canvas:
            try:
                self.chart_canvas.get_tk_widget().destroy()
            except Exception:
                pass
            self.chart_canvas = None

        for child in self.winfo_children():
            child.destroy()

    def logout(self):
        """Terminates active session and routes back to Login Screen."""
        if messagebox.askyesno("Confirm Sign Out", "Are you sure you want to sign out?"):
            self.session = {"role": None, "user": None}
            self.current_page = "dashboard"
            self.show_login()

    # =====================================================================
    # 4. AUTHENTICATION & LOGIN SCREEN
    # =====================================================================
    def show_login(self):
        """Constructs modern, polished role-based login screen."""
        self._clear_window()
        self.configure(bg=self.theme["bg"])

        # Main Centered Container
        center_wrap = tk.Frame(self, bg=self.theme["bg"])
        center_wrap.place(relx=0.5, rely=0.5, anchor="center")

        # Top Theme Toggle Pill in top right
        top_bar = tk.Frame(self, bg=self.theme["bg"])
        top_bar.pack(side="top", fill="x", padx=24, pady=16)

        theme_lbl = "🌙 Dark Mode" if self.theme["name"] == "light" else "☀️ Light Mode"
        self.make_secondary_button(top_bar, theme_lbl, self.toggle_theme).pack(side="right")

        # Login Card Container
        card = tk.Frame(
            center_wrap,
            bg=self.theme["card"],
            padx=40,
            pady=36,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        card.pack()

        # Header Badge
        badge = tk.Frame(card, bg=self.theme["accent"], padx=10, pady=4)
        badge.pack(anchor="center", pady=(0, 10))
        tk.Label(
            badge,
            text="● ACADEMIC SUITE • 2026",
            bg=self.theme["accent"],
            fg="#FCF8F9",
            font=("Segoe UI", 8, "bold")
        ).pack()

        tk.Label(
            card,
            text="Student Academic Analysis System",
            bg=self.theme["card"],
            fg=self.theme["text"],
            font=FONT_TITLE
        ).pack(anchor="center")

        tk.Label(
            card,
            text="Unified Performance Analytics & Adaptive Study Recommendations",
            bg=self.theme["card"],
            fg=self.theme["text_muted"],
            font=FONT_SMALL
        ).pack(anchor="center", pady=(4, 20))

        # Role Selector Switcher (Admin vs Student)
        self.login_role_var = tk.StringVar(value="admin")

        role_bar = tk.Frame(card, bg=self.theme["sidebar"], padx=4, pady=4)
        role_bar.pack(fill="x", pady=(0, 22))

        self.btn_role_admin = tk.Button(
            role_bar,
            text="🔐 Administrator Portal",
            command=lambda: self._switch_login_mode("admin"),
            bg=self.theme["accent"],
            fg="#FCF8F9",
            font=FONT_BOLD,
            relief="flat",
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2"
        )
        self.btn_role_admin.pack(side="left", fill="x", expand=True)

        self.btn_role_student = tk.Button(
            role_bar,
            text="🎓 Student Portal",
            command=lambda: self._switch_login_mode("student"),
            bg=self.theme["sidebar"],
            fg=self.theme["text_muted"],
            font=FONT_BODY,
            relief="flat",
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2"
        )
        self.btn_role_student.pack(side="left", fill="x", expand=True)

        # Dynamic Forms Frame
        self.login_form_frame = tk.Frame(card, bg=self.theme["card"])
        self.login_form_frame.pack(fill="x")

        self._render_login_form("admin")

    def _switch_login_mode(self, mode):
        """Switches active login form between Admin and Student."""
        self.login_role_var.set(mode)
        if mode == "admin":
            self.btn_role_admin.config(bg=self.theme["accent"], fg="#FCF8F9", font=FONT_BOLD)
            self.btn_role_student.config(bg=self.theme["sidebar"], fg=self.theme["text_muted"], font=FONT_BODY)
        else:
            self.btn_role_student.config(bg=self.theme["accent"], fg="#FCF8F9", font=FONT_BOLD)
            self.btn_role_admin.config(bg=self.theme["sidebar"], fg=self.theme["text_muted"], font=FONT_BODY)

        self._render_login_form(mode)

    def _render_login_form(self, mode):
        """Renders either Admin credential inputs or Student Roll Number inputs."""
        for child in self.login_form_frame.winfo_children():
            child.destroy()

        if mode == "admin":
            tk.Label(
                self.login_form_frame,
                text="Administrator Sign In",
                bg=self.theme["card"],
                fg=self.theme["text"],
                font=FONT_H1,
                anchor="w"
            ).pack(fill="x", pady=(0, 4))

            tk.Label(
                self.login_form_frame,
                text="Access batch records, grade calculations, and analytics controls",
                bg=self.theme["card"],
                fg=self.theme["text_muted"],
                font=FONT_SMALL,
                anchor="w"
            ).pack(fill="x", pady=(0, 14))

            # Username
            tk.Label(self.login_form_frame, text="Username", bg=self.theme["card"],
                     fg=self.theme["text_muted"], font=FONT_BODY, anchor="w").pack(fill="x")
            u_frame, self.e_admin_user = self.make_input_entry(self.login_form_frame, width=34)
            u_frame.pack(fill="x", pady=(4, 12))
            self.e_admin_user.insert(0, "admin")

            # Password
            tk.Label(self.login_form_frame, text="Password", bg=self.theme["card"],
                     fg=self.theme["text_muted"], font=FONT_BODY, anchor="w").pack(fill="x")
            p_frame, self.e_admin_pass = self.make_input_entry(self.login_form_frame, width=34, show="•")
            p_frame.pack(fill="x", pady=(4, 16))
            self.e_admin_pass.insert(0, "admin123")
            self.e_admin_pass.bind("<Return>", lambda e: self._do_admin_login())

            # Submit button
            self.make_primary_button(
                self.login_form_frame,
                "Sign In as Admin ➔",
                self._do_admin_login
            ).pack(fill="x", pady=(4, 12))

            # Hint
            hint_box = tk.Frame(self.login_form_frame, bg=self.theme["sidebar"], padx=10, pady=8)
            hint_box.pack(fill="x", pady=(4, 0))
            tk.Label(
                hint_box,
                text="💡 Demo Credentials: Username 'admin' | Password 'admin123'",
                bg=self.theme["sidebar"],
                fg=self.theme["text_muted"],
                font=FONT_MINI
            ).pack(anchor="center")

        else:
            tk.Label(
                self.login_form_frame,
                text="Student Portal Login",
                bg=self.theme["card"],
                fg=self.theme["text"],
                font=FONT_H1,
                anchor="w"
            ).pack(fill="x", pady=(0, 4))

            tk.Label(
                self.login_form_frame,
                text="Enter your Roll Number and Name to access your personalized report card",
                bg=self.theme["card"],
                fg=self.theme["text_muted"],
                font=FONT_SMALL,
                anchor="w"
            ).pack(fill="x", pady=(0, 14))

            # Roll Number
            tk.Label(self.login_form_frame, text="Roll Number", bg=self.theme["card"],
                     fg=self.theme["text_muted"], font=FONT_BODY, anchor="w").pack(fill="x")
            r_frame, self.e_student_roll = self.make_input_entry(self.login_form_frame, width=34)
            r_frame.pack(fill="x", pady=(4, 12))
            self.e_student_roll.insert(0, "101")

            # Full Name
            tk.Label(self.login_form_frame, text="Full Name", bg=self.theme["card"],
                     fg=self.theme["text_muted"], font=FONT_BODY, anchor="w").pack(fill="x")
            n_frame, self.e_student_name = self.make_input_entry(self.login_form_frame, width=34)
            n_frame.pack(fill="x", pady=(4, 16))
            self.e_student_name.insert(0, "abc def")
            self.e_student_name.bind("<Return>", lambda e: self._do_student_login())

            # Submit button
            self.make_primary_button(
                self.login_form_frame,
                "Access My Student Portal ➔",
                self._do_student_login
            ).pack(fill="x", pady=(4, 12))

            # Helper Hint with available students
            hint_box = tk.Frame(self.login_form_frame, bg=self.theme["sidebar"], padx=10, pady=8)
            hint_box.pack(fill="x", pady=(4, 0))
            tk.Label(
                hint_box,
                text="💡 Example Students: Roll 10 (abc def) ",
                bg=self.theme["sidebar"],
                fg=self.theme["text_muted"],
                font=FONT_MINI
            ).pack(anchor="center")

    def _do_admin_login(self):
        """Validates administrator credentials."""
        u = self.e_admin_user.get().strip()
        p = self.e_admin_pass.get().strip()

        if u == DEFAULT_ADMIN_USER and p == DEFAULT_ADMIN_PASS:
            self.session = {"role": "admin", "user": {"name": "Administrator"}}
            self.current_page = "dashboard"
            self._build_admin_layout()
        else:
            messagebox.showerror(
                "Access Denied",
                "Invalid Administrator credentials!\nPlease check username and password."
            )

    def _do_student_login(self):
        """Validates student credentials by Roll Number and Name."""
        r = self.e_student_roll.get().strip()
        name = self.e_student_name.get().strip().lower()

        if not r or not name:
            messagebox.showerror("Incomplete Details", "Please provide both Roll Number and Full Name.")
            return

        self.students = load_students()
        matched_student = None

        for s in self.students:
            if str(s.get("roll_no", "")).strip() == r:
                # Name check (tolerant of case and extra spaces)
                db_name = s.get("name", "").strip().lower()
                if db_name == name or name in db_name or db_name in name:
                    matched_student = s
                    break

        if matched_student:
            self.session = {"role": "student", "user": matched_student}
            self.current_page = "student_overview"
            self._build_student_layout()
        else:
            messagebox.showerror(
                "Student Not Found",
                f"No student record matched Roll Number '{r}' with Name '{name.title()}'.\n\n"
                "Please verify your details or ask your administrator to register your record."
            )

    # =====================================================================
    # 5. ADMIN PORTAL LAYOUT & NAVIGATION
    # =====================================================================
    def _build_admin_layout(self):
        """Constructs Admin Sidebar and Dynamic Content Container."""
        self._clear_window()
        self.students = load_students()

        # 1. Sidebar
        self.sidebar = tk.Frame(self, bg=self.theme["sidebar"], width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand Header
        brand_box = tk.Frame(self.sidebar, bg=self.theme["sidebar"], padx=18, pady=20)
        brand_box.pack(fill="x")

        badge = tk.Frame(brand_box, bg=self.theme["accent"], padx=9, pady=3)
        badge.pack(anchor="w", pady=(0, 8))
        tk.Label(
            badge,
            text="● ADMIN CONSOLE",
            bg=self.theme["accent"],
            fg="#FCF8F9",
            font=("Segoe UI", 8, "bold")
        ).pack()

        tk.Label(
            brand_box,
            text="Academic Hub",
            bg=self.theme["sidebar"],
            fg=self.theme["text"],
            font=FONT_TITLE,
            anchor="w"
        ).pack(anchor="w")

        tk.Label(
            brand_box,
            text="Batch Management & Analytics",
            bg=self.theme["sidebar"],
            fg=self.theme["text_muted"],
            font=FONT_SMALL,
            anchor="w"
        ).pack(anchor="w")

        tk.Frame(self.sidebar, bg=self.theme["border"], height=1).pack(fill="x", padx=16, pady=10)

        # Admin Nav Menu
        admin_menu = [
            ("📊 Dashboard & Graphs", "dashboard", self.show_admin_dashboard),
            ("📋 Student Records",    "records",   self.show_admin_records),
            ("➕ Add Student",        "add",       self.show_admin_add),
            ("✏️ Update Marks",       "update",    self.show_admin_update),
            ("💡 Academic Insights",  "insights",  self.show_admin_insights),
        ]

        self.admin_nav_buttons = {}
        for title, key, cmd in admin_menu:
            is_active = (self.current_page == key)
            btn = tk.Button(
                self.sidebar,
                text=f"  {title}",
                command=lambda c=cmd, k=key: self._switch_admin_page(c, k),
                bg=self.theme["accent"] if is_active else self.theme["sidebar"],
                fg="#FCF8F9" if is_active else self.theme["text_muted"],
                activebackground=self.theme["card_hover"],
                activeforeground=self.theme["text"],
                font=FONT_BOLD if is_active else FONT_BODY,
                relief="flat",
                anchor="w",
                padx=16,
                pady=10,
                cursor="hand2",
                bd=0
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.admin_nav_buttons[key] = btn

        # Sidebar Bottom Controls (Theme & Sign Out)
        bottom_box = tk.Frame(self.sidebar, bg=self.theme["card"], padx=12, pady=12)
        bottom_box.pack(side="bottom", fill="x", padx=12, pady=16)

        theme_text = "🌙 Dark Mode" if self.theme["name"] == "light" else "☀️ Light Mode"
        self.make_secondary_button(bottom_box, theme_text, self.toggle_theme).pack(fill="x", pady=(0, 6))
        self.make_secondary_button(bottom_box, "🚪 Sign Out", self.logout).pack(fill="x")

        tk.Label(
            bottom_box,
            text=f"Logged in: Admin ({len(self.students)} students)",
            bg=self.theme["card"],
            fg=self.theme["text_muted"],
            font=FONT_MINI
        ).pack(anchor="w", pady=(8, 0))

        # 2. Main Content Canvas with Scrollbar
        self.scroll_area = ScrollableFrame(self, self.theme["bg"])
        self.scroll_area.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        self.content = self.scroll_area.content

        # Route initial page
        if self.current_page == "dashboard":
            self.show_admin_dashboard()
        elif self.current_page == "records":
            self.show_admin_records()
        elif self.current_page == "add":
            self.show_admin_add()
        elif self.current_page == "update":
            self.show_admin_update()
        else:
            self.show_admin_insights()

    def _switch_admin_page(self, command, page_key):
        """Navigates to chosen admin page and updates active menu style."""
        self.current_page = page_key
        for key, btn in self.admin_nav_buttons.items():
            if key == page_key:
                btn.config(bg=self.theme["accent"], fg="#FCF8F9", font=FONT_BOLD)
            else:
                btn.config(bg=self.theme["sidebar"], fg=self.theme["text_muted"], font=FONT_BODY)
        command()

    def _clear_content(self):
        """Clears content and frees matplotlib canvas resources."""
        if self.chart_canvas:
            try:
                self.chart_canvas.get_tk_widget().destroy()
            except Exception:
                pass
            self.chart_canvas = None

        for child in self.content.winfo_children():
            child.destroy()

    def _make_header(self, title, subtitle=""):
        """Displays consistent page title and subtitle."""
        tk.Label(self.content, text=title, bg=self.theme["bg"],
                 fg=self.theme["accent"], font=FONT_TITLE, anchor="w").pack(anchor="w")
        if subtitle:
            tk.Label(self.content, text=subtitle, bg=self.theme["bg"],
                     fg=self.theme["text_muted"], font=FONT_BODY, anchor="w").pack(anchor="w", pady=(2, 0))
        tk.Frame(self.content, bg=self.theme["border"], height=1).pack(fill="x", pady=(10, 16))

    # =====================================================================
    # 6. ADMIN PAGE 1: DASHBOARD & GRAPHS
    # =====================================================================
    def show_admin_dashboard(self):
        """Displays KPI summary cards and multi-mode charts."""
        self._clear_content()
        self.students = load_students()
        self._make_header(
            "Batch Analytics Dashboard",
            "Comprehensive class statistics, multi-subject averages, and distribution charts"
        )

        if not self.students:
            empty_box = tk.Frame(self.content, bg=self.theme["card"], padx=24, pady=24)
            empty_box.pack(fill="x")
            tk.Label(empty_box, text="No students registered yet.",
                     bg=self.theme["card"], fg=self.theme["text"], font=FONT_H1).pack()
            self.make_primary_button(empty_box, "Add First Student", self.show_admin_add).pack(pady=(12, 0))
            return

        analytics = calculate_analytics(self.students)

        # KPI Stat Cards
        kpi_row = tk.Frame(self.content, bg=self.theme["bg"])
        kpi_row.pack(fill="x", pady=(0, 14))

        cards = [
            ("Total Students", str(analytics["total"])),
            ("Class Average",  f"{analytics['average']}%"),
            ("Highest Score",  f"{analytics['highest']}%"),
            ("Lowest Score",   f"{analytics['lowest']}%"),
            ("Pass Rate",      f"{analytics['pass_percentage']}%"),
            ("Failed (<40%)",  str(analytics["failed"]))
        ]

        for i, (label, val) in enumerate(cards):
            card = tk.Frame(
                kpi_row,
                bg=self.theme["card"],
                padx=14,
                pady=12,
                highlightthickness=1,
                highlightbackground=self.theme["border"]
            )
            card.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 8, 0))

            tk.Label(card, text=label, bg=self.theme["card"],
                     fg=self.theme["text_muted"], font=FONT_SMALL).pack(anchor="w")
            val_color = self.theme["accent"] if label in ("Highest Score", "Pass Rate") else self.theme["text"]
            tk.Label(card, text=val, bg=self.theme["card"],
                     fg=val_color, font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(4, 0))

        # Graph Mode Selector
        ctrl_bar = tk.Frame(
            self.content,
            bg=self.theme["card"],
            padx=10,
            pady=8,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        ctrl_bar.pack(fill="x", pady=(0, 12))

        tk.Label(ctrl_bar, text="SELECT VISUALIZATION:", bg=self.theme["card"],
                 fg=self.theme["text_muted"], font=("Segoe UI", 8, "bold")).pack(side="left", padx=(4, 10))

        graph_options = [
            ("🔲 Dual View",          "dual"),
            ("📚 Subject Averages",   "subjects"),
            ("📊 Overall Percentages", "bar"),
            ("🍩 Grade Distribution", "donut"),
            ("🏛️ Course Comparison",   "course"),
            ("📉 Score Brackets",     "brackets")
        ]

        self.graph_btns = {}
        for text, mode in graph_options:
            is_active = (self.current_graph == mode)
            btn = tk.Button(
                ctrl_bar,
                text=text,
                command=lambda m=mode: self._switch_graph(m),
                bg=self.theme["accent"] if is_active else self.theme["btn_sec_bg"],
                fg="#FCF8F9" if is_active else self.theme["btn_sec_fg"],
                font=("Segoe UI", 8, "bold" if is_active else "normal"),
                relief="flat",
                cursor="hand2",
                padx=9,
                pady=4,
                bd=0
            )
            btn.pack(side="left", padx=3)
            self.graph_btns[mode] = btn

        # Container for Matplotlib Canvas
        self.chart_container = tk.Frame(
            self.content,
            bg=self.theme["card"],
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        self.chart_container.pack(fill="both", expand=True)

        self._draw_charts(analytics)

    def _switch_graph(self, mode):
        """Switches the chart view."""
        self.current_graph = mode
        for m, btn in self.graph_btns.items():
            if m == mode:
                btn.config(bg=self.theme["accent"], fg="#FCF8F9", font=("Segoe UI", 8, "bold"))
            else:
                btn.config(bg=self.theme["btn_sec_bg"], fg=self.theme["btn_sec_fg"], font=("Segoe UI", 8, "normal"))

        analytics = calculate_analytics(self.students)
        self._draw_charts(analytics)

    def _draw_charts(self, analytics):
        """Draws clean charts with proper spacing, margins, and non-overlapping text."""
        for w in self.chart_container.winfo_children():
            w.destroy()

        mode = self.current_graph

        if mode == "dual":
            fig = Figure(figsize=(9.6, 4.3), facecolor=self.theme["chart_bg"], dpi=100)
            ax1 = fig.add_subplot(1, 2, 1)
            ax2 = fig.add_subplot(1, 2, 2)
            self._plot_subject_averages(ax1, analytics)
            self._plot_donut(ax2, analytics)
            fig.tight_layout(pad=2.2)

        elif mode == "subjects":
            fig = Figure(figsize=(9.6, 4.3), facecolor=self.theme["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_subject_averages(ax, analytics, detailed=True)
            fig.tight_layout(pad=2.0)

        elif mode == "bar":
            fig = Figure(figsize=(9.6, 4.3), facecolor=self.theme["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_bar(ax)
            fig.tight_layout(pad=2.0)

        elif mode == "donut":
            fig = Figure(figsize=(9.6, 4.3), facecolor=self.theme["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_donut(ax, analytics, detailed=True)
            fig.tight_layout(pad=2.0)

        elif mode == "course":
            fig = Figure(figsize=(9.6, 4.3), facecolor=self.theme["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_course(ax, analytics)
            fig.tight_layout(pad=2.0)

        else:
            fig = Figure(figsize=(9.6, 4.3), facecolor=self.theme["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_brackets(ax, analytics)
            fig.tight_layout(pad=2.0)

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

    def _plot_subject_averages(self, ax, analytics, detailed=False):
        """Plots bar chart of Class Averages across all 5 subjects."""
        ax.set_facecolor(self.theme["chart_plot"])
        stats = analytics.get("subject_stats", {})

        subjects = DEFAULT_SUBJECTS
        short_names = ["Math", "Python", "Prof Skills", "DBMS", "DSD"]
        averages = [stats.get(s, {}).get("average", 0.0) for s in subjects]

        x = range(len(subjects))
        bars = ax.bar(x, averages, color=self.theme["chart_bar"], width=0.5, edgecolor=self.theme["border"])

        for bar, avg in zip(bars, averages):
            ax.annotate(
                f"{avg:.1f}%",
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center", va="bottom",
                color=self.theme["text"],
                fontsize=8.5,
                fontweight="bold"
            )

        ax.set_xticks(list(x))
        ax.set_xticklabels(short_names, fontsize=8.5, color=self.theme["text"])
        ax.set_ylim(0, 115)
        ax.set_ylabel("Class Average (%)", color=self.theme["text_muted"], fontsize=8.5)
        ax.set_title("Subject-Wise Class Performance", color=self.theme["accent"], fontsize=11, fontweight="bold", pad=8)
        ax.tick_params(colors=self.theme["text_muted"], labelsize=8)

        # Baseline at 40 (Passing) and 75 (Target)
        ax.axhline(40, color=self.theme["text_muted"], linestyle="--", linewidth=1.0, alpha=0.7, label="Pass Benchmark (40%)")
        ax.axhline(75, color=self.theme["accent"], linestyle=":", linewidth=1.1, alpha=0.8, label="Target (75%)")

        for spine in ax.spines.values():
            spine.set_color(self.theme["chart_border"])
        ax.grid(axis="y", color=self.theme["chart_border"], linestyle=":", alpha=0.6)
        ax.legend(facecolor=self.theme["card"], edgecolor=self.theme["chart_border"],
                  labelcolor=self.theme["text"], fontsize=7.5, loc="upper right")

    def _plot_bar(self, ax):
        """Plots bar chart of student aggregate percentage scores."""
        ax.set_facecolor(self.theme["chart_plot"])

        names = []
        for s in self.students:
            full = s["name"].strip().title()
            parts = full.split()
            names.append(f"{parts[0]} {parts[1][0]}." if len(parts) > 1 else full[:9])

        pcts = [float(s.get("percentage", s.get("marks", 0.0))) for s in self.students]
        x = range(len(names))
        n_students = len(pcts)
        bar_width = 0.55 if n_students <= 6 else max(0.4, 4.5 / n_students)

        colors = [self.theme["chart_bar"] if p >= 40 else self.theme["chart_bar_alt"] for p in pcts]
        bars = ax.bar(x, pcts, color=colors, width=bar_width, edgecolor=self.theme["border"], linewidth=0.8)

        for bar, p in zip(bars, pcts):
            grade = calculate_grade(p)
            ax.annotate(
                f"{p:.0f}%\n({grade})",
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center", va="bottom",
                color=self.theme["text"],
                fontsize=7.5 if n_students > 8 else 8.5,
                fontweight="bold"
            )

        ax.set_xticks(list(x))
        rotation_angle = 35 if n_students >= 5 else 0
        ha_align = "right" if rotation_angle > 0 else "center"
        ax.set_xticklabels(names, rotation=rotation_angle, ha=ha_align, fontsize=8, color=self.theme["text"])

        avg = sum(pcts) / len(pcts) if pcts else 0.0
        ax.axhline(40, color=self.theme["text_muted"], linestyle="--", linewidth=1.1, alpha=0.8, label="Pass (40%)")
        ax.axhline(avg, color=self.theme["accent"], linestyle=":", linewidth=1.2, alpha=0.9, label=f"Avg ({avg:.1f}%)")

        ax.set_ylim(0, max(115, max(pcts, default=100) + 12))
        ax.set_ylabel("Overall Percentage (%)", color=self.theme["text_muted"], fontsize=8.5)
        ax.set_title("Student Aggregate Scores", color=self.theme["accent"], fontsize=11, fontweight="bold", pad=8)
        ax.tick_params(colors=self.theme["text_muted"], labelsize=8)

        for spine in ax.spines.values():
            spine.set_color(self.theme["chart_border"])
        ax.grid(axis="y", color=self.theme["chart_border"], linestyle=":", alpha=0.6)
        ax.legend(facecolor=self.theme["card"], edgecolor=self.theme["chart_border"],
                  labelcolor=self.theme["text"], fontsize=7.5, loc="upper right")

    def _plot_donut(self, ax, analytics, detailed=False):
        """Plots clean donut chart for grade distribution."""
        ax.set_facecolor(self.theme["chart_bg"])
        grade_counts = analytics["grade_counts"]
        labels = [g for g, c in grade_counts.items() if c > 0]
        counts = [c for g, c in grade_counts.items() if c > 0]

        if not counts:
            ax.text(0.5, 0.5, "No Data", color=self.theme["text_muted"], ha="center", va="center")
            return

        crimson_palette = ["#A21721", "#BF2632", "#D64852", "#E87881", "#F2A8AF", "#FBD3D7"]
        slice_colors = crimson_palette[:len(labels)]

        wedges, texts, autotexts = ax.pie(
            counts,
            autopct="%1.0f%%",
            pctdistance=0.72,
            startangle=140,
            colors=slice_colors,
            textprops={"fontsize": 8, "fontweight": "bold", "color": "#FFFFFF"},
            wedgeprops={"edgecolor": self.theme["chart_bg"], "linewidth": 2, "width": 0.45}
        )

        for at in autotexts:
            at.set_color("#FFFFFF")

        ax.text(0, 0, f"Total\n{analytics['total']}", ha="center", va="center",
                color=self.theme["accent"], fontsize=10, fontweight="bold")
        ax.set_title("Grade Distribution", color=self.theme["accent"], fontsize=11, fontweight="bold", pad=8)

        legend_labels = [f"Grade {g}: {c}" for g, c in zip(labels, counts)]
        ax.legend(
            wedges, legend_labels,
            loc="center left",
            bbox_to_anchor=(0.92, 0.5),
            facecolor=self.theme["card"],
            edgecolor=self.theme["chart_border"],
            labelcolor=self.theme["text"],
            fontsize=8
        )

    def _plot_course(self, ax, analytics):
        """Plots horizontal bar chart comparing course averages."""
        ax.set_facecolor(self.theme["chart_plot"])
        stats = analytics.get("course_stats", {})
        if not stats:
            ax.text(0.5, 0.5, "No Course Data", color=self.theme["text_muted"], ha="center", va="center")
            return

        courses = list(stats.keys())
        averages = [data["average"] for data in stats.values()]

        y = range(len(courses))
        bars = ax.barh(y, averages, color=self.theme["chart_bar"], height=0.45, edgecolor=self.theme["border"])

        for bar, avg in zip(bars, averages):
            ax.annotate(
                f" {avg:.1f}%",
                xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                xytext=(6, 0),
                textcoords="offset points",
                ha="left", va="center",
                color=self.theme["text"],
                fontsize=9,
                fontweight="bold"
            )

        ax.set_yticks(y)
        ax.set_yticklabels(courses, color=self.theme["text"], fontsize=9.5)
        ax.set_xlim(0, 115)
        ax.set_xlabel("Average Score (%)", color=self.theme["text_muted"], fontsize=9)
        ax.set_title("Course Performance Breakdown", color=self.theme["accent"], fontsize=11, fontweight="bold", pad=8)
        ax.tick_params(colors=self.theme["text_muted"])

        for spine in ax.spines.values():
            spine.set_color(self.theme["chart_border"])
        ax.grid(axis="x", color=self.theme["chart_border"], linestyle=":", alpha=0.6)

    def _plot_brackets(self, ax, analytics):
        """Plots score ranges histogram."""
        ax.set_facecolor(self.theme["chart_plot"])
        ranges = analytics.get("score_ranges", {})
        labels = list(ranges.keys())
        values = list(ranges.values())

        colors = ["#8E7679", "#D64852", "#BF2632", "#A21721"]
        bars = ax.bar(labels, values, color=colors, width=0.5, edgecolor=self.theme["border"])

        for bar, val in zip(bars, values):
            ax.annotate(
                f"{val} student(s)",
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center", va="bottom",
                color=self.theme["text"],
                fontsize=9,
                fontweight="bold"
            )

        ax.set_ylim(0, max(values, default=1) + 2)
        ax.set_ylabel("Student Count", color=self.theme["text_muted"], fontsize=9)
        ax.set_title("Score Bracket Distribution", color=self.theme["accent"], fontsize=11, fontweight="bold", pad=8)
        ax.tick_params(colors=self.theme["text_muted"], labelsize=9)

        for spine in ax.spines.values():
            spine.set_color(self.theme["chart_border"])
        ax.grid(axis="y", color=self.theme["chart_border"], linestyle=":", alpha=0.6)

    # =====================================================================
    # 7. ADMIN PAGE 2: VIEW STUDENT RECORDS (TABLE, SEARCH, DELETE)
    # =====================================================================
    def show_admin_records(self):
        """Displays multi-subject student records table with search & actions."""
        self._clear_content()
        self.students = load_students()
        self._make_header("Student Records", f"{len(self.students)} registered student(s) with multi-subject marks")

        toolbar = tk.Frame(self.content, bg=self.theme["bg"])
        toolbar.pack(fill="x", pady=(0, 12))

        tk.Label(toolbar, text="Search Records:", bg=self.theme["bg"],
                 fg=self.theme["text_muted"], font=FONT_BODY).pack(side="left", padx=(0, 8))

        search_wrap, self.search_box = self.make_input_entry(toolbar, width=24)
        search_wrap.pack(side="left", padx=(0, 12))
        self.search_box.bind("<KeyRelease>", lambda e: self._filter_students())

        self.make_secondary_button(toolbar, "Delete Selected", self._delete_student).pack(side="right", padx=(8, 0))
        self.make_secondary_button(toolbar, "View Report Card", self._inspect_selected_student).pack(side="right", padx=(8, 0))
        self.make_secondary_button(toolbar, "➕ Add Student", self.show_admin_add).pack(side="right")

        table_box = tk.Frame(
            self.content,
            bg=self.theme["card"],
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        table_box.pack(fill="both", expand=True)

        columns = (
            "roll_no", "name", "course", "math", "python",
            "prof", "dbms", "dsd", "total", "pct", "grade", "cgpa", "status"
        )
        self.tree = ttk.Treeview(table_box, columns=columns, show="headings",
                                 style="Custom.Treeview", selectmode="browse", height=14)

        headers = [
            ("roll_no", "Roll No",   75,  "center"),
            ("name",    "Student",   140, "w"),
            ("course",  "Course",    100, "w"),
            ("math",    "Math",      55,  "center"),
            ("python",  "Python",    60,  "center"),
            ("prof",    "Prof Sk",   60,  "center"),
            ("dbms",    "DBMS",      55,  "center"),
            ("dsd",     "DSD",       55,  "center"),
            ("total",   "Total/500", 75,  "center"),
            ("pct",     "Pct %",     65,  "center"),
            ("grade",   "Grade",     55,  "center"),
            ("cgpa",    "CGPA",      55,  "center"),
            ("status",  "Status",    90,  "center"),
        ]

        for col_id, col_text, col_width, col_align in headers:
            self.tree.heading(col_id, text=col_text)
            self.tree.column(col_id, width=col_width, anchor=col_align)

        sb = ttk.Scrollbar(table_box, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", lambda e: self._inspect_selected_student())
        self._populate_table(self.students)

    def _populate_table(self, records):
        """Fills treeview rows with student data."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for s in records:
            subjs = s.get("subjects", {})
            m_math = subjs.get("Mathematics", 0.0)
            m_py   = subjs.get("Python Programming", 0.0)
            m_prof = subjs.get("Professional Skills", 0.0)
            m_db   = subjs.get("Database Management", 0.0)
            m_dsd  = subjs.get("DSD", 0.0)

            tot = s.get("total_marks", 0.0)
            pct = s.get("percentage", 0.0)
            grd = s.get("grade", calculate_grade(pct))
            cgpa = s.get("cgpa", round(pct / 10.0, 2))
            status = s.get("status", "PASSED" if pct >= 40 else "FAILED")

            self.tree.insert("", "end", values=(
                s["roll_no"], s["name"].title(), s.get("course", "General"),
                f"{m_math:.0f}", f"{m_py:.0f}", f"{m_prof:.0f}", f"{m_db:.0f}", f"{m_dsd:.0f}",
                f"{tot:.0f}", f"{pct:.1f}%", grd, f"{cgpa:.2f}", status
            ))

    def _filter_students(self):
        """Live search filter as user types."""
        q = self.search_box.get().strip().lower()
        if not q:
            self._populate_table(self.students)
            return

        filtered = []
        for s in self.students:
            if (q in str(s["roll_no"]).lower() or
                q in str(s["name"]).lower() or
                q in str(s.get("course", "")).lower()):
                filtered.append(s)

        self._populate_table(filtered)

    def _inspect_selected_student(self):
        """Opens a modal dialogue displaying full student report card."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Student", "Please select a student row to inspect.")
            return

        row = self.tree.item(selected[0], "values")
        roll_no = row[0]
        found = next((s for s in self.students if str(s["roll_no"]) == str(roll_no)), None)
        if not found:
            return

        # Modal Dialog
        dlg = tk.Toplevel(self)
        dlg.title(f"Student Report Card • {found['name'].title()}")
        dlg.geometry("540x560")
        dlg.minsize(480, 500)
        dlg.configure(bg=self.theme["card"])
        dlg.transient(self)
        dlg.grab_set()

        p = tk.Frame(dlg, bg=self.theme["card"], padx=24, pady=24)
        p.pack(fill="both", expand=True)

        tk.Label(p, text=found["name"].title(), bg=self.theme["card"],
                 fg=self.theme["accent"], font=FONT_TITLE).pack(anchor="w")
        tk.Label(p, text=f"Roll Number: {found['roll_no']}  •  Course: {found.get('course', 'General')}  •  Age: {found.get('age', 20)}",
                 bg=self.theme["card"], fg=self.theme["text_muted"], font=FONT_BODY).pack(anchor="w", pady=(2, 16))

        tk.Frame(p, bg=self.theme["border"], height=1).pack(fill="x", pady=(0, 16))

        tk.Label(p, text="SUBJECT PERFORMANCE (OUT OF 100):", bg=self.theme["card"],
                 fg=self.theme["text_muted"], font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 8))

        subjs = found.get("subjects", {})
        for subj in DEFAULT_SUBJECTS:
            score = subjs.get(subj, 0.0)
            grd = calculate_grade(score)
            s_row = tk.Frame(p, bg=self.theme["sidebar"], padx=12, pady=6)
            s_row.pack(fill="x", pady=2)

            tk.Label(s_row, text=subj, bg=self.theme["sidebar"],
                     fg=self.theme["text"], font=FONT_BOLD).pack(side="left")
            tk.Label(s_row, text=f"Grade {grd}  |  {score:.1f} / 100", bg=self.theme["sidebar"],
                     fg=self.theme["accent"], font=FONT_BOLD).pack(side="right")

        tk.Frame(p, bg=self.theme["border"], height=1).pack(fill="x", pady=(16, 12))

        # Overall summary
        pct = found.get("percentage", 0.0)
        tot = found.get("total_marks", 0.0)
        cgpa = found.get("cgpa", round(pct / 10.0, 2))
        grd = found.get("grade", calculate_grade(pct))

        summary_box = tk.Frame(p, bg=self.theme["card"])
        summary_box.pack(fill="x", pady=(0, 16))

        tk.Label(summary_box, text=f"Aggregate: {tot:.1f} / 500  •  {pct:.2f}%  •  Grade {grd}  •  CGPA: {cgpa:.2f}",
                 bg=self.theme["card"], fg=self.theme["text"], font=FONT_H1).pack(anchor="w")

        self.make_secondary_button(p, "Close", dlg.destroy).pack(side="right")

    def _delete_student(self):
        """Deletes selected student record."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Student", "Please select a student row to delete.")
            return

        row = self.tree.item(selected[0], "values")
        roll_no, name = row[0], row[1]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student record:\n\n{name} (Roll: {roll_no})?"):
            self.students = [s for s in self.students if str(s["roll_no"]) != str(roll_no)]
            save_students(self.students)
            self.show_admin_records()

    # =====================================================================
    # 8. ADMIN PAGE 3: ADD NEW STUDENT (WITH 5 SUBJECTS & LIVE PREVIEW)
    # =====================================================================
    def show_admin_add(self):
        """Form to register a new student with individual marks for 5 subjects."""
        self._clear_content()
        self._make_header("Add New Student", "Register student credentials and subject scores out of 100")

        # Outer card container
        card = tk.Frame(
            self.content,
            bg=self.theme["card"],
            padx=28,
            pady=24,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        card.pack(anchor="nw", fill="x", padx=(0, 20))
        card.columnconfigure(1, weight=1)

        # Section 1: Demographics
        tk.Label(card, text="1. STUDENT PROFILE", bg=self.theme["card"],
                 fg=self.theme["accent"], font=("Segoe UI", 9, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        self.e_roll   = self.make_form_row(card, "Roll Number",      1)
        self.e_name   = self.make_form_row(card, "Full Name",        2)
        self.e_age    = self.make_form_row(card, "Age (1-120)",      3)
        self.e_course = self.make_form_row(card, "Course / Stream",  4)

        # Section 2: Multi-Subject Marks
        tk.Label(card, text="2. SUBJECT SCORES (0 - 100)", bg=self.theme["card"],
                 fg=self.theme["accent"], font=("Segoe UI", 9, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", pady=(14, 8))

        self.subject_entries = {}
        for idx, subj in enumerate(DEFAULT_SUBJECTS):
            e = self.make_form_row(card, f"{subj} Marks", 6 + idx)
            e.bind("<KeyRelease>", lambda event: self._recalculate_add_preview())
            self.subject_entries[subj] = e

        # Live Calculation Preview Card
        self.preview_box = tk.Frame(card, bg=self.theme["sidebar"], padx=14, pady=10)
        self.preview_box.grid(row=6 + len(DEFAULT_SUBJECTS), column=0, columnspan=2, sticky="ew", pady=(16, 12))

        self.lbl_add_preview = tk.Label(
            self.preview_box,
            text="Aggregate: 0.0 / 500  |  Percentage: 0.00%  |  Grade: N/A  |  CGPA: 0.00",
            bg=self.theme["sidebar"],
            fg=self.theme["text"],
            font=FONT_BOLD
        )
        self.lbl_add_preview.pack(anchor="w")

        # Action Buttons
        btn_row = tk.Frame(card, bg=self.theme["card"])
        btn_row.grid(row=7 + len(DEFAULT_SUBJECTS), column=0, columnspan=2, sticky="w", pady=(12, 0))

        self.make_primary_button(btn_row, "Save Student Record", self._do_add).pack(side="left", padx=(0, 10))
        self.make_secondary_button(btn_row, "Clear Form", self._clear_add_form).pack(side="left")

    def _recalculate_add_preview(self):
        """Dynamically computes total, percentage, grade, and CGPA as marks are typed."""
        subjs = {}
        for subj, entry in self.subject_entries.items():
            val_str = entry.get().strip()
            try:
                subjs[subj] = float(val_str)
            except ValueError:
                subjs[subj] = 0.0

        stats = calculate_student_stats(subjs)
        self.lbl_add_preview.config(
            text=f"Aggregate: {stats['total_marks']:.1f} / 500  |  Percentage: {stats['percentage']:.2f}%  |  Grade: {stats['grade']} ({stats['remark']})  |  CGPA: {stats['cgpa']:.2f}"
        )

    def _clear_add_form(self):
        for entry in (self.e_roll, self.e_name, self.e_age, self.e_course):
            entry.delete(0, "end")
        for entry in self.subject_entries.values():
            entry.delete(0, "end")
        self._recalculate_add_preview()

    def _do_add(self):
        roll_no = self.e_roll.get().strip()
        name    = self.e_name.get().strip()
        course  = self.e_course.get().strip()

        if not roll_no or not name or not course:
            messagebox.showerror("Validation Error", "Roll number, name, and course are required fields.")
            return

        for s in self.students:
            if str(s["roll_no"]).strip() == roll_no:
                messagebox.showerror("Duplicate Roll Number", f"Roll number '{roll_no}' is already registered.")
                return

        try:
            age = int(self.e_age.get().strip())
            if age <= 0 or age > 120:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Age must be an integer between 1 and 120.")
            return

        # Validate subjects
        subjects = {}
        for subj, entry in self.subject_entries.items():
            val_str = entry.get().strip()
            if not val_str:
                messagebox.showerror("Missing Mark", f"Please enter marks for {subj}.")
                return
            try:
                val = float(val_str)
                if val < 0.0 or val > 100.0:
                    raise ValueError
                subjects[subj] = round(val, 2)
            except ValueError:
                messagebox.showerror("Invalid Marks", f"Marks for {subj} must be a number between 0 and 100.")
                return

        stats = calculate_student_stats(subjects)
        new_student = {
            "roll_no": roll_no,
            "name": name,
            "age": age,
            "course": course,
            "subjects": subjects,
            "total_marks": stats["total_marks"],
            "max_marks": stats["max_marks"],
            "percentage": stats["percentage"],
            "marks": stats["percentage"],
            "grade": stats["grade"],
            "cgpa": stats["cgpa"],
            "remark": stats["remark"],
            "status": stats["status"]
        }

        self.students.append(new_student)
        save_students(self.students)

        messagebox.showinfo("Success", f"Student '{name}' added successfully with Grade {stats['grade']}!")
        self._clear_add_form()
        self.show_admin_records()

    # =====================================================================
    # 9. ADMIN PAGE 4: UPDATE MARKS (MULTI-SUBJECT)
    # =====================================================================
    def show_admin_update(self):
        """Form to search student and update multi-subject marks."""
        self._clear_content()
        self._make_header("Update Student Marks", "Select or search student to modify multi-subject scores")

        search_bar = tk.Frame(self.content, bg=self.theme["bg"])
        search_bar.pack(anchor="w", pady=(0, 16))

        tk.Label(search_bar, text="Roll Number to Update:", bg=self.theme["bg"],
                 fg=self.theme["text_muted"], font=FONT_BODY).pack(side="left", padx=(0, 8))

        wrap, self.e_upd_search = self.make_input_entry(search_bar, width=20)
        wrap.pack(side="left", padx=(0, 10))
        self.e_upd_search.bind("<Return>", lambda e: self._load_student_for_update())

        self.make_primary_button(search_bar, "Load Record", self._load_student_for_update).pack(side="left")

        # Container for update form
        self.upd_card = tk.Frame(
            self.content,
            bg=self.theme["card"],
            padx=28,
            pady=24,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        self.upd_card.pack(anchor="nw", fill="x", padx=(0, 20))
        self.upd_card.columnconfigure(1, weight=1)

        tk.Label(
            self.upd_card,
            text="Enter a Roll Number above and click 'Load Record' to edit marks.",
            bg=self.theme["card"],
            fg=self.theme["text_muted"],
            font=FONT_BODY
        ).pack(anchor="w")

    def _load_student_for_update(self):
        """Finds student and populates edit fields for all 5 subjects."""
        roll = self.e_upd_search.get().strip()
        found = next((s for s in self.students if str(s["roll_no"]).strip() == roll), None)

        for child in self.upd_card.winfo_children():
            child.destroy()

        if not found:
            tk.Label(
                self.upd_card,
                text=f"No student record found with Roll Number '{roll}'.",
                bg=self.theme["card"],
                fg=self.theme["accent"],
                font=FONT_BOLD
            ).pack(anchor="w")
            return

        self.current_updating_student = found

        # Header info
        tk.Label(
            self.upd_card,
            text=f"Editing Marks for: {found['name'].title()} (Roll: {found['roll_no']})",
            bg=self.theme["card"],
            fg=self.theme["accent"],
            font=FONT_H1
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        subjs = found.get("subjects", {})
        self.upd_entries = {}

        for idx, subj in enumerate(DEFAULT_SUBJECTS):
            e = self.make_form_row(self.upd_card, f"{subj} Marks", 1 + idx)
            curr_val = subjs.get(subj, 0.0)
            e.insert(0, str(curr_val))
            e.bind("<KeyRelease>", lambda event: self._recalculate_upd_preview())
            self.upd_entries[subj] = e

        # Live calculation preview
        self.upd_preview_box = tk.Frame(self.upd_card, bg=self.theme["sidebar"], padx=14, pady=10)
        self.upd_preview_box.grid(row=1 + len(DEFAULT_SUBJECTS), column=0, columnspan=2, sticky="ew", pady=(16, 12))

        pct = found.get("percentage", 0.0)
        tot = found.get("total_marks", 0.0)
        grd = found.get("grade", calculate_grade(pct))
        cgpa = found.get("cgpa", round(pct / 10.0, 2))

        self.lbl_upd_preview = tk.Label(
            self.upd_preview_box,
            text=f"Aggregate: {tot:.1f} / 500  |  Percentage: {pct:.2f}%  |  Grade: {grd}  |  CGPA: {cgpa:.2f}",
            bg=self.theme["sidebar"],
            fg=self.theme["text"],
            font=FONT_BOLD
        )
        self.lbl_upd_preview.pack(anchor="w")

        btn_row = tk.Frame(self.upd_card, bg=self.theme["card"])
        btn_row.grid(row=2 + len(DEFAULT_SUBJECTS), column=0, columnspan=2, sticky="w", pady=(12, 0))

        self.make_primary_button(btn_row, "Save Updated Marks", self._do_save_update).pack(side="left")

    def _recalculate_upd_preview(self):
        """Dynamically computes preview for update form."""
        subjs = {}
        for subj, entry in self.upd_entries.items():
            val_str = entry.get().strip()
            try:
                subjs[subj] = float(val_str)
            except ValueError:
                subjs[subj] = 0.0

        stats = calculate_student_stats(subjs)
        self.lbl_upd_preview.config(
            text=f"Aggregate: {stats['total_marks']:.1f} / 500  |  Percentage: {stats['percentage']:.2f}%  |  Grade: {stats['grade']} ({stats['remark']})  |  CGPA: {stats['cgpa']:.2f}"
        )

    def _do_save_update(self):
        """Validates and saves modified multi-subject marks."""
        subjs = {}
        for subj, entry in self.upd_entries.items():
            val_str = entry.get().strip()
            try:
                val = float(val_str)
                if val < 0.0 or val > 100.0:
                    raise ValueError
                subjs[subj] = round(val, 2)
            except ValueError:
                messagebox.showerror("Invalid Marks", f"Marks for {subj} must be a number between 0 and 100.")
                return

        stats = calculate_student_stats(subjs)
        s = self.current_updating_student
        s["subjects"] = subjs
        s["total_marks"] = stats["total_marks"]
        s["max_marks"] = stats["max_marks"]
        s["percentage"] = stats["percentage"]
        s["marks"] = stats["percentage"]
        s["grade"] = stats["grade"]
        s["cgpa"] = stats["cgpa"]
        s["remark"] = stats["remark"]
        s["status"] = stats["status"]

        save_students(self.students)
        messagebox.showinfo(
            "Success",
            f"Marks for {s['name'].title()} updated successfully!\n\n"
            f"New Aggregate: {stats['total_marks']}/500\n"
            f"Percentage: {stats['percentage']}%\n"
            f"Grade: {stats['grade']} (CGPA: {stats['cgpa']})"
        )
        self.show_admin_records()

    # =====================================================================
    # 10. ADMIN PAGE 5: ACADEMIC INSIGHTS
    # =====================================================================
    def show_admin_insights(self):
        """Displays Honor roll, class difficulty benchmarks, and at-risk students."""
        self._clear_content()
        self.students = load_students()
        self._make_header("Academic Insights", "Cohort honor roll, subject toppers, and remedial intervention alerts")

        if not self.students:
            tk.Label(self.content, text="No student records available.",
                     bg=self.theme["bg"], fg=self.theme["text_muted"], font=FONT_BODY).pack()
            return

        insights = get_insights(self.students)
        top = insights["top_performer"]
        struggling = insights["struggling_students"]

        # Top Performer Card
        top_card = tk.Frame(
            self.content,
            bg=self.theme["card"],
            padx=24,
            pady=18,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        top_card.pack(fill="x", pady=(0, 16))

        tk.Label(top_card, text="🏆 COHORT TOP PERFORMER (RANK #1)", bg=self.theme["card"],
                 fg=self.theme["accent"], font=("Segoe UI", 9, "bold")).pack(anchor="w")

        if top:
            pct = float(top.get("percentage", top.get("marks", 0.0)))
            grd = top.get("grade", calculate_grade(pct))
            cgpa = top.get("cgpa", round(pct / 10.0, 2))
            tk.Label(
                top_card,
                text=f"{top['name'].title()}  •  {pct:.1f}% (Grade {grd}, CGPA: {cgpa:.2f})",
                bg=self.theme["card"],
                fg=self.theme["text"],
                font=FONT_H1
            ).pack(anchor="w", pady=(4, 2))
            tk.Label(
                top_card,
                text=f"Course: {top.get('course', 'General')}  |  Roll Number: {top['roll_no']}",
                bg=self.theme["card"],
                fg=self.theme["text_muted"],
                font=FONT_SMALL
            ).pack(anchor="w")

        # Subject Difficulty Benchmarks
        bench_row = tk.Frame(self.content, bg=self.theme["bg"])
        bench_row.pack(fill="x", pady=(0, 16))

        if insights.get("strongest_subject") and insights.get("toughest_subject"):
            b_card1 = tk.Frame(bench_row, bg=self.theme["card"], padx=18, pady=14,
                               highlightthickness=1, highlightbackground=self.theme["border"])
            b_card1.pack(side="left", fill="both", expand=True, padx=(0, 8))
            tk.Label(b_card1, text="🌟 HIGHEST PERFORMING SUBJECT", bg=self.theme["card"],
                     fg=self.theme["badge_maint"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
            tk.Label(b_card1, text=f"{insights['strongest_subject']['subject']} ({insights['strongest_subject']['average']}%)",
                     bg=self.theme["card"], fg=self.theme["text"], font=FONT_H1).pack(anchor="w", pady=(4, 0))

            b_card2 = tk.Frame(bench_row, bg=self.theme["card"], padx=18, pady=14,
                               highlightthickness=1, highlightbackground=self.theme["border"])
            b_card2.pack(side="left", fill="both", expand=True)
            tk.Label(b_card2, text="⚠️ TOUGHEST SUBJECT (LOWEST AVG)", bg=self.theme["card"],
                     fg=self.theme["badge_high"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
            tk.Label(b_card2, text=f"{insights['toughest_subject']['subject']} ({insights['toughest_subject']['average']}%)",
                     bg=self.theme["card"], fg=self.theme["text"], font=FONT_H1).pack(anchor="w", pady=(4, 0))

        # Subject Toppers List
        toppers_card = tk.Frame(
            self.content,
            bg=self.theme["card"],
            padx=24,
            pady=18,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        toppers_card.pack(fill="x", pady=(0, 16))

        tk.Label(toppers_card, text="🥇 SUBJECT-WISE TOP SCORERS", bg=self.theme["card"],
                 fg=self.theme["accent"], font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 10))

        for subj, info in insights.get("subject_toppers", {}).items():
            r = tk.Frame(toppers_card, bg=self.theme["sidebar"], padx=12, pady=6)
            r.pack(fill="x", pady=2)
            tk.Label(r, text=subj, bg=self.theme["sidebar"], fg=self.theme["text"], font=FONT_BOLD).pack(side="left")
            tk.Label(r, text=f"{info['student_name'].title()} (Roll {info['roll_no']}) — {info['score']}/100",
                     bg=self.theme["sidebar"], fg=self.theme["accent"], font=FONT_BOLD).pack(side="right")

        # Students Needing Support
        sup_card = tk.Frame(
            self.content,
            bg=self.theme["card"],
            padx=24,
            pady=18,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        sup_card.pack(fill="x")

        tk.Label(sup_card, text="🚨 ACADEMIC SUPPORT REQUIRED (Failed Subject or <40% Aggregate)",
                 bg=self.theme["card"], fg=self.theme["accent"], font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 8))

        if not struggling:
            tk.Label(sup_card, text="✓ Outstanding! All students are currently meeting passing criteria across all subjects.",
                     bg=self.theme["card"], fg=self.theme["text"], font=FONT_BODY).pack(anchor="w")
        else:
            for item in struggling:
                s = item["student"]
                pct = item["percentage"]
                failed_str = ", ".join(item["failed_subjects"]) if item["failed_subjects"] else "Aggregate < 40%"
                row = tk.Frame(sup_card, bg=self.theme["card"])
                row.pack(anchor="w", pady=3)
                tk.Label(row, text="•", bg=self.theme["card"], fg=self.theme["accent"], font=FONT_BOLD).pack(side="left", padx=(0, 6))
                tk.Label(row, text=f"{s['name'].title()} (Roll {s['roll_no']}) — {pct:.1f}% [{failed_str}]",
                         bg=self.theme["card"], fg=self.theme["text"], font=FONT_BODY).pack(side="left")

    # =====================================================================
    # 11. STUDENT PORTAL LAYOUT & NAVIGATION
    # =====================================================================
    def _build_student_layout(self):
        """Constructs Student Sidebar and Student Content Area."""
        self._clear_window()
        student = self.session["user"]

        # 1. Left Sidebar
        self.sidebar = tk.Frame(self, bg=self.theme["sidebar"], width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand Header
        brand_box = tk.Frame(self.sidebar, bg=self.theme["sidebar"], padx=18, pady=20)
        brand_box.pack(fill="x")

        badge = tk.Frame(brand_box, bg=self.theme["accent"], padx=9, pady=3)
        badge.pack(anchor="w", pady=(0, 8))
        tk.Label(
            badge,
            text="● STUDENT PORTAL",
            bg=self.theme["accent"],
            fg="#FCF8F9",
            font=("Segoe UI", 8, "bold")
        ).pack()

        tk.Label(
            brand_box,
            text=student["name"].title(),
            bg=self.theme["sidebar"],
            fg=self.theme["text"],
            font=FONT_H1,
            anchor="w"
        ).pack(anchor="w")

        tk.Label(
            brand_box,
            text=f"Roll No: {student['roll_no']}  •  {student.get('course', 'AI & DS')}",
            bg=self.theme["sidebar"],
            fg=self.theme["text_muted"],
            font=FONT_SMALL,
            anchor="w"
        ).pack(anchor="w")

        tk.Frame(self.sidebar, bg=self.theme["border"], height=1).pack(fill="x", padx=16, pady=10)

        # Student Nav Menu
        student_menu = [
            ("👤 Academic Overview",        "student_overview", self.show_student_overview),
            ("📊 Subject Performance",      "student_subjects", self.show_student_subjects),
            ("🤖 Study Plan & Assistance", "student_planner",  self.show_student_planner),
        ]

        self.student_nav_buttons = {}
        for title, key, cmd in student_menu:
            is_active = (self.current_page == key)
            btn = tk.Button(
                self.sidebar,
                text=f"  {title}",
                command=lambda c=cmd, k=key: self._switch_student_page(c, k),
                bg=self.theme["accent"] if is_active else self.theme["sidebar"],
                fg="#FCF8F9" if is_active else self.theme["text_muted"],
                activebackground=self.theme["card_hover"],
                activeforeground=self.theme["text"],
                font=FONT_BOLD if is_active else FONT_BODY,
                relief="flat",
                anchor="w",
                padx=16,
                pady=11,
                cursor="hand2",
                bd=0
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.student_nav_buttons[key] = btn

        # Sidebar Bottom Controls
        bottom_box = tk.Frame(self.sidebar, bg=self.theme["card"], padx=12, pady=12)
        bottom_box.pack(side="bottom", fill="x", padx=12, pady=16)

        theme_text = "🌙 Dark Mode" if self.theme["name"] == "light" else "☀️ Light Mode"
        self.make_secondary_button(bottom_box, theme_text, self.toggle_theme).pack(fill="x", pady=(0, 6))
        self.make_secondary_button(bottom_box, "🚪 Sign Out", self.logout).pack(fill="x")

        # 2. Main Scrollable Content Area
        self.scroll_area = ScrollableFrame(self, self.theme["bg"])
        self.scroll_area.pack(side="left", fill="both", expand=True, padx=24, pady=20)
        self.content = self.scroll_area.content

        # Route page
        if self.current_page == "student_overview":
            self.show_student_overview()
        elif self.current_page == "student_subjects":
            self.show_student_subjects()
        else:
            self.show_student_planner()

    def _switch_student_page(self, command, page_key):
        """Navigates to chosen student portal page and updates active menu style."""
        self.current_page = page_key
        for key, btn in self.student_nav_buttons.items():
            if key == page_key:
                btn.config(bg=self.theme["accent"], fg="#FCF8F9", font=FONT_BOLD)
            else:
                btn.config(bg=self.theme["sidebar"], fg=self.theme["text_muted"], font=FONT_BODY)
        command()

    # =====================================================================
    # 12. STUDENT PAGE 1: ACADEMIC OVERVIEW & PROFILE CARD
    # =====================================================================
    def show_student_overview(self):
        """Displays personalized student profile hero card and core KPI cards."""
        self._clear_content()
        student = self.session["user"]
        self._make_header(
            "My Academic Profile",
            f"Personalized performance summary and academic standing for {student['name'].title()}"
        )

        # Profile Hero Card
        hero = tk.Frame(
            self.content,
            bg=self.theme["card"],
            padx=28,
            pady=22,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        hero.pack(fill="x", pady=(0, 16))

        hero_top = tk.Frame(hero, bg=self.theme["card"])
        hero_top.pack(fill="x")

        avatar_badge = tk.Frame(hero_top, bg=self.theme["accent"], padx=14, pady=8)
        avatar_badge.pack(side="left", padx=(0, 16))
        tk.Label(
            avatar_badge,
            text=student["name"][:2].upper(),
            bg=self.theme["accent"],
            fg="#FCF8F9",
            font=("Segoe UI", 16, "bold")
        ).pack()

        info_box = tk.Frame(hero_top, bg=self.theme["card"])
        info_box.pack(side="left", fill="x", expand=True)

        tk.Label(info_box, text=student["name"].title(), bg=self.theme["card"],
                 fg=self.theme["text"], font=FONT_TITLE).pack(anchor="w")
        tk.Label(
            info_box,
            text=f"Roll Number: {student['roll_no']}   |   Course: {student.get('course', 'AI & DS')}   |   Age: {student.get('age', 20)} years",
            bg=self.theme["card"],
            fg=self.theme["text_muted"],
            font=FONT_BODY
        ).pack(anchor="w", pady=(2, 0))

        # Status badge on right
        pct = float(student.get("percentage", student.get("marks", 0.0)))
        status_text = "Good Standing" if pct >= 60 else ("Passing" if pct >= 40 else "Academic Support Needed")
        status_color = self.theme["badge_maint"] if pct >= 60 else (self.theme["badge_med"] if pct >= 40 else self.theme["badge_high"])

        status_badge = tk.Frame(hero_top, bg=status_color, padx=12, pady=5)
        status_badge.pack(side="right")
        tk.Label(status_badge, text=status_text, bg=status_color, fg="#FFFFFF", font=FONT_BOLD).pack()

        # Row of 4 Core KPI Stat Cards
        kpi_row = tk.Frame(self.content, bg=self.theme["bg"])
        kpi_row.pack(fill="x", pady=(0, 16))

        tot = student.get("total_marks", pct * 5.0)
        grd = student.get("grade", calculate_grade(pct))
        cgpa = student.get("cgpa", round(pct / 10.0, 2))
        remark = student.get("remark", get_grade_remark(grd))

        # Rank calculation in class
        all_students = load_students()
        sorted_by_pct = sorted(all_students, key=lambda s: float(s.get("percentage", s.get("marks", 0.0))), reverse=True)
        rank = 1
        for idx, s in enumerate(sorted_by_pct):
            if str(s["roll_no"]) == str(student["roll_no"]):
                rank = idx + 1
                break

        kpi_cards = [
            ("Overall Percentage", f"{pct:.2f}%"),
            ("Final Grade",        f"{grd} ({remark})"),
            ("CGPA (10.0 Scale)",  f"{cgpa:.2f}"),
            ("Total Aggregate",    f"{tot:.0f} / 500"),
            ("Class Rank",         f"#{rank} of {len(all_students)}")
        ]

        for i, (label, val) in enumerate(kpi_cards):
            c = tk.Frame(
                kpi_row,
                bg=self.theme["card"],
                padx=14,
                pady=12,
                highlightthickness=1,
                highlightbackground=self.theme["border"]
            )
            c.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 8, 0))

            tk.Label(c, text=label, bg=self.theme["card"],
                     fg=self.theme["text_muted"], font=FONT_SMALL).pack(anchor="w")
            c_color = self.theme["accent"] if label in ("Overall Percentage", "Class Rank") else self.theme["text"]
            tk.Label(c, text=val, bg=self.theme["card"],
                     fg=c_color, font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(4, 0))

        # Quick Performance Highlight Card
        prof = generate_study_profile(student)
        hl_card = tk.Frame(
            self.content,
            bg=self.theme["card"],
            padx=24,
            pady=20,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        hl_card.pack(fill="x", pady=(0, 16))

        tk.Label(hl_card, text="🎯 ACADEMIC HIGHLIGHTS & SUMMARY", bg=self.theme["card"],
                 fg=self.theme["accent"], font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 10))

        str_sub = prof["top_strength"]
        weak_sub = prof["top_weakness"]

        tk.Label(
            hl_card,
            text=f"• Top Performing Subject: {str_sub['subject']} with {str_sub['marks']:.1f}/100 ({str_sub['grade']}) — {str_sub['status_label']}",
            bg=self.theme["card"],
            fg=self.theme["text"],
            font=FONT_BODY
        ).pack(anchor="w", pady=2)

        tk.Label(
            hl_card,
            text=f"• Key Growth Area: {weak_sub['subject']} with {weak_sub['marks']:.1f}/100 ({weak_sub['grade']}) — {weak_sub['status_label']}",
            bg=self.theme["card"],
            fg=self.theme["text"],
            font=FONT_BODY
        ).pack(anchor="w", pady=2)

        tk.Label(
            hl_card,
            text=f"• Recommended Adaptive Study: {prof['total_weekly_hours']:.1f} hours/week across all 5 subjects.",
            bg=self.theme["card"],
            fg=self.theme["text_muted"],
            font=FONT_BODY
        ).pack(anchor="w", pady=(4, 0))

    # =====================================================================
    # 13. STUDENT PAGE 2: SUBJECT PERFORMANCE & CLASS COMPARISON
    # =====================================================================
    def show_student_subjects(self):
        """Displays subject-wise breakdown, progress indicators, and comparative charts."""
        self._clear_content()
        student = self.session["user"]
        self._make_header(
            "Subject Performance & Benchmarks",
            "Individual subject scores compared directly against the class average"
        )

        all_students = load_students()
        analytics = calculate_analytics(all_students)
        subject_stats = analytics.get("subject_stats", {})

        subjs = student.get("subjects", {})

        # 5 Subject Progress Cards Container
        cards_frame = tk.Frame(self.content, bg=self.theme["bg"])
        cards_frame.pack(fill="x", pady=(0, 16))

        for subj in DEFAULT_SUBJECTS:
            my_score = float(subjs.get(subj, 0.0))
            class_avg = subject_stats.get(subj, {}).get("average", 0.0)
            diff = my_score - class_avg

            card = tk.Frame(
                cards_frame,
                bg=self.theme["card"],
                padx=16,
                pady=14,
                highlightthickness=1,
                highlightbackground=self.theme["border"]
            )
            card.pack(fill="x", pady=4)

            # Top Row: Subject Title + Score
            top_row = tk.Frame(card, bg=self.theme["card"])
            top_row.pack(fill="x")

            tk.Label(top_row, text=subj, bg=self.theme["card"],
                     fg=self.theme["text"], font=FONT_H1).pack(side="left")

            grd = calculate_grade(my_score)
            tk.Label(top_row, text=f"{my_score:.1f} / 100  (Grade {grd})", bg=self.theme["card"],
                     fg=self.theme["accent"], font=FONT_H1).pack(side="right")

            # Middle Row: Visual Custom Progress Bar
            progress_bg = tk.Frame(card, bg=self.theme["sidebar"], height=10)
            progress_bg.pack(fill="x", pady=8)
            progress_bg.pack_propagate(False)

            fill_ratio = max(0.01, min(1.0, my_score / 100.0))
            bar_color = self.theme["badge_maint"] if my_score >= 80 else (self.theme["badge_med"] if my_score >= 60 else self.theme["badge_high"])
            progress_fill = tk.Frame(progress_bg, bg=bar_color, height=10)
            progress_fill.place(relx=0, rely=0, relwidth=fill_ratio, relheight=1.0)

            # Bottom Row: Class Comparison metric
            bot_row = tk.Frame(card, bg=self.theme["card"])
            bot_row.pack(fill="x")

            diff_str = f"+{diff:.1f}% above class average" if diff >= 0 else f"{diff:.1f}% below class average"
            diff_color = self.theme["badge_maint"] if diff >= 0 else self.theme["badge_high"]

            tk.Label(bot_row, text=f"Class Average: {class_avg:.1f}%", bg=self.theme["card"],
                     fg=self.theme["text_muted"], font=FONT_SMALL).pack(side="left")
            tk.Label(bot_row, text=diff_str, bg=self.theme["card"],
                     fg=diff_color, font=FONT_BOLD).pack(side="right")

        # Matplotlib Comparative Grouped Bar Chart
        chart_box = tk.Frame(
            self.content,
            bg=self.theme["card"],
            padx=12,
            pady=12,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        chart_box.pack(fill="both", expand=True, pady=(0, 16))

        fig = Figure(figsize=(9.6, 4.0), facecolor=self.theme["chart_bg"], dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor(self.theme["chart_plot"])

        subjects = DEFAULT_SUBJECTS
        short_names = ["Math", "Python", "Prof Skills", "DBMS", "DSD"]
        my_scores = [float(subjs.get(s, 0.0)) for s in subjects]
        class_avgs = [subject_stats.get(s, {}).get("average", 0.0) for s in subjects]

        import numpy as np
        indices = np.arange(len(subjects))
        width = 0.35

        bars1 = ax.bar(indices - width/2, my_scores, width=width,
                       color=self.theme["chart_bar"], label="My Score", edgecolor=self.theme["border"])
        bars2 = ax.bar(indices + width/2, class_avgs, width=width,
                       color=self.theme["chart_bar_alt"], label="Class Average", edgecolor=self.theme["border"])

        # Add annotations
        for bar in bars1:
            ax.annotate(f"{bar.get_height():.0f}",
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                        color=self.theme["text"], fontsize=8, fontweight="bold")

        for bar in bars2:
            ax.annotate(f"{bar.get_height():.0f}",
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                        color=self.theme["text_muted"], fontsize=8)

        ax.set_xticks(indices)
        ax.set_xticklabels(short_names, fontsize=8.5, color=self.theme["text"])
        ax.set_ylim(0, 115)
        ax.set_ylabel("Score (0 - 100)", color=self.theme["text_muted"], fontsize=8.5)
        ax.set_title("Comparative Analysis: My Score vs. Class Benchmark", color=self.theme["accent"], fontsize=11, fontweight="bold", pad=8)
        ax.axhline(40, color=self.theme["text_muted"], linestyle="--", linewidth=1.0, alpha=0.7)

        for spine in ax.spines.values():
            spine.set_color(self.theme["chart_border"])
        ax.grid(axis="y", color=self.theme["chart_border"], linestyle=":", alpha=0.6)
        ax.legend(facecolor=self.theme["card"], edgecolor=self.theme["chart_border"],
                  labelcolor=self.theme["text"], fontsize=8, loc="upper right")
        fig.tight_layout(pad=1.8)

        self.chart_canvas = FigureCanvasTkAgg(fig, master=chart_box)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Strengths & Weaknesses Breakdown Cards
        prof = generate_study_profile(student)
        sw_row = tk.Frame(self.content, bg=self.theme["bg"])
        sw_row.pack(fill="x")

        # Strength Card
        s_card = tk.Frame(sw_row, bg=self.theme["card"], padx=18, pady=16,
                          highlightthickness=1, highlightbackground=self.theme["border"])
        s_card.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(s_card, text="🌟 TOP ACADEMIC STRENGTH", bg=self.theme["card"],
                 fg=self.theme["badge_maint"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        str_item = prof["top_strength"]
        tk.Label(s_card, text=f"{str_item['subject']} ({str_item['marks']:.1f}/100)",
                 bg=self.theme["card"], fg=self.theme["text"], font=FONT_H1).pack(anchor="w", pady=(4, 2))
        tk.Label(s_card, text=str_item["action_title"], bg=self.theme["card"],
                 fg=self.theme["text_muted"], font=FONT_SMALL).pack(anchor="w")

        # Weakness Card
        w_card = tk.Frame(sw_row, bg=self.theme["card"], padx=18, pady=16,
                          highlightthickness=1, highlightbackground=self.theme["border"])
        w_card.pack(side="left", fill="both", expand=True)

        tk.Label(w_card, text="🎯 PRIORITY FOCUS AREA", bg=self.theme["card"],
                 fg=self.theme["badge_high"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        weak_item = prof["top_weakness"]
        tk.Label(w_card, text=f"{weak_item['subject']} ({weak_item['marks']:.1f}/100)",
                 bg=self.theme["card"], fg=self.theme["text"], font=FONT_H1).pack(anchor="w", pady=(4, 2))
        tk.Label(w_card, text=weak_item["action_title"], bg=self.theme["card"],
                 fg=self.theme["text_muted"], font=FONT_SMALL).pack(anchor="w")

    # =====================================================================
    # 14. STUDENT PAGE 3: AI STUDY ASSISTANT & ADAPTIVE WEEKLY TIMETABLE
    # =====================================================================
    def show_student_planner(self):
        """Displays AI recommendations, priority categorization, and weekly schedule."""
        self._clear_content()
        student = self.session["user"]
        self._make_header(
            "AI-Driven Study Assistant",
            "Personalized subject priority ranking, study allocations, and adaptive weekly schedule"
        )

        study_profile = generate_study_profile(student)
        analyses = study_profile["analyses"]
        timetable = study_profile["weekly_schedule"]

        # Priority Counts KPI Bar
        kpi_row = tk.Frame(self.content, bg=self.theme["bg"])
        kpi_row.pack(fill="x", pady=(0, 16))

        p_counts = study_profile["priority_counts"]
        boxes = [
            ("Recommended Study Load", f"{study_profile['total_weekly_hours']:.1f} hrs/week", self.theme["text"]),
            ("High Priority (<60%)",   f"{p_counts['High Priority']} Subject(s)", self.theme["badge_high"]),
            ("Medium Priority (60-79%)", f"{p_counts['Medium Priority']} Subject(s)", self.theme["badge_med"]),
            ("Maintenance (≥80%)",     f"{p_counts['Maintenance']} Subject(s)", self.theme["badge_maint"]),
        ]

        for i, (label, val, val_color) in enumerate(boxes):
            c = tk.Frame(
                kpi_row,
                bg=self.theme["card"],
                padx=14,
                pady=12,
                highlightthickness=1,
                highlightbackground=self.theme["border"]
            )
            c.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 8, 0))

            tk.Label(c, text=label, bg=self.theme["card"],
                     fg=self.theme["text_muted"], font=FONT_SMALL).pack(anchor="w")
            tk.Label(c, text=val, bg=self.theme["card"],
                     fg=val_color, font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(4, 0))

        # Section 1: Subject Action Recommendations Cards
        tk.Label(self.content, text="SUBJECT PRIORITY ACTION PLANS:", bg=self.theme["bg"],
                 fg=self.theme["accent"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 8))

        for item in study_profile["sorted_by_priority"]:
            card = tk.Frame(
                self.content,
                bg=self.theme["card"],
                padx=20,
                pady=16,
                highlightthickness=1,
                highlightbackground=self.theme["border"]
            )
            card.pack(fill="x", pady=4)

            top = tk.Frame(card, bg=self.theme["card"])
            top.pack(fill="x")

            # Left: Subject and Current Score
            tk.Label(top, text=item["subject"], bg=self.theme["card"],
                     fg=self.theme["text"], font=FONT_H1).pack(side="left")
            tk.Label(top, text=f"• Current Score: {item['marks']:.1f}% ({item['grade']})",
                     bg=self.theme["card"], fg=self.theme["text_muted"], font=FONT_BODY).pack(side="left", padx=(10, 0))

            # Right: Priority Badge
            p_badge = tk.Frame(top, bg=item["badge_color"], padx=10, pady=3)
            p_badge.pack(side="right")
            tk.Label(p_badge, text=item["priority"].upper(), bg=item["badge_color"],
                     fg="#FFFFFF", font=("Segoe UI", 8, "bold")).pack()

            # Recommendation text
            tk.Label(
                card,
                text=f"Allocation: {item['weekly_hours']}   |   Focus: {item['action_title']}",
                bg=self.theme["card"],
                fg=item["badge_color"],
                font=FONT_BOLD
            ).pack(anchor="w", pady=(8, 2))

            tk.Label(
                card,
                text=f"Strategy: {item['strategy']}",
                bg=self.theme["card"],
                fg=self.theme["text"],
                font=FONT_BODY
            ).pack(anchor="w")

            tk.Label(
                card,
                text=f"Actionable Roadmap: {item['recommendation']}",
                bg=self.theme["card"],
                fg=self.theme["text_muted"],
                font=FONT_SMALL,
                wraplength=900,
                justify="left"
            ).pack(anchor="w", pady=(2, 0))

        # Section 2: Weekly Study Timetable Grid Widget
        tk.Label(
            self.content,
            text="ADAPTIVE WEEKLY STUDY TIMETABLE (MONDAY – SUNDAY):",
            bg=self.theme["bg"],
            fg=self.theme["accent"],
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(18, 8))

        timetable_box = tk.Frame(
            self.content,
            bg=self.theme["card"],
            padx=16,
            pady=16,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        timetable_box.pack(fill="x", pady=(0, 20))

        # Table Header
        h_row = tk.Frame(timetable_box, bg=self.theme["sidebar"], padx=10, pady=8)
        h_row.pack(fill="x", pady=(0, 4))
        tk.Label(h_row, text="Day", width=12, anchor="w", bg=self.theme["sidebar"], fg=self.theme["accent"], font=FONT_BOLD).pack(side="left")
        tk.Label(h_row, text="Time Slot", width=22, anchor="w", bg=self.theme["sidebar"], fg=self.theme["accent"], font=FONT_BOLD).pack(side="left")
        tk.Label(h_row, text="Primary Focus Subject", width=24, anchor="w", bg=self.theme["sidebar"], fg=self.theme["accent"], font=FONT_BOLD).pack(side="left")
        tk.Label(h_row, text="Session Objective & Study Task", anchor="w", bg=self.theme["sidebar"], fg=self.theme["accent"], font=FONT_BOLD).pack(side="left", fill="x", expand=True)

        # 7 Days Rows
        for day_plan in timetable:
            row = tk.Frame(timetable_box, bg=self.theme["card"], padx=10, pady=7)
            row.pack(fill="x", pady=2)

            # Day
            tk.Label(row, text=day_plan["day"], width=12, anchor="w",
                     bg=self.theme["card"], fg=self.theme["text"], font=FONT_BOLD).pack(side="left")

            # Time Slot
            tk.Label(row, text=day_plan["session_time"], width=22, anchor="w",
                     bg=self.theme["card"], fg=self.theme["text_muted"], font=FONT_SMALL).pack(side="left")

            # Primary Subject
            p_color = self.theme["badge_high"] if day_plan["priority_tag"] == "High Priority" else (self.theme["badge_med"] if day_plan["priority_tag"] == "Medium Priority" else self.theme["badge_maint"])
            subj_lbl = tk.Label(row, text=day_plan["primary_subject"], width=24, anchor="w",
                                bg=self.theme["card"], fg=p_color, font=FONT_BOLD)
            subj_lbl.pack(side="left")

            # Task Objective
            tk.Label(row, text=day_plan["task_objective"], anchor="w",
                     bg=self.theme["card"], fg=self.theme["text"], font=FONT_SMALL).pack(side="left", fill="x", expand=True)


# =====================================================================
# START APPLICATION
# =====================================================================
if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()

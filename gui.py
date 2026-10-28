"""
gui.py - Modern Graphical User Interface for Student Management System.
Features:
  - Exact custom color palette inspired by modern UI design:
      * Base Canvas / Obsidian Dark : #162311
      * Vibrant Electric Crimson    : #FF2A54
      * Soft Light Ivory / White    : #FFF9F9
  - Full Class Performance Dashboard with multiple embedded interactive graphs:
      * Overview Dual View (Bar & Donut side-by-side)
      * Individual Student Marks (Bar Chart)
      * Letter Grade Distribution (Donut Chart)
      * Course-wise Average Performance (Bar Chart)
      * Score Range Distribution (Histogram / Bracket Chart)
  - Student Records Table with real-time search, sorting, and deletion
  - Add Student, Search Student, and Update Marks workflows
  - Academic Performance Insights
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from storage import load_students, save_students
from analytics import calculate_analytics
from insights import get_insights
from grade_calculator import calculate_grade, get_grade_remark


# ==============================================================================
# COLOR PALETTE SPECIFICATION
# (Directly calibrated to: #FFF9F9 ivory, #FF2A54 crimson, #162311 obsidian)
# ==============================================================================
COLOR_BG            = "#162311"   # Base dark canvas (obsidian olive)
COLOR_SIDEBAR       = "#0F1A0C"   # Deep sidebar surface
COLOR_SURFACE       = "#1D2D18"   # Primary elevated card surface
COLOR_SURFACE_ALT   = "#25381E"   # Secondary card surface / table alternate
COLOR_SURFACE_INPUT = "#131C0E"   # Input field background
COLOR_BORDER        = "#2E4226"   # Card & separator border lines
COLOR_BORDER_FOCUS  = "#FF2A54"   # Active input border

COLOR_ACCENT        = "#FF2A54"   # Vibrant electric coral crimson
COLOR_ACCENT_HOVER  = "#FF4D71"   # Lighter crimson for hover states
COLOR_ACCENT_MUTED  = "#3E1721"   # Deep crimson tint for pill badges
COLOR_ACCENT_TEXT   = "#FFA3B5"   # Soft pink for secondary accent text

COLOR_TEXT          = "#FFF9F9"   # Primary text (crisp warm ivory white)
COLOR_TEXT_MUTED    = "#A1B39F"   # Secondary / muted sage text
COLOR_TEXT_DIM      = "#6B7E69"   # Subtle placeholder / dim text

COLOR_SUCCESS       = "#4ADE80"   # Success green (Passing)
COLOR_DANGER        = "#FF2A54"   # Danger / Failure crimson
COLOR_WARNING       = "#FBBF24"   # Warning amber
COLOR_INFO          = "#60A5FA"   # Info blue

# Typography presets
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_H1    = ("Segoe UI", 14, "bold")
FONT_H2    = ("Segoe UI", 12, "bold")
FONT_BODY  = ("Segoe UI", 10)
FONT_BOLD  = ("Segoe UI", 10, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO  = ("Consolas", 10)


# ==============================================================================
# REUSABLE UI WIDGET HELPERS
# ==============================================================================
def create_entry(parent, width=28, **kwargs):
    """Create a styled, modern entry widget with custom border and colors."""
    container = tk.Frame(parent, bg=COLOR_BORDER, padx=1, pady=1)
    entry = tk.Entry(
        container,
        bg=COLOR_SURFACE_INPUT,
        fg=COLOR_TEXT,
        insertbackground=COLOR_TEXT,
        relief="flat",
        font=FONT_BODY,
        bd=0,
        width=width,
        **kwargs
    )
    entry.pack(fill="both", expand=True, padx=6, pady=6)

    # Focus animation effects
    entry.bind("<FocusIn>",  lambda e: container.config(bg=COLOR_ACCENT))
    entry.bind("<FocusOut>", lambda e: container.config(bg=COLOR_BORDER))
    return container, entry


def create_button(parent, text, command, bg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
                  fg_color="#FFFFFF", width=None, icon=""):
    """Create a modern pill-like button with smooth hover feedback."""
    display_text = f"{icon} {text}".strip() if icon else text
    btn = tk.Button(
        parent,
        text=display_text,
        command=command,
        bg=bg_color,
        fg=fg_color,
        activebackground=hover_color,
        activeforeground=fg_color,
        relief="flat",
        cursor="hand2",
        font=FONT_BOLD,
        padx=14,
        pady=7,
        bd=0,
        width=width
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
    return btn


def create_form_row(parent, label_text, row_idx):
    """Build a labeled form row with consistent padding and alignment."""
    lbl = tk.Label(
        parent,
        text=label_text,
        bg=COLOR_SURFACE,
        fg=COLOR_TEXT_MUTED,
        font=FONT_BODY,
        anchor="w"
    )
    lbl.grid(row=row_idx, column=0, sticky="w", padx=(0, 16), pady=8)

    wrap, entry = create_entry(parent, width=32)
    wrap.grid(row=row_idx, column=1, sticky="ew", pady=8)
    return entry


# ==============================================================================
# MAIN APPLICATION WINDOW
# ==============================================================================
class StudentApp(tk.Tk):
    """Main desktop application window for the Student Management System."""

    def __init__(self):
        super().__init__()
        self.title("Student Management System • Analytics Dashboard")
        self.geometry("1120x720")
        self.minsize(980, 620)
        self.configure(bg=COLOR_BG)

        # Application state
        self.students = load_students()
        self.active_nav_btn = None
        self.current_graph_mode = "dual"  # "dual", "bar", "donut", "course", "brackets"
        self.chart_canvas = None

        self._configure_styles()
        self._build_shell()

    # ── THEME & STYLE SYSTEM ──────────────────────────────────────────────────
    def _configure_styles(self):
        """Configure ttk styles for treeviews and scrollbars."""
        style = ttk.Style(self)
        style.theme_use("clam")

        # Treeview styling
        style.configure(
            "Modern.Treeview",
            background=COLOR_SURFACE,
            foreground=COLOR_TEXT,
            fieldbackground=COLOR_SURFACE,
            rowheight=32,
            font=FONT_BODY,
            borderwidth=0
        )
        style.configure(
            "Modern.Treeview.Heading",
            background=COLOR_SIDEBAR,
            foreground=COLOR_TEXT,
            font=FONT_BOLD,
            relief="flat",
            padding=(6, 8)
        )
        style.map(
            "Modern.Treeview",
            background=[("selected", COLOR_ACCENT)],
            foreground=[("selected", "#FFFFFF")]
        )
        style.map(
            "Modern.Treeview.Heading",
            background=[("active", COLOR_SURFACE_ALT)]
        )

        # Clean scrollbar
        style.configure(
            "Modern.Vertical.TScrollbar",
            background=COLOR_SURFACE_ALT,
            troughcolor=COLOR_SIDEBAR,
            borderwidth=0,
            arrowsize=12
        )

    # ── BASE LAYOUT SHELL ─────────────────────────────────────────────────────
    def _build_shell(self):
        """Build the permanent sidebar and dynamic main content container."""
        # ── Sidebar ──
        self.sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=225)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand header
        brand_frame = tk.Frame(self.sidebar, bg=COLOR_SIDEBAR, padx=16, pady=20)
        brand_frame.pack(fill="x")

        # Logo pill badge
        pill_badge = tk.Frame(brand_frame, bg=COLOR_ACCENT_MUTED, padx=10, pady=4)
        pill_badge.pack(anchor="w", pady=(0, 8))
        tk.Label(
            pill_badge,
            text="● ACADEMIC SUITE",
            bg=COLOR_ACCENT_MUTED,
            fg=COLOR_ACCENT,
            font=("Segoe UI", 8, "bold")
        ).pack()

        tk.Label(
            brand_frame,
            text="Student Hub",
            bg=COLOR_SIDEBAR,
            fg=COLOR_TEXT,
            font=FONT_TITLE,
            anchor="w"
        ).pack(anchor="w")

        tk.Label(
            brand_frame,
            text="Records & Analytics",
            bg=COLOR_SIDEBAR,
            fg=COLOR_TEXT_MUTED,
            font=FONT_SMALL,
            anchor="w"
        ).pack(anchor="w")

        tk.Frame(self.sidebar, bg=COLOR_BORDER, height=1).pack(fill="x", padx=16, pady=(12, 16))

        # Navigation menu items
        nav_items = [
            ("📊 Dashboard & Graphs", self.show_dashboard),
            ("📋 Student Records",    self.show_view),
            ("➕ Add Student",        self.show_add),
            ("🔍 Search Student",     self.show_search),
            ("✏️ Update Marks",       self.show_update),
            ("💡 Academic Insights",  self.show_insights),
        ]

        self.nav_buttons = {}
        for text, cmd in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=f"  {text}",
                command=lambda c=cmd, t=text: self._navigate(c, t),
                bg=COLOR_SIDEBAR,
                fg=COLOR_TEXT_MUTED,
                activebackground=COLOR_SURFACE,
                activeforeground=COLOR_TEXT,
                relief="flat",
                anchor="w",
                padx=16,
                pady=11,
                font=FONT_BODY,
                cursor="hand2",
                bd=0
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.nav_buttons[text] = btn

        # Sidebar footer (system statistics summary)
        self.footer_frame = tk.Frame(self.sidebar, bg=COLOR_SURFACE, padx=12, pady=12)
        self.footer_frame.pack(side="bottom", fill="x", padx=12, pady=16)

        self.footer_lbl = tk.Label(
            self.footer_frame,
            text=f"Enrolled: {len(self.students)} students",
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT,
            font=FONT_SMALL
        )
        self.footer_lbl.pack(anchor="w")

        status_row = tk.Frame(self.footer_frame, bg=COLOR_SURFACE)
        status_row.pack(anchor="w", pady=(4, 0))
        tk.Label(status_row, text="●", bg=COLOR_SURFACE, fg=COLOR_SUCCESS, font=("Segoe UI", 8)).pack(side="left")
        tk.Label(status_row, text=" Database Active", bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, font=FONT_SMALL).pack(side="left")

        # ── Main Content Container ──
        self.content = tk.Frame(self, bg=COLOR_BG)
        self.content.pack(side="left", fill="both", expand=True, padx=24, pady=24)

        # Show Dashboard as default landing page with rich graphs
        self._navigate(self.show_dashboard, "📊 Dashboard & Graphs")

    def _navigate(self, command, nav_key):
        """Handle sidebar navigation state and button active styling."""
        for name, btn in self.nav_buttons.items():
            if name == nav_key:
                btn.config(bg=COLOR_ACCENT, fg="#FFFFFF", font=FONT_BOLD)
            else:
                btn.config(bg=COLOR_SIDEBAR, fg=COLOR_TEXT_MUTED, font=FONT_BODY)
        command()

    def _clear_content(self):
        """Clear dynamic content widgets safely and release matplotlib resources."""
        if self.chart_canvas:
            try:
                self.chart_canvas.get_tk_widget().destroy()
            except Exception:
                pass
            self.chart_canvas = None

        for widget in self.content.winfo_children():
            widget.destroy()

    def _page_header(self, title, subtitle="", action_btn_text=None, action_cmd=None):
        """Build a standardized modern page header with optional top-right action."""
        hdr_frame = tk.Frame(self.content, bg=COLOR_BG)
        hdr_frame.pack(fill="x", pady=(0, 16))

        left = tk.Frame(hdr_frame, bg=COLOR_BG)
        left.pack(side="left", fill="x", expand=True)

        tk.Label(left, text=title, bg=COLOR_BG, fg=COLOR_TEXT, font=FONT_TITLE, anchor="w").pack(anchor="w")
        if subtitle:
            tk.Label(left, text=subtitle, bg=COLOR_BG, fg=COLOR_TEXT_MUTED, font=FONT_BODY, anchor="w").pack(anchor="w", pady=(2, 0))

        if action_btn_text and action_cmd:
            create_button(hdr_frame, action_btn_text, action_cmd, bg_color=COLOR_SURFACE,
                          hover_color=COLOR_SURFACE_ALT, fg_color=COLOR_TEXT).pack(side="right")

        # Sleek gradient-like accent border below header
        sep = tk.Frame(self.content, bg=COLOR_ACCENT, height=2)
        sep.pack(fill="x", pady=(0, 16))

    def _refresh_state(self):
        """Reload students from storage and refresh footer count."""
        self.students = load_students()
        self.footer_lbl.config(text=f"Enrolled: {len(self.students)} students")

    # ==========================================================================
    # 1. CLASS PERFORMANCE DASHBOARD (WITH MULTI-GRAPH VISUALIZATIONS)
    # ==========================================================================
    def show_dashboard(self):
        """Render the comprehensive analytics dashboard with multiple graph views."""
        self._clear_content()
        self._refresh_state()

        self._page_header(
            "Class Performance Dashboard",
            "Comprehensive academic analytics, grade distributions & performance graphs",
            action_btn_text="🔄 Refresh Data",
            action_cmd=self.show_dashboard
        )

        if not self.students:
            empty_card = tk.Frame(self.content, bg=COLOR_SURFACE, padx=32, pady=32,
                                  highlightthickness=1, highlightbackground=COLOR_BORDER)
            empty_card.pack(fill="x", pady=20)
            tk.Label(empty_card, text="No Student Records Found", bg=COLOR_SURFACE, fg=COLOR_TEXT, font=FONT_H1).pack()
            tk.Label(
                empty_card,
                text="Register student records to generate analytics and graphs automatically.",
                bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, font=FONT_BODY
            ).pack(pady=(6, 16))
            create_button(empty_card, "Add First Student", self.show_add).pack()
            return

        analytics = calculate_analytics(self.students)

        # ── KPI METRICS SUMMARY ROW ──
        kpi_container = tk.Frame(self.content, bg=COLOR_BG)
        kpi_container.pack(fill="x", pady=(0, 16))

        metrics = [
            ("Total Students",  str(analytics["total"]),           COLOR_TEXT,     "👥"),
            ("Class Average",   f"{analytics['average']:.1f}",     COLOR_TEXT,     "📊"),
            ("Highest Score",   f"{analytics['highest']}",         COLOR_SUCCESS,  "🏆"),
            ("Lowest Score",    f"{analytics['lowest']}",          COLOR_DANGER,   "📉"),
            ("Pass Rate",       f"{analytics['pass_percentage']}%",COLOR_SUCCESS,  "🎯"),
            ("At-Risk / Fail",  str(analytics["failed"]),          COLOR_DANGER,   "⚠️"),
        ]

        # Use uniform grid for responsive card distribution
        for i, (title, value, color, icon) in enumerate(metrics):
            card = tk.Frame(kpi_container, bg=COLOR_SURFACE, padx=14, pady=12,
                            highlightthickness=1, highlightbackground=COLOR_BORDER)
            card.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 8, 0))

            top_row = tk.Frame(card, bg=COLOR_SURFACE)
            top_row.pack(fill="x")
            tk.Label(top_row, text=icon, bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, font=FONT_SMALL).pack(side="left")
            tk.Label(top_row, text=title, bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, font=FONT_SMALL).pack(side="left", padx=6)

            tk.Label(card, text=value, bg=COLOR_SURFACE, fg=color, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(4, 0))

        # ── GRAPH TYPE SELECTOR SEGMENTED TOOLBAR ──
        ctrl_bar = tk.Frame(self.content, bg=COLOR_SURFACE, padx=10, pady=8,
                            highlightthickness=1, highlightbackground=COLOR_BORDER)
        ctrl_bar.pack(fill="x", pady=(0, 12))

        tk.Label(ctrl_bar, text="SELECT GRAPH VIEW:", bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED,
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(4, 12))

        graph_options = [
            ("🔲 Overview (Dual Charts)",        "dual"),
            ("📊 Student Marks (Bar Chart)",     "bar"),
            ("🍩 Grade Distribution (Donut)",     "donut"),
            ("📚 Course Averages (Bar Chart)",    "course"),
            ("📉 Score Brackets (Histogram)",     "brackets"),
        ]

        self.graph_btn_refs = {}
        for label, mode in graph_options:
            is_active = (self.current_graph_mode == mode)
            btn = tk.Button(
                ctrl_bar,
                text=label,
                command=lambda m=mode: self._switch_graph_mode(m),
                bg=COLOR_ACCENT if is_active else COLOR_SURFACE_ALT,
                fg="#FFFFFF" if is_active else COLOR_TEXT,
                activebackground=COLOR_ACCENT_HOVER,
                activeforeground="#FFFFFF",
                relief="flat",
                cursor="hand2",
                font=("Segoe UI", 9, "bold" if is_active else "normal"),
                padx=10,
                pady=4,
                bd=0
            )
            btn.pack(side="left", padx=4)
            self.graph_btn_refs[mode] = btn

        # ── EMBEDDED GRAPH CANVAS CONTAINER ──
        self.graph_container = tk.Frame(self.content, bg=COLOR_SURFACE,
                                        highlightthickness=1, highlightbackground=COLOR_BORDER)
        self.graph_container.pack(fill="both", expand=True)

        self._render_current_graph(analytics)

    def _switch_graph_mode(self, mode):
        """Switch graph display mode and update toolbar highlights."""
        self.current_graph_mode = mode
        for m, btn in self.graph_btn_refs.items():
            if m == mode:
                btn.config(bg=COLOR_ACCENT, fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
            else:
                btn.config(bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT, font=("Segoe UI", 9, "normal"))

        analytics = calculate_analytics(self.students)
        self._render_current_graph(analytics)

    def _render_current_graph(self, analytics):
        """Render the selected graph mode onto the embedded canvas with dark styling."""
        # Clean previous canvas
        for w in self.graph_container.winfo_children():
            w.destroy()

        mode = self.current_graph_mode

        # Initialize dark-themed figure
        if mode == "dual":
            fig = Figure(figsize=(9, 4.4), facecolor=COLOR_SURFACE, dpi=100)
            ax1 = fig.add_subplot(1, 2, 1)
            ax2 = fig.add_subplot(1, 2, 2)
            self._plot_student_bars(ax1)
            self._plot_grade_donut(ax2, analytics)
            fig.tight_layout(pad=2.2)
        elif mode == "bar":
            fig = Figure(figsize=(9, 4.4), facecolor=COLOR_SURFACE, dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_student_bars(ax, detailed=True)
            fig.tight_layout(pad=2.0)
        elif mode == "donut":
            fig = Figure(figsize=(9, 4.4), facecolor=COLOR_SURFACE, dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_grade_donut(ax, analytics, detailed=True)
            fig.tight_layout(pad=2.0)
        elif mode == "course":
            fig = Figure(figsize=(9, 4.4), facecolor=COLOR_SURFACE, dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_course_bars(ax, analytics)
            fig.tight_layout(pad=2.0)
        elif mode == "brackets":
            fig = Figure(figsize=(9, 4.4), facecolor=COLOR_SURFACE, dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_score_brackets(ax, analytics)
            fig.tight_layout(pad=2.0)

        # Embed into Tkinter
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    # ── INDIVIDUAL GRAPH PLOTTING ROUTINES ────────────────────────────────────
    def _plot_student_bars(self, ax, detailed=False):
        """Plot individual student marks bar chart."""
        ax.set_facecolor(COLOR_BG)

        names = [s.get("name", "").title() for s in self.students]
        marks = [float(s.get("marks", 0)) for s in self.students]

        # Truncate long names for presentation
        short_names = [n if len(n) <= 12 else n[:10] + ".." for n in names]

        # Color-code bars: Electric Crimson for failing, Emerald/Coral for passing
        bar_colors = [COLOR_DANGER if m < 40 else COLOR_ACCENT for m in marks]

        bars = ax.bar(short_names, marks, color=bar_colors, edgecolor=COLOR_TEXT, linewidth=0.8, width=0.55)

        # Pass threshold reference line (40 marks)
        ax.axhline(40, color=COLOR_WARNING, linestyle="--", linewidth=1.2, alpha=0.85, label="Passing Mark (40)")

        # Class average reference line
        avg = sum(marks) / len(marks)
        ax.axhline(avg, color=COLOR_TEXT, linestyle=":", linewidth=1.2, alpha=0.75, label=f"Average ({avg:.1f})")

        # Annotations on top of bars
        for bar, m in zip(bars, marks):
            grade = calculate_grade(m)
            height = bar.get_height()
            ax.annotate(
                f"{m:.0f}\n({grade})",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center", va="bottom",
                color=COLOR_TEXT,
                fontsize=8 if not detailed else 9,
                fontweight="bold"
            )

        ax.set_ylim(0, max(105, max(marks, default=100) + 15))
        ax.set_ylabel("Marks (0-100)", color=COLOR_TEXT_MUTED, fontsize=9)
        ax.set_title("Student Marks Comparison", color=COLOR_TEXT, fontsize=11, fontweight="bold", pad=10)

        ax.tick_params(colors=COLOR_TEXT_MUTED, labelsize=8.5)
        if len(names) > 5:
            ax.tick_params(axis="x", rotation=25)

        for spine in ax.spines.values():
            spine.set_color(COLOR_BORDER)

        ax.grid(axis="y", color=COLOR_BORDER, linestyle=":", alpha=0.6)
        ax.legend(facecolor=COLOR_SURFACE, edgecolor=COLOR_BORDER, labelcolor=COLOR_TEXT, fontsize=7.5, loc="upper right")

    def _plot_grade_donut(self, ax, analytics, detailed=False):
        """Plot modern donut chart representing letter grade breakdown."""
        ax.set_facecolor(COLOR_SURFACE)

        grade_counts = analytics["grade_counts"]
        # Filter grades with at least 1 student
        filtered = {g: count for g, count in grade_counts.items() if count > 0}

        if not filtered:
            ax.text(0.5, 0.5, "No Data", color=COLOR_TEXT_MUTED, ha="center", va="center")
            return

        labels = list(filtered.keys())
        counts = list(filtered.values())

        # Curated harmonious color palette matching the theme
        palette_map = {
            "A+": "#4ADE80",  # Emerald
            "A":  "#60A5FA",  # Light Blue
            "B":  "#A78BFA",  # Violet
            "C":  "#FBBF24",  # Amber
            "D":  "#FFF9F9",  # Ivory
            "F":  COLOR_ACCENT  # Electric Crimson
        }
        slice_colors = [palette_map.get(lbl, COLOR_ACCENT) for lbl in labels]

        wedges, texts, autotexts = ax.pie(
            counts,
            labels=labels,
            autopct="%1.0f%%",
            startangle=140,
            colors=slice_colors,
            textprops={"color": COLOR_TEXT, "fontsize": 8.5, "fontweight": "bold"},
            pctdistance=0.75,
            wedgeprops={"edgecolor": COLOR_SURFACE, "linewidth": 2, "width": 0.45}
        )

        for at in autotexts:
            at.set_color("#162311")  # High contrast text inside slices
            at.set_fontsize(8)

        # Center label inside donut hole
        ax.text(0, 0, f"Total\n{analytics['total']}", ha="center", va="center",
                color=COLOR_TEXT, fontsize=10, fontweight="bold")

        ax.set_title("Grade Distribution", color=COLOR_TEXT, fontsize=11, fontweight="bold", pad=10)
        ax.legend(wedges, [f"{g}: {c} student(s)" for g, c in zip(labels, counts)],
                  loc="center left", bbox_to_anchor=(0.85, 0.5),
                  facecolor=COLOR_SURFACE, edgecolor=COLOR_BORDER, labelcolor=COLOR_TEXT, fontsize=8)

    def _plot_course_bars(self, ax, analytics):
        """Plot course-wise average marks horizontal bar chart."""
        ax.set_facecolor(COLOR_BG)

        course_stats = analytics.get("course_stats", {})
        if not course_stats:
            ax.text(0.5, 0.5, "No Course Data", color=COLOR_TEXT_MUTED, ha="center", va="center")
            return

        courses = list(course_stats.keys())
        averages = [data["average"] for data in course_stats.values()]
        counts = [data["count"] for data in course_stats.values()]

        y_pos = range(len(courses))
        bars = ax.barh(y_pos, averages, color=COLOR_ACCENT, edgecolor=COLOR_TEXT, linewidth=0.8, height=0.45)

        for bar, avg, cnt in zip(bars, averages, counts):
            width = bar.get_width()
            ax.annotate(
                f" {avg:.1f} avg ({cnt} student{'s' if cnt > 1 else ''})",
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(6, 0),
                textcoords="offset points",
                ha="left", va="center",
                color=COLOR_TEXT,
                fontsize=9,
                fontweight="bold"
            )

        ax.set_yticks(y_pos)
        ax.set_yticklabels(courses, color=COLOR_TEXT, fontsize=9.5)
        ax.set_xlim(0, 115)
        ax.set_xlabel("Average Marks", color=COLOR_TEXT_MUTED, fontsize=9)
        ax.set_title("Course-wise Academic Performance", color=COLOR_TEXT, fontsize=11, fontweight="bold", pad=10)

        ax.tick_params(colors=COLOR_TEXT_MUTED)
        for spine in ax.spines.values():
            spine.set_color(COLOR_BORDER)
        ax.grid(axis="x", color=COLOR_BORDER, linestyle=":", alpha=0.6)

    def _plot_score_brackets(self, ax, analytics):
        """Plot distribution of marks by score brackets (histogram style)."""
        ax.set_facecolor(COLOR_BG)

        brackets = analytics.get("score_ranges", {})
        labels = list(brackets.keys())
        values = list(brackets.values())

        colors = [COLOR_DANGER, COLOR_WARNING, COLOR_INFO, COLOR_SUCCESS]

        bars = ax.bar(labels, values, color=colors, edgecolor=COLOR_TEXT, linewidth=0.8, width=0.5)

        for bar, val in zip(bars, values):
            h = bar.get_height()
            ax.annotate(
                f"{val} student(s)",
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center", va="bottom",
                color=COLOR_TEXT,
                fontsize=9,
                fontweight="bold"
            )

        ax.set_ylim(0, max(values, default=1) + 2)
        ax.set_ylabel("Student Count", color=COLOR_TEXT_MUTED, fontsize=9)
        ax.set_title("Score Bracket Distribution", color=COLOR_TEXT, fontsize=11, fontweight="bold", pad=10)

        ax.tick_params(colors=COLOR_TEXT_MUTED, labelsize=9)
        for spine in ax.spines.values():
            spine.set_color(COLOR_BORDER)
        ax.grid(axis="y", color=COLOR_BORDER, linestyle=":", alpha=0.6)

    # ==========================================================================
    # 2. VIEW STUDENT RECORDS (TABLE, LIVE SEARCH, DELETE)
    # ==========================================================================
    def show_view(self):
        """Display student records in an interactive table with live search & deletion."""
        self._clear_content()
        self._refresh_state()

        self._page_header(
            "Student Records",
            f"Managing {len(self.students)} registered student(s)",
            action_btn_text="➕ Add New Student",
            action_cmd=self.show_add
        )

        # ── Toolbar: Search & Action Controls ──
        toolbar = tk.Frame(self.content, bg=COLOR_BG)
        toolbar.pack(fill="x", pady=(0, 12))

        tk.Label(toolbar, text="Quick Search:", bg=COLOR_BG, fg=COLOR_TEXT_MUTED, font=FONT_BODY).pack(side="left", padx=(0, 8))

        search_wrap, self.table_search_entry = create_entry(toolbar, width=24)
        search_wrap.pack(side="left", padx=(0, 12))
        self.table_search_entry.bind("<KeyRelease>", lambda e: self._filter_student_table())

        create_button(toolbar, "Delete Selected", self._delete_selected_student,
                      bg_color=COLOR_SURFACE_ALT, hover_color=COLOR_DANGER,
                      fg_color=COLOR_TEXT, icon="🗑️").pack(side="right", padx=(8, 0))

        create_button(toolbar, "Update Marks", self.show_update,
                      bg_color=COLOR_SURFACE_ALT, hover_color=COLOR_ACCENT,
                      fg_color=COLOR_TEXT, icon="✏️").pack(side="right")

        # ── Treeview Table ──
        table_frame = tk.Frame(self.content, bg=COLOR_SURFACE,
                               highlightthickness=1, highlightbackground=COLOR_BORDER)
        table_frame.pack(fill="both", expand=True)

        columns = ("roll_no", "name", "age", "course", "marks", "grade", "status")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Modern.Treeview",
            selectmode="browse"
        )

        headers = [
            ("roll_no", "Roll Number", 110, "center"),
            ("name",    "Student Name", 190, "w"),
            ("age",     "Age",           70, "center"),
            ("course",  "Course / Stream", 160, "w"),
            ("marks",   "Marks",        100, "center"),
            ("grade",   "Grade",         90, "center"),
            ("status",  "Status",       120, "center"),
        ]

        for col_id, col_text, col_width, col_anchor in headers:
            self.tree.heading(col_id, text=col_text)
            self.tree.column(col_id, width=col_width, anchor=col_anchor)

        # Scrollbar
        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview,
                           style="Modern.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self._populate_student_table(self.students)

    def _populate_student_table(self, student_list):
        """Fill treeview rows with student data."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for s in student_list:
            marks = float(s.get("marks", 0))
            grade = calculate_grade(marks)
            status = "PASSED" if marks >= 40 else "NEEDS SUPPORT"
            self.tree.insert("", "end", values=(
                s.get("roll_no", "N/A"),
                s.get("name", "N/A").title(),
                s.get("age", "N/A"),
                s.get("course", "N/A"),
                f"{marks:.2f}",
                grade,
                status
            ))

    def _filter_student_table(self):
        """Filter table records in real-time based on search input."""
        query = self.table_search_entry.get().strip().lower()
        if not query:
            self._populate_student_table(self.students)
            return

        filtered = [
            s for s in self.students
            if query in str(s.get("roll_no", "")).lower()
            or query in str(s.get("name", "")).lower()
            or query in str(s.get("course", "")).lower()
        ]
        self._populate_student_table(filtered)

    def _delete_selected_student(self):
        """Delete selected student record after user confirmation."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a student from the table to delete.")
            return

        values = self.tree.item(selected[0], "values")
        roll_no = values[0]
        name = values[1]

        confirmed = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to remove student:\n\n{name} (Roll No: {roll_no})?\n\nThis action cannot be undone."
        )
        if not confirmed:
            return

        self.students = [s for s in self.students if s.get("roll_no") != roll_no]
        if save_students(self.students):
            messagebox.showinfo("Deleted", f"Student '{name}' was removed successfully.")
            self.show_view()

    # ==========================================================================
    # 3. ADD NEW STUDENT
    # ==========================================================================
    def show_add(self):
        """Render the registration form for adding new student records."""
        self._clear_content()
        self._page_header("Add New Student", "Register a new student record into the system")

        card = tk.Frame(self.content, bg=COLOR_SURFACE, padx=32, pady=28,
                        highlightthickness=1, highlightbackground=COLOR_BORDER)
        card.pack(anchor="nw", fill="x", padx=(0, 40))
        card.columnconfigure(1, weight=1)

        self.e_roll   = create_form_row(card, "Roll Number",      0)
        self.e_name   = create_form_row(card, "Full Student Name", 1)
        self.e_age    = create_form_row(card, "Age (1-120)",       2)
        self.e_course = create_form_row(card, "Course / Stream",   3)
        self.e_marks  = create_form_row(card, "Marks (0 - 100)",   4)

        btn_row = tk.Frame(card, bg=COLOR_SURFACE)
        btn_row.grid(row=5, column=0, columnspan=2, sticky="w", pady=(20, 0))

        create_button(btn_row, "Save Student Record", self._do_add, icon="💾").pack(side="left", padx=(0, 12))
        create_button(btn_row, "Clear Form", self._clear_add_form, bg_color=COLOR_SURFACE_ALT,
                      hover_color=COLOR_BORDER, fg_color=COLOR_TEXT).pack(side="left")

    def _clear_add_form(self):
        """Clear all inputs in the Add Student form."""
        for entry in (self.e_roll, self.e_name, self.e_age, self.e_course, self.e_marks):
            entry.delete(0, "end")

    def _do_add(self):
        """Validate inputs and persist the new student record."""
        roll_no = self.e_roll.get().strip()
        name    = self.e_name.get().strip()
        course  = self.e_course.get().strip()

        if not roll_no or not name or not course:
            messagebox.showerror("Missing Information", "Roll number, name, and course are required fields.")
            return

        # Check for duplicates
        if any(s.get("roll_no") == roll_no for s in self.students):
            messagebox.showerror("Duplicate Roll Number", f"Student with roll number '{roll_no}' already exists.")
            return

        # Validate numeric fields
        try:
            age = int(self.e_age.get().strip())
            marks = float(self.e_marks.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Age must be an integer and marks must be numeric.")
            return

        if age <= 0 or age > 120:
            messagebox.showerror("Invalid Age", "Please enter a valid age between 1 and 120.")
            return

        if marks < 0 or marks > 100:
            messagebox.showerror("Invalid Marks", "Marks must be between 0 and 100.")
            return

        new_student = {
            "roll_no": roll_no,
            "name": name,
            "age": age,
            "course": course,
            "marks": round(marks, 2)
        }

        self.students.append(new_student)
        if save_students(self.students):
            grade = calculate_grade(marks)
            messagebox.showinfo("Success", f"Student '{name}' added successfully with Grade {grade}!")
            self._clear_add_form()
            self._refresh_state()

    # ==========================================================================
    # 4. SEARCH STUDENT
    # ==========================================================================
    def show_search(self):
        """Render the search interface to look up student details by roll number."""
        self._clear_content()
        self._page_header("Search Student Record", "Look up student academic information by roll number")

        search_bar = tk.Frame(self.content, bg=COLOR_BG)
        search_bar.pack(anchor="w", pady=(0, 16))

        tk.Label(search_bar, text="Roll Number:", bg=COLOR_BG, fg=COLOR_TEXT_MUTED, font=FONT_BODY).pack(side="left", padx=(0, 8))

        wrap, self.e_search = create_entry(search_bar, width=24)
        wrap.pack(side="left", padx=(0, 10))
        self.e_search.bind("<Return>", lambda e: self._do_search())

        create_button(search_bar, "Search", self._do_search, icon="🔍").pack(side="left")

        # Container for search result card
        self.search_card_area = tk.Frame(self.content, bg=COLOR_BG)
        self.search_card_area.pack(fill="x", pady=10)

    def _do_search(self):
        """Execute student search and display modern result card."""
        for w in self.search_card_area.winfo_children():
            w.destroy()

        roll_no = self.e_search.get().strip()
        if not roll_no:
            messagebox.showwarning("Input Required", "Please enter a roll number to search.")
            return

        found = next((s for s in self.students if s.get("roll_no") == roll_no), None)
        if not found:
            not_found = tk.Frame(self.search_card_area, bg=COLOR_SURFACE, padx=24, pady=20,
                                 highlightthickness=1, highlightbackground=COLOR_DANGER)
            not_found.pack(anchor="w", fill="x")
            tk.Label(not_found, text=f"❌ No student found with Roll Number '{roll_no}'.",
                     bg=COLOR_SURFACE, fg=COLOR_DANGER, font=FONT_BOLD).pack(anchor="w")
            return

        # Render rich result card
        card = tk.Frame(self.search_card_area, bg=COLOR_SURFACE, padx=28, pady=24,
                        highlightthickness=1, highlightbackground=COLOR_BORDER)
        card.pack(anchor="w", fill="x")

        # Top pill badge
        marks = float(found.get("marks", 0))
        grade = calculate_grade(marks)
        status_color = COLOR_SUCCESS if marks >= 40 else COLOR_DANGER

        header_row = tk.Frame(card, bg=COLOR_SURFACE)
        header_row.pack(fill="x", pady=(0, 14))

        tk.Label(header_row, text=found.get("name", "").title(), bg=COLOR_SURFACE,
                 fg=COLOR_TEXT, font=FONT_TITLE).pack(side="left")

        badge = tk.Frame(header_row, bg=COLOR_ACCENT_MUTED, padx=10, pady=3)
        badge.pack(side="right")
        tk.Label(badge, text=f"GRADE {grade}", bg=COLOR_ACCENT_MUTED,
                 fg=COLOR_ACCENT, font=("Segoe UI", 9, "bold")).pack()

        # Grid of student attributes
        details_grid = tk.Frame(card, bg=COLOR_SURFACE)
        details_grid.pack(fill="x", pady=(0, 12))

        fields = [
            ("Roll Number", found.get("roll_no")),
            ("Age",         f"{found.get('age')} years"),
            ("Course",      found.get("course")),
            ("Marks",       f"{marks:.2f} / 100"),
            ("Evaluation",  get_grade_remark(grade)),
            ("Status",      "Passing Standard" if marks >= 40 else "Needs Academic Support"),
        ]

        for i, (k, v) in enumerate(fields):
            r = i // 2
            c = (i % 2) * 2

            tk.Label(details_grid, text=f"{k}:", bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED,
                     font=FONT_SMALL).grid(row=r, column=c, sticky="w", padx=(0, 8), pady=4)

            val_color = status_color if k in ("Marks", "Evaluation", "Status") else COLOR_TEXT
            tk.Label(details_grid, text=str(v), bg=COLOR_SURFACE, fg=val_color,
                     font=FONT_BOLD).grid(row=r, column=c + 1, sticky="w", padx=(0, 32), pady=4)

    # ==========================================================================
    # 5. UPDATE MARKS
    # ==========================================================================
    def show_update(self):
        """Render interface to modify a student's marks."""
        self._clear_content()
        self._page_header("Update Student Marks", "Locate student and modify their marks record")

        card = tk.Frame(self.content, bg=COLOR_SURFACE, padx=32, pady=28,
                        highlightthickness=1, highlightbackground=COLOR_BORDER)
        card.pack(anchor="nw", fill="x", padx=(0, 40))
        card.columnconfigure(1, weight=1)

        self.e_upd_roll  = create_form_row(card, "Roll Number",            0)
        self.e_upd_marks = create_form_row(card, "New Marks (0 - 100)",    1)

        btn_row = tk.Frame(card, bg=COLOR_SURFACE)
        btn_row.grid(row=2, column=0, columnspan=2, sticky="w", pady=(20, 0))

        create_button(btn_row, "Update Marks Record", self._do_update, icon="🔄").pack(side="left")

    def _do_update(self):
        """Validate and apply updated marks."""
        roll_no = self.e_upd_roll.get().strip()
        found = next((s for s in self.students if s.get("roll_no") == roll_no), None)

        if not found:
            messagebox.showerror("Student Not Found", f"No record exists for roll number '{roll_no}'.")
            return

        try:
            new_marks = float(self.e_upd_marks.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric value for marks.")
            return

        if new_marks < 0 or new_marks > 100:
            messagebox.showerror("Invalid Marks", "Marks must be between 0 and 100.")
            return

        old_marks = found.get("marks", 0)
        found["marks"] = round(new_marks, 2)

        if save_students(self.students):
            new_grade = calculate_grade(new_marks)
            messagebox.showinfo(
                "Update Successful",
                f"Marks for '{found['name']}' updated:\n\n{old_marks}  ➔  {new_marks} (Grade: {new_grade})"
            )
            self.e_upd_roll.delete(0, "end")
            self.e_upd_marks.delete(0, "end")
            self._refresh_state()

    # ==========================================================================
    # 6. ACADEMIC INSIGHTS
    # ==========================================================================
    def show_insights(self):
        """Render actionable academic insights including top performers and at-risk students."""
        self._clear_content()
        self._page_header("Academic Insights & Guidance", "Actionable analysis of performance trends and interventions")

        if not self.students:
            tk.Label(self.content, text="No student records available.", bg=COLOR_BG, fg=COLOR_TEXT_MUTED, font=FONT_BODY).pack()
            return

        insights = get_insights(self.students)
        top = insights["top_performer"]
        struggling = insights["struggling_students"]

        # ── Top Performer Card ──
        top_card = tk.Frame(self.content, bg=COLOR_SURFACE, padx=24, pady=18,
                            highlightthickness=1, highlightbackground=COLOR_ACCENT)
        top_card.pack(fill="x", pady=(0, 16))

        tk.Label(top_card, text="🏆 VALEDICTORIAN / TOP PERFORMER", bg=COLOR_SURFACE, fg=COLOR_ACCENT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")

        if top:
            top_marks = float(top.get("marks", 0))
            top_grade = calculate_grade(top_marks)
            tk.Label(
                top_card,
                text=f"{top.get('name', '').title()}  •  {top_marks:.1f} Marks  (Grade {top_grade})",
                bg=COLOR_SURFACE, fg=COLOR_TEXT, font=FONT_H1
            ).pack(anchor="w", pady=(4, 2))
            tk.Label(
                top_card,
                text=f"Course: {top.get('course')}  |  Roll Number: {top.get('roll_no')}",
                bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, font=FONT_SMALL
            ).pack(anchor="w")

        # ── Class Standing Card ──
        class_card = tk.Frame(self.content, bg=COLOR_SURFACE, padx=24, pady=16,
                              highlightthickness=1, highlightbackground=COLOR_BORDER)
        class_card.pack(fill="x", pady=(0, 16))

        tk.Label(class_card, text="📊 CLASS OVERALL STANDING", bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")

        tk.Label(
            class_card,
            text=f"Class Mean Average: {insights['average']:.2f} Marks",
            bg=COLOR_SURFACE, fg=COLOR_TEXT, font=FONT_H1
        ).pack(anchor="w", pady=(4, 2))

        # ── Students Needing Academic Support ──
        support_card = tk.Frame(
            self.content,
            bg=COLOR_SURFACE,
            padx=24,
            pady=18,
            highlightthickness=1,
            highlightbackground=COLOR_DANGER if struggling else COLOR_BORDER
        )
        support_card.pack(fill="x")

        tk.Label(
            support_card,
            text="⚠️ STUDENTS REQUIRING ACADEMIC INTERVENTION (< 40 marks)",
            bg=COLOR_SURFACE,
            fg=COLOR_DANGER if struggling else COLOR_SUCCESS,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        if not struggling:
            tk.Label(
                support_card,
                text="✓ All students are currently meeting the academic passing threshold (≥ 40 marks).",
                bg=COLOR_SURFACE, fg=COLOR_SUCCESS, font=FONT_BODY
            ).pack(anchor="w", pady=(8, 0))
        else:
            for s in struggling:
                row = tk.Frame(support_card, bg=COLOR_SURFACE)
                row.pack(anchor="w", pady=4)
                tk.Label(row, text="•", bg=COLOR_SURFACE, fg=COLOR_DANGER, font=FONT_BOLD).pack(side="left", padx=(0, 6))
                tk.Label(
                    row,
                    text=f"{s.get('name', '').title()} (Roll {s.get('roll_no')}) — {s.get('marks')} Marks in {s.get('course')}",
                    bg=COLOR_SURFACE, fg=COLOR_TEXT, font=FONT_BODY
                ).pack(side="left")


# ==============================================================================
# APPLICATION ENTRYPOINT
# ==============================================================================
if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()

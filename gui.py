"""
gui.py - Modern Student Management System & Analytics Dashboard.
Color System:
  Strictly designed with the requested palette:
    - #FFF9F9 (Porcelain Ivory White)
    - #162311 (Obsidian Forest Dark)
Includes:
  - Interactive multi-graph dashboard (Overview dual view, Student bar chart,
    Grade donut chart, Course performance, Score bracket histogram)
  - Student records table with live search and delete features
  - Add, search, and update workflows
  - Seamless Dark (#162311) & Light (#FFF9F9) theme toggle
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
# THEME DEFINITIONS (#FFF9F9 & #162311)
# ==============================================================================
DARK_THEME = {
    "name": "dark",
    "bg":               "#162311",   # Obsidian olive dark canvas
    "sidebar":          "#0F1A0C",   # Deepest sidebar tone
    "surface":          "#1D2D18",   # Primary elevated card
    "surface_alt":      "#273A21",   # Secondary card / hover
    "input_bg":         "#121D0E",   # Field background
    "border":           "#31442A",   # Subtle dark border
    "border_focus":     "#FFF9F9",   # Focus highlight border
    "text":             "#FFF9F9",   # Crisp ivory white
    "text_muted":       "#A2B49F",   # Soft silvery sage
    "text_dim":         "#6C7E6A",   # Dim guide text
    "btn_primary_bg":   "#FFF9F9",   # Top pill style: white background
    "btn_primary_fg":   "#162311",   # Dark text on white pill
    "btn_primary_hov":  "#E8E2E2",   # Hover state
    "btn_sec_bg":       "#273A21",   # Secondary button background
    "btn_sec_fg":       "#FFF9F9",   # Secondary button text
    "btn_sec_hov":      "#344D2C",   # Secondary button hover
    "chart_bg":         "#1D2D18",   # Matplotlib figure background
    "chart_ax":         "#162311",   # Matplotlib plot area
    "chart_bar":        "#FFF9F9",   # Primary bar color
    "chart_bar_alt":    "#7F977B",   # Secondary bar color
    "chart_border":     "#31442A",   # Graph spines
}

LIGHT_THEME = {
    "name": "light",
    "bg":               "#FFF9F9",   # Porcelain ivory white canvas
    "sidebar":          "#F2ECEC",   # Light sidebar
    "surface":          "#FFFFFF",   # Crisp white card
    "surface_alt":      "#F4EEEE",   # Hover surface
    "input_bg":         "#FFFFFF",   # White field
    "border":           "#DDD4D4",   # Soft border
    "border_focus":     "#162311",   # Dark focus border
    "text":             "#162311",   # Obsidian dark text
    "text_muted":       "#556651",   # Muted dark olive
    "text_dim":         "#8A9A86",   # Dim guide text
    "btn_primary_bg":   "#162311",   # Pill style: dark background
    "btn_primary_fg":   "#FFF9F9",   # Ivory text on dark pill
    "btn_primary_hov":  "#273A21",   # Hover state
    "btn_sec_bg":       "#EBE3E3",   # Secondary button background
    "btn_sec_fg":       "#162311",   # Secondary button text
    "btn_sec_hov":      "#DFD7D7",   # Secondary button hover
    "chart_bg":         "#FFFFFF",   # Matplotlib figure background
    "chart_ax":         "#FFF9F9",   # Matplotlib plot area
    "chart_bar":        "#162311",   # Primary bar color
    "chart_bar_alt":    "#7F977B",   # Secondary bar color
    "chart_border":     "#DDD4D4",   # Graph spines
}

# Typography
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_H1    = ("Segoe UI", 13, "bold")
FONT_H2    = ("Segoe UI", 11, "bold")
FONT_BODY  = ("Segoe UI", 10)
FONT_BOLD  = ("Segoe UI", 10, "bold")
FONT_SMALL = ("Segoe UI", 9)


# ==============================================================================
# MAIN APPLICATION
# ==============================================================================
class StudentApp(tk.Tk):
    """Student Management System with high-contrast #FFF9F9 & #162311 aesthetic."""

    def __init__(self):
        super().__init__()
        self.title("Student Management System • Analytics Dashboard")
        self.geometry("1140x730")
        self.minsize(980, 620)

        # Active theme (defaults to dark #162311 base)
        self.t = DARK_THEME
        self.configure(bg=self.t["bg"])

        # State
        self.students = load_students()
        self.current_page = "dashboard"
        self.current_graph_mode = "dual"  # "dual", "bar", "donut", "course", "brackets"
        self.chart_canvas = None

        self._configure_treeview_styles()
        self._build_layout()

    # ── THEME MANAGER ─────────────────────────────────────────────────────────
    def _toggle_theme(self):
        """Switch between dark (#162311) and light (#FFF9F9) themes."""
        self.t = LIGHT_THEME if self.t["name"] == "dark" else DARK_THEME
        self.configure(bg=self.t["bg"])
        self._configure_treeview_styles()

        # Rebuild whole UI with updated colors
        for w in self.winfo_children():
            w.destroy()
        self._build_layout()

    def _configure_treeview_styles(self):
        """Apply ttk styles for treeview matching current theme."""
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Custom.Treeview",
            background=self.t["surface"],
            foreground=self.t["text"],
            fieldbackground=self.t["surface"],
            rowheight=32,
            font=FONT_BODY,
            borderwidth=0
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=self.t["sidebar"],
            foreground=self.t["text"],
            font=FONT_BOLD,
            relief="flat",
            padding=(6, 8)
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", self.t["btn_primary_bg"])],
            foreground=[("selected", self.t["btn_primary_fg"])]
        )
        style.map(
            "Custom.Treeview.Heading",
            background=[("active", self.t["surface_alt"])]
        )

    # ── WIDGET FACTORIES ──────────────────────────────────────────────────────
    def _btn_primary(self, parent, text, command, width=None, icon=""):
        """Create primary pill button matching the signature pill style."""
        disp = f"{icon} {text}".strip() if icon else text
        btn = tk.Button(
            parent,
            text=disp,
            command=command,
            bg=self.t["btn_primary_bg"],
            fg=self.t["btn_primary_fg"],
            activebackground=self.t["btn_primary_hov"],
            activeforeground=self.t["btn_primary_fg"],
            relief="flat",
            cursor="hand2",
            font=FONT_BOLD,
            padx=16,
            pady=7,
            bd=0,
            width=width
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=self.t["btn_primary_hov"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.t["btn_primary_bg"]))
        return btn

    def _btn_secondary(self, parent, text, command, width=None, icon=""):
        """Create secondary neutral button."""
        disp = f"{icon} {text}".strip() if icon else text
        btn = tk.Button(
            parent,
            text=disp,
            command=command,
            bg=self.t["btn_sec_bg"],
            fg=self.t["btn_sec_fg"],
            activebackground=self.t["btn_sec_hov"],
            activeforeground=self.t["btn_sec_fg"],
            relief="flat",
            cursor="hand2",
            font=FONT_BODY,
            padx=14,
            pady=7,
            bd=0,
            width=width
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=self.t["btn_sec_hov"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.t["btn_sec_bg"]))
        return btn

    def _styled_entry(self, parent, width=28, **kwargs):
        """Create an entry input framed with clean border."""
        wrapper = tk.Frame(parent, bg=self.t["border"], padx=1, pady=1)
        entry = tk.Entry(
            wrapper,
            bg=self.t["input_bg"],
            fg=self.t["text"],
            insertbackground=self.t["text"],
            relief="flat",
            font=FONT_BODY,
            bd=0,
            width=width,
            **kwargs
        )
        entry.pack(fill="both", expand=True, padx=8, pady=6)
        entry.bind("<FocusIn>",  lambda e: wrapper.config(bg=self.t["border_focus"]))
        entry.bind("<FocusOut>", lambda e: wrapper.config(bg=self.t["border"]))
        return wrapper, entry

    def _form_field(self, parent, label_text, row_idx):
        """Build standard form row with label and entry."""
        tk.Label(
            parent,
            text=label_text,
            bg=self.t["surface"],
            fg=self.t["text_muted"],
            font=FONT_BODY,
            anchor="w"
        ).grid(row=row_idx, column=0, sticky="w", padx=(0, 16), pady=8)

        wrap, entry = self._styled_entry(parent, width=32)
        wrap.grid(row=row_idx, column=1, sticky="ew", pady=8)
        return entry

    # ── LAYOUT SHELL ──────────────────────────────────────────────────────────
    def _build_layout(self):
        """Build the left sidebar and main content frame."""
        # ── Sidebar ──
        self.sidebar = tk.Frame(self, bg=self.t["sidebar"], width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand header
        brand = tk.Frame(self.sidebar, bg=self.t["sidebar"], padx=18, pady=20)
        brand.pack(fill="x")

        # Pill logo badge
        pill_badge = tk.Frame(brand, bg=self.t["btn_primary_bg"], padx=10, pady=4)
        pill_badge.pack(anchor="w", pady=(0, 8))
        tk.Label(
            pill_badge,
            text="● ACADEMIC SUITE",
            bg=self.t["btn_primary_bg"],
            fg=self.t["btn_primary_fg"],
            font=("Segoe UI", 8, "bold")
        ).pack()

        tk.Label(brand, text="Student Manager", bg=self.t["sidebar"],
                 fg=self.t["text"], font=FONT_TITLE, anchor="w").pack(anchor="w")
        tk.Label(brand, text="#fff9f9 • #162311 Edition", bg=self.t["sidebar"],
                 fg=self.t["text_muted"], font=FONT_SMALL, anchor="w").pack(anchor="w")

        tk.Frame(self.sidebar, bg=self.t["border"], height=1).pack(fill="x", padx=16, pady=(12, 14))

        # Navigation items
        nav_items = [
            ("📊 Dashboard & Graphs", "dashboard", self.show_dashboard),
            ("📋 Student Records",    "view",      self.show_view),
            ("➕ Add Student",        "add",       self.show_add),
            ("🔍 Search Student",     "search",    self.show_search),
            ("✏️ Update Marks",       "update",    self.show_update),
            ("💡 Academic Insights",  "insights",  self.show_insights),
        ]

        self.nav_buttons = {}
        for label, page_key, cmd in nav_items:
            is_active = (self.current_page == page_key)
            btn = tk.Button(
                self.sidebar,
                text=f"  {label}",
                command=lambda c=cmd, k=page_key: self._navigate(c, k),
                bg=self.t["btn_primary_bg"] if is_active else self.t["sidebar"],
                fg=self.t["btn_primary_fg"] if is_active else self.t["text_muted"],
                activebackground=self.t["surface_alt"],
                activeforeground=self.t["text"],
                relief="flat",
                anchor="w",
                padx=16,
                pady=10,
                font=FONT_BOLD if is_active else FONT_BODY,
                cursor="hand2",
                bd=0
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.nav_buttons[page_key] = btn

        # Theme toggle in sidebar
        toggle_frame = tk.Frame(self.sidebar, bg=self.t["surface"], padx=12, pady=12)
        toggle_frame.pack(side="bottom", fill="x", padx=12, pady=16)

        theme_text = "☀️ Switch to Light (#FFF9F9)" if self.t["name"] == "dark" else "🌙 Switch to Dark (#162311)"
        self._btn_secondary(toggle_frame, theme_text, self._toggle_theme).pack(fill="x")

        # Database indicator
        tk.Label(
            toggle_frame,
            text=f"Enrolled: {len(self.students)} students",
            bg=self.t["surface"],
            fg=self.t["text_muted"],
            font=FONT_SMALL
        ).pack(anchor="w", pady=(8, 0))

        # ── Main Content Area ──
        self.content = tk.Frame(self, bg=self.t["bg"])
        self.content.pack(side="left", fill="both", expand=True, padx=24, pady=24)

        # Show current page
        if self.current_page == "dashboard":
            self.show_dashboard()
        elif self.current_page == "view":
            self.show_view()
        elif self.current_page == "add":
            self.show_add()
        elif self.current_page == "search":
            self.show_search()
        elif self.current_page == "update":
            self.show_update()
        else:
            self.show_insights()

    def _navigate(self, command, page_key):
        """Update active navigation button state and switch page."""
        self.current_page = page_key
        for key, btn in self.nav_buttons.items():
            if key == page_key:
                btn.config(bg=self.t["btn_primary_bg"], fg=self.t["btn_primary_fg"], font=FONT_BOLD)
            else:
                btn.config(bg=self.t["sidebar"], fg=self.t["text_muted"], font=FONT_BODY)
        command()

    def _clear_content(self):
        """Safely clean content frame and destroy matplotlib canvas."""
        if self.chart_canvas:
            try:
                self.chart_canvas.get_tk_widget().destroy()
            except Exception:
                pass
            self.chart_canvas = None

        for w in self.content.winfo_children():
            w.destroy()

    def _page_header(self, title, subtitle="", action_btn_text=None, action_cmd=None):
        """Create consistent modern header across all pages."""
        header_row = tk.Frame(self.content, bg=self.t["bg"])
        header_row.pack(fill="x", pady=(0, 14))

        left = tk.Frame(header_row, bg=self.t["bg"])
        left.pack(side="left", fill="x", expand=True)

        tk.Label(left, text=title, bg=self.t["bg"], fg=self.t["text"], font=FONT_TITLE, anchor="w").pack(anchor="w")
        if subtitle:
            tk.Label(left, text=subtitle, bg=self.t["bg"], fg=self.t["text_muted"], font=FONT_BODY, anchor="w").pack(anchor="w", pady=(2, 0))

        if action_btn_text and action_cmd:
            self._btn_secondary(header_row, action_btn_text, action_cmd).pack(side="right")

        tk.Frame(self.content, bg=self.t["border"], height=1).pack(fill="x", pady=(0, 16))

    def _refresh_state(self):
        """Reload student records from disk."""
        self.students = load_students()

    # ==========================================================================
    # 1. CLASS PERFORMANCE DASHBOARD (WITH MULTI-GRAPH VISUALIZATIONS)
    # ==========================================================================
    def show_dashboard(self):
        """Render the complete analytics dashboard with embedded graphs."""
        self._clear_content()
        self._refresh_state()

        self._page_header(
            "Performance Dashboard",
            "Class metrics & interactive data visualizations (#fff9f9 / #162311)",
            action_btn_text="🔄 Refresh",
            action_cmd=self.show_dashboard
        )

        if not self.students:
            card = tk.Frame(self.content, bg=self.t["surface"], padx=32, pady=32,
                            highlightthickness=1, highlightbackground=self.t["border"])
            card.pack(fill="x", pady=20)
            tk.Label(card, text="No Student Records Found", bg=self.t["surface"], fg=self.t["text"], font=FONT_H1).pack()
            tk.Label(card, text="Add student records to generate class analytics and graphs.",
                     bg=self.t["surface"], fg=self.t["text_muted"], font=FONT_BODY).pack(pady=(6, 16))
            self._btn_primary(card, "Add First Student", self.show_add).pack()
            return

        analytics = calculate_analytics(self.students)

        # ── KPI Stat Cards Row ──
        kpi_row = tk.Frame(self.content, bg=self.t["bg"])
        kpi_row.pack(fill="x", pady=(0, 14))

        kpis = [
            ("Total Students", str(analytics["total"]),           "👥"),
            ("Class Average",  f"{analytics['average']:.1f}",     "📊"),
            ("Highest Marks",  f"{analytics['highest']}",         "🏆"),
            ("Lowest Marks",   f"{analytics['lowest']}",          "📉"),
            ("Pass Rate",      f"{analytics['pass_percentage']}%","🎯"),
            ("At-Risk (<40)",  str(analytics["failed"]),          "⚠️"),
        ]

        for i, (title, value, icon) in enumerate(kpis):
            card = tk.Frame(kpi_row, bg=self.t["surface"], padx=14, pady=12,
                            highlightthickness=1, highlightbackground=self.t["border"])
            card.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 8, 0))

            top = tk.Frame(card, bg=self.t["surface"])
            top.pack(fill="x")
            tk.Label(top, text=icon, bg=self.t["surface"], fg=self.t["text_muted"], font=FONT_SMALL).pack(side="left")
            tk.Label(top, text=title, bg=self.t["surface"], fg=self.t["text_muted"], font=FONT_SMALL).pack(side="left", padx=5)

            tk.Label(card, text=value, bg=self.t["surface"], fg=self.t["text"], font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(4, 0))

        # ── Graph Selector Toolbar ──
        toolbar = tk.Frame(self.content, bg=self.t["surface"], padx=10, pady=8,
                           highlightthickness=1, highlightbackground=self.t["border"])
        toolbar.pack(fill="x", pady=(0, 12))

        tk.Label(toolbar, text="GRAPH TYPE:", bg=self.t["surface"], fg=self.t["text_muted"],
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(4, 10))

        graph_modes = [
            ("🔲 Dual Charts (Overview)",   "dual"),
            ("📊 Marks Comparison (Bar)",   "bar"),
            ("🍩 Grade Breakdown (Donut)",   "donut"),
            ("📚 Course Averages (Bar)",     "course"),
            ("📉 Score Brackets (Histogram)","brackets"),
        ]

        self.graph_btns = {}
        for label, mode in graph_modes:
            is_active = (self.current_graph_mode == mode)
            btn = tk.Button(
                toolbar,
                text=label,
                command=lambda m=mode: self._change_graph_mode(m),
                bg=self.t["btn_primary_bg"] if is_active else self.t["surface_alt"],
                fg=self.t["btn_primary_fg"] if is_active else self.t["text"],
                activebackground=self.t["btn_primary_hov"],
                activeforeground=self.t["btn_primary_fg"],
                relief="flat",
                cursor="hand2",
                font=("Segoe UI", 9, "bold" if is_active else "normal"),
                padx=10,
                pady=4,
                bd=0
            )
            btn.pack(side="left", padx=4)
            self.graph_btns[mode] = btn

        # ── Canvas Area ──
        self.graph_box = tk.Frame(self.content, bg=self.t["surface"],
                                  highlightthickness=1, highlightbackground=self.t["border"])
        self.graph_box.pack(fill="both", expand=True)

        self._render_graph_view(analytics)

    def _change_graph_mode(self, mode):
        """Switch active graph mode and re-plot."""
        self.current_graph_mode = mode
        for m, btn in self.graph_btns.items():
            if m == mode:
                btn.config(bg=self.t["btn_primary_bg"], fg=self.t["btn_primary_fg"], font=("Segoe UI", 9, "bold"))
            else:
                btn.config(bg=self.t["surface_alt"], fg=self.t["text"], font=("Segoe UI", 9, "normal"))

        analytics = calculate_analytics(self.students)
        self._render_graph_view(analytics)

    def _render_graph_view(self, analytics):
        """Render charts using the clean #fff9f9 & #162311 palette."""
        for w in self.graph_box.winfo_children():
            w.destroy()

        mode = self.current_graph_mode

        if mode == "dual":
            fig = Figure(figsize=(9, 4.4), facecolor=self.t["chart_bg"], dpi=100)
            ax1 = fig.add_subplot(1, 2, 1)
            ax2 = fig.add_subplot(1, 2, 2)
            self._plot_bar_chart(ax1)
            self._plot_donut_chart(ax2, analytics)
            fig.tight_layout(pad=2.2)
        elif mode == "bar":
            fig = Figure(figsize=(9, 4.4), facecolor=self.t["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_bar_chart(ax)
            fig.tight_layout(pad=2.0)
        elif mode == "donut":
            fig = Figure(figsize=(9, 4.4), facecolor=self.t["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_donut_chart(ax, analytics)
            fig.tight_layout(pad=2.0)
        elif mode == "course":
            fig = Figure(figsize=(9, 4.4), facecolor=self.t["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_course_chart(ax, analytics)
            fig.tight_layout(pad=2.0)
        elif mode == "brackets":
            fig = Figure(figsize=(9, 4.4), facecolor=self.t["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_brackets_chart(ax, analytics)
            fig.tight_layout(pad=2.0)

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.graph_box)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    # ── PLOTTING HELPERS ──────────────────────────────────────────────────────
    def _plot_bar_chart(self, ax):
        """Bar chart of student marks."""
        ax.set_facecolor(self.t["chart_ax"])

        names = [s.get("name", "").title() for s in self.students]
        marks = [float(s.get("marks", 0)) for s in self.students]
        short_names = [n if len(n) <= 12 else n[:10] + ".." for n in names]

        # Contrast bar coloring
        bar_color = self.t["chart_bar"]
        alt_bar_color = self.t["chart_bar_alt"]
        colors = [bar_color if m >= 40 else alt_bar_color for m in marks]

        edge_color = self.t["text"] if self.t["name"] == "light" else self.t["chart_ax"]
        bars = ax.bar(short_names, marks, color=colors, edgecolor=edge_color, linewidth=0.8, width=0.55)

        # Benchmark reference lines
        avg = sum(marks) / len(marks)
        ax.axhline(40, color=self.t["text_muted"], linestyle="--", linewidth=1.1, alpha=0.8, label="Pass Mark (40)")
        ax.axhline(avg, color=self.t["text"], linestyle=":", linewidth=1.2, alpha=0.8, label=f"Average ({avg:.1f})")

        for bar, m in zip(bars, marks):
            grade = calculate_grade(m)
            ax.annotate(
                f"{m:.0f}\n({grade})",
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center", va="bottom",
                color=self.t["text"],
                fontsize=8.5,
                fontweight="bold"
            )

        ax.set_ylim(0, max(105, max(marks, default=100) + 15))
        ax.set_ylabel("Marks (0-100)", color=self.t["text_muted"], fontsize=9)
        ax.set_title("Student Marks Comparison", color=self.t["text"], fontsize=11, fontweight="bold", pad=10)

        ax.tick_params(colors=self.t["text_muted"], labelsize=8.5)
        if len(names) > 5:
            ax.tick_params(axis="x", rotation=25)

        for spine in ax.spines.values():
            spine.set_color(self.t["chart_border"])

        ax.grid(axis="y", color=self.t["chart_border"], linestyle=":", alpha=0.5)
        ax.legend(facecolor=self.t["surface"], edgecolor=self.t["chart_border"],
                  labelcolor=self.t["text"], fontsize=7.5, loc="upper right")

    def _plot_donut_chart(self, ax, analytics):
        """Donut chart for grade breakdown using elegant monochromatic shades."""
        ax.set_facecolor(self.t["chart_bg"])

        grade_counts = analytics["grade_counts"]
        filtered = {g: count for g, count in grade_counts.items() if count > 0}

        if not filtered:
            ax.text(0.5, 0.5, "No Data", color=self.t["text_muted"], ha="center", va="center")
            return

        labels = list(filtered.keys())
        counts = list(filtered.values())

        # Monochromatic shades between #FFF9F9 and #162311
        if self.t["name"] == "dark":
            slice_palette = ["#FFF9F9", "#D5E2D3", "#A1B69E", "#71896E", "#475C44", "#2B3A28"]
        else:
            slice_palette = ["#162311", "#2D4026", "#4C6345", "#738C6C", "#A2B89C", "#D8E3D5"]

        slice_colors = slice_palette[:len(labels)]

        wedges, texts, autotexts = ax.pie(
            counts,
            labels=labels,
            autopct="%1.0f%%",
            startangle=140,
            colors=slice_colors,
            textprops={"color": self.t["text"], "fontsize": 8.5, "fontweight": "bold"},
            pctdistance=0.75,
            wedgeprops={"edgecolor": self.t["surface"], "linewidth": 2, "width": 0.45}
        )

        for at in autotexts:
            at.set_color("#162311" if self.t["name"] == "dark" else "#FFF9F9")
            at.set_fontsize(8)

        ax.text(0, 0, f"Total\n{analytics['total']}", ha="center", va="center",
                color=self.t["text"], fontsize=10, fontweight="bold")

        ax.set_title("Grade Distribution", color=self.t["text"], fontsize=11, fontweight="bold", pad=10)
        ax.legend(wedges, [f"{g}: {c} student(s)" for g, c in zip(labels, counts)],
                  loc="center left", bbox_to_anchor=(0.85, 0.5),
                  facecolor=self.t["surface"], edgecolor=self.t["chart_border"],
                  labelcolor=self.t["text"], fontsize=8)

    def _plot_course_chart(self, ax, analytics):
        """Horizontal bar chart comparing course averages."""
        ax.set_facecolor(self.t["chart_ax"])

        stats = analytics.get("course_stats", {})
        if not stats:
            ax.text(0.5, 0.5, "No Course Data", color=self.t["text_muted"], ha="center", va="center")
            return

        courses = list(stats.keys())
        averages = [data["average"] for data in stats.values()]
        counts = [data["count"] for data in stats.values()]

        y_pos = range(len(courses))
        bars = ax.barh(y_pos, averages, color=self.t["chart_bar"], edgecolor=self.t["chart_ax"], linewidth=0.8, height=0.45)

        for bar, avg, cnt in zip(bars, averages, counts):
            ax.annotate(
                f" {avg:.1f} avg ({cnt} student{'s' if cnt > 1 else ''})",
                xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                xytext=(6, 0),
                textcoords="offset points",
                ha="left", va="center",
                color=self.t["text"],
                fontsize=9,
                fontweight="bold"
            )

        ax.set_yticks(y_pos)
        ax.set_yticklabels(courses, color=self.t["text"], fontsize=9.5)
        ax.set_xlim(0, 115)
        ax.set_xlabel("Average Marks", color=self.t["text_muted"], fontsize=9)
        ax.set_title("Course Performance Summary", color=self.t["text"], fontsize=11, fontweight="bold", pad=10)

        ax.tick_params(colors=self.t["text_muted"])
        for spine in ax.spines.values():
            spine.set_color(self.t["chart_border"])
        ax.grid(axis="x", color=self.t["chart_border"], linestyle=":", alpha=0.5)

    def _plot_brackets_chart(self, ax, analytics):
        """Score bracket distribution histogram."""
        ax.set_facecolor(self.t["chart_ax"])

        brackets = analytics.get("score_ranges", {})
        labels = list(brackets.keys())
        values = list(brackets.values())

        if self.t["name"] == "dark":
            colors = ["#71896E", "#A1B69E", "#D5E2D3", "#FFF9F9"]
        else:
            colors = ["#A2B89C", "#738C6C", "#4C6345", "#162311"]

        bars = ax.bar(labels, values, color=colors, edgecolor=self.t["chart_ax"], linewidth=0.8, width=0.5)

        for bar, val in zip(bars, values):
            ax.annotate(
                f"{val} student(s)",
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center", va="bottom",
                color=self.t["text"],
                fontsize=9,
                fontweight="bold"
            )

        ax.set_ylim(0, max(values, default=1) + 2)
        ax.set_ylabel("Count", color=self.t["text_muted"], fontsize=9)
        ax.set_title("Score Bracket Distribution", color=self.t["text"], fontsize=11, fontweight="bold", pad=10)

        ax.tick_params(colors=self.t["text_muted"], labelsize=9)
        for spine in ax.spines.values():
            spine.set_color(self.t["chart_border"])
        ax.grid(axis="y", color=self.t["chart_border"], linestyle=":", alpha=0.5)

    # ==========================================================================
    # 2. VIEW STUDENT RECORDS (TABLE, LIVE SEARCH, DELETE)
    # ==========================================================================
    def show_view(self):
        """View student records with search and action buttons."""
        self._clear_content()
        self._refresh_state()

        self._page_header(
            "Student Records",
            f"Managing {len(self.students)} registered students",
            action_btn_text="➕ Add Student",
            action_cmd=self.show_add
        )

        toolbar = tk.Frame(self.content, bg=self.t["bg"])
        toolbar.pack(fill="x", pady=(0, 12))

        tk.Label(toolbar, text="Quick Search:", bg=self.t["bg"], fg=self.t["text_muted"], font=FONT_BODY).pack(side="left", padx=(0, 8))

        search_wrap, self.table_search = self._styled_entry(toolbar, width=24)
        search_wrap.pack(side="left", padx=(0, 12))
        self.table_search.bind("<KeyRelease>", lambda e: self._filter_table())

        self._btn_secondary(toolbar, "Delete Selected", self._delete_student, icon="🗑️").pack(side="right", padx=(8, 0))
        self._btn_secondary(toolbar, "Update Marks", self.show_update, icon="✏️").pack(side="right")

        table_box = tk.Frame(self.content, bg=self.t["surface"],
                             highlightthickness=1, highlightbackground=self.t["border"])
        table_box.pack(fill="both", expand=True)

        cols = ("roll_no", "name", "age", "course", "marks", "grade", "status")
        self.tree = ttk.Treeview(table_box, columns=cols, show="headings",
                                 style="Custom.Treeview", selectmode="browse")

        headers = [
            ("roll_no", "Roll Number", 110, "center"),
            ("name",    "Student Name", 190, "w"),
            ("age",     "Age",           70, "center"),
            ("course",  "Course",       160, "w"),
            ("marks",   "Marks",        100, "center"),
            ("grade",   "Grade",         90, "center"),
            ("status",  "Status",       120, "center"),
        ]

        for cid, chead, cwidth, canchor in headers:
            self.tree.heading(cid, text=chead)
            self.tree.column(cid, width=cwidth, anchor=canchor)

        sb = ttk.Scrollbar(table_box, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self._fill_table(self.students)

    def _fill_table(self, records):
        """Populate treeview rows."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for s in records:
            m = float(s.get("marks", 0))
            self.tree.insert("", "end", values=(
                s.get("roll_no", "N/A"),
                s.get("name", "N/A").title(),
                s.get("age", "N/A"),
                s.get("course", "N/A"),
                f"{m:.2f}",
                calculate_grade(m),
                "PASSED" if m >= 40 else "NEEDS SUPPORT"
            ))

    def _filter_table(self):
        """Filter table in real-time as user types."""
        q = self.table_search.get().strip().lower()
        if not q:
            self._fill_table(self.students)
            return

        filtered = [
            s for s in self.students
            if q in str(s.get("roll_no", "")).lower()
            or q in str(s.get("name", "")).lower()
            or q in str(s.get("course", "")).lower()
        ]
        self._fill_table(filtered)

    def _delete_student(self):
        """Delete student after user confirmation."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select Student", "Please select a row in the table to delete.")
            return

        row = self.tree.item(sel[0], "values")
        roll_no, name = row[0], row[1]

        if messagebox.askyesno("Confirm Delete", f"Delete record for {name} (Roll: {roll_no})?"):
            self.students = [s for s in self.students if s.get("roll_no") != roll_no]
            save_students(self.students)
            self.show_view()

    # ==========================================================================
    # 3. ADD STUDENT
    # ==========================================================================
    def show_add(self):
        """Form to add a new student record."""
        self._clear_content()
        self._page_header("Add New Student", "Register a new student into the system")

        card = tk.Frame(self.content, bg=self.t["surface"], padx=32, pady=28,
                        highlightthickness=1, highlightbackground=self.t["border"])
        card.pack(anchor="nw", fill="x", padx=(0, 40))
        card.columnconfigure(1, weight=1)

        self.e_roll   = self._form_field(card, "Roll Number",      0)
        self.e_name   = self._form_field(card, "Full Student Name", 1)
        self.e_age    = self._form_field(card, "Age (1-120)",       2)
        self.e_course = self._form_field(card, "Course / Stream",   3)
        self.e_marks  = self._form_field(card, "Marks (0 - 100)",   4)

        btn_row = tk.Frame(card, bg=self.t["surface"])
        btn_row.grid(row=5, column=0, columnspan=2, sticky="w", pady=(20, 0))

        self._btn_primary(btn_row, "Save Record", self._do_add, icon="💾").pack(side="left", padx=(0, 10))
        self._btn_secondary(btn_row, "Clear Form", self._clear_add).pack(side="left")

    def _clear_add(self):
        for e in (self.e_roll, self.e_name, self.e_age, self.e_course, self.e_marks):
            e.delete(0, "end")

    def _do_add(self):
        roll_no = self.e_roll.get().strip()
        name    = self.e_name.get().strip()
        course  = self.e_course.get().strip()

        if not roll_no or not name or not course:
            messagebox.showerror("Error", "Roll number, name, and course are required.")
            return

        if any(s.get("roll_no") == roll_no for s in self.students):
            messagebox.showerror("Duplicate", f"Roll number '{roll_no}' already exists.")
            return

        try:
            age = int(self.e_age.get().strip())
            marks = float(self.e_marks.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Age must be integer and marks numeric.")
            return

        if age <= 0 or age > 120 or marks < 0 or marks > 100:
            messagebox.showerror("Out of Range", "Check age (1-120) and marks (0-100).")
            return

        new_student = {
            "roll_no": roll_no, "name": name,
            "age": age, "course": course, "marks": round(marks, 2)
        }
        self.students.append(new_student)
        save_students(self.students)
        messagebox.showinfo("Success", f"Student '{name}' added successfully!")
        self._clear_add()
        self._refresh_state()

    # ==========================================================================
    # 4. SEARCH STUDENT
    # ==========================================================================
    def show_search(self):
        """Lookup student by roll number."""
        self._clear_content()
        self._page_header("Search Student", "Locate student details by roll number")

        search_bar = tk.Frame(self.content, bg=self.t["bg"])
        search_bar.pack(anchor="w", pady=(0, 16))

        tk.Label(search_bar, text="Roll Number:", bg=self.t["bg"], fg=self.t["text_muted"], font=FONT_BODY).pack(side="left", padx=(0, 8))

        wrap, self.e_search = self._styled_entry(search_bar, width=24)
        wrap.pack(side="left", padx=(0, 10))
        self.e_search.bind("<Return>", lambda e: self._do_search())

        self._btn_primary(search_bar, "Search", self._do_search, icon="🔍").pack(side="left")

        self.search_area = tk.Frame(self.content, bg=self.t["bg"])
        self.search_area.pack(fill="x", pady=10)

    def _do_search(self):
        for w in self.search_area.winfo_children():
            w.destroy()

        r = self.e_search.get().strip()
        found = next((s for s in self.students if s.get("roll_no") == r), None)

        if not found:
            box = tk.Frame(self.search_area, bg=self.t["surface"], padx=24, pady=20,
                           highlightthickness=1, highlightbackground=self.t["border"])
            box.pack(anchor="w", fill="x")
            tk.Label(box, text=f"No student found with Roll Number '{r}'.",
                     bg=self.t["surface"], fg=self.t["text"], font=FONT_BOLD).pack()
            return

        marks = float(found.get("marks", 0))
        grade = calculate_grade(marks)

        card = tk.Frame(self.search_area, bg=self.t["surface"], padx=28, pady=24,
                        highlightthickness=1, highlightbackground=self.t["border"])
        card.pack(anchor="w", fill="x")

        # Title & badge
        top = tk.Frame(card, bg=self.t["surface"])
        top.pack(fill="x", pady=(0, 14))

        tk.Label(top, text=found.get("name", "").title(), bg=self.t["surface"],
                 fg=self.t["text"], font=FONT_TITLE).pack(side="left")

        badge = tk.Frame(top, bg=self.t["btn_primary_bg"], padx=10, pady=3)
        badge.pack(side="right")
        tk.Label(badge, text=f"GRADE {grade}", bg=self.t["btn_primary_bg"],
                 fg=self.t["btn_primary_fg"], font=("Segoe UI", 9, "bold")).pack()

        details = [
            ("Roll Number", found.get("roll_no")),
            ("Age",         f"{found.get('age')} years"),
            ("Course",      found.get("course")),
            ("Marks",       f"{marks:.2f} / 100"),
            ("Remarks",     get_grade_remark(grade)),
            ("Status",      "Passing Standard" if marks >= 40 else "Needs Support"),
        ]

        grid = tk.Frame(card, bg=self.t["surface"])
        grid.pack(fill="x")
        for i, (k, v) in enumerate(details):
            row = i // 2
            col = (i % 2) * 2
            tk.Label(grid, text=f"{k}:", bg=self.t["surface"], fg=self.t["text_muted"],
                     font=FONT_SMALL).grid(row=row, column=col, sticky="w", padx=(0, 8), pady=4)
            tk.Label(grid, text=str(v), bg=self.t["surface"], fg=self.t["text"],
                     font=FONT_BOLD).grid(row=row, column=col + 1, sticky="w", padx=(0, 32), pady=4)

    # ==========================================================================
    # 5. UPDATE MARKS
    # ==========================================================================
    def show_update(self):
        """Update student marks."""
        self._clear_content()
        self._page_header("Update Student Marks", "Modify marks for an existing student record")

        card = tk.Frame(self.content, bg=self.t["surface"], padx=32, pady=28,
                        highlightthickness=1, highlightbackground=self.t["border"])
        card.pack(anchor="nw", fill="x", padx=(0, 40))
        card.columnconfigure(1, weight=1)

        self.e_upd_roll  = self._form_field(card, "Roll Number",         0)
        self.e_upd_marks = self._form_field(card, "New Marks (0 - 100)", 1)

        btn_row = tk.Frame(card, bg=self.t["surface"])
        btn_row.grid(row=2, column=0, columnspan=2, sticky="w", pady=(20, 0))

        self._btn_primary(btn_row, "Update Marks", self._do_update, icon="🔄").pack(side="left")

    def _do_update(self):
        r = self.e_upd_roll.get().strip()
        found = next((s for s in self.students if s.get("roll_no") == r), None)

        if not found:
            messagebox.showerror("Not Found", f"No student found with Roll Number '{r}'.")
            return

        try:
            m = float(self.e_upd_marks.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Marks must be numeric.")
            return

        if m < 0 or m > 100:
            messagebox.showerror("Out of Range", "Marks must be between 0 and 100.")
            return

        old_m = found.get("marks", 0)
        found["marks"] = round(m, 2)
        save_students(self.students)

        messagebox.showinfo("Success", f"Marks updated for {found['name']}:\n\n{old_m} ➔ {m}")
        self.e_upd_roll.delete(0, "end")
        self.e_upd_marks.delete(0, "end")
        self._refresh_state()

    # ==========================================================================
    # 6. ACADEMIC INSIGHTS
    # ==========================================================================
    def show_insights(self):
        """Academic highlights & guidance."""
        self._clear_content()
        self._page_header("Academic Insights", "Qualitative review and performance standings")

        if not self.students:
            tk.Label(self.content, text="No student records available.",
                     bg=self.t["bg"], fg=self.t["text_muted"], font=FONT_BODY).pack()
            return

        insights = get_insights(self.students)
        top = insights["top_performer"]
        struggling = insights["struggling_students"]

        # Top Performer
        top_card = tk.Frame(self.content, bg=self.t["surface"], padx=24, pady=18,
                            highlightthickness=1, highlightbackground=self.t["border"])
        top_card.pack(fill="x", pady=(0, 16))

        tk.Label(top_card, text="🏆 TOP PERFORMER", bg=self.t["surface"],
                 fg=self.t["text_muted"], font=("Segoe UI", 9, "bold")).pack(anchor="w")

        if top:
            tm = float(top.get("marks", 0))
            tk.Label(top_card, text=f"{top.get('name', '').title()}  •  {tm:.1f} Marks ({calculate_grade(tm)})",
                     bg=self.t["surface"], fg=self.t["text"], font=FONT_H1).pack(anchor="w", pady=(4, 2))
            tk.Label(top_card, text=f"Course: {top.get('course')}  |  Roll Number: {top.get('roll_no')}",
                     bg=self.t["surface"], fg=self.t["text_muted"], font=FONT_SMALL).pack(anchor="w")

        # Class Average
        avg_card = tk.Frame(self.content, bg=self.t["surface"], padx=24, pady=16,
                            highlightthickness=1, highlightbackground=self.t["border"])
        avg_card.pack(fill="x", pady=(0, 16))

        tk.Label(avg_card, text="📊 CLASS AVERAGE STANDING", bg=self.t["surface"],
                 fg=self.t["text_muted"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(avg_card, text=f"Overall Class Mean: {insights['average']:.2f} Marks",
                 bg=self.t["surface"], fg=self.t["text"], font=FONT_H1).pack(anchor="w", pady=(4, 2))

        # Academic Support List
        sup_card = tk.Frame(self.content, bg=self.t["surface"], padx=24, pady=18,
                            highlightthickness=1, highlightbackground=self.t["border"])
        sup_card.pack(fill="x")

        tk.Label(sup_card, text="⚠️ STUDENTS NEEDING SUPPORT (< 40 marks)", bg=self.t["surface"],
                 fg=self.t["text_muted"], font=("Segoe UI", 9, "bold")).pack(anchor="w")

        if not struggling:
            tk.Label(sup_card, text="✓ All enrolled students currently meet the passing threshold (≥ 40 marks).",
                     bg=self.t["surface"], fg=self.t["text"], font=FONT_BODY).pack(anchor="w", pady=(8, 0))
        else:
            for s in struggling:
                row = tk.Frame(sup_card, bg=self.t["surface"])
                row.pack(anchor="w", pady=4)
                tk.Label(row, text="•", bg=self.t["surface"], fg=self.t["text"], font=FONT_BOLD).pack(side="left", padx=(0, 6))
                tk.Label(row, text=f"{s.get('name', '').title()} (Roll {s.get('roll_no')}) — {s.get('marks')} Marks ({s.get('course')})",
                         bg=self.t["surface"], fg=self.t["text"], font=FONT_BODY).pack(side="left")


# ==============================================================================
# ENTRYPOINT
# ==============================================================================
if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()

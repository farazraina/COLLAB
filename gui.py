# =====================================================================
# gui.py
# Graphical User Interface (GUI) for Student Management System.
# Built with Tkinter and Matplotlib.
#
# Color Theme:
#   - Primary Light : #fcf8f9 (Porcelain Pearl White)
#   - Primary Crimson: #a21721 (Cardinal Crimson Ruby)
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
from grade_calculator import calculate_grade, get_grade_remark


# =====================================================================
# 1. COLOR THEMES (#fcf8f9 and #a21721)
# =====================================================================

# Light Theme (Default: Clean Porcelain Pearl & Cardinal Crimson)
LIGHT_THEME = {
    "name": "light",
    "bg":             "#FCF8F9",   # Porcelain Pearl White canvas
    "sidebar":        "#F3E9EB",   # Soft rose-tinted gray sidebar
    "card":           "#FFFFFF",   # Crisp white card surface
    "card_hover":     "#FAF2F3",   # Card hover
    "input_bg":       "#FFFFFF",   # Entry box background
    "border":         "#E8D9DC",   # Subtle border
    "text":           "#1C0F11",   # Deep dark charcoal text
    "text_muted":     "#6E5659",   # Soft taupe-rose muted text
    "accent":         "#A21721",   # Signature Cardinal Crimson
    "accent_hover":   "#BF2430",   # Brighter crimson hover
    "btn_primary_bg": "#A21721",   # Crimson primary button
    "btn_primary_fg": "#FCF8F9",   # White text on crimson button
    "btn_primary_hov":"#831019",   # Dark crimson hover
    "btn_sec_bg":     "#F2E6E8",   # Neutral soft secondary button
    "btn_sec_fg":     "#A21721",   # Crimson text on secondary button
    "btn_sec_hov":    "#E6D4D7",   # Secondary button hover
    "chart_bg":       "#FFFFFF",   # Matplotlib figure background
    "chart_plot":     "#FCF8F9",   # Matplotlib axes plot area
    "chart_bar":      "#A21721",   # Main bar color
    "chart_bar_alt":  "#8E7679",   # Failing student bar color
    "chart_border":   "#E8D9DC",   # Spines & gridlines
}

# Dark Theme (Obsidian Crimson Dark)
DARK_THEME = {
    "name": "dark",
    "bg":             "#150C0E",   # Deep obsidian dark canvas
    "sidebar":        "#0E0709",   # Deeper dark sidebar
    "card":           "#201215",   # Dark crimson-tinted card surface
    "card_hover":     "#2C1A1E",   # Card hover
    "input_bg":       "#13090B",   # Entry box background
    "border":         "#381E23",   # Subtle dark border
    "text":           "#FCF8F9",   # Crisp porcelain white text
    "text_muted":     "#BBA4A7",   # Soft silver-rose muted text
    "accent":         "#A21721",   # Signature Cardinal Crimson
    "accent_hover":   "#BF2430",   # Brighter crimson hover
    "btn_primary_bg": "#A21721",   # Crimson primary button
    "btn_primary_fg": "#FCF8F9",   # White text on crimson button
    "btn_primary_hov":"#BF2430",   # Hover state
    "btn_sec_bg":     "#2C1A1E",   # Neutral dark button
    "btn_sec_fg":     "#FCF8F9",   # White text
    "btn_sec_hov":    "#3B2329",   # Hover state
    "chart_bg":       "#201215",   # Matplotlib figure background
    "chart_plot":     "#150C0E",   # Matplotlib axes plot area
    "chart_bar":      "#A21721",   # Main bar color
    "chart_bar_alt":  "#6B5356",   # Failing student bar color
    "chart_border":   "#381E23",   # Spines & gridlines
}

# Fonts
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_H1    = ("Segoe UI", 13, "bold")
FONT_BODY  = ("Segoe UI", 10)
FONT_BOLD  = ("Segoe UI", 10, "bold")
FONT_SMALL = ("Segoe UI", 9)


# =====================================================================
# 2. MAIN APPLICATION CLASS
# =====================================================================
class StudentApp(tk.Tk):
    """
    Main Application Window.
    Inherits from tk.Tk (the main Tkinter window).
    """

    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Academic Management Portal • Analytics Dashboard")
        self.geometry("1180x750")
        self.minsize(1020, 640)

        # Default to Light Theme (#FCF8F9 & #A21721)
        self.theme = LIGHT_THEME
        self.configure(bg=self.theme["bg"])

        # Load students list from file
        self.students = load_students()

        # Track active page and graph mode
        self.current_page = "dashboard"
        self.current_graph = "dual"
        self.chart_canvas = None

        # Build user interface
        self._setup_table_style()
        self._build_sidebar_and_content()

    # -----------------------------------------------------------------
    # THEME AND STYLES
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
            rowheight=32,
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

        for widget in self.winfo_children():
            widget.destroy()

        self._build_sidebar_and_content()

    # -----------------------------------------------------------------
    # WIDGET CREATION HELPERS
    # -----------------------------------------------------------------
    def make_primary_button(self, parent, text, command):
        """Creates signature pill button in Cardinal Crimson #A21721."""
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

    def make_input_entry(self, parent, width=30):
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
            width=width
        )
        entry.pack(fill="both", expand=True, padx=8, pady=6)
        entry.bind("<FocusIn>",  lambda e: border_frame.config(bg=self.theme["accent"]))
        entry.bind("<FocusOut>", lambda e: border_frame.config(bg=self.theme["border"]))
        return border_frame, entry

    def make_form_row(self, parent, label_text, row_num):
        """Adds label and entry input to a form grid."""
        tk.Label(
            parent,
            text=label_text,
            bg=self.theme["card"],
            fg=self.theme["text_muted"],
            font=FONT_BODY,
            anchor="w"
        ).grid(row=row_num, column=0, sticky="w", padx=(0, 16), pady=8)

        frame, entry = self.make_input_entry(parent, width=32)
        frame.grid(row=row_num, column=1, sticky="ew", pady=8)
        return entry

    # -----------------------------------------------------------------
    # BASE LAYOUT (SIDEBAR & CONTENT AREA)
    # -----------------------------------------------------------------
    def _build_sidebar_and_content(self):
        """Constructs left sidebar and main content frame."""
        # 1. Left Sidebar
        self.sidebar = tk.Frame(self, bg=self.theme["sidebar"], width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand Header
        brand_box = tk.Frame(self.sidebar, bg=self.theme["sidebar"], padx=18, pady=20)
        brand_box.pack(fill="x")

        # Crimson Pill badge
        badge = tk.Frame(brand_box, bg=self.theme["accent"], padx=9, pady=3)
        badge.pack(anchor="w", pady=(0, 8))
        tk.Label(
            badge,
            text="● ACADEMIC SUITE",
            bg=self.theme["accent"],
            fg="#FCF8F9",
            font=("Segoe UI", 8, "bold")
        ).pack()

        tk.Label(
            brand_box,
            text="Student Hub",
            bg=self.theme["sidebar"],
            fg=self.theme["text"],
            font=FONT_TITLE,
            anchor="w"
        ).pack(anchor="w")

        tk.Label(
            brand_box,
            text="#fcf8f9 • #a21721 Edition",
            bg=self.theme["sidebar"],
            fg=self.theme["text_muted"],
            font=FONT_SMALL,
            anchor="w"
        ).pack(anchor="w")

        tk.Frame(self.sidebar, bg=self.theme["border"], height=1).pack(fill="x", padx=16, pady=12)

        # Navigation Buttons list
        menu_items = [
            ("📊 Dashboard & Graphs", "dashboard", self.show_dashboard),
            ("📋 Student Records",    "view",      self.show_view),
            ("➕ Add Student",        "add",       self.show_add),
            ("🔍 Search Student",     "search",    self.show_search),
            ("✏️ Update Marks",       "update",    self.show_update),
            ("💡 Academic Insights",  "insights",  self.show_insights),
        ]

        self.nav_buttons = {}
        for title, key, cmd in menu_items:
            is_active = (self.current_page == key)
            btn = tk.Button(
                self.sidebar,
                text=f"  {title}",
                command=lambda c=cmd, k=key: self._switch_page(c, k),
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
            self.nav_buttons[key] = btn

        # Theme Switcher at bottom of sidebar
        bottom_box = tk.Frame(self.sidebar, bg=self.theme["card"], padx=12, pady=12)
        bottom_box.pack(side="bottom", fill="x", padx=12, pady=16)

        theme_text = "🌙 Dark Mode" if self.theme["name"] == "light" else "☀️ Light Mode (#FCF8F9)"
        self.make_secondary_button(bottom_box, theme_text, self.toggle_theme).pack(fill="x")

        tk.Label(
            bottom_box,
            text=f"Total: {len(self.students)} students",
            bg=self.theme["card"],
            fg=self.theme["text_muted"],
            font=FONT_SMALL
        ).pack(anchor="w", pady=(8, 0))

        # 2. Main Content Area
        self.content = tk.Frame(self, bg=self.theme["bg"])
        self.content.pack(side="left", fill="both", expand=True, padx=24, pady=24)

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

    def _switch_page(self, command, page_key):
        """Switches page and updates active sidebar button."""
        self.current_page = page_key
        for key, btn in self.nav_buttons.items():
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
    # 3. DASHBOARD PAGE (KPI CARDS + GRAPHS)
    # =====================================================================
    def show_dashboard(self):
        """Displays KPI summary cards and clean, non-overlapping graphs."""
        self._clear_content()
        self.students = load_students()
        self._make_header("Performance Dashboard", "Class performance summary & visual graphs (#fcf8f9 • #a21721)")

        if not self.students:
            empty_box = tk.Frame(self.content, bg=self.theme["card"], padx=24, pady=24)
            empty_box.pack(fill="x")
            tk.Label(empty_box, text="No students registered yet.",
                     bg=self.theme["card"], fg=self.theme["text"], font=FONT_H1).pack()
            self.make_primary_button(empty_box, "Add First Student", self.show_add).pack(pady=(12, 0))
            return

        analytics = calculate_analytics(self.students)

        # Row of 6 KPI Stat Cards
        kpi_row = tk.Frame(self.content, bg=self.theme["bg"])
        kpi_row.pack(fill="x", pady=(0, 14))

        cards = [
            ("Total Students", str(analytics["total"])),
            ("Class Average",  str(analytics["average"])),
            ("Highest Marks",  str(analytics["highest"])),
            ("Lowest Marks",   str(analytics["lowest"])),
            ("Pass Rate",      f"{analytics['pass_percentage']}%"),
            ("Failed (<40)",   str(analytics["failed"]))
        ]

        for i, (label, val) in enumerate(cards):
            card = tk.Frame(kpi_row, bg=self.theme["card"], padx=14, pady=12,
                            highlightthickness=1, highlightbackground=self.theme["border"])
            card.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 8, 0))

            tk.Label(card, text=label, bg=self.theme["card"],
                     fg=self.theme["text_muted"], font=FONT_SMALL).pack(anchor="w")
            val_color = self.theme["accent"] if label in ("Highest Marks", "Pass Rate") else self.theme["text"]
            tk.Label(card, text=val, bg=self.theme["card"],
                     fg=val_color, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(4, 0))

        # Graph Mode Selector Buttons
        ctrl_bar = tk.Frame(self.content, bg=self.theme["card"], padx=10, pady=8,
                            highlightthickness=1, highlightbackground=self.theme["border"])
        ctrl_bar.pack(fill="x", pady=(0, 12))

        tk.Label(ctrl_bar, text="CHOOSE GRAPH:", bg=self.theme["card"],
                 fg=self.theme["text_muted"], font=("Segoe UI", 8, "bold")).pack(side="left", padx=(4, 10))

        graph_options = [
            ("🔲 Dual Charts",      "dual"),
            ("📊 Bar Chart (Marks)", "bar"),
            ("🍩 Donut Chart (Grade)", "donut"),
            ("📚 Course Averages",   "course"),
            ("📉 Score Brackets",    "brackets")
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
                font=("Segoe UI", 9, "bold" if is_active else "normal"),
                relief="flat",
                cursor="hand2",
                padx=10,
                pady=4,
                bd=0
            )
            btn.pack(side="left", padx=4)
            self.graph_btns[mode] = btn

        # Container for Matplotlib Chart Canvas
        self.chart_container = tk.Frame(self.content, bg=self.theme["card"],
                                        highlightthickness=1, highlightbackground=self.theme["border"])
        self.chart_container.pack(fill="both", expand=True)

        self._draw_charts(analytics)

    def _switch_graph(self, mode):
        """Switches the chart view."""
        self.current_graph = mode
        for m, btn in self.graph_btns.items():
            if m == mode:
                btn.config(bg=self.theme["accent"], fg="#FCF8F9", font=("Segoe UI", 9, "bold"))
            else:
                btn.config(bg=self.theme["btn_sec_bg"], fg=self.theme["btn_sec_fg"], font=("Segoe UI", 9, "normal"))

        analytics = calculate_analytics(self.students)
        self._draw_charts(analytics)

    def _draw_charts(self, analytics):
        """Draws clean charts with proper spacing, margins, and non-overlapping text."""
        for w in self.chart_container.winfo_children():
            w.destroy()

        mode = self.current_graph

        # 1. Dual View (Both Bar Chart and Donut Chart side by side)
        if mode == "dual":
            fig = Figure(figsize=(9.6, 4.4), facecolor=self.theme["chart_bg"], dpi=100)
            ax1 = fig.add_subplot(1, 2, 1)
            ax2 = fig.add_subplot(1, 2, 2)
            self._plot_bar(ax1)
            self._plot_donut(ax2, analytics)
            fig.tight_layout(pad=2.2)

        # 2. Single Bar Chart
        elif mode == "bar":
            fig = Figure(figsize=(9.6, 4.4), facecolor=self.theme["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_bar(ax, detailed=True)
            fig.tight_layout(pad=2.0)

        # 3. Single Donut Chart
        elif mode == "donut":
            fig = Figure(figsize=(9.6, 4.4), facecolor=self.theme["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_donut(ax, analytics, detailed=True)
            fig.tight_layout(pad=2.0)

        # 4. Course Performance Bar Chart
        elif mode == "course":
            fig = Figure(figsize=(9.6, 4.4), facecolor=self.theme["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_course(ax, analytics)
            fig.tight_layout(pad=2.0)

        # 5. Score Brackets Histogram
        else:
            fig = Figure(figsize=(9.6, 4.4), facecolor=self.theme["chart_bg"], dpi=100)
            ax = fig.add_subplot(1, 1, 1)
            self._plot_brackets(ax, analytics)
            fig.tight_layout(pad=2.0)

        # Embed into Tkinter
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

    # -----------------------------------------------------------------
    # GRAPH PLOTTING FUNCTIONS (PROPER SPACING & FORMATTING)
    # -----------------------------------------------------------------
    def _plot_bar(self, ax, detailed=False):
        """Plots bar chart of student marks with rotated names and neat values."""
        ax.set_facecolor(self.theme["chart_plot"])

        # Format student names cleanly so they never overlap
        names = []
        for s in self.students:
            full = s["name"].strip().title()
            parts = full.split()
            if len(parts) > 1:
                short_name = f"{parts[0]} {parts[1][0]}."
            else:
                short_name = full[:9]
            names.append(short_name)

        marks = [float(s["marks"]) for s in self.students]
        x_indices = range(len(names))

        # Dynamic bar width based on student count
        n_students = len(marks)
        bar_width = 0.55 if n_students <= 6 else max(0.4, 4.5 / n_students)

        # Cardinal Crimson #A21721 for pass, muted for fail
        colors = [self.theme["chart_bar"] if m >= 40 else self.theme["chart_bar_alt"] for m in marks]
        bars = ax.bar(x_indices, marks, color=colors, width=bar_width, edgecolor=self.theme["border"], linewidth=0.8)

        # Annotations on top of bars
        for bar, m in zip(bars, marks):
            grade = calculate_grade(m)
            label = f"{m:.0f}\n({grade})" if (detailed or n_students <= 6) else f"{m:.0f}"
            ax.annotate(
                label,
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center", va="bottom",
                color=self.theme["text"],
                fontsize=8 if n_students > 8 else 8.5,
                fontweight="bold"
            )

        # Properly rotate student names to prevent jumbled overlapping
        ax.set_xticks(list(x_indices))
        rotation_angle = 35 if n_students >= 5 else 0
        ha_align = "right" if rotation_angle > 0 else "center"
        ax.set_xticklabels(names, rotation=rotation_angle, ha=ha_align, fontsize=8, color=self.theme["text"])

        # Benchmark reference lines
        avg = sum(marks) / len(marks)
        ax.axhline(40, color=self.theme["text_muted"], linestyle="--", linewidth=1.1, alpha=0.8, label="Pass (40)")
        ax.axhline(avg, color=self.theme["accent"], linestyle=":", linewidth=1.2, alpha=0.9, label=f"Avg ({avg:.1f})")

        ax.set_ylim(0, max(112, max(marks, default=100) + 12))
        ax.set_ylabel("Marks (0-100)", color=self.theme["text_muted"], fontsize=8.5)
        ax.set_title("Student Marks Comparison", color=self.theme["accent"], fontsize=11, fontweight="bold", pad=8)
        ax.tick_params(colors=self.theme["text_muted"], labelsize=8)

        for spine in ax.spines.values():
            spine.set_color(self.theme["chart_border"])
        ax.grid(axis="y", color=self.theme["chart_border"], linestyle=":", alpha=0.7)
        ax.legend(facecolor=self.theme["card"], edgecolor=self.theme["chart_border"],
                  labelcolor=self.theme["text"], fontsize=7.5, loc="upper right")

    def _plot_donut(self, ax, analytics, detailed=False):
        """Plots clean donut chart with side legend to avoid crowded slice text."""
        ax.set_facecolor(self.theme["chart_bg"])

        grade_counts = analytics["grade_counts"]
        labels = []
        counts = []
        for g, c in grade_counts.items():
            if c > 0:
                labels.append(g)
                counts.append(c)

        if not counts:
            ax.text(0.5, 0.5, "No Data", color=self.theme["text_muted"], ha="center", va="center")
            return

        # Slices in a rich Cardinal Crimson #A21721 gradient
        crimson_palette = ["#A21721", "#BF2632", "#D64852", "#E87881", "#F2A8AF", "#FBD3D7"]
        slice_colors = crimson_palette[:len(labels)]

        # Draw donut without crowded outer text labels (legend handles labels)
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

        # Center hole text
        ax.text(0, 0, f"Total\n{analytics['total']}", ha="center", va="center",
                color=self.theme["accent"], fontsize=10, fontweight="bold")

        ax.set_title("Grade Distribution", color=self.theme["accent"], fontsize=11, fontweight="bold", pad=8)

        # Clean legend on the right side
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

        y_positions = range(len(courses))
        bars = ax.barh(y_positions, averages, color=self.theme["chart_bar"], height=0.45,
                       edgecolor=self.theme["border"])

        for bar, avg in zip(bars, averages):
            ax.annotate(
                f" {avg:.1f} avg",
                xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                xytext=(6, 0),
                textcoords="offset points",
                ha="left", va="center",
                color=self.theme["text"],
                fontsize=9,
                fontweight="bold"
            )

        ax.set_yticks(y_positions)
        ax.set_yticklabels(courses, color=self.theme["text"], fontsize=9.5)
        ax.set_xlim(0, 115)
        ax.set_xlabel("Average Marks", color=self.theme["text_muted"], fontsize=9)
        ax.set_title("Course Performance Summary", color=self.theme["accent"], fontsize=11, fontweight="bold", pad=8)
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
    # 4. VIEW STUDENT RECORDS (TABLE, LIVE SEARCH, DELETE)
    # =====================================================================
    def show_view(self):
        """Displays table of all students with search and delete options."""
        self._clear_content()
        self.students = load_students()
        self._make_header("Student Records", f"{len(self.students)} student(s) registered")

        toolbar = tk.Frame(self.content, bg=self.theme["bg"])
        toolbar.pack(fill="x", pady=(0, 12))

        tk.Label(toolbar, text="Search:", bg=self.theme["bg"],
                 fg=self.theme["text_muted"], font=FONT_BODY).pack(side="left", padx=(0, 8))

        search_wrap, self.search_box = self.make_input_entry(toolbar, width=24)
        search_wrap.pack(side="left", padx=(0, 12))
        self.search_box.bind("<KeyRelease>", lambda e: self._filter_students())

        self.make_secondary_button(toolbar, "Delete Selected", self._delete_student).pack(side="right", padx=(8, 0))
        self.make_secondary_button(toolbar, "Update Marks", self.show_update).pack(side="right")

        table_box = tk.Frame(self.content, bg=self.theme["card"],
                             highlightthickness=1, highlightbackground=self.theme["border"])
        table_box.pack(fill="both", expand=True)

        columns = ("roll_no", "name", "age", "course", "marks", "grade", "status")
        self.tree = ttk.Treeview(table_box, columns=columns, show="headings",
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

        for col_id, col_text, col_width, col_align in headers:
            self.tree.heading(col_id, text=col_text)
            self.tree.column(col_id, width=col_width, anchor=col_align)

        sb = ttk.Scrollbar(table_box, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self._populate_table(self.students)

    def _populate_table(self, records):
        """Fills treeview rows with student data."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for s in records:
            marks = float(s["marks"])
            grade = calculate_grade(marks)
            status = "PASSED" if marks >= 40 else "FAILED"
            self.tree.insert("", "end", values=(
                s["roll_no"], s["name"].title(), s["age"], s["course"],
                f"{marks:.2f}", grade, status
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
                q in str(s["course"]).lower()):
                filtered.append(s)

        self._populate_table(filtered)

    def _delete_student(self):
        """Deletes selected student record."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Student", "Please select a student row to delete.")
            return

        row = self.tree.item(selected[0], "values")
        roll_no, name = row[0], row[1]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete:\n\n{name} (Roll: {roll_no})?"):
            self.students = [s for s in self.students if s["roll_no"] != roll_no]
            save_students(self.students)
            self.show_view()

    # =====================================================================
    # 5. ADD STUDENT PAGE
    # =====================================================================
    def show_add(self):
        """Form to register a new student."""
        self._clear_content()
        self._make_header("Add New Student", "Enter student details to save into the system")

        card = tk.Frame(self.content, bg=self.theme["card"], padx=32, pady=28,
                        highlightthickness=1, highlightbackground=self.theme["border"])
        card.pack(anchor="nw", fill="x", padx=(0, 40))
        card.columnconfigure(1, weight=1)

        self.e_roll   = self.make_form_row(card, "Roll Number",      0)
        self.e_name   = self.make_form_row(card, "Full Name",        1)
        self.e_age    = self.make_form_row(card, "Age (1-120)",      2)
        self.e_course = self.make_form_row(card, "Course / Stream",  3)
        self.e_marks  = self.make_form_row(card, "Marks (0 - 100)",  4)

        btn_row = tk.Frame(card, bg=self.theme["card"])
        btn_row.grid(row=5, column=0, columnspan=2, sticky="w", pady=(20, 0))

        self.make_primary_button(btn_row, "Save Student", self._do_add).pack(side="left", padx=(0, 10))
        self.make_secondary_button(btn_row, "Clear Form", self._clear_add_form).pack(side="left")

    def _clear_add_form(self):
        for entry in (self.e_roll, self.e_name, self.e_age, self.e_course, self.e_marks):
            entry.delete(0, "end")

    def _do_add(self):
        roll_no = self.e_roll.get().strip()
        name    = self.e_name.get().strip()
        course  = self.e_course.get().strip()

        if not roll_no or not name or not course:
            messagebox.showerror("Error", "Roll number, name, and course are required.")
            return

        for s in self.students:
            if s["roll_no"] == roll_no:
                messagebox.showerror("Duplicate", f"Roll number '{roll_no}' already exists.")
                return

        try:
            age = int(self.e_age.get().strip())
            marks = float(self.e_marks.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Age and marks must be numeric.")
            return

        if age <= 0 or age > 120 or marks < 0 or marks > 100:
            messagebox.showerror("Out of Range", "Check age (1-120) and marks (0-100).")
            return

        student = {
            "roll_no": roll_no,
            "name": name,
            "age": age,
            "course": course,
            "marks": round(marks, 2)
        }
        self.students.append(student)
        save_students(self.students)

        messagebox.showinfo("Success", f"Student '{name}' added successfully!")
        self._clear_add_form()

    # =====================================================================
    # 6. SEARCH STUDENT PAGE
    # =====================================================================
    def show_search(self):
        """Search student by roll number."""
        self._clear_content()
        self._make_header("Search Student", "Find a student's full record by roll number")

        search_bar = tk.Frame(self.content, bg=self.theme["bg"])
        search_bar.pack(anchor="w", pady=(0, 16))

        tk.Label(search_bar, text="Roll Number:", bg=self.theme["bg"],
                 fg=self.theme["text_muted"], font=FONT_BODY).pack(side="left", padx=(0, 8))

        wrap, self.e_search = self.make_input_entry(search_bar, width=24)
        wrap.pack(side="left", padx=(0, 10))
        self.e_search.bind("<Return>", lambda e: self._do_search())

        self.make_primary_button(search_bar, "Search", self._do_search).pack(side="left")

        self.search_result_box = tk.Frame(self.content, bg=self.theme["bg"])
        self.search_result_box.pack(fill="x", pady=10)

    def _do_search(self):
        for child in self.search_result_box.winfo_children():
            child.destroy()

        r = self.e_search.get().strip()
        found = None
        for s in self.students:
            if s["roll_no"] == r:
                found = s
                break

        if not found:
            box = tk.Frame(self.search_result_box, bg=self.theme["card"], padx=20, pady=16)
            box.pack(anchor="w", fill="x")
            tk.Label(box, text=f"No student found with Roll Number '{r}'.",
                     bg=self.theme["card"], fg=self.theme["text"], font=FONT_BOLD).pack()
            return

        marks = float(found["marks"])
        grade = calculate_grade(marks)

        card = tk.Frame(self.search_result_box, bg=self.theme["card"], padx=24, pady=20,
                        highlightthickness=1, highlightbackground=self.theme["border"])
        card.pack(anchor="w", fill="x")

        tk.Label(card, text=found["name"].title(), bg=self.theme["card"],
                 fg=self.theme["accent"], font=FONT_TITLE).pack(anchor="w", pady=(0, 10))

        details = [
            ("Roll Number", found["roll_no"]),
            ("Age",         f"{found['age']} years"),
            ("Course",      found["course"]),
            ("Marks",       f"{marks} / 100"),
            ("Grade",       f"{grade} ({get_grade_remark(grade)})"),
            ("Status",      "Passed" if marks >= 40 else "Needs Support")
        ]

        for k, v in details:
            row = tk.Frame(card, bg=self.theme["card"])
            row.pack(anchor="w", pady=2)
            tk.Label(row, text=f"{k}:", width=14, anchor="w", bg=self.theme["card"],
                     fg=self.theme["text_muted"], font=FONT_SMALL).pack(side="left")
            tk.Label(row, text=str(v), bg=self.theme["card"],
                     fg=self.theme["text"], font=FONT_BOLD).pack(side="left")

    # =====================================================================
    # 7. UPDATE MARKS PAGE
    # =====================================================================
    def show_update(self):
        """Update student marks form."""
        self._clear_content()
        self._make_header("Update Marks", "Change marks for an existing student")

        card = tk.Frame(self.content, bg=self.theme["card"], padx=32, pady=28,
                        highlightthickness=1, highlightbackground=self.theme["border"])
        card.pack(anchor="nw", fill="x", padx=(0, 40))
        card.columnconfigure(1, weight=1)

        self.e_upd_roll  = self.make_form_row(card, "Roll Number",         0)
        self.e_upd_marks = self.make_form_row(card, "New Marks (0 - 100)", 1)

        btn_row = tk.Frame(card, bg=self.theme["card"])
        btn_row.grid(row=2, column=0, columnspan=2, sticky="w", pady=(20, 0))

        self.make_primary_button(btn_row, "Update Marks", self._do_update).pack(side="left")

    def _do_update(self):
        r = self.e_upd_roll.get().strip()
        found = None
        for s in self.students:
            if s["roll_no"] == r:
                found = s
                break

        if not found:
            messagebox.showerror("Not Found", f"No student found with Roll Number '{r}'.")
            return

        try:
            new_marks = float(self.e_upd_marks.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Marks must be numeric.")
            return

        if new_marks < 0 or new_marks > 100:
            messagebox.showerror("Out of Range", "Marks must be between 0 and 100.")
            return

        old_marks = found["marks"]
        found["marks"] = round(new_marks, 2)
        save_students(self.students)

        messagebox.showinfo("Success", f"Marks for {found['name']} updated: {old_marks} ➔ {new_marks}")
        self.e_upd_roll.delete(0, "end")
        self.e_upd_marks.delete(0, "end")

    # =====================================================================
    # 8. ACADEMIC INSIGHTS PAGE
    # =====================================================================
    def show_insights(self):
        """Academic highlights, top performer, and students needing support."""
        self._clear_content()
        self._make_header("Academic Insights", "Analysis of class performance and support needs")

        if not self.students:
            tk.Label(self.content, text="No student records available.",
                     bg=self.theme["bg"], fg=self.theme["text_muted"], font=FONT_BODY).pack()
            return

        insights = get_insights(self.students)
        top = insights["top_performer"]
        struggling = insights["struggling_students"]

        # Top Performer Card
        top_card = tk.Frame(self.content, bg=self.theme["card"], padx=24, pady=18,
                            highlightthickness=1, highlightbackground=self.theme["border"])
        top_card.pack(fill="x", pady=(0, 16))

        tk.Label(top_card, text="🏆 TOP PERFORMER", bg=self.theme["card"],
                 fg=self.theme["accent"], font=("Segoe UI", 9, "bold")).pack(anchor="w")

        if top:
            m = float(top["marks"])
            tk.Label(top_card, text=f"{top['name'].title()}  •  {m:.1f} Marks ({calculate_grade(m)})",
                     bg=self.theme["card"], fg=self.theme["text"], font=FONT_H1).pack(anchor="w", pady=(4, 2))
            tk.Label(top_card, text=f"Course: {top['course']}  |  Roll Number: {top['roll_no']}",
                     bg=self.theme["card"], fg=self.theme["text_muted"], font=FONT_SMALL).pack(anchor="w")

        # Class Average Card
        avg_card = tk.Frame(self.content, bg=self.theme["card"], padx=24, pady=16,
                            highlightthickness=1, highlightbackground=self.theme["border"])
        avg_card.pack(fill="x", pady=(0, 16))

        tk.Label(avg_card, text="📊 CLASS AVERAGE", bg=self.theme["card"],
                 fg=self.theme["accent"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(avg_card, text=f"Class Mean: {insights['average']:.2f} Marks",
                 bg=self.theme["card"], fg=self.theme["text"], font=FONT_H1).pack(anchor="w", pady=(4, 2))

        # Academic Support Needed
        sup_card = tk.Frame(self.content, bg=self.theme["card"], padx=24, pady=18,
                            highlightthickness=1, highlightbackground=self.theme["border"])
        sup_card.pack(fill="x")

        tk.Label(sup_card, text="⚠️ STUDENTS NEEDING SUPPORT (< 40 marks)", bg=self.theme["card"],
                 fg=self.theme["accent"], font=("Segoe UI", 9, "bold")).pack(anchor="w")

        if not struggling:
            tk.Label(sup_card, text="✓ Great job! All students are meeting the passing standard (≥ 40 marks).",
                     bg=self.theme["card"], fg=self.theme["text"], font=FONT_BODY).pack(anchor="w", pady=(8, 0))
        else:
            for s in struggling:
                row = tk.Frame(sup_card, bg=self.theme["card"])
                row.pack(anchor="w", pady=4)
                tk.Label(row, text="•", bg=self.theme["card"], fg=self.theme["accent"], font=FONT_BOLD).pack(side="left", padx=(0, 6))
                tk.Label(row, text=f"{s['name'].title()} (Roll {s['roll_no']}) — {s['marks']} Marks ({s['course']})",
                         bg=self.theme["card"], fg=self.theme["text"], font=FONT_BODY).pack(side="left")


# =====================================================================
# START APPLICATION
# =====================================================================
if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()

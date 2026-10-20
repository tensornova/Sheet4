# Sheet 4 - Problem 2(a)
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

f  = lambda x: x ** 3 + 4 * x ** 2 - 10
df = lambda x: 3 * x ** 2 + 8 * x
g  = lambda x: (10 - x ** 3) ** 0.5 / 2  # |g'(x)| < 1 on [1, 2]

def update_btn_colors(*args):
    for rb in radio_btns:
        is_sel = (rb['value'] == var_method.get())
        rb.config(fg="#11111b" if is_sel else FG_TXT)

def evaluate():
    tree.delete(*tree.get_children())
    method = var_method.get()
    rows = []

    if method == "Bisection":
        cols = (("n", "n", 45), ("a", "a", 85), ("b", "b", 85), ("c", "c", 90), ("s", "Sign of f(c)", 110))
        a, b = 1.0, 2.0
        for n in range(1, 14):
            c = (a + b) / 2
            rows.append((n, f"{a:g}", f"{b:g}", f"{c:.4f}", "-ve" if f(c) < 0 else "+ve"))
            a, b = (c, b) if f(a) * f(c) > 0 else (a, c)
        root_val, formula_txt = c, "Interval [1, 2]   |   c = (a + b) / 2"
    else:
        cols = (("n", "n", 90), ("x_next", "xₙ₊₁", 190))
        xn = 1.5
        for n in range(15):
            x_next = g(xn) if method == "Fixed-Point" else xn - f(xn) / df(xn)
            rows.append((n, f"{x_next:.4f}"))
            if round(x_next, 4) == round(xn, 4) and n > 0: break
            xn = x_next
        root_val = x_next
        formula_txt = "xₙ₊₁ = 0.5 √(10 - xₙ³)  ,   x₀ = 1.5" if method == "Fixed-Point" else "xₙ₊₁ = xₙ - f(xₙ) / f'(xₙ)  ,   x₀ = 1.5"

    # Setup Table Columns & Rows
    tree.config(columns=[c[0] for c in cols], height=min(len(rows), 6))
    for cid, title, w in cols:
        tree.heading(cid, text=title)
        tree.column(cid, width=w, anchor="center")

    for i, r in enumerate(rows):
        tree.insert("", "end", values=r, tags=('even' if i % 2 == 0 else 'odd',))

    lbl_formula.config(text=formula_txt)
    lbl_result.config(text=f"Approximate Root ≈ {root_val:.4f}")

    # Reveal Table & Plot Container on First Click
    if not table_frame.winfo_ismapped():
        table_frame.pack(pady=8, padx=25, fill="x", before=lbl_formula)
        plot_container.pack(fill="both", expand=True, padx=25, pady=(5, 20))
        root.geometry("560x770")

    # Plot Graph
    plt.close('all')
    fig, ax = plt.subplots(figsize=(5, 2.7), dpi=100)
    fig.patch.set_facecolor('#1e1e2e')
    ax.set_facecolor('#313244')
    ax.tick_params(colors='#cdd6f4', labelsize=9)

    x_line = np.linspace(1.0, 2.0, 100)
    ax.plot(x_line, f(x_line), color='#89b4fa', linewidth=2, label='f(x) = x³ + 4x² - 10')
    ax.axhline(0, color='#f38ba8', linestyle='--', linewidth=1, alpha=0.7)
    ax.scatter([root_val], [f(root_val)], color='#a6e3a1', s=65, zorder=5, label=f'Root ({root_val:.4f})')

    ax.set_title(f"{method} Method Convergence", color='#cdd6f4', fontsize=11, fontweight='bold', pad=10)
    ax.legend(facecolor='#1e1e2e', edgecolor='#45475a', labelcolor='#cdd6f4', fontsize=9)
    ax.grid(color='#45475a', linestyle='--', linewidth=0.5, alpha=0.7)
    fig.tight_layout()

    for w in plot_container.winfo_children(): w.destroy()
    canvas = FigureCanvasTkAgg(fig, master=plot_container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# GUI Setup 
root = tk.Tk()
root.title("Numerical Methods - Sheet 4")
root.geometry("560x280")
root.configure(bg="#1e1e2e")

FNT, BG_CARD, FG_TXT = "Segoe UI", "#313244", "#cdd6f4"

# Headers
tk.Label(root, text="Root Finding Calculator", font=(FNT, 17, "bold"), bg="#1e1e2e", fg=FG_TXT).pack(pady=(15, 2))
tk.Label(root, text="Sheet 4 - Problem 2(a): f(x) = x³ + 4x² - 10", font=(FNT, 11, "bold"), bg="#1e1e2e", fg="#89b4fa").pack(pady=(0, 12))

# Modern Segmented Method Selector
card = tk.Frame(root, bg=BG_CARD, padx=12, pady=10)
card.pack(padx=25, fill="x")
tk.Label(card, text="Method:", font=(FNT, 10, "bold"), bg=BG_CARD, fg=FG_TXT).pack(side="left", padx=(5, 12))

var_method = tk.StringVar(value="Newton")
radio_btns = []
for m in ["Bisection", "Fixed-Point", "Newton"]:
    rb = tk.Radiobutton(card, text=m, variable=var_method, value=m, indicatoron=0,
                        font=(FNT, 10, "bold"), width=12, pady=4, relief="flat", bd=0,
                        highlightthickness=0, cursor="hand2",
                        bg="#262637", fg=FG_TXT, selectcolor="#89b4fa",
                        activebackground="#45475a", activeforeground=FG_TXT, command=update_btn_colors)
    rb.pack(side="left", expand=True, fill="x", padx=4)
    radio_btns.append(rb)
update_btn_colors()

# Evaluate Button
tk.Button(root, text="Generate Table & Plot", font=(FNT, 11, "bold"),
          bg="#89b4fa", fg="#11111b", activebackground="#b4befe",
          relief="flat", cursor="hand2", width=24, pady=6, command=evaluate).pack(pady=14)

# Treeview Style & Hidden Container
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background=BG_CARD, foreground=FG_TXT, fieldbackground=BG_CARD, borderwidth=0, font=(FNT, 10), rowheight=26)
style.configure("Treeview.Heading", background="#181825", foreground=FG_TXT, font=(FNT, 10, "bold"), padding=4)
style.map("Treeview", background=[("selected", "#45475a")])

table_frame = tk.Frame(root, bg="#1e1e2e")
tree = ttk.Treeview(table_frame, show="headings")
tree.tag_configure('even', background="#313244")
tree.tag_configure('odd', background="#292a3a")
tree.pack(fill="x", expand=True)

# Output Labels (Formula Font Size Increased to 13)
lbl_formula = tk.Label(root, text="", font=(FNT, 13, "bold"), bg="#1e1e2e", fg="#f38ba8")
lbl_formula.pack(pady=(4, 0))
lbl_result = tk.Label(root, text="Root = ---", font=(FNT, 14, "bold"), bg="#1e1e2e", fg="#a6e3a1")
lbl_result.pack(pady=(2, 8))

plot_container = tk.Frame(root, bg="#1e1e2e")

root.mainloop()
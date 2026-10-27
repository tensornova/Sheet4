import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to update radio button colors based on selection
def update_btn_colors(*args):
    for rb in radio_btns:
        is_sel = (rb['value'] == var_method.get())
        rb.config(fg="#11111b" if is_sel else FG_TXT)

# Main function to calculate iterations, update table, and plot
def evaluate():
    tree.delete(*tree.get_children())
    method = var_method.get()
    omega = 0.9595  # Relaxation factor for SOR method
    
    # Initialize variables for x, y, z and lists for plotting
    x, y, z = 0.0, 0.0, 0.0
    rows = [(0, f"{x:.4f}", f"{y:.4f}", f"{z:.4f}")]
    x_v, y_v, z_v, n_v = [0], [0], [0], [0]
    
    # Perform iterations based on the selected numerical method
    max_iter = 6
    for n in range(1, max_iter + 1):
        if method == "Jacobi":
            xn = 0.25 * (4 + y - z)
            yn = 0.50 * (4 - x - z)
            zn = 0.50 * (1 + x)
        elif method == "Gauss-Seidel":
            xn = 0.25 * (4 + y - z)
            yn = 0.50 * (4 - xn - z)
            zn = 0.50 * (1 + xn)
        else: # SOR Method
            x_new = 0.25 * (4 + y - z)
            xn = (1 - omega) * x + omega * x_new
            
            y_new = 0.50 * (4 - xn - z)
            yn = (1 - omega) * y + omega * y_new
            
            z_new = 0.50 * (1 + xn)
            zn = (1 - omega) * z + omega * z_new
            
        x, y, z = xn, yn, zn
        rows.append((n, f"{x:.4f}", f"{y:.4f}", f"{z:.4f}"))
        x_v.append(x)
        y_v.append(y)
        z_v.append(z)
        n_v.append(n)

    # Configure and populate the Treeview table with results
    cols = (("n", "n", 60), ("x", "xₙ", 120), ("y", "yₙ", 120), ("z", "zₙ", 120))
    tree.config(columns=[c[0] for c in cols], height=7)
    for cid, title, w in cols:
        tree.heading(cid, text=title)
        tree.column(cid, width=w, anchor="center")

    for i, r in enumerate(rows):
        tree.insert("", "end", values=r, tags=('even' if i % 2 == 0 else 'odd',))

    # Set multi-line formulas for clarity in the GUI
    if method == "Jacobi":
        formula_txt = "xₙ₊₁ = 0.25 (4 + yₙ - zₙ)\nyₙ₊₁ = 0.50 (4 - xₙ - zₙ)\nzₙ₊₁ = 0.50 (1 + xₙ)"
    elif method == "Gauss-Seidel":
        formula_txt = "xₙ₊₁ = 0.25 (4 + yₙ - zₙ)\nyₙ₊₁ = 0.50 (4 - xₙ₊₁ - zₙ)\nzₙ₊₁ = 0.50 (1 + xₙ₊₁)"
    else:
        formula_txt = f"SOR (ω = {omega})\nxₙ₊₁ = (1-ω)xₙ + ω[0.25(4+yₙ-zₙ)]\nyₙ₊₁ = (1-ω)yₙ + ω[0.5(4-xₙ₊₁-zₙ)]"

    lbl_formula.config(text=formula_txt)
    lbl_result.config(text=f"Approximation: x={x:.4f}, y={y:.4f}, z={z:.4f}")

    # Reveal table and plot on the first evaluation
    if not table_frame.winfo_ismapped():
        table_frame.pack(pady=8, padx=25, fill="x", before=lbl_formula)
        plot_container.pack(fill="both", expand=True, padx=25, pady=(5, 20))
        root.geometry("640x880")

    # Generate and display the convergence plot
    plt.close('all')
    fig, ax = plt.subplots(figsize=(6, 2.5), dpi=100)
    fig.patch.set_facecolor('#1e1e2e')
    ax.set_facecolor('#313244')
    ax.tick_params(colors='#cdd6f4', labelsize=9)

    ax.plot(n_v, x_v, color='#89b4fa', marker='o', markersize=5, linewidth=2, label='x')
    ax.plot(n_v, y_v, color='#a6e3a1', marker='s', markersize=5, linewidth=2, label='y')
    ax.plot(n_v, z_v, color='#f38ba8', marker='^', markersize=5, linewidth=2, label='z')
    ax.axhline(1.0, color='#cdd6f4', linestyle='--', linewidth=1, alpha=0.5, label='Exact Sol (1.0)')

    ax.set_title(f"{method} Convergence", color='#cdd6f4', fontsize=11, fontweight='bold', pad=10)
    ax.set_xlabel("Iteration (n)", color='#cdd6f4', fontsize=9)
    ax.legend(facecolor='#1e1e2e', edgecolor='#45475a', labelcolor='#cdd6f4', fontsize=9, loc='lower right')
    ax.grid(color='#45475a', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.set_xticks(range(7))
    fig.tight_layout()

    # Embed the matplotlib figure into Tkinter
    for w in plot_container.winfo_children(): w.destroy()
    canvas = FigureCanvasTkAgg(fig, master=plot_container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# GUI Setup
root = tk.Tk()
root.title("Iterative Methods - Sheet 5")
root.geometry("640x350")
root.configure(bg="#1e1e2e")

# Define common styles
FNT, BG_CARD, FG_TXT = "Segoe UI", "#313244", "#cdd6f4"

# Main window headers
tk.Label(root, text="Linear Systems Solver", font=(FNT, 17, "bold"), bg="#1e1e2e", fg=FG_TXT).pack(pady=(15, 2))
tk.Label(root, text="Sheet 5 - Problem (b) (Rearranged for Diagonal Dominance)", font=(FNT, 11, "bold"), bg="#1e1e2e", fg="#89b4fa").pack(pady=(0, 2))
tk.Label(root, text="4x - y + z = 4   |   x + 2y + z = 4   |   -x + 2z = 1", font=("Consolas", 10, "bold"), bg="#1e1e2e", fg="#a6e3a1").pack(pady=(0, 12))

# Method selection frame
card = tk.Frame(root, bg=BG_CARD, padx=12, pady=10)
card.pack(padx=25, fill="x")
tk.Label(card, text="Method:", font=(FNT, 10, "bold"), bg=BG_CARD, fg=FG_TXT).pack(side="left", padx=(5, 12))

# Create radio buttons for method selection
var_method = tk.StringVar(value="Jacobi")
radio_btns = []
for m in ["Jacobi", "Gauss-Seidel", "SOR"]:
    rb = tk.Radiobutton(card, text=m, variable=var_method, value=m, indicatoron=0,
                        font=(FNT, 10, "bold"), width=12, pady=4, relief="flat", bd=0,
                        highlightthickness=0, cursor="hand2",
                        bg="#262637", fg=FG_TXT, selectcolor="#89b4fa",
                        activebackground="#45475a", activeforeground=FG_TXT, command=update_btn_colors)
    rb.pack(side="left", expand=True, fill="x", padx=4)
    radio_btns.append(rb)
update_btn_colors()

# Evaluation button
tk.Button(root, text="Generate Table & Plot", font=(FNT, 11, "bold"),
          bg="#89b4fa", fg="#11111b", activebackground="#b4befe",
          relief="flat", cursor="hand2", width=24, pady=6, command=evaluate).pack(pady=14)

# Styling for Treeview (Table)
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background=BG_CARD, foreground=FG_TXT, 
                fieldbackground=BG_CARD, borderwidth=0, font=(FNT, 10), rowheight=26)
style.configure("Treeview.Heading", background="#181825", foreground=FG_TXT, 
                font=(FNT, 10, "bold"), padding=4)
style.map("Treeview", background=[("selected", "#45475a")])

# Treeview container
table_frame = tk.Frame(root, bg="#1e1e2e")
tree = ttk.Treeview(table_frame, show="headings")
tree.tag_configure('even', background="#313244")
tree.tag_configure('odd', background="#292a3a")
tree.pack(fill="x", expand=True)

# Formula and Result labels
lbl_formula = tk.Label(root, text="", font=(FNT, 14, "bold"), bg="#1e1e2e", fg="#f38ba8", justify="center")
lbl_formula.pack(pady=(4, 0))
lbl_result = tk.Label(root, text="", font=(FNT, 15, "bold"), bg="#1e1e2e", fg="#a6e3a1")
lbl_result.pack(pady=(8, 8))

# Plot container
plot_container = tk.Frame(root, bg="#1e1e2e")

# Start application
root.mainloop()
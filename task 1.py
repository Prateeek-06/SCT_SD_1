import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Color Palette ----------
BG = "#0b0d13"
CARD = "#161925"
FIELD = "#1f2333"
BORDER = "#2a2f42"
TEXT = "#f5f6fa"
SUBTEXT = "#8b91a7"

ACCENT1 = "#7f5af0"        # violet
ACCENT2 = "#ff6ec7"        # pink
ACCENT_HOVER1 = "#9b7cf5"
ACCENT_HOVER2 = "#ff8ed4"
HIGHLIGHT = "#2cf9c6"       # mint (result / swap accent)

# ---------- Gradient helpers ----------
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

def interpolate(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((int(r1 + (r2 - r1) * t),
                        int(g1 + (g2 - g1) * t),
                        int(b1 + (b2 - b1) * t)))

def draw_gradient(canvas, width, height, color1, color2):
    canvas.delete("gradient")
    for i in range(width):
        t = i / width
        canvas.create_line(i, 0, i, height, fill=interpolate(color1, color2, t), tags=("gradient",))
    canvas.tag_lower("gradient")

# ---------- Conversion logic ----------
def to_celsius(value, unit):
    if unit == "Celsius": return value
    elif unit == "Fahrenheit": return (value - 32) * 5/9
    elif unit == "Kelvin": return value - 273.15

def from_celsius(value, unit):
    if unit == "Celsius": return value
    elif unit == "Fahrenheit": return (value * 9/5) + 32
    elif unit == "Kelvin": return value + 273.15

def convert(event=None):
    try:
        value = float(entry_value.get())
        celsius = to_celsius(value, from_combo.get())
        result = from_celsius(celsius, to_combo.get())
        result_label.config(text=f"{result:.2f} {to_combo.get()}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

def swap_units():
    f, t = from_combo.get(), to_combo.get()
    from_combo.set(t)
    to_combo.set(f)
    convert()

def on_btn_enter(e):
    draw_gradient(convert_canvas, 310, 52, ACCENT_HOVER1, ACCENT_HOVER2)
    convert_canvas.tag_raise(btn_text_id)

def on_btn_leave(e):
    draw_gradient(convert_canvas, 310, 52, ACCENT1, ACCENT2)
    convert_canvas.tag_raise(btn_text_id)

# ---------- Window ----------
root = tk.Tk()
root.title("Temperature Converter")
root.geometry("420x580")
root.configure(bg=BG)
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground=FIELD, background=FIELD, foreground=TEXT,
                arrowcolor=ACCENT1, bordercolor=BORDER, lightcolor=FIELD, darkcolor=FIELD)
style.map("TCombobox", fieldbackground=[("readonly", FIELD)])

# ---------- Gradient header banner ----------
header_canvas = tk.Canvas(root, width=420, height=110, highlightthickness=0, bg=BG)
draw_gradient(header_canvas, 420, 110, ACCENT1, ACCENT2)
header_canvas.create_text(210, 45, text="Temperature Converter",
                           font=("Segoe UI", 19, "bold"), fill="white")
header_canvas.create_text(210, 75, text="Celsius · Fahrenheit · Kelvin",
                           font=("Segoe UI", 10), fill="#f3e8ff")
header_canvas.pack()

# ---------- Card ----------
card = tk.Frame(root, bg=CARD, padx=25, pady=22,
                 highlightbackground=BORDER, highlightthickness=1)
card.pack(pady=(20, 15), padx=30, fill="both")

tk.Label(card, text="ENTER VALUE", font=("Segoe UI", 9, "bold"), bg=CARD, fg=SUBTEXT).pack(anchor="w")
entry_value = tk.Entry(card, font=("Segoe UI", 15), bg=FIELD, fg=TEXT,
                        insertbackground=HIGHLIGHT, relief="flat", justify="center",
                        highlightthickness=2, highlightbackground=BORDER, highlightcolor=ACCENT1)
entry_value.pack(fill="x", ipady=9, pady=(6, 18))

row = tk.Frame(card, bg=CARD)
row.pack(fill="x")

units = ["Celsius", "Fahrenheit", "Kelvin"]

col1 = tk.Frame(row, bg=CARD)
col1.pack(side="left", expand=True, fill="x")
tk.Label(col1, text="FROM", font=("Segoe UI", 9, "bold"), bg=CARD, fg=SUBTEXT).pack(anchor="w")
from_combo = ttk.Combobox(col1, values=units, state="readonly", font=("Segoe UI", 11), width=12)
from_combo.pack(fill="x", pady=5, ipady=3)
from_combo.current(0)

swap_btn = tk.Button(row, text="⇄", command=swap_units, bg=CARD, fg=HIGHLIGHT,
                      font=("Segoe UI", 16, "bold"), relief="flat", cursor="hand2",
                      activebackground=CARD, activeforeground=ACCENT_HOVER1, bd=0)
swap_btn.pack(side="left", padx=10, pady=(18, 0))

col2 = tk.Frame(row, bg=CARD)
col2.pack(side="left", expand=True, fill="x")
tk.Label(col2, text="TO", font=("Segoe UI", 9, "bold"), bg=CARD, fg=SUBTEXT).pack(anchor="w")
to_combo = ttk.Combobox(col2, values=units, state="readonly", font=("Segoe UI", 11), width=12)
to_combo.pack(fill="x", pady=5, ipady=3)
to_combo.current(1)

# ---------- Gradient convert button ----------
convert_canvas = tk.Canvas(card, width=310, height=52, highlightthickness=0, bg=CARD, cursor="hand2")
draw_gradient(convert_canvas, 310, 52, ACCENT1, ACCENT2)
btn_text_id = convert_canvas.create_text(155, 26, text="Convert",
                                          font=("Segoe UI", 12, "bold"), fill="white")
convert_canvas.pack(pady=(18, 5))
convert_canvas.bind("<Enter>", on_btn_enter)
convert_canvas.bind("<Leave>", on_btn_leave)
convert_canvas.bind("<Button-1>", convert)

# ---------- Result chip ----------
result_frame = tk.Frame(root, bg=BG)
result_frame.pack(pady=(5, 25))
tk.Label(result_frame, text="RESULT", font=("Segoe UI", 9, "bold"), bg=BG, fg=SUBTEXT).pack()
result_chip = tk.Frame(result_frame, bg=FIELD, highlightbackground=ACCENT1,
                        highlightthickness=1, padx=25, pady=10)
result_chip.pack(pady=(6, 0))
result_label = tk.Label(result_chip, text="—", font=("Segoe UI", 24, "bold"), bg=FIELD, fg=HIGHLIGHT)
result_label.pack()

# Enter key submits from anywhere in the window
root.bind("<Return>", convert)
entry_value.focus_set()

root.mainloop()
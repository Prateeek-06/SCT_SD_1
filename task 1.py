import tkinter as tk
from tkinter import ttk, messagebox

# ---------- "Nude" Palette ----------
DARKEST   = "#3A2D25"
MAUVE     = "#A58377"
TAN       = "#CBAC8F"
BEIGE     = "#D0C8BD"
LIGHT     = "#ECE3DC"
CREAM     = "#F1ECE6"


# ---------- Helper: draw a rounded rectangle on a canvas ----------
def round_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
        x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
        x1, y2, x1, y2-radius, x1, y1+radius, x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# ---------- Rounded Entry (oval-ish input box) ----------
class RoundedEntry(tk.Canvas):
    def __init__(self, parent, width=280, height=46, radius=23, **kwargs):
        super().__init__(parent, width=width, height=height, bg=LIGHT, highlightthickness=0)
        round_rect(self, 2, 2, width-2, height-2, radius, fill=CREAM, outline=BEIGE, width=1)
        self.entry = tk.Entry(self, font=("Georgia", 14), bg=CREAM, fg=DARKEST,
                               insertbackground=DARKEST, relief="flat", justify="center",
                               highlightthickness=0, bd=0, **kwargs)
        self.create_window(width/2, height/2, window=self.entry, width=width-30, height=height-14)

    def get(self):
        return self.entry.get()

    def bind_key(self, seq, func):
        self.entry.bind(seq, func)

    def focus(self):
        self.entry.focus_set()


# ---------- Rounded (pill-shaped) Button ----------
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, width=280, height=48,
                 bg=DARKEST, hover=MAUVE, fg=CREAM, **kwargs):
        super().__init__(parent, width=width, height=height, bg=LIGHT, highlightthickness=0)
        self.command = command
        self.bg_color = bg
        self.hover_color = hover
        radius = height / 2   # full pill shape
        self.shape = round_rect(self, 1, 1, width-1, height-1, radius, fill=bg, outline="")
        self.text_id = self.create_text(width/2, height/2, text=text, fill=fg,
                                         font=("Segoe UI", 11, "bold"))
        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", lambda e: self.itemconfig(self.shape, fill=self.hover_color))
        self.bind("<Leave>", lambda e: self.itemconfig(self.shape, fill=self.bg_color))
        self.configure(cursor="hand2")


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
        result_label.config(text=f"{result:.2f}°")
        result_unit_label.config(text=to_combo.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")


root = tk.Tk()
root.title("Temperature Converter")
root.geometry("440x700")
root.configure(bg=CREAM)
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground=LIGHT, background=LIGHT, foreground=DARKEST,
                arrowcolor=DARKEST, bordercolor=BEIGE, lightcolor=LIGHT, darkcolor=LIGHT,
                relief="flat")
style.map("TCombobox", fieldbackground=[("readonly", LIGHT)])

outer = tk.Frame(root, bg=CREAM, highlightbackground=BEIGE, highlightthickness=1)
outer.pack(fill="both", expand=True, padx=15, pady=15)

# Header
tk.Label(outer, text="Temperature", font=("Georgia", 26), bg=CREAM, fg=DARKEST).pack(pady=(30, 4))
tk.Label(outer, text="Celsius  ·  Fahrenheit  ·  Kelvin", font=("Segoe UI", 9),
         bg=CREAM, fg=MAUVE).pack(pady=(0, 18))

# ---------- Oval-ish card (rounded rectangle drawn on canvas) ----------
card_canvas = tk.Canvas(outer, width=370, height=280, bg=CREAM, highlightthickness=0)
card_canvas.pack(pady=(0, 10))
round_rect(card_canvas, 2, 2, 368, 278, 40, fill=LIGHT, outline=BEIGE, width=1)

card = tk.Frame(card_canvas, bg=LIGHT)
card_canvas.create_window(185, 140, window=card, width=310, height=250)

tk.Label(card, text="ENTER VALUE", font=("Segoe UI", 8, "bold"),
         bg=LIGHT, fg=MAUVE).pack(anchor="w", pady=(4, 4))

entry_value = RoundedEntry(card, width=310, height=46)
entry_value.pack(pady=(0, 14))
entry_value.bind_key("<Return>", convert)
entry_value.focus()

row = tk.Frame(card, bg=LIGHT)
row.pack(fill="x")

units = ["Celsius", "Fahrenheit", "Kelvin"]

col1 = tk.Frame(row, bg=LIGHT)
col1.pack(side="left", expand=True, fill="x", padx=(0, 6))
tk.Label(col1, text="FROM", font=("Segoe UI", 8, "bold"), bg=LIGHT, fg=MAUVE).pack(anchor="w")
from_combo = ttk.Combobox(col1, values=units, state="readonly", font=("Segoe UI", 10))
from_combo.pack(fill="x", pady=5, ipady=3)
from_combo.current(0)
from_combo.bind("<Return>", convert)

col2 = tk.Frame(row, bg=LIGHT)
col2.pack(side="left", expand=True, fill="x", padx=(6, 0))
tk.Label(col2, text="TO", font=("Segoe UI", 8, "bold"), bg=LIGHT, fg=MAUVE).pack(anchor="w")
to_combo = ttk.Combobox(col2, values=units, state="readonly", font=("Segoe UI", 10))
to_combo.pack(fill="x", pady=5, ipady=3)
to_combo.current(1)
to_combo.bind("<Return>", convert)

# ---------- Oval Convert Button ----------
convert_btn = RoundedButton(outer, "CONVERT", convert, width=310, height=50)
convert_btn.pack(pady=(18, 0))

# Result section
result_frame = tk.Frame(outer, bg=CREAM)
result_frame.pack(pady=30)

tk.Label(result_frame, text="RESULT", font=("Segoe UI", 8, "bold"),
         bg=CREAM, fg=MAUVE).pack()
result_label = tk.Label(result_frame, text="—", font=("Georgia", 34, "bold"),
                         bg=CREAM, fg=DARKEST)
result_label.pack()
result_unit_label = tk.Label(result_frame, text="", font=("Segoe UI", 10),
                              bg=CREAM, fg=TAN)
result_unit_label.pack()

root.bind("<Return>", convert)

root.mainloop()
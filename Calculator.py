import tkinter as tk
from tkinter import messagebox
import math

class SmartCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Jagsir's Smart Calculator")
        self.root.geometry("400x600")
        self.root.resizable(0, 0)

        self.is_dark = False
        self.history = []
        self.screen = tk.StringVar()

        self.create_widgets()
        self.bind_keys()
        self.apply_theme()

    def create_widgets(self):
        # Display Entry
        self.entry = tk.Entry(self.root, textvar=self.screen, font="Arial 22", bd=10, relief=tk.GROOVE, justify="right")
        self.entry.pack(fill="both", ipadx=8, ipady=15, padx=10, pady=10)

        # Frames
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.scientific_frame = tk.Frame(self.root)
        self.scientific_frame.pack()

        # Buttons Layout
        self.buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", "=", "+"]
        ]

        for row in self.buttons:
            row_frame = tk.Frame(self.button_frame)
            row_frame.pack()
            for btn_text in row:
                btn = tk.Button(row_frame, text=btn_text, font="Arial 18", width=6, height=2,
                                relief=tk.RIDGE, borderwidth=2,
                                bg="lightblue" if btn_text not in ("=", "C") else "orange")
                btn.pack(side="left", padx=5, pady=5)
                btn.bind("<Button-1>", self.click)

        # Scientific Buttons
        sci_buttons = ["sin", "cos", "tan", "sqrt"]
        for i, text in enumerate(sci_buttons):
            btn = tk.Button(self.scientific_frame, text=text, font="Arial 16", width=8, height=1, bg="lightblue")
            btn.grid(row=0, column=i, padx=5, pady=5)
            btn.bind("<Button-1>", self.click)

        # History Box
        self.history_box = tk.Text(self.root, height=5, font="Arial 10", state="disabled", bg="#f0f0f0")
        self.history_box.pack(fill="both", padx=10, pady=(5, 10))

        # 🌗 Theme Toggle Button
        self.theme_btn = tk.Button(self.root, text="🌗 Toggle Theme", font="Arial 12", command=self.toggle_theme)
        self.theme_btn.pack(pady=5)

    def bind_keys(self):
        self.root.bind("<Key>", self.key_press)

    def key_press(self, event):
        key = event.keysym
        if key == "Return":
            self.evaluate()
        elif key == "BackSpace":
            current = self.screen.get()
            self.screen.set(current[:-1])
        elif key.lower() == "c":
            self.screen.set("")
        elif key in ("plus", "minus", "slash", "asterisk", "period") or key.isdigit():
            key_map = {
                "plus": "+",
                "minus": "-",
                "slash": "/",
                "asterisk": "*",
                "period": "."
            }
            char = key_map.get(key, key)
            self.screen.set(self.screen.get() + char)

    def click(self, event):
        text = event.widget.cget("text")
        if text == "=":
            self.evaluate()
        elif text == "C":
            self.screen.set("")
        elif text == "sqrt":
            try:
                result = math.sqrt(float(self.screen.get()))
                self.add_to_history(f"√{self.screen.get()} = {result}")
                self.screen.set(str(result))
            except:
                self.screen.set("Error")
        elif text in ("sin", "cos", "tan"):
            try:
                value = float(self.screen.get())
                func = getattr(math, text)
                result = func(math.radians(value))
                self.add_to_history(f"{text}({value}) = {result}")
                self.screen.set(str(result))
            except:
                self.screen.set("Error")
        else:
            self.screen.set(self.screen.get() + text)

    def evaluate(self):
        try:
            result = str(eval(self.screen.get()))
            self.add_to_history(f"{self.screen.get()} = {result}")
            self.screen.set(result)
        except Exception:
            self.screen.set("Error")

    def add_to_history(self, entry):
        self.history.append(entry)
        self.history_box.configure(state="normal")
        self.history_box.insert("end", entry + "\n")
        self.history_box.configure(state="disabled")
        self.history_box.see("end")

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()

    def apply_theme(self):
        bg_color = "#222222" if self.is_dark else "#ffffff"
        fg_color = "#ffffff" if self.is_dark else "#000000"
        entry_bg = "#444444" if self.is_dark else "#ffffff"

        self.root.configure(bg=bg_color)
        self.entry.configure(bg=entry_bg, fg=fg_color, insertbackground=fg_color)

        for frame in (self.button_frame, self.scientific_frame):
            frame.configure(bg=bg_color)
            for child in frame.winfo_children():
                try:
                    child.configure(bg="gray" if self.is_dark else "lightblue", fg=fg_color)
                except tk.TclError:
                    pass

        self.history_box.configure(bg="#333333" if self.is_dark else "#f0f0f0", fg=fg_color)
        self.theme_btn.configure(bg="#555555" if self.is_dark else "#e0e0e0", fg=fg_color)

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCalculator(root)
    root.mainloop()

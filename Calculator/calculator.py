"""A small, polished desktop calculator built with Tkinter."""

import tkinter as tk
from tkinter import ttk


class CalculatorApp(tk.Tk):
    """Calculator window for two numbers and one basic arithmetic operation."""

    OPERATIONS = {
        "Add (+)": ("+", lambda first, second: first + second),
        "Subtract (−)": ("−", lambda first, second: first - second),
        "Multiply (×)": ("×", lambda first, second: first * second),
        "Divide (÷)": ("÷", lambda first, second: first / second),
    }

    def __init__(self):
        super().__init__()
        self.title("Simple Calculator")
        self.geometry("490x500")
        self.minsize(420, 460)
        self.configure(bg="#111827")

        self.first_number = tk.StringVar()
        self.second_number = tk.StringVar()
        self.operation = tk.StringVar(value="Add (+)")
        self.result = tk.StringVar(value="Ready when you are")
        self.expression = tk.StringVar(value="Enter two numbers to begin")

        self._set_style()
        self._build_interface()
        self.bind("<Return>", lambda _event: self.calculate())
        self.bind("<Escape>", lambda _event: self.clear())
        self.first_entry.focus_set()

    def _set_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Card.TFrame", background="#1f2937")
        style.configure("Title.TLabel", background="#1f2937", foreground="#f9fafb", font=("Segoe UI", 22, "bold"))
        style.configure("Hint.TLabel", background="#1f2937", foreground="#9ca3af", font=("Segoe UI", 10))
        style.configure("Field.TLabel", background="#1f2937", foreground="#d1d5db", font=("Segoe UI", 10, "bold"))
        style.configure("Result.TLabel", background="#0f172a", foreground="#f9fafb", font=("Segoe UI", 23, "bold"))
        style.configure("Expression.TLabel", background="#0f172a", foreground="#94a3b8", font=("Segoe UI", 10))
        style.configure("TEntry", fieldbackground="#111827", foreground="#f9fafb", insertcolor="#f9fafb", bordercolor="#374151", lightcolor="#374151", darkcolor="#374151", padding=10, font=("Segoe UI", 12))
        style.configure("TCombobox", fieldbackground="#111827", background="#111827", foreground="#f9fafb", arrowcolor="#a78bfa", padding=8, font=("Segoe UI", 11))
        style.map("TCombobox", fieldbackground=[("readonly", "#111827")], foreground=[("readonly", "#f9fafb")])
        style.configure("Calculate.TButton", background="#7c3aed", foreground="#ffffff", borderwidth=0, padding=11, font=("Segoe UI", 11, "bold"))
        style.map("Calculate.TButton", background=[("active", "#8b5cf6")])
        style.configure("Clear.TButton", background="#374151", foreground="#e5e7eb", borderwidth=0, padding=11, font=("Segoe UI", 11, "bold"))
        style.map("Clear.TButton", background=[("active", "#4b5563")])

    def _build_interface(self):
        container = ttk.Frame(self, style="Card.TFrame", padding=28)
        container.pack(expand=True, fill="both", padx=22, pady=22)
        container.columnconfigure(0, weight=1)

        ttk.Label(container, text="Simple Calculator", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(container, text="Two numbers. One clear answer.", style="Hint.TLabel").grid(row=1, column=0, sticky="w", pady=(3, 24))

        self._field(container, "FIRST NUMBER", self.first_number, 2)
        self._field(container, "SECOND NUMBER", self.second_number, 4)

        ttk.Label(container, text="OPERATION", style="Field.TLabel").grid(row=6, column=0, sticky="w", pady=(16, 6))
        operation_box = ttk.Combobox(container, textvariable=self.operation, values=list(self.OPERATIONS), state="readonly")
        operation_box.grid(row=7, column=0, sticky="ew")

        actions = ttk.Frame(container, style="Card.TFrame")
        actions.grid(row=8, column=0, sticky="ew", pady=(22, 20))
        actions.columnconfigure(0, weight=3)
        actions.columnconfigure(1, weight=1)
        ttk.Button(actions, text="Calculate", style="Calculate.TButton", command=self.calculate).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(actions, text="Clear", style="Clear.TButton", command=self.clear).grid(row=0, column=1, sticky="ew")

        result_frame = tk.Frame(container, bg="#0f172a", highlightbackground="#334155", highlightthickness=1, padx=18, pady=15)
        result_frame.grid(row=9, column=0, sticky="ew")
        ttk.Label(result_frame, textvariable=self.expression, style="Expression.TLabel").pack(anchor="w")
        ttk.Label(result_frame, textvariable=self.result, style="Result.TLabel").pack(anchor="w", pady=(5, 0))

        ttk.Label(container, text="Tip: Press Enter to calculate • Esc to clear", style="Hint.TLabel").grid(row=10, column=0, pady=(16, 0))

    def _field(self, parent, label, variable, row):
        ttk.Label(parent, text=label, style="Field.TLabel").grid(row=row, column=0, sticky="w", pady=(0 if row == 2 else 16, 6))
        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row + 1, column=0, sticky="ew")
        if row == 2:
            self.first_entry = entry

    @staticmethod
    def _format_number(value):
        return f"{value:g}"

    def calculate(self):
        try:
            first = float(self.first_number.get().strip())
            second = float(self.second_number.get().strip())
            symbol, operation = self.OPERATIONS[self.operation.get()]
            if symbol == "÷" and second == 0:
                raise ZeroDivisionError
            answer = operation(first, second)
        except ValueError:
            self.expression.set("Please check your inputs")
            self.result.set("Enter valid numbers")
        except ZeroDivisionError:
            self.expression.set("Division needs a non-zero divisor")
            self.result.set("Cannot divide by zero")
        else:
            self.expression.set(f"{self._format_number(first)} {symbol} {self._format_number(second)} =")
            self.result.set(self._format_number(answer))

    def clear(self):
        self.first_number.set("")
        self.second_number.set("")
        self.operation.set("Add (+)")
        self.expression.set("Enter two numbers to begin")
        self.result.set("Ready when you are")
        self.first_entry.focus_set()


if __name__ == "__main__":
    CalculatorApp().mainloop()

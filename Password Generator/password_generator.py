"""Secure, attractive desktop password generator built with Tkinter."""

import secrets
import string
import tkinter as tk


CHARACTER_SETS = {
    "Uppercase letters": string.ascii_uppercase,
    "Lowercase letters": string.ascii_lowercase,
    "Numbers": string.digits,
    "Symbols": "!@#$%^&*()-_=+[]{};:,.?/",
}


def generate_password(length: int, character_sets: list[str]) -> str:
    """Return a secure password containing at least one character from each set."""
    if not character_sets:
        raise ValueError("Select at least one character type.")
    if length < len(character_sets):
        raise ValueError("Increase the length or select fewer character types.")

    alphabet = "".join(CHARACTER_SETS[name] for name in character_sets)
    password = [secrets.choice(CHARACTER_SETS[name]) for name in character_sets]
    password.extend(secrets.choice(alphabet) for _ in range(length - len(password)))
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


class PasswordGeneratorApp(tk.Tk):
    """Graphical password generator application."""

    BACKGROUND = "#101827"
    PANEL = "#1d293d"
    ENTRY = "#0b1220"
    TEXT = "#f8fafc"
    MUTED = "#a8b5ca"
    ACCENT = "#55d6be"
    ACCENT_DARK = "#2bb89d"
    WARNING = "#f9c74f"

    def __init__(self) -> None:
        super().__init__()
        self.title("VaultKey — Password Generator")
        self.geometry("650x610")
        self.minsize(590, 570)
        self.configure(bg=self.BACKGROUND)

        self.length = tk.IntVar(value=16)
        self.password = tk.StringVar()
        self.status = tk.StringVar(value="Ready to create a strong password.")
        self.options = {name: tk.BooleanVar(value=True) for name in CHARACTER_SETS}
        self._build_ui()
        self.generate()

    def _build_ui(self) -> None:
        outer = tk.Frame(self, bg=self.BACKGROUND, padx=38, pady=32)
        outer.pack(fill="both", expand=True)

        tk.Label(outer, text="VaultKey", font=("Segoe UI", 28, "bold"),
                 bg=self.BACKGROUND, fg=self.ACCENT).pack(anchor="w")
        tk.Label(outer, text="Generate a password that is hard to guess.",
                 font=("Segoe UI", 11), bg=self.BACKGROUND, fg=self.MUTED).pack(anchor="w", pady=(2, 24))

        output = tk.Frame(outer, bg=self.PANEL, padx=20, pady=18)
        output.pack(fill="x")
        tk.Label(output, text="YOUR NEW PASSWORD", font=("Segoe UI", 9, "bold"),
                 bg=self.PANEL, fg=self.MUTED).pack(anchor="w")
        tk.Entry(output, textvariable=self.password, state="readonly", readonlybackground=self.ENTRY,
                 relief="flat", font=("Consolas", 16, "bold"), fg=self.TEXT).pack(fill="x", pady=(9, 13), ipady=12)

        actions = tk.Frame(output, bg=self.PANEL)
        actions.pack(fill="x")
        self._button(actions, "↻  Generate", self.generate, self.ACCENT, self.ENTRY).pack(side="left")
        self._button(actions, "Copy password", self.copy_password, self.PANEL, self.TEXT, "#526078").pack(side="right")

        controls = tk.Frame(outer, bg=self.BACKGROUND)
        controls.pack(fill="x", pady=(25, 0))
        header = tk.Frame(controls, bg=self.BACKGROUND)
        header.pack(fill="x")
        tk.Label(header, text="Password length", font=("Segoe UI", 11, "bold"), bg=self.BACKGROUND, fg=self.TEXT).pack(side="left")
        tk.Label(header, textvariable=self.length, font=("Segoe UI", 11, "bold"), bg=self.BACKGROUND, fg=self.ACCENT).pack(side="right")
        tk.Scale(controls, from_=4, to=64, orient="horizontal", variable=self.length,
                 command=lambda _value: self._update_strength(), showvalue=False, resolution=1,
                 bg=self.BACKGROUND, fg=self.MUTED, troughcolor="#344158", activebackground=self.ACCENT,
                 highlightthickness=0, sliderrelief="flat").pack(fill="x", pady=(7, 18))

        tk.Label(controls, text="Include", font=("Segoe UI", 11, "bold"), bg=self.BACKGROUND, fg=self.TEXT).pack(anchor="w", pady=(0, 7))
        choices = tk.Frame(controls, bg=self.BACKGROUND)
        choices.pack(fill="x")
        for column, (name, variable) in enumerate(self.options.items()):
            tk.Checkbutton(choices, text=name, variable=variable, command=self._update_strength,
                           font=("Segoe UI", 10), bg=self.BACKGROUND, fg=self.TEXT, selectcolor=self.PANEL,
                           activebackground=self.BACKGROUND, activeforeground=self.TEXT,
                           highlightthickness=0).grid(row=column // 2, column=column % 2, sticky="w", padx=(0, 36), pady=4)

        footer = tk.Frame(outer, bg=self.PANEL, padx=15, pady=11)
        footer.pack(fill="x", pady=(23, 0))
        self.status_label = tk.Label(footer, textvariable=self.status, font=("Segoe UI", 10), bg=self.PANEL, fg=self.ACCENT)
        self.status_label.pack(anchor="w")

    def _button(self, parent, text, command, background, foreground, border=None):
        return tk.Button(parent, text=text, command=command, font=("Segoe UI", 10, "bold"), padx=15, pady=8,
                         cursor="hand2", relief="flat", bd=0, bg=background, fg=foreground,
                         activebackground=self.ACCENT_DARK, activeforeground=self.ENTRY,
                         highlightthickness=1, highlightbackground=border or background)

    def _selected_sets(self) -> list[str]:
        return [name for name, variable in self.options.items() if variable.get()]

    def _update_strength(self) -> None:
        selected = self._selected_sets()
        score = self.length.get() + (len(selected) * 5)
        if not selected:
            message, color = "Choose at least one character type.", self.WARNING
        elif score < 18:
            message, color = "Strength: Fair — use a longer password.", self.WARNING
        elif score < 32:
            message, color = "Strength: Good", self.ACCENT
        else:
            message, color = "Strength: Strong", self.ACCENT
        self.status.set(message)
        self.status_label.configure(fg=color)

    def generate(self) -> None:
        try:
            self.password.set(generate_password(self.length.get(), self._selected_sets()))
            self._update_strength()
        except ValueError as error:
            self.status.set(str(error))
            self.status_label.configure(fg=self.WARNING)

    def copy_password(self) -> None:
        if self.password.get():
            self.clipboard_clear()
            self.clipboard_append(self.password.get())
            self.status.set("Password copied to clipboard.")
            self.status_label.configure(fg=self.ACCENT)


if __name__ == "__main__":
    PasswordGeneratorApp().mainloop()

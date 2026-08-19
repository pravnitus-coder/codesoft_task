"""A modern, local contact book desktop application.

Run with: python contact_book.py
"""

from __future__ import annotations

import json
import re
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from uuid import uuid4


APP_BG = "#f5f7fb"
PANEL = "#ffffff"
NAVY = "#14213d"
ACCENT = "#4763e6"
ACCENT_DARK = "#344dcc"
MUTED = "#64748b"
DANGER = "#dc3f5d"
DATA_FILE = Path(__file__).with_name("contacts.json")


class ContactBook(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Contact Book")
        self.geometry("1120x680")
        self.minsize(960, 580)
        self.configure(bg=APP_BG)
        self.contacts = self.load_contacts()
        self.selected_id: str | None = None
        self.search_text = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready")
        self.fields: dict[str, tk.StringVar] = {
            key: tk.StringVar() for key in ("name", "phone", "email", "address")
        }
        self.configure_styles()
        self.build_ui()
        self.refresh_list()

    @staticmethod
    def load_contacts() -> list[dict]:
        if not DATA_FILE.exists():
            return []
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def save_contacts(self) -> None:
        DATA_FILE.write_text(json.dumps(self.contacts, indent=2), encoding="utf-8")

    def configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=42,
                        background=PANEL, fieldbackground=PANEL, foreground=NAVY,
                        borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 10),
                        background="#eef1f8", foreground=MUTED, relief="flat")
        style.map("Treeview", background=[("selected", "#dfe5ff")], foreground=[("selected", NAVY)])
        style.configure("TEntry", padding=9, font=("Segoe UI", 10), fieldbackground="#f8fafc")
        style.configure("Accent.TButton", background=ACCENT, foreground="white",
                        font=("Segoe UI Semibold", 10), padding=(15, 10), borderwidth=0)
        style.map("Accent.TButton", background=[("active", ACCENT_DARK)])
        style.configure("Soft.TButton", background="#e9edff", foreground=ACCENT,
                        font=("Segoe UI Semibold", 10), padding=(14, 9), borderwidth=0)
        style.map("Soft.TButton", background=[("active", "#dce3ff")])
        style.configure("Danger.TButton", background="#fff0f2", foreground=DANGER,
                        font=("Segoe UI Semibold", 10), padding=(14, 9), borderwidth=0)

    def build_ui(self) -> None:
        header = tk.Frame(self, bg=NAVY, height=106)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="CONTACT BOOK", font=("Segoe UI", 11, "bold"), fg="#aebcff", bg=NAVY).place(x=38, y=21)
        tk.Label(header, text="Keep the people who matter close.", font=("Segoe UI", 22, "bold"), fg="white", bg=NAVY).place(x=38, y=47)
        self.count_label = tk.Label(header, font=("Segoe UI", 10), fg="#c9d2ff", bg=NAVY)
        self.count_label.place(relx=.95, y=48, anchor="e")

        content = tk.Frame(self, bg=APP_BG, padx=34, pady=28)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        left = tk.Frame(content, bg=PANEL, padx=22, pady=20, highlightthickness=1, highlightbackground="#e6eaf2")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 22))
        left.rowconfigure(2, weight=1)
        left.columnconfigure(0, weight=1)
        top = tk.Frame(left, bg=PANEL)
        top.grid(row=0, column=0, sticky="ew")
        tk.Label(top, text="Your contacts", font=("Segoe UI", 16, "bold"), fg=NAVY, bg=PANEL).pack(side="left")
        ttk.Button(top, text="+  New contact", style="Accent.TButton", command=self.clear_form).pack(side="right")
        search = ttk.Entry(left, textvariable=self.search_text)
        search.grid(row=1, column=0, sticky="ew", pady=(19, 15))
        search.insert(0, "Search by name or phone number")
        search.bind("<FocusIn>", self.clear_hint)
        search.bind("<KeyRelease>", lambda _event: self.refresh_list())

        tree_box = tk.Frame(left, bg=PANEL)
        tree_box.grid(row=2, column=0, sticky="nsew")
        tree_box.columnconfigure(0, weight=1)
        tree_box.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(tree_box, columns=("name", "phone"), show="headings", selectmode="browse")
        self.tree.heading("name", text="NAME")
        self.tree.heading("phone", text="PHONE NUMBER")
        self.tree.column("name", width=250, anchor="w")
        self.tree.column("phone", width=180, anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew")
        bar = ttk.Scrollbar(tree_box, orient="vertical", command=self.tree.yview)
        bar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=bar.set)
        self.tree.bind("<<TreeviewSelect>>", self.load_selected)

        right = tk.Frame(content, bg=PANEL, padx=27, pady=24, highlightthickness=1, highlightbackground="#e6eaf2")
        right.grid(row=0, column=1, sticky="nsew")
        tk.Label(right, text="Contact details", font=("Segoe UI", 16, "bold"), fg=NAVY, bg=PANEL).pack(anchor="w")
        tk.Label(right, text="Add someone new or edit a selected contact.", font=("Segoe UI", 9), fg=MUTED, bg=PANEL).pack(anchor="w", pady=(4, 21))
        labels = [("name", "Full name *"), ("phone", "Phone number *"), ("email", "Email address"), ("address", "Address")]
        for key, label in labels:
            tk.Label(right, text=label, font=("Segoe UI Semibold", 9), fg=NAVY, bg=PANEL).pack(anchor="w", pady=(0, 6))
            ttk.Entry(right, textvariable=self.fields[key]).pack(fill="x", pady=(0, 15))
        actions = tk.Frame(right, bg=PANEL)
        actions.pack(fill="x", pady=(7, 0))
        ttk.Button(actions, text="Save contact", style="Accent.TButton", command=self.save_contact).pack(side="left")
        ttk.Button(actions, text="Delete", style="Danger.TButton", command=self.delete_contact).pack(side="right")
        ttk.Button(right, text="Clear form", style="Soft.TButton", command=self.clear_form).pack(anchor="w", pady=(13, 0))
        tk.Label(right, textvariable=self.status_text, font=("Segoe UI", 9), fg=MUTED, bg=PANEL, wraplength=310, justify="left").pack(anchor="w", pady=(22, 0))

    def clear_hint(self, _event: tk.Event) -> None:
        if self.search_text.get() == "Search by name or phone number":
            self.search_text.set("")

    def refresh_list(self) -> None:
        query = self.search_text.get().strip().lower()
        if query == "search by name or phone number":
            query = ""
        for row in self.tree.get_children():
            self.tree.delete(row)
        displayed = 0
        for contact in sorted(self.contacts, key=lambda c: c["name"].lower()):
            if query and query not in contact["name"].lower() and query not in contact["phone"].lower():
                continue
            self.tree.insert("", "end", iid=contact["id"], values=(contact["name"], contact["phone"]))
            displayed += 1
        total = len(self.contacts)
        self.count_label.config(text=f"{total} contact{'s' if total != 1 else ''} saved")
        if query:
            self.status_text.set(f"Showing {displayed} matching contact{'s' if displayed != 1 else ''}.")

    def load_selected(self, _event: tk.Event) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        self.selected_id = selection[0]
        contact = next((c for c in self.contacts if c["id"] == self.selected_id), None)
        if contact:
            for key, value in self.fields.items():
                value.set(contact.get(key, ""))
            self.status_text.set(f"Editing {contact['name']}. Save to apply your changes.")

    def clear_form(self) -> None:
        self.selected_id = None
        for value in self.fields.values():
            value.set("")
        self.tree.selection_remove(self.tree.selection())
        self.status_text.set("New contact form ready.")

    def save_contact(self) -> None:
        values = {key: value.get().strip() for key, value in self.fields.items()}
        if not values["name"] or not values["phone"]:
            messagebox.showwarning("Missing information", "Please enter both a name and phone number.")
            return
        if values["email"] and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", values["email"]):
            messagebox.showwarning("Invalid email", "Please enter a valid email address.")
            return
        if self.selected_id:
            contact = next(c for c in self.contacts if c["id"] == self.selected_id)
            contact.update(values)
            message = f"Updated {values['name']}."
        else:
            values["id"] = str(uuid4())
            self.contacts.append(values)
            self.selected_id = values["id"]
            message = f"Added {values['name']}."
        self.save_contacts()
        self.refresh_list()
        self.status_text.set(message)

    def delete_contact(self) -> None:
        if not self.selected_id:
            messagebox.showinfo("Select a contact", "Select a contact from the list before deleting it.")
            return
        contact = next((c for c in self.contacts if c["id"] == self.selected_id), None)
        if not contact or not messagebox.askyesno("Delete contact", f"Delete {contact['name']}? This cannot be undone."):
            return
        self.contacts = [c for c in self.contacts if c["id"] != self.selected_id]
        self.save_contacts()
        self.clear_form()
        self.refresh_list()
        self.status_text.set(f"Deleted {contact['name']}.")


if __name__ == "__main__":
    ContactBook().mainloop()

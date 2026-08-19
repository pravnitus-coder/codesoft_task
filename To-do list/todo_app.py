"""A small, persistent desktop to-do list application built with Tkinter."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


DATA_FILE = Path(__file__).with_name("tasks.json")
PRIORITIES = ("High", "Medium", "Low")


class TodoApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("TaskFlow | Personal Planner")
        self.geometry("980x680")
        self.minsize(820, 580)
        self.configure(bg="#f4f6fb")
        self.tasks = self.load_tasks()
        self.selected_id: int | None = None
        self.filter_value = tk.StringVar(value="All")
        self.search_value = tk.StringVar()
        self.title_value = tk.StringVar()
        self.category_value = tk.StringVar()
        self.due_value = tk.StringVar()
        self.priority_value = tk.StringVar(value="Medium")
        self.build_style()
        self.build_ui()
        self.refresh()

    def build_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=40, font=("Segoe UI", 10), background="white", fieldbackground="white", borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 10), background="#edf0ff", foreground="#313b68", relief="flat")
        style.map("Treeview", background=[("selected", "#e1e7ff")], foreground=[("selected", "#172554")])
        style.configure("Accent.TButton", font=("Segoe UI Semibold", 10), padding=(16, 9), background="#635bdb", foreground="white", borderwidth=0)
        style.map("Accent.TButton", background=[("active", "#5149c5")])
        style.configure("Soft.TButton", font=("Segoe UI Semibold", 10), padding=(13, 8), background="#e9edff", foreground="#4b43b5", borderwidth=0)
        style.map("Soft.TButton", background=[("active", "#dce3ff")])

    def build_ui(self) -> None:
        header = tk.Frame(self, bg="#25206b", padx=34, pady=24)
        header.pack(fill="x")
        tk.Label(header, text="TaskFlow", bg="#25206b", fg="white", font=("Segoe UI", 26, "bold")).pack(anchor="w")
        tk.Label(header, text="Your calm, focused space for getting things done.", bg="#25206b", fg="#d7d5ff", font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 0))

        main = tk.Frame(self, bg="#f4f6fb", padx=30, pady=20)
        main.pack(fill="both", expand=True)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(3, weight=1)

        stats = tk.Frame(main, bg="#f4f6fb")
        stats.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        for column in range(3):
            stats.grid_columnconfigure(column, weight=1)
        self.total_card = self.make_stat_card(stats, 0, "TOTAL TASKS", "0", "Everything on your list", "#6159d9")
        self.active_card = self.make_stat_card(stats, 1, "IN PROGRESS", "0", "Ready for your attention", "#2f83d5")
        self.done_card = self.make_stat_card(stats, 2, "COMPLETED", "0", "Wins to celebrate", "#13a37f")

        form = tk.LabelFrame(main, text="  Add or edit a task  ", bg="white", fg="#24315c", font=("Segoe UI", 10, "bold"), padx=14, pady=12, bd=1, relief="solid")
        form.grid(row=1, column=0, sticky="ew")
        form.grid_columnconfigure(0, weight=3)
        form.grid_columnconfigure(1, weight=1)
        form.grid_columnconfigure(2, weight=1)
        form.grid_columnconfigure(3, weight=1)
        self.make_entry(form, "Task", self.title_value, 0, 0)
        self.make_entry(form, "Category", self.category_value, 0, 1)
        self.make_entry(form, "Due date (YYYY-MM-DD)", self.due_value, 0, 2)
        tk.Label(form, text="Priority", bg="white", fg="#556080", font=("Segoe UI", 9)).grid(row=0, column=3, sticky="w", padx=(10, 0))
        ttk.Combobox(form, textvariable=self.priority_value, values=PRIORITIES, state="readonly", width=12).grid(row=1, column=3, sticky="ew", padx=(10, 0), pady=(3, 0))
        actions = tk.Frame(form, bg="white")
        actions.grid(row=2, column=0, columnspan=4, sticky="e", pady=(12, 0))
        ttk.Button(actions, text="Clear form", style="Soft.TButton", command=self.clear_form).pack(side="right")
        ttk.Button(actions, text="+  Save task", style="Accent.TButton", command=self.save_task).pack(side="right", padx=(0, 8))

        toolbar = tk.Frame(main, bg="#f4f6fb", pady=15)
        toolbar.grid(row=2, column=0, sticky="ew")
        tk.Label(toolbar, text="Your tasks", bg="#f4f6fb", fg="#27305b", font=("Segoe UI Semibold", 13)).pack(side="left", padx=(0, 18))
        tk.Label(toolbar, text="View", bg="#f4f6fb", fg="#667085").pack(side="left")
        filter_box = ttk.Combobox(toolbar, textvariable=self.filter_value, values=("All", "Active", "Completed"), state="readonly", width=12)
        filter_box.pack(side="left", padx=(7, 15)); filter_box.bind("<<ComboboxSelected>>", lambda _e: self.refresh())
        tk.Entry(toolbar, textvariable=self.search_value, width=28, relief="solid", bd=1, font=("Segoe UI", 10), highlightthickness=0).pack(side="left")
        self.search_value.trace_add("write", lambda *_: self.refresh())
        ttk.Button(toolbar, text="Complete / reopen", style="Soft.TButton", command=self.toggle_complete).pack(side="right")
        ttk.Button(toolbar, text="Delete", command=self.delete_task).pack(side="right", padx=8)

        table_frame = tk.Frame(main, bg="white", bd=1, relief="solid")
        table_frame.grid(row=3, column=0, sticky="nsew")
        columns = ("status", "title", "category", "priority", "due")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        for column, heading, width in (("status", "Status", 110), ("title", "Task", 310), ("category", "Category", 150), ("priority", "Priority", 110), ("due", "Due date", 135)):
            self.table.heading(column, text=heading)
            self.table.column(column, width=width, anchor="w")
        self.table.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scroll.pack(side="right", fill="y"); self.table.configure(yscrollcommand=scroll.set)
        self.table.bind("<<TreeviewSelect>>", self.load_selection)
        self.table.bind("<Double-1>", lambda _e: self.toggle_complete())
        self.table.tag_configure("high", foreground="#b42318")
        self.table.tag_configure("medium", foreground="#9a6700")
        self.table.tag_configure("low", foreground="#1570ef")
        self.table.tag_configure("done", foreground="#7b879e")
        self.status = tk.Label(main, bg="#f4f6fb", fg="#667085", font=("Segoe UI", 9))
        self.status.grid(row=4, column=0, sticky="w", pady=(10, 0))

    @staticmethod
    def make_stat_card(parent: tk.Widget, column: int, label: str, value: str, caption: str, color: str) -> dict[str, tk.Label]:
        card = tk.Frame(parent, bg="white", padx=17, pady=13, highlightbackground="#e7eaf3", highlightthickness=1)
        card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 8, 8 if column < 2 else 0))
        tk.Label(card, text=label, bg="white", fg=color, font=("Segoe UI Semibold", 8)).pack(anchor="w")
        number = tk.Label(card, text=value, bg="white", fg="#1f2937", font=("Segoe UI", 22, "bold"))
        number.pack(anchor="w", pady=(2, 0))
        tk.Label(card, text=caption, bg="white", fg="#8a93a8", font=("Segoe UI", 9)).pack(anchor="w")
        return {"value": number}

    @staticmethod
    def make_entry(parent: tk.Widget, label: str, variable: tk.StringVar, row: int, column: int) -> None:
        tk.Label(parent, text=label, bg="white", fg="#556080", font=("Segoe UI", 9)).grid(row=row, column=column, sticky="w", padx=(0 if column == 0 else 10, 0))
        tk.Entry(parent, textvariable=variable, relief="solid", bd=1, font=("Segoe UI", 10)).grid(row=row + 1, column=column, sticky="ew", padx=(0 if column == 0 else 10, 0), pady=(3, 0))

    def load_tasks(self) -> list[dict]:
        try:
            with DATA_FILE.open(encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def persist(self) -> None:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=2, ensure_ascii=False)

    def visible_tasks(self) -> list[dict]:
        query = self.search_value.get().strip().casefold()
        filtered = []
        for task in self.tasks:
            if self.filter_value.get() == "Active" and task["completed"]:
                continue
            if self.filter_value.get() == "Completed" and not task["completed"]:
                continue
            if query and query not in f'{task["title"]} {task["category"]}'.casefold():
                continue
            filtered.append(task)
        return sorted(filtered, key=lambda item: (item["completed"], item["due"] or "9999-12-31", item["id"]))

    def refresh(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)
        for task in self.visible_tasks():
            state = "Done" if task["completed"] else "To do"
            tag = "done" if task["completed"] else task["priority"].lower()
            self.table.insert("", "end", iid=str(task["id"]), tags=(tag,), values=(state, task["title"], task["category"] or "-", task["priority"], task["due"] or "-"))
        done = sum(task["completed"] for task in self.tasks)
        active = len(self.tasks) - done
        self.total_card["value"].config(text=str(len(self.tasks)))
        self.active_card["value"].config(text=str(active))
        self.done_card["value"].config(text=str(done))
        self.status.config(text=f"{len(self.tasks)} task{'s' if len(self.tasks) != 1 else ''} total  |  {done} completed  |  Double-click a task to toggle completion")

    def clear_form(self) -> None:
        self.selected_id = None
        self.title_value.set(""); self.category_value.set(""); self.due_value.set(""); self.priority_value.set("Medium")
        for item in self.table.selection(): self.table.selection_remove(item)

    def save_task(self) -> None:
        title = self.title_value.get().strip()
        due = self.due_value.get().strip()
        if not title:
            messagebox.showwarning("Task title required", "Please give the task a name.")
            return
        if due:
            try: date.fromisoformat(due)
            except ValueError:
                messagebox.showwarning("Invalid due date", "Use the YYYY-MM-DD date format.")
                return
        record = {"title": title, "category": self.category_value.get().strip(), "due": due, "priority": self.priority_value.get()}
        if self.selected_id is None:
            record.update({"id": max((task["id"] for task in self.tasks), default=0) + 1, "completed": False})
            self.tasks.append(record)
        else:
            task = next((item for item in self.tasks if item["id"] == self.selected_id), None)
            if task: task.update(record)
        self.persist(); self.clear_form(); self.refresh()

    def selected_task(self) -> dict | None:
        selection = self.table.selection()
        if not selection:
            messagebox.showinfo("Choose a task", "Select a task from the list first.")
            return None
        return next((task for task in self.tasks if task["id"] == int(selection[0])), None)

    def load_selection(self, _event: object = None) -> None:
        task = self.selected_task() if self.table.selection() else None
        if task:
            self.selected_id = task["id"]
            self.title_value.set(task["title"]); self.category_value.set(task["category"])
            self.due_value.set(task["due"]); self.priority_value.set(task["priority"])

    def toggle_complete(self) -> None:
        task = self.selected_task()
        if task:
            task["completed"] = not task["completed"]
            self.persist(); self.refresh()

    def delete_task(self) -> None:
        task = self.selected_task()
        if task and messagebox.askyesno("Delete task", f'Delete "{task["title"]}"?'):
            self.tasks.remove(task); self.persist(); self.clear_form(); self.refresh()


if __name__ == "__main__":
    TodoApp().mainloop()

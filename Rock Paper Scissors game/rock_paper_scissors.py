"""A colourful Rock, Paper, Scissors desktop game made with Tkinter."""

import random
import tkinter as tk
from tkinter import messagebox


CHOICES = ("Rock", "Paper", "Scissors")
EMOJI = {"Rock": "✊", "Paper": "✋", "Scissors": "✌"}
COLORS = {
    "Rock": ("#F47A5B", "#FFF0EC"),
    "Paper": ("#E6AE36", "#FFF8E5"),
    "Scissors": ("#4A9CC9", "#EAF7FF"),
}


class RockPaperScissors(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock • Paper • Scissors")
        self.geometry("800x650")
        self.minsize(680, 570)
        self.configure(bg="#EAF0EB")

        self.player_score = 0
        self.computer_score = 0
        self.round_number = 1

        self._build_interface()
        self.bind("r", lambda _event: self.play("Rock"))
        self.bind("p", lambda _event: self.play("Paper"))
        self.bind("s", lambda _event: self.play("Scissors"))
        self.bind("R", lambda _event: self.play("Rock"))
        self.bind("P", lambda _event: self.play("Paper"))
        self.bind("S", lambda _event: self.play("Scissors"))

    def _build_interface(self):
        card = tk.Frame(self, bg="#FFFDF8", highlightthickness=1, highlightbackground="#D5DDD5")
        card.pack(fill="both", expand=True, padx=28, pady=24)

        tk.Label(card, text="THE CLASSIC HAND GAME", bg="#FFFDF8", fg="#C85E3F",
                 font=("Consolas", 10, "bold")).pack(pady=(30, 6))
        tk.Label(card, text="Rock  •  Paper  •  Scissors", bg="#FFFDF8", fg="#1B2A23",
                 font=("Segoe UI", 28, "bold")).pack()
        tk.Label(card, text="Choose a move and try to outsmart the computer.", bg="#FFFDF8", fg="#66746C",
                 font=("Segoe UI", 11)).pack(pady=(8, 22))

        score_box = tk.Frame(card, bg="#FFFFFF", highlightthickness=1, highlightbackground="#D5DDD5")
        score_box.pack(padx=150, fill="x")
        self.player_score_label = self._score_column(score_box, "YOU", "#D45B3C")
        tk.Label(score_box, text="VS", bg="#FFFFFF", fg="#859088", font=("Consolas", 11, "bold")).pack(side="left", padx=32)
        self.computer_score_label = self._score_column(score_box, "COMPUTER", "#397AA4", right=True)

        arena = tk.Frame(card, bg="#F5F3ED")
        arena.pack(fill="x", padx=42, pady=(24, 0))
        arena.grid_columnconfigure((0, 1, 2), weight=1)
        self.player_move = self._move_column(arena, "YOUR PICK", 0)
        centre = tk.Frame(arena, bg="#F5F3ED")
        centre.grid(row=0, column=1, sticky="nsew", padx=10, pady=16)
        self.round_label = tk.Label(centre, text="ROUND 01", bg="#F5F3ED", fg="#C85E3F", font=("Consolas", 10, "bold"))
        self.round_label.pack(pady=(8, 4))
        self.result_label = tk.Label(centre, text="Make your move", bg="#F5F3ED", fg="#1B2A23", font=("Segoe UI", 17, "bold"))
        self.result_label.pack()
        self.detail_label = tk.Label(centre, text="Rock beats scissors, scissors beat paper, paper beats rock.", bg="#F5F3ED", fg="#66746C", wraplength=225, justify="center", font=("Segoe UI", 9))
        self.detail_label.pack(pady=(4, 8))
        self.computer_move = self._move_column(arena, "COMPUTER", 2)

        choices = tk.Frame(card, bg="#FFFDF8")
        choices.pack(fill="x", padx=42, pady=26)
        for choice, key in zip(CHOICES, ("R", "P", "S")):
            color, pale = COLORS[choice]
            button = tk.Button(choices, text=f"{EMOJI[choice]}\n{choice.upper()}\n[{key}]", command=lambda c=choice: self.play(c),
                               bg=pale, activebackground=color, fg="#1B2A23", cursor="hand2",
                               font=("Segoe UI Emoji", 12, "bold"), relief="flat", bd=0, padx=24, pady=12)
            button.pack(side="left", expand=True, fill="both", padx=7)

        footer = tk.Frame(card, bg="#FFFDF8")
        footer.pack(fill="x", padx=42, pady=(0, 22))
        tk.Button(footer, text="Reset score", command=self.reset, bg="#FFFDF8", fg="#66746C",
                  activebackground="#FFFDF8", activeforeground="#1B2A23", relief="flat", cursor="hand2",
                  font=("Segoe UI", 9, "underline")).pack(side="left")
        tk.Label(footer, text="Tip: use R, P, or S on your keyboard", bg="#FFFDF8", fg="#7B8780", font=("Segoe UI", 9)).pack(side="right")

    @staticmethod
    def _move_column(parent, title, column):
        frame = tk.Frame(parent, bg="#F5F3ED")
        frame.grid(row=0, column=column, sticky="nsew", pady=16)
        tk.Label(frame, text=title, bg="#F5F3ED", fg="#66746C", font=("Consolas", 9, "bold")).pack()
        label = tk.Label(frame, text="?", width=3, bg="#E8E7E1", fg="#9CA69F", font=("Segoe UI", 31, "bold"))
        label.pack(pady=(8, 0))
        return label

    @staticmethod
    def _score_column(parent, name, color, right=False):
        frame = tk.Frame(parent, bg="#FFFFFF")
        frame.pack(side="right" if right else "left", expand=True, pady=10)
        tk.Label(frame, text=name, bg="#FFFFFF", fg="#66746C", font=("Consolas", 9, "bold")).pack()
        value = tk.Label(frame, text="0", bg="#FFFFFF", fg=color, font=("Segoe UI", 24, "bold"))
        value.pack()
        return value

    def play(self, player):
        computer = random.choice(CHOICES)
        self._show_move(self.player_move, player)
        self._show_move(self.computer_move, computer)

        if player == computer:
            title, detail = "It's a tie!", f"You both chose {player.lower()}. Try another round."
        elif (player, computer) in (("Rock", "Scissors"), ("Paper", "Rock"), ("Scissors", "Paper")):
            self.player_score += 1
            title, detail = "You win this round!", f"{player} beats {computer.lower()}. Nicely played."
        else:
            self.computer_score += 1
            title, detail = "Computer wins this round", f"{computer} beats {player.lower()}. Go again!"

        self.player_score_label.config(text=str(self.player_score))
        self.computer_score_label.config(text=str(self.computer_score))
        self.result_label.config(text=title)
        self.detail_label.config(text=detail)
        self.round_number += 1
        self.round_label.config(text=f"ROUND {self.round_number:02d}")

    def _show_move(self, label, choice):
        color, pale = COLORS[choice]
        label.config(text=EMOJI[choice], bg=pale, fg=color)

    def reset(self):
        if not messagebox.askyesno("Reset score", "Reset both scores and begin again?"):
            return
        self.player_score = self.computer_score = 0
        self.round_number = 1
        self.player_score_label.config(text="0")
        self.computer_score_label.config(text="0")
        self.round_label.config(text="ROUND 01")
        self.result_label.config(text="Make your move")
        self.detail_label.config(text="Rock beats scissors, scissors beat paper, paper beats rock.")
        for label in (self.player_move, self.computer_move):
            label.config(text="?", bg="#E8E7E1", fg="#9CA69F")


if __name__ == "__main__":
    RockPaperScissors().mainloop()

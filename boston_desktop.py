#!/usr/bin/env python3
"""BostonBBS standalone desktop preview. No radio or server connection."""
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from boston_personality import load_settings, save_settings, phrase

SETTINGS = Path.home() / ".bostonbbs" / "personality.json"
BG, PANEL, GREEN, RED, CREAM = "#101a18", "#1c2d29", "#138b58", "#d94343", "#f5eedc"

class BostonDesktop:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings(SETTINGS)
        root.title("BOSTON BBS | THE HUB • 617")
        root.geometry("780x520")
        root.minsize(640, 430)
        root.configure(bg=BG)
        tk.Label(root, text="BOSTON BBS", bg=BG, fg=CREAM, font=("Menlo", 26, "bold")).pack(pady=(25, 3))
        tk.Label(root, text="THE HUB  •  617  •  WICKED PISSAH EDITION", bg=BG, fg=GREEN, font=("Menlo", 11)).pack()
        frame = tk.Frame(root, bg=PANEL, padx=20, pady=20)
        frame.pack(fill="both", expand=True, padx=25, pady=22)
        tk.Label(frame, text="THE ATTITUDE ADJUSTAH", bg=PANEL, fg=CREAM, font=("Menlo", 15, "bold")).pack(anchor="w")
        self.mode = tk.StringVar(value=self.settings["mode"])
        self.level = tk.IntVar(value=self.settings["intensity"])
        row = tk.Frame(frame, bg=PANEL)
        row.pack(anchor="w", pady=12)
        for label, mode in (("Wicked Clean", "clean"), ("No Filtah (opt-in)", "uncensored")):
            tk.Radiobutton(row, text=label, value=mode, variable=self.mode, command=self.apply,
                           bg=PANEL, fg=CREAM, selectcolor=BG, activebackground=PANEL,
                           activeforeground=CREAM).pack(side="left", padx=(0, 18))
        row2 = tk.Frame(frame, bg=PANEL)
        row2.pack(anchor="w")
        tk.Label(row2, text="Boston attitude:", bg=PANEL, fg=CREAM).pack(side="left", padx=(0, 15))
        for value, label in ((3, "Mild"), (7, "Heavy"), (11, "11/10")):
            tk.Radiobutton(row2, text=label, value=value, variable=self.level, command=self.apply,
                           bg=PANEL, fg=CREAM, selectcolor=BG, activebackground=PANEL,
                           activeforeground=CREAM).pack(side="left", padx=5)
        self.preview = tk.Message(frame, width=650, bg=BG, fg=CREAM, font=("Menlo", 12), padx=15, pady=18)
        self.preview.pack(fill="x", pady=18)
        tk.Button(frame, text="RESET TO WICKED CLEAN", command=self.reset, bg=RED, fg="white",
                  relief="flat", padx=12, pady=8).pack(anchor="w")
        tk.Label(frame, text="DEMO MODE • No radio connection • No transmissions", bg=PANEL, fg=GREEN,
                 font=("Menlo", 10)).pack(anchor="w", pady=(20, 0))
        self.refresh()

    def refresh(self):
        self.preview.configure(text=phrase("welcome", self.settings))

    def apply(self):
        self.settings = save_settings(SETTINGS, {"mode": self.mode.get(), "intensity": self.level.get()})
        self.refresh()

    def reset(self):
        self.mode.set("clean")
        self.level.set(11)
        self.apply()

if __name__ == "__main__":
    root = tk.Tk()
    BostonDesktop(root)
    root.mainloop()

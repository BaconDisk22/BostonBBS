#!/usr/bin/env python3
"""BostonBBS desktop launcher. Process status is not proof of radio connectivity."""
import os
from pathlib import Path
import subprocess
import sys
import threading
import queue
import tkinter as tk
from tkinter import ttk, messagebox
from boston_personality import load_settings, save_settings, phrase

ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
DATA = Path.home() / ".bostonbbs"
CONFIG = DATA / "personality.json"
BG, PANEL, RED, GREEN, WHITE = "#101215", "#1b2228", "#d8192e", "#19b86c", "#f6f1e9"

class BostonApp:
    def __init__(self, root):
        self.root = root
        self.process = None
        self.lines = queue.Queue()
        self.settings = load_settings(CONFIG)
        self.mode = tk.StringVar(value=self.settings["mode"])
        self.intensity = tk.IntVar(value=self.settings["intensity"])
        self.demo = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value="SERVER STOPPED • Radio not connected")
        root.title("BostonBBS | Boston Communications Division")
        root.geometry("960x700")
        root.minsize(760, 580)
        root.configure(bg=BG)
        self.label(root, "BOSTON BBS", 32, WHITE).pack(pady=(22, 0))
        self.label(root, "BOSTON • COMMUNICATIONS DIVISION • WICKED NODES", 11, RED).pack(pady=(0, 16))
        nav = tk.Frame(root, bg=PANEL, padx=14, pady=12)
        nav.pack(fill="x", padx=18)
        self.label(nav, "THE HUB  /  BBS  /  RADIO  /  NODES  /  SETTINGS", 12).pack(anchor="w")
        top = tk.Frame(root, bg=BG)
        top.pack(fill="x", padx=18, pady=14)
        left = tk.Frame(top, bg=PANEL, padx=18, pady=16)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.label(left, "BBS SERVER", 16).pack(anchor="w")
        tk.Label(left, textvariable=self.status, bg=PANEL, fg=GREEN, wraplength=380).pack(anchor="w", pady=10)
        tk.Button(left, text="START LIVE BBS", command=self.start, bg=GREEN, fg="black", padx=14, pady=9).pack(fill="x", pady=4)
        tk.Button(left, text="STOP SERVER", command=self.stop, bg=RED, fg="white", padx=14, pady=9).pack(fill="x", pady=4)
        tk.Checkbutton(left, text="Demo mode (no radio)", variable=self.demo, bg=PANEL, fg=WHITE,
                       selectcolor=BG, activebackground=PANEL, activeforeground=WHITE).pack(anchor="w", pady=8)
        right = tk.Frame(top, bg=PANEL, padx=18, pady=16)
        right.pack(side="left", fill="both", expand=True)
        self.label(right, "THE ATTITUDE ADJUSTAH", 16).pack(anchor="w")
        for title, value in (("Clean (default)", "clean"), ("Uncensored (opt-in)", "uncensored")):
            tk.Radiobutton(right, text=title, value=value, variable=self.mode, command=self.save,
                           bg=PANEL, fg=WHITE, selectcolor=BG, activebackground=PANEL,
                           activeforeground=WHITE).pack(anchor="w")
        for value in (3, 7, 11):
            tk.Radiobutton(right, text=f"Attitude {value}/11", value=value, variable=self.intensity,
                           command=self.save, bg=PANEL, fg=WHITE, selectcolor=BG,
                           activebackground=PANEL, activeforeground=WHITE).pack(anchor="w")
        self.preview = tk.StringVar()
        tk.Label(right, textvariable=self.preview, bg=PANEL, fg=WHITE,
                 wraplength=380, justify="left").pack(anchor="w", pady=8)
        logframe = tk.Frame(root, bg=PANEL, padx=14, pady=12)
        logframe.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        self.label(logframe, "SERVER LOG • LIVE PROCESS OUTPUT", 14).pack(anchor="w")
        self.log = tk.Text(logframe, bg="#080c0d", fg="#81e6a6", insertbackground=WHITE,
                           height=12, font=("Menlo", 10), state="disabled")
        self.log.pack(fill="both", expand=True, pady=(10, 0))
        self.save()
        root.after(200, self.poll)
        root.protocol("WM_DELETE_WINDOW", self.close)

    def label(self, parent, text, size, color=WHITE):
        return tk.Label(parent, text=text, bg=parent["bg"], fg=color, font=("Menlo", size, "bold"))

    def save(self):
        self.settings = save_settings(CONFIG, {"mode": self.mode.get(), "intensity": self.intensity.get()})
        self.preview.set(phrase("welcome", self.settings))

    def write(self, line):
        self.log.configure(state="normal")
        self.log.insert("end", line + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def start(self):
        if self.process and self.process.poll() is None:
            self.write("Server process already running.")
            return
        if self.demo.get():
            self.status.set("DEMO • No radio connection")
            self.write("Demo mode active. No packets sent.")
            return
        server = ROOT / "server.py"
        config = DATA / "config.ini"
        if not server.is_file():
            messagebox.showerror("Missing server", "server.py is missing from this build.")
            return
        if not config.is_file():
            DATA.mkdir(parents=True, exist_ok=True)
            example = ROOT / "example_config.ini"
            if example.exists():
                config.write_bytes(example.read_bytes())
            messagebox.showwarning("Configure radio first",
                f"Review your radio settings in {config} before starting the BBS.")
            return
        try:
            command = ([sys.executable, "--bbs-server", "--config", str(config)]\n                       if getattr(sys, "frozen", False) else\n                       [sys.executable, "-u", str(server), "--config", str(config)])\n            self.process = subprocess.Popen(command,
                cwd=str(DATA), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1)
        except OSError as exc:
            messagebox.showerror("Server launch failed", str(exc))
            return
        self.status.set("BBS PROCESS STARTING • Radio unverified")
        self.write("Started server process. Waiting for radio connection logs.")
        threading.Thread(target=self.read_output, args=(self.process,), daemon=True).start()

    def read_output(self, process):
        for line in process.stdout:
            self.lines.put(line.rstrip())
        self.lines.put(f"Server process exited with code {process.wait()}")

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.write("Stop requested.")
        self.status.set("SERVER STOPPED • Radio not connected")

    def poll(self):
        while not self.lines.empty():
            line = self.lines.get_nowait()
            self.write(line)
            if "exited with code" in line:
                self.status.set("SERVER STOPPED • Check log")
        self.root.after(200, self.poll)

    def close(self):
        self.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    BostonApp(root)
    root.mainloop()

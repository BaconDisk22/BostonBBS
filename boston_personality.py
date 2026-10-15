"""Boston BBS personality settings: local-only, clean by default.

Only apply personality to app-authored decorative text. Never alter user messages,
radio payloads, diagnostics, alerts, or weather/emergency notices.
"""
from __future__ import annotations
import json
from pathlib import Path

MODES = ("clean", "uncensored")
INTENSITIES = (3, 7, 11)
DEFAULTS = {"mode": "clean", "intensity": 11}

LINES = {
    "welcome": {
        "clean": {
            3: "Welcome to Boston BBS. Wicked good to see ya.",
            7: "Ay, welcome to the Hub! Grab ya Dunks and check the signal.",
            11: "AYYY, LOOK WHO FINALLY SHOWED UP! Grab ya Dunks, pahk ya cah, and quit bustin' my chops. We got a wicked good signal!",
        },
        "uncensored": {
            3: "Welcome to Boston BBS. Let's get this shit running.",
            7: "Ay, where the hell ya been? Grab ya Dunks and get on the damn network.",
            11: "AYYY, WHERE THE HELL YA BEEN?! Grab ya fuckin' Dunks, pahk ya cah, and get on the damn network. This signal's wicked pissah!",
        },
    }
}

def normalize(settings: dict | None = None) -> dict:
    data = settings if isinstance(settings, dict) else {}
    mode = data.get("mode", "clean")
    intensity = data.get("intensity", 11)
    return {
        "mode": mode if mode in MODES else "clean",
        "intensity": intensity if type(intensity) is int and intensity in INTENSITIES else 11,
    }

def load_settings(path: str | Path) -> dict:
    try:
        return normalize(json.loads(Path(path).read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError):
        return DEFAULTS.copy()

def save_settings(path: str | Path, settings: dict) -> dict:
    validated = normalize(settings)
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(validated, indent=2) + "\n", encoding="utf-8")
    return validated

def phrase(key: str, settings: dict | None = None) -> str:
    selected = normalize(settings)
    return LINES[key][selected["mode"]][selected["intensity"]]

def personality_command(command: str, settings: dict, path: str | Path) -> str:
    """Handle PERSONALITY, PERSONALITY CLEAN|UNCENSORED, PERSONALITY 3|7|11."""
    parts = command.strip().upper().split()
    if not parts or parts[0] != "PERSONALITY":
        raise ValueError("Not a PERSONALITY command")
    current = normalize(settings)
    if len(parts) == 1:
        return f"THE ATTITUDE ADJUSTAH: {current['mode'].upper()}, {current['intensity']}/11. Try PERSONALITY CLEAN, PERSONALITY UNCENSORED, or PERSONALITY 3|7|11."
    if len(parts) != 2:
        return "Usage: PERSONALITY [CLEAN|UNCENSORED|3|7|11]"
    value = parts[1]
    if value in ("CLEAN", "UNCENSORED"):
        current["mode"] = value.lower()
    elif value in ("3", "7", "11"):
        current["intensity"] = int(value)
    else:
        return "Usage: PERSONALITY [CLEAN|UNCENSORED|3|7|11]"
    settings.update(save_settings(path, current))
    return f"Attitude adjusted: {current['mode'].upper()}, {current['intensity']}/11."

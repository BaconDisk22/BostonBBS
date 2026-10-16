"""Boston BBS personality: clean by default, opt-in colorful language.

Use only for locally generated flavor text, never user messages, radio payloads,
weather/emergency alerts, diagnostics, or system errors.
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

MODES = ("clean", "uncensored")
INTENSITIES = (3, 7, 11)
DEFAULTS = {"mode": "clean", "intensity": 11}
HELP = "PERSONALITY [STATUS|CLEAN|UNCENSORED|3|7|11|RESET|PREVIEW]"

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
    },
    "goodbye": {
        "clean": {
            3: "See ya around the Hub.",
            7: "Catch ya latah. Keep that signal wicked strong.",
            11: "AYY, GET OUTTA HEAH! Don't forget ya Dunks on the way out.",
        },
        "uncensored": {
            3: "See ya around the damn Hub.",
            7: "Catch ya latah. Keep that damn signal strong.",
            11: "AYY, GET THE HELL OUTTA HEAH! Don't forget ya fuckin' Dunks.",
        },
    },
}

def normalize(settings: dict | None = None) -> dict:
    data = settings if isinstance(settings, dict) else {}
    mode = data.get("mode", "clean")
    intensity = data.get("intensity", 11)
    return {
        "mode": mode if isinstance(mode, str) and mode in MODES else "clean",
        "intensity": intensity if type(intensity) is int and intensity in INTENSITIES else 11,
    }

def load_settings(path: str | Path) -> dict:
    try:
        return normalize(json.loads(Path(path).expanduser().read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError):
        return DEFAULTS.copy()

def save_settings(path: str | Path, settings: dict) -> dict:
    """Persist settings with an atomic replace to avoid partial JSON writes."""
    validated = normalize(settings)
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent,
                                         prefix=".boston-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(validated, handle, indent=2)
            handle.write("\n")
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return validated

def phrase(key: str, settings: dict | None = None) -> str:
    selected = normalize(settings)
    return LINES[key][selected["mode"]][selected["intensity"]]

def personality_command(command: str, settings: dict, path: str | Path) -> str:
    """Parse a command; invalid commands never modify persisted settings."""
    parts = command.strip().upper().split()
    if not parts or parts[0] != "PERSONALITY":
        raise ValueError("Not a PERSONALITY command")
    current = normalize(settings)
    if len(parts) == 1 or parts == ["PERSONALITY", "STATUS"]:
        return f"THE ATTITUDE ADJUSTAH: {current['mode'].upper()}, {current['intensity']}/11. {HELP}"
    if len(parts) != 2:
        return f"Usage: {HELP}"
    value = parts[1]
    if value == "PREVIEW":
        return phrase("welcome", current)
    if value == "RESET":
        current = DEFAULTS.copy()
    elif value in ("CLEAN", "UNCENSORED"):
        current["mode"] = value.lower()
    elif value in ("3", "7", "11"):
        current["intensity"] = int(value)
    else:
        return f"Usage: {HELP}"
    saved = save_settings(path, current)
    settings.clear()
    settings.update(saved)
    return f"Attitude adjusted: {saved['mode'].upper()}, {saved['intensity']}/11."

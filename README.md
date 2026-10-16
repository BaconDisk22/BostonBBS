# BostonBBS — The Hub

**Wicked smaht communications. No nonsense.**

Boston-flavored personality support for a future Boston edition of the TC2 mesh BBS. This repository currently contains a standalone personality module and tests; **the complete BBS server, radio integration, and Mac app have not yet been imported or built.**

## The Attitude Adjustah

Clean language is the default. Users must explicitly opt into uncensored flavor text. The attitude level defaults to 11/11 and supports 3, 7, and 11.

| Command | What it does |
| --- | --- |
| `PERSONALITY` or `PERSONALITY STATUS` | Show current settings |
| `PERSONALITY CLEAN` | Disable profanity |
| `PERSONALITY UNCENSORED` | Enable profanity for generated flavor text |
| `PERSONALITY 3`, `7`, or `11` | Adjust intensity |
| `PERSONALITY PREVIEW` | Preview the welcome text |
| `PERSONALITY RESET` | Restore clean defaults |

These commands are implemented in `boston_personality.py` as a reusable handler. They **are not wired into a running BBS command router yet**.

### Integration example

```python
from pathlib import Path
from boston_personality import load_settings, personality_command, phrase

settings_path = Path.home() / ".bostonbbs" / "personality.json"
settings = load_settings(settings_path)

print(phrase("welcome", settings))
print(personality_command("PERSONALITY PREVIEW", settings, settings_path))
```

Use `phrase("welcome", settings)` and `phrase("goodbye", settings)` only for application-generated decorative text. Never modify user-generated content, radio packets, system diagnostics, emergency alerts, or weather warnings.

### Tests

```sh
python3 -m unittest discover -v
```

## Roadmap

- Import and independently maintain the working Sitdown BBS codebase
- Connect personality commands to the real BBS menu and command dispatcher
- Build a Fenway-green / MBTA-inspired Boston terminal interface
- Add Boston-themed menus, neighborhood references, and optional Easter eggs
- Build and validate an Intel macOS application and release automation

## Attribution

BostonBBS is planned as an adaptation of [The Sitdown BBS](https://github.com/BaconDisk22/The-Sitdown-BBS), itself derived from [TC2-BBS-mesh](https://github.com/TheCommsChannel/TC2-BBS-mesh). Preserve upstream license and attribution when importing code.

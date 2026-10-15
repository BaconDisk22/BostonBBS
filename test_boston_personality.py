import tempfile
import unittest
from pathlib import Path
from boston_personality import load_settings, save_settings, phrase, personality_command

class PersonalityTests(unittest.TestCase):
    def test_default_clean(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(load_settings(Path(folder) / "missing.json"), {"mode": "clean", "intensity": 11})

    def test_opt_in_and_persistence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "settings.json"
            settings = load_settings(path)
            personality_command("PERSONALITY UNCENSORED", settings, path)
            self.assertEqual(load_settings(path)["mode"], "uncensored")
            personality_command("PERSONALITY CLEAN", settings, path)
            self.assertEqual(load_settings(path)["mode"], "clean")

    def test_intensity(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "settings.json"
            settings = load_settings(path)
            personality_command("PERSONALITY 3", settings, path)
            self.assertEqual(load_settings(path)["intensity"], 3)

    def test_invalid_values_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "settings.json"
            save_settings(path, {"mode": "anything", "intensity": 99})
            self.assertEqual(load_settings(path), {"mode": "clean", "intensity": 11})
            self.assertEqual(phrase("welcome", load_settings(path)), phrase("welcome", {"mode": "clean", "intensity": 11}))

if __name__ == "__main__":
    unittest.main()

import os
import json

class Settings:
    """
    A simple settings storage with load/save stubs.
    """
    def __init__(self) -> None:
        self._data = {
            "auto_shuffle": False,
            "hard_level": False,
            "auto_win_mode": "ask",
            "language": "eng"
        }
        self.path = os.path.join("game", "config", "settings.json")
        self.load()

    def load(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as file:
                try:
                    self._data.update(json.load(file))
                except json.JSONDecodeError:
                    pass
        else:
            self.save()

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self._data, file, indent=4)
        self.load()

    def change(self, key: str, value) -> None:
        self._data[key] = value
        self.save()
    
    def get(self, key, default=None):
        return self._data.get(key, default)
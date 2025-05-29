import os
import json


class Settings:
    """Handles game settings with persistent JSON storage.

    This class loads settings from a JSON file on initialization,
    allows changing settings, and saves them back to the file.
    """

    def __init__(self) -> None:
        """Initialize default settings and load from file if it exists."""
        self._data = {
            "auto_shuffle": False,
            "hard_level": False,
            "music": True,
            "auto_win_mode": "ask",
            "language": "en",
        }
        self.path = os.path.join("game", "config", "settings.json")
        self.load()

    def load(self) -> dict:
        """Load settings from the JSON file.

        If the file exists and contains valid JSON, update the settings.
        Otherwise, save default settings to create the file.

        Returns:
            dict: The current settings dictionary.
        """
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as file:
                try:
                    self._data.update(json.load(file))
                except json.JSONDecodeError:
                    # Ignore invalid JSON and keep defaults
                    pass
        else:
            self.save()
        return self._data

    def save(self) -> None:
        """Save the current settings to the JSON file."""
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self._data, file, indent=4)
        # Reload to ensure consistency
        self.load()

    def change(self, key: str, value) -> None:
        """Change a setting and immediately save it.

        Args:
            key (str): The key of the setting to change.
            value: The new value to assign to the key.
        """
        self._data[key] = value
        self.save()

    def get(self, key, default=None):
        """Get a setting value by key.

        Args:
            key: The key to retrieve.
            default: The value to return if key is not found.

        Returns:
            The value associated with the key or default if missing.
        """
        return self._data.get(key, default)

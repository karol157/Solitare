import json
import os

class Translator:
    """Handles loading and providing translations for a specified language."""

    def __init__(self, language_code='en'):
        """
        Initialize the translator with a language code.

        Args:
            language_code (str): The language code to load translations for (default 'en').
        """
        self.language_code = language_code
        self.translations = {}
        self.load_language(language_code)

    def load_language(self, language_code):
        """
        Load translation data from a JSON file for the given language code.

        Args:
            language_code (str): The language code corresponding to the translation file.
        """
        locale_path = os.path.join('locales', f'{language_code}.json')
        try:
            with open(locale_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            # If translation file is missing, fallback to empty dict
            self.translations = {}

    def set_language(self, language_code):
        """
        Change the current language and reload translations.

        Args:
            language_code (str): The new language code to set.
        """
        self.language_code = language_code
        self.load_language(language_code)

    def t(self, key):
        """
        Translate a key to the current language.

        Args:
            key (str): The translation key to lookup.

        Returns:
            str: The translated string if found, else returns the key itself.
        """
        return self.translations.get(key, key)

import json
import os

class Translator:
    def __init__(self, language_code='en'):
        self.language_code = language_code
        self.translations = {}
        self.load_language(language_code)

    def load_language(self, language_code):
        locale_path = os.path.join('locales', f'{language_code}.json')
        try:
            with open(locale_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            self.translations = {}

    def set_language(self, language_code):
        self.language_code = language_code
        self.load_language(language_code)

    def t(self, key):
        return self.translations.get(key, key)
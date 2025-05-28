from textual import events
from textual.widgets import Static
import asyncio
from .translator import Translator
from .Settings import Settings


class Timer:
    minutes = 0  # class variable
    seconds = 0  # class variable

    def __init__(self, widget, language_code='en'):
        # self.seconds = 0
        # self.minutes = 0
        self.timer = None
        self.widget = widget
        self.translator = Translator(language_code)

    def start(self):
        if self.timer and not self.timer.done():
            self.timer.cancel()
        self.timer = asyncio.create_task(self.loop())

    def stop(self):
        if self.timer and not self.timer.done():
            self.timer.cancel()

    def reset(self):
        self.stop()
        Timer.minutes = 0
        Timer.seconds = 0
        self.start()

    async def loop(self):
        while True:
            await asyncio.sleep(1)
            Timer.seconds += 1
            if Timer.seconds >= 60:
                Timer.minutes += 1
                Timer.seconds = 0
            self.widget.update_info()


class Score:
    score = 0  # class variable

    @classmethod
    def add(cls, value):
        cls.score += value

    @classmethod
    def reset(cls):
        cls.score = 0


class Information(Static):
    def on_mount(self, event: events.Mount) -> None:
        settings = Settings()
        language_code = settings.get("language", "en")
        self.timer = Timer(self, language_code=language_code)
        self.translator = Translator(language_code)
        self.update_info()
        self.timer.start()

    def update_info(self):
        self.update(
            f"{self.translator.t('time')}: {self.timer.minutes}:{self.timer.seconds:02d} min\n"
            f"{self.translator.t('score')}: {Score.score}"
        )

    def reset(self):
        self.timer.reset()
        Score.reset()
        self.update_info()

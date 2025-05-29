from textual import events
from textual.widgets import Static
import asyncio
from game.translator import Translator
from game.Settings import Settings


class Timer:
    """Manages time tracking and updates the UI widget with elapsed time."""

    minutes = 0  # Elapsed minutes
    seconds = 0  # Elapsed seconds
    timer = None  # asyncio task for the timer loop

    def __init__(self, widget, language_code='en'):
        """
        Initialize the timer.

        Args:
            widget (Widget): The widget that displays timer information.
            language_code (str): Language code for translation (default: 'en').
        """
        self.widget = widget
        self.translator = Translator(language_code)

    def start(self):
        """Start or restart the timer loop."""
        if Timer.timer and not Timer.timer.done():
            Timer.timer.cancel()
        Timer.timer = asyncio.create_task(self.loop())

    def stop(self):
        """Stop the timer loop."""
        if Timer.timer and not Timer.timer.done():
            Timer.timer.cancel()

    def reset(self):
        """Reset the timer to 0 and restart it."""
        self.stop()
        Timer.minutes = 0
        Timer.seconds = 0
        self.start()

    async def loop(self):
        """Asynchronous loop that increments time every second."""
        while True:
            await asyncio.sleep(1)
            Timer.seconds += 1
            if Timer.seconds >= 60:
                Timer.minutes += 1
                Timer.seconds = 0
            self.widget.update_info()


class Score:
    """Handles the player's score."""

    score = 0  # Current score value

    @classmethod
    def add(cls, value):
        """
        Add points to the current score.

        Args:
            value (int): Number of points to add.
        """
        cls.score += value

    @classmethod
    def reset(cls):
        """Reset the score to 0."""
        cls.score = 0


class Information(Static):
    """Widget that displays the current game time and score."""

    def on_mount(self, event: events.Mount) -> None:
        """
        Called when the widget is mounted. Initializes settings and starts the timer.

        Args:
            event (events.Mount): The mount event.
        """
        settings = Settings()
        language_code = settings.get("language", "en")
        self.timer = Timer(self, language_code=language_code)
        self.translator = Translator(language_code)
        self.update_info()
        self.timer.start()

    def update_info(self):
        """Update the display with current time and score."""
        self.update(
            f"{self.translator.t('time')}: {self.timer.minutes}:{self.timer.seconds:02d} min\n"
            f"{self.translator.t('score')}: {Score.score}"
        )

    def reset(self):
        """Reset both the timer and the score, then update the display."""
        self.timer.reset()
        Score.reset()
        self.update_info()

from operator import truediv

from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.reactive import reactive
import asyncio

class Timer:
    def __init__(self):
        self.seconds = 0
        self.minutes = 0
        self.timer = None

    def start(self):
        self.timer =  asyncio.create_task(self.loop())
    def stop(self):
        self.timer.cancel()
    def reset(self):
        self.stop()
        self.minutes = 0
        self.seconds = 0

    async def loop(self):
        while True:
            await asyncio.sleep(1)
            self.seconds += 1
            if self.seconds >= 60:
                self.minutes += 1
                self.seconds = 0

class Score:
    def __init__(self):
        self.score = 0

    def add(self, value):
        self.score += value

    def reset(self):
        self.score = 0


class Information(Static):
    def _on_mount(self, event: events.Mount) -> None:
        self.value = ""
        self.timer = Timer()
        self.score = Score()
        asyncio.create_task(self.loop())

    async def loop(self):
        self.timer.start()
        while True:
            await asyncio.sleep(0.5)
            self.update(f"Time: {self.timer.minutes}:{self.timer.seconds}\n"
                        f"Score: {self.score.score}")
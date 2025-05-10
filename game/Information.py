from textual import events
from textual.widgets import Static
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
        self.minutes = 0
        self.seconds = 0

    async def loop(self):
        while True:
            await asyncio.sleep(1)
            self.seconds += 1
            if self.seconds >= 60:
                self.minutes += 1
                self.seconds = 00

class Score:
    def __init__(self):
        self.score = 0

    def add(self, value):
        self.score += value

    def reset(self):
        self.score = 00


class Information(Static):
    def _on_mount(self, event: events.Mount) -> None:
        self.value = ""
        self.timer = Timer()
        self.score = Score()
        asyncio.create_task(self.loop())

    async def loop(self):
        self.timer.start()
        while True:
            await asyncio.sleep(0.0001)
            self.update(f"Time: {self.timer.minutes}:{self.timer.seconds} min\n"
                        f"Score: {self.score.score}")

    def reset(self):
        self.timer.reset()
        self.score.reset()
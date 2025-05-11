from textual import events
from textual.widgets import Static
import asyncio

class Timer:
    seconds = 0
    minutes = 0
    def __init__(self):
        self.timer = None

    def start(self):
        self.timer =  asyncio.create_task(self.loop())
    def stop(self):
        self.timer.cancel()
    def reset(self):
        Timer.minutes = 0
        Timer.seconds = 0

    async def loop(self):
        while True:
            await asyncio.sleep(1)
            Timer.seconds += 1
            if Timer.seconds >= 60:
                Timer.minutes += 1
                Timer.seconds = 00

class Score:
    score = 0
    def add(self, value):
        Score.score += value

    def reset(self):
        Score.score = 00


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
            self.update(f"Time: {Timer.minutes}:{Timer.seconds} min\n"
                        f"Score: {Score.score}")

    def reset(self):
        self.timer.reset()
        self.score.reset()
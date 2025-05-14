from textual import events
from textual.widgets import Static
import asyncio

class Timer:
    seconds = 00
    minutes = 0
    def __init__(self, widget):
        self.timer = None
        self.widget = widget

    def start(self):
        self.timer = asyncio.create_task(self.loop())
    def stop(self):
        self.timer.cancel()
    def reset(self):
        Timer.minutes = 0
        Timer.seconds = 0
        self.start()

    async def loop(self):
        while True:
            await asyncio.sleep(1)
            Timer.seconds += 1
            if Timer.seconds >= 60:
                Timer.minutes += 1
                Timer.seconds = 00
            self.widget.update(f"Time: {Timer.minutes}:{Timer.seconds:02d} min\n")

class Score:
    score = 0
    def add(self, value):
        Score.score += value

    def reset(self):
        Score.score = 00


class Information(Static):
    def _on_mount(self, event: events.Mount) -> None:
        self.value = ""
        self.timer = Timer(self)
        self.timer.start()
        self.score = Score()
    '''        asyncio.create_task(self.loop())

    async def loop(self):
        self.timer.start()
        while True:
            self.update(f"Time: {Timer.minutes}:{Timer.seconds} min\n"
                        f"Score: {Score.score}")'''

    def reset(self):
        self.timer.reset()
        self.score.reset()
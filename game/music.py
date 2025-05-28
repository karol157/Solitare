import simpleaudio
import threading


class MusicPlayer:
    _registry = {}  # Class-level registry to keep track of instances

    def __init__(self, file_path, id):
        self.wave_obj = simpleaudio.WaveObject.from_wave_file(
            file_path
        )  # Load the sound file
        self.playing = False  # Flag to control playback
        self.thread = None  # Thread for playing the sound
        self._current = None  # Current playback object
        MusicPlayer._registry[id] = self  # Register this instance with the given id

    def _loop(self):
        while self.playing:
            self._current = self.wave_obj.play()
            self._current.wait_done()  # Wait for the sound to finish before looping

    def start(self):
        if not self.playing:
            self.playing = True
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.playing = False
        if self._current:
            self._current.stop()

    @classmethod
    def get_instance(cls, id):
        """Retrieve an instance by its id."""
        return cls._registry.get(id)

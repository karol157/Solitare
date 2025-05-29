import simpleaudio
import threading


class MusicPlayer:
    """A music player that plays WAV audio files in a loop on a background thread.

    This class supports multiple named instances tracked by an internal registry.

    Attributes:
        _registry (dict): Class-level dictionary mapping IDs to MusicPlayer instances.
    """

    _registry = {}  # Registry to keep track of MusicPlayer instances by id

    def __init__(self, file_path: str, id: str):
        """
        Initialize a MusicPlayer instance.

        Args:
            file_path (str): Path to the WAV audio file to play.
            id (str): Unique identifier for this music player instance.
        """
        self.wave_obj = simpleaudio.WaveObject.from_wave_file(file_path)
        self.playing = False
        self.thread = None
        self._current = None
        MusicPlayer._registry[id] = self

    def _loop(self):
        """Internal method to continuously play the audio while 'playing' is True."""
        while self.playing:
            self._current = self.wave_obj.play()
            self._current.wait_done()  # Block until current playback finishes

    def start(self):
        """Start playing the audio loop in a separate daemon thread."""
        if not self.playing:
            self.playing = True
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()

    def stop(self):
        """Stop playing the audio and terminate playback immediately."""
        self.playing = False
        if self._current:
            self._current.stop()

    @classmethod
    def get_instance(cls, id: str) -> "MusicPlayer":
        """
        Retrieve a MusicPlayer instance by its ID.

        Args:
            id (str): The identifier of the desired MusicPlayer instance.

        Returns:
            MusicPlayer or None: The instance if found, otherwise None.
        """
        return cls._registry.get(id)

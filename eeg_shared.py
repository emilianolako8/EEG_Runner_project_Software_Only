# eeg_shared.py
import threading
from collections import deque

class SharedEEG:
    """
    This object is shared between threads:
    - The simulator thread writes new samples into a buffer.
    - The game + plot threads read from that buffer.

    We use a Lock to avoid reading while writing (thread safety).
    """
    def __init__(self, maxlen=512):
        self.lock = threading.Lock()
        self.samples = deque(maxlen=maxlen)   # rolling raw EEG samples
        self.blink_event = False              # set True when blink detected

    def add_sample(self, x: float):
        """Add one EEG sample into the rolling buffer."""
        with self.lock:
            self.samples.append(x)

    def get_samples_copy(self):
        """Return a COPY of the buffer so readers can safely use it."""
        with self.lock:
            return list(self.samples)

    def set_blink(self):
        """Mark that a blink happened (event flag)."""
        with self.lock:
            self.blink_event = True

    def consume_blink(self) -> bool:
        """
        The game calls this.
        If a blink happened since last check, return True AND clear it.
        """
        with self.lock:
            if self.blink_event:
                self.blink_event = False
                return True
            return False

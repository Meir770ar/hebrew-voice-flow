"""Microphone recorder — captures audio into memory while active."""
import threading
import numpy as np
import sounddevice as sd


class Recorder:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.recording = False
        self.frames: list = []
        self.stream = None
        self.lock = threading.Lock()

    def _callback(self, indata, frame_count, time_info, status):
        if self.recording:
            self.frames.append(indata.copy())

    def start(self) -> bool:
        with self.lock:
            if self.recording:
                return False
            self.frames = []
            try:
                self.stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype="float32",
                    callback=self._callback,
                )
                self.stream.start()
                self.recording = True
                return True
            except Exception as e:
                print(f"[recorder] failed to start: {e}")
                self.stream = None
                return False

    def stop(self):
        with self.lock:
            if not self.recording:
                return None
            self.recording = False
            if self.stream is not None:
                try:
                    self.stream.stop()
                    self.stream.close()
                except Exception as e:
                    print(f"[recorder] stop error: {e}")
                self.stream = None
            if not self.frames:
                return None
            audio = np.concatenate(self.frames, axis=0).flatten().astype(np.float32)
            self.frames = []
            return audio

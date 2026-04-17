"""Whisper transcriber — loads on first use, auto-unloads after idle."""
import gc
import threading
import time

from faster_whisper import WhisperModel


class Transcriber:
    def __init__(
        self,
        model_size: str = "medium",
        device: str = "cuda",
        compute_type: str = "int8_float16",
        idle_timeout: int = 60,
        initial_prompt: str = "",
    ):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.idle_timeout = idle_timeout
        self.initial_prompt = initial_prompt
        self.model = None
        self.last_used = 0.0
        self.lock = threading.Lock()

        t = threading.Thread(target=self._monitor_idle, daemon=True)
        t.start()

    def _load(self):
        if self.model is not None:
            return
        print(f"[transcriber] loading {self.model_size} on {self.device} ({self.compute_type})...")
        start = time.time()
        try:
            self.model = WhisperModel(
                self.model_size, device=self.device, compute_type=self.compute_type
            )
        except Exception as e:
            print(f"[transcriber] {self.device} failed ({e}); falling back to CPU int8.")
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
        print(f"[transcriber] ready in {time.time() - start:.1f}s")

    def _unload(self):
        if self.model is None:
            return
        print("[transcriber] unloading (idle)")
        del self.model
        self.model = None
        gc.collect()
        try:
            import torch

            torch.cuda.empty_cache()
        except Exception:
            pass

    def _monitor_idle(self):
        while True:
            time.sleep(10)
            with self.lock:
                if self.model is not None and time.time() - self.last_used > self.idle_timeout:
                    self._unload()

    def transcribe(self, audio, language: str = "he") -> str:
        with self.lock:
            self._load()
            self.last_used = time.time()
            segments, _info = self.model.transcribe(
                audio,
                language=language,
                beam_size=5,
                vad_filter=True,
                initial_prompt=self.initial_prompt or None,
            )
            text = " ".join(seg.text.strip() for seg in segments).strip()
            self.last_used = time.time()
            return text

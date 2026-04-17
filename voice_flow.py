"""Voice Flow - push-to-talk dictation for Windows.

Hotkeys (push-to-talk):
  Right Ctrl  = raw Whisper transcription
  Right Alt   = Whisper + Groq gentle cleanup
  Right Shift = Whisper + Groq dev-request rewrite (for Claude Code)
"""
import json
import os
import sys
import threading

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import time
import winsound
from datetime import datetime
from pathlib import Path

import keyboard as kb_lib
import pyperclip
import pystray
from PIL import Image, ImageDraw
from pynput import keyboard
from pynput.keyboard import Controller, Key

from ai_cleaner import AiCleaner
from recorder import Recorder
from transcriber import Transcriber

BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"
HISTORY_PATH = BASE_DIR / "history.json"

DEFAULT_CONFIG = {
    "model": "medium",
    "language": "he",
    "sounds_enabled": True,
    "history_enabled": True,
    "max_history": 50,
    "min_recording_duration": 0.3,
    "idle_timeout": 60,
    "initial_prompt": "",
    "hotkeys": {"raw": "ctrl_r", "cleanup": "alt_r", "dev_request": "shift_r"},
    "groq_model": "llama-3.3-70b-versatile",
}

HOTKEY_TO_MODE = {
    "ctrl_r": ("raw", Key.ctrl_r),
    "alt_r": ("cleanup", Key.alt_r),
    "shift_r": ("dev_request", Key.shift_r),
}


def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        for k, v in DEFAULT_CONFIG.items():
            cfg.setdefault(k, v)
        return cfg
    return dict(DEFAULT_CONFIG)


def save_config(cfg: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def load_history() -> list:
    if HISTORY_PATH.exists():
        try:
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_history(history: list) -> None:
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def append_history(text: str, mode: str, cfg: dict) -> None:
    if not cfg.get("history_enabled", True):
        return
    history = load_history()
    history.insert(0, {"text": text, "mode": mode, "timestamp": datetime.now().isoformat()})
    history = history[: cfg.get("max_history", 50)]
    save_history(history)


def _beep(freq: int, dur: int, enabled: bool) -> None:
    if not enabled:
        return
    try:
        winsound.Beep(freq, dur)
    except Exception:
        pass


def _safe_print(msg: str) -> None:
    try:
        print(msg)
    except Exception:
        pass


class TrayUI:
    COLORS = {
        "idle": "#2ea043",
        "recording": "#d73a49",
        "transcribing": "#dbab09",
        "ai": "#6f42c1",
    }

    def __init__(self, app: "VoiceFlowApp"):
        self.app = app
        self.icon: pystray.Icon | None = None
        self.state = "idle"

    def _make_icon(self, color: str) -> Image.Image:
        img = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
        d = ImageDraw.Draw(img)
        d.ellipse((8, 8, 56, 56), fill=color)
        return img

    def set_state(self, state: str) -> None:
        self.state = state
        if self.icon is None:
            return
        self.icon.icon = self._make_icon(self.COLORS.get(state, "#2ea043"))
        self.icon.title = f"Voice Flow - {state}"

    def _menu(self) -> pystray.Menu:
        return pystray.Menu(
            pystray.MenuItem(lambda item: f"Voice Flow - {self.state}", None, enabled=False),
            pystray.MenuItem(
                lambda item: f"AI: {'on' if self.app.ai.available else 'off (no GROQ_API_KEY)'}",
                None,
                enabled=False,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Sounds",
                lambda icon, item: self.app.toggle_sounds(),
                checked=lambda item: self.app.cfg.get("sounds_enabled", True),
            ),
            pystray.MenuItem(
                "Save history",
                lambda icon, item: self.app.toggle_history(),
                checked=lambda item: self.app.cfg.get("history_enabled", True),
            ),
            pystray.MenuItem("Clear history", lambda icon, item: self.app.clear_history()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", lambda icon, item: self.app.quit()),
        )

    def run(self) -> None:
        self.icon = pystray.Icon(
            "voice_flow",
            self._make_icon(self.COLORS["idle"]),
            "Voice Flow - idle",
            menu=self._menu(),
        )
        self.icon.run()


class VoiceFlowApp:
    def __init__(self) -> None:
        self.cfg = load_config()
        save_config(self.cfg)
        self.recorder = Recorder()
        self.transcriber = Transcriber(
            model_size=self.cfg["model"],
            idle_timeout=self.cfg["idle_timeout"],
            initial_prompt=self.cfg.get("initial_prompt", ""),
        )
        self.ai = AiCleaner(model=self.cfg.get("groq_model", "llama-3.3-70b-versatile"))
        self.kb = Controller()
        self.tray = TrayUI(self)
        self.recording_started_at: float | None = None
        self.active_mode: str | None = None

    def toggle_sounds(self) -> None:
        self.cfg["sounds_enabled"] = not self.cfg.get("sounds_enabled", True)
        save_config(self.cfg)

    def toggle_history(self) -> None:
        self.cfg["history_enabled"] = not self.cfg.get("history_enabled", True)
        save_config(self.cfg)

    def clear_history(self) -> None:
        save_history([])

    def quit(self) -> None:
        if self.tray.icon:
            self.tray.icon.stop()
        os._exit(0)

    def _key_to_mode(self, key) -> str | None:
        if key == Key.ctrl_r:
            return "raw"
        if key == Key.alt_r:
            return "cleanup"
        if key == Key.shift_r:
            return "dev_request"
        return None

    def on_press(self, key) -> None:
        mode = self._key_to_mode(key)
        if mode is None or self.active_mode is not None:
            return
        self.active_mode = mode
        self._start_recording()

    def on_release(self, key) -> None:
        mode = self._key_to_mode(key)
        if mode is None or mode != self.active_mode:
            return
        self.active_mode = None
        self._stop_and_process(mode)

    def _start_recording(self) -> None:
        ok = self.recorder.start()
        if not ok:
            _beep(300, 200, self.cfg.get("sounds_enabled", True))
            return
        self.recording_started_at = time.time()
        self.tray.set_state("recording")
        _beep(800, 80, self.cfg.get("sounds_enabled", True))

    def _stop_and_process(self, mode: str) -> None:
        duration = time.time() - (self.recording_started_at or time.time())
        audio = self.recorder.stop()
        self.recording_started_at = None

        if audio is None or duration < self.cfg["min_recording_duration"]:
            self.tray.set_state("idle")
            return

        self.tray.set_state("transcribing")
        threading.Thread(
            target=self._pipeline, args=(audio, mode), daemon=True
        ).start()

    def _pipeline(self, audio, mode: str) -> None:
        try:
            raw_text = self.transcriber.transcribe(audio, language=self.cfg["language"])
            if not raw_text:
                _beep(300, 200, self.cfg.get("sounds_enabled", True))
                return

            _safe_print(f"[voice_flow] raw ({mode}): {raw_text}")

            final_text = raw_text
            if mode in ("cleanup", "dev_request"):
                if not self.ai.available:
                    _safe_print("[voice_flow] AI disabled (no GROQ_API_KEY) - pasting raw")
                else:
                    self.tray.set_state("ai")
                    final_text = self.ai.process(raw_text, mode) or raw_text
                    _safe_print(f"[voice_flow] {mode}: {final_text}")

            pyperclip.copy(final_text)
            append_history(final_text, mode, self.cfg)
            time.sleep(0.08)
            self._send_paste(final_text)
            _beep(1200, 60, self.cfg.get("sounds_enabled", True))
        except Exception as e:
            _safe_print(f"[voice_flow] pipeline error: {e}")
            _beep(300, 200, self.cfg.get("sounds_enabled", True))
        finally:
            self.tray.set_state("idle")

    def _send_paste(self, text: str) -> None:
        try:
            kb_lib.send("ctrl+v")
        except Exception as e:
            _safe_print(f"[voice_flow] ctrl+v failed, falling back to typing: {e}")
            try:
                self.kb.type(text)
            except Exception as e2:
                _safe_print(f"[voice_flow] typing fallback also failed: {e2}")

    def run(self) -> None:
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()
        ai_state = "enabled" if self.ai.available else "disabled (no GROQ_API_KEY)"
        print(f"[voice_flow] running. AI: {ai_state}")
        print("  Right Ctrl  = raw")
        print("  Right Alt   = cleanup")
        print("  Right Shift = dev-request")
        self.tray.run()


def main() -> None:
    app = VoiceFlowApp()
    app.run()


if __name__ == "__main__":
    main()

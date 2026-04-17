# Hebrew Voice Flow — Project Context

Free, open-source Windows voice dictation for Hebrew with English code-switching. Published as public GitHub repo under MIT.

## About
Built in a single session by Meir Arad + Claude Code (2026-04-17) as a free alternative to Wispr Flow (which doesn't support Hebrew well).

**Repo:** https://github.com/Meir770ar/hebrew-voice-flow
**Local path:** `C:\tools\voice-flow\`
**Demo assets:** `C:\tools\voice-flow-demo\` (outside repo, not checked in)

## Architecture
```
voice_flow.py       ← main: hotkey listener + tray + dispatch
├── recorder.py     ← sounddevice microphone capture
├── transcriber.py  ← faster-whisper medium, auto-unload after 60s idle
└── ai_cleaner.py   ← Groq Llama 3.3 70B (optional), 3 modes
```

**Paste mechanism:** `pyperclip.copy()` + `keyboard.send('ctrl+v')` via the `keyboard` library (NOT `pynput.type()` — that broke in VSCode with Hebrew characters).

## Hotkeys
- `Right Ctrl` — raw Whisper transcription (always available)
- `Right Alt` — + Groq gentle cleanup (AI mode only)
- `Right Shift` — + Groq dev-request rewrite for Claude Code prompts (AI mode only)

## Critical implementation gotchas
1. **Windows console encoding** — `sys.stdout.reconfigure(encoding="utf-8")` at startup. Without it, any `print(hebrew_text)` crashes with `'charmap' codec can't encode`. This broke paste in early iterations.
2. **pynput vs keyboard lib for paste** — pynput's `Controller.type()` scrambles Hebrew chars in VSCode/Monaco. `keyboard.send('ctrl+v')` is the working method.
3. **faster-whisper model format** — different from openai-whisper. `medium.pt` in `~/.cache/whisper/` is NOT reused. faster-whisper downloads CT2 format to `~/.cache/huggingface/hub/models--Systran--faster-whisper-medium`.
4. **Right Shift + Filter Keys** — holding Right Shift for 8s triggers Windows Filter Keys accessibility prompt. Users must disable this in Settings → Accessibility → Keyboard.
5. **GPU VRAM** — on 4GB GPUs (like Quadro T1000), `medium` with `int8_float16` = ~1.5GB. Auto-unload after 60s idle frees VRAM for other GPU work (Remotion renders etc.).

## Two install modes
- `setup.bat` asks: local only (no groq) vs with-ai (with groq+dotenv). Single codebase, different requirements files. `requirements.txt` is minimal; `requirements-ai.txt` adds groq.
- `install.bat` (top-level, also in v0.1.0 release assets) is the one-click installer — checks Python via winget, clones repo, runs setup, creates desktop shortcut.

## Secrets
- GROQ_API_KEY is loaded via `python-dotenv` from `.env` in the project folder.
- `.env` is gitignored.
- Users get their own free key at https://console.groq.com/keys (14,400 req/day free tier).
- Never embed API keys or tokens in the codebase — even in bat files.

## Dev loop
- Edit files → kill running instance via tray icon (Quit) → `python voice_flow.py` from shell to see logs.
- `run-debug.bat` = foreground with console. `run.bat` = `pythonw` silent.
- History at `history.json` (gitignored) shows last 50 transcriptions with their mode.

## When adding features
- New hotkey → update `_key_to_mode()` in voice_flow.py AND `HOTKEY_TO_MODE` dict
- New AI mode → add prompt to `PROMPTS` dict in ai_cleaner.py, add hotkey mapping in voice_flow.py
- Config changes → add to `DEFAULT_CONFIG` dict in voice_flow.py (defaults merge with user config.json)

## Demo video
- Source: `C:\mehubarim-upgrade\remotion\src\HebrewVoiceFlowDemo.tsx` (part of mehubarim remotion project, composition ID `HebrewVoiceFlowDemo`)
- Render: `cd mehubarim-upgrade && npx remotion render remotion/src/index.ts HebrewVoiceFlowDemo ./out.mp4 --public-dir="remotion/public"`
- Audio: `remotion/public/voice-flow/` (bgm-tech, keyclick, typing, ding, whoosh)
- Release assets hosted at github.com/Meir770ar/hebrew-voice-flow/releases/tag/v0.1.0

## Testing paste in problem apps
If a user reports paste doesn't work in some app, the fallback chain is:
1. `keyboard.send('ctrl+v')` (primary)
2. `pynput.type(text)` char-by-char (fallback — may scramble Hebrew)

Clipboard is always populated via `pyperclip.copy()`, so manual Ctrl+V always works.

## Not done / future
- Windows auto-start installer option (currently manual via startup folder shortcut)
- Per-app hotkey overrides
- Custom vocabulary / user dictionary for technical jargon
- Whisper large-v3 support (requires 3GB VRAM)
- Localization of tray menu

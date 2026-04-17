# Changelog

All notable changes to Hebrew Voice Flow will be documented in this file.

## [0.1.0] - 2026-04-17

Initial release.

### Features
- Push-to-talk voice dictation for Windows
- System-wide text injection via clipboard + Ctrl+V
- Hebrew + English code-switching support
- Local Whisper transcription (faster-whisper)
- Auto-unload model after idle to free VRAM
- System tray icon with state indicator
- Configurable hotkeys and sounds
- Local history with toggle

### AI mode
- Groq-powered text cleanup (Llama 3.3 70B)
- Three modes: raw / cleanup / dev-request
- Anti-hallucination prompt for dev-request mode
- Optional, disabled by default

### Setup
- Interactive `setup.bat` for one-click install
- Separate dependency sets for local vs AI mode

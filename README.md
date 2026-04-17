# Hebrew Voice Flow

Free, private, system-wide voice dictation for Windows — in Hebrew (with mixed English technical terms).

Hold a key, speak, release — text appears at your cursor. Works in any app: WhatsApp Web, Gmail, VSCode, Notepad, Chrome, Telegram, everywhere.

> דיקטציה קולית חינמית ופרטית בעברית עבור Windows. תומכת במונחים טכניים באנגלית. עובדת בכל אפליקציה.

---

## Features

- **Local transcription** with [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — private, free, offline-capable
- **Hebrew + English code-switching** — perfect for developers ("commit the API changes")
- **Push-to-talk** — hold a key, speak, release
- **Two versions, one codebase:**
  - **Local only** — Whisper transcription, nothing leaves your machine
  - **With AI** — adds optional Groq-powered text refinement (free tier)
- **Works everywhere** — uses clipboard + Ctrl+V, no browser extensions, no app-specific integration
- **System tray icon** — always running, minimal footprint

---

## Requirements

### System
- **OS:** Windows 10 or Windows 11 (x64)
- **Python:** 3.11 or newer
- **Node.js:** not required
- **Internet:** only required for AI mode (local mode is fully offline after install)

### Hardware
- **CPU:** any modern x64 CPU (4+ cores recommended)
- **RAM:** 4 GB free minimum, 8 GB recommended
- **GPU (optional but recommended):** NVIDIA with CUDA support, 2 GB+ VRAM
  - With GPU: transcription in ~1 second
  - Without GPU (CPU only): transcription in 3–5 seconds
- **Microphone:** any working input device
- **Disk space:** ~2 GB for Whisper medium model (downloaded on first run)

### AI mode only
- Free [Groq API key](https://console.groq.com/keys) (the free tier is generous — 14,400 requests/day)

---

## Quick Start

```bash
git clone https://github.com/Meir770ar/hebrew-voice-flow.git
cd hebrew-voice-flow
setup.bat
```

The setup script will:
1. Check Python is installed
2. Ask which version to install (Local / AI)
3. Install dependencies
4. (AI mode only) Ask for your Groq API key and save it to `.env`

After setup:
```bash
run.bat
```

A green circle appears in your system tray. You are ready to dictate.

---

## Usage

### Hotkeys

| Key | Mode | What it does |
|---|---|---|
| **Right Ctrl** | Raw | Hold, speak, release → transcription appears at cursor |
| **Right Alt** | Cleanup *(AI mode only)* | Adds punctuation, removes fillers ("uh", "um"), preserves your casual tone |
| **Right Shift** | Dev-request *(AI mode only)* | Rewrites casual speech into a clear technical request for AI coding assistants (Claude Code, Cursor, Copilot) |

In local-only mode, only Right Ctrl is active.

### Example

**You say (raw speech, Hebrew):**
> *"אה, אז... אני רוצה להוסיף כפתור דארק מוד לדף הבית, אתה יודע, בפינה למעלה, ושיישמר לפעם הבאה"*

**Raw (Right Ctrl):**
> "אז אני רוצה להוסיף כפתור דארק מוד לדף הבית בפינה למעלה ושיישמר לפעם הבאה"

**Cleanup (Right Alt):**
> "אני רוצה להוסיף כפתור דארק מוד לדף הבית, בפינה למעלה, ושיישמר לפעם הבאה."

**Dev-request (Right Shift):**
> "הוסף כפתור Dark Mode בפינה הימנית העליונה של דף הבית. שמור את ההעדפה כך שתישמר בין sessions."

---

## First run

The first time you press Right Ctrl, the Whisper `medium` model (~1.5 GB) downloads automatically and loads to your GPU/CPU. This takes 30–60 seconds. **Subsequent uses take ~1 second.**

---

## Configuration

Edit `config.json`:

```json
{
  "model": "medium",                    // tiny | base | small | medium | large-v3
  "language": "he",                     // he | en | auto
  "sounds_enabled": true,
  "history_enabled": true,
  "max_history": 50,
  "idle_timeout": 60,                   // seconds before model unloads from VRAM
  "groq_model": "llama-3.3-70b-versatile"
}
```

**Tip:** use `small` for 2 GB VRAM systems, `medium` for 4 GB, `large-v3` for 6 GB+.

---

## Privacy

- **Local mode:** audio and text never leave your computer. Whisper runs on your GPU/CPU.
- **AI mode:** audio still stays local. Only the transcribed text is sent to Groq for refinement. Groq does not train on your data — see their [privacy policy](https://groq.com/privacy-policy).

No telemetry. No analytics. No cloud storage.

---

## Documentation

- [Installation guide](docs/installation.md) — step-by-step, including CUDA setup
- [Troubleshooting](docs/troubleshooting.md) — common issues and fixes
- [Changelog](CHANGELOG.md)

---

## Why?

[Wispr Flow](https://wisprflow.ai/) is an excellent commercial dictation app, but it is paid and proprietary. Hebrew speakers have limited options for system-wide Hebrew dictation that works in every app. This project is a fully free, open-source alternative that:

1. Runs locally by default (privacy)
2. Handles Hebrew + English code-switching natively (great for developers)
3. Optionally adds AI text refinement via Groq's free tier
4. Works in every Windows app via clipboard + Ctrl+V

---

## Contributing

Issues and pull requests welcome. Please check [existing issues](https://github.com/Meir770ar/hebrew-voice-flow/issues) first.

---

## License

[MIT](LICENSE)

---

## Credits

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — optimized Whisper inference
- [OpenAI Whisper](https://github.com/openai/whisper) — the underlying model
- [Groq](https://groq.com) — fast LLM inference (AI mode)

---

<div dir="rtl">

## בעברית

Hebrew Voice Flow הוא כלי חינמי ופתוח להכתבה קולית בעברית במערכת Windows.

### איך זה עובד?
לוחץ והחזק את `Right Ctrl`, מדבר, משחרר. הטקסט מופיע במקום שהסמן נמצא — בכל אפליקציה.

### התקנה
1. `git clone https://github.com/Meir770ar/hebrew-voice-flow.git`
2. `cd hebrew-voice-flow`
3. הרץ `setup.bat` ובחר גרסה (Local או AI)
4. הרץ `run.bat` להפעלה

### דרישות
- Windows 10/11
- Python 3.11+
- GPU עם CUDA (מומלץ, 2GB VRAM לפחות) — אחרת רץ על CPU
- 4GB RAM פנוי

### מצבים
- **Right Ctrl** — תמלול גלם (בלי שינויים)
- **Right Alt** — תמלול + ניסוח קליל (AI)
- **Right Shift** — תמלול + בקשת פיתוח ל-Claude Code (AI)

לפרטים נוספים: [docs/installation.md](docs/installation.md)

</div>

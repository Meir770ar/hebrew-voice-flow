# Installation Guide

## Prerequisites

### 1. Python 3.11+
Download from https://python.org and install. Make sure "Add Python to PATH" is checked.

Verify:
```bash
python --version
```

### 2. CUDA (GPU users — strongly recommended)
If you have an NVIDIA GPU, install the CUDA toolkit for much faster transcription:
- Go to https://developer.nvidia.com/cuda-downloads
- Choose Windows → x86_64 → your version → exe (local)
- Install with default options

Verify:
```bash
nvidia-smi
```

Without CUDA, the app falls back to CPU transcription (3–5 seconds instead of ~1 second).

### 3. Microphone
Ensure your microphone works in the Windows Sound settings.

---

## Install Steps

### Step 1: Clone
```bash
git clone https://github.com/Meir770ar/hebrew-voice-flow.git
cd hebrew-voice-flow
```

### Step 2: Run setup
```bash
setup.bat
```

You will be asked to pick a version:

**[1] Local only**
- Whisper transcription on your machine
- No internet needed (after install + first model download)
- No AI cleanup
- Only `Right Ctrl` hotkey is active

**[2] With AI**
- Everything from Local, plus
- Groq-powered text refinement
- `Right Alt` for cleanup, `Right Shift` for dev-request rewrite
- Requires a free Groq API key

### Step 3: (AI mode) Get a Groq API key
1. Go to https://console.groq.com/keys
2. Sign in (Google/GitHub account works)
3. Click "Create API Key"
4. Copy the key (starts with `gsk_...`)
5. Paste it when setup asks

The key is saved to `.env` which is gitignored.

### Step 4: Run
```bash
run.bat
```

A green circle will appear in your system tray (look for it near the clock — you might need to click the "Show hidden icons" arrow).

---

## Disable Windows Filter Keys (important)

Holding `Right Shift` for 8 seconds triggers Windows' Filter Keys accessibility feature. Disable it:

1. Open Settings → Accessibility → Keyboard
2. Turn off "Filter keys"
3. Also turn off the shortcut: "Keyboard shortcut for Filter keys"

Same for Sticky Keys (5 Shift presses trigger it):
1. Turn off "Sticky keys" and its shortcut

---

## First-time model download

The first time you press `Right Ctrl`, the Whisper `medium` model (~1.5 GB) will download. This takes 30–60 seconds depending on your connection. All subsequent uses are instant.

Model location: `%USERPROFILE%\.cache\huggingface\hub\models--Systran--faster-whisper-medium`

---

## Auto-start on Windows boot (optional)

1. Press `Win+R`
2. Type `shell:startup` and press Enter
3. Create a shortcut to `run.bat` in the folder that opens

Voice Flow will start silently each time you log in.

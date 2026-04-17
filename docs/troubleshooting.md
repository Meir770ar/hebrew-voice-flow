# Troubleshooting

## "No icon appears in the system tray"
Look for the **"Show hidden icons"** arrow (^) near the clock. The icon may be hidden there. Drag it out to pin it.

## "I hear beeps but no text appears"
Check `history.json` in the app folder. If transcriptions appear there, the issue is paste injection, not transcription.
- Try in **Notepad** first — if it works there but not in your target app, the app is blocking programmatic Ctrl+V. Workaround: paste manually (Ctrl+V) after the completion beep.
- VSCode, Chrome, Electron apps should work.

## "No sound when I press the hotkey"
- Check that Voice Flow is running (green icon in tray).
- Check that `sounds_enabled` is `true` in `config.json`.
- Some laptops mute system beeps via a driver setting.

## "Transcription is garbled / wrong language"
- Make sure `"language": "he"` in `config.json` for Hebrew.
- For mixed Hebrew/English, keep `"language": "he"` — Whisper handles code-switching well.
- Use the `medium` model or larger for best Hebrew quality (`small` and below struggle).

## "Out of memory / CUDA out of memory"
- Your GPU doesn't have enough VRAM. Change `"model"` in `config.json` to a smaller size:
  - `large-v3` → 3 GB VRAM
  - `medium` → 1.5 GB VRAM (default)
  - `small` → 500 MB VRAM
  - `base` → 200 MB VRAM

## "Windows asks about Filter Keys / Sticky Keys when I hold Right Shift"
Disable these accessibility shortcuts:
1. Settings → Accessibility → Keyboard
2. Turn off "Filter keys" and "Sticky keys" and their keyboard shortcuts

## "Transcription is slow (5+ seconds)"
- You are running on CPU. Install CUDA and a matching PyTorch build to use your NVIDIA GPU.
- `nvidia-smi` should show your GPU — if not, CUDA is not installed properly.

## "AI mode says 'no GROQ_API_KEY'"
- Check that `.env` exists in the app folder with `GROQ_API_KEY=gsk_...`.
- Or set the environment variable manually: `setx GROQ_API_KEY gsk_yourkey`.
- Restart the app after changing.

## "ImportError: No module named 'groq'"
You installed local-only mode but are trying to use AI features. Re-run `setup.bat` and choose option 2, or manually:
```bash
pip install groq python-dotenv
```

## "pyperclip / keyboard permission denied"
On some corporate/managed Windows machines, keyboard hook access is blocked. Run Voice Flow as Administrator.

## "Ctrl+V doesn't trigger in some apps (games, remote desktop)"
Apps with anti-cheat or custom input handling may block synthetic Ctrl+V. The text is still copied to clipboard — you can paste manually.

## "Hotkey conflicts with another app"
Edit `config.json` to change the hotkey bindings. Supported values: `ctrl_r`, `ctrl_l`, `alt_r`, `alt_l`, `shift_r`, `shift_l`, `f9`, `f10`, etc.

---

## Still stuck?
Open an issue: https://github.com/Meir770ar/hebrew-voice-flow/issues

Include:
- Windows version (`winver`)
- Python version (`python --version`)
- GPU info (`nvidia-smi`)
- Contents of `history.json` (last few entries)
- Any error messages from `run-debug.bat`

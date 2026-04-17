# Getting a free Groq API key

Groq offers a generous free tier (14,400 requests/day) — more than enough for personal voice dictation.

## Steps

### 1. Go to the Groq Console
https://console.groq.com/keys

### 2. Sign in
Click **"Sign in"** (top right).
You can use:
- Google account (fastest)
- GitHub account
- Email + password

No credit card required.

### 3. Create a new API key
Once logged in:
1. You will see the **API Keys** page
2. Click the **"Create API Key"** button
3. Give the key a name (e.g. `voice-flow`) — this is just for your reference
4. Click **"Submit"**

### 4. Copy the key immediately
A popup will show your new key. It looks like:
```
gsk_abc123xyz456...
```

**Important:** Copy it now. For security reasons, you won't be able to see the full key again after closing this popup.

### 5. Paste it in the installer
When the installer asks for your API key, paste what you copied. It will be saved locally in a `.env` file in the project folder.

---

## Security

- Your key is stored **only on your machine** in `C:\Users\<you>\hebrew-voice-flow\.env`
- The `.env` file is in `.gitignore` — it will never be committed or uploaded anywhere
- Only you and applications running on your machine can read it
- You can delete the key anytime at https://console.groq.com/keys

## Usage limits

Groq's free tier (as of 2026):
- 14,400 requests per day
- 500,000 tokens per day for Llama 3.3 70B
- No billing, no credit card

For perspective: 14,400 voice dictations per day = one every 6 seconds for 24 hours straight. You will never hit this limit in normal use.

## If you lose the key

Go back to https://console.groq.com/keys, delete the old key, and create a new one. Then re-run the installer or edit `.env` manually.

## Troubleshooting

### "Invalid API key" error
- Make sure you copied the **entire** key (they start with `gsk_`)
- Check for extra spaces or line breaks
- The key should be on a single line in `.env`

### Want to disable AI mode later?
- Delete the `.env` file
- Or leave it empty
- The app will fall back to raw transcription (no AI cleanup)

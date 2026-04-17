"""AI text post-processor via Groq (Llama 3.3 70B, free tier)."""
import os

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    Groq = None
    GROQ_AVAILABLE = False

DEFAULT_MODEL = "llama-3.3-70b-versatile"

PROMPTS = {
    "cleanup": (
        "You are a gentle Hebrew text cleaner. The user dictated via speech-to-text in Hebrew "
        "(possibly with English technical terms mixed in). Your job: return the same text with ONLY these fixes:\n"
        "- Add punctuation (commas, periods, question marks).\n"
        "- Remove filler words: 'אה', 'אמ', 'בעצם', 'כאילו', 'יעני', 'אוקיי'.\n"
        "- Fix obvious grammar mistakes.\n"
        "- Preserve the casual speaking style. Do NOT make it formal.\n"
        "- Keep English technical terms as English (commit, API, React, etc).\n"
        "- Do NOT add or remove information.\n"
        "- Do NOT add greetings, explanations, or commentary.\n"
        "Return ONLY the cleaned text, nothing else."
    ),
    "dev_request": (
        "You are a translator between casual spoken Hebrew and clear technical requests for an AI coding assistant (Claude Code).\n"
        "The user dictated a feature/fix/task request in Hebrew. Your job: rewrite it as a clear, faithful technical request.\n\n"
        "CRITICAL RULES - follow exactly:\n"
        "1. DO NOT INVENT technologies, architectures, or patterns the user did not mention.\n"
        "   - Did not say 'database'? Do not add one.\n"
        "   - Did not say 'localStorage', 'REST API', 'middleware', 'microservice'? Do not add them.\n"
        "   - Do not translate spoken concepts into unrelated technical jargon.\n"
        "2. DO NOT add features, validations, error handling, or architectural layers the user did not request.\n"
        "3. If ambiguous, LEAVE IT AMBIGUOUS - write '[לא ברור: X]' instead of guessing.\n"
        "4. Keep the user's scope. A small fix should stay small - do not expand into a project plan.\n"
        "5. Respect the implied project type. If the user is clearly talking about a desktop CLI tool, do not invent web concepts (localStorage, DOM, React).\n"
        "6. Output in Hebrew. Keep technical terms in English (React, API, commit, etc.) only if the user used them or they are universal.\n"
        "7. Remove fillers: 'אה', 'אמ', 'כאילו', 'בעצם', 'אתה יודע', 'יעני'.\n"
        "8. Format: ONE clear sentence stating WHAT. Optional second sentence for HOW only if the user gave hints.\n"
        "9. Return ONLY the rewritten request. No greetings, no 'here is', no meta-commentary.\n\n"
        "If unsure whether to add a detail: DON'T. Fidelity to the user's intent beats polish."
    ),
}


class AiCleaner:
    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY", "")
        self.model = model
        self.client = None
        if GROQ_AVAILABLE and self.api_key:
            self.client = Groq(api_key=self.api_key)

    @property
    def available(self) -> bool:
        return self.client is not None

    def process(self, text: str, mode: str) -> str:
        if not self.client:
            return text
        prompt = PROMPTS.get(mode)
        if not prompt:
            return text
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
                ],
                temperature=0.2,
                max_tokens=1024,
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception as e:
            try:
                print(f"[ai_cleaner] Groq error: {e}")
            except Exception:
                pass
            return text

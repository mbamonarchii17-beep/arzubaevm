import os
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ── CORS ─────────────────────────────────────────────────────────────────────
ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    # Deploy qilgandan keyin GitHub Pages domeningizni qo'shing:
    # "https://mbamonarchii17-beep.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/")
def health():
    return {"status": "ok", "message": "MoodTune backend ishlayapti 🔥"}

# ── /api/chat  →  Anthropic API ───────────────────────────────────────────────
@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()

    messages   = body.get("messages")
    system     = body.get("system", "")
    max_tokens = body.get("max_tokens", 2000)

    if not messages or not isinstance(messages, list):
        return JSONResponse({"error": "messages maydoni kerak"}, status_code=400)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return JSONResponse({"error": "Server: ANTHROPIC_API_KEY sozlanmagan"}, status_code=500)

    payload = {
        "model":      "claude-sonnet-4-6",
        "max_tokens": max_tokens,
        "system":     system,
        "messages":   messages,
    }

    headers = {
        "Content-Type":      "application/json",
        "x-api-key":         api_key,
        "anthropic-version": "2023-06-01",
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            json=payload,
            headers=headers,
        )

    if resp.status_code != 200:
        return JSONResponse(resp.json(), status_code=resp.status_code)

    return JSONResponse(resp.json())

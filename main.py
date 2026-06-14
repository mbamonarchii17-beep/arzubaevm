import os
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="MoodTune API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # keyin domeningizni qo'ying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "MoodTune backend ishlayapti 🔥"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/chat")
async def chat(request: Request):
    try:
        body = await request.json()

        messages = body.get("messages", [])
        system = body.get("system", "")
        max_tokens = body.get("max_tokens", 2000)

        if not messages:
            return JSONResponse(
                status_code=400,
                content={"error": "messages maydoni bo'sh"}
            )

        if not ANTHROPIC_API_KEY:
            return JSONResponse(
                status_code=500,
                content={"error": "ANTHROPIC_API_KEY topilmadi"}
            )

        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages
        }

        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                json=payload,
                headers=headers
            )

        try:
            result = response.json()
        except Exception:
            result = {"error": response.text}

        return JSONResponse(
            status_code=response.status_code,
            content=result
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

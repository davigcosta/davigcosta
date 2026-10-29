import os
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langdetect import detect

app = FastAPI(title="Aurora Robot Assistant")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str
    language: str | None = None

async def cloud_response(message: str, language: str):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    payload = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [
            {"role": "system", "content": "You are Aurora, an original sweet, funny, multilingual robot assistant. Reply in the requested language. Be concise and helpful."},
            {"role": "user", "content": f"Requested language: {language}\n{message}"},
        ],
        "temperature": 0.7,
    }
    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except Exception:
        return None

async def ollama_response(message: str, language: str):
    try:
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                os.getenv("OLLAMA_URL", "http://localhost:11434") + "/api/chat",
                json={"model": os.getenv("OLLAMA_MODEL", "llama3.2"), "stream": False, "messages": [
                    {"role": "system", "content": f"Reply in {language}. Be sweet, funny, and useful."},
                    {"role": "user", "content": message},
                ]},
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
    except Exception:
        return None

@app.get("/health")
async def health():
    return {"ok": True, "cloud_configured": bool(os.getenv("OPENAI_API_KEY"))}

@app.post("/chat")
async def chat(request: ChatRequest):
    language = request.language or detect(request.message)
    text = await cloud_response(request.message, language)
    provider = "cloud"
    if not text:
        text = await ollama_response(request.message, language)
        provider = "ollama"
    if not text:
        text = "Please configure a cloud API key or start Ollama."
        provider = "offline"
    return {"text": text, "language": language, "provider": provider}

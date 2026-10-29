# Aurora Robot Assistant MVP

A cross-platform Godot 4 3D robot assistant with multilingual chat and hybrid AI routing.

## Features
- Original cute 3D robot generated at runtime.
- Godot 4 client foundation for Android, iOS, Web, Windows, and Linux exports.
- FastAPI backend with cloud-first AI and Ollama fallback.
- Automatic language detection with an optional language override.
- API keys stay on the backend and are never shipped in the client.

## Run the backend

```bash
cd backend
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Set `OPENAI_API_KEY` for cloud mode. For local fallback, start Ollama and set `OLLAMA_MODEL`.

## Run the client

Open `client/project.godot` in Godot 4.3+ and press Run. The default backend URL is `http://127.0.0.1:8000`.

The assistant uses an original personality and assets; it does not copy JARVIS or Iron Man protected assets or voice.

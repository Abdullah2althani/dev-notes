# dev-notes/backend

Quick notes for running the FastAPI backend.

## Prerequisites
- Python 3.8+
- pip

## Setup
```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
pip install fastapi uvicorn
```

## Run (development)
From this folder (`dev-notes/backend`) run:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

What the command means:
- `uvicorn` — ASGI server that runs the FastAPI app.
- `main:app` — import `app` from `main.py`.
- `--reload` — auto-restart on code changes (development only).
- `--host 127.0.0.1` — bind to localhost.
- `--port 8000` — listen on port 8000.

## Endpoints
- GET  /notes         — list notes
- POST /notes         — create note (send JSON matching Note model)
- DELETE /notes/{id}  — delete note by id
- PUT /notes/{id}     — update note by id

## Quick test
```bash
curl http://127.0.0.1:8000/notes
```

## References
- FastAPI docs: https://fastapi.tiangolo.com/
- Uvicorn
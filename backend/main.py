import os
import requests
import json

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

# Initialize FastAPI
app = FastAPI()

# Allow Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Notes file
NOTES_FILE = "notes.json"

def load_notes():

    try:

        with open(NOTES_FILE, "r") as file:
            return json.load(file)

    except:
        return []


def save_notes(notes_data):

    with open(NOTES_FILE, "w") as file:
        json.dump(notes_data, file, indent=2)


notes = load_notes()

# Note schema
class Note(BaseModel):
    id: int
    text: str


# GET all notes
@app.get("/notes")
def get_notes():
    return notes


# CREATE note
@app.post("/notes")
def create_note(note: Note):

    notes.append(note.dict())

    save_notes(notes)

    return note


# DELETE note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):

    global notes

    notes = [
        note for note in notes
        if note["id"] != note_id
    ]

    save_notes(notes)

    return {
        "message": "Note deleted"
    }

# UPDATE note
@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: Note):

    for index, note in enumerate(notes):

        if note["id"] == note_id:

            notes[index] = updated_note.dict()

            save_notes(notes)

            return updated_note

# // Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

#  Summarize notes
@app.post("/summarize")
def summarize_notes():

    notes_text = "\n".join([
        note["text"] for note in notes
    ])

    prompt = f"""
    Summarize these notes:

    {notes_text}

    Give:
    - short summary
    - key ideas
    - action items
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization":
            f"Bearer {OPENROUTER_API_KEY}",

            "Content-Type":
            "application/json",
        },
        json={
            "model": "openai/gpt-4o-mini",

            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        },
    )

    data = response.json()

    print(data)


    if "choices" not in data:
        return {
            "error": data
        }

    return {
        "result":
        data["choices"][0]["message"]["content"]
    }

class QuestionRequest(BaseModel):
    question: str


# Ask AI
@app.post("/ask-ai")
def ask_ai(request: QuestionRequest):

    notes_text = "\n".join([
        note["text"] for note in notes
    ])

    prompt = f"""
    Here are the user's notes:

    {notes_text}

    User question:
    {request.question}
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization":
            f"Bearer {OPENROUTER_API_KEY}",

            "Content-Type":
            "application/json",
        },
        json={
            "model": "openai/gpt-4o-mini",

            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        },
    )

    data = response.json()

    return {
        "result":
        data["choices"][0]["message"]["content"]
    }

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

# Ask AI Stream
@app.post("/ask-stream")
async def ask_stream(data: dict):

    question = data.get("question", "")

    notes_data = data.get("notes", [])

    notes_text = "\n".join([
        note["text"] for note in notes_data
    ])

    prompt = f"""
    Here are the user's notes:

    {notes_text}

    User question:
    {question}
    """

    def generate():

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json={
                "model": "deepseek/deepseek-chat-v3-0324:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():

            if line:

                decoded = line.decode("utf-8")

                if decoded.startswith("data: "):

                    chunk = decoded.replace("data: ", "")

                    if chunk == "[DONE]":
                        break

                    try:

                        json_data = json.loads(chunk)

                        content = (
                            json_data["choices"][0]["delta"]
                            .get("content", "")
                        )

                        if content:
                            yield content

                    except:
                        pass

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )

import os
import requests

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Fake database
notes = []

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
    notes.append(note)

    return note


# DELETE note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    global notes

    notes = [
        note for note in notes
        if note.id != note_id
    ]

    return {
        "message": "Note deleted"
    }


# UPDATE note
@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: Note):

    for index, note in enumerate(notes):

        if note.id == note_id:
            notes[index] = updated_note

            return updated_note

    return {
        "message": "Note not found"
    }

# // Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

#  Summarize notes
@app.post("/summarize")
def summarize_notes():

    notes_text = "\n".join([
        note.text for note in notes
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

    return {
        "result":
        data["choices"][0]["message"]["content"]
    }

class QuestionRequest(BaseModel):
    question: str


@app.post("/ask-ai")
def ask_ai(request: QuestionRequest):

    notes_text = "\n".join([
        note.text for note in notes
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
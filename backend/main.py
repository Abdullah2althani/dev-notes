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

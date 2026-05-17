import { Injectable, computed, inject, signal } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Note } from "../models/note";

@Injectable({
  providedIn: "root",
})
export class NotesService {
  // HTTP client
  http = inject(HttpClient);

  // Backend API URL
  apiUrl = "http://127.0.0.1:8000/notes";

  // Main notes state
  notes = signal<Note[]>([]);

  // Edit state
  editingNoteId = signal<number | null>(null);

  // Search state
  searchTerm = signal("");

  // Edit text state
  editingText = signal("");

  // Total notes count
  totalNotes = computed(() => this.notes().length);

  // Filtered notes
  filteredNotes = computed(() => {
    const term = this.searchTerm().toLowerCase();

    return this.notes().filter((note) => note.text.toLowerCase().includes(term));
  });

  // // CREATE local
  // addNote(text: string) {
  //   const trimmed = text.trim();

  //   if (!trimmed) return;

  //   const newNote: Note = {
  //     id: Date.now(),
  //     text: trimmed,
  //   };

  //   // Add the new note to the state
  //   this.notes.update((notes) => [...notes, newNote]);

  //   this.saveNotes();
  // }

  // ADD NOTE
  addNote(text: string) {
    const trimmed = text.trim();

    if (!trimmed) return;

    const newNote: Note = {
      id: Date.now(),
      text: trimmed,
    };

    // Create the note on the server
    this.http.post<Note>(this.apiUrl, newNote).subscribe((createdNote) => {
      this.notes.update((notes) => [...notes, createdNote]);
    });
  }

  // // DELETE local
  // deleteNote(id: number) {
  //   this.notes.update((notes) => notes.filter((note) => note.id !== id));

  //   this.saveNotes();
  // }

  // DELETE
  deleteNote(id: number) {
    // Delete the note on the server
    this.http.delete(`${this.apiUrl}/${id}`).subscribe(() => {
      this.notes.update((notes) => notes.filter((note) => note.id !== id));
    });
  }

  // START EDITING
  startEditing(note: Note) {
    this.editingNoteId.set(note.id);

    this.editingText.set(note.text);
  }

  // // UPDATE local
  // saveEdit() {
  //   const id = this.editingNoteId();

  //   if (id === null) return;

  //   this.notes.update((notes) =>
  //     notes.map((note) =>
  //       note.id === id
  //         ? {
  //             ...note,
  //             text: this.editingText(),
  //           }
  //         : note,
  //     ),
  //   );

  //   // Clear edit states
  //   this.editingNoteId.set(null);

  //   // Clear editing text
  //   this.editingText.set("");

  //   this.saveNotes();
  // }

  saveEdit() {
    const id = this.editingNoteId();

    if (id === null) return;

    const updatedNote: Note = {
      id,
      text: this.editingText(),
    };

    // Update the note on the server
    this.http.put<Note>(`${this.apiUrl}/${id}`, updatedNote).subscribe((savedNote) => {
      this.notes.update((notes) => notes.map((note) => (note.id === id ? savedNote : note)));

      this.editingNoteId.set(null);

      this.editingText.set("");
    });
  }

  // CANCEL EDIT
  cancelEdit() {
    this.editingNoteId.set(null);

    this.editingText.set("");
  }

  // SAVE TO LOCAL STORAGE
  saveNotes() {
    localStorage.setItem("notes", JSON.stringify(this.notes()));
  }

  // // LOAD FROM LOCAL STORAGE
  // loadNotes() {
  //   const stored = localStorage.getItem("notes");

  //   // Check if there are any stored notes
  //   if (!stored) return;

  //   // Parse and set the notes
  //   this.notes.set(JSON.parse(stored));
  // }

  // LOAD NOTES FROM FASTAPI
  loadNotes() {
    this.http.get<Note[]>(this.apiUrl).subscribe((notes) => {
      this.notes.set(notes);
    });
  }
}

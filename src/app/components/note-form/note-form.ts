import { Component, inject, signal } from '@angular/core';
import { NotesService } from '../../services/notes';

@Component({
  selector: 'app-note-form',
  imports: [],
  templateUrl: './note-form.html',
  styleUrl: './note-form.css',
})
export class NoteForm {
  // Signal to hold the current note
  note = signal('');

  // Inject the NotesService
  notesService = inject(NotesService);

  // Method to add a new note
  addNote() {
    // Call the addNote method from the NotesService
    this.notesService.addNote(this.note());

    // Clear the note input
    this.note.set('');
  }
}

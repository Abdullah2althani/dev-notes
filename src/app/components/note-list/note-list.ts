import { Component, inject } from "@angular/core";
import { NotesService } from "../../services/notes";

@Component({
  selector: "app-note-list",
  imports: [],
  templateUrl: "./note-list.html",
  styleUrl: "./note-list.css",
})
export class NoteList {
  // Inject the NotesService
  notesService = inject(NotesService);

  // Load notes on initialization
  constructor() {
    this.notesService.loadNotes();
  }
}

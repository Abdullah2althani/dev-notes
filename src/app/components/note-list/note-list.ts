import { Component, inject } from "@angular/core";
import { NotesService } from "../../services/notes";
import { ElementRef, ViewChild, effect } from "@angular/core";

@Component({
  selector: "app-note-list",
  imports: [],
  templateUrl: "./note-list.html",
  styleUrl: "./note-list.css",
})
export class NoteList {
  notesService = inject(NotesService);

  @ViewChild("chatContainer")
  chatContainer?: ElementRef;

  constructor() {
    effect(() => {
      this.notesService.chatMessages();

      setTimeout(() => {
        const el = this.chatContainer?.nativeElement;

        if (!el) return;

        el.scrollTop = el.scrollHeight;
      });
    });
  }
}

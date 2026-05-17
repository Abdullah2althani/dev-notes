import { Component, signal } from "@angular/core";
import { NoteForm } from "./components/note-form/note-form";
import { NoteList } from "./components/note-list/note-list";

@Component({
  selector: "app-root",
  imports: [NoteForm, NoteList],
  templateUrl: "./app.html",
  styleUrl: "./app.css",
})
export class App {
  protected readonly title = signal("dev-notes");
}

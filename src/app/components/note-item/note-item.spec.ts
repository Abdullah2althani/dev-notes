import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NoteItem } from './note-item';

describe('NoteItem', () => {
  let component: NoteItem;
  let fixture: ComponentFixture<NoteItem>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NoteItem],
    }).compileComponents();

    fixture = TestBed.createComponent(NoteItem);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

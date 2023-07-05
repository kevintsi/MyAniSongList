import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Subject, debounceTime, distinctUntilChanged } from 'rxjs';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.css']
})
export class SearchBarComponent {
  @Input() placeholder: string = "Recherche..."
  @Input() defaultValue?: any
  @Output() searchEvent: EventEmitter<string> = new EventEmitter<string>();
  private searchTermSubject: Subject<string> = new Subject<string>();

  constructor() {
    this.searchTermSubject
      .pipe(
        debounceTime(500),
        distinctUntilChanged()
      ).subscribe((query: string) => this.searchEvent.emit(query))
  }

  get_value(event: Event): string {
    return (event.target as HTMLInputElement).value;
  }

  onSearchInput(searchTerm: string) {
    this.searchTermSubject.next(searchTerm);
  }
}

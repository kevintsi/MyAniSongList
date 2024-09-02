import { Component, EventEmitter, OnDestroy, OnInit, Output } from '@angular/core';
import { Subject, debounceTime, distinctUntilChanged, takeUntil } from 'rxjs';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.css']
})
export class SearchBarComponent implements OnDestroy, OnInit {
  @Output() searchEvent: EventEmitter<string> = new EventEmitter<string>();
  private searchTermSubject: Subject<string> = new Subject<string>();
  private destroy$: Subject<boolean> = new Subject<boolean>()

  constructor() { }

  ngOnInit() {
    this.searchTermSubject
      .pipe(
        debounceTime(500),
        distinctUntilChanged(),
        takeUntil(this.destroy$)
      ).subscribe((query: string) => this.searchEvent.emit(query))
  }

  ngOnDestroy(): void {
    this.destroy$.next(true)
    this.destroy$.unsubscribe()
  }

  getValue(event: Event): string {
    return (event.target as HTMLInputElement).value;
  }

  onSearchInput(searchTerm: string) {
    this.searchTermSubject.next(searchTerm);
  }
}

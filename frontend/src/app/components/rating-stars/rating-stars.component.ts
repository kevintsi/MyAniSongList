import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-rating-stars',
  templateUrl: './rating-stars.component.html',
  styleUrls: ['./rating-stars.component.css']
})
export class RatingStarsComponent {
  @Input() rate!: number
  @Input() isStatic!: boolean
  @Input() type!: string
  @Output() rateChange: EventEmitter<number> = new EventEmitter<number>();
  maxStar: number = 10

  constructor() { }

  getRange(start: number, end: number): number[] {
    return Array.from({ length: end - start + 1 }, (_, index) => start + index);
  }

  toInt(value: number) {
    return Math.round(value)
  }

  onChange(value: string) {
    this.rate = parseInt(value)
    this.rateChange.emit(this.rate)
  }

  getValue(event: Event): string {
    return (event.target as HTMLInputElement).value;
  }

}

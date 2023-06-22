import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-rating-stars',
  templateUrl: './rating-stars.component.html',
  styleUrls: ['./rating-stars.component.css']
})
export class RatingStarsComponent implements OnInit {
  @Input() rate!: number
  @Input() isStatic!: boolean
  @Input() type!: string
  @Output() rateChange: EventEmitter<number> = new EventEmitter<number>();
  maxStar: number = 10

  constructor() { }

  ngOnInit() {
    console.log(this.rate)
  }

  getRange(start: number, end: number): number[] {
    return Array.from({ length: end - start + 1 }, (_, index) => start + index);
  }

  toInt(value: number) {
    return Math.round(value)
  }

  onChange(value: string) {
    console.log(value)
    this.rate = parseInt(value)
    this.rateChange.emit(this.rate)
  }

  getValue(event: Event): string {
    return (event.target as HTMLInputElement).value;
  }

}

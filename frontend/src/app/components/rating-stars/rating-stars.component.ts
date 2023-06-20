import { Component, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-rating-stars',
  templateUrl: './rating-stars.component.html',
  styleUrls: ['./rating-stars.component.css']
})
export class RatingStarsComponent implements OnInit {
  @Input() rate!: number
  @Input() isStatic!: boolean
  @Input() id!: number

  maxStar: number = 10

  constructor() { }

  ngOnInit() {
    console.log(this.rate)
  }

  getRange(start: number, end: number): number[] {
    return Array.from({ length: end - start + 1 }, (_, index) => start + index);
  }

}

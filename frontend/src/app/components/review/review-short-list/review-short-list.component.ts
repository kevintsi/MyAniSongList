import { Component, Input } from '@angular/core';
import { Review } from 'src/app/models/Review';

@Component({
  selector: 'app-review-short-list',
  templateUrl: './review-short-list.component.html',
  styleUrls: ['./review-short-list.component.css']
})
export class ReviewShortListComponent {
  @Input() reviews!: Review[]
}

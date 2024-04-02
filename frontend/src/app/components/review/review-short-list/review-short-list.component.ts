import { Component, Input } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { Review } from 'src/app/models/review.model';

@Component({
  selector: 'app-review-short-list',
  templateUrl: './review-short-list.component.html',
  styleUrls: ['./review-short-list.component.css']
})
export class ReviewShortListComponent {
  @Input() reviews!: Review[]


  constructor(
    private translateService: TranslateService) { }

  trackByReviewId(index: number, review: Review) {
    return review.id;
  }


  getCurrentLang() {
    return this.translateService.currentLang
  }
}

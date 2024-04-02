import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ReviewService } from 'src/app/services/review/review.service';
import { PagedReview } from 'src/app/models/review.model';
import { Subscription, firstValueFrom } from 'rxjs'
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-review-list',
  templateUrl: './review-list.component.html',
  styleUrls: ['./review-list.component.css']
})
export class ReviewListComponent implements OnDestroy, OnInit {
  isLoading = true
  reviews!: PagedReview

  languageSubscription?: Subscription

  currentPage: number = 2;
  pageSize: number = 10;
  totalItems: number = 0;

  constructor(
    private service: ReviewService,
    private route: ActivatedRoute,
    private translateService: TranslateService
  ) { }


  ngOnInit(): void {
    this.fetchData()
    this.languageSubscription = this.translateService.onLangChange.subscribe(() => {
      this.fetchData()
    })
  }


  ngOnDestroy(): void {
    this.languageSubscription?.unsubscribe()
  }

  async fetchData() {
    try {
      this.reviews = await this.fetchReviews()
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  fetchReviews() {
    let id_music = Number(this.route.snapshot.paramMap.get("id_music"))
    return firstValueFrom(this.service.getAllByIdMusic(id_music, this.currentPage, this.pageSize))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }

  getCurrentLang() {
    return this.translateService.currentLang
  }
}

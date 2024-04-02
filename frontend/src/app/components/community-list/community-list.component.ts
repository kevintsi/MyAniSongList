import { Component } from '@angular/core';
import { ReviewService } from 'src/app/services/review/review.service';
import { PagedReview } from 'src/app/models/review.model';
import { Subscription, firstValueFrom } from 'rxjs'
import { Title } from '@angular/platform-browser';
import { TranslateService } from '@ngx-translate/core';
import { getAppTitle } from 'src/app/config/app.config';

@Component({
  selector: 'app-community-list',
  templateUrl: './community-list.component.html',
  styleUrls: ['./community-list.component.css']
})
export class CommunityListComponent {
  isLoading = true
  reviews!: PagedReview


  languageSubscription?: Subscription

  currentPage: number = 1;
  pageSize: number = 10;
  totalItems: number = 0;

  constructor(
    private service: ReviewService,
    private title: Title,
    private translateService: TranslateService

  ) { }

  ngOnInit(): void {
    this.fetchData()
    this.languageSubscription = this.translateService.onLangChange.subscribe(() => {
      this.fetchData()
    })
  }

  async fetchData() {
    try {
      this.reviews = await this.fetchReviews()
      this.title.setTitle(getAppTitle("Communauté"))
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  fetchReviews() {
    return firstValueFrom(this.service.getAll(this.currentPage, this.pageSize))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }


  getCurrentLang() {
    return this.translateService.currentLang
  }
}

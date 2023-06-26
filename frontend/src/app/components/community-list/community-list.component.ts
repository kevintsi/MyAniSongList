import { Component } from '@angular/core';
import { ReviewService } from 'src/app/_services/review.service';
import { PagedReview } from 'src/app/models/Review';
import { firstValueFrom } from 'rxjs'

@Component({
  selector: 'app-community-list',
  templateUrl: './community-list.component.html',
  styleUrls: ['./community-list.component.css']
})
export class CommunityListComponent {
  isLoading = true
  reviews!: PagedReview

  currentPage: number = 1;
  pageSize: number = 10;
  totalItems: number = 0;

  constructor(private service: ReviewService) { }
  ngOnInit(): void {
    this.fetchData()
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
    return firstValueFrom(this.service.getAll(this.currentPage, this.pageSize))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }
}

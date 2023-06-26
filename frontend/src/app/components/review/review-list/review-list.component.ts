import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ReviewService } from 'src/app/_services/review.service';
import { PagedReview } from 'src/app/models/Review';
import { firstValueFrom } from 'rxjs'

@Component({
  selector: 'app-review-list',
  templateUrl: './review-list.component.html',
  styleUrls: ['./review-list.component.css']
})
export class ReviewListComponent {
  isLoading = true
  reviews!: PagedReview

  currentPage: number = 2;
  pageSize: number = 10;
  totalItems: number = 0;

  constructor(private service: ReviewService, private route: ActivatedRoute) { }
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
    let id_music = Number(this.route.snapshot.paramMap.get("id_music"))
    return firstValueFrom(this.service.getAllByIdMusic(id_music, this.currentPage, this.pageSize))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }
}

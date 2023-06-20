import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { AuthService } from 'src/app/_services/auth.service';
import { MusicService } from 'src/app/_services/music.service';
import { ReviewService } from 'src/app/_services/review.service';
import { Music } from 'src/app/models/Music';
import { Review } from 'src/app/models/Review';

@Component({
  selector: 'app-music-detail',
  templateUrl: './music-detail.component.html',
  styleUrls: ['./music-detail.component.css']
})
export class MusicDetailComponent {
  isLoading: boolean = true
  music!: Music
  reviews!: Review[]

  constructor(
    private route: ActivatedRoute,
    private music_service: MusicService,
    private review_service: ReviewService,
    private auth_service: AuthService
  ) { }

  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    let id_music = Number(this.route.snapshot.paramMap.get("id"))
    try {
      this.music = await this.getMusic(id_music);
      console.log(this.music)
      this.reviews = (await this.getMusicReviews(id_music)).items
      console.log(this.reviews)
    } catch (error) {
      console.error(error)
    }

    this.isLoading = false
  }

  getMusic(id: number) {
    return firstValueFrom(this.music_service.get(id))
  }

  isLoggedIn() {
    return this.auth_service.isLoggedIn()
  }

  getMusicReviews(id: number) {
    return firstValueFrom(this.review_service.getAll(id))
  }

  getRange(start: number, end: number): number[] {
    return Array.from({ length: end - start + 1 }, (_, index) => start + index);
  }


  toInt(value: number) {
    return Math.round(value)
  }

  counter(id?: number) {
    return id ? new Array(Math.round(id)) : []
  }
}

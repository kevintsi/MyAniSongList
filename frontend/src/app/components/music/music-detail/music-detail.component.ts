import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Subscription, firstValueFrom } from 'rxjs';
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
  userReview!: Review | null

  noteVisual: number = 0
  noteMusic: number = 0
  description = new FormControl("")

  reviewAddedSubscription!: Subscription

  constructor(
    private route: ActivatedRoute,
    private musicService: MusicService,
    private reviewService: ReviewService,
    private authService: AuthService,
  ) { }

  ngOnInit(): void {
    this.fetchData()
    this.initReviewAddedSubscription()
  }

  ngOnDestroy() {
    this.reviewAddedSubscription.unsubscribe();
  }


  async fetchData() {
    let id_music = Number(this.route.snapshot.paramMap.get("id"))
    try {
      this.music = await this.getMusic(id_music);
      console.log(this.music)
      this.reviews = (await this.getMusicReviews(id_music)).items
      if (this.isLoggedIn()) {
        this.userReview = await this.getUserReview(id_music)
        console.log(this.userReview)
        if (this.userReview) {
          this.description.setValue(this.userReview.description)
          this.noteMusic = this.userReview.note_music * 2
          this.noteVisual = this.userReview.note_visual * 2
        }
      }
      console.log(this.reviews)
    } catch (error) {
      console.error(error)
    } finally {
      this.isLoading = false
    }

  }

  async initReviewAddedSubscription() {
    this.reviewAddedSubscription = this.reviewService.reviewAdded.subscribe((data: boolean) => {
      if (data) {
        this.fetchData()
      }
    });

  }


  getMusic(id: number) {
    return firstValueFrom(this.musicService.get(id))
  }

  isLoggedIn() {
    return this.authService.isLoggedIn()
  }

  getMusicReviews(id: number) {
    return firstValueFrom(this.reviewService.getAllByIdMusic(id, 1, 10))
  }

  getUserReview(id: number) {
    return firstValueFrom(this.reviewService.getUserReview(id))
  }

  getRange(start: number, end: number): number[] {
    return Array.from({ length: end - start + 1 }, (_, index) => start + index);
  }

  onRating(value: string) {
    console.log(value)
  }

  onSubmit() {
    console.log("On submit")
    console.log(this.description)
    console.log(this.noteMusic)
    console.log(this.noteVisual)
    if (this.noteMusic == 0 || this.noteVisual == 0) {
      return
    }
    let id_music = Number(this.route.snapshot.paramMap.get("id"))

    let review = {
      description: this.description.value,
      note_visual: this.noteVisual / 2,
      note_music: this.noteMusic / 2,
      music_id: id_music
    }

    this.reviewService.create(review).subscribe({
      next: () => {
        alert("Avis ajouté/modifié avec succès")
        this.reviewService.reviewAdded.next(true)
      },
      error: (err) => {
        console.error(err.message)
      },
    })

  }
  toInt(value: number) {
    return Math.round(value)
  }

  counter(id?: number) {
    return id ? new Array(Math.round(id)) : []
  }
}

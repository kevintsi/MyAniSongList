import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription, firstValueFrom } from 'rxjs';
import { AuthService } from 'src/app/services/auth/auth.service';
import { MusicService } from 'src/app/services/music/music.service';
import { ReviewService } from 'src/app/services/review/review.service';
import { Music } from 'src/app/models/music.model';
import { Review } from 'src/app/models/review.model';
import { DomSanitizer, Title } from '@angular/platform-browser';
import { ToastrService } from 'ngx-toastr';
import { TranslateService } from '@ngx-translate/core';
import { getAppTitle } from 'src/app/config/app.config';

@Component({
  selector: 'app-music-detail',
  templateUrl: './music-detail.component.html',
  styleUrls: ['./music-detail.component.css']
})
export class MusicDetailComponent implements OnDestroy, OnInit {

  isLoading: boolean = true
  music!: Music
  favorites: Music[] = []
  reviews: Review[] = []
  userReview!: Review | null

  noteVisual: number = 0
  noteMusic: number = 0
  description = new FormControl("")

  reviewAddedSubscription?: Subscription
  addFavoriteSubscription?: Subscription
  deleteFavoriteSubscription?: Subscription
  createReviewSubscription?: Subscription
  languageSubscription?: Subscription;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private musicService: MusicService,
    private reviewService: ReviewService,
    private authService: AuthService,
    private translateService: TranslateService,
    private sanitizer: DomSanitizer,
    private title: Title,
    private toastr: ToastrService
  ) { }

  ngOnInit(): void {
    this.fetchData()
    this.initReviewAddedSubscription()
    this.languageSubscription = this.translateService.onLangChange.subscribe(() => {
      this.fetchData()
    })
  }

  getSafeUrl(id_video: string) {
    return this.sanitizer.bypassSecurityTrustResourceUrl("https://www.youtube.com/embed/" + id_video)
  }

  ngOnDestroy() {
    this.reviewAddedSubscription?.unsubscribe();
    this.addFavoriteSubscription?.unsubscribe();
    this.deleteFavoriteSubscription?.unsubscribe();
    this.createReviewSubscription?.unsubscribe();
    this.languageSubscription?.unsubscribe()
  }


  async fetchData() {
    let id_music = Number(this.route.snapshot.paramMap.get("id"))
    try {
      this.music = await this.getMusic(id_music);
      this.title.setTitle(getAppTitle(this.music.name))
      this.reviews = (await this.getMusicReviews(id_music)).items
      if (this.isLoggedIn()) {
        this.userReview = await this.getUserReview(id_music)
        if (this.userReview) {
          this.description.setValue(this.userReview.description)
          this.noteMusic = this.userReview.note_music * 2
          this.noteVisual = this.userReview.note_visual * 2
        }
        this.favorites = await this.getFavorites()
      }
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

  toggleFavorite() {
    if (!this.isLoggedIn()) {
      this.router.navigateByUrl("/login")
      return
    }
    if (this.isFavorite()) {
      this.removeFromFavorites();
    } else {
      this.addToFavorites();
    }
  }

  isFavorite() {
    return this.favorites.some((fav_music => fav_music.id == this.music.id))
  }


  getMusic(id: number) {
    return firstValueFrom(this.musicService.get(id, this.translateService.currentLang))
  }
  addToFavorites(): void {
    this.addFavoriteSubscription = this.musicService.addToFavorites(this.music.id).subscribe({
      next: () => {
        this.favorites.push(this.music);
        this.toastr.success("Ajoutée aux favoris", 'Ajout', {
          progressBar: true,
          timeOut: 3000
        })
      },
      error: (err) => {
        console.error(err.message)
        this.toastr.error("Echec ajout au favoris", 'Ajout', {
          progressBar: true,
          timeOut: 3000
        })
      }
    });
  }

  removeFromFavorites(): void {
    this.deleteFavoriteSubscription = this.musicService.removeFromFavorites(this.music.id).subscribe({
      next: () => {
        this.favorites = this.favorites.filter((favItem) => favItem.id !== this.music.id);
        this.toastr.success("Supprimée des favoris", 'Suppression', {
          progressBar: true,
          timeOut: 3000
        })
      },
      error: (err) => {
        console.error(err.message)
        this.toastr.error("Echec suppression des favoris", 'Ajout', {
          progressBar: true,
          timeOut: 3000
        })
      }
    });
  }

  getFavorites() {
    return firstValueFrom(this.musicService.getFavorites())
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

  onSubmit() {
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

    this.createReviewSubscription = this.reviewService.create(review).subscribe({
      next: () => {
        this.toastr.success("Avis ajouté/modifié avec succès", 'Avis', {
          progressBar: true,
          timeOut: 3000
        })
        this.reviewService.reviewAdded.next(true)
      },
      error: (err) => {
        console.error(err.message)
        this.toastr.error("Echec modification/ajout de l'avis", 'Avis', {
          progressBar: true,
          timeOut: 3000
        })
      },
    })

  }
  toInt(value: number) {
    return Math.round(value)
  }

  counter(id?: number) {
    return id ? new Array(Math.round(id)) : []
  }

  getCurrentLang() {
    return this.translateService.currentLang
  }

}

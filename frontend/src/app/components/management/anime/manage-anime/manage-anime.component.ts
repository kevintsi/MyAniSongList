import { Component, OnDestroy, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { TranslateService } from '@ngx-translate/core';
import { Subscription, firstValueFrom } from 'rxjs';
import { AnimeService } from 'src/app/services/anime/anime.service';
import { getAppTitle } from 'src/app/config/app.config';
import { Anime, PagedAnime } from 'src/app/models/anime.model';

@Component({
  selector: 'app-manage-anime',
  templateUrl: './manage-anime.component.html',
  styleUrls: ['./manage-anime.component.css']
})
export class ManageAnimeComponent implements OnInit, OnDestroy {
  isLoading = true
  animes!: PagedAnime
  currentPage: number = 1
  languageChangeSubscription?: Subscription
  searchSubscription?: Subscription
  deleteSubscription?: Subscription

  constructor(
    private service: AnimeService,
    private translateService: TranslateService,
    private title: Title,
  ) {
    this.title.setTitle(getAppTitle("Gestion - Animes"))
  }

  ngOnInit(): void {
    this.fetchData()
    this.translateService.onLangChange.subscribe({
      next: () => this.fetchData()
    })
  }

  ngOnDestroy(): void {
    this.searchSubscription?.unsubscribe();
    this.deleteSubscription?.unsubscribe();
    this.languageChangeSubscription?.unsubscribe();
  }


  async fetchData() {
    try {
      this.animes = await this.fetchAnimes()
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
    }
  }

  performSearch(searchTerm: string) {
    this.searchSubscription = this.service.search(searchTerm, this.translateService.currentLang).subscribe({
      next: (animes) => {
        this.animes = animes
      },
      error: (err) => console.error(err.message)
    })
  }

  fetchAnimes() {
    return firstValueFrom(this.service.getAll(this.currentPage, this.translateService.currentLang))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }

  delete(selected: Anime) {
    this.deleteSubscription = this.service.delete(selected).subscribe({
      next: () => {
        this.animes.items = this.animes.items?.filter(anime => anime.id != selected.id)
      },
      error: (err) => console.log(err.message)
    })
  }
}

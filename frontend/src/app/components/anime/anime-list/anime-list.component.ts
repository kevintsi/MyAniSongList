import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { Anime, PagedAnime } from '../../../models/anime.model';
import { AnimeService } from '../../../services/anime/anime.service';
import { Title } from '@angular/platform-browser';
import { Subscription, firstValueFrom } from 'rxjs';
import { LanguageService } from 'src/app/services/language/language.service';
import { TranslateService } from '@ngx-translate/core';
import { getAppTitle } from 'src/app/config/app.config';

@Component({
  selector: 'app-anime-list',
  templateUrl: './anime-list.component.html',
  styleUrls: ['./anime-list.component.css']
})
export class AnimeListComponent implements OnInit, OnChanges {
  isLoading = true
  animes!: PagedAnime

  currentPage: number = 1

  languageSubscription?: Subscription;


  constructor(
    private service: AnimeService,
    private translateService: TranslateService,
    private title: Title) {
  }


  ngOnInit(): void {
    this.title.setTitle(getAppTitle("Animes"))
    this.fetchData()
    this.languageSubscription = this.translateService.onLangChange.subscribe(() => {
      this.fetchData()
    })
  }

  ngOnDestroy(): void {
    this.languageSubscription?.unsubscribe()
  }


  ngOnChanges(changes: SimpleChanges): void {
    // When the 'data' property changes, scroll to the top
    if (changes['currentPage'] && !changes['currentPage'].firstChange) {
      window.scrollTo(0, 0);
    }
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

  fetchAnimes() {
    return firstValueFrom(this.service.getAll(this.currentPage, this.translateService.currentLang))
  }



  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
    window.scrollTo(0, 0)
  }
}

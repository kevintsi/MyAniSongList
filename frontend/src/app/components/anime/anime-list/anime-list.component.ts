import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { Anime, PagedAnime } from '../../../models/Anime';
import { AnimeService } from '../../../_services/anime.service';
import { Title } from '@angular/platform-browser';
import { firstValueFrom } from 'rxjs';
import { LanguageService } from 'src/app/_services/language.service';

@Component({
  selector: 'app-anime-list',
  templateUrl: './anime-list.component.html',
  styleUrls: ['./anime-list.component.css']
})
export class AnimeListComponent implements OnInit, OnChanges {
  isLoading = true
  animes!: PagedAnime

  currentPage: number = 1


  constructor(
    private service: AnimeService,
    private languageService: LanguageService,
    private title: Title) { }

  ngOnInit(): void {
    this.fetchData()
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
      this.title.setTitle("MyAniSongList - Animes")
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
    }
  }

  fetchAnimes() {
    return firstValueFrom(this.service.getAll(this.currentPage, this.languageService.getLanguage()))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
    window.scrollTo(0, 0)
  }
}

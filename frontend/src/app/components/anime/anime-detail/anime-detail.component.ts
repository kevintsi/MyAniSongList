import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription, firstValueFrom } from 'rxjs'
import { Music } from 'src/app/models/music.model'
import { MusicService } from 'src/app/services/music/music.service';
import { AnimeService } from 'src/app/services/anime/anime.service';
import { Anime } from 'src/app/models/anime.model';
import { ActivatedRoute } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { TranslateService } from '@ngx-translate/core';
import { getAppTitle } from 'src/app/config/app.config';

@Component({
  selector: 'app-anime-detail',
  templateUrl: './anime-detail.component.html',
  styleUrls: ['./anime-detail.component.css']
})
export class AnimeDetailComponent implements OnInit, OnDestroy {
  isLoading: boolean = true
  musics!: Music[]
  anime!: Anime

  languageSubscription?: Subscription
  constructor(
    private route: ActivatedRoute,
    private musicService: MusicService,
    private animeService: AnimeService,
    private translateService: TranslateService,
    private title: Title
  ) {
  }

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
    let id_anime = Number(this.route.snapshot.paramMap.get("id"))
    try {
      this.anime = await this.fetchAnime(id_anime)
      this.title.setTitle(getAppTitle(this.anime.name))
      this.musics = await this.fetchMusics(id_anime)
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  async fetchAnime(id: number) {
    return firstValueFrom(this.animeService.get(id, this.translateService.currentLang))
  }

  async fetchMusics(id: number) {
    return firstValueFrom(this.musicService.getMusicsAnime(id, this.translateService.currentLang))
  }


  getCurrentLang() {
    return this.translateService.currentLang
  }

}



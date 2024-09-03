import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { Subscription, firstValueFrom } from 'rxjs'
import { ArtistService } from 'src/app/services/artist/artist.service';
import { MusicService } from 'src/app/services/music/music.service';
import { getAppTitle } from 'src/app/config/app.config';
import { Artist } from 'src/app/models/artist.model';
import { Music } from 'src/app/models/music.model';

@Component({
  selector: 'app-artist-detail',
  templateUrl: './artist-detail.component.html',
  styleUrls: ['./artist-detail.component.css']
})
export class ArtistDetailComponent implements OnInit {
  isLoading: boolean = true
  musics: Music[] = []
  artist!: Artist

  private languageSubscription!: Subscription;

  constructor(
    private route: ActivatedRoute,
    private musicService: MusicService,
    private artistService: ArtistService,
    private translateService: TranslateService,
    private title: Title
  ) { }


  ngOnInit(): void {
    this.fetchData()
    this.languageSubscription = this.translateService.onLangChange.subscribe(() => {
      this.fetchData()
    })
  }

  ngOnDestroy(): void {
    if (this.languageSubscription) this.languageSubscription.unsubscribe()
  }


  async fetchData() {
    let artistId = Number(this.route.snapshot.paramMap.get("id"))
    try {
      this.artist = await this.fetchArtist(artistId)
      this.musics = await this.fetchMusicsArtist(artistId)
      this.title.setTitle(getAppTitle(this.artist.name))
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  async fetchArtist(id: number) {
    return firstValueFrom(this.artistService.get(id))
  }

  async fetchMusicsArtist(id: number) {
    return firstValueFrom(this.musicService.getMusicsArtist(id, this.translateService.currentLang))
  }


  getCurrentLang() {
    return this.translateService.currentLang
  }
}

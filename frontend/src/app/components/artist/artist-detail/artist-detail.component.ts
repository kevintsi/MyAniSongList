import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { Subscription, firstValueFrom } from 'rxjs'
import { ArtistService } from 'src/app/_services/artist.service';
import { MusicService } from 'src/app/_services/music.service';
import { Artist } from 'src/app/models/Artist';
import { Music } from 'src/app/models/Music';

@Component({
  selector: 'app-artist-detail',
  templateUrl: './artist-detail.component.html',
  styleUrls: ['./artist-detail.component.css']
})
export class ArtistDetailComponent implements OnInit {
  isLoading: boolean = true
  musics: Music[] = []
  artist!: Artist

  languageSubscription?: Subscription;

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
    this.languageSubscription?.unsubscribe()
  }


  async fetchData() {
    let id_artist = Number(this.route.snapshot.paramMap.get("id"))
    try {
      this.artist = await this.fetchArtist(id_artist)
      this.musics = await this.fetchMusicsArtist(id_artist)
      this.title.setTitle("MyAniSongList - " + this.artist.name)
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
}

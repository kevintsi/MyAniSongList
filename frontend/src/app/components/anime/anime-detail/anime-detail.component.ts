import { Component, OnInit } from '@angular/core';
import { firstValueFrom } from 'rxjs'
import { Music } from 'src/app/models/Music'
import { MusicService } from 'src/app/_services/music.service';
import { AnimeService } from 'src/app/_services/anime.service';
import { Anime } from 'src/app/models/Anime';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-anime-detail',
  templateUrl: './anime-detail.component.html',
  styleUrls: ['./anime-detail.component.css']
})
export class AnimeDetailComponent implements OnInit {
  isLoading: boolean = true
  musics!: Music[]
  anime!: Anime
  constructor(
    private route: ActivatedRoute,
    private musicService: MusicService,
    private animeService: AnimeService
  ) { }

  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    let id_anime = Number(this.route.snapshot.paramMap.get("id"))
    try {
      this.anime = await this.fetchAnime(id_anime)
      this.musics = await this.fetchMusics(id_anime)
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  async fetchAnime(id: number) {
    return firstValueFrom(this.animeService.get(id))
  }

  async fetchMusics(id: number) {
    return firstValueFrom(this.musicService.getMusicsAnime(id))
  }
}



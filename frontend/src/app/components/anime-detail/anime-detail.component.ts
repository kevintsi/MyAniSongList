import { Component, OnInit } from '@angular/core';
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
  musics: Music[] = []
  anime?: Anime
  constructor(
    private route: ActivatedRoute,
    private music_service: MusicService,
    private anime_service: AnimeService
  ) { }

  ngOnInit(): void {
    let id_anime = Number(this.route.snapshot.paramMap.get("id"))
    this.music_service.get_musics_anime(id_anime).subscribe({
      next: (musics) => {
        console.log("Musics : ", musics)
        this.musics = musics
      },
      error: (err) => console.log(err)
    })

    this.anime_service.get(id_anime).subscribe({
      next: (anime) => {
        console.log("Anime : ", anime)
        this.anime = anime
      },
      error: (err) => console.log(err)
    })
  }
}

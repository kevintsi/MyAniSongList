import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
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
  musics: Music[] = []
  artist?: Artist
  constructor(
    private route: ActivatedRoute,
    private music_service: MusicService,
    private anime_service: ArtistService
  ) { }

  ngOnInit(): void {
    let id_artist = Number(this.route.snapshot.paramMap.get("id"))
    this.music_service.getMusicsArtist(id_artist).subscribe({
      next: (musics) => {
        console.log("Musics : ", musics)

        this.musics = musics
      },
      error: (err) => console.log(err)
    })

    this.anime_service.get(id_artist).subscribe({
      next: (artist) => {
        console.log("Artist : ", artist)
        this.artist = artist
      },
      error: (err) => console.log(err)
    })
  }
}

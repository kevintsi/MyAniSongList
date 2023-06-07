import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MusicService } from 'src/app/_services/music.service';
import { Music } from 'src/app/models/Music';

@Component({
  selector: 'app-music-detail',
  templateUrl: './music-detail.component.html',
  styleUrls: ['./music-detail.component.css']
})
export class MusicDetailComponent {
  music?: Music
  constructor(
    private route: ActivatedRoute,
    private music_service: MusicService
  ) { }

  ngOnInit(): void {
    let id_music = Number(this.route.snapshot.paramMap.get("id"))
    this.music_service.get(id_music).subscribe({
      next: (music) => {
        console.log("Music : ", music)
        this.music = music
      },
      error: (err) => console.log(err)
    })
  }
}

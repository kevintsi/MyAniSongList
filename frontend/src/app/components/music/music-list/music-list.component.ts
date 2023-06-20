import { Component } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { MusicService } from 'src/app/_services/music.service';
import { Music } from 'src/app/models/Music';

@Component({
  selector: 'app-music-list',
  templateUrl: './music-list.component.html',
  styleUrls: ['./music-list.component.css']
})
export class MusicListComponent {
  loading = true
  musics?: Music[]

  constructor(private service: MusicService, private title: Title) { }
  ngOnInit(): void {
    this.title.setTitle(this.title.getTitle() + " - Liste de musiques")
    this.service.getAll().subscribe({
      next: (musics) => {
        console.log("Musics : ", musics.items)
        this.musics = musics.items
      },
      error: (err) => console.log(err),
      complete: () => this.loading = false
    })
  }
}

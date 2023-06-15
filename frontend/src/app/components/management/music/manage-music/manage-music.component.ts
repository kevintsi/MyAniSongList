import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { MusicService } from 'src/app/_services/music.service';
import { Music } from 'src/app/models/Music';

@Component({
  selector: 'app-manage-music',
  templateUrl: './manage-music.component.html',
  styleUrls: ['./manage-music.component.css']
})
export class ManageMusicComponent {
  loading = true
  musics!: Music[]

  constructor(private service: MusicService, private router: Router) { }


  ngOnInit(): void {
    this.service.getAll().subscribe({
      next: (musics) => {
        console.log("Musics : ", musics)
        this.musics = musics
      },
      error: (err) => console.log(err),
      complete: () => this.loading = false
    })
  }

  delete(selected_music: Music) {
    this.service.delete(Number(selected_music.id)).subscribe({
      next: () => {
        this.musics = this.musics?.filter(music => music.id != selected_music.id)
        console.log(this.musics)
      },
      error: (err) => console.log(err.message)
    })
  }

}

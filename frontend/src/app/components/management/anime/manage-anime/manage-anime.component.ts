import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AnimeService } from 'src/app/_services/anime.service';
import { Anime } from 'src/app/models/Anime';

@Component({
  selector: 'app-manage-anime',
  templateUrl: './manage-anime.component.html',
  styleUrls: ['./manage-anime.component.css']
})
export class ManageAnimeComponent implements OnInit {
  loading = true
  animes!: Anime[]

  constructor(private service: AnimeService, private router: Router) { }


  ngOnInit(): void {
    this.service.getAll().subscribe({
      next: (animes) => {
        console.log("Animes : ", animes.items)
        this.animes = animes.items
      },
      error: (err) => console.log(err),
      complete: () => this.loading = false
    })
  }

  delete(selected: Anime) {
    this.service.delete(Number(selected.id)).subscribe({
      next: () => {
        this.animes = this.animes?.filter(anime => anime.id != selected.id)
        console.log(this.animes)
      },
      error: (err) => console.log(err.message)
    })
  }
}

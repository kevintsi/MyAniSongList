import { Component, OnInit } from '@angular/core';
import { Anime } from '../../models/Anime';
import { AnimeService } from '../../_services/anime.service';

@Component({
  selector: 'app-anime-list',
  templateUrl: './anime-list.component.html',
  styleUrls: ['./anime-list.component.css']
})
export class AnimeListComponent implements OnInit {
  loading = true
  animes?: Anime[]

  constructor(private service: AnimeService) { }
  ngOnInit(): void {
    this.service.get_all().subscribe({
      next: (animes) => {
        console.log("Animes : ", animes)
        this.animes = animes
      },
      error: (err) => console.log(err),
      complete: () => this.loading = false
    })
  }

}

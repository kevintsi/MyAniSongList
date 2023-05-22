import { Component, OnInit } from '@angular/core';
import { Anime } from '../../models/Anime';
import { AnimeService } from '../../_services/anime.service';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-anime-list',
  templateUrl: './anime-list.component.html',
  styleUrls: ['./anime-list.component.css']
})
export class AnimeListComponent implements OnInit {
  loading = true
  animes?: Anime[]

  constructor(private service: AnimeService, private title: Title) { }
  ngOnInit(): void {
    this.title.setTitle(this.title.getTitle() + " - Liste d'animés")
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

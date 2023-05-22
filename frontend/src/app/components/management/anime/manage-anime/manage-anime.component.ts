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
  animes?: Anime[]

  constructor(private service: AnimeService, private router: Router) { }


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

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subject, firstValueFrom } from 'rxjs';
import { AnimeService } from 'src/app/_services/anime.service';
import { Anime, PagedAnime } from 'src/app/models/Anime';

@Component({
  selector: 'app-manage-anime',
  templateUrl: './manage-anime.component.html',
  styleUrls: ['./manage-anime.component.css']
})
export class ManageAnimeComponent implements OnInit {
  isLoading = true
  animes!: PagedAnime
  currentPage: number = 1

  constructor(private service: AnimeService, private router: Router) { }

  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    try {
      this.animes = await this.fetchAnimes()
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
    }
  }

  performSearch(searchTerm: string) {
    this.service.search(searchTerm).subscribe({
      next: (anime) => {
        this.animes = anime
      },
      error: (err) => console.error(err.message)
    })
  }

  fetchAnimes() {
    return firstValueFrom(this.service.getAll(this.currentPage))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }

  delete(selected: Anime) {
    this.service.delete(Number(selected.id)).subscribe({
      next: () => {
        this.animes.items = this.animes.items?.filter(anime => anime.id != selected.id)
        console.log(this.animes)
      },
      error: (err) => console.log(err.message)
    })
  }
}

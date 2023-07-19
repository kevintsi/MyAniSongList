import { Component, OnInit } from '@angular/core';
import { Anime, PagedAnime } from '../../../models/Anime';
import { AnimeService } from '../../../_services/anime.service';
import { Title } from '@angular/platform-browser';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-anime-list',
  templateUrl: './anime-list.component.html',
  styleUrls: ['./anime-list.component.css']
})
export class AnimeListComponent implements OnInit {
  isLoading = true
  animes!: PagedAnime

  currentPage: number = 1


  constructor(private service: AnimeService) { }
  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    try {
      this.animes = await this.fetchAnimes()
      console.log("Animes : ", this.animes)
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
    }
  }

  fetchAnimes() {
    return firstValueFrom(this.service.getAll(this.currentPage))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }
}

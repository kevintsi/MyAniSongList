import { Component, OnDestroy, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { Subscription, firstValueFrom } from 'rxjs';
import { AnimeService } from 'src/app/_services/anime.service';
import { Anime, PagedAnime } from 'src/app/models/Anime';

@Component({
  selector: 'app-manage-anime',
  templateUrl: './manage-anime.component.html',
  styleUrls: ['./manage-anime.component.css']
})
export class ManageAnimeComponent implements OnInit, OnDestroy {
  isLoading = true
  animes!: PagedAnime
  currentPage: number = 1
  searchSubscription?: Subscription
  deleteSubscription?: Subscription

  constructor(private service: AnimeService, private title: Title) { }

  ngOnInit(): void {
    this.fetchData()
  }

  ngOnDestroy(): void {
    this.searchSubscription?.unsubscribe();
    this.deleteSubscription?.unsubscribe();
  }


  async fetchData() {
    try {
      this.animes = await this.fetchAnimes()
      this.title.setTitle("MyAniSongList - Gestion - Anime")
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
    }
  }

  performSearch(searchTerm: string) {
    this.searchSubscription = this.service.search(searchTerm).subscribe({
      next: (animes) => {
        this.animes = animes
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
    this.deleteSubscription = this.service.delete(selected.id).subscribe({
      next: () => {
        this.animes.items = this.animes.items?.filter(anime => anime.id != selected.id)
      },
      error: (err) => console.log(err.message)
    })
  }
}

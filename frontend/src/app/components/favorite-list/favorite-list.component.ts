import { Component } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { MusicService } from 'src/app/_services/music.service';
import { Music } from 'src/app/models/Music';

@Component({
  selector: 'app-favorite',
  templateUrl: './favorite-list.component.html',
  styleUrls: ['./favorite-list.component.css']
})
export class FavoriteListComponent {
  loading = true
  musics!: Music[]

  currentPage: number = 1

  constructor(private service: MusicService) { }
  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    try {
      this.musics = await this.fetchFavoritesMusics()
    } catch (error) {
      console.log(error)
    }
    finally {
      this.loading = false
    }
  }

  fetchFavoritesMusics() {
    return firstValueFrom(this.service.getFavorites())
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }
}

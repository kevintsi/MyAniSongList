import { Component } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { firstValueFrom } from 'rxjs';
import { MusicService } from 'src/app/services/music/music.service';
import { getAppTitle } from 'src/app/config/app.config';
import { Music } from 'src/app/models/music.model';

@Component({
  selector: 'app-favorite',
  templateUrl: './favorite-list.component.html',
  styleUrls: ['./favorite-list.component.css']
})
export class FavoriteListComponent {
  isLoading = true
  musics!: Music[]

  currentPage: number = 1

  constructor(private service: MusicService, private title: Title) { }
  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    try {
      this.musics = await this.fetchFavoritesMusics()
      this.title.setTitle(getAppTitle("Mes musiques favorites"))
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
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

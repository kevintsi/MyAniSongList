import { Component } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { firstValueFrom } from 'rxjs';
import { MusicService } from 'src/app/services/music/music.service';
import { getAppTitle } from 'src/app/config/app.config';
import { PagedMusic } from 'src/app/models/music.model';

@Component({
  selector: 'app-music-list',
  templateUrl: './music-list.component.html',
  styleUrls: ['./music-list.component.css']
})
export class MusicListComponent {
  isLoading = true
  musics!: PagedMusic
  currentPage: number = 1

  constructor(private service: MusicService, private title: Title) { }
  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    try {
      this.musics = await this.fetchMusics()
      this.title.setTitle(getAppTitle("Musiques"))
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
    }
  }

  fetchMusics() {
    return firstValueFrom(this.service.getAll(this.currentPage))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }
}

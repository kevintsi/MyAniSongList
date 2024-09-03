import { Component } from '@angular/core';
import { MusicService } from 'src/app/services/music/music.service';
import { PagedMusic } from 'src/app/models/music.model';
import { firstValueFrom } from 'rxjs'
import { Title } from '@angular/platform-browser';
import { getAppTitle } from 'src/app/config/app.config';

@Component({
  selector: 'app-ranking-music',
  templateUrl: './ranking-music.component.html',
  styleUrls: ['./ranking-music.component.css']
})
export class RankingMusicComponent {
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
      this.title.setTitle(getAppTitle("Classement des musiques"))
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
    }
  }

  fetchMusics() {
    return firstValueFrom(this.service.getAll(this.currentPage, 'avg_note'))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }
}

import { Component } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { MusicService } from 'src/app/_services/music.service';
import { PagedMusic } from 'src/app/models/Music';
import { firstValueFrom } from 'rxjs'

@Component({
  selector: 'app-ranking-music',
  templateUrl: './ranking-music.component.html',
  styleUrls: ['./ranking-music.component.css']
})
export class RankingMusicComponent {
  loading = true
  musics!: PagedMusic

  currentPage: number = 1

  constructor(private service: MusicService, private title: Title) { }
  ngOnInit(): void {
    this.title.setTitle("Classement des musiques")
    this.fetchData()
  }

  async fetchData() {
    try {
      this.musics = await this.fetchMusics()
    } catch (error) {
      console.log(error)
    }
    finally {
      this.loading = false
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

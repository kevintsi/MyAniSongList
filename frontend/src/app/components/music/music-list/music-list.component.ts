import { Component } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { firstValueFrom } from 'rxjs';
import { MusicService } from 'src/app/_services/music.service';
import { Music, PagedMusic } from 'src/app/models/Music';

@Component({
  selector: 'app-music-list',
  templateUrl: './music-list.component.html',
  styleUrls: ['./music-list.component.css']
})
export class MusicListComponent {
  loading = true
  musics!: PagedMusic

  currentPage: number = 1

  constructor(private service: MusicService, private title: Title) { }
  ngOnInit(): void {
    this.title.setTitle("Liste de musiques")
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
    return firstValueFrom(this.service.getAll(this.currentPage))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }
}

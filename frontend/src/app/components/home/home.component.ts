import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { firstValueFrom } from 'rxjs';
import { MusicService } from 'src/app/_services/music.service';
import { getAppTitle } from 'src/app/config/app';
import { Music } from 'src/app/models/Music';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  isLoading: boolean = true
  latestMusics: Music[] = []
  popularMusics: Music[] = []

  constructor(private title: Title, private musicService: MusicService) {
    this.title.setTitle(getAppTitle("Accueil"))
  }

  ngOnInit() {
    this.fetchData()
  }

  async fetchData() {
    try {
      this.latestMusics = await this.fetchLatest()
      this.popularMusics = await this.fetchPopular()
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  fetchPopular() {
    return firstValueFrom(this.musicService.getPopular())
  }

  fetchLatest() {
    return firstValueFrom(this.musicService.getLatest())
  }

}

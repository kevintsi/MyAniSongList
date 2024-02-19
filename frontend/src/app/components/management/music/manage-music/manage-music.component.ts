import { Component, OnDestroy, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { Subject, Subscription, firstValueFrom } from 'rxjs';
import { MusicService } from 'src/app/_services/music.service';
import { Music, PagedMusic } from 'src/app/models/Music';

@Component({
  selector: 'app-manage-music',
  templateUrl: './manage-music.component.html',
  styleUrls: ['./manage-music.component.css']
})
export class ManageMusicComponent implements OnDestroy, OnInit {
  isLoading = true
  musics!: PagedMusic
  currentPage: number = 1
  searchSubscription?: Subscription
  deleteSubscription?: Subscription

  constructor(private service: MusicService, private title: Title) { }

  ngOnDestroy(): void {
    this.searchSubscription?.unsubscribe()
    this.deleteSubscription?.unsubscribe()
  }
  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    try {
      this.musics = await this.fetchMusics()
      this.title.setTitle("MyAniSongList - Gestion - Musique")
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


  performSearch(searchTerm: string) {
    this.searchSubscription = this.service.search(searchTerm).subscribe({
      next: (music) => {
        this.musics = music
      },
      error: (err) => console.error(err.message)
    })
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }

  delete(selected_music: Music) {
    this.deleteSubscription = this.service.delete(Number(selected_music.id)).subscribe({
      next: () => {
        this.musics.items = this.musics.items.filter(music => music.id != selected_music.id)
      },
      error: (err) => console.log(err.message)
    })
  }

}

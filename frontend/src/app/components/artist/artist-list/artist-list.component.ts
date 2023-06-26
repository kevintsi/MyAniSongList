import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { firstValueFrom } from 'rxjs';
import { ArtistService } from 'src/app/_services/artist.service';
import { Artist, PagedArtist } from 'src/app/models/Artist';

@Component({
  selector: 'app-artist-list',
  templateUrl: './artist-list.component.html',
  styleUrls: ['./artist-list.component.css']
})
export class ArtistListComponent implements OnInit {
  loading = true
  artists!: PagedArtist

  currentPage: number = 1

  constructor(private service: ArtistService, private title: Title) { }
  ngOnInit(): void {
    this.title.setTitle(this.title.getTitle() + " - Liste d'artistes")
    this.fetchData()
  }

  async fetchData() {
    try {
      this.artists = await this.fetchArtists()
    } catch (error) {
      console.log(error)
    }
    finally {
      this.loading = false
    }
  }

  fetchArtists() {
    return firstValueFrom(this.service.getAll(this.currentPage))
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }
}

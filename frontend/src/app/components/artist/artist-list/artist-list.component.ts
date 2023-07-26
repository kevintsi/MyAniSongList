import { Component, OnInit } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { ArtistService } from 'src/app/_services/artist.service';
import { PagedArtist } from 'src/app/models/Artist';

@Component({
  selector: 'app-artist-list',
  templateUrl: './artist-list.component.html',
  styleUrls: ['./artist-list.component.css']
})
export class ArtistListComponent implements OnInit {
  isLoading = true
  artists!: PagedArtist

  currentPage: number = 1

  constructor(private service: ArtistService) { }
  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    try {
      this.artists = await this.fetchArtists()
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
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

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { ArtistService } from 'src/app/_services/artist.service';
import { Artist, PagedArtist } from 'src/app/models/Artist';

@Component({
  selector: 'app-manage-artist',
  templateUrl: './manage-artist.component.html',
  styleUrls: ['./manage-artist.component.css']
})
export class ManageArtistComponent {
  isLoading = true
  artists!: PagedArtist

  currentPage: number = 1

  constructor(private service: ArtistService, private router: Router) { }

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

  performSearch(searchTerm: string) {
    this.service.search(searchTerm).subscribe({
      next: (artists) => {
        this.artists = artists
      },
      error: (err) => console.error(err.message)
    })
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.fetchData()
  }

  delete(artist: Artist) {
    this.service.delete(Number(artist.id)).subscribe({
      next: () => {
        this.artists.items = this.artists.items.filter(artist => artist.id != artist.id)
        console.log(this.artists)
      },
      error: (err) => console.log(err.message)
    })
  }
}

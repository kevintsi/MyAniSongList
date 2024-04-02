import { Component, OnDestroy } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { Subscription, firstValueFrom } from 'rxjs';
import { ArtistService } from 'src/app/services/artist/artist.service';
import { getAppTitle } from 'src/app/config/app.config';
import { Artist, PagedArtist } from 'src/app/models/artist.model';

@Component({
  selector: 'app-manage-artist',
  templateUrl: './manage-artist.component.html',
  styleUrls: ['./manage-artist.component.css']
})
export class ManageArtistComponent implements OnDestroy {
  isLoading = true
  artists!: PagedArtist
  searchSubscription?: Subscription
  deleteSubscription?: Subscription
  currentPage: number = 1

  constructor(private service: ArtistService, private title: Title) { }
  ngOnDestroy(): void {
    this.searchSubscription?.unsubscribe()
    this.deleteSubscription?.unsubscribe()
  }

  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    try {
      this.artists = await this.fetchArtists()
      this.title.setTitle(getAppTitle("Gestion - Artiste"))
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
    this.searchSubscription = this.service.search(searchTerm).subscribe({
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
    this.deleteSubscription = this.service.delete(artist.id).subscribe({
      next: () => {
        this.artists.items = this.artists.items.filter(artist => artist.id != artist.id)
      },
      error: (err) => console.log(err.message)
    })
  }
}

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ArtistService } from 'src/app/_services/artist.service';
import { Artist } from 'src/app/models/Artist';

@Component({
  selector: 'app-manage-artist',
  templateUrl: './manage-artist.component.html',
  styleUrls: ['./manage-artist.component.css']
})
export class ManageArtistComponent {
  loading = true
  artists!: Artist[]

  constructor(private service: ArtistService, private router: Router) { }


  ngOnInit(): void {
    this.service.getAll().subscribe({
      next: (artists) => {
        console.log("Artists : ", artists)
        this.artists = artists
      },
      error: (err) => console.log(err),
      complete: () => this.loading = false
    })
  }

  delete(artist: Artist) {
    this.service.delete(Number(artist.id)).subscribe({
      next: () => {
        this.artists = this.artists?.filter(artist => artist.id != artist.id)
        console.log(this.artists)
      },
      error: (err) => console.log(err.message)
    })
  }
}

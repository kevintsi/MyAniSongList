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
  artists?: Artist[]

  constructor(private service: ArtistService, private router: Router) { }


  ngOnInit(): void {
    this.service.get_all().subscribe({
      next: (animes) => {
        console.log("Artists : ", animes)
        this.artists = animes
      },
      error: (err) => console.log(err),
      complete: () => this.loading = false
    })
  }

  delete(id: any) {
    this.service.delete(id).subscribe({
      next: () => {
        this.artists = this.artists?.filter(anime => anime.id != id)
        console.log(this.artists)
      },
      error: (err) => console.log(err.message)
    })
  }
}

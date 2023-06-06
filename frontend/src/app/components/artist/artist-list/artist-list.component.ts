import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ArtistService } from 'src/app/_services/artist.service';
import { Artist } from 'src/app/models/Artist';

@Component({
  selector: 'app-artist-list',
  templateUrl: './artist-list.component.html',
  styleUrls: ['./artist-list.component.css']
})
export class ArtistListComponent implements OnInit {
  loading = true
  artists?: Artist[]

  constructor(private service: ArtistService, private title: Title) { }
  ngOnInit(): void {
    this.title.setTitle(this.title.getTitle() + " - Liste d'artistes")
    this.service.get_all().subscribe({
      next: (artists) => {
        console.log("Artists : ", artists)
        this.artists = artists
      },
      error: (err) => console.log(err),
      complete: () => this.loading = false
    })
  }
}

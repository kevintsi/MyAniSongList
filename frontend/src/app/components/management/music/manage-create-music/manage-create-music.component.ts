import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { AnimeService } from 'src/app/_services/anime.service';
import { ArtistService } from 'src/app/_services/artist.service';
import { MusicService } from 'src/app/_services/music.service';
import { TypeService } from 'src/app/_services/type.service';
import { Anime, PagedAnime } from 'src/app/models/Anime';
import { Artist, PagedArtist } from 'src/app/models/Artist';
import { Type } from 'src/app/models/Type';

@Component({
  selector: 'app-manage-create-music',
  templateUrl: './manage-create-music.component.html',
  styleUrls: ['./manage-create-music.component.css']
})
export class ManageCreateMusicComponent implements OnInit {
  create_form = this.form_builder.group({
    name: '',
    release_date: '',
    type_id: null,
  })
  preview_image?: any = null
  file: any
  types?: Type[]
  artists!: PagedArtist
  animes!: PagedAnime
  selected_artists: Array<Artist> = []
  selected_anime?: Anime
  artist_name: string = ""

  constructor(
    private music_service: MusicService,
    private type_service: TypeService,
    private anime_service: AnimeService,
    private artist_service: ArtistService,
    private form_builder: FormBuilder,
  ) { }

  ngOnInit(): void {
    this.get_type_list()
  }

  performSearchAnime(searchTerm: string) {
    console.log("NEW TERM ANIME : " + searchTerm)
    if (!searchTerm) {
      this.animes.items = []
      return
    }

    this.anime_service.search(searchTerm).subscribe({
      next: (animes) => {
        this.animes = animes
      },
      error: (err) => console.error(err.message)
    })
  }

  performSearchArtist(searchTerm: string) {
    console.log("NEW TERM Artist : " + searchTerm)
    if (!searchTerm) {
      this.artists.items = []
      return
    }

    this.artist_service.search(searchTerm).subscribe({
      next: (artists) => {
        this.artists = artists
      },
      error: (err) => console.error(err.message)
    })
  }

  onSubmit() {
    console.log(this.create_form.value)
    if (this.selected_anime && this.selected_artists.length > 0) {
      this.music_service.create(this.create_form.value, this.file, this.selected_anime, this.selected_artists)
        .subscribe({
          next: () => {
            alert("Musique ajouté")
          },
          error: (err) => console.log(err)
        })
    }
  }

  get_value(event: Event): string {
    return (event.target as HTMLInputElement).value;
  }

  get_type_list() {
    this.type_service.getAll()
      .subscribe({
        next: (types) => {
          this.types = types
        },
        error: (err) => console.log(err)
      })
  }


  onchange(event: Event) {
    console.log(event.target)
  }

  onselectartist(artist: Artist) {
    console.log("Selected : ", artist)
    if (!this.selected_artists.includes(artist)) {
      this.selected_artists.push(artist)
    }
    console.log("Selected artists : ", this.selected_artists)
    this.artists.items = []
  }

  onunselectartist(artist: Artist) {
    console.log("Selected : ", artist)
    this.selected_artists = this.selected_artists.filter(item => item.id != Number(artist.id))
    console.log("Selected artists : ", this.selected_artists)
    // this.resetData()
  }


  onselectanime(anime: Anime) {
    console.log("Selected : ", anime)
    if (this.selected_anime?.id != anime.id) {
      this.selected_anime = anime
    }
    console.log("Selected anime : ", this.selected_anime)
    this.animes.items = []
    this.create_form
  }

  onunselectanime(anime: any) {
    console.log("Selected : ", anime.target?.id)
    this.selected_anime = undefined
    console.log("Selected anime : ", this.selected_anime)
    // this.resetData()
  }



  processFile(imageInput: any) {
    this.file = imageInput.files[0];
    if (this.file) {
      if (["image/jpeg", "image/png", "image/svg+xml"].includes(this.file.type)) {
        console.log("Image selected : ", this.file)
        let fileReader = new FileReader();
        fileReader.readAsDataURL(this.file);
        fileReader.addEventListener('load', event => {
          this.preview_image = event.target?.result
        })
      }
    }
  }
}

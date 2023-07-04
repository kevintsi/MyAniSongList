import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AnimeService } from 'src/app/_services/anime.service';
import { ArtistService } from 'src/app/_services/artist.service';
import { MusicService } from 'src/app/_services/music.service';
import { TypeService } from 'src/app/_services/type.service';
import { Anime, PagedAnime } from 'src/app/models/Anime';
import { Artist, PagedArtist } from 'src/app/models/Artist';
import { Type } from 'src/app/models/Type';

@Component({
  selector: 'app-manage-music-detail',
  templateUrl: './manage-music-detail.component.html',
  styleUrls: ['./manage-music-detail.component.css']
})
export class ManageMusicDetailComponent {
  update_form = this.form_builder.group({
    name: '',
    release_date: "",
    type_id: undefined,
    id_video: ""
  })
  preview_image?: any
  file: any
  types?: Type[]
  artists!: PagedArtist
  animes!: PagedAnime
  selected_artists!: Array<Artist>
  selected_anime?: Anime

  constructor(
    private music_service: MusicService,
    private type_service: TypeService,
    private anime_service: AnimeService,
    private artist_service: ArtistService,
    private router: Router,
    private route: ActivatedRoute,
    private form_builder: FormBuilder,
  ) { }

  ngOnInit(): void {
    console.log(`Music id : ${this.route.snapshot.paramMap.get('id')}`)
    let id = Number(this.route.snapshot.paramMap.get('id'))
    this.get(id)
    this.get_type_list()
  }

  get(id: number) {
    this.music_service.get(id).subscribe({
      next: (value) => {
        this.update_form.setValue({
          name: value.name,
          release_date: new Date(value.release_date).toISOString().split("T")[0],
          type_id: value.type.id,
          id_video: value.id_video
        })

        this.selected_anime = value.anime
        this.selected_artists = value.authors

        this.preview_image = value.poster_img
      },
      error: (err) => console.log(err)
    })
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
    let id = Number(this.route.snapshot.paramMap.get('id'))
    if (this.selected_anime && this.selected_artists) {
      this.music_service.update(id, this.update_form.value, this.file, this.selected_anime, this.selected_artists)
        .subscribe({
          next: () => {
            alert("Informations mises à jour")
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

  onselectartist(artist: Artist) {
    console.log("Selected : ", artist)
    if (!this.selected_artists.some(_ => _.id === artist.id)) {
      this.selected_artists.push(artist)
    }
    console.log("Selected artists : ", this.selected_artists)
    this.artists.items = []
  }

  onunselectartist(artist: Artist) {
    console.log("Selected : ", artist)
    this.selected_artists = this.selected_artists.filter(item => item.id != Number(artist.id))
    console.log("Selected artists : ", this.selected_artists)
  }


  onselectanime(anime: Anime) {
    console.log("Selected : ", anime)
    if (this.selected_anime?.id != anime.id) {
      this.selected_anime = anime
    }
    console.log("Selected anime : ", this.selected_anime)
    this.animes.items = []
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

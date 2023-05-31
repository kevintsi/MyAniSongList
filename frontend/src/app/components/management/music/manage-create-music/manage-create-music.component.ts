import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Observable, Subject, debounceTime, defaultIfEmpty, distinctUntilChanged, switchMap } from 'rxjs';
import { AnimeService } from 'src/app/_services/anime.service';
import { ArtistService } from 'src/app/_services/artist.service';
import { MusicService } from 'src/app/_services/music.service';
import { TypeService } from 'src/app/_services/type.service';
import { Anime } from 'src/app/models/Anime';
import { Artist } from 'src/app/models/Artist';
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
  artists?: Observable<Artist[]>
  animes?: Observable<Anime[]>
  private input_anime = new Subject<string>()
  private input_artist = new Subject<string>()
  selected_artists: Array<Artist> = []
  selected_anime?: Anime

  constructor(
    private music_service: MusicService,
    private type_service: TypeService,
    private anime_service: AnimeService,
    private artist_service: ArtistService,
    private form_builder: FormBuilder,
  ) { }

  ngOnInit(): void {
    this.get_type_list()
    this.animes = this.input_anime.pipe(
      debounceTime(500),
      distinctUntilChanged(),
      switchMap(query => this.anime_service.search(query)),
    )

    this.artists = this.input_artist.pipe(
      debounceTime(500),
      distinctUntilChanged(),
      switchMap(query => this.artist_service.search(query)),
    )
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
    this.type_service.get_all()
      .subscribe({
        next: (types) => {
          this.types = types
        },
        error: (err) => console.log(err)
      })
  }

  get_artist_list(query: string) {
    this.input_artist.next(query)
  }

  get_anime_list(query: string) {
    this.input_anime.next(query)
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
    // this.resetData()
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
    // this.resetData()
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

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { AnimeService } from 'src/app/_services/anime.service';
import { ArtistService } from 'src/app/_services/artist.service';
import { MusicService } from 'src/app/_services/music.service';
import { TypeService } from 'src/app/_services/type.service';
import { Anime, PagedAnime } from 'src/app/models/Anime';
import { Artist, PagedArtist } from 'src/app/models/Artist';
import { Music } from 'src/app/models/Music';
import { Type } from 'src/app/models/Type';

@Component({
  selector: 'app-form-music',
  templateUrl: './form-music.component.html',
  styleUrls: ['./form-music.component.css']
})
export class FormMusicComponent {
  @Input() isUpdate!: boolean; // Indicates if it's an update operation
  @Input() music!: Music; // Existing data for update operation

  @Output() submitForm: EventEmitter<any> = new EventEmitter<any>();

  form!: FormGroup;
  previewImage?: any = null
  types?: Type[]
  artists!: PagedArtist
  animes!: PagedAnime
  artist_name: string = ""

  constructor(
    private type_service: TypeService,
    private anime_service: AnimeService,
    private artist_service: ArtistService,
    private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.initForm();
    if (this.isUpdate) {
      this.populateForm();
    }
    this.get_type_list()
  }

  initForm() {
    this.form = this.formBuilder.group({
      name: new FormControl("", [Validators.required]),
      release_date: new FormControl("", [Validators.required]),
      poster_img: new FormControl(null, [this.isUpdate ? Validators.nullValidator : Validators.required]),
      selected_anime: new FormControl(null, [Validators.required]),
      selected_artists: new FormControl([], [this.validateArrayNotEmpty]),
      id_video: new FormControl(null, [Validators.required]),
      type_id: new FormControl(null, [Validators.required])
    });
  }

  validateArrayNotEmpty(control: AbstractControl) {
    const array = control.value;
    console.log("Check array ", Array.isArray(array) && array.length === 0)
    if (Array.isArray(array) && array.length === 0) {
      return { arrayEmpty: true };
    }
    return null;
  }

  populateForm() {
    this.form.patchValue({
      name: this.music.name,
      release_date: new Date(this.music.release_date).toISOString().split("T")[0],
      selected_anime: this.music.anime,
      selected_artists: this.music.authors,
      type_id: this.music.type.id,
      id_video: this.music.id_video
    });

    this.previewImage = this.music.poster_img
  }

  onSubmit() {
    console.log(this.form)
    console.log(this.form.valid)
    if (this.form.valid) {
      const formData = this.form.value;
      this.submitForm.emit(formData);
    }
  }

  performSearchAnime(searchTerm: string) {
    console.log("NEW TERM ANIME : " + searchTerm + " ", searchTerm.trim().length == 0)
    if (searchTerm.trim().length == 0) {
      console.log("EMPTY STRING RESET")
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
    console.log("NEW TERM ARTIST : " + searchTerm + " ", searchTerm.trim().length == 0)
    if (searchTerm.trim().length == 0) {
      console.log("EMPTY STRING RESET")
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
    if (this.form.value.selected_artists && !this.form.value.selected_artists.some((_: Artist) => _.id === artist.id)) {
      this.form.patchValue({
        selected_artists: [...this.form.value.selected_artists, artist]
      })
    }
    console.log("Selected artists : ", this.form.value.selected_artists)
    this.artists.items = []
  }

  onunselectartist(artist: Artist) {
    console.log("Selected : ", artist)
    let selected_artists = this.form.value.selected_artists.filter((item: Artist) => item.id != Number(artist.id))
    this.form.patchValue({
      selected_artists: selected_artists
    })
    console.log("Selected artists : ", this.form.value.selected_artists)
    // this.resetData()
  }


  onselectanime(anime: Anime) {
    console.log("Selected : ", anime)
    if (this.form.value.selected_anime?.id != anime.id) {
      this.form.patchValue({
        selected_anime: anime
      })
    }
    console.log("Selected anime : ", this.form.value.selected_anime)
    this.animes.items = []
  }

  onunselectanime(anime: any) {
    console.log("Selected : ", anime.target?.id)
    this.form.patchValue({
      selected_anime: null
    })
    console.log("Selected anime : ", this.form.value.selected_anime)
    // this.resetData()
  }


  processFile(imageInput: any) {
    const file = imageInput.files[0];
    if (file) {
      if (["image/jpeg", "image/png", "image/svg+xml"].includes(file.type)) {
        console.log("Image selected : ", file)
        this.form.patchValue({
          poster_img: file
        })

        this.previewImage = URL.createObjectURL(file)
      }
    }
  }
}

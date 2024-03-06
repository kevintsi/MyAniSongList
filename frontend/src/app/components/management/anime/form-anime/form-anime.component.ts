import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core';
import { firstValueFrom } from 'rxjs';
import { AnimeService } from 'src/app/_services/anime.service';
import { Anime } from 'src/app/models/Anime';
import { Language } from 'src/app/models/Language';

@Component({
  selector: 'app-form-anime',
  templateUrl: './form-anime.component.html',
  styleUrls: ['./form-anime.component.css']
})
export class FormAnimeComponent {
  @Input() isUpdate!: boolean; // Indicates if it's an update operation
  @Input() anime!: Anime; // Existing data for update operation
  @Input() languagesAnime?: Language[]
  @Input() languages?: Language[]

  @Output() submitForm: EventEmitter<any> = new EventEmitter<any>();

  form!: FormGroup;
  previewImage?: any = null

  constructor(
    private service: AnimeService,
    private formBuilder: FormBuilder,
    private translateService: TranslateService
  ) { }

  ngOnInit() {
    this.initForm();
    if (this.isUpdate) {
      this.populateForm();
    }
  }

  async fetchData() {
    try {
      this.anime = await this.get(parseInt(String(this.anime.id)), this.form.get("language")?.value)
      this.form.patchValue({
        name: this.anime.name,
        description: this.anime.description
      })
    } catch (error) {
      console.log(error)
    }
  }

  get(id: number, lang: string) {
    return firstValueFrom(this.service.get(id, lang))
  }

  initForm() {
    this.form = this.formBuilder.group({
      name: new FormControl("", [Validators.required]),
      description: new FormControl("", [Validators.required]),
      poster_img: new FormControl(null, [this.isUpdate ? Validators.nullValidator : Validators.required])
    });
  }

  populateForm() {
    this.form.addControl("language", new FormControl(this.translateService.currentLang, [Validators.required]))
    this.form.patchValue({
      name: this.anime.name,
      description: this.anime.description,
    });

    this.previewImage = this.anime.poster_img
  }

  onChange($event: Event) {
    let lang_code: string = ($event.target as HTMLSelectElement).value
    console.log("Change : ", lang_code)
    this.form.patchValue({
      language: lang_code
    })
    this.fetchData()
  }

  onSubmit() {
    if (this.form.valid) {
      const formData = this.form.value;
      this.submitForm.emit(formData);
    }
  }

  processFile(imageInput: any) {
    const file = imageInput.files[0];
    if (file) {
      if (["image/jpeg", "image/png", "image/svg+xml"].includes(file.type)) {
        this.form.patchValue({
          poster_img: file
        })

        this.previewImage = URL.createObjectURL(file)
      }
    }
  }
}

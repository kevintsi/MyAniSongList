import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Subscription, firstValueFrom } from 'rxjs';
import { AnimeService } from 'src/app/services/anime/anime.service';
import { LanguageService } from 'src/app/services/language/language.service';
import { Anime } from 'src/app/models/anime.model';
import { Language } from 'src/app/models/language.model';

@Component({
  selector: 'app-manage-create-anime-translation',
  templateUrl: './manage-create-anime-translation.component.html',
  styleUrls: ['./manage-create-anime-translation.component.css']
})
export class ManageCreateAnimeTranslationComponent implements OnInit, OnDestroy {
  isLoading: boolean = true
  languages!: Language[]
  formAnimeGroup!: FormGroup
  addTranslationSubscription: Subscription = new Subscription()

  constructor(
    private languageService: LanguageService,
    private animeService: AnimeService,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private toast: ToastrService
  ) { }


  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    try {
      this.languages = await this.getLanguages()
      this.formAnimeGroup = this.formBuilder.group({
        name: new FormControl('', [Validators.required]),
        description: new FormControl('', [Validators.required]),
        language: new FormControl('fr', [Validators.required])
      })
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }
  getLanguages() {
    return firstValueFrom(this.languageService.getAll())
  }

  onSubmit() {
    if (this.formAnimeGroup.valid) {
      let anime: Anime = {
        id: parseInt(String(this.route.snapshot.paramMap.get('id'))),
        name: this.formAnimeGroup.get("name")?.value,
        description: this.formAnimeGroup.get('description')?.value
      }
      this.addTranslationSubscription = this.animeService.addTranslation(anime, this.formAnimeGroup.get('language')?.value).subscribe({
        next: () => {
          this.toast.success("La traduction a bien été ajoutée", 'Ajout')
        },
        error: (err: HttpErrorResponse) => {
          console.error(err)
          if (err.status == 409) {
            this.toast.error("La traduction pour cette langue existe déjà", 'Ajout')
          }
        }
      })
    }
  }

  ngOnDestroy(): void {
    this.addTranslationSubscription.unsubscribe()
  }

  onChange($event: Event) {
    let lang_code: string = ($event.target as HTMLSelectElement).value
    this.formAnimeGroup.patchValue({
      language: lang_code
    })
  }
}

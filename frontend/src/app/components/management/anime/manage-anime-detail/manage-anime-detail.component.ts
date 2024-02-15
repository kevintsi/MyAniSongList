import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AnimeService } from 'src/app/_services/anime.service';
import { Anime } from 'src/app/models/Anime';
import { Subscription, firstValueFrom } from 'rxjs'
import { ToastrService } from 'ngx-toastr';
import { Title } from '@angular/platform-browser';
import { Language } from 'src/app/models/Language';
import { LanguageService } from 'src/app/_services/language.service';
@Component({
  selector: 'app-manage-anime-detail',
  templateUrl: './manage-anime-detail.component.html',
  styleUrls: ['./manage-anime-detail.component.css']
})
export class ManageAnimeDetailComponent implements OnInit, OnDestroy {
  isLoading = true
  anime!: Anime
  animeSubscription = new Subscription()
  languages: Language[] = []
  languagesAnime: Language[] = []

  constructor(
    private service: AnimeService,
    private languageService: LanguageService,
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private title: Title
  ) {
    this.title.setTitle("MyAniSongList - Gestion - Modifier un anime")
  }

  ngOnDestroy(): void {
    this.animeSubscription.unsubscribe()
  }

  ngOnInit() {
    this.fetchData()
  }

  async fetchData() {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    try {
      this.anime = await this.get(id)
      this.languagesAnime = await this.getLanguagesByAnimeId()
      this.languages = await this.getLanguages()
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  getLanguagesByAnimeId() {
    return firstValueFrom(this.languageService.getSupportedLanguagesByAnime(this.anime))
  }

  getLanguages() {
    return firstValueFrom(this.languageService.getAll())
  }

  get(id: number) {
    return firstValueFrom(this.service.get(id))
  }

  onSubmit(formData: any) {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    this.animeSubscription = this.service.update(id, formData, formData.language)
      .subscribe({
        next: () => {
          this.toastr.success("Informations de l'animé mis à jour avec succès", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => {
          console.log(err)
          this.toastr.error("Echec de mise à jour des informations", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        }
      })
  }

}

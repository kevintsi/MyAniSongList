import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AnimeService } from 'src/app/_services/anime.service';
import { Anime } from 'src/app/models/Anime';
import { Subscription, firstValueFrom } from 'rxjs'
import { ToastrService } from 'ngx-toastr';
import { Title } from '@angular/platform-browser';
import { Type } from 'src/app/models/Type';
import { TypeService } from 'src/app/_services/type.service';
import { LanguageService } from 'src/app/_services/language.service';
import { Language } from 'src/app/models/Language';
@Component({
  selector: 'app-manage-type-detail',
  templateUrl: './manage-type-detail.component.html',
  styleUrls: ['./manage-type-detail.component.css']
})
export class ManageTypeDetailComponent implements OnInit, OnDestroy {
  isLoading = true
  type!: Type
  languagesType: Language[] = []
  typeSubscription = new Subscription()
  languages: Language[] = []

  constructor(
    private service: TypeService,
    private serviceLanguage: LanguageService,
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private title: Title
  ) {
    this.title.setTitle("MyAniSongList - Gestion - Modifier un type")
  }

  ngOnDestroy(): void {
    this.typeSubscription.unsubscribe()
  }

  ngOnInit() {
    this.fetchData()
  }

  async fetchData() {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    try {
      this.type = await this.get(id)
      this.languagesType = await this.getLanguagesByTypeId()
      this.languages = await this.getLanguages()
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  getLanguagesByTypeId() {
    return firstValueFrom(this.serviceLanguage.getSupportedLanguagesByType(this.type))
  }

  getLanguages() {
    return firstValueFrom(this.serviceLanguage.getAll())
  }

  get(id: number) {
    return firstValueFrom(this.service.get(id))
  }



  onSubmit(form: any) {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    let type: Type = {
      name: form.name
    }
    this.typeSubscription = this.service.updateTranslation(id, type, form.language)
      .subscribe({
        next: () => {
          this.toastr.success("Informations du type mis à jour avec succès", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => {
          console.log(err)
          this.toastr.error("Echec de mise à jour des informations du type", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        }
      })
  }

}

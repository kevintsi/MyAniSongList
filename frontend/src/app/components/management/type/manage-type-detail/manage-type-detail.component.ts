import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription, firstValueFrom } from 'rxjs'
import { ToastrService } from 'ngx-toastr';
import { Title } from '@angular/platform-browser';
import { Type } from 'src/app/models/type.model';
import { TypeService } from 'src/app/services/type/type.service';
import { LanguageService } from 'src/app/services/language/language.service';
import { Language } from 'src/app/models/language.model';
import { getAppTitle } from 'src/app/config/app.config';
import { TranslateService } from '@ngx-translate/core';
@Component({
  selector: 'app-manage-type-detail',
  templateUrl: './manage-type-detail.component.html',
  styleUrls: ['./manage-type-detail.component.css']
})
export class ManageTypeDetailComponent implements OnInit, OnDestroy {
  isLoading = true
  type!: Type
  languagesType: Language[] = []
  languages: Language[] = []


  typeSubscription?: Subscription
  languageChangeSubscription?: Subscription


  constructor(
    private service: TypeService,
    private serviceLanguage: LanguageService,
    private translateService: TranslateService,
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private title: Title
  ) {
    this.title.setTitle(getAppTitle("Gestion - Modifier un type"))
  }

  ngOnDestroy(): void {
    this.typeSubscription?.unsubscribe()
    this.languageChangeSubscription?.unsubscribe();
  }

  ngOnInit() {
    this.fetchData()
    this.languageChangeSubscription = this.translateService.onLangChange.subscribe({
      next: () => this.fetchData()
    })
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
    return firstValueFrom(this.service.get(id, this.translateService.currentLang))
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

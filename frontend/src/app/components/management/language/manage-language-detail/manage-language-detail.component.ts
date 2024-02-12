import { Component } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Subscription, firstValueFrom } from 'rxjs';
import { LanguageService } from 'src/app/_services/language.service';
import { Language } from 'src/app/models/Language';

@Component({
  selector: 'app-manage-language-detail',
  templateUrl: './manage-language-detail.component.html',
  styleUrls: ['./manage-language-detail.component.css']
})
export class ManageLanguageDetailComponent {
  isLoading = true
  language!: Language
  languageSubscription = new Subscription()

  constructor(
    private service: LanguageService,
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private title: Title
  ) { }

  ngOnDestroy(): void {
    this.languageSubscription.unsubscribe()
  }

  async ngOnInit() {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    try {
      this.language = await this.get(id)
      this.title.setTitle("MyAniSongList - Gestion - Modifier une langue")
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  get(id: number) {
    return firstValueFrom(this.service.get(id))
  }

  onSubmit(lang: Language) {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    this.languageSubscription = this.service.update(id, lang)
      .subscribe({
        next: () => {
          this.toastr.success("Le code de la langue a été mis à jour avec succès", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => {
          console.log(err)
          this.toastr.error("Echec de mise à jour du code de la langue", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        }
      })
  }
}

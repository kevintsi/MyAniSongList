import { Component } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ToastrService } from 'ngx-toastr';
import { Subscription } from 'rxjs';
import { LanguageService } from 'src/app/services/language/language.service';
import { getAppTitle } from 'src/app/config/app.config';
import { Language } from 'src/app/models/language.model';

@Component({
  selector: 'app-manage-create-language',
  templateUrl: './manage-create-language.component.html',
  styleUrls: ['./manage-create-language.component.css']
})
export class ManageCreateLanguageComponent {
  createSubscription?: Subscription
  constructor(
    private service: LanguageService,
    private toastr: ToastrService,
    private title: Title
  ) {

    this.title.setTitle(getAppTitle("Gestion - Ajouter une langue"))
  }
  ngOnDestroy(): void {
    this.createSubscription?.unsubscribe();
  }

  onSubmit(lang: Language) {

    this.service.add(lang)
      .subscribe({
        next: () => {
          this.toastr.success("Langue ajoutée avec succès", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => {
          console.log(err)
          this.toastr.error("Echec de l'ajout de la langue", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        }
      })
  }
}

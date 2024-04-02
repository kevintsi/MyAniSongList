import { Component, OnDestroy, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { Subscription, firstValueFrom } from 'rxjs';
import { LanguageService } from 'src/app/services/language/language.service';
import { getAppTitle } from 'src/app/config/app.config';
import { Language } from 'src/app/models/language.model';

@Component({
  selector: 'app-manage-language',
  templateUrl: './manage-language.component.html',
  styleUrls: ['./manage-language.component.css']
})
export class ManageLanguageComponent implements OnInit, OnDestroy {
  isLoading: boolean = true
  languages: Array<Language> = []
  deleteSubscription?: Subscription

  constructor(private service: LanguageService, private title: Title) { }

  ngOnInit(): void {
    this.title.setTitle(getAppTitle("Gestion - Langue"))
    this.fetchData()
  }

  async fetchData() {
    try {
      this.languages = await this.fetchLanguages()
    } catch (error) {
      console.error(error)
    }
    finally {
      this.isLoading = false
    }
  }

  fetchLanguages() {
    return firstValueFrom(this.service.getAll())
  }

  delete(selected: Language) {
    this.deleteSubscription = this.service.delete(selected).subscribe({
      next: () => {
        this.languages = this.languages?.filter(lang => lang.id != selected.id)
      },
      error: (err) => console.log(err)
    })
  }

  ngOnDestroy(): void {
    this.deleteSubscription?.unsubscribe()
  }

}

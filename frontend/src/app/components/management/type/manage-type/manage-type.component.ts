import { Component, OnDestroy, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { TranslateService } from '@ngx-translate/core';
import { Subscription, firstValueFrom } from 'rxjs';
import { TypeService } from 'src/app/_services/type.service';
import { getAppTitle } from 'src/app/config/app';
import { Type } from 'src/app/models/Type';

@Component({
  selector: 'app-manage-type',
  templateUrl: './manage-type.component.html',
  styleUrls: ['./manage-type.component.css']
})
export class ManageTypeComponent implements OnInit, OnDestroy {
  isLoading = true
  types: Type[] = []

  deleteSubscription?: Subscription
  languageChangeSubscription?: Subscription

  constructor(
    private service: TypeService,
    private translateService: TranslateService,
    private title: Title) {
    this.title.setTitle(getAppTitle("Gestion - Types"))
  }

  ngOnInit(): void {
    this.fetchData()
    this.languageChangeSubscription = this.translateService.onLangChange.subscribe({
      next: () => this.fetchData()
    })
  }

  ngOnDestroy(): void {
    this.deleteSubscription?.unsubscribe();
    this.languageChangeSubscription?.unsubscribe();
  }


  async fetchData() {
    try {
      this.types = await this.fetchTypes()
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
    }
  }

  fetchTypes() {
    return firstValueFrom(this.service.getAll(this.translateService.currentLang))
  }

  delete(selected: Type) {
    this.deleteSubscription = this.service.delete(selected).subscribe({
      next: () => {
        this.types = this.types?.filter(type => type.id != selected.id)
      },
      error: (err) => console.log(err.message)
    })
  }
}

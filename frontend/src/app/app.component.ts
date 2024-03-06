import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { getLangFromStorage } from './config/lang';
import { APP_TITLE } from './config/app';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title: string = APP_TITLE

  constructor(translateService: TranslateService) {
    let lang = getLangFromStorage()
    translateService.use(lang.id)
  }
}

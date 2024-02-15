import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title: string = "MyAniSongList"

  constructor(translateService: TranslateService) {
    let lang = localStorage.getItem('lang') ? JSON.parse(String(localStorage.getItem('lang')))["id"] : "fr"
    translateService.use(lang)
  }
}

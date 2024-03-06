import { Component } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { getAppTitle } from 'src/app/config/app';

@Component({
  selector: 'app-not-found',
  templateUrl: './not-found.component.html'
})
export class NotFoundComponent {
  constructor(private title: Title) {
    this.title.setTitle(getAppTitle("Page non trouvée"))
  }
}

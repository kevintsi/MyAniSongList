import { Component } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-not-found',
  templateUrl: './not-found.component.html'
})
export class NotFoundComponent {
  constructor(private title: Title) {
    this.title.setTitle("MyAniSongList - Page non trouvée")
  }
}

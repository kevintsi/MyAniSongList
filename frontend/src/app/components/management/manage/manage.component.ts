import { Component } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { getAppTitle } from 'src/app/config/app';

@Component({
  selector: 'app-manage',
  templateUrl: './manage.component.html',
  styleUrls: ['./manage.component.css']
})
export class ManageComponent {
  constructor(private title: Title) {
    this.title.setTitle(getAppTitle("Gestion"))
  }

}

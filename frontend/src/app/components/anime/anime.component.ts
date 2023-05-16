import { Component, Input, OnInit } from '@angular/core';
import { Anime } from '../../models/Anime';

@Component({
  selector: 'app-anime',
  templateUrl: './anime.component.html',
  styleUrls: ['./anime.component.css']
})


export class AnimeComponent implements OnInit {
  @Input() anime?: Anime;

  ngOnInit(): void {
    console.log("Anime : " + this.anime?.id + ", name : " + this.anime?.name)
  }
}

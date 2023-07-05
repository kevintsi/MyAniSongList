import { Component } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AnimeService } from 'src/app/_services/anime.service';

@Component({
  selector: 'app-manage-create-anime',
  templateUrl: './manage-create-anime.component.html',
  styleUrls: ['./manage-create-anime.component.css']
})
export class ManageCreateAnimeComponent {
  constructor(
    private service: AnimeService,
  ) { }

  onSubmit(formData: any) {
    console.log(formData)
    this.service.create(formData)
      .subscribe({
        next: () => {
          alert("Animé ajouté")
        },
        error: (err) => console.log(err)
      })
  }

}


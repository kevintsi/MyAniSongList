import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ArtistService } from 'src/app/_services/artist.service';

@Component({
  selector: 'app-manage-create-artist',
  templateUrl: './manage-create-artist.component.html',
  styleUrls: ['./manage-create-artist.component.css']
})
export class ManageCreateArtistComponent {

  constructor(
    private service: ArtistService,
  ) { }

  onSubmit(formData: any) {
    console.log(formData)
    this.service.create(formData)
      .subscribe({
        next: () => {
          alert("Artiste ajouté")
        },
        error: (err) => console.log(err)
      })
  }
}

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
  create_form = this.form_builder.group({
    name: '',
    creation_year: '',
  })
  preview_image?: any = null
  file: any

  constructor(
    private service: ArtistService,
    private form_builder: FormBuilder,
  ) { }

  onSubmit() {
    this.service.create(this.create_form.value, this.file)
      .subscribe({
        next: () => {
          alert("Artiste ajouté")
        },
        error: (err) => console.log(err)
      })
  }

  processFile(imageInput: any) {
    this.file = imageInput.files[0];
    if (this.file) {
      if (["image/jpeg", "image/png", "image/svg+xml"].includes(this.file.type)) {
        console.log("Image selected : ", this.file)
        let fileReader = new FileReader();
        fileReader.readAsDataURL(this.file);
        fileReader.addEventListener('load', event => {
          this.preview_image = event.target?.result
        })
      }
    }
  }
}

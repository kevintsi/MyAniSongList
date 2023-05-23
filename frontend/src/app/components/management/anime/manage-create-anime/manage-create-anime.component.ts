import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AnimeService } from 'src/app/_services/anime.service';

@Component({
  selector: 'app-manage-create-anime',
  templateUrl: './manage-create-anime.component.html',
  styleUrls: ['./manage-create-anime.component.css']
})
export class ManageCreateAnimeComponent {
  create_form = this.form_builder.group({
    name: '',
    description: '',
  })
  preview_image?: any = null
  file: any

  constructor(
    private service: AnimeService,
    private router: Router,
    private route: ActivatedRoute,
    private form_builder: FormBuilder,
  ) { }

  onSubmit() {
    this.service.create(this.create_form.value, this.file)
      .subscribe({
        next: () => {
          alert("Animé ajouté")
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

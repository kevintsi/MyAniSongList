import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ArtistService } from 'src/app/_services/artist.service';

@Component({
  selector: 'app-manage-artist-detail',
  templateUrl: './manage-artist-detail.component.html',
  styleUrls: ['./manage-artist-detail.component.css']
})
export class ManageArtistDetailComponent {
  update_form = this.form_builder.group({
    name: '',
    creation_year: ''
  })
  preview_image?: any
  file: any

  constructor(
    private service: ArtistService,
    private router: Router,
    private route: ActivatedRoute,
    private form_builder: FormBuilder,
  ) { }

  ngOnInit(): void {
    console.log(`Artist id : ${this.route.snapshot.paramMap.get('id')}`)
    let id = Number(this.route.snapshot.paramMap.get('id'))
    this.get(id)
  }

  get(id: number) {
    this.service.get(id).subscribe({
      next: (value) => {
        this.update_form.setValue({
          name: String(value.name),
          creation_year: String(value.creation_year),
        })

        this.preview_image = String(value.poster_img)
      },
      error: (err) => console.log(err)
    })
  }

  onSubmit() {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    this.service.update(id, this.update_form.value, this.file)
      .subscribe({
        next: () => {
          alert("Informations mises à jour")
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

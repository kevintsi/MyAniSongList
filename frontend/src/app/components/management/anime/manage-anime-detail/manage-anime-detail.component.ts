import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AnimeService } from 'src/app/_services/anime.service';

@Component({
  selector: 'app-manage-anime-detail',
  templateUrl: './manage-anime-detail.component.html',
  styleUrls: ['./manage-anime-detail.component.css']
})
export class ManageAnimeDetailComponent {
  update_form = this.form_builder.group({
    name: '',
    description: '',
  })
  preview_image?: any
  file: any

  constructor(
    private service: AnimeService,
    private router: Router,
    private route: ActivatedRoute,
    private form_builder: FormBuilder,
  ) { }

  ngOnInit(): void {
    console.log(`Anime id : ${this.route.snapshot.paramMap.get('id')}`)
    let id = Number(this.route.snapshot.paramMap.get('id'))
    this.get(id)
  }

  get(id: number) {
    this.service.get(id).subscribe({
      next: (value) => {
        this.update_form.setValue({
          name: String(value.name),
          description: String(value.description),
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

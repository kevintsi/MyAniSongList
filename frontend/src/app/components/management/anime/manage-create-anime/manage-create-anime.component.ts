import { Component } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { AnimeService } from 'src/app/_services/anime.service';

@Component({
  selector: 'app-manage-create-anime',
  templateUrl: './manage-create-anime.component.html',
  styleUrls: ['./manage-create-anime.component.css']
})
export class ManageCreateAnimeComponent {
  constructor(
    private service: AnimeService,
    private toastr: ToastrService
  ) { }

  onSubmit(formData: any) {
    console.log(formData)
    this.service.create(formData)
      .subscribe({
        next: () => {
          this.toastr.success("Animé ajouté avec succès", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => console.log(err)
      })
  }

}


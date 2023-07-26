import { Component } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { ArtistService } from 'src/app/_services/artist.service';

@Component({
  selector: 'app-manage-create-artist',
  templateUrl: './manage-create-artist.component.html',
  styleUrls: ['./manage-create-artist.component.css']
})
export class ManageCreateArtistComponent {
  constructor(
    private service: ArtistService,
    private toastr: ToastrService
  ) { }

  onSubmit(formData: any) {
    console.log(formData)
    this.service.create(formData)
      .subscribe({
        next: () => {
          this.toastr.success("Artiste ajouté(e) avec succès", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => console.log(err)
      })
  }
}

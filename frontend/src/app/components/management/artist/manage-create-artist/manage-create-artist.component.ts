import { Component, OnDestroy } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ToastrService } from 'ngx-toastr';
import { Subscription } from 'rxjs';
import { ArtistService } from 'src/app/services/artist/artist.service';
import { getAppTitle } from 'src/app/config/app.config';

@Component({
  selector: 'app-manage-create-artist',
  templateUrl: './manage-create-artist.component.html',
  styleUrls: ['./manage-create-artist.component.css']
})
export class ManageCreateArtistComponent implements OnDestroy {
  createSubscription?: Subscription
  constructor(
    private service: ArtistService,
    private toastr: ToastrService,
    private title: Title
  ) {
    this.title.setTitle(getAppTitle("Gestion - Ajouter un(e) artiste"))
  }

  ngOnDestroy(): void {
    this.createSubscription?.unsubscribe()
  }

  onSubmit(formData: any) {
    this.service.create(formData)
      .subscribe({
        next: () => {
          this.toastr.success("Artiste ajouté(e) avec succès", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => {
          console.log(err)
          this.toastr.success("Echec de l'ajout de l'artiste", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        }
      })
  }
}

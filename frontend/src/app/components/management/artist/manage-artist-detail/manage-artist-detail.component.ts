import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ArtistService } from 'src/app/services/artist/artist.service';
import { Artist } from 'src/app/models/artist.model';
import { Subscription, firstValueFrom } from 'rxjs'
import { ToastrService } from 'ngx-toastr';
import { Title } from '@angular/platform-browser';
import { getAppTitle } from 'src/app/config/app.config';

@Component({
  selector: 'app-manage-artist-detail',
  templateUrl: './manage-artist-detail.component.html',
  styleUrls: ['./manage-artist-detail.component.css']
})
export class ManageArtistDetailComponent implements OnDestroy, OnInit {
  artist!: Artist
  isLoading: boolean = true
  successMessage?: string
  updateSubscription?: Subscription
  constructor(
    private service: ArtistService,
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private title: Title
  ) { }

  ngOnDestroy(): void {
    this.updateSubscription?.unsubscribe()
  }

  async ngOnInit() {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    try {
      this.artist = await this.get(id)
      this.title.setTitle(getAppTitle("Gestion - Modifier un(e) artiste"))
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  get(id: number) {
    return firstValueFrom(this.service.get(id))
  }

  onSubmit(formData: any) {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    this.updateSubscription = this.service.update(id, formData)
      .subscribe({
        next: () => {
          this.toastr.success("Informations de l'artiste mis à jour avec succès", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => {
          console.log(err)
          this.toastr.error("Echec mise à jour des informations de l'artiste", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        }
      })
  }

}

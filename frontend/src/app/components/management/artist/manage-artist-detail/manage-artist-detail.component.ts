import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ArtistService } from 'src/app/_services/artist.service';
import { Artist } from 'src/app/models/Artist';
import { firstValueFrom } from 'rxjs'
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-manage-artist-detail',
  templateUrl: './manage-artist-detail.component.html',
  styleUrls: ['./manage-artist-detail.component.css']
})
export class ManageArtistDetailComponent {
  artist!: Artist
  isLoading: boolean = true
  successMessage?: string

  constructor(
    private service: ArtistService,
    private route: ActivatedRoute,
    private toastr: ToastrService
  ) { }

  async ngOnInit() {
    console.log(`Artist id : ${this.route.snapshot.paramMap.get('id')}`)
    let id = Number(this.route.snapshot.paramMap.get('id'))
    try {
      this.artist = await this.get(id)
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
    this.service.update(id, formData)
      .subscribe({
        next: () => {
          this.toastr.success("Informations de l'artiste mis à jour avec succès", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => console.log(err)
      })
  }

}

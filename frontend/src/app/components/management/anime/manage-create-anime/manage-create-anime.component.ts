import { Component, OnDestroy } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ToastrService } from 'ngx-toastr';
import { Subscription } from 'rxjs';
import { AnimeService } from 'src/app/_services/anime.service';

@Component({
  selector: 'app-manage-create-anime',
  templateUrl: './manage-create-anime.component.html',
  styleUrls: ['./manage-create-anime.component.css']
})
export class ManageCreateAnimeComponent implements OnDestroy {
  createSubscription?: Subscription
  constructor(
    private service: AnimeService,
    private toastr: ToastrService,
    private title: Title
  ) {

    this.title.setTitle("MyAniSongList - Gestion - Ajouter un anime")
  }
  ngOnDestroy(): void {
    this.createSubscription?.unsubscribe();
  }

  onSubmit(formData: any) {
    this.service.create(formData)
      .subscribe({
        next: () => {
          this.toastr.success("Animé ajouté avec succès", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => {
          console.log(err)
          this.toastr.error("Echec de l'ajout de l'anime", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        }
      })
  }

}


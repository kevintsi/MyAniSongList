import { Component, OnDestroy, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ToastrService } from 'ngx-toastr';
import { Subscription } from 'rxjs';
import { MusicService } from 'src/app/_services/music.service';

@Component({
  selector: 'app-manage-create-music',
  templateUrl: './manage-create-music.component.html',
  styleUrls: ['./manage-create-music.component.css']
})
export class ManageCreateMusicComponent implements OnDestroy {
  createSubscription?: Subscription

  constructor(
    private musicService: MusicService,
    private toastr: ToastrService,
    private title: Title
  ) {
    this.title.setTitle("MyAniSongList - Gestion - Ajouter une musique")
  }
  ngOnDestroy(): void {
    this.createSubscription?.unsubscribe();
  }


  onSubmit(formData: any) {
    this.createSubscription = this.musicService.create(formData)
      .subscribe({
        next: () => {
          this.toastr.success("Musique ajoutée avec succès", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => {
          console.log(err)
          this.toastr.error("Echec de l'ajout de la musique", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        }
      })
  }
}

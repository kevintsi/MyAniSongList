import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ToastrService } from 'ngx-toastr';
import { MusicService } from 'src/app/_services/music.service';

@Component({
  selector: 'app-manage-create-music',
  templateUrl: './manage-create-music.component.html',
  styleUrls: ['./manage-create-music.component.css']
})
export class ManageCreateMusicComponent {
  constructor(
    private music_service: MusicService,
    private toastr: ToastrService,
    private title: Title
  ) {
    this.title.setTitle("MyAniSongList - Gestion - Ajouter une musique")
  }


  onSubmit(formData: any) {
    console.log(formData)
    this.music_service.create(formData)
      .subscribe({
        next: () => {
          this.toastr.success("Musique ajoutée avec succès", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => console.log(err)
      })
  }
}

import { Component, OnInit } from '@angular/core';
import { MusicService } from 'src/app/_services/music.service';

@Component({
  selector: 'app-manage-create-music',
  templateUrl: './manage-create-music.component.html',
  styleUrls: ['./manage-create-music.component.css']
})
export class ManageCreateMusicComponent {

  constructor(
    private music_service: MusicService,
  ) { }


  onSubmit(formData: any) {
    console.log(formData)
    this.music_service.create(formData)
      .subscribe({
        next: () => {
          alert("Musique ajouté")
        },
        error: (err) => console.log(err)
      })
  }
}

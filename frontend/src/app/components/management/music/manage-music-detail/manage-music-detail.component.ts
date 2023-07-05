import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { MusicService } from 'src/app/_services/music.service';
import { Music } from 'src/app/models/Music';
@Component({
  selector: 'app-manage-music-detail',
  templateUrl: './manage-music-detail.component.html',
  styleUrls: ['./manage-music-detail.component.css']
})
export class ManageMusicDetailComponent {
  isLoading = true
  music!: Music
  constructor(
    private music_service: MusicService,
    private route: ActivatedRoute,
  ) { }

  async ngOnInit() {
    console.log(`Music id : ${this.route.snapshot.paramMap.get('id')}`)
    let id = Number(this.route.snapshot.paramMap.get('id'))
    try {
      this.music = await this.get(id)
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  get(id: number) {
    return firstValueFrom(this.music_service.get(id))
  }


  onSubmit(formData: any) {
    console.log(formData)
    let id = Number(this.route.snapshot.paramMap.get('id'))
    this.music_service.update(id, formData)
      .subscribe({
        next: () => {
          alert("Informations mises à jour")
        },
        error: (err) => console.log(err)
      })

  }


}


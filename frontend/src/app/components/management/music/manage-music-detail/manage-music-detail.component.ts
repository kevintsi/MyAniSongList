import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { ToastrService } from 'ngx-toastr';
import { firstValueFrom } from 'rxjs';
import { MusicService } from 'src/app/services/music/music.service';
import { getAppTitle } from 'src/app/config/app.config';
import { Music } from 'src/app/models/music.model';
@Component({
  selector: 'app-manage-music-detail',
  templateUrl: './manage-music-detail.component.html',
  styleUrls: ['./manage-music-detail.component.css']
})
export class ManageMusicDetailComponent implements OnInit {
  isLoading = true
  music!: Music

  constructor(
    private music_service: MusicService,
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private translateService: TranslateService,
    private title: Title
  ) { }

  async ngOnInit() {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    try {
      this.music = await this.get(id)
      this.title.setTitle(getAppTitle("Gestion - Modifier une musique"))
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  get(id: number) {
    return firstValueFrom(this.music_service.get(id, this.translateService.currentLang))
  }


  onSubmit(formData: any) {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    this.music_service.update(id, formData)
      .subscribe({
        next: () => {
          this.toastr.success("Informations de la musique mis à jour avec succès", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => {
          console.log(err)
          this.toastr.error("Echec mise à jour des information de la musique", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        }
      })

  }


}


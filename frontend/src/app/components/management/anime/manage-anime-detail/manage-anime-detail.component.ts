import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AnimeService } from 'src/app/_services/anime.service';
import { Anime } from 'src/app/models/Anime';
import { firstValueFrom, timeout } from 'rxjs'
import { ToastrService } from 'ngx-toastr';
import { Title } from '@angular/platform-browser';
@Component({
  selector: 'app-manage-anime-detail',
  templateUrl: './manage-anime-detail.component.html',
  styleUrls: ['./manage-anime-detail.component.css']
})
export class ManageAnimeDetailComponent {
  isLoading = true
  anime!: Anime

  constructor(
    private service: AnimeService,
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private title: Title
  ) { }

  async ngOnInit() {
    console.log(`Anime id : ${this.route.snapshot.paramMap.get('id')}`)
    let id = Number(this.route.snapshot.paramMap.get('id'))
    try {
      this.anime = await this.get(id)
      this.title.setTitle("MyAniSongList - Gestion - Modifier un anime")
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
    console.log(formData)
    this.service.update(id, formData)
      .subscribe({
        next: () => {
          this.toastr.success("Informations de l'animé mis à jour avec succès", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => console.log(err)
      })
  }

}

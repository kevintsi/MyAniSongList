import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AnimeService } from 'src/app/_services/anime.service';
import { Anime } from 'src/app/models/Anime';
import { firstValueFrom } from 'rxjs'
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
  ) { }

  async ngOnInit() {
    console.log(`Anime id : ${this.route.snapshot.paramMap.get('id')}`)
    let id = Number(this.route.snapshot.paramMap.get('id'))
    try {
      this.anime = await this.get(id)
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
          alert("Informations mises à jour")
        },
        error: (err) => console.log(err)
      })
  }

}

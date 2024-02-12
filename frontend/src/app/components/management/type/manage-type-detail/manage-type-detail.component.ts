import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AnimeService } from 'src/app/_services/anime.service';
import { Anime } from 'src/app/models/Anime';
import { Subscription, firstValueFrom } from 'rxjs'
import { ToastrService } from 'ngx-toastr';
import { Title } from '@angular/platform-browser';
import { Type } from 'src/app/models/Type';
import { TypeService } from 'src/app/_services/type.service';
@Component({
  selector: 'app-manage-type-detail',
  templateUrl: './manage-type-detail.component.html',
  styleUrls: ['./manage-type-detail.component.css']
})
export class ManageTypeDetailComponent implements OnInit, OnDestroy {
  isLoading = true
  type!: Type
  typeSubscription = new Subscription()

  constructor(
    private service: TypeService,
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private title: Title
  ) { }

  ngOnDestroy(): void {
    this.typeSubscription.unsubscribe()
  }

  async ngOnInit() {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    try {
      this.type = await this.get(id)
      this.title.setTitle("MyAniSongList - Gestion - Modifier un type")
    } catch (error) {
      console.log(error)
    } finally {
      this.isLoading = false
    }
  }

  get(id: number) {
    return firstValueFrom(this.service.get(id))
  }

  onSubmit(type: Type) {
    let id = Number(this.route.snapshot.paramMap.get('id'))
    this.typeSubscription = this.service.updateTranslation(id, type)
      .subscribe({
        next: () => {
          this.toastr.success("Informations du type mis à jour avec succès", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => {
          console.log(err)
          this.toastr.error("Echec de mise à jour des informations du type", 'Modification', {
            progressBar: true,
            timeOut: 3000
          })
        }
      })
  }

}

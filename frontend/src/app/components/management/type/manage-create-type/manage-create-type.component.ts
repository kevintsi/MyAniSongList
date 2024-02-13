import { Component, OnDestroy } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ToastrService } from 'ngx-toastr';
import { Subscription } from 'rxjs';
import { TypeService } from 'src/app/_services/type.service';
import { Type } from 'src/app/models/Type';

@Component({
  selector: 'app-manage-create-anime',
  templateUrl: './manage-create-type.component.html',
  styleUrls: ['./manage-create-type.component.css']
})
export class ManageCreateTypeComponent implements OnDestroy {
  createSubscription?: Subscription
  constructor(
    private service: TypeService,
    private toastr: ToastrService,
    private title: Title
  ) {

    this.title.setTitle("MyAniSongList - Gestion - Ajouter un type")
  }
  ngOnDestroy(): void {
    this.createSubscription?.unsubscribe();
  }

  onSubmit(form: any) {
    let type: Type = {
      name: form.name
    }
    this.service.add(type)
      .subscribe({
        next: () => {
          this.toastr.success("Type " + type.name + " ajouté avec succès", 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: (err) => {
          console.log(err)
          this.toastr.error("Echec de l'ajout du type " + type.name, 'Ajout', {
            progressBar: true,
            timeOut: 3000
          })
        }
      })
  }

}


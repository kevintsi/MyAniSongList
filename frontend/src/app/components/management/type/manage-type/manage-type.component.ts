import { Component, OnDestroy, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { Subscription, firstValueFrom } from 'rxjs';
import { TypeService } from 'src/app/_services/type.service';
import { Type } from 'src/app/models/Type';

@Component({
  selector: 'app-manage-type',
  templateUrl: './manage-type.component.html',
  styleUrls: ['./manage-type.component.css']
})
export class ManageTypeComponent implements OnInit, OnDestroy {
  isLoading = true
  types!: Array<Type>
  deleteSubscription?: Subscription

  constructor(private service: TypeService, private title: Title) {
    this.title.setTitle("MyAniSongList - Gestion - Types")
  }

  ngOnInit(): void {
    this.fetchData()
  }

  ngOnDestroy(): void {
    this.deleteSubscription?.unsubscribe();
  }


  async fetchData() {
    try {
      this.types = await this.fetchTypes()
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
    }
  }

  fetchTypes() {
    return firstValueFrom(this.service.getAll())
  }

  delete(selected: Type) {
    this.deleteSubscription = this.service.delete(selected).subscribe({
      next: () => {
        this.types = this.types?.filter(type => type.id != selected.id)
      },
      error: (err) => console.log(err.message)
    })
  }
}

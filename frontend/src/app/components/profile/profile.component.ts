import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { UserService } from 'src/app/services/user/user.service';
import { getAppTitle } from 'src/app/config/app.config';
import { Music } from 'src/app/models/music.model';
import { User } from 'src/app/models/user.model';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  isLoading: boolean = true
  userInfo!: User
  favorites!: Music[]

  constructor(private userService: UserService, private route: ActivatedRoute, private title: Title) { }

  ngOnInit(): void {
    this.fetchData()
  }

  async fetchData() {
    try {
      let id = Number(this.route.snapshot.paramMap.get("id"))
      this.userInfo = await this.fetchUser(id)
      this.favorites = await this.fetchFavorites(id)
      this.title.setTitle(getAppTitle("Profil - " + this.userInfo.username))
    } catch (error) {
      console.log(error)
    }
    finally {
      this.isLoading = false
    }
  }

  async fetchUser(id: number) {
    return firstValueFrom(this.userService.get(id))
  }
  async fetchFavorites(id: number) {
    return firstValueFrom(this.userService.getFavorites(id))
  }

}

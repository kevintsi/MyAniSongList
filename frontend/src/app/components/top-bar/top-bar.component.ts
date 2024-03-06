import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../../_services/auth.service';
import { NavigationEnd, Router } from '@angular/router';
import { MusicService } from 'src/app/_services/music.service';
import { ArtistService } from 'src/app/_services/artist.service';
import { AnimeService } from 'src/app/_services/anime.service';
import { Subscription, firstValueFrom } from 'rxjs';
import { TokenService } from 'src/app/_services/token.service';
import { UserService } from 'src/app/_services/user.service';
import { TranslateService } from '@ngx-translate/core';
import { AppLanguages } from 'src/app/config/lang';
import { AppLanguage } from 'src/app/interfaces/AppLanguage';
import { LANGUAGE_STORAGE_KEY } from 'src/app/config/storage';

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})


export class TopBarComponent implements OnInit, OnDestroy {
  isLoading = false
  isMenuOpen: boolean = false;
  isSearchBarOpen: boolean = false
  category: string = "animes"
  result_search?: any[] = []
  user_pfp?: string = ""
  username?: string = ""
  languages = AppLanguages


  routerSubscription?: Subscription
  searchSubscription?: Subscription
  logOutSubscription?: Subscription

  constructor(
    private authService: AuthService,
    private musiService: MusicService,
    private artistService: ArtistService,
    private userService: UserService,
    private animeService: AnimeService,
    private router: Router,
    private tokenService: TokenService,
    private translateService: TranslateService
  ) {
  }

  ngOnInit() {
    this.routerSubscription = this.router.events.subscribe({
      next: async (ev) => {
        if (ev instanceof NavigationEnd) {
          this.isMenuOpen = false
          this.isSearchBarOpen = false
          if (!!this.tokenService.getToken()) {
            let userInfo = await this.getProfile()
            this.user_pfp = userInfo.profile_picture
            this.username = userInfo.username
          }
        }
      }
    })

  }

  ngOnDestroy() {
    this.routerSubscription?.unsubscribe();
    this.searchSubscription?.unsubscribe();
    this.logOutSubscription?.unsubscribe();
  }

  onLanguageSelect(lang: AppLanguage) {
    this.translateService.use(lang.id)
    localStorage.setItem(LANGUAGE_STORAGE_KEY, lang.id)
  }

  performSearch(searchTerm: string) {
    this.isLoading = true
    if (!searchTerm) {
      this.result_search = []
      this.isLoading = false
      return
    }
    switch (this.category) {
      case "animes": {
        this.searchSubscription = this.animeService.search(searchTerm, this.translateService.currentLang).subscribe({
          next: (anime) => {
            this.result_search = anime.items
          },
          error: (err) => console.error(err.message),
          complete: () => this.isLoading = false
        })
      }
        break
      case "musics": {
        this.searchSubscription = this.musiService.search(searchTerm).subscribe({
          next: (music) => {
            this.result_search = music.items
          },
          error: (err) => console.error(err.message),
          complete: () => this.isLoading = false
        })
      }
        break
      case "artists": {
        this.searchSubscription = this.artistService.search(searchTerm).subscribe({
          next: (artist) => {
            this.result_search = artist.items
          },
          error: (err) => console.error(err.message),
          complete: () => this.isLoading = false
        })
      }
        break
      case "profile": {
        this.searchSubscription = this.userService.search(searchTerm).subscribe({
          next: (users) => {
            this.result_search = users.items
          },
          error: (err) => console.error(err.message),
          complete: () => this.isLoading = false
        })
      }
        break
    }
  }

  goToItem(id: string) {
    this.router.navigate(["/", this.category, id]).then((ok) => {
      if (ok) {
        this.isSearchBarOpen = false
        this.result_search = []
        window.location.reload()
      }
    })
  }

  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
    this.isSearchBarOpen = false;
  }

  toggleSearchBar() {
    this.isSearchBarOpen = !this.isSearchBarOpen;
    this.isMenuOpen = false;
  }


  isLoggedIn() {
    return this.authService.isLoggedIn()
  }

  isManager() {
    return this.authService.isManager()
  }

  logout() {
    this.logOutSubscription = this.authService.logout().subscribe({
      next: () => {
        this.router.navigate(["/login"])
      },
      error: (err) => console.log(err),
      complete: () => this.tokenService.clean()
    })
  }

  getProfile() {
    return firstValueFrom(this.authService.get())
  }

}

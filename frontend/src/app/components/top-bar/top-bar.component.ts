import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../_services/auth.service';
import { NavigationEnd, Router } from '@angular/router';
import { MusicService } from 'src/app/_services/music.service';
import { ArtistService } from 'src/app/_services/artist.service';
import { AnimeService } from 'src/app/_services/anime.service';
import { Subject } from 'rxjs';
import { TokenService } from 'src/app/_services/token.service';
import jwtDecode from 'jwt-decode';

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})


export class TopBarComponent implements OnInit {
  isMenuOpen: boolean = false;
  isSearchBarOpen: boolean = false
  category: string = "animes"
  result_search?: any[] = []
  user_pfp: string = ""

  constructor(
    private authService: AuthService,
    private musiService: MusicService,
    private artistService: ArtistService,
    private animeService: AnimeService,
    private router: Router,
    private tokenService: TokenService
  ) {
  }

  ngOnInit() {
    this.router.events.subscribe({
      next: (ev) => {
        if (ev instanceof NavigationEnd) {
          this.isMenuOpen = false
          this.isSearchBarOpen = false
        }
      }
    });
    if (!!this.tokenService.getToken()) {
      let decodedToken: any = jwtDecode(String(this.tokenService.getToken()))
      this.user_pfp = decodedToken.sub.profile_picture
    }
  }

  performSearch(searchTerm: string) {
    console.log("New search : ", this.category)
    console.log("Term : " + !searchTerm)
    if (!searchTerm) {
      this.result_search = []
      return
    }
    switch (this.category) {
      case "animes": {
        this.animeService.search(searchTerm).subscribe({
          next: (anime) => {
            this.result_search = anime.items
          },
          error: (err) => console.error(err.message)
        })
      }
        break
      case "musics": {
        this.musiService.search(searchTerm).subscribe({
          next: (music) => {
            this.result_search = music.items
          },
          error: (err) => console.error(err.message)
        })
      }
        break
      case "artists": {
        this.artistService.search(searchTerm).subscribe({
          next: (artist) => {
            this.result_search = artist.items
          },
          error: (err) => console.error(err.message)
        })
      }
        break
    }
  }

  goToItem(id: string) {
    console.log("Id : ", id)
    this.router.navigate(["/", this.category, id]).then((ok) => {
      if (ok) {
        this.isSearchBarOpen = false
        this.result_search = []
        window.location.reload()
      }
    })
  }

  toggleMenu() {
    console.log('Menu toggled')
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
    console.log("Logout function called")
    this.authService.logout().subscribe({
      next: () => {
        this.tokenService.clean()
        this.router.navigate(["/login"])
      },
      error: (err) => console.log(err),
      complete: () => this.tokenService.clean()
    })
  }

}

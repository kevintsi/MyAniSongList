import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';
import { StorageService } from '../../_services/storage.service';
import { MusicService } from 'src/app/_services/music.service';
import { ArtistService } from 'src/app/_services/artist.service';
import { AnimeService } from 'src/app/_services/anime.service';
import { Observable, Subject, debounceTime, distinctUntilChanged, switchMap, takeUntil } from 'rxjs';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})


export class TopBarComponent {
  isMenuOpen: boolean = false;
  isSearchBarOpen: boolean = false
  category: string = "animes"
  result_search?: any[] = []
  searchQuery: string = ""
  searchQueryChanged: Subject<string> = new Subject<string>();

  constructor(
    private authService: AuthService,
    private music_service: MusicService,
    private artist_service: ArtistService,
    private anime_service: AnimeService,
    private router: Router,
    private storageService: StorageService
  ) {
  }

  performSearch(searchTerm: string) {
    console.log("New search : ", this.category)
    switch (this.category) {
      case "animes": {
        this.anime_service.search(searchTerm).subscribe({
          next: (anime) => {
            this.result_search = anime
          },
          error: (err) => console.error(err.message)
        })
      }
        break
      // case "musics": {
      //   this.music_service.search(query)
      // }
      // break
      case "artists": {
        this.artist_service.search(searchTerm).subscribe({
          next: (artist) => {
            this.result_search = artist
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

  onSearchQueryChange() {
    this.searchQueryChanged.next(this.searchQuery);
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

  logout() {
    console.log("Logout function called")
    this.authService.logout().subscribe({
      next: () => {
        this.storageService.clean()
        this.router.navigate(["/"])
      },
      error: (err) => console.log(err)
    })
  }

}

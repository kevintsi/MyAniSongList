import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';
import { StorageService } from '../../_services/storage.service';
import { MusicService } from 'src/app/_services/music.service';
import { ArtistService } from 'src/app/_services/artist.service';
import { AnimeService } from 'src/app/_services/anime.service';
import { Observable, Subject, debounceTime, distinctUntilChanged, switchMap } from 'rxjs';

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})


export class TopBarComponent implements OnInit {
  isMenuOpen: boolean = false;
  isSearchBarOpen: boolean = false
  category: string = "animes"
  result_search?: Observable<any[]>
  private input_term = new Subject<string>()

  constructor(
    private authService: AuthService,
    private music_service: MusicService,
    private artist_service: ArtistService,
    private anime_service: AnimeService,
    private router: Router,
    private storageService: StorageService
  ) { }

  ngOnInit(): void {
    this.input_term.pipe(
      debounceTime(500),
      distinctUntilChanged(),
    ).subscribe((query: string) => {
      console.log("New search : ", this.category)
      switch (this.category) {
        case "animes": {
          this.result_search = this.anime_service.search(query)
        }
          break
        // case "musics": {
        //   this.music_service.search(query)
        // }
        // break
        case "artists": {
          this.result_search = this.artist_service.search(query)
        }
          break
      }
    })
  }

  get_value(event: Event): string {
    return (event.target as HTMLInputElement).value;
  }

  get_list(term: string) {
    this.input_term.next(term)

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

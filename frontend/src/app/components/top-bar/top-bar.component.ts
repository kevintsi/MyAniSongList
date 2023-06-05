import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';
import { StorageService } from '../../_services/storage.service';

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})


export class TopBarComponent implements OnInit {
  isMenuOpen: boolean = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private storageService: StorageService
  ) { }

  ngOnInit(): void {
    console.log("ngOnInit TopBarComponent")
  }

  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
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

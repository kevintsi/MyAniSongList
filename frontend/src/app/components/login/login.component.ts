import { Component, OnInit } from '@angular/core';
import { FormBuilder } from "@angular/forms"
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';
import { User } from '../../models/User';
import { StorageService } from '../../_services/storage.service';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginForm = this.formBuilder.group({
    username: '',
    password: ''
  })
  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private storageService: StorageService,
    private router: Router,
    private title: Title
  ) {
    console.log("In constructor");
  }
  ngOnInit(): void {
    this.title.setTitle(this.title.getTitle() + " - Se connecter")
  }

  onSubmit() {
    console.log("onSubmit")
    console.log(this.loginForm.value)
    const { username, password } = this.loginForm.value

    if (username?.length == 0 || password?.length == 0) return;

    let user: User = {
      username: username?.toString(),
      password: password?.toString()
    }

    this.authService.login(user)
      .subscribe({
        next: data => {
          this.storageService.saveUser(data)
          this.router.navigateByUrl("/")
        },
        error: err => {
          console.log(err)
        }
      })
  }
}

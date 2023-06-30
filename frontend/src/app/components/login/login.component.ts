import { Component, OnInit } from '@angular/core';
import { FormBuilder } from "@angular/forms"
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';
import { User } from '../../models/User';
import { StorageService } from '../../_services/storage.service';
import { Title } from '@angular/platform-browser';
import { TokenService } from 'src/app/_services/token.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginForm = this.formBuilder.group({
    email: '',
    password: ''
  })
  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private tokenService: TokenService,
    private router: Router,
    private title: Title
  ) {
    console.log("In constructor");
  }
  ngOnInit(): void {
    this.title.setTitle("Se connecter")
  }

  onSubmit() {
    console.log("onSubmit")
    console.log(this.loginForm.value)
    const { email, password } = this.loginForm.value

    if (email?.length == 0 || password?.length == 0) return;

    let user: User = {
      email: email?.toString(),
      password: password?.toString()
    }

    this.authService.login(user)
      .subscribe({
        next: data => {
          this.tokenService.setToken(data)
          this.router.navigateByUrl("/")
        },
        error: err => {
          console.log(err)
        }
      })
  }
}

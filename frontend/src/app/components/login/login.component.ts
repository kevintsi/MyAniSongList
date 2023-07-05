import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, Validators } from "@angular/forms"
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';
import { User } from '../../models/User';
import { Title } from '@angular/platform-browser';
import { TokenService } from 'src/app/_services/token.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginForm = this.formBuilder.group({
    email: new FormControl("", [Validators.email, Validators.required]),
    password: new FormControl("", [Validators.required]),
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

    if (this.loginForm.valid) {
      const { email, password } = this.loginForm.value
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
}

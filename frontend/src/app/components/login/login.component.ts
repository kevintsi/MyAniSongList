import { Component } from '@angular/core';
import { FormBuilder, FormControl, Validators } from "@angular/forms"
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';
import { User } from '../../models/User';
import { TokenService } from 'src/app/_services/token.service';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  isLoading: boolean = false
  errorLogin?: string
  loginForm = this.formBuilder.group({
    email: new FormControl("", [Validators.email, Validators.required]),
    password: new FormControl("", [Validators.required]),
  })
  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private tokenService: TokenService,
    private router: Router,
  ) {
    console.log("In constructor");
  }

  async onSubmit() {
    console.log("onSubmit")
    if (this.loginForm.valid) {
      const { email, password } = this.loginForm.value
      let user: User = {
        email: email?.toString(),
        password: password?.toString()
      }

      try {
        this.isLoading = true
        let token = await this.loggingIn(user)
        this.tokenService.setToken(token)
        this.router.navigateByUrl("/")
      } catch (error) {
        console.log(error)
        this.errorLogin = "Email ou mot de passe incorrect"
      } finally {
        this.isLoading = false
      }
    }
  }
  loggingIn(user: User) {
    return firstValueFrom(this.authService.login(user))
  }
}

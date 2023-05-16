import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { User } from '../../models/User';
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})


export class RegistrationComponent {

  registrationForm = this.formBuilder.group({
    username: "",
    email: "",
    password: "",
    confirmPassword: ""
  });

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    console.log("In constructor");
  }

  onSubmit(): void {
    console.log("onSubmit")
    console.log(this.registrationForm.value)
    const { username, email, password, confirmPassword } = this.registrationForm.value

    if (username?.length == 0 || password?.length == 0 || email?.length == 0 || confirmPassword?.length == 0) return;
    if (password != confirmPassword) return;

    let user: User = {
      username: username?.toString(),
      email: email?.toString(),
      password: password?.toString(),
    }

    this.authService.register(user)
      .subscribe({
        next: () => {
          this.router.navigateByUrl("/login")
        },
        error: err => {
          console.log(err)
        }
      })
  }

}

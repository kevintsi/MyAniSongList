import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { User } from '../../models/User';
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})


export class RegistrationComponent implements OnInit {

  registrationForm = this.formBuilder.group({
    username: new FormControl("", [Validators.required, Validators.minLength(4)]),
    email: new FormControl("", [Validators.email, Validators.required]),
    password: new FormControl("", [Validators.required]),
    confirmPassword: new FormControl("", [Validators.required])
  });

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private title: Title
  ) { }

  ngOnInit(): void {
    this.title.setTitle("MyAniSongList - S'incrire")
  }

  onSubmit(): void {
    console.log("onSubmit")
    const { username, email, password, confirmPassword } = this.registrationForm.value
    if (this.registrationForm.valid && password === confirmPassword) {
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
}

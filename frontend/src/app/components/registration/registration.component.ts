import { Component, OnDestroy, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { User } from '../../models/user.model';
import { AuthService } from '../../services/auth/auth.service';
import { Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { passwordMatchingValidator } from 'src/app/utils/utils';
import { ToastrService } from 'ngx-toastr';
import { Subscription } from 'rxjs';
import { getAppTitle } from 'src/app/config/app.config';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})


export class RegistrationComponent implements OnInit, OnDestroy {

  registrationForm = this.formBuilder.group({
    username: new FormControl("", [Validators.required, Validators.minLength(4)]),
    email: new FormControl("", [Validators.email, Validators.required]),
    password: new FormControl("", [Validators.required]),
    confirmPassword: new FormControl("", [Validators.required])
  }, { validators: passwordMatchingValidator });

  registerSubscription?: Subscription

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private title: Title,
    private toastr: ToastrService
  ) { }
  ngOnDestroy(): void {
    this.registerSubscription?.unsubscribe()
  }

  ngOnInit(): void {
    this.title.setTitle(getAppTitle("S'incrire"))
  }

  onSubmit(): void {
    const { username, email, password, confirmPassword } = this.registrationForm.value
    if (this.registrationForm.valid && password === confirmPassword) {
      let user: User = {
        username: username?.toString(),
        email: email?.toString(),
        password: password?.toString(),
      }

      this.registerSubscription = this.authService.register(user)
        .subscribe({
          next: () => {
            this.toastr.success("Inscription réussie", 'Ajout', {
              progressBar: true,
              timeOut: 3000
            })
            this.router.navigateByUrl("/login")
          },
          error: err => {
            console.log(err)
            this.toastr.error("Inscription echouée", 'Ajout', {
              progressBar: true,
              timeOut: 3000
            })
          }
        })
    }
  }
}

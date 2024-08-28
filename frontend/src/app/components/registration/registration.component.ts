import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { User } from '../../models/user.model';
import { AuthService } from '../../services/auth/auth.service';
import { Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { passwordMatchingValidator } from 'src/app/utils/utils';
import { ToastrService } from 'ngx-toastr';
import { Subscription } from 'rxjs';
import { getAppTitle } from 'src/app/config/app.config';
import { HttpErrorResponse } from '@angular/common/http';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})


export class RegistrationComponent implements OnInit, OnDestroy {


  isLoading: boolean = false
  alreadyExistsError: boolean = false
  systemError: boolean = false

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
    private translateService: TranslateService,
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

    if (this.registrationForm.valid) {
      this.isLoading = true
      const { username, email, password } = this.registrationForm.value

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
          error: (err: HttpErrorResponse) => {
            switch (err.status) {
              case 409:
                this.alreadyExistsError = true
                break
              default:
                this.systemError = true
            }
            this.toastr.error("Inscription echouée", 'Ajout', {
              progressBar: true,
              timeOut: 3000
            })

            this.isLoading = false
          },
          complete: () => this.isLoading = false
        })
    }
  }
}

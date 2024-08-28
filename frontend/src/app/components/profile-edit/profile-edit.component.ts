import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { User } from '../../models/user.model';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { Title } from '@angular/platform-browser';
import { ToastrService } from 'ngx-toastr';
import { passwordMatchingValidator } from 'src/app/utils/utils';
import { Subscription } from 'rxjs';
import { getAppTitle } from 'src/app/config/app.config';
import { HttpErrorResponse } from '@angular/common/http';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-profile-edit',
  templateUrl: './profile-edit.component.html',
  styleUrls: ['./profile-edit.component.css']
})

export class ProfileEditComponent implements OnInit, OnDestroy {
  isLoading: boolean = true
  alreadyExistsError: boolean = false
  systemError: boolean = false
  updateForm = this.formBuilder.group({
    username: new FormControl("", [Validators.required, Validators.minLength(4)]),
    email: new FormControl("", [Validators.email, Validators.required]),
    password: new FormControl(""),
    confirmPassword: new FormControl("")
  }, { validators: [passwordMatchingValidator] });

  previewImage?: any
  file: any

  authSubscription?: Subscription
  updateSubscription?: Subscription

  constructor(
    private authService: AuthService,
    private formBuilder: FormBuilder,
    private translateService: TranslateService,
    private title: Title,
    private toastr: ToastrService

  ) {
    this.title.setTitle(getAppTitle("Mon profil"))
  }
  ngOnDestroy(): void {
    this.authSubscription?.unsubscribe();
    this.updateSubscription?.unsubscribe();
  }



  ngOnInit(): void {
    this.authSubscription = this.authService.get().subscribe({
      next: (user) => {
        this.updateForm.patchValue({
          username: user.username,
          email: user.email,
        })

        this.previewImage = user.profile_picture
      },
      error: (err) => { console.error(err.message) },
      complete: () => this.isLoading = false
    })
  }


  onSubmit(): void {
    console.log(this.updateForm)
    if (this.updateForm.valid) {
      const { username, email, password, confirmPassword } = this.updateForm.value

      let user: User;

      if ((password && confirmPassword) && (password?.length > 0 && confirmPassword?.length > 0)) {
        user = {
          username: username?.toString(),
          email: email?.toString(),
          password: password?.toString(),
        }
      } else {
        user = {
          username: username?.toString(),
          email: email?.toString()
        }
      }



      this.updateSubscription = this.authService.update(user, this.file)
        .subscribe({
          next: () => {
            this.toastr.success("Mise à jour du profil", 'Update', {
              progressBar: true,
              timeOut: 3000
            })
          },
          error: (err: HttpErrorResponse) => {
            console.log(err)
            switch (err.status) {
              case 409:
                this.alreadyExistsError = true
                break
              default:
                this.systemError = true
            }
            this.toastr.error("Echec mise à jour du profil", 'Update', {
              progressBar: true,
              timeOut: 3000
            })
          }
        })
    }

  }

  processFile(imageInput: any) {
    this.file = imageInput.files[0];
    if (this.file) {
      if (["image/jpeg", "image/png", "image/svg+xml"].includes(this.file.type)) {
        let fileReader = new FileReader();
        fileReader.readAsDataURL(this.file);
        fileReader.addEventListener('load', event => {
          this.previewImage = event.target?.result
        })
      }
    }
  }

}

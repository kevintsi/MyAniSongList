import { Component } from '@angular/core';
import { AuthService } from '../../_services/auth.service';
import { User } from '../../models/User';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { Title } from '@angular/platform-browser';
import { ToastrService } from 'ngx-toastr';
import { passwordMatchingValidator } from 'src/app/utils/utils';

@Component({
  selector: 'app-profile-edit',
  templateUrl: './profile-edit.component.html',
  styleUrls: ['./profile-edit.component.css']
})

export class ProfileEditComponent {
  isLoading: boolean = true
  updateForm = this.formBuilder.group({
    username: new FormControl("", [Validators.required]),
    email: new FormControl("", [Validators.email, Validators.required]),
    password: new FormControl("", [Validators.required]),
    confirmPassword: new FormControl("", [Validators.required])
  }, { validators: passwordMatchingValidator });

  previewImage?: any
  file: any

  constructor(
    private authService: AuthService,
    private formBuilder: FormBuilder,
    private title: Title,
    private toastr: ToastrService

  ) {
    this.title.setTitle("MyAniSongList - Mon profil")
  }



  ngOnInit(): void {
    this.authService.get().subscribe({
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
    console.log("onSubmit")
    console.log(this.updateForm.value)
    const { username, email, password, confirmPassword } = this.updateForm.value

    if (username?.length == 0 || password?.length == 0 || email?.length == 0 || confirmPassword?.length == 0) return;
    if (password != confirmPassword) return;

    let user: User = {
      username: username?.toString(),
      email: email?.toString(),
      password: password?.toString(),
    }

    this.authService.update(user, this.file)
      .subscribe({
        next: () => {
          this.toastr.success("Mise à jour du profil", 'Update', {
            progressBar: true,
            timeOut: 3000
          })
        },
        error: err => {
          console.log(err)
        }
      })
  }

  processFile(imageInput: any) {
    this.file = imageInput.files[0];
    if (this.file) {
      if (["image/jpeg", "image/png", "image/svg+xml"].includes(this.file.type)) {
        console.log("Image selected : ", this.file)
        let fileReader = new FileReader();
        fileReader.readAsDataURL(this.file);
        fileReader.addEventListener('load', event => {
          this.previewImage = event.target?.result
        })
      }
    }
  }

}

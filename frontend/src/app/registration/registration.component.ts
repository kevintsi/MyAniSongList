import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';

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

  constructor(private formBuilder: FormBuilder) {
    console.log("In constructor");
  }

  onSubmit(): void {
    console.log("onSubmit")
    console.log(this.registrationForm.value)
  }

}

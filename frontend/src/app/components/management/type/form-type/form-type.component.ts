import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Type } from 'src/app/models/Type';

@Component({
  selector: 'app-form-type',
  templateUrl: './form-type.component.html',
  styleUrls: ['./form-type.component.css']
})
export class FormTypeComponent {
  @Input() isUpdate!: boolean; // Indicates if it's an update operation
  @Input() type!: Type; // Existing data for update operation

  @Output() submitForm: EventEmitter<any> = new EventEmitter<any>();

  typeNameControl!: FormControl

  constructor() { }

  ngOnInit() {
    this.initForm();
    if (this.isUpdate) {
      this.populateForm();
    }
  }

  initForm() {
    this.typeNameControl = new FormControl("", [Validators.required])
  }

  populateForm() {
    this.typeNameControl.patchValue(this.type.name)
  }

  onSubmit() {
    if (this.typeNameControl.valid) {
      let type: Type = {
        name: this.typeNameControl.value
      }
      this.submitForm.emit(type);
    }
  }
}

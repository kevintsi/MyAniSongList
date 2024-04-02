import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { Language } from 'src/app/models/language.model';
@Component({
  selector: 'app-form-language',
  templateUrl: './form-language.component.html',
  styleUrls: ['./form-language.component.css']
})
export class FormLanguageComponent implements OnInit {
  @Input() isUpdate!: boolean; // Indicates if it's an update operation
  @Input() language!: Language; // Existing data for update operation

  @Output() submitForm: EventEmitter<any> = new EventEmitter<any>();

  langName!: FormControl;

  constructor() { }

  ngOnInit() {
    this.initForm();
    if (this.isUpdate) {
      this.populateForm();
    }
  }

  initForm() {
    this.langName = new FormControl("", [Validators.required])
  }

  populateForm() {
    this.langName.patchValue(this.language.code)
  }

  onSubmit() {
    if (this.langName.valid) {
      let lang: Language = {
        code: this.langName.value
      }
      this.submitForm.emit(lang);
    }
  }


}

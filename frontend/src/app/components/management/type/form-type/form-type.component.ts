import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core';
import { firstValueFrom } from 'rxjs';
import { TypeService } from 'src/app/_services/type.service';
import { Language } from 'src/app/models/Language';
import { Type } from 'src/app/models/Type';

@Component({
  selector: 'app-form-type',
  templateUrl: './form-type.component.html',
  styleUrls: ['./form-type.component.css']
})
export class FormTypeComponent {
  @Input() isUpdate!: boolean; // Indicates if it's an update operation
  @Input() type!: Type; // Existing data for update operation
  @Input() languagesType?: Language[]
  @Input() languages?: Language[]

  @Output() submitForm: EventEmitter<any> = new EventEmitter<any>();

  formTypeGroup!: FormGroup

  constructor(
    private service: TypeService,
    private translateService: TranslateService,
    private formBuilder: FormBuilder
  ) { }

  ngOnInit() {
    this.initForm();
    if (this.isUpdate) {
      this.populateForm();
    }
  }

  async fetchData() {
    try {
      this.type = await this.get(parseInt(String(this.type.id)), this.formTypeGroup.get("language")?.value)
      this.formTypeGroup.patchValue({
        name: this.type.name
      })
    } catch (error) {
      console.log(error)
    }
  }

  get(id: number, lang: String) {
    return firstValueFrom(this.service.get(id, lang))
  }

  initForm() {
    this.formTypeGroup = this.formBuilder.group({
      name: new FormControl("", [Validators.required])
    })
  }

  populateForm() {
    this.formTypeGroup.addControl("language", new FormControl(this.translateService.currentLang, [Validators.required]))
    this.formTypeGroup.patchValue({
      name: this.type.name
    })
  }

  onChange(ev: Event) {
    let lang_code: string = (ev.target as HTMLSelectElement).value
    console.log("Change : ", lang_code)
    this.formTypeGroup.patchValue({
      language: lang_code
    })
    this.fetchData()
  }

  onSubmit() {
    if (this.formTypeGroup.valid) {
      this.submitForm.emit(this.formTypeGroup.value);
    }
  }
}

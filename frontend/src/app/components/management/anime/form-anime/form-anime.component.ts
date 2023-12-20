import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Anime } from 'src/app/models/Anime';

@Component({
  selector: 'app-form-anime',
  templateUrl: './form-anime.component.html',
  styleUrls: ['./form-anime.component.css']
})
export class FormAnimeComponent {
  @Input() isUpdate!: boolean; // Indicates if it's an update operation
  @Input() anime!: Anime; // Existing data for update operation

  @Output() submitForm: EventEmitter<any> = new EventEmitter<any>();

  form!: FormGroup;
  previewImage?: any = null

  constructor(private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.initForm();
    if (this.isUpdate) {
      this.populateForm();
    }
  }

  initForm() {
    this.form = this.formBuilder.group({
      name: new FormControl("", [Validators.required]),
      description: new FormControl("", [Validators.required]),
      poster_img: new FormControl(null, [this.isUpdate ? Validators.nullValidator : Validators.required])
    });
  }

  populateForm() {
    this.form.patchValue({
      name: this.anime.name,
      description: this.anime.description
    });

    this.previewImage = this.anime.poster_img
  }

  onSubmit() {
    if (this.form.valid) {
      const formData = this.form.value;
      this.submitForm.emit(formData);
    }
  }

  processFile(imageInput: any) {
    const file = imageInput.files[0];
    if (file) {
      if (["image/jpeg", "image/png", "image/svg+xml"].includes(file.type)) {
        this.form.patchValue({
          poster_img: file
        })

        this.previewImage = URL.createObjectURL(file)
      }
    }
  }
}
